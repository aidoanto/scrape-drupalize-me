---
title: "Overview: Configuration Management in Drupalfree"
url: "https://drupalize.me/tutorial/overview-configuration-management-drupal?p=2478"
guide: "[[drupal-site-administration]]"
order: 2
---

# Overview: Configuration Management in Drupalfree

## Content

Drupal stores many of your site's settings, such as content types, views, roles, and image styles, as **configuration**. When you're working with multiple environments or collaborating with a team, you need a reliable way to move those configuration changes from place to place. Drupal's **configuration management system** provides tools to export, track, and import configuration, keeping your site consistent from local development to the live site and enabling you to test configuration changes safely in a development environment and deploy them in code to the live site.

In this tutorial, we'll introduce the configuration management workflow in Drupal and explain how to synchronize your configuration across environments.

## Goal

Understand at a high level what configuration management is in Drupal and how it helps you keep configuration synchronized across environments.

## Prerequisites

- None.

## What is configuration management?

Configuration management is the process of **moving configuration changes** (for example, updated content types or views) from one Drupal site environment to another. Drupal stores configuration as YAML files when exported, allowing you to version, review, and deploy these changes alongside your custom code.

Configuration management is beneficial when:

- More than one person works on a site
- You maintain separate environments (local, dev, stage, prod)
- You want predictable, reviewable deployments

Configuration is different from content. Content changes happen on the live site. Configuration changes usually occur during development when working on a new feature or updating site configuration using the administrative UI.

## Where is configuration data stored?

Drupal stores configuration in two places:

1. **Active configuration:** The configuration currently being used by the site.
2. **Exported configuration:** A set of YAML files that represent those settings. These files can be committed to version control and deployed across environments.

The configuration management workflow is built around **exporting** YAML files from one site and **importing** them into another. To enable this workflow, you will need to set up a clone of your site (codebase and database), create a configuration sync directory outside the docroot, and update the configuration sync directory value in your site's *settings.php* file.

Learn more:

- [Configuration Sync Directory Setup](https://drupalize.me/tutorial/configuration-sync-directory-setup)
- [Create a Clone of Your Drupal Site with Drush and Git](https://drupalize.me/tutorial/clone-your-drupal-site-drush-and-git)
- [Clone a Drupal Site using Web-Based Tools](https://drupalize.me/tutorial/clone-drupal-site-using-web-based-tools)

## Tools for managing and deploying configuration

There are two tools available to synchronize (export and import) and inspect configuration:

1. **Admin UI:** Export and import configuration using the Configuration synchronization admin UI.
2. **Drush commands:** Use commands like `drush config-export` and `drush config-import` for faster, scriptable workflows.

Get started with the fundamentals of managing and inspecting configuration:

- [Synchronize Configuration with the UI](https://drupalize.me/tutorial/synchronize-configuration-ui)
- [Synchronize Configuration with Drush](https://drupalize.me/tutorial/synchronize-configuration-drush)
- [Inspect Configuration with Drush](https://drupalize.me/tutorial/inspect-configuration-drush)

To understand and set up more complex **configuration management, development, and deployment workflows**, including environment-specific configuration overrides, dig into these tutorials:

- [Live vs. Local Configuration Management](https://drupalize.me/tutorial/live-vs-local-configuration-management)
- [Configuration Interdependencies](https://drupalize.me/tutorial/configuration-interdependencies)
- [How to Override Configuration](https://drupalize.me/tutorial/how-override-configuration)
- [Set Up and Use Configuration Split Module](https://drupalize.me/tutorial/set-and-use-configuration-split-module)
- [Automate Deployment of Configuration](https://drupalize.me/tutorial/automate-deployment-configuration)
- [Reimport Default Configuration during Development](https://drupalize.me/tutorial/reimport-default-configuration-during-development)

## Recap

Configuration management helps you reliably and consistently move Drupal site configuration—such as content types, views, and roles—between environments. By exporting configuration to YAML files and importing them elsewhere, you maintain a stable, predictable configuration workflow as your site evolves.

## Further your understanding

- Which parts of your site change regularly during development, and how would exporting configuration help you track those changes?
- How many environments does your project use, and how does configuration currently move between them?

## Additional resources

- [Synchronizing Configuration Versions (Drupal User Guide)](https://drupalize.me/tutorial/user-guide/extend-config-versions?p=2357) (Drupalize.Me)
- [Chapter 9: Working with Data (Module Developer Guide)](https://drupalize.me/guide/drupal-module-developer-guide) (Drupalize.Me)
- Course: [Configuration API in Drupal](https://drupalize.me/course/configuration-api-drupal) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Configuration Sync Directory Setup](/tutorial/configuration-sync-directory-setup?p=2478)

Clear History

Ask Drupalize.Me AI

close