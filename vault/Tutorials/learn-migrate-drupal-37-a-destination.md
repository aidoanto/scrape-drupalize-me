---
title: "a destination"
url: "https://drupalize.me/tutorial/destination-plugins"
guide: "[[learn-migrate-drupal]]"
order: 37
---

# a destination

## Content

Destination plugins handle the *load* phase of the [ETL (Extract, Transform, Load) process](https://drupalize.me/tutorial/migrate-system-terms-and-concepts) and are responsible for saving new data as Drupal content or configuration.

In this tutorial, we'll:

- Examine the role that destination plugins fulfill
- Learn about existing destination plugins
- Better understand when you might need to write your own destination plugin

By the end of this tutorial, you should be able to explain what destination plugins does and understand how you'll make use of them in your own migration.

## Goal

Explain how destination plugins work and the role they play.

## Prerequisites

- [Migrate System: Terms and Concepts](https://drupalize.me/tutorial/migrate-system-terms-and-concepts)
- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins)

Sprout Video

## What is a destination plugin?

Destination plugins understand Drupal's content and configuration data storage APIs and are responsible for saving incoming data during a migration.

Destination plugins:

- Dictate the fields that data can be saved to
- Determine the unique ID of the record created during the migration for mapping purposes
- Create new records from imported data and persist them to Drupal's storage

As an example, if you want to import data as nodes you would use the `entity:node` destination plugin. This plugin is capable of using Drupal's Entity API to create new node objects. It can look up the list of fields for a given node type (bundle) to ensure proper mapping from source field to destination field, save new node objects to the database, and provide the Migrate API with the unique ID of the node that was just created.

As a migration author you can use this destination plugin to create nodes by configuring it in your migration plugin instead of having to write PHP code to process and save nodes.

The destination plugin used is determined by the migration definition; each migration has a single destination.

Example from a migration plugin YAML file using the `entity:node` destination plugin:

```
destination:
  plugin: entity:node
```

## Common destination plugins

Drupal core already provides destination plugins for common use cases. In fact, it's unlikely that you'll need to write your own destination plugins. Drupal has standardized data storage around either the Entity API (content) or the Configuration API (configuration) and provides generic destination plugins for both that will work in most cases.

Importing content is the most common use case, and the `entity:{entity type}` plugin works great for this. Replace `{entity type}` with the machine name of your entity type. Example: `entity:node` to create new nodes.

Importing configuration values is another common use case for destination plugins. Drupal core provides a generic `config` destination, and an `EntityConfigBase` class that can be extended to write custom destination plugins for configuration entities.

[View a full list of destination plugins provided by Drupal core](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Annotation%21MigrateDestination.php/class/annotations/MigrateDestination/).

## Destination plugin configuration

Some destination plugins accept additional configuration options which can be set in your migration plugin's YAML file. However, knowing what those options are, and what each one does, can be a bit tricky.

First of all, the documentation isn't great. So you're likely going to need to dive into the code a little bit to figure out both what options are available, and how to use them. But, the good thing is, once you know how to figure this out for one destination plugin you can apply the same logic to any of them.

Let's use the `config` plugin as an example.

Locate the class that implements the plugin in question, `\Drupal\migrate\Plugin\migrate\destination\Config`. The first thing to look for is any documentation about configuration options in the `@docblock` comment for the class. For example, the `@docblock` for the `Config` class contains:

```
 * Available configuration keys:
 * - store null: (optional) Boolean, if TRUE, when a property is NULL, NULL is
 *   stored, otherwise the default is used. Defaults to FALSE.
 * - translations: (optional) Boolean, if TRUE, the destination will be
 *   associated with the langcode provided by the source plugin. Defaults to
 *   FALSE.
 *
 * Destination properties expected in the imported row:
 * - config_name: The machine name of the config.
 * - langcode: (optional) The language code of the config.
```

This is followed by a couple of examples.

Additionally, you can read through the code looking for instances of `$this->configuration['some_configuration_key']`. The values of `$this->configuration` can be set by specifying them in the migration plugin when declaring which destination plugin to use. In the above examples, the `config_name` key would be accessible via `$this->configuration['config_name'];`. This can also be an informative way to figure out how the individual configuration options are actually used during processing of a migration.

Example:

```
destination:
  plugin: 'config'
  config_name: mymodule.settings
```

## Do I need to write a destination plugin?

Destination plugins are typically provided by the module that is responsible for the data in question. So unless you're the maintainer of the module you probably don't need to write a destination plugin.

Additionally, in Drupal, most modules store both their configuration and their content using the Entity API. Plus, the core Migrate module provides a set of generic destination plugins for both configuration and content entities. Generally these can be used as is. In some cases you may need to extend the core plugins customizations for an individual module's specific needs. You can take a look at the available destination plugins in the `src/Plugin/migrate/destination` directory of any module that provides them.

The entity destination plugin uses derivative plugins in most cases. Meaning that the same code is used for every entity type, but the way it works varies based on configuration. Specifically, the deriver uses the `{entity type}` bit to determine which type of entity you're talking about.

In some cases there are specific subclasses of the `entity` plugin that handle special cases. [`entity:user`](https://www.drupal.org/node/2183357) and [`entity:file`](https://www.drupal.org/node/2637890) are good examples of this. Both require the ability to provide additional configuration for the plugin beyond just entity type. So instead of using the generic `\Drupal\migrate\Plugin\migrate\destination\EntityContentBase`, specific classes are defined for each that expose and use additional configuration.

If your module maintains data in its own table(s), or needs to provide some advanced configuration options like the `entity:file` plugin, you may need to write your own destination plugin.

## The details

Migration destination plugins implement `\Drupal\migrate\Plugin\MigrateDestinationInterface` and often extend `\Drupal\migrate\Plugin\migrate\destination\DestinationBase`. They use a `\Drupal\migrate\Attribute\MigrateDestination` attribute, and must be in the *src/Plugin/migrate/destination* directory of the module that defines them.

The `\Drupal\migrate\Plugin\migrate\destination\EntityContentBase` and `\Drupal\migrate\Plugin\migrate\destination\EntityConfigBase` base classes are great starting points for destination plugins that save content or configuration entities.

Migration destination plugins are managed by the `\Drupal\migrate\Plugin\MigrateDestinationPluginManager` class.

## Recap

Destination plugins perform the load phase of the ETL process. They understand how Drupal's internal systems like Entities work, and provide a mechanism for saving data into Drupal. Module developers can write custom destination plugins as needed, and can often do so more efficiently by extending existing destination plugins.

## Further your understanding

- What are destination plugins used for?
- What destination plugin would I use if I wanted to save a taxonomy term?
- Can you come up with an example of a custom destination plugin that you might write for your own migration purposes?

## Additional resources

- [Migrate destination](https://www.drupal.org/node/2174881) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Clear History

Ask Drupalize.Me AI

close