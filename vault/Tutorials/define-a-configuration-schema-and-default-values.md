---
title: "Define a Configuration Schema and Default Values"
url: "https://drupalize.me/tutorial/define-configuration-schema-and-default-values?p=3243"
guide: "[[drupal-module-developer-guide]]"
---

# Define a Configuration Schema and Default Values

## Content

Modules must provide metadata about their configuration data via a schema definition, which serves localization and validation purposes. Modules can optionally specify default configuration values to ensure that the module functions when installed.

In this tutorial, we'll:

- Define schema for the Anytown module's configuration.
- Set default module settings.

By the end of this tutorial you should be able to define a configuration object's schema and default values.

## Goal

Add a schema and default settings for the Anytown module's configuration.

## Prerequisites

- [Concept: Configuration API](https://drupalize.me/tutorial/concept-configuration-api)
- [Retrieve and Update Weather Forecast Settings](https://drupalize.me/tutorial/retrieve-and-update-weather-forecast-settings)

## Video tutorial

Sprout Video

## Configuration schemas

Modules that introduce configuration need a *configuration schema* to inform Drupal about the data types of configuration values. This schema supports multilingual functionality and ensures accurate data type usage across operations. This tutorial will guide you through setting up a schema for weather forecast settings in the Anytown module.

## Default configuration

Modules can supply default configuration values, which are applied upon installation and can be overridden by site administrators.

Let's examine the `anytown.settings` configuration object and create a schema and default configuration based on it:

- `display_forecast`: Boolean to control weather forecast display.
- `location`: A 5-digit U.S. ZIP code for weather forecast retrieval.
- `weather_closures`: Multi-line string listing weather-related closures.

## Add a configuration schema definition

Configuration schemas are defined in *config/schema/MODULE\_NAME.schema.yml*.

Create *config/schema/anytown.schema.yml* with the following content:

```
# Schema for the configuration files of the Anytown module.
# https://www.drupal.org/docs/drupal-apis/configuration-api/configuration-schemametadata
anytown.settings:
  type: config_object
  label: 'Anytown settings'
  mapping:
    display_forecast:
      type: boolean
      label: 'Toggle forecast display on/off'
    location:
      type: string
      label: 'ZIP code where the market takes place'
    weather_closures:
      type: string
      label: 'Weather related closures'
```

This defines a configuration schema for the Anytown Drupal module. The top-level key, `anytown.settings` refers to both the basename of the associated file, *anytown.settings.yml* as well as the name of the configuration object, i.e. `$this->config('anytown.settings')` or `drush config-get anytown.settings`.

Under `anytown.settings`, is an array with the keys: `type`, `label`, and `mapping`.

- `type`: (required) commonly `config_object` for simple configuration or `config_entity` for configuration entities (or any other valid schema type)
- `label`: (optional) A translatable string describing the configuration object or entity as a whole
- `mapping`: `mapping` corresponds to the schema type `mapping` which should contain an array of known keys. Could alternatively be `sequence` if configuration object is `type: sequence`
  - `{property-name}`: the name of the configuration property
    - `type`: the data type of the property (can be one of any valid schema type)
    - `label`: a translatable label for this property

Possible `type` values include base types:

- boolean
- email
- integer
- float
- string
- uri

Subtypes of the base `string` can be used for specific use cases:

- **label**: Short and translatable string
- **plural\_label**: Label that contains plural variants
- **text**: Long and translatable string
- **uuid**: String that is a UUID
- **path**: String that is a Drupal path
- **date\_format**: String that is a PHP date format
- **color\_hex**: String that is a hex color value

For complex data types like **arrays**, use either:

- **mapping**: A key-value pair list type ("associative array" or "hash") where each element may have a different type.
- **sequence**: A simple indexed list ("indexed array") where elements are either of the same type and the keys are irrelevant. The keys may be strings, or the array may be defined as numeric.

The [Configuration Inspector module](https://www.drupal.org/project/config_inspector) provides useful utilities for developers to inspect, define, and debug, configuration schemas. And [this cheat sheet](https://www.drupal.org/docs/drupal-apis/configuration-api/configuration-schemametadata#cheatsheet) is a detailed resource.

## Add default configuration values

Default settings are outlined in YAML under *config/install/CONFIG\_OBJECT\_NAME.yml*, where `CONFIG_OBJECT_NAME` is the module's configuration object name.

Create *config/install/anytown.settings.yml*:

```
# Default configuration for the Anytown module.
display_forecast: true
location: '00000'
weather_closures: 'None'
```

These defaults are applied when the module is installed. It provides initial module settings that administrators can then modify.

**Tip:** Use `drush config-get anytown.settings` to review current configuration if the module is already in use. Adjust the default configuration in *config/install/* as needed based on this output.

## Recap

This tutorial detailed adding a schema definition for module configuration and establishing default settings. These steps ensure your module operates correctly upon installation and supports Drupal's configuration management system.

## Further your understanding

- Why might default values be necessary for a module to function?

## Additional resources

- [Configuration Data Types](https://drupalize.me/tutorial/configuration-data-types) (Drupalize.Me)
- [Configuration Schema](https://www.drupal.org/docs/drupal-apis/configuration-api/configuration-schemametadata) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Retrieve and Update Weather Forecast Settings](/tutorial/retrieve-and-update-weather-forecast-settings?p=3243)

Next
[Concept: Entity API and Data Storage](/tutorial/concept-entity-api-and-data-storage?p=3243)

Clear History

Ask Drupalize.Me AI

close