---
title: "Use Drush to Deploy Drupal Updates"
url: "https://drupalize.me/tutorial/use-drush-deploy-drupal-updates?p=2593"
guide: "[[command-line-tools-drupal]]"
order: 14
---

# Use Drush to Deploy Drupal Updates

## Content

One of the problems that Drush solves for developers is the automation and optimization of routine tasks. Drush commands attempt to speed up workflows and tasks that developers and site maintainers would otherwise have to do manually through the UI, or run one-by-one via the command line. One of those tasks is the process of deploying changes to a Drupal application from one environment to another.

The typical Drupal deployment process consists of repeatable steps such as importing configuration changes, applying database updates, and clearing the cache. Drush comes with the handy `drush deploy` command that allows you to automate the execution of all of these tasks post code deployment.

In this tutorial we'll:

- Learn about the `drush deploy` command
- Discuss when you would use the `deploy` command

By the end of this tutorial you'll know how to use the `drush deploy` command in conjunction with other useful deployment-related commands to help automate the task of deploying changes to a Drupal site's configuration and code.

## Goal

Introduce Drush deploy command and illustrate some common use cases.

## Prerequisites

- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)
- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)

## The Drush deploy command

The `drush deploy` command helps standardize, automate, and simplify the deployment process. This command is meant to be run when a code deployment is done to one of your environments. The most common implementation would be as part of a CI script that builds the latest code artifacts, deploys them to an environment, and then needs to update the Drupal site's configuration and database schema to match what's in the new code.

In a nutshell, the `drush deploy` is actually a collection of other Drush commands run in a specific order. The list of commands is as follows:

```
drush updatedb --no-cache-clear
drush cache:rebuild
drush config:import
drush cache:rebuild
drush deploy:hook
```

The main reason to use `drush deploy` rather than the above set of commands in your deployment scripts to ensure that these commands are run in a consistent order. It's imperative to update the database schema *before* importing configuration changes.

Developers can also pair the command with an appropriate update hook that is invoked during the different stages of deployment. The hooks that are invoked by this command are as follows:

- `HOOK_update_n()` - runs during the database update process (`drush updatedb`). Code defined in this hook cannot interact with Drupal API. Primarily used for database schema changes.
- `HOOK_post_update_NAME()` - runs before configuration is imported (also triggered by `drush updatedb`). This code can utilize Drupal APIs. Used when you need to perform operations on a fully bootstrapped Drupal application.
- `HOOK_deploy_NAME()` - runs after the configuration is imported (`drush config:import`). This is a Drush-provided hook that executes one-time functions that run after configuration is imported during a deployment. These are a higher level alternative to `HOOK_update_n()` and `HOOK_post_update_NAME()` functions. For a detailed comparison refer to the [official Drush documentation](https://www.drush.org/latest/deploycommand/#authoring-update-functions) about authoring update functions.

## Other useful deployment related commands

While `drush deploy` covers the majority of post code deployment tasks, there are a couple more tasks that Drush can help with. One of them could be a backup of the database.

We recommend calling the `drush sql:dump` command prior to `drush deploy` so that you can revert to a database backup in case something goes wrong during the deployment.

Another command that might be useful to run is `drush:cron`. This command initiates a cron run. While not required for all deployments, it might be useful to run post `drush deploy` in case you deployed modules or code changes that rely on cron. For example, if you need to re-index the site, and you are not using the Search API module for search functionality on your site. The `drush cron` command is typically chained after `drush deploy`.

If the Search API module is used for the site's search functionality, you may want to chain its Drush commands in order to initiate re-indexing of the site after the deployment and `drush deploy` call.

The commands can be chained as part of a CI Bash script or a Composer script. Refer to [Automating Drupal Tasks with Drush and Bash Scripts](https://drupalize.me/tutorial/automating-drupal-tasks-drush-and-bash-scripts) to learn more about how to chain multiple Drush commands together.

## Recap

Drush provides a way to standardize, simplify, and automate post-deployment tasks for developers. The `drush deploy` command should be called after code has been deployed and chains together common post-deployment commands such as database updates, configuration imports, and clearing the cache. It also invokes optional deploy hooks.

## Further your understanding

- How would you pass options to the child commands of `drush:deploy`?
- Write a Composer script to chain together the `drush sql:dump` command and `drush deploy` command.
- Are there any other steps that are part of your deployment process that could be scripted with Drush?

## Additional resources

- [Drush official documentation](https://www.drush.org)
- [Drush Git repository](https://github.com/drush-ops/drush)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Use Drush to Speed up Common Drupal Development Tasks](/tutorial/use-drush-speed-common-drupal-development-tasks?p=2593)

Next
[Overview: Drush's Output Formatting System](/tutorial/overview-drushs-output-formatting-system?p=2593)

Clear History

Ask Drupalize.Me AI

close