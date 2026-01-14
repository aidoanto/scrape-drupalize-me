---
title: "Overview: Creating Your Own Custom Drush Commands"
url: "https://drupalize.me/tutorial/overview-creating-your-own-custom-drush-commands?p=2593"
guide: "[[command-line-tools-drupal]]"
---

# Overview: Creating Your Own Custom Drush Commands

## Content

Developers can implement the Drush Command API to write their own custom Drush commands. This allows you to include Drush commands with your modules to allow the module's features to be used via the CLI. You can also create project-specific Drush commands that help with the development, deployment, and maintenance of your particular application.

We've written Drush commands to help generate reports, make it easier for new team members to get up and running, compile custom theme assets, and more. Any time we need to write PHP code that interacts with our Drupal site where we're worried the code might time out because it takes too long to execute we'll reach for Drush. Custom Drush commands are also useful to combine background processes that can be executed on cron, such as nightly imports, data synchronization, bulk database manipulation, custom queues processing, and so much more.

In this tutorial we'll:

- Learn about different types of custom Drush commands
- Review the anatomy of a Drush command
- See how the Drush bootstrap process relates to commands

By the end of this tutorial, you'll be able to identify the parts of a custom Drush command and start writing your own.

## Goal

Introduce the components that make up a custom Drush command.

## Prerequisites

- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)
- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)
- [PHP Attributes](https://drupalize.me/tutorial/php-attributes)

## Custom Drush commands

Custom Drush commands are Drush commands that don't come with the core Drush installation and are only present if they are explicitly installed. There are 3 different types of custom Drush commands:

1. Those that live in a custom module
2. Site-wide commands
3. Global commands

In most cases it's easiest to add your custom commands to a module. But if the command spans multiple projects, or doesn't relate to a single module, there are other options.

### Custom module commands

These commands reside in a custom module and help automate tasks related to the features the module provides by exposing them to the CLI via Drush. They are useful for custom recurring imports, queue and cache purgers, email senders, and bulk CRUD tasks on content and custom entities.

Commands declared as part of a module are the easiest to maintain. They can be integrated with Drupal's service container to allow easier use of Drupal's APIs.

### Site-wide commands

These commands are not bundled with a Drupal module and are called site-wide commands. They are commonly placed in a *drush/Commands* folder in the root of a Drupal project.

**Tip:** We often create a project-specific module with Drush commands and other code that is only intended to ever work for that one project.

Site-wide commands can be installed with Composer; they can be managed in a separate Git repository and act as a project dependency. This makes it convenient to declare those commands for routine tasks that are not related to any particular module functionality but are useful for multiple Drupal projects. For example, maybe your team uses a custom database dump command with an additional level of sanitization to provide GDPR compliance across multiple projects.

### Global commands

The third type of Drush commands are global commands. These commands are not part of any Drupal installation but are instead installed globally and available anywhere regardless of the presence of Drupal. It's similar to other command line applications like Git or Pantheon's Terminus. These commands are not supported by default and developers need to make special configuration inside a *drush.yml* file in order to point Drush to the location of those commands. It's preferable to use site-wide commands and avoid global Drush commands. If there is a strong need for a global command, it's preferable to explore writing a *\*.phar* file or a script instead.

## The anatomy of a Drush command

Every Drush command consists of 3 main user-facing parts: the command's *name* (e.g. `user:login`) and user input in the form of *options* (e.g. `--name="ryan"`) and *parameters* (e.g. `node/add/blog`) that influence the command's features.

Image

![](../assets/images/drush-command-anatomy.png)

Drush commands are written in PHP, and require:

- PHP code that is placed in one of the places that Drush knows to look for it. Usually the correct PSR-4 namespace within a custom module.
- A *command file* that contains a PHP class with attributes (or annotations) and methods for each individual command.
- Using the autowire trait (`Drush\Commands\AutowireTrait`) to inject services into the command class.

### The Drush command file

Command files contain the PHP code that makes up the core logic of your custom Drush command. These *.php* files need to be located in one of the places that Drush knows to look for them, and contain a PHP class that extends the `\Drush\Commands\DrushCommands` base class.

This file will usually reside inside the *src/Drush/Commands* directory of a custom module.

Example:

```
my_module/
  composer.json
  my_module.info.yml
  src/Commands/MyDrushCommands.php
```

**Tip:** A command file can be generated with the help of the `drush generate` command. If you need a refresher on how the `drush generate` command works, see [Develop Drupal Modules Faster with Drush Code Generators](https://drupalize.me/tutorial/develop-drupal-modules-faster-drush-code-generators).

Each command class may declare 1 or more commands. Typically, modules bundle commands related to the same functionality in the same class. For instance, the Search API module has 1 command file, and it provides the declaration of all the Search API commands.

Within a Drush command class, each individual command is defined as a method with a set of PHP attributes. The executable command code goes inside the method and the attributes provide metadata, like the command name, aliases, help, options, parameters and special properties such as whether a command can throw an exception, what it returns, and any validation steps.

Drush uses the values of these attributes to figure out how to map the input provided to the Drush executable to the code that should be executed.

As an example, the `drush language:add` command from Drush core looks like the following:

Example *src/Commands/LanguageCommands.php*:

```
namespace Drush\Drupal\Commands\core;

use Consolidation\OutputFormatters\StructuredData\RowsOfFields;
use Drupal\Core\Extension\ModuleHandlerInterface;
use Drupal\Core\Language\LanguageManagerInterface;
use Drupal\language\Entity\ConfigurableLanguage;
use Drush\Attributes as CLI;
use Drush\Commands\DrushCommands;
use Drush\Utils\StringUtils;
use Symfony\Component\DependencyInjection\ContainerInterface;

class LanguageCommands extends DrushCommands {
  ... 
    #[CLI\Command(name: self::ADD, aliases: ['language-add'])]
    #[CLI\Help(hidden: true)]
    #[CLI\Argument(name: 'langcode', description: 'A comma delimited list of language codes.')]
    #[CLI\Option(name: 'skip-translations', description: 'Prevent translations from being downloaded and/or imported.')]
    #[CLI\Usage(name: 'drush language:add nl,fr', description: 'Add Dutch and French language and import their translations.')]
    #[CLI\Usage(name: 'drush language:add nl --skip-translations', description: 'Add Dutch language without importing translations.')]
    #[CLI\ValidateModulesEnabled(modules: ['language'])]
    public function add($langcode, $options = ['skip-translations' => false]): void
    {
      // Command code goes here ...
    }
  ...
}
```

These attributes declare a new `CLI\Command` named `language:add`. When a user executes `drush language:add` at the command line, Drush will call the `LanguageCommands:add()` method. In addition to the command name, the metadata in the attributes is used by Drush to help provide context for Drush about the user-provided input that the command accepts and guidance for how to deal with the command's expected return value.

### Attributes versus annotations

Drush used to use, and still supports, annotations for command metadata. We recommend using attributes as they are the method used by Drush core. But don't be surprised if you see examples on other sites that use annotations.

### Arguments (aka parameters)

Broadly speaking, arguments are usually used to express the thing on which a command should perform its logic.

Arguments are input parameters passed to the Drush command via stdIn. Their value is passed as a variable to the method that implements the command. They aren't necessarily required, but the logic within the command method is required to validate the input and throw any appropriate errors.

Arguments are typically used when the pool of possible values is rather wide. The value itself typically doesn't influence the behavior of the command but rather is used as a dynamic value inside the command logic.

For example, the `language:add` command has a `langcode` argument. When a user executes the command, they pass a value to the command as an input parameter:

```
drush language:add en
```

Then this langcode argument (in our case, `en`) is passed to the command method as a variable.

Example snippet of code from the `LanguageCommands:add` method:

```
/**
 * Add a configurable language.
 */
 #[CLI\Command(name: self::ADD, aliases: ['language-add'])]
 #[CLI\Argument(name: 'langcode', description: 'A comma delimited list of language codes.')]
public function add($langcode, $options = ['skip-translations' => FALSE]) {
    // Command code here.
  }
```

Arguments are declared using a `CLI\Argument` attribute. To pass multiple parameters each one needs to have its own attribute declaration. The `drush user:password` command is an example of a command that takes multiple arguments.

Learn more about passing arguments to a Drush command in [Pass Parameters to a Drush Command](https://drupalize.me/tutorial/use-command-line-arguments-custom-drush-command).

### Options

Options are primarily used to control the run-time configuration of a Drush command. They are prefixed with a `--` at the command line, and are also frequently called flags. For example, a `--format` option can configure a command to output the results of a command as either CSV, or JSON.

Options are declared using `CLI\Option` attribute. A command can have any number of options and each one should have its own attribute line.

The collected values are passed to the command method as a single `$options` associative array where the key is the option `{name}` and the value is whatever the user entered at the command line. You can set default values for options, and mark them as "value required" or "value optional" as part of the command method's signature.

Example snippet of code from the `LanguageCommands:add` method:

```
#[CLI\Command(name: self::ADD, aliases: ['language-add'])]
#[CLI\Option(name: 'skip-translations', description: 'Prevent translations from being downloaded and/or imported.')]
public function add($langcode, $options = ['skip-translations' => false]) {
 // Code goes here ...
}
```

In the above example from the `language:add` command, the `skip-translations` option is declared as an attribute. It takes a `TRUE` or `FALSE` value, with the default being `FALSE`. This example also takes advantage of the fact that if we pass a named option with no value its value will be set to `TRUE`. So writing `--skip-translations` is the same as `--skip-translations=true` or `--skip-translations=1`. If the option isn't specified, then its value in this particular case is assumed to be `FALSE`.

Learn more about passing options to a command in [Pass Options to a Drush Command](https://drupalize.me/tutorial/add-options-custom-drush-command).

### Provide documentation for your command

The value that a user sees when looking at the "help" for your command is derived from the attributes.

Consider the example snippet of code from the `LanguageCommands:add` method:

```
#[CLI\Command(name: self::ADD, aliases: ['language-add'])]
#[CLI\Help(hidden: true)]
#[CLI\Argument(name: 'langcode', description: 'A comma delimited list of language codes.')]
#[CLI\Option(name: 'skip-translations', description: 'Prevent translations from being downloaded and/or imported.')]
#[CLI\Usage(name: 'drush language:add nl,fr', description: 'Add Dutch and French language and import their translations.')]
#[CLI\Usage(name: 'drush language:add nl --skip-translations', description: 'Add Dutch language without importing translations.')]
#[CLI\ValidateModulesEnabled(modules: ['language'])]
public function add($langcode, $options = ['skip-translations' => false]): void
```

The command `drush help language:add` will output the following:

```
Add a configurable language.

Examples:
  drush language:add nl,fr                  Add Dutch and French language and import their translations.
  drush language:add nl --skip-translations Add Dutch language without importing translations.

Arguments:
  langcode A comma delimited list of language codes.

Options:
  --skip-translations Prevent translations to be downloaded and/or imported.

Aliases: language-add
```

You can see how Drush translates the command attributes into human-readable output. Note that the *Arguments* map to the `CLI\Argument` attributes. The *Examples* come from the `CLI\Usage` attributes.

## The Drush bootstrap process

Drush is capable of bootstrapping the Drupal environment, similar to how Drupal is bootstrapped when a page request is made. This allows Drush commands to rely on Drupal services, database connections, and other APIs. By default, commands assume that they'll be run in the context of a fully functioning Drupal instance, and will fail without that context.

However, not all commands require a fully functional Drupal installation. Some commands may operate just fine with a partial bootstrap or no bootstrap at all. Custom Drush commands can specify via their attributes the level to which they need Drupal to bootstrap in order to perform their function.

When you are authoring a custom Drush command, or debugging an existing one, it's useful to understand what bootstrap level is specified for the command.

Bootstrapping is done from a Symfony Console command hook. The following are valid bootstrap levels declared in `\Drush\Boot\DrupalBootLevels`:

- `DrupalBootLevels::NONE`: Only Drush is bootstrapped, and preflight operation is complete. At this level, the commands should operate within the Drush installation context. But we cannot make any assumptions about Drupal.
- `DrupalBootLevels::ROOT`: Checks for a valid Drupal root. Code shouldn't operate on a specific site but can work with the entire Drupal installation.
- `DrupalBootLevels::SITE`: The Drupal *sites* directory is set up, environment variables and configuration in PHP variables are present. This is an ideal phase for commands that modify the *settings.php* file.
- `DrupalBootLevels::CONFIGURATION`: This is the first phase where Drupal-specific code can be invoked. It's typically used for code that interacts with the Drupal Install API.
- `DrupalBootLevels::DATABASE`: The database connection is established from the parameters in *settings.php*. Ideal phase for interaction with the Database API.
- `DrupalBootLevels::FULL`: Drupal is fully bootstrapped and functional. Any command that interacts with core's general Drupal APIs can run on this level.

There is also a special `CLI\Bootstrap` value that is not a Bootstrap phase *per se* -- the `DrupalBootLevels::MAX` value. Commands with the `#[CLI\Bootstrap(level: DrupalBootLevels::MAX)]` bootstrap attribute treat it as progressive bootstrap. The command will try to bootstrap the site as far as possible before executing the code. This is useful for commands with progressive output that changes based on the current bootstrap level. For example: `drush status`.

## Recap

Drush commands are made up of 3 user-facing parts: a command name, options, and parameters. These and other features of the command are provided via attributes and are used by the Drush executable to map user input to the correct code to execute. Developers can author custom Drush commands by creating a command file that contains a Drush command class, adding a *drush.services.yml* file and adjusting the project's *composer.json* file to tell Drush about the existence of custom commands.

There are 3 different types of Drush commands: module provided, site-wide, and global. You can write your own commands to automate tasks and operations provided by your custom module -- or site-wide commands that can be reused on multiple sites and are not specific to a module.

## Further your understanding

- Can you list some examples of things in your regular development workflow that could be made easier by writing custom Drush commands?
- We showed one `CLI\Usage` example; can there be more `CLI\Usage` attributes for one method? Why would you need them? Explore [Drupal core commands to find more examples](https://github.com/drush-ops/drush/blob/master/src/Drupal/Commands/core/LanguageCommands.php)
- In what cases you would use module-specific commands vs site-wide commands?

## Additional resources

- [Drush official documentation](https://www.drush.org) (drush.org)
- [Drush Git repository](https://github.com/drush-ops/drush) (GitHub.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Create a Custom Drush Code Generator](/tutorial/create-custom-drush-code-generator?p=2593)

Next
[Create a Custom Drush Command](/tutorial/create-custom-drush-command?p=2593)

Clear History

Ask Drupalize.Me AI

close