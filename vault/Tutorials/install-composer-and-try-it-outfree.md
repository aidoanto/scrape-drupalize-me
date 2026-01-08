---
title: "Install Composer and Try It Outfree"
url: "https://drupalize.me/tutorial/install-composer-and-try-it-out?p=2467"
guide: "[[command-line-tools-drupal]]"
---

# Install Composer and Try It Outfree

## Content

This tutorial demonstrates the value of using Composer. This demonstration will employ the most basic use case of using Composer to create a new, non-Drupal application that writes a message to the system log. It will encompass the fundamental concepts of Composer installation, requiring (installing) a new dependency, autoloading it, and implementing it.

In this tutorial we'll:

- Install Composer
- Use Composer to start a new project
- Use Composer to require a 3rd party dependency
- Use the required code in an example application

By the end of this tutorial you should be able to explain the value of Composer, and have Composer installed and working on your local machine.

## Goal

Take Composer for a quick test drive to experience its power first-hand. We will create a disposable “demo” application and perform a few operations on it.

## Prerequisites

- [What Is Composer?](https://drupalize.me/tutorial/what-composer)
- PHP installed on machine. See [Composer System Requirements](https://getcomposer.org/doc/00-intro.md#system-requirements).

## Installing Composer on your machine

First, we need to install Composer on your machine. To install Composer, your machine must already have PHP installed. See [Composer System Requirements](https://getcomposer.org/doc/00-intro.md#system-requirements) for more detail.

Follow the [Composer installation instructions](https://getcomposer.org/doc/00-intro.md#system-requirements) and return here when you’re finished!

If you’re a homebrew user on macOS, you can use `brew install composer`.

## Create a new project

Next, we will create a new, bare bones PHP application. Execute the following commands:

```
mkdir my-new-project
cd my-new-project
touch index.php
```

The previous commands:

- Created a new directory named `my-new-project`
- Entered that directory
- Created a new empty file named `index.php`.

Initialize Composer for this new application by executing:

```
composer init
```

This presents you with a series of command line prompts in order to gather basic information *package* information about your application.

In Composer terminology, your new PHP application is a Composer *package* of type *project*. We may correctly use the terms application, package, and project to refer to `my-new-project`. Other types of Composer packages include *library*, *composer-plugin*, *drupal-module*, *drupal-theme*, and more.

You may set the name, description, and license to whatever you'd like. This is simply metadata about your project.

Composer package names consist of the vendor name and project name, separated by `/`. E.g., `[my-organization]/[my-new-project]`.

Unless you intend on distributing your PHP application (we don't), then this information is only for your personal reference.

Please answer **no** to the following questions:

- Would you like to define your dependencies (require) interactively?
- Would you like to define your dev dependencies (require-dev) interactively?

We are going to use a different command to define our dependencies later.

- For the PSR-4 autoload mapping question, it's up to you! This question is asking whether to add a PSR-4 autoload mapping to the *composer.json*. (We'll show example output for both options.)

### Without PSR-4 autoload mapping

```
composer init

                                            
  Welcome to the Composer config generator  
                                            

This command will guide you through creating your composer.json config.

Package name (<vendor>/<name>) [myname/my-new-project]: 
Description []: My example Composer project
Author [Me <[email protected]>, n to skip]: 
Minimum Stability []: 
Package Type (e.g. library, project, metapackage, composer-plugin) []: project
License []: 

Define your dependencies.

Would you like to define your dependencies (require) interactively [yes]? n
Would you like to define your dev dependencies (require-dev) interactively [yes]? n
Add PSR-4 autoload mapping? Maps namespace "Me\MyNewProject" to the entered relative path. [src/, n to skip]: n

{
    "name": "me/my-new-project",
    "description": "My example Composer project",
    "type": "project",
    "authors": [
        {
            "name": "Me",
            "email": "[email protected]"
        }
    ],
    "require": {}
}

Do you confirm generation [yes]? 
ls
composer.json	index.php
```

### With PSR-4 autoload mapping

If you provide a directory for PSR-4 autoload mapping, e.g. `/src`, you get this output instead:

```
Add PSR-4 autoload mapping? Maps namespace "Me\MyOtherNewProject" to the entered relative path. [src/, n to skip]: 

{
    "name": "me/my-other-new-project",
    "description": "My other new project",
    "type": "project",
    "autoload": {
        "psr-4": {
            "Me\\MyOtherNewProject\\": "src/"
        }
    },
    "require": {}
}

Do you confirm generation [yes]? yes
Generating autoload files
Generated autoload files
PSR-4 autoloading configured. Use "namespace Me\MyOtherNewProject;" in src/
Include the Composer autoloader with: require 'vendor/autoload.php';
```

Let's take a moment to review what the `composer init` command did for us. It:

- Prompted us for information about our demo application
- Created a `composer.json` file in the application's root directory, formatted as a JSON array.

To learn more about each option for `composer init`, [see Composer's documentation](https://getcomposer.org/doc/03-cli.md#init).

## Requiring a new dependency

Next, we tell Composer that our application *requires* the *package* `monolog/monolog`.
Our application will use [monolog](https://packagist.org/packages/monolog/monolog)'s PHP classes to write messages to the system log. In Composer terminology, a *dependency* is defined as the *requirement* for a *package*. We may correctly refer to `monolog/monolog` as a dependency or a requirement.

Execute the following:

```
composer require monolog/monolog
```

What just happened? The `composer require` command:

- Modified our `composer.json` file and added `monolog/monolog` to the `require` array.
- Inspected our existing dependencies and found a version of `monolog/monolog` that is compatible with our other requirements (currently none) and with your machine's version of PHP.
- Downloaded `monolog/monolog` to `vendor/monolog/monolog`.
- Created a `composer.lock` file that defines the exact version of `monolog/monolog` that was downloaded. Learn more about the `composer.lock` file in [Composer Anatomy](https://drupalize.me/tutorial/anatomy-composer-project).
- Generated autoload files that include our new `monolog/monolog` dependency.

To browse all packages available via Composer, visit [Packagist](https://packagist.org/).

## Implement our dependency

Now let's use our new dependency by adding the following code to `index.php`:

```
<?php

// Require Composer's autoloader.
require __DIR__ . "/vendor/autoload.php";

use Monolog\Logger;
use Monolog\Handler\StreamHandler;

// Create a logger
$log = new Logger('my-log');
$log->pushHandler(new StreamHandler(__DIR__ . "/my.log", Logger::WARNING));

// Log a message!
$log->error('I did it!');
```

This snippet demonstrates the utility of autoloading. By requiring the `vendor/autoload.php` file that Composer generated, we automatically get access to all of the PHP classes from all of our Composer dependencies including `monolog/monolog`.

Rather than writing our own logger, we used an existing and robust logging library that was freely available. Composer found, installed, and loaded it for us. In Composer terminology, *installing* a package simply means downloading it to `vendor` and updating the autoloader.

Let's try using our application by executing:

```
php -f index.php
```

Now check the `my-new-project` directory. It should contain a new `my.log` file with `I did it!` written to it as an error. For example:

```
cat my.log
[2017-12-27 18:05:05] my-log.ERROR: I did it! [] []
```

You can destroy your demo application now; we're finished with it!

```
cd ..
rm -rf my-new-project
```

## Recap

In this tutorial, we created a new PHP application and used Composer to install the `monolog/monolog` library. We used Composer's autoloader to implement `monolog/monolog`'s classes and log a simple message to `my.log`.

## Further your understanding

- In Composer terminology, define the following words: requirement, dependency, application, package, project, library, plugin, module, install.
- What happens when you execute `composer require [package-name]`?
- Where does Composer download dependencies to by default?

## Additional resources

- [Composer resources](https://drupalize.me/topic/composer) (Drupalize.Me)
- Many local development environment tools include Composer in their stack. See our [Development Environments resources](https://drupalize.me/topic/development-environments) (Drupalize.Me)
- [Composer requirements for Drupal](https://www.drupal.org/docs/system-requirements/composer-requirements) (Drupal.org)
- [Composer installation instructions](https://getcomposer.org/doc/00-intro.md#system-requirements) (getcomposer.org)
- [`composer init` command reference](https://getcomposer.org/doc/03-cli.md#init) (getcomposer.org)
- [`composer require` command reference](https://getcomposer.org/doc/03-cli.md#require) (getcomposer.org)
- [Monolog library](https://packagist.org/packages/monolog/monolog) (packagist.org)
- [Packagist](https://packagist.org/) (packagist.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[What Is Composer?](/tutorial/what-composer?p=2467)

Next
[Anatomy of a Composer Project](/tutorial/anatomy-composer-project?p=2467)

Clear History

Ask Drupalize.Me AI

close