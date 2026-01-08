---
title: "a source"
url: "https://drupalize.me/tutorial/source-plugins"
guide: "[[learn-migrate-drupal]]"
---

# a source

## Content

Source plugins extract data from a source and return it as a set of rows representing an individual item to import and some additional information about the properties that make up that row.

Anyone writing a custom migration, or module developers who want to provide a migration path from their Drupal 6 or 7 module, will need to work with source plugins.

In this tutorial we'll talk about the role that source plugins fulfill and how they work. By the end of this tutorial you should be able to determine whether or not you need to write a source plugin for your migration.

Sprout Video

## Goal

Explain how source plugins work and the role they play.

## Prerequisites

- [Migrate System: Terms and Concepts](https://drupalize.me/tutorial/migrate-system-terms-and-concepts)
- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins)

## What is a source plugin?

Source plugins understand your existing data. They know how to extract the data from whatever storage it currently resides in. They know what each of the fields represents, how tables join together to create a complete record, and what that archaic file naming convention really means. Source plugins use this knowledge of your existing data in order to present the Migrate API with individual data records that represent a unique object to be imported.

A source plugin extracts data from a source as a row with properties. Each row can be operated on individually, and each property is defined in a way that allows other components in the system to know what properties exist. The source might be a previous Drupal version, or some other form of data store, a database, XML, CSV, or YAML, to list just a few.

How about a couple of examples?

- Given a CSV file as a source, a source plugin can iterate over the file returning each line one at a time and inform the rest of the system that the first column is a name, and the second column is a birthday.
- Given a custom database, a source plugin can query the database, join the users table with the email\_address table and select the appropriate columns to create an individual record that contains both the user's profile and their email address, and then describe each of those columns to the rest of the system

The source plugin used is determined by the migration definition; each migration has a single source plugin.

Example from a migration plugin YAML file:

```
source:
  plugin: baseball_player
```

## Tracking changes with the `track_changes` option

Source plugins can be configured to track changes and re-import a record updating the previously-created entry in Drupal with new values if the source row changes.

Example:

```
source:
  plugin: baseball_player
  track_changes: true
```

This works because Drupal creates a map table when running a migration. This table contains one record for every row imported, maps the source ID to the destination ID, and saves a hash for the source row. When running a migration, if `track_changes` is `true` Drupal will hash the source row and compare it to the previously-saved value. If they do not match the row will be re-imported and the corresponding destination record will be updated.

