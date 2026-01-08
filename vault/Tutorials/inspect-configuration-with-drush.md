---
title: "Inspect Configuration with Drush"
url: "https://drupalize.me/tutorial/inspect-configuration-drush?p=2478"
guide: "[[drupal-site-administration]]"
---

# Inspect Configuration with Drush

## Content

There are some administrative UI tools for managing configuration, but some tasks can only be completed with Drush. As a site administrator, you will find Drush an indispensable tool for managing configuration between instances of the same site. Furthermore, Drush includes integration with Git in certain commands, enabling you to create a configuration workflow with Drush that also uses best practices in version control.

By the end of this lesson you should be able to:

- Get the status of a site's configuration
- List configuration on a site
- View configuration objects
- Set values for a specific key inside a configuration object
- Edit a configuration object in active configuration without needing a configuration form
- Integrate a Git workflow with Drush

## Goal

Be able to use Drush to inspect configuration objects on a Drupal site.

## Prerequisites

- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)
- [Introduction to Git](https://drupalize.me/series/introduction-git)

## Inspect and interact with configuration

Drush provides a number of commands for inspecting and interacting with your Drupal site's configuration. With Drush, you can perform a number of administrative tasks related to configuration, including:

- [Get the status of a site's configuration](#config-status)
- [List site configuration](#config-list)
- [Inspect configuration objects](#config-get)
  - Discover keys and values inside a configuration object
  - View the value for a specific key inside a configuration object
- [Edit an active configuration value](#config-set)
- [Edit one or more values in active configuration](#config-edit)

**Note:**: All Drush command examples in this tutorial assume you are executing the commands from the root of your Drupal site.

To change directories, use `cd`:

```
cd path/to/your/site
```

## Configuration status

The `config:status` command will give you information about the state of your site's configuration: .

Sometimes you will want to see if there are any differences between your site's active configuration (stored in the database by default) and the data contained in exported YAML files stored in your site's configuration sync directory.

To show which configuration items need to be synchronized:

```
drush config:status
```

Example output:

```
------------- ----------- 
  Name          State      
------------- ----------- 
  system.site   Different  
------------- -----------
```

With `config:status`, you can also filter by state, prefix, label as well as choose a filter for output with the following options:

- `--state[=STATE]`: A comma-separated, quoted list of states to filter results. [default: "Only in DB,Only in sync dir,Different"]

Scenario: Someone created a new image style using the admin UI.

Find configuration that is only in the database and hasn't been exported yet:

```
drush config:status --state="Only in DB"
```

Example output:

```
----------------------- ------------ 
  Name                    State       
----------------------- ------------ 
  image.style.hero_wide   Only in DB  
----------------------- ------------
```

- `--prefix=PREFIX`: A config prefix. For example, "system". No prefix will return all names in the system. Does not accept more than one prefix.

Example:

```
drush config:status --prefix="image"
```

Example output:

```
----------------------- ------------ 
Name                    State       
----------------------- ------------ 
image.style.hero_wide   Only in DB  
----------------------- ------------
```

- `--label=LABEL`: A config directory label (i.e. a key in `$config_directories` array in *settings.php*). Note: The ability to support multiple configuration directories in the `$config_directories` array is deprecated as of Drupal 8.8.0 and will be removed in Drupal 9.
- `--format=FORMAT`: Format the result data. Available formats: csv, json, list, php, print-r, sections, string, table, tsv, var\_dump, var\_export, xml, yaml [default: "table"]
- `--fields=FIELDS` Available fields: Name (name), State (state) [default: "name,state"]
- `--field=FIELD` Select just one field, and force format to 'string'.

## List site configuration

**Note**: If you were using `drush config-list` in an older version of Drush, use `config:status` instead. (See above.)

## Inspect active configuration objects

The `drush config-get` or `drush cget` command is useful when you want to quickly view the contents of a configuration object.

```
drush config-get <config-name>
```

- Discover keys and values inside a configuration object
- Command: `config:get`
- Aliases/Shortcuts: `cget`, `config-get`
- Accepts 2 arguments:
  - [Required] config-name: The name of the configuration object, for example, `system.site`. Accepts quoted and non-quoted string.
  - [Optional] key: Provide an optional key in a configuration object, for example `drush system.site uuid`, to retrieve the site's UUID.

For example:

```
drush config-get system.site
```

Example output:

```
uuid: ea163347-3e7e-4eba-876d-a52ce7600e90
name: 'Demo: Configuration Entities in Drupal'
mail: [email protected]
slogan: ''
page:
  403: ''
  404: ''
  front: /node
admin_compact_mode: false
weight_select_max: 100
langcode: en
default_langcode: en
_core:
  default_config_hash: AyT9s8OUcclfALRE_imByOMgtZ19eOlqdF6zI3p7yqo
```

If you already know the name of a key inside a configuration object, it can be useful to retrieve the value for a specific key. For example, to get the site name, use the optional `key` argument, after the configuration name.

For example:

```
drush config-get system.site name
```

Example output:

```
'system.site:name': 'Demo: Configuration Entities in Drupal'
```

## Edit a single active configuration value

To set a configuration item value directly, use `drush config-set`.

```
drush config-set <config-name> <config-key> <value>
```

This command is useful if you want to quickly set a value without using a configuration form in Drupal's administrative UI, for example, changing the display-name of your site. You will need to know the configuration object name and the specific key whose value you want to edit. (**Hint:** use `config:state` to find this out.)

For example:

```
drush config-set system.site name "Configuration Management with Drush"
```

- Aliases/Shortcuts: `cset`, `config-set`
- Command: `config:set`
- Accepts 3 arguments (all required):
  - config-name: The configuration object name, for example `system.site`.
  - key: The configuration key, for example, `name` or `page.front`.
  - value: The value to assign to the configuration key. Use `-` to read from STDIN.

**Hint:** You may need to enter `drush cr` (`drush cache-rebuild`) to see the change appear on your site.

## Edit active configuration in a text editor

Use `drush config-edit` to edit a configuration object in a text editor.

```
drush config-edit <config-name>
```

The `config-edit` subcommand is useful when you want to edit more than one value at once, if you don't know or feel like looking up the key, or if you don't want to use configuration forms.

Edits are imported into active configuration after closing editor, after the confirmation prompt. However, depending on the configuration item, you may not see the change reflected in the corresponding configuration form or front-facing value (i.e. the site name in the branding block) until you clear (or rebuild) the cache with `drush cache-rebuild`.

For example:

```
drush config-edit system.site
```

- Command: `config:edit`
- Aliases/Shortcuts: `cedit`, `config-edit`
- Opens the configuration object for editing in your command line shell's default text editor.
- Edit multiple values at once.
- Accepts 1 required argument:
  - config-name

After closing the file, you will be prompted to import the configuration into active configuration.

To view options for `config-edit` type `drush help config-edit`.

## Recap

In this tutorial, we took a look at Drush commands you can use to inspect and edit configuration values in Drupal. We learned how to:

- Get the status of a site's configuration
- List configuration on a site
- Inspect configuration objects
- Set values for a specific key inside a configuration object
- Edit a configuration object in active configuration without needing a configuration form

## Further your understanding

- In your CLI, use `drush help <command>` to view the description, arguments, and options for a particular command. You might learn about a new useful option that you'll want to use when managing configuration for your site.

## Additional resources

- [DrushCommands.com](https://drushcommands.com/)
- [Synchronize Configuration with Drush](https://drupalize.me/tutorial/synchronize-configuration-drush) (Drupalize.Me)
- [Live vs. Local Configuration Management](https://drupalize.me/tutorial/live-vs-local-configuration-management) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Synchronize Configuration with Drush](/tutorial/synchronize-configuration-drush?p=2478)

Next
[Live vs. Local Configuration Management](/tutorial/live-vs-local-configuration-management?p=2478)

Clear History

Ask Drupalize.Me AI

close