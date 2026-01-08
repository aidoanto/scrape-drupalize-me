---
title: "Logging and Error Handling in Drush Commands"
url: "https://drupalize.me/tutorial/logging-and-error-handling-drush-commands?p=2593"
guide: "[[command-line-tools-drupal]]"
---

# Logging and Error Handling in Drush Commands

## Content

Adding logging and error handling are an important part of authoring Drush commands. Logs allow developers to get timely feedback from a command and inform users about potential alterations and flags, events to monitor, and the progress of long-running commands. Correct error handling allows for clean exits, meaningful error descriptions, and provides a path forward for developers to fix the errors and accomplish their goals.

In this tutorial we'll:

- Explore the different types of logging messages Drush commands can output
- Learn how to handle errors from within a Drush command

By the end of this tutorial you'll know what types of log messages you can use; how to log success messages, errors, or debug statements from a custom Drush command; and how to handle errors and exceptions.

## Goal

Illustrate methods for logging messages and handling errors in a custom Drush command.

## Prerequisites

- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)
- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)
- [Overview: Creating Your Own Custom Drush Commands](https://drupalize.me/tutorial/overview-creating-your-own-custom-drush-commands)

## The Drush logger service

Drush utilizes Drupal's `Psr\Log\LoggerInterface` as part of its logging mechanism. A Drush *logger* instance can be accessed from within the command class via the `$this->logger()` function. The logger object can be used to output messages directly to the command line during command execution.

Messages passed to the logger instance must be a string or an object that implements a `__toString()` method.

## Message types

The logger interface identifies the following types of messages:

- **alert**: Action must be taken immediately
- **critical**: The system is in critical condition
- **debug**: Detailed debug information
- **emergency**: The system is unusable
- **error**: Runtime errors that don't require immediate action but should be logged and monitored
- **info**: Informational messages
- **log**: Generic log messages with arbitrary severity levels
- **notice**: Notification of normal, but significant, events
- **warning**: Exceptions that are not classified as errors
- **success**: Successful execution of the command or operation

Examples of the output of various log message types:

Image

![Screenshot of command line with the logged messages of different types](/sites/default/files/styles/max_800w/public/tutorials/images/logger_messages.png?itok=JIKKadPk)

Below we'll provide more details about each message type, and how to implement them in your code.

All the logger methods take 2 arguments unless otherwise noted:

- `$message`: The message to display
- An optional `$context` array

### Alert messages

Alerts are messages that call for immediate action from the user. Alerts can be logged by invoking the `alert()` method of the Drush logger instance from a hook or command callback.

Example:

```
$this->logger()->alert("Attention, maintenance is in progress, please stop the migration immediately!");
```

### Critical messages

Critical messages are messages that indicate critical system conditions. For example a service, component or integration is not available and throws unhandled, unexpected exceptions.

Critical messages can be logged by invoking the `critical()` method of the Drush logger instance from a hook or command callback.

Example:

```
$this->logger()->critical("Critical: database service is not available at the time, please check the access to the server and credentials");
```

### Debug messages

Debug messages provide additional debugging information to the users. They are typically used to add details about command alterations and hooks. Debug messages are only visible when the `--debug` option is passed to the command.

Debug messages can be logged by invoking the `debug()` method of the Drush logger instance from a hook or command callback.

Example:

```
$this->logger()->debug("Added new argument 'time' to the command annotation");
```

### Emergency messages

Emergency messages are logged when the system is unusable. Emergency messages can be logged by invoking the `emergency()` method of the Drush logger instance from a hook or command callback.

Example:

```
$this->logger()->emergency("Ping is failing, performance outage is detected!");
```

### Error messages

Error messages are used for logging runtime errors. These errors usually don't require immediate action but need to be logged and monitored. Error messages can be logged by invoking the `error()` method of the Drush logger instance from a hook or command callback.

```
$this->logger()->error("Date format isn't correct and cannot be parsed.");
```

### Info messages

Info messages output debugging info that is used for informational purposes during the debugging / development cycles. They are only visible when the `--debug` option is used. Info messages can be logged by invoking the `info()` method of the Drush logger instance from a hook or command callback.

Example:

```
$this->logger()->info(“Command execution has started.”);
```

### Log messages

Log messages are used to log events with arbitrary levels of severity. The message is logged using the `log()` method which takes 3 arguments:

- `$level`: Severity level. Corresponds to the logging severity levels defined in RFC 5424, section 6.2.1. Use a constant defined as part of `\Drupal\Core\Logger\RfcLogLevel`.
- `$message`: The message to log and display
- `$context`, an optional context array

Example:

```
$this->logger()->log(RfcLogLevel::ERROR, "Severe system malfunction");
```

The `log()` method can also be used in instances where the severity level is determined dynamically.

Example:

```
$severity = $this->howBadIsIt();
$this->logger()->log($severity, "Look out. Something happened.");
```

### Notice messages

Notices are used to log routine but significant events. Notice messages can be logged by invoking the `notice()` method of the Drush logger instance from a hook or command callback.

Example:

```
$this->logger()->notice("The content has been updated.");
```

### Warning messages

Warnings are used to log exceptions, or *not ideal* states, that are not classified as errors, critical, or emergency states. Warning messages can be logged by invoking the `warning()` method of the Drush logger instance from a hook or command callback.

Example:

```
$this->logger()->warning("The title of the entity wasn't provided in the legacy database; the placeholder title is used instead.");
```

### Success messages

Success messages indicate successful completion of an operation or command. Success messages can be logged by invoking the `success()` method of the Drush logger instance from a hook or command callback.

Example:

```
$this->logger()->success("The caches are cleared");
```

## Handling errors in Drush commands

To handle exceptions a Drush command can return a `\Consolidation\AnnotatedCommand\CommandError`, in which case the validation fails, execution stops, and result status and message are printed in the command line. Or it can throw an exception that will be converted into a `CommandError` automatically.

To throw an exception you can do something like the following:

```
throw new \Exception("New user password must be longer than 10 characters");
```

Exceptions will automatically be converted into the `CommandError` instances and logged into the command line.

To return a `CommandError` you can do something like the following:

```
return new CommandError("New user password must be longer than 10 characters");
```

The biggest difference between throwing an exception and calling `$this->logger()->error()` is that throwing an exception will cause the command to halt execution immediately, and by default will set the exit code to `1`.

## Recap

In this tutorial, we learned how to output logging messages, and throw exceptions, from a Drush command. The Drush logger instance implements the Drupal `Psr\Log\LoggerInterface`. It can be used to output messages with different severity levels, indicating the type of action required, that are displayed to the user.

Errors in custom Drush commands can be handled by either throwing an `\Exception` or returning `CommandError`. All exceptions are automatically converted into the `CommandError` and the constructors of both objects take the message as an argument. In both cases, command execution is halted and an exit code is returned.

## Further your understanding

- What’s the difference between the `log()` method and the `notice()`, `warning()`, and `error()` methods? Try passing an undefined level such as *trivial* to the `log()` method. What do you see?
- Try adding logging and exception handling in your custom Drush commands.

## Additional resources

- [Drush official documentation](https://www.drush.org) (drush.org)
- [Drush Git repository](https://github.com/drush-ops/drush) (github.com)
- [Drupal logger interface is the PHP-FIG PSR-3: Logger Interface](https://www.php-fig.org/psr/psr-3/) (github.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add an Interactive Prompt to a Drush Command](/tutorial/add-interactive-prompt-drush-command?p=2593)

Next
[Create Site-Wide Custom Drush Commands](/tutorial/create-site-wide-custom-drush-commands?p=2593)

Clear History

Ask Drupalize.Me AI

close