Learn more in [Track Changes to Source Data During a Migration](https://drupalize.me/tutorial/track-changes-source-data-during-migration).

## Use highwater marks to control which records get imported

*Highwater marks* allow the Migrate API to track what has already been processed and only import content that has been created or updated since the migration was previously run.

When using a highwater mark each time the migration runs it will log the *highest* value migrated so far. The next time the migration runs it'll skip ahead to that point in the source data. This can be more efficient than using `track_changes` if your source data can accommodate it, since there's no need to hash every source record to determine if it's changed or not.

Example:

```
source:
  plugin: baseball_player
  highwater_mark:
    name: changed
    alias: bp
```

Learn more in [Use Highwater Marks to Limit What Gets Imported](https://drupalize.me/tutorial/use-highwater-marks-limit-what-gets-imported).

**Note:** When using highwater marks make sure the source data is sorted by the highwater field.

## Should this row be imported?

This is the process that the Migrate API will go through when determining whether or not it should process a row provided by the source plugin, it'll start processing as soon as it finds a true statement:

1. Has this row been imported yet?
2. Is this row explicitly set to update via the map table?
3. Is there a highwater mark, and if so is this row newer than the currently-logged value?
4. If there isn't a highwater mark, and track changes is enabled, does the hash of the row match the previous value for this row?

## Do I need to write a source plugin?

When migrating from a non-Drupal data store you'll need to write a source plugin, or customize an existing one, in order to define your data so that the Drupal migration system can access it.

In some cases one of the generic source plugins might work for you. These are fairly generic plugins that can be configured to extract and describe data without having to write extra code. The most interesting ones right now are:

- [Migrate Source CSV](https://drupal.org/project/migrate_source_csv) - use this if you're importing CSV data
- The URL Source contained in the [Migrate Plus module](https://drupal.org/project/migrate_plus) - use this to import JSON, XML, or SOAP data from a URL or file. [Learn more](http://virtuoso-performance.com/blog/mikeryan/drupal-8-plugins-xml-and-json-migrations).

These source plugins can call be configured via settings in your migration plugin and can likely be used simply by altering the configuration for your needs. [This migration plugin](https://github.com/heddn/d8_custom_migrate/blob/master/web/modules/custom/custom_migrate/config/install/migrate_plus.migration.migrate_csv.yml) contains a good example of the CSV source plugin being configured via the migration instead of writing a custom source plugin.

If you're migrating from a custom MySQL database you'll need to [write a source plugin](https://drupalize.me/tutorial/write-custom-source-plugin) that performs a query against your existing tables and describes the columns returned. In most cases where you're extracting data from an existing database you'll likely end up writing multiple source plugins, one for each set of things you want to import. For example: users, blog posts, and comments are all likely to have their own unique migration path. One way to think about this is by knowing what type of record you're creating in Drupal. If you're going to create comments, and user accounts, you'll likely have a migration path, and thus source plugin, for both.

If you're a module maintainer, and you're trying to provide a migration path for the data that your module is responsible for you'll likely need to write a source plugin to describe that data.

## The details

Source plugins are managed by the [MigratePluginManager](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21MigratePluginManager.php/class/MigratePluginManager/).

Migrate source plugins implement `\Drupal\migrate\Plugin\MigrateSourceInterface` and often extend `\Drupal\migrate\Plugin\migrate\source\SourcePluginBase`. They are annotated with the `\Drupal\migrate\Annotation\MigrateSource` annotation and must be at `src/Plugin/migrate/source` of the module that defines them.

[View a full list of source plugins provided by Drupal core](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Annotation%21MigrateSource.php/class/annotations/MigrateSource/). These are mostly related to extracting data from previous versions of Drupal. These provide great examples of how a source plugin works.

The best examples available for learning how to write a source plugin are in the *migrate\_example*, and *migrate\_example\_advanced* modules that are part of the Migrate Plus project. The code there is very well documented and is intended to illustrate how the system works. You can learn more about these examples in the Documentation and Examples tutorial.

The source code form Migrate Source CSV is a great example of how to write a plugin that reads from something other than an SQL database.

Some good examples from core include the source plugins for extracting information about user-uploaded files from a Drupal 6 site, available at `Drupal/core/modules/file/src/Plugin/migrate/source/d6/`.

- The File(.php) plugin handles fetching file information
- The Upload(.php) plugin handles fetching upload information
- The UploadInstance(.php) plugin handles fetching upload instance information

## Recap

Source plugins perform the extract phase of the ETL process. They are responsible for reading data from an external source and chunking it up into individual records that can imported into Drupal. There are a few source plugins already present in Drupal core that can be extended and customized, as well as many contributed modules with source plugins for non-SQL data like CSV, or XML files. Module developers can write custom source plugins when they need more control over what data is provided to be considered for migration.

## Further your understanding

- What role do source plugins play in the migration process?
- What format is the data that you're migrating currently in? Can you use one of the generic source plugins or are you going to need to write one yourself?

## Additional resources

- [Write a Custom Source Plugin](https://drupalize.me/tutorial/write-custom-source-plugin) (Drupalize.Me)
- [Migrate source](https://www.drupal.org/node/2129649) (Drupal.org)
- [Migrating from a JSON source using the URL source plugin from Migrate Plus](https://github.com/karens/import_drupal) (github.com)
- [Use Highwater Marks to Limit What Gets Imported](https://drupalize.me/tutorial/use-highwater-marks-limit-what-gets-imported) (Drupalize.Me)
- [Track Changes to Source Data During a Migration](https://drupalize.me/tutorial/track-changes-source-data-during-migration) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Clear History

Ask Drupalize.Me AI

close