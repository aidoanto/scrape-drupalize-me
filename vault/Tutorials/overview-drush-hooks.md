---
title: "Overview: Drush Hooks"
url: "https://drupalize.me/tutorial/overview-drush-hooks?p=2593"
guide: "[[command-line-tools-drupal]]"
---

# Overview: Drush Hooks

## Content

If you want to change the way an existing Drush command works, you use hooks. Hooks are useful for altering command parameters, options, attributes data, and adding custom logic during particular stages of the command execution process. Drush hooks are conceptually similar to [Drupal hooks](https://drupalize.me/tutorial/what-are-hooks).

Hooks are methods on a Drush command class with an attribute indicating what hook is being implemented, and thus when the code should be invoked. The code in the methods is executed during specific stages of the command cycle. Developers can use core hooks -- predefined methods that come with Drush core -- or declare a custom hook that other commands can use.

In this tutorial we'll:

- Explore the different core Drush hooks
- Learn which hooks are called at what stage of the command cycle
- View example hook attributes and method implementations

By the end of this tutorial you'll know what types of core hooks are available to you and when they are called.

## Goal

Introduce Drush hooks and provide examples of how they get used.

## Prerequisites

- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)
- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)
- [Overview: Creating Your Own Custom Drush Commands](https://drupalize.me/tutorial/overview-creating-your-own-custom-drush-commands)

## Implementing a hook

There are 2 parts to implementing a Drush hook:

- Use an attribute to tell Drush when to call your code
- Write the code that alters or extends a specific Drush command

The code for implementing a hook exists as part of a Drush command class. See [Overview: Creating Your Own Custom Drush Commands](https://drupalize.me/tutorial/overview-creating-your-own-custom-drush-commands) for details about creating a command class so that Drush can find it.

The hook itself is a method on the command class, and is registered using a `CLI\Hook` attribute. The attribute consists of 2 parts:

- The *type* of the hook. For example `\Consolidation\AnnotatedCommand\Hooks\HookManager::COMMAND_EVENT` or `\Consolidation\AnnotatedCommand\Hooks\HookManager::POST_ALTER_RESULT`. These tell Drush when to trigger this code.
- A *target* that indicates which command(s) this hook applies to. It can be one of the following: the command's name (`pm:enable`), the label for a group of commands (`@pm`), blank to apply the code to all commands in *this* command class, or `*` to apply to all commands in *all* command classes.

Target is optional; depending on how it's defined, the hook may be attached to just one particular command, a set of commands with the given label, all commands defined in the same class file, or all Drush commands.

The format of a hook annotation looks like below.

```
#[CLI\Hook(type: HookManager::COMMAND_EVENT, target: 'drush-helpers:hook-example')]
```

## Drush hook types

There are 8 types of Drush core hooks, which correspond to the different states of the command cycle. Each type of hook has 3 variations: *pre-*, the actual hook, and *post-*. This allows for flexibility and precision in the definition when your code is called. For example, you might want to ensure that your code is called after (*post*) all other hooks that alter a command's options.

Within one subtype of hook the execution order is undefined and not guaranteed.

Below is a list of the core hooks, their subtypes, some comments about what the hook should be used for, and example implementations. They are listed in the order they are invoked.

### Command event hooks

- `HookManager::PRE_COMMAND_EVENT`
- `HookManager::COMMAND_EVENT`
- `HookManager::POST_COMMAND_EVENT`

This hook is called prior to the command event dispatching and validation. It's called via Symfony Command console notification. Symfony limits the ability to alter the `$input` object in this hook. You cannot alter parameters or options during this hook since the `$input` object is parsed at a later stage.

```
use Consolidation\AnnotatedCommand\CommandData;
use Drush\Attributes as CLI;

/**
 * Example ...
 */
#[CLI\Hook(type: HookManager::PRE_COMMAND_EVENT, target: 'pm:enable')]
public function preCommand(CommandData $commandData) {
    // Do something before pm:enable command is run.
}

/**
 * Example ...
 */
 #[CLI\Hook(type: HookManager::POST_COMMAND_EVENT, target: 'pm:enable')]
public function postCommand($result, CommandData $commandData) {
    // Do something after pm:enable command is run.
}
```

### Option hooks

- `HookManager::PRE_OPTION_HOOK`
- `HookManager::OPTION_HOOK`
- `HookManager::POST_OPTION_HOOK`

Option hooks are called when a command is being executed and Drush is figuring out possible options and their values. It's also called when the help command is called and Drush needs to list all the options for a command. It's typically used for dynamically adding options to a command.

Option hooks take in two arguments:

- A `Command` object
- An `AnnotationData` object.

Dynamic options are added using the `addOption()` method of the `$command` object.

Example:

```
use Consolidation\AnnotatedCommand\AnnotationData;
use Symfony\Component\Console\Command\Command;
use Drush\Attributes as CLI;

/**
 * Example ...
 */
 #[CLI\Hook(type: HookManager::OPTION_HOOK, target: 'pm:enable')]
public function additionalOption(Command $command, AnnotationData $annotationData) {
    $command->addOption(
        'validate-password',
        '',
        InputOption::VALUE_NONE,
        'Option added by @hook option pm:enable'
    );
}
```

If you do not need to dynamically alter the list of options, static options can be injected into any hook (regardless of its type) using the `CLI\Option` attribute.

The following example would add a new `--my-debug` option to the Drush core `user:login` command.

```
use Consolidation\AnnotatedCommand\Hooks\HookManager;
use Consolidation\AnnotatedCommand\AnnotationData;
use Symfony\Component\Console\Command\Command;
use Drush\Attributes as CLI;

/**
 * Register new option for user:login command.
 */
#[CLI\Hook(type: HookManager::OPTION_HOOK, target: 'user:login')]
#[CLI\Option('my-debug', 'Enable Debug Mode', InputOption::VALUE_NONE)]
public function additionalOptionsUserLogin(Command $command, AnnotationData $annotationData)
{
    // Alternatively you can dynamically add options using the `addOption()` method of the `$command` object.
}
```

If you need a refresher on how to use the `CLI\Option` attribute in Drush commands, refer to our tutorial [Add Options to a Custom Drush Command](https://drupalize.me/tutorial/add-options-custom-drush-command).

### Initialize hooks

- `HookManager::PRE_INITIALIZE`
- `HookManager::INITIALIZE`
- `HookManager::POST_INITIALIZE`

Initialize hooks run prior to the user starting interaction with the command. These hooks are typically used to populate arguments and options from a configuration file. They can also be used to alter the `AnnotationData` object.

Example:

```
use Consolidation\AnnotatedCommand\AnnotationData;
use Symfony\Component\Console\Input\InputInterface;
use Consolidation\AnnotatedCommand\Hooks\HookManager;
use Drush\Attributes as CLI;

/**
 * Example ...
 */
#[CLI\Hook(type: HookManager::INITIALIZE, target: 'user:login')]
public function initSomeCommand(InputInterface $input, AnnotationData $annotationData) {
    $value = $input->getOption('uid');
    if ($value == 1) {
        $input->setOption('uid', 256);
    }
}
```

In this example we hardcoded a different admin user id than user 1 since user 1 is blocked for security reasons. Anytime a user calls the command `drush user:login --uid=1` (which is also the default) we assume they're trying to log in as the *root* user and automatically rewrite the value of the option.

### Interact hooks

- `HookManager::PRE_INTERACT`
- `HookManager::INTERACT`
- `HookManager::POST_INTERACT`

Interact hooks are used to populate values for required parameters and options that were not supplied by the user. This is usually accomplished by prompting the user to provide the required values.

The execution of an interact hook may be suppressed by supplying the `--no-interaction` flag. This is useful for scripting solutions such as Composer and CI scripts that run Drush commands.

**Note:** Unlike *interact* hooks, *init* hooks are called even if the `--no-interaction` flag is supplied. Therefore, it's important to never use init hooks to initiate user interactions.

Example:

```
use Consolidation\AnnotatedCommand\AnnotationData;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\Style\SymfonyStyle;
use Consolidation\AnnotatedCommand\Hooks\HookManager;
use Drush\Attributes as CLI;

/**
 * Example ...
 */
#[CLI\Hook(type: HookManager::INTERACT, target: 'user:create')]
public function interact(InputInterface $input, OutputInterface $output, AnnotationData $annotationData) {
    $io = new SymfonyStyle($input, $output);

    // If no password is provided, then prompt for one.
    $password = $input->getOption('password');
    if (empty($password)) {
        $password = $io->askHidden("Enter a password:", function ($value) { return $value; });
        $input->setOption('password', $password);
    }
}
```

The above code modifies the `user:create` command and interactively prompts the user for a password if none is supplied, essentially making the password option required -- unless the command is run with the `--no-interaction` flag. In that case, this hook is skipped and the default behavior of generating a random password is used.

### Validate hooks

- `HookManager::PRE_ARGUMENT_VALIDATOR`
- `HookManager::ARGUMENT_VALIDATOR`
- `HookManager::POST_ARGUMENT_VALIDATOR`

Validate hooks are used to create custom validation rules for arguments and options.

Example:

```
use Consolidation\AnnotatedCommand\CommandData;
use Consolidation\AnnotatedCommand\Hooks\HookManager;
use Drush\Attributes as CLI;

/**
 * Example ...
 */
#[CLI\Hook(type: HookManager::VALIDATE, target: 'user:create')]
public function validatePassword(CommandData $commandData) {
    $input = $commandData->input();
    $password = $input->getOption('password');

    if (strpbrk($password, '!;$`') === false) {
        throw new \Exception("The password MUST contain at least one of the characters ! ; ` or $.");
    }
}
```

In the code above, we check if the password contains at least 1 of the special characters specified and throw an exception if it doesn't.

The validation hook may return nothing, which indicates that validation passed. If it returns a `CommandError`, or throws an exception (which Drush will convert to a `CommandError`), the validation fails, execution stops, and result status and messages are printed in the command line. If more than 1 validation hook runs against a command and at least 1 of them fails, the execution of the command stops.

### Command hooks

- `HookManager::PRE_COMMAND_HOOK`
- `HookManager::COMMAND_HOOK`
- `HookManager::POST_COMMAND_HOOK`

These hooks excel at performing modifications to the `$commandData` object right before and right after command execution. The *post-command* hook also allows you to alter the results returned from a command.

The *pre-command* and *command* hooks are equivalent to the *post-validate* hooks, and should conform to the `ValidatorInterface` interface. They are called after the last *post-validate* hook is called.

The *post-command* hook is an equivalent to the *pre-process* hook and is called before the first *pre-process* hook. It conforms to the `ProcessResultInterface` interface.

Examples:

```
use Consolidation\AnnotatedCommand\CommandData;
use Consolidation\AnnotatedCommand\Hooks\HookManager;
use Drush\Attributes as CLI;

/**
 * Example ...
 */
#[CLI\Hook(type: HookManager::PRE_COMMAND_HOOK, target: 'pm:enable')]
public function preCommand(CommandData $commandData) {
    // Do something before pm:enable
}

/**
 * Example ...
 */
#[CLI\Hook(type: HookManager::POST_COMMAND_HOOK, target: 'pm:enable')]
public function postCommand($result, CommandData $commandData) {
    // Do something after pm:enable
}
```

### Process hooks

- `HookManager::PRE_PROCESS_RESULT`
- `HookManager::PROCESS_RESULT`
- `HookManager::POST_PROCESS_RESULT`

Perform processing operations on the command results and return the final result in the specified format.

Example:

```
use Consolidation\AnnotatedCommand\CommandData;
use Consolidation\AnnotatedCommand\Hooks\HookManager;
use Drush\Attributes as CLI;

/**
 * Example ...
 */
#[CLI\Hook(type: HookManager::PROCESS_RESULT, target: 'pm:enable')]
public function process($result, CommandData $commandData) {
    // Process results.
}
```

### Alter hooks

- `HookManager::PRE_ALTER_RESULT`
- `HookManager::ALTER_RESULT`
- `HookManager::POST_ALTER_RESULT`

Alter hooks operate on the result object. They should only operate on the result object of a specified type, and may return an object of the same type or convert the original result object into a different type.

Example:

```
use Consolidation\AnnotatedCommand\CommandData;
use Consolidation\AnnotatedCommand\Hooks\HookManager;
use Drush\Attributes as CLI;

/**
 * @hook alter pm:enable
 * @option $alteration Alter the result of the command in some way.
 * @usage pm:enable --alteration
 */
#[CLI\Hook(type: HookManager::ALTER_RESULT, target: 'pm:enable')]
#[CLI\Option(name: 'alteration', description: 'Alter the result of the command in some way.')]
#[CLI\Usage(name: 'pm:enable --alteration', description: 'Enable modules with alterations.')]
public function alterSomeCommand($result, CommandData $commandData) {
    if ($commandData->input()->getOption('alteration')) {
        $result[] = $this->getOneMoreRow();
    }

    return $result;
}
```

The above example adds the output from `$this->getOneMoreRow()` to the `$result` array if the `--alteration` flag gets passed when the command gets called.

## Recap

Hooks allow custom to code to alter, and extend, Drush commands provided by Drush core or another module. Drush comes with the 8 types of hooks that allow modifications at different points in the command execution cycle. Each type of the hook has 3 variations: *pre-*, *post-*, and the main hook. This allows for flexibility in the order your code gets called.

Hooks are implemented as methods on a Drush command class with a `CLI\Hook` attribute. Hooks can be targeted at a specific command, a group of commands, all commands in the same command class, and *all* Drush commands.

## Further your understanding

- Choose any hook type and implement it to hook into any Drush core command.
- Add a `--debug-options` option to all commands that, when present, will output the values of all options before any options are altered, and after all option values are set by either the user or code.

## Additional resources

- [Drush official documentation](https://www.drush.org) (drush.org)
- [Drush Git repository](https://github.com/drush-ops/drush) (GitHub.com)
- [Drush hooks documentation](https://github.com/consolidation/annotated-command#hooks) (GitHub.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Create Site-Wide Custom Drush Commands](/tutorial/create-site-wide-custom-drush-commands?p=2593)

Next
[Alter an Existing Drush Command](/tutorial/alter-existing-drush-command?p=2593)

Clear History

Ask Drupalize.Me AI

close