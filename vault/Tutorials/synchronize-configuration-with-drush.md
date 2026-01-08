---
title: "Synchronize Configuration with Drush"
url: "https://drupalize.me/tutorial/synchronize-configuration-drush?p=2478"
guide: "[[drupal-site-administration]]"
---

# Synchronize Configuration with Drush

## Content

While the administrative UI for *Configuration synchronization* certainly provides a simple and effective means to export and import configuration, it is by no means the preferred method. The Drush command line utility provides the same functionality without the need for a web interface or the need to log in.

## Goal

Be able to use Drush to export and import configuration on a Drupal site.

## Prerequisites

- [Overview: Configuration Management in Drupal](https://drupalize.me/tutorial/overview-configuration-management-drupal)
- [Configuration Sync Directory Setup](https://drupalize.me/tutorial/configuration-sync-directory-setup)
- [Synchronize Configuration with the UI](https://drupalize.me/tutorial/synchronize-configuration-ui)
- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)

**Note:** Drush 8 command syntax differs from later versions.

## Export the configuration

Exporting the configuration is very straightforward with Drush. Using the configuration export subcommand, `config:export` (aliases: `cex`, `config-export`), you can export the site's active configuration to the sync directory.

### Navigate to your site

Using a local command prompt or an SSH program, navigate to the directory containing your site.

```
cd path/to/your/site
```

### Use Drush to export your site's configuration

Use the Drush configuration export command alias `cex` to export your configuration to the file system.

```
drush cex
```

You will be prompted with a list of changes, if any. Enter `y` to accept them.

## Export configuration without confirmation

Often, you will want to export the configuration without any sort of confirmation prompt. This is useful when you are already certain you wish to export all configurations or when running `drush cex` in a script. In these situations, you can skip the confirmation prompt by passing a `--yes` or `-y`, also known as a "yes" switch.

### Navigate to your site

Using a local command prompt or an SSH program, navigate to the directory containing your site.

```
cd path/to/your/site
```

**Note**: All remaining Drush command examples in this tutorial assume you are executing the commands from the root of your Drupal site.

### Export configuration, skipping confirmation

Use the Drush configuration export command and pass `--yes` to skip the confirmation.

```
drush cex --yes
```

**Tip:** Use `-y` instead of `--yes`.

## Inspect if configuration needs to be exported

**Note:** While the `-y` switch (shortcut for `--yes`) will work with `drush cex`, the `-n` flag is also a shortcut for `--no-interaction`, which is the equivalent of passing `-y`, which in essence, automatically answers "yes" to any interaction.

To see if configuration needs to be exported, there are 2 ways to do this:

Example 1 (preferred):

```
drush config:status
```

Example 1 output:

```
----------------------- ----------- 
Name                    State      
----------------------- ----------- 
image.style.hero_wide   Different  
----------------------- -----------
```

Example 2 (alternative):

```
drush cex --no
```

Example 2 output:

```
Differences of the active config to the export directory:

+------------+-----------------------+-----------+
| Collection | Config                | Operation |
+------------+-----------------------+-----------+
|            | image.style.hero_wide | Update    |
+------------+-----------------------+-----------+

 !                                                                                                                      
 ! [WARNING] The .yml files in your export directory (../config/sync) will be deleted and replaced with the active      
 !           config.: no.                                                                                               
 !                                                                                                                      

 [error]  Cancelled.
```

As you can see, the first example produced a cleaner output. See [Inspect Configuration with Drush](https://drupalize.me/tutorial/inspect-configuration-drush) for more details on `config:status` and other commands to inspect and interact with configuration.

## Automation strategies for exporting configuration

Scripts and automation systems like Continuous Integration can use `drush cex --no` or `drush:status` as a check prior to performing a site build. By examining the output of the command, a build can be intentionally failed if configuration changes have been made to the site. This way, those changes will not be overwritten when newly deployed configuration is imported.

## Import configuration using Drush

Importing configuration is a very similar operation to exporting when using Drush. The `config:import` (aliases: `cim`, `config-import`) subcommand will import all configuration in the sync directory, overwriting any changes in the active configuration.

To import the configuration using Drush:

### Navigate to your site

Using a local command prompt or an SSH program, navigate to the directory container of your site.

```
cd path/to/your/site
```

### Use Drush to import configuration

Use the Drush configuration import command alias, `cim` to import configuration.

```
drush cim
```

### Note any changes to be made

Enter `y` to accept them, or `n` to reject them.

## Skipping confirmation when importing with Drush

Like the `cex` command, you may skip confirmation for the `cim` command by passing a switch.

To skip confirmation and import configuration:

```
drush cim -y
```

Likewise, you can reject the import operation using `-n` for "no", and inspect the changes to be imported.

For example:

```
drush cim -n
```

## Other useful Drush commands

There are other Drush commands that you may find useful as you manage configuration between instances of the same site. These aren't "config specific", but all the same, might be useful in your configuration management workflow.

### `site:ssh` (aliases: `ssh`, `site-ssh`)

If you are accessing an external server with Drush aliases and SSH access is required to run Git commands, you can use Drush to target the external server using a Drush alias (where you have configured SSH credentials) and running a Git command through SSH. For example, to show changes in Git before pushing those changes:

```
drush @demo.prod ssh git show
```

See the tutorial [Live vs. Local Configuration Management](https://drupalize.me/tutorial/live-vs-local-configuration-management) for details on how to set up Drush aliases.

### `updatedb` (alias `updb`)

Sometimes configuration changes will require a database update, beyond just the *config\** tables (assuming the default active configuration). It can be useful and sometimes necessary to include a `drush updatedb` command in your workflow to ensure that configuration changes are correctly applied to your site.

```
drush @demo.prod updatedb
```

## Workflows and commands for hosted Drupal sites

If you are hosting your Drupal sites on a specific platform, like Acquia Cloud or Pantheon, there may be a particular workflow or even proprietary commands or tools that you must use on those hosting environments. Be sure to check your host's documentation on configuration management.

For example:

- [Configuration management for Drupal on Acquia Cloud](https://docs.acquia.com/cloud-platform/develop/config-drupal/)
- [Configuration Workflow for Drupal 8 Sites on Pantheon](https://pantheon.io/docs/drupal-8-configuration-management/)

## Recap

Using Drush to export or import configuration is not only easy, it is ready-made for use in scripts and in automation systems such as Continuous Integration. By using `drush cex` to export or `drush cim` to import, you can manage your configuration without the need to access the web UI or login.

## Further your understanding

- When doing a database update, should you do an import (`drush cim`) before or after a `drush updb`?

## Additional resources

- [Learn Drush: The Drupal Shell](https://drupalize.me/series/learn-drush-drupal-shell) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Synchronize Configuration with the UI](/tutorial/synchronize-configuration-ui?p=2478)

Next
[Inspect Configuration with Drush](/tutorial/inspect-configuration-drush?p=2478)

Clear History

Ask Drupalize.Me AI

close