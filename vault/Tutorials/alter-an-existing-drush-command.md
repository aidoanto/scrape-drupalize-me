---
title: "Alter an Existing Drush Command"
url: "https://drupalize.me/tutorial/alter-existing-drush-command?p=2593"
guide: "[[command-line-tools-drupal]]"
---

# Alter an Existing Drush Command

## Content

Often, there's an existing Drush command that does most of what you want, but needs just a few tweaks or enhancements to make it meet your project requirements. Maybe the existing core Drush command has the functionality but lacks some additional validation. Or maybe you need to add an option to perform some application-specific debugging logic for all commands in a group.

[Drush hooks](https://drupalize.me/tutorial/overview-drush-hooks) can be used to alter, extend, and enhance existing Drush commands.

In this tutorial we'll:

- Learn how to alter a Drush command with code in a custom module
- Declare a validation hook that alters the `user:password` command with additional password validation logic

By the end of this tutorial you should be able to alter a Drush command provided by Drush core or a contributed module with your own custom code.

## Goal

Alter the `drush user:password` command to require a password length of 10 characters or more.

## Prerequisites

- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)
- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)
- [Overview: Drush Hooks](https://drupalize.me/tutorial/overview-drush-hooks)

## Initial setup

The code we're going to write needs to live in a module. You can add it to an existing one, or create a new one. We'll be using the custom module we created in the tutorial, [Create a Custom Drush Command](https://drupalize.me/tutorial/create-custom-drush-command).

Our module is called *Drush Helpers* with the machine name `drush_helpers` and it’s already enabled. If your module isn't enabled, run `drush en drush_helpers -y` in the command line. Then run `drush cr` to clear Drupal's cache.

## Implement a Drush hook

The critical part is that the code for implementing a Drush hook lives in a Drush command file. We'll be modifying the `Drupal\drush\_helpers\Drush\Commands\DrushHelpersCommands` class in the *drush\_helpers/src/Command/DrushHelpersCommands.php* file to host our validation hook.

You'll also need to know what interface to implement, depending on the hook type. This will tell you the signature for the method you add to your command class.

| Hook | Interface |
| --- | --- |
| (pre-, post-) option | [OptionHookInterface](https://github.com/consolidation/annotated-command/blob/main/src/Hooks/OptionHookInterface.php) |
| (pre-, post-) init | [InitializeHookInterface](https://github.com/consolidation/annotated-command/blob/main/src/Hooks/InitializeHookInterface.php) |
| (pre-, post-) interact | [InteractorInterface](https://github.com/consolidation/annotated-command/blob/main/src/Hooks/InteractorInterface.php) |
| (pre-, post-) validate | [ValidatorInterface](https://github.com/consolidation/annotated-command/blob/main/src/Hooks/ValidatorInterface.php) |
| (pre-) command | [ValidatorInterface](https://github.com/consolidation/annotated-command/blob/main/src/Hooks/ValidatorInterface.php) |
| post-command | [ProcessResultInterface](https://github.com/consolidation/annotated-command/blob/main/src/Hooks/ProcessResultInterface.php) |
| (pre-, post-) process | [ProcessResultInterface](https://github.com/consolidation/annotated-command/blob/main/src/Hooks/ProcessResultInterface.php) |
| (pre-, post-) alter | [AlterResultInterface](https://github.com/consolidation/annotated-command/blob/main/src/Hooks/AlterResultInterface.php) |

### Add a validation hook

To add a validation hook, we need to add a method to the `Drupal\drush\_helpers\Drush\Commands\DrushHelpersCommands` class with a special `CLI\Hook` attribute. The type of the hook will be `HookManager::ARGUMENT_VALIDATOR` and the target is the core user password command `user:password`. The signature of the new method needs to match the [ValidatorInterface](https://github.com/consolidation/annotated-command/blob/main/src/Hooks/ValidatorInterface.php).

Example:

```
/**
 * Additional validation for user:password command.
 */
#[CLI\Hook(type: HookManager::ARGUMENT_VALIDATOR, target: 'user:password')]
public function userPasswordValidate(CommandData $commandData) {}
```

The above annotation tells Drush that this should be invoked when `validate` hooks are called, and only if the command being executed is the `user:password` command.

The validate hook takes a `$commandData` argument. So, you'll need to add a `use` statement for the `Consolidation\AnnotatedCommand\CommandData` class at the top of the file.

```
use Consolidation\AnnotatedCommand\CommandData;
```

If you need a refresher on hook annotations see [Overview: Drush Hooks](https://drupalize.me/tutorial/overview-drush-hooks).

### Test the command

Test that the hook is invoked by adding a logger statement to the method:

Example:

```
/**
 * Additional validation for user:password command.
 */
#[CLI\Hook(type: HookManager::ARGUMENT_VALIDATOR, target: 'user:password')]
public function userPasswordValidate(CommandData $commandData) {
  $this->logger->notice(dt("Achievement unlocked!"));
}
```

Then clear Drush's cache with `drush cc drush` and run `drush user:password [name] [password]`. Replace `[name]` and `[password]` with values that work for your Drupal project.

Since we are updating the password, we don't recommend testing this command on a production environment.

After you run the command you should see the following output in the command line:

```
 [notice] Achievement unlocked!
 [success] Changed password for editor.
```

This indicates that our custom code is being called by Drush.

### Validate the password length

Add some logic to validate that the password provided is at least 10 characters.

Example:

```
/**
 * Additional validation for user:password command.
 */
#[CLI\Hook(type: HookManager::ARGUMENT_VALIDATOR, target: 'user:password')]
public function userPasswordValidate(CommandData $commandData) {
  $password = $commandData->input()->getArgument('password');
  if (strlen($password) < 10) {
    throw new \Exception(dt('Password must be at least 10 characters long.'));
  }
}
```

We need to get the value of the password entered by the user, check its length, and throw an exception, if the password is shorter than 10 characters.

We get the user input by calling `$commandData->input()`. Since the password is a parameter (argument) for the `user:password` command, we then call the `getArgument()` method on the `$input` object and pass the name of the argument. If you don't know the parameter name, you can look at the attributes for the command you're altering. If password was defined as an option in the command attributes, we would need to call the `getOption()` method instead.

The exception thrown in the command is automatically transformed into a `CommandError` object, so we don't need to do anything special to convert it ourselves.

Refer to the `CommandData` class code and documentation in the [Drush Git repository](https://github.com/drush-ops/drush) to see all available methods and learn more about it.

### Test the final hook implementation

Run the command `drush user:password [name] 1234`. The password `1234` is shorter than 10 characters and should fail validation. After running the command you should see the following output:

```
In DrushHelpersCommands.php line 98:
                                                       
  New user password must be longer than 10 characters
```

Exceptions are automatically converted into `CommandErrors` and the error message output.

Run the command with the correct password length -- `drush user:password editor 0123456789` -- and it should pass the new validation.

Example:

```
[success] Changed password for [name].
```

## Recap

Drush hooks allow modules to alter the logic of commands provided by Drush core or contributed modules. Drush hooks get defined as methods on a Drush commands class with a `CLI\Hook` attribute. They use the `CLI\Hook` attribute to declare which hook to associate with, and to target one or more commands. Remember, the method signature needs to match the correct interface.

## Further your understanding

- We implemented a validate hook; which hook could be used to prompt the user for a more secure password if validation doesn't pass?
- Alter the code to implement this hook and prompt the user for a more secure password instead of throwing an exception.
- Can you update the code above so that it adds a new `--skip-password-length` flag that could be used to skip the new password length validation?

## Additional resources

- [Drush official documentation](https://www.drush.org) (drush.org)
- [Drush Git repository](https://github.com/drush-ops/drush) (GitHub.com)
- [Drush hooks documentation](https://github.com/consolidation/annotated-command) (GitHub.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview: Drush Hooks](/tutorial/overview-drush-hooks?p=2593)

Clear History

Ask Drupalize.Me AI

close