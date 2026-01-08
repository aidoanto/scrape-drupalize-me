---
title: "Migrate System: Terms and Conceptsfree"
url: "https://drupalize.me/tutorial/migrate-system-terms-and-concepts?p=3117"
guide: "[[learn-migrate-drupal]]"
---

# Migrate System: Terms and Conceptsfree

## Content

To follow along with the rest of the migration tutorials you'll want to make sure you understand the following concepts and terms as they relate to Drupal migrations.

In this tutorial, we'll take look at the basic components of a migration and familiarize ourselves with some of the concepts and terminology needed to understand how the system works. We'll cover:

- What is a migration?
- Migration templates
- The extract, transform, load process
- Destinations and sources
- Additional Drupalisms

By the end of this tutorial you should be able to identify the various components that a migration is composed of, and explain at a basic level what each is responsible for.

## Goal

Explain the components that make up a Drupal migration so that when you encounter them while learning how to write migrations you'll know what they mean.

## Prerequisites

- [Introduction to Migrations with Drupal](https://drupalize.me/tutorial/introduction-migrations-drupal)

## Contents

- [Migration](#migration)
- [Drupal-to-Drupal Migration](#drupal-to-drupal-migration)
- [Migration plugins](#migration-plugins)
- [Extract, Transform, Load](#etl)
- [Source plugins](#source)
- [Process plugins](#process)
- [Destination plugins](#destination)
- [Upgrade path](#upgrade-path)
- [Execute and rollback](#execute-rollback)
- [Highwater marks](#highwater)

Sprout Video

## Migration

Defining the term "Migration" is complex, and its exact meaning depends on the context in which it's used.

We use to it describe the entire process of importing content to Drupal. Example: "I'm going to perform a Drupal 7 to Drupal 9 migration."

We also use the term migration to represent the definition of how a particular subset of data flows from a source into Drupal. Example: "The Flag module provides a migration path for its own data."

In general, a migration imports data from some alternate source into your destination Drupal site that uses the latest version of Drupal.

## Drupal-to-Drupal Migration

Unlike previous versions of Drupal, there is no direct upgrade path for Drupal 6 or 7 to the current version of Drupal. Moving content from previous Drupal versions (Drupal 7 or previous) to the latest Drupal version (Drupal 8 or later) should utilize the Migrate system.

Using the Migrate Drupal module allows you to migrate all content (with supported upgrade paths) to the latest version of Drupal.

If you want to learn more about this change and why it was made you can:

- Read our tutorial, [Custom Drupal-to-Drupal Migrations](https://drupalize.me/tutorial/custom-drupal-drupal-migrations)
- Read [a blog post we wrote about it](https://drupalize.me/blog/201412/drupal-8-upgrade-path).
- Mike Ryan also wrote [a blog post](http://virtuoso-performance.com/blog/mikeryan/migration-update-drupal-81) that covers some of the reasoning, and [this really long issue](https://www.drupal.org/node/2313651) provides a lot of additional background.

## Migration plugins

Each individual module is responsible for its own content and configuration, and needs to describe to the migration system both the data and how to access it. A migration template provides a set of instructions the migration system can use to map the path that a set of data needs to take to get from the source to the destination.

Migration templates are stored in the `module_name/migrations` sub-directory of a module. (For backward compatibility they may also appear in `module_name/migration_templates`.) They are plugins, described in YAML files, and are responsible for determining how to source, process, and import data in to your destination Drupal site that uses the latest version of Drupal.

Look at `Drupal/core/modules/file/migrations/d6_file.yml` for an example. This plugin defines which source, process, and destination plugins to use, and configuration for each.

## Extract, Transform, Load

Migrating data to a site using the latest version of Drupal follows what is known as an [ETL process](https://en.wikipedia.org/wiki/Extract,_transform,_load). This stands for Extract, Transform, and Load, and is a pattern used in many aspects of computing. The basic flow of the process is as follows:

```
[Extract] --> [Transform] --> [Load]
```

The *Extract* phase is where data is extracted from a data source: this might be a previous Drupal version, or some other form of data store, a database, XML, CSV, or YAML, to list just a few.

The *Transform* phase of a migration is the stage in which source data is manipulated, prior to being imported to its final destination.

The *Load* phase is the stage of the process where data is inserted into Drupal. This phase is handled by *destination plugins*.

In terms of a Drupal migration, the process is controlled by three types of plugins:

```
[Source] --> [Process] --> [Destination]
```

## Source plugins

The extract phase in the Drupal migrate system is handled by *source plugins*. Source plugins extract data from a source and return it as a set of rows representing an individual item to import and some additional information about the properties that make up that row.

Learn more about [Source Plugins in this tutorial](https://drupalize.me/tutorial/source-plugins).

## Process plugins

In a Drupal migration the transform phase is handled by *process plugins*. Each row of data provided by a source plugin will be passed through one or more process plugins which operate on the source data to transform it into the desired format. This result is then passed to a destination plugin during the load phase.

Learn more about [Process Plugins in this tutorial](https://drupalize.me/tutorial/process-plugins).

## Destination plugins

In the context of a Drupal migration, the load phase is handled by *destination plugins*, which are responsible for saving new data as Drupal content or configuration.

Learn more about [Destination Plugins in this tutorial](https://drupalize.me/tutorial/destination-plugins).

**Note:** In Drupal parlance the term *load* is generally used to represent any action that retrieves data from the database and loads it into memory. For example, loading a node. In this particular case *load* refers to the process of taking data from memory and loading, or saving, it into the database.

## Upgrade path

If modules have support for migrating data to the latest version of Drupal, they are said to have an "Available Upgrade Path".

Modules that do not support migrating data from previous Drupal versions are said to have a "Missing Upgrade Path".

## Execute and rollback

Migrations are performed (executed) via the Drupal UI, or using Drush.

Once a migration has run, it can also be "Rolled back" to remove anything imported during the migration, and provide you with a clean slate.

## Highwater marks

The Drupal migration system supports highwater marks, which are used to support continuous upgrades. These highwater marks are used as a sanity check for imported content. If a highwater mark exists for the import, the content will not be reimported unless changed.

With Drupal 7 Nodes for example, the data used as the highwater mark is the `node_last_changed` field.

## Recap

In this tutorial we defined some common terminology that anyone working on a Drupal migration project should be familiar with. Knowing these terms will make it easier for you to read documentation — and to find the help you need.

## Further your understanding

- What is the responsibility of a source plugin?
- Explain to a colleague how Drupal uses the Extract, Transform, Load process during a migration.

## Additional resources

- [Migration handbook](https://www.drupal.org/upgrade/migrate) (Drupal.org)
- The [API documentation](https://api.drupal.org/api/drupal/core%21modules%21migrate%21migrate.api.php/group/migration/) contains more information about plugins and how they relate to the ETL process (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Introduction to Migrations with Drupal](/tutorial/introduction-migrations-drupal?p=3117)

Next
[Migrate to Drupal: Documentation and Examples](/tutorial/migrate-drupal-documentation-and-examples?p=3117)

Clear History

Ask Drupalize.Me AI

close