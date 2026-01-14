---
title: "Migration-Related Contributed Modules"
url: "https://drupalize.me/tutorial/migration-related-contributed-modules?p=3117"
guide: "[[learn-migrate-drupal]]"
order: 37
---

# Migration-Related Contributed Modules

## Content

There's a whole ecosystem of contributed modules that build on the Migrate API in Drupal core. They do things like provide Drush commands for working with migrations, add new sources (CSV, JSON, etc.), add new destinations, provide code examples, and fill in other gaps. Think of these as the tools of the trade you’ll use to do your work. In most cases you’ll use these to do the migration, but then once the migration is complete you can remove them from your project.

Then there are the contributed modules that add features to your site. Like Flag, Paragraphs, or Webform. These modules often contain migration-related code that is intended to help make it easier to handle data specific to these modules. There is code in the Flag module, for example, that can help with knowing how to extract flagging records from Drupal 7, and for transforming that data into the format the module expects it to be in for Drupal 10. You might end up having to tweak it a bit, but at least you’re not starting from scratch.

In this tutorial we'll:

- Look at some of the most commonly used *toolset* modules.
- Explain what you can expect to find in standard contributed modules related to migrations.

By the end of this tutorial you should have a better sense of the various tools available to you for authoring a migration.

## Goal

List contributed modules that are useful to anyone working on a Drupal migration.

## Prerequisites

