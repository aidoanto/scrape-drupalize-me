---
title: "Concept: Configuration APIfree"
url: "https://drupalize.me/tutorial/concept-configuration-api?p=3243"
guide: "[[drupal-module-developer-guide]]"
---

# Concept: Configuration APIfree

## Content

The Configuration API provides a standardized method for storing and managing a module's settings in Drupal. This tutorial covers the concepts of active configuration, simple configuration, configuration entities, and configuration schemas, and how to interact with, create, and retrieve configuration data.

By the end of this tutorial, you'll have a better understanding of how to work with configuration data in Drupal, focusing on simple configuration for module settings.

## Goal

Understand how to work with simple configuration data using Drupal's Configuration API.

## Prerequisites

- [Concept: Data Types in Drupal](https://drupalize.me/tutorial/concept-data-types-drupal)

## Understanding active configuration

*Active configuration* refers to the configuration settings currently being used by a Drupal site in a specific environment. Examples include site name, email addresses, content types, and view settings. Configuration can be stored in the database for operational use or exported to YAML files for deployment to another environment.

## Deploying configuration changes

Drupal's Configuration API facilitates the deployment of configuration between different environments, such as from development to production. This ensures consistency between instances of the site and the ability to track configuration changes across environments.

## Storing and retrieving configuration data

Drupal stores configuration data in the database which can be exported as YAML files. This dual capability facilitates the deployment of configuration across different environments, ensuring consistency and allowing for a "configuration as code" approach.

## Configuration schemas and default values

Configuration schemas define the structure and data types of configuration objects, facilitating data integrity and translation. Modules can provide default configuration values through YAML files, establishing initial settings upon installation. Modules can alter another module's configuration entities and add new fields to them.

## Simple configuration and configuration entities

Drupal distinguishes between 2 main types of configuration: *simple configuration* and *configuration entities*. Understanding the use cases for each helps module developers decide which to use when storing their module's settings.

### Simple configuration

Use simple configuration for storing key/value pairs or simple data types like strings and booleans. It's suitable for single, site-wide settings, such as API keys or user preferences.

### Configuration entities

For more complex configurations or when multiple configurations of the same type might exist, use configuration entities. Examples of configuration entities include content types, views, and image styles.

## How do developers use configuration?

- **Module settings form**: Create and retrieve simple configuration for module settings, like API keys or specific preferences.
- **Default configuration**: Provide default module configurations in YAML files, useful for pre-configuring settings.
- **Responding to configuration changes**: Implement hooks to react to configuration item updates, allowing for dynamic module behavior.
- **Configuration synchronization**: Use the Configuration API for exporting and importing configuration across different environments, ensuring consistency between the same site hosted on different environments.

## Working with configuration in code

Configuration is primarily accessed via the **configuration factory** service.

Example of retrieving and using configuration data:

```
// Load the 'anytown.settings' configuration object.
$config = \Drupal::config('anytown.settings');

// Retrieve specific configuration items.
$api_key = $config->get('api_key');
$location = $config->get('location');
```

To modify and save configuration data use the configuration management service for mutable configuration:

```
// Load the mutable configuration object for 'anytown.settings'.
$config = \Drupal::service('config.factory')->getEditable('anytown.settings');

// Set new values for specific configuration items.
$config->set('api_key', 'new_api_key')
       ->set('location', 'new_location')
       ->save();
```

## Recap

This tutorial introduced the Configuration API, focusing on simple configuration for module settings. We explored active configuration, configuration schemas, and how to manage configuration data. You'll apply these concepts when writing code that interacts with configuration data.

## Further your understanding

- How does the Configuration API's abstraction of storage details benefit module development?
- Consider a module that needs user-configurable settings. How would you decide between using simple configuration and a configuration entity?

## Additional resources

- Learn more about how configuration data is managed and deployed in this [Configuration Management course](https://drupalize.me/course/configuration-management) (Drupalize.Me)
- [Overview: Configuration Management in Drupal](https://drupalize.me/tutorial/overview-configuration-management-drupal)
- [Overview: Configuration API](https://drupalize.me/tutorial/overview-configuration-api-drupal)
- [Configuration API](https://api.drupal.org/api/drupal/core%21core.api.php/group/config_api) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Data Types in Drupal](/tutorial/concept-data-types-drupal?p=3243)

Next
[Retrieve and Update Weather Forecast Settings](/tutorial/retrieve-and-update-weather-forecast-settings?p=3243)

Clear History

Ask Drupalize.Me AI

close