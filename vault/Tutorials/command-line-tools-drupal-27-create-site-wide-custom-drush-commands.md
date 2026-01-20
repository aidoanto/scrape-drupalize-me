---
title: "Create Site-Wide Custom Drush Commands"
url: "https://drupalize.me/tutorial/create-site-wide-custom-drush-commands?p=2593"
guide: "[[command-line-tools-drupal]]"
order: 27
---

# Create Site-Wide Custom Drush Commands

## Content

When you manage many Drupal websites, you may perform repetitive tasks that are common across all of your sites. In our experience, this usually relates to having a personal preference for how certain tasks are accomplished. For example, maybe you like to make backups of the database and files in a specific way before testing upgrades, or you have a set of scripts for running scans of core web vitals. Although these tasks can be bundled into a custom module, it could be useful to create a site-wide Drush command instead. Site-wide commands can be installed with Composer, managed in a separate Git repository, and act as a project dependency. This way they are easy to maintain through a separate upstream. Changes to this code will be reflected on all the sites where it's used.

In this tutorial we'll:

- Declare a custom site-wide Drush command
- Demonstrate how to use Composer to manage a package that contains a Drush command

By the end of this tutorial you'll be able to create a site-wide Drush command and manage the code with Git and Composer.

## Goal

Create a site-wide Drush command to check the public files directory, and then display its size and the number of files it contains.

## Prerequisites

- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)
- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)
- [Overview: Creating Your Own Custom Drush Commands](https://drupalize.me/tutorial/overview-creating-your-own-custom-drush-commands)

## Create a Drush command to display directory information

The goal is to create a new Drush command that will list the number of files in the project's public files directory and the total size of all those files. Rather than putting the code for the command into a custom module, we'll create a non-module Composer package that can be installed on any Drupal site.

The output of the command may look something like below:

```
drush get-files-size

> The number of files is 2, and the size of the public files directory is: 156M.
```

### Create a command file

Site-wide commands reside inside the *drush/Commands* folder in the root directory of a Drupal project. These commands are not bundled with a Drupal module, but because they are in a location that Drush knows to look for them, they'll still work. Site-wide commands cannot use Drush's dependency injection system, so they don't need a *drush.services.yml* file or a *composer.json* file. The only file a site-wide Drush command needs is the Drush command class file.

In the root of your Drupal directory, create the file *drush/Commands/FilesDirectoryCommands.php*. Your directory structure may look like the following:

```
├── composer.json
├── drush
│   ├── Commands
│   │   ├── FilesDirectoryCommands.php
│   │
├── web (Drupal code)
```

Add the following code to the new file:

```
<?php

namespace Drush\Commands;

use Drush\Attributes as CLI;
use Drush\Commands\AutowireTrait;
use Drush\Commands\DrushCommands;

final class FilesDirectoryCommands extends DrushCommands {

  use AutowireTrait;

  /**
   * Command that returns info about the public files directory.
   */
  #[CLI\Command(name: 'get-files-size', aliases: ['gfs'])]
  #[CLI\Usage(name: 'get-files-size', description: 'Returns size of the public files directory and number of files')]
  public function getFilesSize() {
    $this->logger()->success(dt('Achievement unlocked.'));
  }

}
```

The command class needs to be in the `Drush\Commands` namespace in order to be discovered. The annotation of the command is exactly the same as for a custom Drush command defined in a module. If you need a refresher on this topic, please refer to [Create a Custom Drush Command](https://drupalize.me/tutorial/create-custom-drush-command).

### Test the new command

In the command line, run `drush cr -y` to clear Drupal's cache. and `drush cc drush` to clear Drush's cache. This will ensure Drush discovers your newly added command file. Then run `drush list` and you should see the new command under the `_global` category.

Run the command with `drush get-files-size` and you should see an *Achievement unlocked.* message.

Example:

```
$ drush get-files-size
 [success] Achievement unlocked.
```

Now that we know Drush can find our command, we can update the code.

### Update the command logic

We need to read the public files directory, find the number of files in it and all enclosed subdirectories, and calculate the total size of those files.

Here's what the updated code looks like:

```
<?php

namespace Drush\Commands;

use Drupal\Core\File\FileSystemInterface;
use Drush\Attributes as CLI;
use Drush\Boot\DrupalBootLevels;
use Drush\Commands\AutowireTrait;
use Drush\Commands\DrushCommands;

final class FilesDirectoryCommands extends DrushCommands {

  use AutowireTrait;

  /**
   * Constructs a FilesDirectoryCommands object.
   */
  public function __construct(
    private readonly FileSystemInterface $fileSystem,
  ) {
    parent::__construct();
  }

  /**
   * Command that returns info about the public files directory.
   */
  #[CLI\Command(name: 'get-files-size', aliases: ['gfs'])]
  #[CLI\Usage(name: 'get-files-size', description: 'Returns size of the public files directory and number of files')]
  #[CLI\Bootstrap(level: DrupalBootLevels::FULL)]
  public function getFilesSize() {
    $path = $this->fileSystem->realpath('public://');
    $filesize = exec('du -sh ' . $path);
    $fi = new \FilesystemIterator(__DIR__, \FilesystemIterator::SKIP_DOTS);
    $num_files = iterator_count($fi);
    $this->logger()->success(dt('The number of files is ' . $num_files . ', and the size of the public files directory is: ' . $filesize));
  }

}
```

In the code above we use Drupal's `FileSystem` service to get the real path of the `public://` directory. Then we rely on PHP's default file functions to get the number of files in the directory and the directory's size.

Because we're using Drupal's service container, via autowiring, to get the FileSystem service we need to ensure that the command executes in the context of a fully bootstrapped Drupal environment. So we added the `CLI\Bootstrap(level: DrupalBootLevels::FULL)` attribute to the command method. This ensures that our command will only run in a fully bootstrapped environment.

Test it out by running `drush get-files-size`. You should see something like below:

```
drush get-files-size

The number of files is 2, and the size of the public files directory is: 6.5M.
```

### Convert the command into a Composer package

Now that we have the command working, we can convert it into a Composer package. This is optional, but useful if you want to be able to use the command on different Drupal projects.

First, create a directory somewhere outside your Drupal project that will house the new Composer package. For example, */get\_files\_size*.

Then move the command class from *drush/Commands* into this new directory. Resulting in */get\_files\_size/FilesDirectoryCommands.php*

Inside the */get\_files\_size* directory, add a *composer.json* file with the following content:

```
{
  "name": "my_org/get-files-size",
  "description": "Drush command that returns the size of the public files directory and number of files there.",
  "license": "MIT",
  "type": "drupal-drush",
  "authors": [
    {
      "name": "John Doe",
      "email": "[email protected]"
    }
  ],
  "require": {
    "php": "^7.4"
  },
  "minimum-stability": "dev",
  "prefer-stable": true
}
```

Installing commands as part of a Composer project requires that the project's type be `drupal-drush`. This ensures that when it's installed in a Drupal project it'll be placed into a location that Drush knows to look for it.

Upload the package to GitHub as a separate repository dedicated to the command.

Ensure the *composer.json* file in the root of your Drupal project has the `drupal-drush` type in the `installer-paths` array.

Example:

```
...
"installer-paths": {
  "web/core": ["type:drupal-core"],
  "web/libraries/{$name}": ["type:drupal-library", "type:npm-asset"],
  "web/modules/contrib/{$name}": ["type:drupal-module"],
  "web/profiles/contrib/{$name}": ["type:drupal-profile"],
  "web/themes/contrib/{$name}": ["type:drupal-theme"],
  "drush/Commands/contrib/{$name}": ["type:drupal-drush"]
},
...
```

You also need to update the `repositories` key in the *composer.json* file of your Drupal project to include your new repository:

```
...
{
  "type": "package",
  "package": {
    "name": "my_org/get-files-size",
    "type": "drupal-drush",
    "version": "1.0.0",
    "dist": {
      "url": "https://github.com/my_org/get-files-size.zip",
      "type": "zip"
    },
    "require": {
      "composer/installers": "~1.0"
    }
  }
},
...
```

After that you can run `composer require my_org/get-files-size` and the command will be installed via Composer into *drush/Commands/contrib/get-files-size*.

## Recap

In this tutorial, we learned how to create a site-wide Drush command that returns the size and number of files in the Drupal public files directory. We learned that site-wide Drush commands require only a command class file that contains the command callback (or callbacks for multiple related commands) and it needs to be placed in the */{project-root}/drush/Commands* directory in order for Drush to find it. We also learned how to optionally bundle a site-wide command as a Composer package, so it can be shared between projects.

## Further your understanding

- What are the advantages and disadvantages of creating a site-wide command instead of a putting the command code in a module?
- We used the `CLI\Bootstrap(level: DrupalBootLevels::FULL)` attribute; what other bootstrap levels are available as values for this property? When would you use each one of them, and why?

## Additional resources

- [Drush official documentation](https://www.drush.org) (drush.org)
- [Drush Git repository](https://github.com/drush-ops/drush) (GitHub.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Logging and Error Handling in Drush Commands](/tutorial/logging-and-error-handling-drush-commands?p=2593)

Next
[Overview: Drush Hooks](/tutorial/overview-drush-hooks?p=2593)

Clear History

Ask Drupalize.Me AI

close