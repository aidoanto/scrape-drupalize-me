---
title: "Write a Custom Source Plugin"
url: "https://drupalize.me/tutorial/write-custom-source-plugin?p=3115"
guide: "[[learn-migrate-drupal]]"
---

# Write a Custom Source Plugin

## Content

This tutorial covers writing a custom source plugin that imports data from a MySQL database into Drupal nodes. After completing this tutorial you should understand how to write your own custom source plugin that can:

- Extract data from an SQL source
- Describe the various fields in the source data to the Migrate API for mapping
- Provide unique IDs for each row of imported data

By the end of this tutorial you should be able write a custom source plugin that uses an SQL data store as well as have a foundation for writing source plugins that extract data from any source that PHP can read.

## Goal

Write a migration source plugin that can extract player data from a MySQL database and prepare it for import into Drupal.

## Prerequisites

- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins)
- [Source Plugins](https://drupalize.me/tutorial/source-plugins)
- Example code for this tutorial can be found at <https://github.com/DrupalizeMe/migrate-10x>
- [Set up Migrate Demo Site and Source Data](https://drupalize.me/tutorial/set-migrate-demo-site-and-source-data) will walk you through getting the example data we use in this tutorial.

## The basics

Source plugins are managed by the [MigratePluginManager](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21MigratePluginManager.php/class/MigratePluginManager/).

Before you write your own custom source plugin first make sure there isn't already one that you can use. See [Do I need to write a source plugin?](https://drupalize.me/tutorial/source-plugins)

## Connecting to a database

Make sure that you create a database entry in *settings.php* for use with `SqlBase`. This tells the Migrate API how to connect to the MySQL database that contains your source data. These are defined just like standard database connection in your *settings.php* file. The key to making this work is naming your connection correctly. These should always use the name 'migrate', `$databases['migrate']['default'] = array()`, so that `SqlBase` can find it. See the [documentation for `SqlBase::setUpDatabase()`](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21migrate%21source%21SqlBase.php/function/SqlBase%3A%3AsetUpDatabase) for more information.

Example: *sites/default/settings.php*

```
$databases['migrate']['default'] = array (
  'database' => 'lahmansbaseballdb',
  'username' => 'root',
  'password' => 'root',
  'prefix' => '',
  'host' => 'localhost',
  'port' => '3306',
  'namespace' => 'Drupal\\Core\\Database\\Driver\\mysql',
  'driver' => 'mysql',
);
```

## Write a source plugin

Source plugins need to do the following:

- Use PHP to extract data from some data store and then divide it up into rows and fields that can be iterated over
- Provide a unique ID for each row of data for tracking purposes
- Tell the Migrate API about the fields of data so they can be processed during the next phase of the import

This source plugin will extract data from a MySQL database containing information about baseball players. [Read about our source data](https://drupalize.me/tutorial/set-migrate-demo-site-and-source-data) if you want to follow along.

Source plugins live in the `Drupal\{MY_MODULE}\Plugin\migrate\source` namespace. In our case this will be `Drupal\baseball_migration\Plugin\migrate\source`, with our code living in the file *baseball\_migration/src/Plugin/migrate/source/BaseballPlayer.php*.

Source plugins are annotated with the `\Drupal\migrate\Annotation\MigrateSource` annotation. Generally, all you'll need to specify is the `id`. However, in the case of a Drupal-to-Drupal migration, you'll also need to specify a `source_module`. (See [this change record](https://www.drupal.org/node/2831566).) View the annotation class' documentation for details about additional parameters. The `id` specified here is the name you will use to refer to your source plugin when writing a migration.

```
/**
 * Source plugin for baseball players.
 *
 * @MigrateSource(
 *   id = "baseball_player"
 * )
 */
```

Migrate source plugins implement `\Drupal\migrate\Plugin\MigrateSourceInterface` though in practice it's probably best to start from `\Drupal\migrate\Plugin\migrate\source\SourcePluginBase` at a minimum. It already implements most of the required iteration functionality.

Our `BaseballPlayer` class will extend the [`SqlBase`](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21migrate%21source%21SqlBase.php/class/SqlBase) class, which already extends `SourcePluginBase`, and simplifies working with an SQL source by reducing boilerplate code.

```
use Drupal\migrate\Plugin\migrate\source\SqlBase;

class BaseballPlayer extends SqlBase {

}
```

In our `BaseballPlayer` class we need to implement a `query()` method to tell the plugin what data to retrieve, a `fields()` method that will tell the Migrate API about the fields of data in each row, and a `getIds()` method to define a unique ID for each row of data. These are documented in depth in the example code below.

## Example source plugin

```
<?php

namespace Drupal\baseball_migration\Plugin\migrate\source;

use Drupal\migrate\Plugin\migrate\source\SqlBase;
use Drupal\migrate\Row;

/**
 * Source plugin for baseball players.
 *
 * @MigrateSource(
 *   id = "baseball_player"
 * )
 */
class BaseballPlayer extends SqlBase {

  /**
   * {@inheritdoc}
   */
  public function query() {
    // Write a query using the standard Drupal query builder that will be run
    // against the {source} database to retrieve information about players. Each
    // row returned from the query should represent one item that we would like
    // to import. So, basically, one row per player.
    //
    // In this case, we can just select all rows from the people table in the
    // {source} database, and limit to just the fields we plan to migrate.
    $query = $this->select('people', 'm')
      ->fields('m', array(
        'playerID',
        'birthYear',
        'birthMonth',
        'birthDay',
        'deathYear',
        'deathMonth',
        'deathDay',
        'nameFirst',
        'nameLast',
        'nameGiven',
        'weight',
        'height',
        'bats',
        'throws',
      ));
    return $query;
  }

  /**
   * {@inheritdoc}
   */
  public function fields() {
    // Provide documentation about source fields that are available for
    // mapping as key/value pairs. The key is the name of the field from the
    // database, and the value is the human readable description of the field.
    $fields = array(
      'playerID' => $this->t('Player ID'),
      'birthYear' => $this->t('Birth year'),
      'birthMonth' => $this->t('Birth month'),
      'birthDay' => $this->t('Birth day'),
      'deathYear' => $this->t('Death year'),
      'deathMonth' => $this->t('Death month'),
      'deathDay' => $this->t('Death day'),
      'nameFirst' => $this->t('First name'),
      'nameLast' => $this->t('Last name'),
      'nameGiven' => $this->t('Given name'),
      'weight' => $this->t('Weight'),
      'height' => $this->t('Height'),
      'bats' => $this->t('Bats'),
      'throws' => $this->t('Throws'),
    );

    // If using prepareRow() to create computed fields you can describe them
    // here as well.

    return $fields;
  }

  /**
   * {@inheritdoc}
   */
  public function getIds() {
    // Use a Schema Definition array to describe the field from the source row
    // that will be used as the unique ID for each row.
    //
    // @link https://www.drupal.org/node/146939 - Schema array docs.
    //
    // @see \Drupal\migrate\Plugin\migrate\source\SqlBase::initializeIterator
    // for more about the 'alias' key.
    return [
      // Key is the name of the field from the fields() method above that we
      // want to use as the unique ID for each row.
      'playerID' => [
        // Type is from the schema array definition.
        'type' => 'text',
        // This is an optional key currently only used by SqlBase.
        'alias' => 'm',
      ],
    ];
  }
}
```

A note about the **alias** parameter in the `getIds()` method: the key is part of the SqlBase implementation and is used to distinguish between ambiguous field names in some situations, such as when a SQL source query joins two tables with the same field. Providing an optional alias results in using {alias}.{field\_name} being used as the ID field.

Starting from `SourcePluginBase` instead of `SqlBase`? [This article](https://ohthehugemanatee.org/blog/2015/05/02/how-to-build-a-new-source-for-drupal-migrate-8/) discusses the important methods you'll need to implement. `SqlBase` is handling some of those methods for us in the above example.

## Use your custom source plugin

To use the BaseballPlayer source plugin we just created, refer to it by the ID from the annotation in your migration YAML file.

Example:

```
source:
  plugin: baseball_player
```

## Using services

In some cases you may want to use a service in your source plugin. For example, maybe you're consuming data from Twitter and want to use the `http_client` service. [This article](http://www.drupalwatchdog.net/blog/2015/6/write-migrate-process-plugin-learn-drupal-8) demonstrates how you can use dependency injection to inject any service into a process plugin, but the method is the same for source plugins as well.

## Recap

In this tutorial we walked through writing a custom source plugin, which is a PHP class that lives in the `Drupal\{module_name}\Plugin\migrate\source` namespace and extends `Drupal\migrate\Plugin\migrate\source\SqlBase`. We chose to extend this class because of the helpful features it contains for accessing data stored in SQL databases. Our source plugin queries the `people` table from our source database in order to extract records for eventual import into Drupal. It also provides some additional information about the fields and unique IDs in our source data that are helpful for the Migrate API.

## Further your understanding

- What are the 3 things that any migration source plugin is required to do?
- Where is the data you're going to migrate currently stored? Do you need a custom source plugin or is there an existing one you can try first?

## Additional resources

- The source plugins in the migrate\_example module (part of [Migrate Plus](https://www.drupal.org/project/migrate_plus)) are very well-documented
- [Drupal to Drupal 8 via Migrate API](https://www.chapterthree.com/blog/drupal-to-drupal-8-via-migrate-api) (chapterthree.com) - This article provides an example of creating source plugins to perform a Drupal to Drupal migration in which you only want to migrate a subset of the existing data. Good example of creating source plugins in general as well
- [How to Build a New Source for Drupal Migrate 8](https://ohthehugemanatee.org/blog/2015/05/02/how-to-build-a-new-source-for-drupal-migrate-8/) (ohthehugemanatee.org) - Our suggestion differs from this article in that we implement the plugin in a custom module instead of in the Migrate Plus module. Otherwise this article has some great sample code.

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Source Plugins](/tutorial/source-plugins?p=3115)

Next
[Process Plugins](/tutorial/process-plugins?p=3115)

Clear History

Ask Drupalize.Me AI

close