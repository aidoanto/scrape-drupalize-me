---
title: "Enable, Update, and Manage Modules and Themes with Drushfree"
url: "https://drupalize.me/tutorial/enable-update-and-manage-modules-and-themes-drush?p=2593"
guide: "[[command-line-tools-drupal]]"
order: 11
---

# Enable, Update, and Manage Modules and Themes with Drushfree

## Content

Every Drupal site consists of many Drupal *projects* like modules and themes. Drush comes with a group of commands that aid in managing projects from the command line. These commands can check which modules are present in a site's codebase, report their security status, enable modules, and display metadata for modules and themes. All of these commands start with the `pm` prefix, and are part of the *project manager* group.

Common use cases for the project manager commands include: quickly enabling/disabling modules via the CLI rather than performing numerous clicks in the UI, and as part of CI/CD process that lists (or maybe even automates) security updates.

In this tutorial we'll:

- List the available `pm` commands
- Enable a module with Drush
- Uninstall a module with Drush
- Use Drush to check for security updates for modules, themes and PHP packages

By the end of this tutorial you'll have an understanding of the project manager commands that come with Drush, how to use them, and how to speed up common workflows and maintenance tasks.

## Goal

Introduce the Drush project manager suite of commands and possible applications for each command.

## Prerequisites

- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)
- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)

## Quick reference

The *project manager* group consists of the following commands:

- `pm:list` - Shows a list of available extensions (modules and themes).
- `pm:enable` - Enables one or more modules.
- `pm:security` - Checks Drupal Composer packages for pending security updates.
- `pm:security-php` - Checks non-Drupal PHP packages for pending security updates.
- `pm:uninstall` - Uninstalls one or more modules and their dependent modules.

## What is Drush project manager?

Drush comes with a suite of commands built around extension management -- installation and removal of modules, module status and metadata, and lists. These commands are part of Drush, in the project manager group, and start with the `pm` prefix.

In the earlier versions of Drush, prior to Drupal's adoption of Composer for dependency management, the list of pm commands was longer. Now Composer is recommended to manage dependencies; therefore, the list of `pm` commands has been reduced, removing some dependency management related commands. Older tutorials will often refer to the `drush pm:download` or `drush dl` command to download a contributed module from Drupal.org. You should now use `composer require...` instead.

Managing extensions with Composer is beneficial since it will not only load the extensions themselves but also their dependencies such as additional required libraries and packages. It also allows for easy patching and version management. If you want to learn more about managing your site with Composer, please refer to the [Introduction to Composer for Drupal Users series](https://drupalize.me/series/introduction-composer-drupal-users).

## Get a list of available extensions

The `drush pm:list` command allows you to see a list of all available extensions -- modules and themes -- on your site. The command allows passing in some options. One of the most useful options is `--type`. This allows you to filter the extension by its type: module or theme.

Run `drush pm:list --type module` to get a list of all the modules available on your site.

By default, the command returns a list of all extensions, regardless of whether they are enabled or disabled. If you'd like to filter by status you can use the `--status` option that takes one of two available values: disabled or enabled.

The `--no-core` option will filter out all core modules from the list. It's useful since the list of core modules is mostly the same for all Drupal sites that are on the same major version of Drupal core. Slight differences might sometimes happen when experimental core modules are being released or removed from Drupal core. Filtering out core modules makes the list more trimmed down, especially on sites with a lot of extensions.

To see the list of all available options, refer to the [official Drush documentation for this command](https://www.drush.org/latest/commands/pm_list/).

Example use cases:

- Check to see if a module is present in a site's codebase, and whether that module is enabled
- Find the machine name of a module for use in another command or script

## Install and uninstall modules with Drush

To enable Drupal modules with Drush, run the following command `drush pm:enable module_1, module_2`

In this command *module\_1*, *module\_2* - is a comma-separated list of machine names of the modules you would like to enable. This command is so widely used by developers that in many tutorials and documentation you may see its alias used instead: `drush en module_1`.

To run the installation command, the module needs to be first brought into the site codebase with Composer. Example:

```
composer require drupal/devel
drush en devel -y
```

To uninstall modules with Drush run `drush pm:uninstall module_1, module_2`. This command also takes a comma-separated list of module machine names.

## Check for security updates

Drush provides 2 commands that allow checking for security updates. The first command is `drush pm:security`. This command checks all Drupal Composer packages (packages whose name is prefixed with *drupal/* in your *composer.json* file) for security updates. Effectively it means checking Drupal modules' and themes' security status on your website. Tip: this command also outputs a Composer snippet that can be used to update outstanding extensions.

The output of this command can be formatted using a variety of different output formatters: csv, json, list, null, php, print-r, sections, string, table, tsv, var\_dump, var\_export, xml, and yaml. This is useful if the command is used as part of security updates automation or audit scripts.

Example `drush pm:security` output:

```
drush pm:security

[warning] One or more of your dependencies has an outstanding security update.
[notice] Try running: composer require drupal/admin_toolbar drupal/core --update-with-dependencies
[notice] If that fails due to a conflict then you must update one or more root dependencies.

+----------------------+-------------------+
| Name                 | Installed Version |
+----------------------+-------------------+
| drupal/admin_toolbar | 2.4.0             |
| drupal/core          | 8.9.13            |
+----------------------+-------------------+
```

The second command `drush pm:security-php` checks the non-Drupal packages for security updates. Those are typically PHP libraries that are downloaded as dependencies for Drupal core and modules, and are stored in the vendor directory of your website.

To see the list of all available options for these commands, refer to the [official Drush documentation](https://www.drush.org/latest/commands/pm_security).

## Recap

Drush comes with a suite of *project manager* commands to aid in the management of a site's modules and themes. Drush `pm` commands are useful for enabling and disabling modules, getting a list of extensions, and checking for security updates of Drupal packages and their dependencies.

## Further your understanding

- Use Drush to create a CSV file listing all the currently enabled, non-core, modules on your site.
- What happens if you use Drush to enable a module like json\_api that has dependencies, but you don't specify the dependencies? What happens if you do?

## Additional resources

- [Drush official documentation](https://www.drush.org) (drush.org)
- [Drush Git repository](https://github.com/drush-ops/drush) (github.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Install Drush Using Composer](/tutorial/install-drush-using-composer?p=2593)

Next
[Use Drush for Common Site and Environment Management Tasks](/tutorial/use-drush-common-site-and-environment-management-tasks?p=2593)

Clear History

Ask Drupalize.Me AI

close