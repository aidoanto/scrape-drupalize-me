---
title: "Automating Drupal Tasks with Drush and Bash Scripts"
url: "https://drupalize.me/tutorial/automating-drupal-tasks-drush-and-bash-scripts?p=2593"
guide: "[[command-line-tools-drupal]]"
---

# Automating Drupal Tasks with Drush and Bash Scripts

## Content

While Drush empowers all Drupal users with its commands, it's even more powerful when used in combination with scripting solutions such as Composer and Bash. Scripts can be used to power post-deployment tasks like importing new configuration or clearing the cache, as part of CI processes to sync a database from one environment to another, to run background processes on the server such as imports and migrations, search indexing, running cron, and much more. If you want to write Bash (or any other scripts) that interact with a Drupal site, then Drush is the tool for you.

In this tutorial we'll:

- Learn how to use Drush commands within Composer and Bash scripts
- Learn how to chain multiple Drush commands together in a script

By the end of this tutorial you'll know how to use Drush as part of a script that automates common or tedious tasks.

## Goal

Introduce Drush scripting methods to developers and explain their corresponding use cases.

## Prerequisites

- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)
- [Composer](https://drupalize.me/topic/composer)
- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)

## History of scripting methods for Drush

Prior to Drush version 9, scripting with Drush was supported by Drush shell aliases. A Drush shell alias is a shortcut to any Drush command, or any shell command. Using Drush shell aliases allowed users to chain Drush and Bash commands together and run them later by calling the alias in the command line.

For Drush 9 and up, the shell alias system has not been ported. The community has explored many options that can be reviewed in this [GitHub issue](https://github.com/drush-ops/drush/issues/2943). Since the work on the original issue has been postponed, scripting options for Drush have moved towards Bash scripts and Composer scripts. In our experience, even for older versions of Drush, we tend to prefer writing Bash (*.sh*) scripts that execute Drush commands alongside any other required commands, and then either call those scripts directly like `./scripts/deploy.sh`, or via Composer like `composer run deploy`.

## Drush Bash scripts

A Bash script is a collection of shell commands that need to run in a specific order. When grouped together in a script, they can be executed all together, saving time over calling the commands one by one. These scripts can be useful for deployment routines, backup scripts, syncing files and databases, setting up new local development websites, running security updates, syncing configuration, and more.

Once installed, Drush acts like any other Bash command and can be called from within a script. Multiple Drush commands can be chained together and mixed with other commands.

Anytime you anticipate someone will run a set of commands in a specific order in the future, it's probably a good idea to script it.

Here's an example script mixing Drush and other common shell commands together:

```
#!/bin/bash
echo "Running database backup procedures"
drush sql-dump --result-file backup.sql
echo "Running database update procedures"
drush updb --yes
echo "Copy all files / directories from one server to other"
rsync -avz --progress username@servername:sourcefolder destinationfolder
drush cr
drush cim sync --yes
npm it
```

This script can be placed in any convenient folder on your machine or server environment. If the script is generic and meant to be used for multiple websites we recommend you place it in a directory accessible to all the sites, e.g. *~/bin* or something similar. If it's specific to a project, or you want everyone to have access to it, we usually put these in a */scripts* directory in the root of our project's Git repository.

**Note:** Consult with your environment configuration to make sure certain extensions and frameworks are installed and configured prior to calling them in the script. For example, the script above expects NPM to be installed.

Because of the Drush commands it contains, this script will only work when run within a directory containing a functional Drupal installation. In a typical setup, Drupal might live in the */web* directory, and scripts in the */scripts* directory of your repository. In this scenario, scripts could be executed from within the */web* directory by calling them at the command line like `./../scripts/script-name.sh`.

Before executing the script you need to make the script file executable. If your script file is called *deploy.sh* then it can be made executable by running the following command from the command line: `chmod u+x deploy.sh` from the directory where the script is located.

Once created, these Bash scripts can run by developers on-demand, as a custom cron task, or as part of a CI/CD process.

## Drush Composer scripts

A Composer script is either a PHP callback defined as a static method or a command line executable command listed in the `scripts` section of a project's *composer.json* file. These scripts can be called manually using `composer run {SCRIPT}`, or automatically during the Composer execution process by following a specific naming convention.

Here's an example `scripts` section from a Drupal project's *composer.json* file:

```
…
"scripts": {
    "pre-install-cmd": [
        "DrupalProject\\composer\\ScriptHandler::checkComposerVersion"
    ],
    "pre-update-cmd": [
        "DrupalProject\\composer\\ScriptHandler::checkComposerVersion"
    ],
    "post-install-cmd": [
        "DrupalProject\\composer\\ScriptHandler::createRequiredFiles",
        "./scripts/deploy.sh"
    ],
    "post-update-cmd": [
        "DrupalProject\\composer\\ScriptHandler::createRequiredFiles",
        "./scripts/deploy.sh"
    ],
    "deploy": [
        "./scripts/deploy.sh"
    ]
},
...
```

All of the `DrupalProject\\` entries are part of the Drupal-recommended projects template and handle things like scaffolding required files that are not part of version control.

In this example we've added a Bash script named *deploy.sh*. We've connected the script's execution to specific Composer events: `post-install-cmd` and `post-update-cmd`. So it'll run automatically when either `composer install` or `composer update` are used. It also has its own stand-alone alias `deploy`, so it can be run like: `composer run deploy`.

To read more about all the possible events, refer to the [Composer scripts documentation](https://getcomposer.org/doc/articles/scripts.md).

The benefits of this approach are that you can:

- Tie the execution of a script to Composer events. For example, run all database updates automatically after pulling in updated modules with `composer update`.
- Provide a single source where developers on a team can look for scripts related to the current project.

## Recap

In this tutorial we covered the basics of scripting with Drush. We learned how to create Bash scripts and call multiple Drush commands one after another by bundling them in one script. We saw how to mix Drush commands with simple shell commands. Then we covered how to execute a Bash script as a Composer script and connect it to one of the Composer event hooks.

## Further your understanding

- We attached a script to a pre-defined Composer event. What would you do to attach the script to a custom event?
- Our Bash script has to be run from a functional Drupal installation. What modifications can be done to the script to make it more generic and possible to run from outside the Drupal installation folder?

## Additional resources

- [Drush official documentation](https://www.drush.org) (drush.org)
- [Drush Git repository](https://github.com/drush-ops/drush) (github.com)
- [Composer scripts documentation](https://getcomposer.org/doc/articles/scripts.md) (getcomposer.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview: Drush's Output Formatting System](/tutorial/overview-drushs-output-formatting-system?p=2593)

Next
[Drush Site Aliases](/tutorial/drush-site-aliases?p=2593)

Clear History

Ask Drupalize.Me AI

close