- [Introduction to Migrations with Drupal](https://drupalize.me/tutorial/introduction-migrations-drupal)
- [Core Migration Modules](https://drupalize.me/tutorial/core-migration-modules)

Jump to a module:

- [Migrate Tools](#migrate-tools)
- [Migrate Upgrade](#migrate-upgrade)
- [Migrate Plus](#migrate-plus)
- [Media Migration](#media-migration)
- [Migrate Manifest](#migrate-manifest)
- [Migrate API](#migrate-api)
- [Migrate Source CSV](#migrate-source-csv)

## The big three

While there are many contributed modules related to migrations, we expect you'll end up using one or all of these three for every migration — at least until the functionality they provide is also moved into Drupal core.

### Migrate Tools

**Project page:** <https://www.drupal.org/project/migrate_tools>

**Note:** As of Drush version 10.4+ these commands are included in Drush core and you likely do not need this module.

The Migrate Tools module provides Drush commands for running and rolling back custom migrations.

Drupal core does not provide a means for running custom migrations at the moment, and instead focuses on Drupal-to-Drupal migrations. If you want to run any custom migrations either via Drush or the UI you'll want to install this module.

### Migrate Upgrade

**Project page:** <https://www.drupal.org/project/migrate_upgrade>

The Migrate Upgrade module provides Drush commands for running Drupal-to-Drupal migrations. These commands can be used in place of the [UI provided by Drupal core](https://drupalize.me/tutorial/core-migration-modules) for running a Drupal-to-Drupal migration. In our recent experience, using the Drush commands to run migrations has proven to be more reliable than the UI.

You'll want to install this module if you're migrating from an older version of Drupal. However, if you're migrating from a non-Drupal source you won't need this module.

[Learn more about running migrations from older versions of Drupal using Drush](https://drupalize.me/tutorial/drupal-drupal-migration-drush).

### Migrate Plus

**Project page:** <https://www.drupal.org/project/migrate_plus>

The Migrate Plus module extends the core Migrate framework to add additional useful functionality.

The URL source plugin can be used as a starting point for importing from XML, JSON, and SOAP data sets. And is the current recommended way to work with those formats. [Learn more](http://drupalsun.com/mikeryan/2016/06/08/drupal-8-plugins-xml-and-json-migrations).

The Migrate Plus module also provides two example modules, *migrate\_example*, and *migrate\_example\_advanced* which demonstrate how you can write source, destination and process plugins as well as migration plugins. If you're familiar with the Drupal 7 migrate module these are the updated versions of the [Beer and Wine example modules](https://drupalize.me/videos/review-migrate-example-modules?p=1271).

## Additional contributed modules

There are a lot of other contributed modules that might help you out, depending on the specific needs of your migration. You'll want to read the project page and take a quick look at the open issues for each when deciding if the module is ready for use.

### Media Migration

**Project page:** <https://www.drupal.org/project/media_migration>

This module provides a Drupal 7 to Drupal 8|9|10 migration path for the Drupal 7 Media module. It can also help with migrating Drupal 7 image fields to Drupal 8+ Media Entities and Media reference fields. It provides a bunch of helpful process plugins for dealing with things like images embedded via WYSIWYG and other things media-related.

### Migrate Manifest

**Project page:** <https://www.drupal.org/project/migrate_manifest>

The Migrate Manifest module provides a Drush command that can be used for running migrations using a manifest file. The manifest file contains a list of one or more individual migrations that you would like to run. This lets you run groups of migrations in a reproducible manner. This looks like promising functionality once it is updated to be compatible with Drupal core 8.1.x.

### Migrate API

**Project page:** <https://www.drupal.org/project/migrate_api>

The Migrate API module is intended to provide "generic functionality for Migrate in contrib and helper services that can be used by runners, UI's and more". At the moment it's a work in progress. What you're likely to see is that in the future other migration-related modules will depend on the Migrate API module for shared functionality, much like CTools and its many dependencies.

For now you probably don't need this module, but it's worth keeping any eye on to see what additional functionality gets added. Our suggestion: before you start writing custom code to add new features to a migration, see if it exists in this module already.

### Non-Drupal sources

Migrating from non-Drupal sources? These modules provide source plugins for common data types. On their own they're not likely to do much, but you can use them when you start writing custom migrations as a way to extract source data.

The Migrate Plus module listed above contains a number of helpful source plugins for dealing with REST APIs, JSON data, XML data, and more. Check there first.

### Migrate Source CSV

**Project page:** <https://www.drupal.org/project/migrate_source_csv>

The Migrate Source CSV module provides the ability to use CSV (or other tab delimited) files as the source data for a migration.

### Deprecated modules

These modules used to be in our recommended list but have since been replaced.

- [Migrate Source XML](https://www.drupal.org/project/migrate_source_xml): For XML based migrations use the URL source in Migrate Plus.
- [Migrate Source JSON](https://www.drupal.org/project/migrate_source_json): For JSON based migrations use the URL source in Migrate Plus.

## Modules that have their own migration paths

In addition to the modules that help you author a migration there are the modules you use to build your site, like Flag, Paragraphs, and Webform. These modules, which also have Drupal 7 versions, are responsible for providing a migration path for the data that they maintain. In short, if you have Flag installed in Drupal 7 and not in Drupal 10 don't expect the Flag-related data to get moved over.

If you're writing a custom migration that migrates data for a contributed module check if that module provides any migrate API plugins you can use to help. Check the *src/Plugin/migrate* directory of the module in question.

Also note that sometimes, like in the case of Webform, the main module itself doesn't have a migration path. But there's another contributed module [Webform: Migrate](https://www.drupal.org/project/webform_migrate) that does.

## Recap

There are a growing number of contributed modules intended to help make migrations easier. At this point, most of them provide methods for running migrations via the UI and Drush commands, or new plugins for different data sources. Keep an eye on these modules, and others that are added into the Import/Export category on Drupal.org, as there are likely to continue to be new tools added at a rapid pace. Before you start writing custom code for migration features, make sure you search and see if someone else is working on something similar already.

## Further your understanding

- If you're going to be writing code for migrations it's worthwhile to take the time to read and understand the example code in the Migrate Plus module.
- It's common to have entire contributed modules that do nothing but implement new source plugins, but rare to have them implement a destination plugin. That's because destination plugins should almost always live in the module that defines the data type itself instead of in a separate module. So while it's not immediately obvious, if you start poking around, many contributed modules (especially those that store data) provide destination plugins.

## Additional resources

- [Drupal 8 (or later) migrate modules](https://www.drupal.org/docs/upgrading-drupal/drupal-8-or-later-migrate-modules) (Drupal.org)
- [Filter the list of modules to those in the Import/Export category that are compatible with Drupal 9](https://www.drupal.org/project/project_module?f%5B0%5D=&f%5B1%5D=&f%5B2%5D=im_vid_3%3A64&f%5B3%5D=sm_core_compatibility%3A9&f%5B4%5D=sm_field_project_type%3Afull&f%5B5%5D=&f%5B6%5D=&text=&solrsort=iss_project_release_usage+desc&op=Search) to find some additional migration-related modules. (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Core Migration Modules](/tutorial/core-migration-modules?p=3117)

Clear History

Ask Drupalize.Me AI

close