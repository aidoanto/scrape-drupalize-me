---
title: "Drush Configuration"
url: "https://drupalize.me/tutorial/drush-configuration?p=2593"
guide: "[[command-line-tools-drupal]]"
---

# Drush Configuration

## Content

The Drush executable can be configured through the use of YAML configuration files and environment variables. This configuration can help cut down on typing lengthy frequently-used commands. You can tell Drush to look for command files in project-specific locations. Configuration can also set the value(s) of a specific command's options, instead of having to type them at the command line every time.

In this tutorial we'll:

- Explore different Drush configuration options
- Learn how to configure Drush for your project

By the end of this tutorial, you'll know how to provide project specific, and global, configuration that helps customize Drush and improve your own efficiency.

## Goal

Introduce Drush configuration options and illustrate common use cases.

## Prerequisites

- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)
- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)

## Drush configuration files

Drush-related configuration is stored in a *drush.yml* file in one of a few known locations.

In order of precedence, these include:

- The Drupal *sites/* directory (e.g. *sites/example.com/drush.yml*). **Note:** [*sites/default/* does not currently work](https://github.com/drush-ops/drush/pull/4345).
- *sites/all/drush/drush.yml*, *WEBROOT/drush/drush.yml*, or *PROJECTROOT/drush/drush.yml*
- Any location specified by the `--config` option at run time
- The user's *~/.drush* folder (e.g. *~/.drush/drush.yml*)
- The system-wide configuration folder (e.g. */etc/drush/drush.yml* or *C:\ProgramData\Drush\drush.yml*)

When placed in one of these locations, the file can be automatically discovered and used. One of the most common placements is within the *PROJECTROOT/drush/* directory. Many Drupal hosting providers' documentation for Drush configuration and aliases assume that the files are placed in this directory.

The final configuration used will be the combination of **all** the files found. If multiple files specify a value for the same option, the one higher in the list will be used.

## Drush configuration options

A *drush.yml* file can store the following data:

- Additional configuration files
- Folders that contain Drush commands files
- Folders that contain Drush site aliases files
- Cache directory
- Backup directory
- Global options
- Command specific options
- Non-options

### Environment variables

Drush configuration files may access environment variables via the `${env}` object. It can be used to map values for Drush configuration options, generate paths, and provide access to values specific to a particular environment. For example, to access the value of the *HOME* directory, use `${env.HOME}`. The variables themselves are pulled from the system environment and can be defined via a *.env* file in the root of a project.

### Additional configuration files

You may want to split the configuration between multiple *drush.yml* files. This is especially useful if the main *drush.yml* file in the *PROJECT\_ROOT*/drush\_ directory contains universal configuration tracked by Git while additional files have configuration specific to an individual environment. The configuration snippet to load additional files may look something like below.

```
drush:
  paths:
    config:
      # Load any personal config files. Filename must be drush.yml
      - ${env.HOME}/.drush/config/drush.yml
```

In the example above we load a *drush.yml* file that is global for a particular environment rather than a particular Drupal project.

### Paths to Drush commands

Command files that are located outside the standard autoloader locations can be loaded as additional includes using the `include` configuration key.

Example:

```
drush:
  include:
    - '${env.HOME}/.drush/commands'
```

**Note:** the configuration expects a path to a command files directory, not an individual file.

### Paths to Drush site aliases directories

Site aliases files that are located outside the standard autoloader locations can be loaded using the `paths` key and `alias-path` sub-key. We cover the topic of aliases in depth in [Drush Site Aliases](https://drupalize.me/tutorial/drush-site-aliases).

Example:

```
drush:
  paths:
    alias-path:
      - '${env.HOME}/.drush/sites'
```

**Note:** the configuration expects a path to an aliases files directory, not an individual file.

### Cache and backup directories

Cache directory specifies where Drush stores its file-based caches. Backup directory specifies where Drush stores backups, including temporary SQL dumps.

Example:

```
drush:
cache-directory: /tmp/.drush
backup-dir: /tmp/drush-backups
```

These configuration options have reasonable defaults and typically don't need to be changed. Consult with your hosting provider documentation before changing the values.

### Global options

Global options control global settings for all Drush commands such as web root directory, site URI, and verbose mode. It's useful to specify at least the URI option to allow for clean generated URLs. Global configuration is defined under the `options` key. The keys correspond to the available options found when running `drush topic core:global-options`.

Example:

```
options:
  # Specify the base_url that should be used when generating links.
  uri: 'https://my-site.com/web'

  # Specify your Drupal core base directory (useful if you use symlinks).
  root: '/home/{USER}/sites/drupal'

  # Enable verbose mode.
  verbose: true
```

### Command-specific options

Command-specific options allow you to hardcode values for frequently used command options. For example, you could pass options to the `sql:dump` command, or define site username and email for the `site:install` command. This allows you to avoid typing the same configuration over and over again and reduces the risk of typos.

Example:

```
command:
site:
    install:
      options:
        # Set a predetermined username and password when using site:install.
        account-name: 'admin'
        account-pass: 'password'
```

The configuration is defined under the `command` key, and then it's grouped by the command group key (such as `site`, `sql`, `cache` etc.), and command name sub-key.

### Non-options

*Non-options* is configuration that is consulted by various commands outside the regular Drush command options system. This includes things like a list of tables to skip for all `sql*` commands, or options to pass to the `ssh` binary for all commands that use the SSH backend.

If you'd like to learn more about non-options configuration refer to the [official Drush documentation](https://www.drush.org/latest/using-drush-configuration/) on this topic. This documentation also includes example values and configuration snippets to use in the *drush.yml* file.

If you'd like a head start on your own *drush.yml* configuration file you can [download one from the Drush website](https://www.drush.org/latest/examples/example.drush.yml/) which includes a bunch of common examples -- and start editing it.

## Drush site aliases

Drush site aliases provide a way for teams to bundle common configuration for remote environments under short names that refer to the `@live`, `@stage`, `@dev`, and any other environments for a project. Site aliases are a type of configuration, but are complex enough to deserve a tutorial of their own. Learn more in [Drush Site Aliases](https://drupalize.me/tutorial/drush-site-aliases).

## Recap

Drush can be configured through the use of *drush.yml* files to help save time and reduce errors when executing frequently used commands. Configuration files can access environment variables, and hardcode values for global and command-specific options. They also allow defining paths to directories with additional configuration files, command files and site aliases files.

## Further your understanding

- Can you configure Drush to skip the content of the user table whenever `sql*` commands are run?
- Learn more about configuring Drush to execute commands on a remote environment using [Drush Site Aliases](https://drupalize.me/tutorial/drush-site-aliases).

## Additional resources

- [Drush official documentation](https://www.drush.org) (drush.org)
- [Drush Git repository](https://github.com/drush-ops/drush) (github.com)
- [Drush configuration system repository](https://github.com/consolidation/config) (github.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Drush Site Aliases](/tutorial/drush-site-aliases?p=2593)

Next
[Develop Drupal Modules Faster with Drush Code Generators](/tutorial/develop-drupal-modules-faster-drush-code-generators?p=2593)

Clear History

Ask Drupalize.Me AI

close