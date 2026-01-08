---
title: "Automate Deployment of Configuration"
url: "https://drupalize.me/tutorial/automate-deployment-configuration?p=2478"
guide: "[[drupal-site-administration]]"
---

# Automate Deployment of Configuration

## Content

When automating the deployment of a Drupal site, it's critical to have a good understanding of the configuration management workflow in order for deployments to be consistent and successful.

## Goal

To understand the best practices when creating automated deployment for a Drupal site with reguards to configuration.

## Prerequisites

- [Configuration Sync Directory Setup](https://drupalize.me/tutorial/configuration-sync-directory-setup)
- [Inspect Configuration with Drush](https://drupalize.me/tutorial/inspect-configuration-drush)
- [Configuration Interdependencies](https://drupalize.me/tutorial/configuration-interdependencies)

## Who wins?

Before we can create any automation scripts to deploy our site, we need to decide who is the canonical configuration source. As a developer you might think, "It's the git repo", but a content editor would assume the active configuration on the live site is canonical instead. The underlying question during a site deployment is "Who wins?"

## Scenario 1: The repo wins

When the git repo is considered canonical, any changes made to the live site are lost on a new deployment. This may be preferred if the site configuration is highly controlled, and day-to-day users of the site do not have permissions to create anything that is not content.

The latter is difficult to achieve, simply because many pieces of content and configuration can become interdependent. A custom module may be essential to a content editor, but it results in frequent configuration changes. It is a process to discover which modules result in configuration changes, and if those changes should be preserved to code.

## Scenario 2: The live site wins

In this situation, the live site is considered the authority on what configurations are canonical. The git repository, then, is a managed mirror of the live configurations.

This works well for content editors and sites where non-developers have broad permissions to make configuration changes in the UI. It comes at the cost of additional difficulty for the developer. When doing a deployment, extra care needs to be taken to capture and preserve any configuration changes made, otherwise they will be lost on the next build.

## Scenario 3: Everyone wins (kinda)

Until recently, the above two options were considered the only available. Another option is to use a configuration merge plugin such as [Config Merge](https://www.drupal.org/project/config_merge) that can safely resolve configuration changes on import. This option is new and untested, but it remains an option.

## Config changes from updates

Another thing to consider when automating a deployment with respect to configuration is how to manage changes that result for core or module updates. Many modules and parts of core expect database updates to be run **before** any configuration import operation. The reason for this is that database schemas, internal settings, as well as the layout of configuration itself may change during an update.

For this reason, Drupal sites are often updated twice when automation is used on live. Developers must first locally perform the update. When finished, they need to use `drush cex` to export any configuration changes that have been made. Once these changes have been made to the git repository, the automation script should run all database updates prior to running an import:

```
cd path/to/site
drush updb -y
```

## Best practice automated workflow

While Scenario 1 may work for some sites, Scenario 2 is by far the most tested and permissive. It allows non-technical users to maintain control of the site at the expense of additional consideration when building automated deployment scripts.

Prior to doing any further build work, your script should check if the site's active configuration is out of sync with that on the file system. By doing this as early in the build as possible, the build can be failed quickly without downtime. Checking for configuration changes is surprisingly simple:

```
cd path/to/site
drush cex --no | grep -q identical
```

The above shell code runs a configuration export (`cex`) but forcefully cancels any operation (`--no`). The output of the command is run through the `grep` utility to look for the word `identical`. If found, the command return 1, otherwise it returns 0.

Why `identical`? If there are no changes to export, Drush outputs the following:

```
$ cd path/to/site

$ drush cex --no

The active configuration is identical to the configuration in the export directory (../config/sync).

$
```

We can leverage the output of Drush to get a 1 for there are no configuration changes, and a 0 for when there are. We can then use this to determine if our automation script or pre-commit hook should continue or fail.

Once the state of the config is ensured to be identical, we should run database updates:

```
drush updb -y
```

Next, we can import the configuration, accepting any changes immediately:

```
drush cim -y
```

Finally, we need to rebuild the Drupal cache. The configuration import operation does not necessarily perform a `drush cr`, so we need to do at the end our automation script:

```
drush cr
```

## Recap

Automating configuration deployment isn't difficult, but you do need to decide who is the canonical source of configurations for your site. Often, having the live site itself be canonical is preferred for small teams which non-developer staff members. Check for configuration changes to live early in the build to minimize downtime. Run database updates before any import operation, and finally rebuild the Drupal cache to ensure smooth operation.

## Further your understanding

- Should configuration be backed up on a build?
- If a build fails due to live configuration changes, how can you fix the build?
- If you're using Drush 9, how might you substitue `drush config:status` for `drush cex --no`? Which keyword would you `grep` for instead? (See [Synchronize Configuration with Drush](https://drupalize.me/tutorial/synchronize-configuration-drush) for more info on the differences between the two commands.)

## Additional resources

- [Avoid Deep Hurting! Deployment beyond Git - Drupalcon Baltimore](https://www.youtube.com/watch?v=2K4B48hrYfE)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Set up and Use Configuration Split Module](/tutorial/set-and-use-configuration-split-module?p=2478)

Next
[Reimport Default Configuration during Development](/tutorial/reimport-default-configuration-during-development?p=2478)

Clear History

Ask Drupalize.Me AI

close