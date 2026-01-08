---
title: "Core Migration Modules"
url: "https://drupalize.me/tutorial/core-migration-modules?p=3117"
guide: "[[learn-migrate-drupal]]"
---

# Core Migration Modules

## Content

In Drupal, there are 3 modules in core related to migration that you'll want to know about. These modules can help you import data into Drupal from disparate sources, or upgrade from a previous version of Drupal.

In this tutorial we'll look at what each of these core migration modules do, and talk about when you'll need to use them.

## Goal

Understand the purpose of each of the core migration modules.

## Prerequisites

- [Introduction to Migrations with Drupal](https://drupalize.me/tutorial/introduction-migrations-drupal)

Jump to a module definition:

- [Migrate](#migrate)
- [Migrate Drupal](#migrate-drupal)
- [Migrate Drupal UI](#migrate-drupal-ui)

## Migrate

The **Migrate** module contains the [core Migrate API](https://www.drupal.org/node/2127611), as well as some generic components required for the Migration system to work. This module is required in order to perform any migrations, though it doesn't actually enable the ability to run a migration by itself. It provides a framework for other modules to build on.

The Migrate module defines the various migration plugin types and plugin managers for handling them. Additionally, it defines some process plugins for common operations (setting default values, mapping values, etc.), and destination plugins for Drupal core objects (configuration, entity, URL alias, etc.), and a couple of source plugins (MySQL, static) that serve as a good starting point for your own migrations.

Using a plugin architecture allows individual modules to provide source, process, and destination plugins for their own content. The Block module, for example, contains a destination plugin that any migration can use to save data into the block system, and a source plugin that can be used to extract data from the block system. Breaking the code up this way makes it easier to locate the plugins for specific types of data, and helps to ensure that the module maintainers -- who are likely the most knowledgeable about the data their modules contain -- are the ones telling the migration system how to handle their data.

If you've got questions about the flow of a migration, or implementation-specific details, you'll probably want to dig into the code of this module first.

For more information on the Migrate module:

- Continue viewing the tutorials in this collection. Everything they cover is based off the core Migrate API.
- See the [Migrate API documentation](https://www.drupal.org/node/2127611) on drupal.org, and the [code documentation](https://api.drupal.org/api/drupal/core%21modules%21migrate%21migrate.api.php/group/migration/) on <api.drupal.org>.

## Migrate Drupal

The Migrate Drupal module provides a framework based on the Migrate module to facilitate migration from a Drupal (6, 7, or 8) site to your site running the latest version of Drupal. If you are planning on migrating data from an existing Drupal site into the latest version of Drupal, you'll want to enable this module. If you're migrating from a non-Drupal source you will likely not need this module.

The [Migrate Drupal overview](https://www.drupal.org/documentation/modules/migrate_drupal) page on Drupal.org contains documentation for the Migrate Drupal module.

In previous versions of Drupal, major version *upgrades*, and minor version *updates*, were handled via the [update.php script](https://drupalize.me/videos/updating-drupal-core?p=1181). In the latest version of Drupal, the *update.php* script is only used for minor version updates (8.8.0 to 8.9.0 for example), and the Migrate Drupal UI module now provides the major version upgrade user interface. Individual modules, both core and contributed, are responsible for using the Migrate API to provide an upgrade path for the data and configuration they provide.

While individual modules, like Node for example, are responsible for providing the necessary migrations to upgrade from a previous version of Drupal, the Migrate Drupal module contains some common functionality that many of these modules share. A fieldable entities source plugin that both the Node, and User modules (and any other modules that provide fieldable entities) can use as a starting point for their own source plugins.

The nice thing about this requirement, where individual modules provide their own migration paths, is that if you don't want to migrate the content for a module you can simply disable that module before running the migrations. Additionally, it makes it easier to prepare for and plan a migration because you can track the readiness of individual contributed modules.

## Migrate Drupal UI

This module contains the user interface for performing direct upgrades from older Drupal versions. This modules requires the Migrate Drupal module, and serves the role of providing a simple user interface for running the migrations provided by the Migrate Drupal module.

If you are planning on migrating data from an existing Drupal site into the latest version of Drupal, you'll want to enable this module. If you're migrating from a non-Drupal source you will likely not need this module. Or, you can skip this module completely and use the Drush commands provided by the Migrate Upgrade module to run the migrations in the [Migrate Drupal module with Drush](https://drupalize.me/tutorial/drupal-drupal-migration-drush).

[Learn more about performing a Drupal-to-Drupal migration using the Migrate Drupal UI](https://drupalize.me/tutorial/drupal-drupal-migration-ui).

The UI provided by core is extremely simple, and assumes that you'll be migrating data for all installed modules that support migrations. At the moment, there is not a UI for customizing migrations, so if you want to alter things like field mappings, or skip entire content types you'll have to write code to do that. This, however, is likely to change in the future. The possibility stands for contributed modules to implement a more complex UI. Check out [this list of migration related contributed modules](https://drupalize.me/tutorial/migration-related-contributed-modules) for more information about what's happening in the contributed module space.

## Special note about Migrate Drupal Multilingual

As of Drupal 8.9.0/9.0.0, translation migrations no longer require the experimental Migrate Drupal Multilingual module (migrate\_drupal\_multilingual). This module will be removed in Drupal 10.

Multilingual migrations (tagged with "Multilingual") are stable and available with the core Migrate module and without the need to enable Migrate Drupal Multilingual module.

For more information, see the change record, [#3080264 Multilingual migrations are stable. Migrate Drupal Multilingual module is no longer required.](https://www.drupal.org/node/3080264).

## Recap

In this tutorial we looked at the core modules directly related to migrating data into Drupal. The Migrate module provides the framework for all migrations. The Migrate Drupal and Migrate Drupal UI modules work together to allow for Drupal-to-Drupal migrations.

## Further your understanding

- Do you already know what you're going to be migrating? If so, does it require the Migrate Drupal module or not?
- One of the best ways to understand the API provided by the core Migrate module is to take a look at the [documentation on api.drupal.org](https://api.drupal.org/api/drupal/core%21modules%21migrate%21migrate.api.php/group/migration/), and look at examples of how different core modules are providing migration paths for their data.

## Additional resources

- [Main Migrate module documentation](https://www.drupal.org/upgrade/migrate) (Drupal.org)
- [Migrate API Documentation](https://www.drupal.org/node/2127611) (Drupal.org)
- [Migrate API Documentation](https://api.drupal.org/api/drupal/core%21modules%21migrate%21migrate.api.php/group/migration/) (api.drupal.org)
- Drupal Upgrade UI module has been renamed to Migrate Drupal UI. See [issue #2701541: Rename Drupal Upgrade UI to Migrate Drupal UI](https://www.drupal.org/node/2701541) (Drupal.org).
- [Multilingual migrations now require the Migrate Drupal Multilingual module](https://www.drupal.org/node/2960040) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Migrate to Drupal: Documentation and Examples](/tutorial/migrate-drupal-documentation-and-examples?p=3117)

Next
[Migration-Related Contributed Modules](/tutorial/migration-related-contributed-modules?p=3117)

Clear History

Ask Drupalize.Me AI

close