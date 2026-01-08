---
title: "Add Options to a Custom Drush Command"
url: "https://drupalize.me/tutorial/add-options-custom-drush-command?p=2593"
guide: "[[command-line-tools-drupal]]"
---

# Add Options to a Custom Drush Command

## Content

When you create a custom Drush command it might be useful to allow users to pass options (predefined values) that change the way a command works. You can think of options as being flags, or variables, that affect the command's internal logic. As an example, consider the Drush core `user:login` command which by default returns a one-time login link for the root account. The command also accepts an optional `--name` option which allows the internal logic to create a link for a specified user instead of only being able to create links for the root user. This makes the command useful in a wider variety of situations. Another common option is the `--format` option which allows a user to specify that they want the command to return its output in a format (CSV, JSON, Table, etc.) other than the default.

Options are defined in the Drush command's attributes. Their values are passed as part of an associative array to the command method. Unlike parameters, options are not ordered, so you can specify them in any order, and they are called with two dashes like `--my-option`. Options are always optional, not required, and can be set up to accept a value `--name=John` or as a boolean flag without a value `--translate`.

In this tutorial we'll:

- Declare options for a custom Drush command in its attributes
- Learn how to use these options inside the custom Drush command method

By the end of this tutorial, you should be able to add options to your own custom Drush commands.

## Goal

Pass a `--show-status` option to a custom Drush command, so it outputs the status of the user if the option is set to `TRUE`.

## Prerequisites

- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)
- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)
- [Overview: Creating Your Own Custom Drush Commands](https://drupalize.me/tutorial/overview-creating-your-own-custom-drush-commands)
- [Create a Custom Drush Command](https://drupalize.me/tutorial/create-custom-drush-command)

## Initial setup

In [Create a Custom Drush Command](https://drupalize.me/tutorial/create-custom-drush-command) we created a custom module named *drush\_helpers*. We defined a custom Drush command named *drush-helpers:blocked-users* in the Drush command class *Drupal\drush\_helpers\Drush\Commands\DrushHelpersCommands*.

In this tutorial, we are going to extend this command and add a `--show-status` option that can be passed to the `drush-helpers:blocked-users` command to return the user status as another column in the output.

Example:

```
# With --status option.
drush drush-helpers:blocked-users --status

--------- ----------- ---------------------- --------
User Id   User Name   User Email             Status  
--------- ----------- ---------------------- --------
6         john        [email protected]   0       
--------- ----------- ---------------------- --------

# Without --status option.
drush drush-helpers:blocked-users

--------- ----------- ----------------------
User Id   User Name   User Email           
--------- ----------- ----------------------
6         john        [email protected] 
--------- ----------- ----------------------
```

## Add option to custom Drush command

Adding an option requires:

- Declaring options using PHP attributes
- Adding new variables to the method signature
- Altering the command's internal logic

### Define options in the command's attributes

Options are declared using PHP attributes. Each option is defined using the `CLI\Option` attribute. The name of the option defined in the attribute becomes the key in the `$options` associative array passed to the command method.

Update the command method in *src/Drush/Commands/DrushHelpersCommands.php* with the following attributes and method signature:

```
/**
 * Command that returns a list of all blocked users.
 *
 * @return \Consolidation\OutputFormatters\StructuredData\RowsOfFields
 */
#[CLI\Command(name: 'drush_helpers:blocked-users', aliases: ['blocked-users'])]
#[CLI\Usage(name: 'drush_helpers:blocked-users', description: 'Returns all blocked users')]
#[CLI\Argument(name: 'status', description: 'The string value of the user status on the site. Available values are: active and blocked')]
#[CLI\Option(name: 'show-status', description: 'Show status of the user in the results')]
#[CLI\FieldLabels(labels: [
  'id' => 'ID',
  'name' => 'Username',
  'email' => 'User email',
  'status' => 'Status',
])]
#[CLI\DefaultTableFields(fields: ['id', 'name', 'email', 'status'])]
public function blockedUsers($status = 'blocked', $options = ['show-status' => FALSE, 'format' => 'table']): RowsOfFields {
```

Notice that in the new `CLI\Option` attribute, the `name` argument is both the value used on the command line (`--{OPTION-NAME}`) and the key in the associative array that contains the provided value.

Since the option influences if the new *Status* column is displayed, we also updated `CLI\FieldLabels` to include the mapping between the `$rows` array key and a label; we also added it into the `CLI\DefaultTableFields` definitions.

**Note:** The attribute above also has `CLI\Argument` properties that represent Drush command parameters. We set those up in [Use Command Line Arguments with a Custom Drush Command](https://drupalize.me/tutorial/use-command-line-arguments-custom-drush-command).

### Update the command method definition

Since we have a new option declared in the attributes, we need to update the command method definition to match. Update the `$options` associative array that is the last argument to the method's signature.

Example:

```
public function blockedUsers($status = 'blocked', $options = ['show-status' => FALSE, 'format' => 'table']): RowsOfFields {}
```

The key(s) of the array should match the option's name from the attribute. The value can be one of the following:

- Boolean value of `FALSE` or `TRUE`
- Any string value
- Or, the special `self:REQ` or `self:OPT` which are shorthand for `InputOption::VALUE_REQUIRED` or `InputOption::VALUE_OPTIONAL`

In our case, we'll be treating the option as a boolean flag, so `FALSE` or `TRUE` values would work. Whatever value you provide here is what the default will be if no value is specified at the command line. You can use `self:OPT` if you want no default value. And `self:REQ` if you want no default value, **and** you want to require the user provide a value. However, in most cases we recommend you use parameters, and not options, for required values.

### Update the command method's logic

Time to use the new options array within the function. Update your code to look like the following:

```
public function blockedUsers($status = 'blocked', $options = ['show-status' => FALSE, 'format' => 'table']): RowsOfFields {
  if ($status === 'active') {
    $status = 1;
  }
  elseif ($status === 'blocked') {
    $status = 0;
  }
  else {
    // Handling incorrect parameter.
    throw new \Exception(dt('You passed an incorrect parameter value. Accepted values are: "active", "blocked"'));
  }

  $users = $this->entityTypeManager->getStorage('user')->loadByProperties(['status' => $status]);
  $rows = [];
  /** @var \Drupal\user\UserInterface $user */
  foreach ($users as $key => $user) {
    if ($user->id() != 0) {
      $rows[$key] = [
        'id' => $user->id(),
        'name' => $user->getAccountName(),
        'email' => $user->getEmail(),
      ];
    }

    if ($options['show-status']) {
      $rows[$key]['status'] = $user->status->value;
    }
  }
  return new RowsOfFields($rows);
}
```

The most important thing here is that we can use the `$options['show-status']` variable to access either the user-provided input or the default value, then use that value to alter the logic in our command. In this case, we checked for the value inside the `$options` array and added a `status` value for the user if the option is set to `TRUE`.

### Test the updated command

To test the updated command, clear the Drush cache (`drush cc drush`) and then call `drush blocked-users active --show-status` at the command line. You should see something like the output shown below:

```
 --------- ----------- --------------------- --------
  User Id   User Name   User Email            Status  
 --------- ----------- --------------------- --------
  8         editor                            1       
  1         sitesuper   [email protected]   1       
 --------- ----------- --------------------- --------
```

## Recap

In this tutorial, we added a `--show-status` option to a custom Drush command. To do this we had to update the command method's attributes to include a new `CLI\Option` attribute, then update/add an `$options` argument to the method definition, and finally update the logic of the method to use the new option. Using options, we can allow the user to provide run-time configuration for a custom Drush command that alters the behavior of the command. And, we can author commands that are more generic and can be used in a wider variety of situations.

## Further your understanding

- Can you update the code to pass a second option like `--limit=N` that allows a user to limit the number of rows returned?
- How would you call a command with multiple options?

## Additional resources

- [Drush official documentation](https://www.drush.org) (drush.org)
- [Drush Git repository](https://github.com/drush-ops/drush) (GitHub.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Use Command Line Arguments with a Custom Drush Command](/tutorial/use-command-line-arguments-custom-drush-command?p=2593)

Next
[Add an Interactive Prompt to a Drush Command](/tutorial/add-interactive-prompt-drush-command?p=2593)

Clear History

Ask Drupalize.Me AI

close