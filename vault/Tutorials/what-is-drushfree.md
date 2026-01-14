---
title: "What Is Drush?free"
url: "https://drupalize.me/tutorial/what-drush-0?p=2593"
guide: "[[command-line-tools-drupal]]"
order: 9
---

# What Is Drush?free

## Content

Drush, aka The Drupal Shell, is a command line utility and UNIX scripting interface for Drupal. It allows access to common Drupal features and tasks via the command line. It can help speed up common tasks for Drupal site builders, developers, and DevOps teams. Among other things, it makes it easier to integrate Drupal into CI/CD workflows.

In this tutorial we'll:

- Learn what Drush is and what can be done with Drush
- Install Drush
- Find a list of Drush commands
- Learn how to execute commands

By the end of this tutorial, you'll understand how to install and use Drush with your Drupal projects, navigate the list of its commands and run them. This is intended as an overview. Other tutorials will provide more detail about common commands and use-cases.

## Goal

Introduce the Drush command line utility tool to Drupal developers.

## Prerequisites

- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)

## Introduction to Drush

Drush is a PHP application that runs in your terminal and allows you to interact with one or more Drupal projects. Drush core ships with commands for performing various common tasks like clearing the cache, running database updates, and managing configuration. It also provides utilities for executing SQL queries and migrations, and for generating scaffolding code for frequently used Drupal core APIs.

The official Drush documentation is at <https://www.drush.org/latest/>.

The code is built and maintained by the Drupal community on GitHub <https://github.com/drush-ops/drush/>.

## Why use Drush?

Drush allows you to speed up, and even automate, many time-consuming tasks that would normally require a user to perform a variety of steps in Drupal's UI. As simplified example, imagine you want to enable a module. In the Drupal UI this requires that you first log in, then navigate to the modules page, find the module in the list and check the box for it, then submit the form, then often times submit a secondary confirmation form, and finally the module is enabled. This same task can be performed with Drush using the following command:

```
drush en {MODULE_NAME} -y
```

If you're already spending a lot of time in the command line using tools like Git, this can be a lot quicker.

As another example, imagine deploying a security update to your site. After updating the code on the production site you need to make a backup, login, run *update.php*, import any configuration changes, clear the cache, etc. By using Drush you can script much of this workflow and make it part of your CI/CD process instead of having to perform the tasks manually. Learn more in [Use Drush To Speed up Common Drupal Development Tasks](https://drupalize.me/tutorial/use-drush-speed-common-drupal-development-tasks), [Enable, Update, and Manage Modules and Themes with Drush](https://drupalize.me/tutorial/enable-update-and-manage-modules-and-themes-drush), and [Use Drush to Deploy Drupal Updates](https://drupalize.me/tutorial/use-drush-deploy-drupal-updates).

Because Drush runs in the command line, it can be used in Bash (or other shell) scripts just like any other command line application. Most Drush commands are capable of returning their results in various formats (like JSON, CSV, and YAML) for consumption by other utilities. Learn more in [Overview of Drush's Output Formatting System](https://drupalize.me/tutorial/overview-drushs-output-formatting-system).

For example, want to gZip the user-generated files directory but aren't exactly sure where it's located as that can change per environment? Use this:

```
tar czf files.tar.gz $(drush dd files)
```

One of our favorites is using Drush to rebuild Drupal's cache while debugging code. Depending on the configuration of your environment, clearing the cache with Drush often provides more detailed debug output since it prints out all the errors and their trace logs into the shell. Learn more about scripting with Drush in [Automating Drupal Tasks with Drush and Bash Scripts](https://drupalize.me/tutorial/automating-drupal-tasks-drush-and-bash-scripts).

Developers also take advantage of Drush's `generate` command to speed up creation of custom modules. The built-in generators can quickly scaffold boilerplate code for creating custom entity types, controller, plugins, forms, and a variety of other Drupal core APIs. Learn more about using generators in [Develop Drupal Modules Faster With Drush Code Generators](https://drupalize.me/tutorial/develop-drupal-modules-faster-drush-code-generators)

Developers can use Drush's API to write their own custom Drush commands specific to their application and functional needs. This is often much quicker than trying to develop a command line application from scratch. Learn more in [Overview of Creating Your Own Custom Drush Commands](https://drupalize.me/tutorial/overview-creating-your-own-custom-drush-commands).

Drush is a very popular utility and many contributed modules also expose their features as Drush commands allowing developers to save time on tasks like (re)building the search index, purging the varnish cache, importing RSS data, and more.

## Install Drush

Assuming that you're [using Composer to manage your Drupal project](https://drupalize.me/tutorial/use-composer-your-drupal-project):

```
composer require --dev drush/drush
```

After that, Drush should be available via `./vendor/bin/drush --version`.

For detailed instructions, and to learn how to install the global Drush launcher, refer to [Install Drush Using Composer](https://drupalize.me/tutorial/install-drush-using-composer).

Earlier versions of Drush -- Drush 8 and 9 -- had various methods of installation. For instance, Drush could be installed globally on your environment. Starting with version 10 (required for Drupal 9 and up), Drush supports only Composer-based installation. This means that your site should be managed with Composer and Drush should be installed as a dependency.

## Basic usage

**Note:** This assumes you've installed the global launcher and can use `drush` instead of `./vendor/bin/drush` when running Drush commands.

To get a list of available Drush commands run `drush` from within the root directory of a Drupal project. By default, Drush will output a list of the commands that it can run in the given context. Most Drush commands expect a working Drupal application is present and piggyback on Drupal's API, database access, and configuration.

This list of commands will vary per project since both Drush core and contributed modules can provide Drush commands. For example, a site that has the Search API module installed will have a different set of commands than one that does not.

Drush can be run by typing `drush` from within your project's root directory -- or anywhere within the Drupal site.

Example:

```
cd /var/www/html/{drupal-project-root}
drush

Drush Commandline Tool 10.6.0

Run `drush help [command]` to view command-specific help.  Run `drush topic` to read even more documentation.

 Available commands:
 _global:
   browse                               Display a link to a given path or open link in a browser.
   config:pull (cpull)                  Export and transfer config from one environment to another.
   deploy                               Run several commands after performing a code deployment.
   drupal:directory (dd)                Return the filesystem path for modules/themes and other key folders.
... <snip>
```

You can filter commands according to module by running `drush list` with the `--filter` option.

Example:

```
drush list --filter=core
```

To execute any command, type `drush {command_name}`.

Example:

```
drush core:status
```

To learn about the arguments and options for a command, use the `drush help` command.

Example:

```
drush help core:status
```

You can explore Drush's built-in manual by using the `drush topic` command.

## Recap

Drush is a Drupal-specific shell -- a command line utility that allows you to execute, script, and automate routine maintenance, site building, and development tasks. Drush can be extended to provide additional module- or project-specific commands. It is frequently used as part of everyday Drupal development tasks and CI/CD workflow. Drush is awesome.

## Further your understanding

- Can you find the built-in help for Views-related commands?
- Why do different Drupal projects have different sets of Drush commands available?

## Additional resources

- [Drush official documentation](https://www.drush.org) (drush.org)
- [Drush Git repository](https://github.com/drush-ops/drush) (github.com)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Install Drush Using Composer](/tutorial/install-drush-using-composer?p=2593)

Clear History

Ask Drupalize.Me AI

close