---
title: "Add an Interactive Prompt to a Drush Command"
url: "https://drupalize.me/tutorial/add-interactive-prompt-drush-command?p=2593"
guide: "[[command-line-tools-drupal]]"
order: 25
---

# Add an Interactive Prompt to a Drush Command

## Content

When the logic of a command depends on user input, it's useful to set up an interactive questionnaire inside the command code. This allows you to provide the user with more context about the input they're providing, and ensure that you collect all the necessary values. This is especially useful when the command uses a pre-defined list of options and the values require memorization. An example of this is the `drush cache-clear` command that comes with Drush core. It requires an argument indicating which cache to clear, which you can specify at the command line; however, if you invoke the command with no arguments it will present you with a list of cache bins to choose from and a UI for selecting one.

Drush 9+ can access the Input/Output (I/O) object via the `$this->io()` method. This object -- an instance of `\Drush\Style\DrushStyle` -- holds information about user-provided input, and utilities for manipulating that input. To ask a user a question, use an `io()` object in the command callback method. It can take over the execution flow of the command as needed to stop and gather additional input. The I/O system has various methods for asking confirmation or choice questions such as `confirm()` and `select()`.

In addition to prompting for input, the I/O object can be used to provide other styling to the command, like progress bars.

In this tutorial we'll:

- Learn how to prompt the user for additional input
- Process the user's answer as part of the command execution flow

By the end of this tutorial you should understand how to prompt a user for additional input for a custom Drush command.

## Goal

Update the `block-users` Drush command to prompt the user to choose a format for the output of the command.

## Prerequisites

- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)
- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)
- [Overview: Creating Your Own Custom Drush Commands](https://drupalize.me/tutorial/overview-creating-your-own-custom-drush-commands)
- [Create a Custom Drush Command](https://drupalize.me/tutorial/create-custom-drush-command)

## Initial setup

In [Create a Custom Drush Command](https://drupalize.me/tutorial/create-custom-drush-command) we created a custom module named *drush\_helpers* and defined a custom Drush command named *drush-helpers:blocked-users*. In this tutorial we are going to extend this command and include a prompt that will allow users to choose an output format of either *Table* or *JSON*.

## Add a format prompt to the Drush command

The styling of the input and output of a Drush command is an extension of the Symfony Console styling system. You can use any of the features it provides via the `$this->io()` method. For more information, read [How to Style a Console Command](https://symfony.com/doc/current/console/style.html).

The three most common methods for gathering user input at run-time are:

- `$this->io()->select() || $this->io()->multiselect()`: Ask a multiple choice question, and receive a predefined value as input
- `$this->io()->confirm()`: Ask a boolean yes/no question, and receive a boolean value as input
- `$this->io()->ask()`: Ask an open-ended question, and receive a string value as input

In this example we'll demonstrate `$this->io()->select()`. The process for using the others is the same.

### Update the command callback

To add the prompt to the Drush command, use the object returned from `$this->io()` and call the `select()` method. The `select()` method takes 3 arguments: the human-readable question to ask the user, an array of answers to choose from, and an optional default answer. The updated part of the command callback may look something like below:

```
public function blockedUsers() {
...
  $format = $this->io()->choice('Select the output format', ['table' => 'Table', 'json' => 'JSON']);
...
}
```

Place this line inside the command callback for your custom Drush command. When that line is encountered during command execution, Drush will halt the application and prompt the user for input. Once the user provides input the provided value gets saved to the `$format` variable.

### Map the selected value to the output format

For `$this->io()->select()` questions, the value that the user chooses corresponds to the key of the array of answers. **Note:** it doesn't correspond to the text of the answer or the numeric option in the command line prompt.

In our case `table` is the key for `Table` and `json` is the key for `JSON` output formats. Update the command code to handle the format. Your code may look something like the following:

```
public function blockedUsers() {
...
  if ($format === 'table') {
    return new RowsOfFields($rows);
  }
  else {
    return $this->output->writeln(json_encode($rows, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));
  }
...
}
```

In the code above, we return the output as a table if the user selected the *Table* option and *JSON* in all other cases. We didn't set *JSON* as a default option in the `select()` method, since we are handling it here in the conditional statement, and we only have 2 possible options for this question.

To print results as JSON we used a Drush output object and encoded the `$rows` array as JSON.

### Test the command

Clear Drush cache. `drush cc drush` and then call `drush blocked-users` in the command line. You should see something like shown below.

```
 Select the output format:
  [0] Cancel
  [1] Table
  [2] JSON
 >
```

Choose *1*, and you should see the results of the command printed as a table.

Example:

```
--------- ----------- ----------------------
  User Id   User Name   User Email            
 --------- ----------- ----------------------
  6         john        [email protected]  
 --------- ----------- ----------------------
```

Run the command one more time and choose *2*. You should see the results printed as JSON.

Example:

```
{
    "6": {
        "id": "6",
        "name": "john",
        "email": "[email protected]"
    }
}
```

If you choose the *Cancel* option it will terminate the command.

## Recap

In this tutorial, we learned how to prompt the user for interactive input for a Drush command. This uses the `$this->io()` object available inside the Drush command callback method. We used the `select()` method to ask a multiple choice question. You can also use `confirm()` for *TRUE* / *FALSE* (yes/no) answers, and `ask()` for open-ended questions. When used, Drush will halt command execution, prompt the user for input, and then return the provided input, so it can be used inside the command callback.

## Further your understanding

- We used the `select()` method; how would you use the `confirm()` method?
- What other use cases can you think of for user input prompts?

## Additional resources

- [Drush official documentation](https://www.drush.org) (drush.org)
- [Drush Git repository](https://github.com/drush-ops/drush) (GitHub.com)
- [How to Style a Console Command](https://symfony.com/doc/current/console/style.html) (symfony.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add Options to a Custom Drush Command](/tutorial/add-options-custom-drush-command?p=2593)

Next
[Logging and Error Handling in Drush Commands](/tutorial/logging-and-error-handling-drush-commands?p=2593)

Clear History

Ask Drupalize.Me AI

close