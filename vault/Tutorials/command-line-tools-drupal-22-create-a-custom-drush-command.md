---
title: "Create a Custom Drush Command"
url: "https://drupalize.me/tutorial/create-custom-drush-command?p=2593"
guide: "[[command-line-tools-drupal]]"
order: 22
---

# Create a Custom Drush Command

## Content

Creating a custom Drush command requires creating a PHP class that Drush can find with methods that have PHP attributes that provide metadata about each custom command. You'll use an autowire trait to inject any services into it. You'll also optionally modify the project's *composer.json* to tell Drush what versions of Drush the command is compatible with.

Custom Drush commands are a great way to expose your custom module's features to help automate these tasks and allow users to perform them as background processes. They can also provide a more efficient way to execute PHP code that takes a long time and is prone to timing out when run via the web server.

Depending on your use-case it can also be more efficient to create a custom Drush command to execute your logic instead of coding a complete UI. For example, if all the command needs to do is generate a CSV list it might take less effort to write a Drush command and pipe the output to a file than to create a UI that generates a file and prompts the user to download it.

In this tutorial we'll:

- Declare a new custom Drush command inside a custom module
- Make our custom Drush command output a list of all the blocked users on the site
- Verify our new command is working

By the end of this tutorial you should understand how to create a custom Drush command that returns a list of blocked users.

## Goal

Create a custom Drush command that outputs a tabular list of blocked users.

## Prerequisites

- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)
- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)
- [Develop Drupal Modules Faster With Drush Code Generators](https://drupalize.me/tutorial/develop-drupal-modules-faster-drush-code-generators)
- [Overview: Creating Your Own Custom Drush Commands](https://drupalize.me/tutorial/overview-creating-your-own-custom-drush-commands)
- [PHP Attributes](https://drupalize.me/tutorial/php-attributes)

## Command overview

In this tutorial we are going to build a custom command that returns a list of blocked users on a site with their IDs, usernames and emails in a tabular format. The command will not take any parameters or options (we'll add those later). The command will be defined inside a custom module.

Example output may look something like below:

```
drush drush-helpers:blocked-users

 --------- ----------- ----------------------
  User Id   User Name   User Email            
 --------- ----------- ----------------------
  6         john        [email protected]  
  17        jane        [email protected]
 --------- ----------- ----------------------
```

## Follow these steps to create a custom Drush command

We'll use `drush generate` to speed things up a bit in this example. If this is your first time authoring a Drush command, it's worth reading [Overview: Creating Your Own Custom Drush Commands](https://drupalize.me/tutorial/overview-creating-your-own-custom-drush-commands) first to familiarize yourself with the parts that are automatically generated below.

### Create a module

Drush commands are generally part of a module. You can either add them to an existing module, or create a new module. For this example, we'll create a new module named *drush\_helpers*.

We'll use the `drush generate` command to create a custom module. If you need a refresher about how to generate a custom module with `drush generate` refer to [Develop Drupal Modules Faster with Drush Code Generators](https://drupalize.me/tutorial/develop-drupal-modules-faster-drush-code-generators) tutorial.

Run the command `drush generate module` and answer the questions.

Example:

```
 Welcome to module generator!
––––––––––––––––––––––––––––––

 Module name:
 ➤ Drush Helpers

 Module machine name [drush_helpers]:
 ➤

 Module description:
 ➤ Contains helper Drush commands for the project.

 Package [Custom]:
 ➤

 Dependencies (comma separated):
 ➤

 Would you like to create module file? [No]:
 ➤

 Would you like to create install file? [No]:
 ➤

 Would you like to create README.md file? [No]:
 ➤

 The following directories and files have been created or updated:
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
 • /var/www/html/web/modules/custom/drush_helpers/drush_helpers.info.yml
```

We generated the module directory inside the custom modules directory and 1 file: *drush\_helpers.info.yml*. Our module's name is *Drush Helpers*.

Enable the module with Drush:

```
drush en drush_helpers
```

### Generate a Drush command file

Next, generate a command file. We'll use `drush generate` for this as well.

Run the following command:

```
drush generate drush:command-file
```

Then fill in the answers:

```
 Welcome to dcf generator!
–––––––––––––––––––––––––––

 Module machine name:
 ➤ drush_helpers

 Class [DrushHelpersCommands]:
 ➤

 Would you like to inject dependencies? [No]:
 ➤

 The following directories and files have been created or updated:
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
 • /var/www/html/web/modules/custom/drush_helpers/src/Drush/Commands/DrushHelpersCommands.php
```

As you can see, the command has generated 1 file within the drush\_helpers module directory: *DrushHelpersCommand.php*.

**Note:** The location, and name, of this file are important. The files are located in *src/Drush/Commands/* directory, which maps to the PSR-4 `Drupal\drush_helpers\Drush\Commands` namespace. The file name, and the class it contains, must end with `*Commands.php`.

### Update the command file

Drush commands use PHP attributes on class methods to define the command, its options and parameters, and other metadata.

Start by updating the comment and attributes above the `commandName()` method in *drush\_helpers/src/Drush/Commands/DrushHelpersCommands.php* and replacing the placeholder example attributes with the real ones.

Your new attributes may look something like the following:

```
/**
 * Command that returns a list of all blocked users.
 */
#[CLI\Command(name: 'drush_helpers:blocked-users', aliases: ['blocked-users'])]
#[CLI\Usage(name: 'drush_helpers:blocked-users', description: 'Returns all blocked users')]
```

We deleted the parameters and options part of the attributes, since we don't need them for our use case. We also updated the command alias and usage example.

The `CLI\Command` attribute tells Drush that our command can be invoked either by its full name `drush drush-helpers:blocked-users` or the shorter alias `drush blocked-users`. Command names and aliases should be unique. It's common to prefix the command name with the name of the module.

Next, update the command method name to match our new command name `blockedUsers`, and remove the method arguments, since our example command doesn't require any. The name you choose here is arbitrary -- Drush relies on the attributes to discover it -- but it's helpful to have it reflect what the code does.

The entire method may look something like below:

```
 /**
   * Command that returns a list of all blocked users.
   *
   * @usage drush-helpers:blocked-users
   *   Returns all blocked users
   *
   * @command drush-helpers:blocked-users
   * @aliases blocked-users
   */
  public function blockedUsers() {
    $this->logger()->success(dt('Achievement unlocked.'));
  }
```

Delete the automatically generated token example from the file.

### Test the new command

Let's test the command. At the command line run `drush cr` to clear Drupal's cache, then run `drush cc drush` to clear Drush cache. If you run `drush list` you should see the new command under the `_global` category.

If you have more than one command declared in the command file for your module, they will be grouped together under the module machine name category.

Now let's run the command `drush blocked-users` . You should see the message *Achievement unlocked.*

Example:

```
drush blocked-users
 [success] Achievement unlocked.
```

### Update the command logic

Let's update the logic of the command. We need to query the database and load all the blocked users. We'll inject the `EntityTypeManager()` service and use it to get the list. To do this we'll use autowiring, which is technique that uses the type hints of the class constructor's arguments to figure out which services to inject.

[Learn more about defining services dependencies automatically (autowiring)](https://symfony.com/doc/current/service_container/autowiring.html) (symfony.com).

Drush also supports the use of a static `create()` method for dependency injection in cases where autowiring is insufficient. This works the same as [injecting services into a Drupal controller](https://drupalize.me/tutorial/concept-dependency-injection).

Update the class file *src/Drush/Commands/DrushHelpersCommands.php*:

```
<?php

namespace Drupal\drush_helpers\Drush\Commands;

use Drupal\Core\Entity\EntityTypeManagerInterface;
use Drush\Attributes as CLI;
use Drush\Commands\AutowireTrait;
use Drush\Commands\DrushCommands;
use Consolidation\OutputFormatters\StructuredData\RowsOfFields;

/**
 * A Drush commandfile.
 */
final class DrushHelpersCommands extends DrushCommands {

  use AutowireTrait;

  /**
   * Constructs a DrushHelpersCommands object.
   */
  public function __construct(
    private readonly EntityTypeManagerInterface $entityTypeManager,
  ) {
    parent::__construct();
  }

  /**
   * Command that returns a list of all blocked users.
   *
   * @return \Consolidation\OutputFormatters\StructuredData\RowsOfFields
   */
  #[CLI\Command(name: 'drush_helpers:blocked-users', aliases: ['blocked-users'])]
  #[CLI\Usage(name: 'drush_helpers:blocked-users', description: 'Returns all blocked users')]
  #[CLI\FieldLabels(labels: [
    'id' => 'ID',
    'name' => 'Username',
    'email' => 'User email',
  ])]
  #[CLI\DefaultTableFields(fields: ['id', 'name', 'email'])]
  public function blockedUsers($options = ['format' => 'table']): RowsOfFields {
    $users = $this->entityTypeManager->getStorage('user')->loadByProperties(['status' => 1]);
    $rows = [];
    /** @var \Drupal\user\UserInterface $user */
    foreach ($users as $user) {
      if ($user->id() != 0) {
        $rows[] = [
          'id' => $user->id(),
          'name' => $user->getAccountName(),
          'email' => $user->getEmail(),
        ];
      }
    }
    return new RowsOfFields($rows);
  }

}
```

There's a lot going on in this new code. We'll explain it briefly below, and go into greater details in the remaining tutorials in this course.

In order to use autowiring, your `DrushHelpersCommands` class needs to include a `use Drush\Commands\AutowireTrait;` statement at the top of the file, and a `use AutowireTrait;` statement at the top of the class declaration. With this in place we can update the class constructor to accept an `EntityTypeManagerInterface` service.

The service (`@entity_type.manager`) is passed to the `__construct()` method when the class is instantiated and then stored on the parameter, `$entityTypeManager`.

Next, we use the `$entityTypeManager` inside the command method:

```
public function blockedUsers($options = ['format' => 'table']): RowsOfFields {
  $users = $this->entityTypeManager->getStorage('user')->loadByProperties(['status' => 1]);
  $rows = [];
  /** @var \Drupal\user\UserInterface $user */
  foreach ($users as $user) {
    if ($user->id() != 0) {
      $rows[] = [
        'id' => $user->id(),
        'name' => $user->getAccountName(),
        'email' => $user->getEmail(),
      ];
    }
  }
  return new RowsOfFields($rows);
}
```

Here we load all users by *status* when the value of *status* is blocked (`0`).

In the simplest use case, you can return a string from your Drush command and pass it through the logger (as in our original example). For this command we want a tabular display output.

To output results in a table, we process the records and build an associative array of results keyed by fields we want to return: id, name, and email. Then we return this array as a `RowsOfFields()` object, and pass a default format option to the `blockedUsers()` method, which means that the output will be rendered as a table.

For the table to display properly, we also need to update the command's attributes. We add the `CLI\FieldLabels` attribute and map the *keys* of the `$rows` array to human-readable labels. The `CLI\FieldLabels` attribute helps to create the table's header row and map values of the array to their corresponding columns.

We also specify the `CLI\DefaultTableFields` attribute and pass to it a list of all the keys of the `$rows` array that we want to be displayed in the table by default.

We need to specify the `@return` value and pass `\Consolidation\OutputFormatters\StructuredData\RowsOfFields` class to it.

This may seem like a lot of extra steps, but it ensures that users of our command can use the `--format` option to output the data from our command in whatever format they need, making the command much more versatile.

Drush utilizes the [Consolidation\OutputFormatters](https://github.com/consolidation/output-formatters#consolidationoutputformatters) library to format the results returned from commands. Formatters are used to allow commands to be implemented independently of Symfony Console output interfaces.

A command receives its input via its method parameters, and returns its result as a PHP object or an associative array. The structured data is then formatted by a formatter, and the result is printed.

If you'd like to read more about different Drush output formats, refer to [Overview: Drush's Output Formatting System](https://drupalize.me/tutorial/overview-drushs-output-formatting-system). You can read about all the available formatters in the *Consolidation\OutputFormatters* [library documentation](https://github.com/consolidation/output-formatters#consolidationoutputformatters).

After making these changes, clear the Drush and Drupal caches with `drush cr` and `drush cc drush`. Then run the command `drush blocked-users`.

The output should look something like below:

```
 --------- ----------- ----------------------
  User Id   User Name   User Email            
 --------- ----------- ----------------------
  6         john        [email protected]  
 --------- ----------- ----------------------
```

**Tip:** If you don't see any output make sure you have at least one blocked user account on your Drupal site.

## Recap

In this tutorial, we learned how to create a custom Drush command to display all blocked users as a table. We learned that a Drush command requires a PHP command file with a command class that has one or more command methods declared using attributes. Any services the command depends on can be injected using autowiring. And commands should return their data in a structured data format.

## Further your understanding

- How could you update this command to allow user input?
- Can you make the command output the list formatted as a CSV file?

## Additional resources

- [Drush official documentation](https://www.drush.org) (drush.org)
- [Drush Git repository](https://github.com/drush-ops/drush) (GitHub.com)
- [Consolidation\OutputFormatters](https://github.com/consolidation/output-formatters#consolidationoutputformatters) (GitHub.com)
- [Defining Services Dependencies Automatically (Autowiring)](https://symfony.com/doc/current/service_container/autowiring.html) (symfony.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview: Creating Your Own Custom Drush Commands](/tutorial/overview-creating-your-own-custom-drush-commands?p=2593)

Next
[Use Command Line Arguments with a Custom Drush Command](/tutorial/use-command-line-arguments-custom-drush-command?p=2593)

Clear History

Ask Drupalize.Me AI

close