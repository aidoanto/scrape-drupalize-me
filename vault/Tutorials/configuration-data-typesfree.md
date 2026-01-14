---
title: "Configuration Data Typesfree"
url: "https://drupalize.me/tutorial/configuration-data-types?p=2476"
guide: "[[work-data-modules]]"
order: 21
---

# Configuration Data Typesfree

## Content

In this tutorial, you'll learn about the two types of configuration data: simple configuration and configuration entities. By the end of this tutorial, you should have a better understanding of which type of configuration to use in your module.

## Goal

Understand the difference between the two types of configuration data in Drupal.

## Prerequisites

- [Overview: Configuration Management in Drupal](https://drupalize.me/tutorial/overview-configuration-management-drupal)

## Watch: Configuration Data Storage

Sprout Video

## Overview of Drupal's data types

In Drupal, there are four data types used for canonical data storage:

- **Content**: Information that's meant to be displayed on your site: articles, images, files, etc. (Learn more about content entities in this [Entity API Overview](https://drupalize.me/tutorial/entity-api-overview).)
- **Session**: Information about individual users' interactions with the site, like whether they're logged in.
- **State**: Information of a temporary nature about the state of your site: for example, the last time cron was run.
- **Configuration**: Information about your site that's not content, and is meant to be more permanent: the name of your site, content types, and views, for example.

We'll focus on **configuration** data in this tutorial.

## Types of configuration data

In Drupal, there are two types of configuration data: **simple configuration** and **configuration entities**.

## Simple configuration

It might be helpful to think of simple configuration as module configuration settings. Each setting must contain a value in order for the module (and by extension, the site) to function properly. Simple configuration is suitable for storing settings as boolean values, integers, or text strings in one or more key/value pairs. Simple configuration can only be dependent on the module providing them.

Default configuration, especially when it contains necessary initial values for a module's settings, can be stored in *config/install/MODULENAME.settings.yml* file. Each module can have as many configuration objects as needed which can be organized into files as *MODULENAME.CONFIG.PREFIX.yml*.

Image

![System module provides many configuration files that store default values.](../assets/images/many-config-files.png)

*System module provides many configuration files that store default values.*

Simple configuration can be very simple indeed, as in this example of default configuration from the Action module (*core/modules/action/config/install/action.settings.yml*):

```
recursion_limit: 35
```

Or, it can be a bit more complex, containing key/value pairs organized into a multidimensional array, like in this *system.site* example, [retrieved from an example site with](https://drupalize.me/tutorial/inspect-configuration-drush) `drush cget system.site`:

```
uuid: ea163347-3e7e-4eba-876d-a52ce7600e90
name: 'My Drupal Site'
mail: [email protected]
slogan: ''
page:
  403: ''
  404: ''
  front: /node
admin_compact_mode: false
weight_select_max: 100
langcode: en
default_langcode: en
_core:
  default_config_hash: AyT9s8OUcclfALRE_imByOMgtZ19eOlqdF6zI3p7yqo
```

## Configuration entities

Configuration entities are suitable for creating user-defined configuration, such as image styles, views, content types, etc. A configuration entity type is defined by a module, default configuration is provided by that module as well as any other module, and then users can create zero or more configuration entities through Drupal's administrative UI.

To learn more about configuration entities and how a configuration entity type is defined in a module, see the tutorial: [Create a Configuration Entity Type](https://drupalize.me/tutorial/create-configuration-entity-type).

## Configuration schemas

Simple configuration, like in module settings, should provide a schema in order to identify translatable strings in your shipped configuration.

Schema files can contain structure descriptions for both settings (simple configuration) and configuration entities. (Schemas are required for configuration entities.) Define a schema in your module's *config/schema/MODULENAME.schema.yml*.

Here is the schema for the `action.settings` configuration object (*core/modules/action/config/schema/action.schema.yml*). It describes the schema for *core/modules/action/config/install/action.settings.yml* (see section "Simple Configuration" above).

```
action.settings:
  type: config_object
  label: 'Action settings'
  mapping:
    recursion_limit:
      type: integer
      label: 'Recursion limit for actions'
```

The top-level key, `action.settings` refers to both the basename of the associated file, *action.settings.yml* as well as the name of the configuration object, i.e. `$this->config('action.settings')` or `drush config-get action.settings` (when Action module is enabled).

Under `action.settings`, an array with the keys: `type`, `label`, and `mapping`.

- `type`: (required) commonly `config_object` for simple configuration or `config_entity` for configuration entities or any other valid schema type
- `label`: (optional) A translatable string describing the configuration object or entity as a whole
- `mapping`: `mapping` corresponds to the schema type `mapping` which should contain an array of known keys. Could alternatively be `sequence` if configuration object is `type: sequence`
  - `property-name`: the name of the configuration property
    - `type`: the data type of the property (can be one of any valid schema type)
    - `label`: a translatable label for this property

This schema example essentially says, "We have a configuration object named `action.settings` with a translatable label, 'Action settings', with the following known key (aka 'mapping'): `recursion_limit`. A `recursion_limit` is an integer with the translatable label, 'Recursion limit for actions'."

### Valid schema types

- **Scalar types**: boolean, integer, float, string, uri, email
- **List types**: mapping (known keys), sequence (unknown keys)
- **Common subtypes**: label (short and translatable), text (long and translatable), config\_object (object root), config\_entity (entity root)

To learn more about schemas and how to implement them, see [Configuration schema/metadata](https://www.drupal.org/docs/drupal-apis/configuration-api/configuration-schemametadata) (Drupal.org) and [Create a Configuration Entity Type](https://drupalize.me/tutorial/create-configuration-entity-type) (section: "Configuration schema").

## Configuration data storage

All active configuration data, regardless of type, are stored in the database by default. The configuration system allows us to [export our configuration to YAML files using Drupal's administrative UI](https://drupalize.me/tutorial/synchronize-configuration-ui) or [Drush](https://drupalize.me/tutorial/inspect-configuration-drush). These configuration files can then be moved and imported into another instance of the site's active configuration, i.e. from local development to staging and then to the live production site.

## Recap

There are five data storage types in Drupal: content, session, state, configuration, and cache. There are two configuration data storage types: simple configuration and configuration entities. All of your active configuration data, regardless of type, is stored in the database by default and the configuration system allows you to export your configuration to YAML files.

## Further your understanding

- Explore the Configuration and Structure administrative pages. Which configuration do you think is simple configuration (configured in one place and only one instance of it) and which do you think are configuration entities (where a type is defined and multiple entities using that type are created)? For example, compare Basic site settings (*/admin/config/system/site-information*) with Image styles (*/admin/config/media/image-styles*).
- How do you see "Basic site settings" displayed and used throughout the site?
- Where do you see image styles used throughout the site in configuration forms? (Hint: configure the field formatter of an image field and select a new image style.)

## Additional resources

- [Overview of Configuration (vs. other types of information)](https://www.drupal.org/docs/drupal-apis/configuration-api/overview-of-configuration-vs-other-types-of-information) (Drupal.org)
- [Configuration schema/metadata](https://www.drupal.org/docs/drupal-apis/configuration-api/configuration-schemametadata) (Drupal.org)
- [Inspect Configuration with Drush](https://drupalize.me/tutorial/inspect-configuration-drush) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview: Configuration API in Drupal](/tutorial/overview-configuration-api-drupal?p=2476)

Next
[Default Configuration in a Module](/tutorial/default-configuration-module?p=2476)

Clear History

Ask Drupalize.Me AI

close