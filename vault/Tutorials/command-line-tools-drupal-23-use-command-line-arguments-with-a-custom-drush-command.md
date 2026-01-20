---
title: "Use Command Line Arguments with a Custom Drush Command"
url: "https://drupalize.me/tutorial/use-command-line-arguments-custom-drush-command?p=2593"
guide: "[[command-line-tools-drupal]]"
order: 23
---

# Use Command Line Arguments with a Custom Drush Command

## Content

Make your custom Drush command more flexible by allowing users to pass command line arguments into it. For example, rather than hard-coding that the command lists users with a specific status, allow the desired status to be specified at run-time. This allows the command's logic to be more generic, and to return different results, or operate on different data, based on the provided parameters.

*Parameters* are variables that are passed from user input at the command line into the Drush command method. Typically, they are either single string values, or comma-delimited strings of values. Parameters are typically used to provide input for the command related to *what* the command should work on, in contrast to *options*, which are typically used to configure *how* the command works.

In this tutorial we'll:

- Declare parameters for a custom Drush command in its attributes
- Use the parameter input inside the custom Drush command method

By the end of this tutorial you should understand how to work with parameters inside custom Drush commands.

## Goal

Pass a status parameter ('active' or 'blocked') to a custom Drush command that returns a list of users.

## Prerequisites

- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)
- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)
- [Overview: Creating Your Own Custom Drush Commands](https://drupalize.me/tutorial/overview-creating-your-own-custom-drush-commands)
- [Create a Custom Drush Command](https://drupalize.me/tutorial/create-custom-drush-command)

## Initial setup

In [Create a Custom Drush Command](https://drupalize.me/tutorial/create-custom-drush-command), we created a custom module named *drush\_helpers*. Then we defined a custom Drush command named *drush-helpers:blocked-users* in the Drush command class *Drupal\drush\_helpers\Drush\Commands\DrushHelpersCommands*. Right now it only returns users with the 'blocked' status.

In this tutorial, we are going to extend this command, and specify a `$status` parameter that can be passed into the command to return users that have the supplied status, making the command more flexible. Parameters in a Drush command act like variables and may have different user-provided values.

Parameters, also often referred to as arguments, tell a Drush command what to work on. If you want to allow the user to modify *how* the command works we recommend using options-style arguments. See [Add Options to a Custom Drush Command](https://drupalize.me/tutorial/add-options-custom-drush-command).

The process of adding a parameter includes:

- Updating the command attributes
- Updating the method signature
- Using the new variable in the command's internal logic

The final command usage may look something like shown below:

```
drush drupal-helpers:blocked-users active

--------- ----------- ----------------------
  User Id   User Name   User Email            
 --------- ----------- ----------------------
  6         john        [email protected]  
 --------- ----------- ----------------------
```

## Add arguments to a Drush command

Parameters are input variables passed to the Drush command method whose value is determined through user input when the command is called. These act as method variables. We need to tell the Drush executable about the values we intend to collect for our command, and it'll do the heavy lifting of parsing the user input and passing the values as variables to our command method where we can make use of them.

All of these changes are made to the existing `Drupal\drush\_helpers\Drupal\Commands\DrushHelpersCommands` class in *drush\_helpers/src/Drush/Commands/DrushHelpersCommands.php*.

### Update the command's attributes

Each parameter needs to have a `CLI\Argument` attribute declaration. The attribute declares the `name` (in our case it's called `$status`), and the human-readable `description` of the parameter. For example: "The string value of the user status on the site. Available values are: *active* and *blocked*".

Update the command attributes with the new `CLI\Argument` property. It may look something like below.

```
/**
 * Command that returns a list of all blocked users.
 *
 * @return \Consolidation\OutputFormatters\StructuredData\RowsOfFields
 */
#[CLI\Command(name: 'drush_helpers:blocked-users', aliases: ['blocked-users'])]
#[CLI\Usage(name: 'drush_helpers:blocked-users', description: 'Returns all blocked users')]
#[CLI\Argument(name: 'status', description: 'The string value of the user status on the site. Available values are: active and blocked')]
#[CLI\FieldLabels(labels: [
  'id' => 'ID',
  'name' => 'Username',
  'email' => 'User email',
])]
#[CLI\DefaultTableFields(fields: ['id', 'name', 'email'])]
```

You can also pass more than one parameter by specifying additional `CLI\Argument` attributes. Commands have no limit to the number of parameters they can accept. They are collected by Drush in the order listed in the attributes separated by a space when calling the command.

Example:

```
drush command-name @param1, @param2,param2a @param3
```

### Update the method definition

Since we have a new parameter declared in the attributes, we need to update the method declaration to match this new parameter. Add a `$status` variable into the method signature:

```
 public function blockedUsers($status = 'blocked', $options = ['format' => 'table']): RowsOfFields {
  // Method code goes here.
}
```

In this example, we set a default value of *blocked* that'll be used if the user does not provide a value. If we had more than one `CLI\Argument` attribute, we would need to include all of them in the method definition -- in the order they are specified in the attributes and named exactly as they are declared in the attributes `name` property.

### Update the command's logic

Time to use the new `$status` parameter within the function:

```
public function blockedUsers($status = 'blocked', $options = ['format' => 'table']): RowsOfFields {
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

In this code we map the text value of `$status` (which is more user-friendly) to the boolean value of it that is stored in the database. Then we pass the `$status` variable into the `loadByProperties()` method of the user storage object.

We also validate the value of the parameters being passed and return a message to the user when the parameter is incorrect by throwing an exception.

### Test the updated command

Clear Drush's cache with `drush cc drush`. Then run `drush blocked-users active`. You should see a table that contains all the active users on your site.

Example:

```
drush blocked-users active

 --------- ----------- ---------------------
  User Id   User Name   User Email           
 --------- ----------- ---------------------
  8         editor                           
  1         sitesuper   [email protected]  
 --------- ----------- ---------------------
```

Now call the command passing the blocked status like `drush blocked-users blocked`. You should see all blocked users on your site.

Example:

```
drush blocked-users blocked

 User Id   User Name   User Email            
 --------- ----------- ----------------------
  6         john        [email protected]  
 --------- ----------- ----------------------
```

Call the command without passing any parameter `drush blocked-users`.

Example:

```
drush blocked-users

--------- ----------- ----------------------
  User Id   User Name   User Email            
 --------- ----------- ----------------------
  6         john        [email protected]  
 --------- ----------- ----------------------
```

And finally, call the command with an invalid parameter `drush blocked-users disabled`.

Example:

```
drush blocked-users disabled

In DrushHelpersCommands.php line 50:

  You passed an incorrect parameter value. Accepted values are: "active", "blocked"
```

As you can see, the default value is working: without a `$status` parameter, the command returns a list of blocked users as expected.

## Recap

In this tutorial, we learned how to pass parameters into a custom Drush command. Doing so requires following 3 steps: update the command's attributes to include a new `CLI\Argument` attribute, add the new argument to the method definition, and update the logic of the method to use it. You can also set default values, and perform input validation, for parameters inside the method definition.

## Further your understanding

- Try removing the default value of the parameter from the method definition. Run the command without passing the parameter. What do you see? Why?
- Try to change the `name` from `$status` to `$stat`, clear the Drush cache and run the command passing `active` status in. What do you see? Why?
- Can you update the command to also take a user ID parameter?

## Additional resources

- [Drush official documentation](https://www.drush.org) (drush.org)
- [Drush Git repository](https://github.com/drush-ops/drush) (GitHub.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Create a Custom Drush Command](/tutorial/create-custom-drush-command?p=2593)

Next
[Add Options to a Custom Drush Command](/tutorial/add-options-custom-drush-command?p=2593)

Clear History

Ask Drupalize.Me AI

close