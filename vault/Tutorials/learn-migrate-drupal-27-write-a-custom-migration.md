---
title: "Write a Custom Migration"
url: "https://drupalize.me/tutorial/write-custom-migration?p=3115"
guide: "[[learn-migrate-drupal]]"
order: 27
---

# Write a Custom Migration

## Content

Migration plugins are the glue that binds [a source](https://drupalize.me/tutorial/source-plugins), [a destination](https://drupalize.me/tutorial/destination-plugins), and multiple [process plugins](https://drupalize.me/tutorial/process-plugins) together to move data from one place to another. Often referred to as migration templates, or simply migrations, migration plugins are YAML files that explain to Drupal where to get the data, how to process it, and where to save the resulting object.

Source, process, and destination plugins do the heavy lifting in each phase of the ETL process in a custom migration. We need to choose which plugins we want to use for each phase, as well as map fields from our source data to fields at our destination. A migration YAML file glues it all together and gives it a unique name that we can use to run it.

In this tutorial we'll:

- Determine what information we're going to move, and where we're going to move it to
- Install Migrate Plus and Migrate Tools which we'll use to run our custom migration
- Write a custom migration plugin (configuration) YAML file that will work with Migrate Tools

By the end of this tutorial you should be able to write a custom migration YAML file and understand how to choose the source, destination, and process plugins that will do the work.

## Goal

Write a migration that imports baseball players from a custom MySQL database into Drupal.

## Prerequisites

- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins)
- [Source Plugins](https://drupalize.me/tutorial/source-plugins)
- [Process Plugins](https://drupalize.me/tutorial/process-plugins)
- [Destination Plugins](https://drupalize.me/tutorial/destination-plugins)
- Example code for this tutorial can be found at <https://github.com/DrupalizeMe/migrate-10x>
- [Set up Migrate Demo Site and Source Data](https://drupalize.me/tutorial/set-migrate-demo-site-and-source-data) will walk you through getting the example data we use in this tutorial.

## Make a plan

This tutorial assumes that you're already familiar with the basics of writing a custom module for the latest version of Drupal and understand the concepts of [source](https://drupalize.me/tutorial/source-plugins), [process](https://drupalize.me/tutorial/process-plugins), and [destination plugins](https://drupalize.me/tutorial/destination-plugins) with regard to their use in the Migrate API.

Start by answering these questions:

- What [source plugin](https://drupalize.me/tutorial/source-plugins) are you going to use to retrieve data during the extract phase?
- What [destination plugin](https://drupalize.me/tutorial/destination-plugins) are you going to use to save the new records in Drupal during the load phase?
- Create a list of all the source fields and indicate the destination fields they are going to be mapped to, as well as what [process plugin(s)](https://drupalize.me/tutorial/process-plugins) you'll use during the transform phase

## Use Migrate Plus and Migrate Tools to make things easier

When writing, and running, custom migrations we’ve found that the easiest way to do so is by using a combination of the Migrate Plus contributed module and the commands built into Drush version 10.4+. The two of them work together to allow us to define custom migrations in a way that they can also be individually executed.

Normally, migrations are defined as a template in a module's */migrations* directory. However, there is not currently a way to individually execute those migrations. Instead, we recommend following the technique used by the Migrate Plus module. Which, involves writing your migration as a configuration entity. In practice, the YAML files used to define the configuration entity are nearly identical to a standard migration plugin. The biggest difference is where they are located, and the way that the rest of the system can interact with them.

Download and install the >= 8.x.2.x versions of:

- [Migrate Plus](https://www.drupal.org/project/migrate_plus)

## Migrations live in modules

If you don't have a module to house your custom migrations now would be a good time to start one. Migrations can live within any module, and a module can contain any number of custom migrations. When writing a custom migration we recommend creating a module specifically for holding code related to the migration and nothing else.

Get started by using the `drush generate module` command to start a new module:

```
drush generate module
```

At a minimum you'll need an info file like the following:

*modules/custom/baseball\_migration/baseball\_migration.info.yml*:

```
name: Baseball Migration
type: module
description: Example custom migration imports from MySQL database of baseball stats.
core_version_requirement: ^8 || ^9 || ^10
package: Custom
dependencies:
  - drupal:migrate
  - migrate_plus:migrate_plus
```

## Where should I put my migration .yml files?

There are two common places where you'll find migration related *.yml* files. We'll look at both. The quick version is put them in *{MODULE\_NAME}/migrations/*, but in some cases *{MODULE\_NAME}/config/install* is used, too.

If you want to know more, read on, or skip to the example migration YAML file below.

Drupal will look for migration *.yml* files in the *migrations/* subdirectory of the module. If you're using the contributed Migrate Plus module, migrations are also found in the *config/install/* subdirectory. The migration *.yml* files are handled differently depending on where they are discovered.

**Note:** You'll see both of these used in different examples and documentation. Both are valid.

### *{MODULE\_NAME}/**migrations/**\*.yml* (preferred)

Example module layout:

```
custom_module/
├── migrations
│   ├── migrate_plus.migration_group.tcdrupal.yml
│   ├── tcdrupal_d7_node_complete_sponsor.yml
│   ├── tcdrupal_d7_node_complete_timeslot.yml
│   └── tcdrupal_d7_user.yml
├── src
│   └── Plugin
│       └── migrate
│           └── source
│               └── TcdrupalUsers.php
├── tcdrupalmigration.info.yml
└── tcdrupalmigration.module
```

Migrations stored here are treated as [YAML plugins](https://drupalize.me/tutorial/plugin-discovery). The content of the YAML file is treated as arguments used to instantiate instances of `\Drupal\migrate\Plugin\Migration`, which are then executed.

This is where you'll find all the migrations for core and contrib modules.

### *{MODULE\_NAME}/\*\*config/install/\*\*migrate\_plus.migration.\*.yml*

Example module layout:

```
tcdrupalmigration/
├── config
│   └── install
│       ├── migrate_plus.migration_group.tcdrupal.yml
│       ├── migrate_plus.migration.tcdrupal_d7_node_complete_sponsor.yml
│       ├── migrate_plus.migration.tcdrupal_d7_node_complete_timeslot.yml
│       └── migrate_plus.migration.tcdrupal_d7_user.yml
├── src
│   └── Plugin
│       └── migrate
│           └── source
│               └── TcdrupalUsers.php
├── tcdrupalmigration.info.yml
└── tcdrupalmigration.module
```

Note the required *migrate\_plus.migration.* filename prefix.

The *config/install/* location as an option works if you're using the Migrate Plus module. Migrations stored here are [configuration entities](https://drupalize.me/tutorial/configuration-data-types) which the Migrate Plus module uses to [dynamically generate plugins](https://drupalize.me/tutorial/plugin-derivatives) and add them to the run-time.

The key difference, and **the reason you would want to use this approach** when writing custom migrations, is that because these are configuration entities you can use [configuration overrides](https://drupalize.me/tutorial/how-override-configuration) to change a migration's settings per-environment. For example, maybe you've got a migration that is sourcing images from a directory and creating Drupal Media entities out of them. The location of the directory is in the migration *.yml* file's `source:` settings.

Example *migrate\_plus.migration.dme\_images.yml*:

```
source:
  plugin: dme_import_images
  directory: "/var/www/html/images_to_import"
```

But the location on disk can vary depending on the environment where the migrations are executed. If the migration is a configuration entity, then in a *settings.php* file you could override it with something like the following.

Example *settings.php*:

```
$config['migrate_plus.migration.dme_images']['source']['directory'] = '/Users/joe/Sites/dme/images_to_import';
```

When the migration is executed, the configuration from the *settings.php* file would take precedent over that, in the file, *migrate\_plus.migration.dme\_images.yml*.

There's a downside to this approach though, and it's kind of a big one, since configuration is only imported when a module is first installed any changes you make to the *.yml* files in the *config/install/* directory are not reflected in the run-time environment until you've forced them to be re-imported. From a developer experience perspective, this can be frustrating. It requires either uninstalling/reinstalling the module. Or using something like:

```
drush config:import --partial --source=modules/custom/my_migration/config/install/
```

Learn more about how to do this in [Reimport Configuration During Development](https://drupalize.me/tutorial/reimport-default-configuration-during-development).

### Migration YAML files in core and contributed modules

Most core modules, and many contributed modules, have migrations defined in a *migrations/* directory. But those aren't always used. Why?

Migrations are only visible to the system if the source plugin that they are configured to use is available. For example when asked for a list of migrations the system discovers the *core/modules/user/migrations/d7\_user\_role.yml* migration which uses the `d7_user_role` source plugin. It then checks to see if the `d7_user_role` source plugin is available using the [standard plugin discovery system](https://drupalize.me/tutorial/discover-existing-plugin-types), and if it can't find that plugin it removes the migration from the list.

All the Drupal-to-Drupal migrations use source plugins that are either in, or depend on, the Migrate Drupal module. And that's why none of the *.yml* files in the *migrations/* subdirectories of all the core modules show up in the list when you run `drush migrate:status` if Migrate Drupal isn't enabled.

## An example migration YAML file

Put your YAML migration definitions into *{MY\_MODULE\_DIRECTORY}/migrations/{MIGRATION\_ID}.yml*. *{MIGRATION\_ID}* is the unique name you want to use for your migration and will also be used in the YAML definition of the migration.

This example migration uses the source data we set up in the [Prepare Your Source Data and Destination Site](https://drupalize.me/tutorial/set-migrate-demo-site-and-source-data) tutorial and demonstrates how to import player data from the custom [player source plugin](https://drupalize.me/tutorial/write-custom-source-plugin) as player nodes.

Example *baseball\_migration/migrations/baseball\_player.yml*:

```
# The machine name for a migration. Also used by various CLI tools when
# referencing the migration as an argument for a command.
id: baseball_player

# A human-friendly description of the migration. This is used by various UI and
# CLI tools when showing a list of available migrations.
label: Migrate list of players

# Optional group for the migration. This is a feature provided by the
# migrate_plus module and allows for running an entire group of migrations
# together.
migration_group: baseball

# Every migration must have a source plugin. Set this to the ID of the plugin to
# use.
#
# This is the extract phase of your migration.
#
# For our custom migration this should be the source plugin we wrote.
# \Drupal\baseball_migration\Plugin\migrate\source\BaseballPlayer The value here is
# the ID value from the source plugin's metadata.
source:
  plugin: baseball_player

# Every migration must also have a destination plugin, which handles writing
# the migrated data in the appropriate form for that particular kind of data.
# This value should be the ID of the destination plugin to use.
#
# This is the load phase of your migration.
destination:
  plugin: entity:node

# Here's the meat of the migration - the processing pipeline. This describes how
# each destination field is to be populated based on the source data. For each
# destination field, one or more process plugins may be invoked.
#
# This is the transform phase of your migration.
process:
  # Hardcode the destination node type (bundle) as 'player' using the
  # 'default_value' process plugin.
  type:
    plugin: default_value
    default_value: player

  # Simple field mappings that require no extra processing can use the default
  # 'get' process plugin. This just copies the value from the source to the
  # destination. 'get' is the default when no plugin is defined, so you can just
  # do destination_field: source_field.
  #
  # Our player content type in Drupal has a field named, 'field_player_weight'
  # and our Source plugin defines a 'weight' field in its ::getFields() method.
  # The destination field (or property) name goes on the left and the source
  # field goes on the right.
  field_player_weight: weight
  field_player_height: height
  field_player_bats: bats
  field_player_throws: throws
  field_player_given_name: nameGiven

  # We generate the node.title (which we treat as the name) by concatenating
  # two source fields together and putting a space between them using the
  # 'concat' process plugin.
  title:
    plugin: concat
    source:
      - nameFirst
      - nameLast
    delimiter: " "

  # Same thing with field_player_birth, concat these fields together using the
  # 'concat' process plugin.
  field_player_birth:
    plugin: concat
    source:
      - birthMonth
      - birthDay
      - birthYear
    delimiter: /

  # For death day we need to provide a default value in the case where the
  # player hasn't died yet. Also provides an example of using multiple process
  # plugins together. In this case we first use the 'concat' plugin to combine
  # three fields from the source data, and then use the 'default_value' plugin
  # to provide a default value for the field in the case that the previous step
  # resulted in an empty value.
  field_player_death:
    -
      plugin: concat
      source:
        - deathMonth
        - deathDay
        - deathYear
      delimiter: /
    -
      plugin: default_value
      default_value: ""

# Declare optional dependencies on another migration for this migration.
# This one has none.
migration_dependencies: {}
```

## Run your migration

At this time the most reliable way to run custom migrations is using the Drush commands provided by the Migrate Tools module.

```
drush migrate-import {MIGRATION_ID}
```

Example:

```
drush migrate:import baseball_player
Processed 17725 items (17725 created, 0 updated, 0 failed, 0 ignored) - done with 'baseball_player'
```

**Pro-tip:** When testing, add a `->range(0, 10)` call to your [source plugin's](https://drupalize.me/tutorial/source-plugins) query builder. This will allow your migrations to execute superfast since you’re only importing 10 rows. It helps when you’re debugging or just testing, and you don’t want to wait for all 17k rows to import.

The `migrate-import` Drush command also has a `--limit` flag that you can use to accomplish roughly the same thing.

[Learn more about running custom migrations](https://drupalize.me/tutorial/run-custom-migrations).

## Non-MySQL migrations

The example above demonstrates migrating from an SQL source using the custom source plugin. But that is just the tip of the iceberg. The Migrate API is capable of pulling in data from a variety of different sources. [Read more about source plugins](https://drupalize.me/tutorial/source-plugins) to understand how.

Here are some good examples we've found demonstrating non-SQL migrations:

- [Migrating from a JSON source using the URL source plugin from Migrate Plus](https://github.com/karens/import_drupal)
- [From XML using Migrate Plus URL source plugin](https://www.palantir.net/blog/migrating-xml-drupal-8)

## Recap

Migration plugins are YAML files that combine a source with a destination, and declare which process plugins to use when mapping values from one to the other. They need to located in the right place so Drupal can find them. In most cases this is a *migrations/* subdirectory of a custom module. Migration YAML files provide the required information that the Migrate API needs in order to allow a migration to be discovered and executed. Module developers can write custom migration plugins in order to migrate data from non-Drupal sources into Drupal.

## Further your understanding

- Can you write a custom migration that would import the teams from our sample data set?

## Additional resources

- [Drupal migrations reference: List of configuration options in YAML definition files](https://agaric.coop/blog/drupal-migrations-reference-list-configuration-options-yaml-definition-files) (agaric.coop)
- The [Migrate Plus module](https://www.drupal.org/project/migrate_plus) contains some excellent examples of custom migrations in the migrate\_example and migrate\_example\_advanced submodules. Worth checking out especially if you learn from example code.
- [This blog post](https://www.chapterthree.com/blog/drupal-to-drupal-8-via-migrate-api) shows an example of writing a custom migration in order to move some, but not all, of the content of a Drupal 7 site to Drupal 8. It also serves as another example of a custom migration YAML file.

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Destination Plugins](/tutorial/destination-plugins?p=3115)

Next
[Run Custom Migrations](/tutorial/run-custom-migrations?p=3115)

Clear History

Ask Drupalize.Me AI

close