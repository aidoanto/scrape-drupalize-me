---
title: "Overview: Configuration API in Drupal"
url: "https://drupalize.me/tutorial/overview-configuration-api-drupal?p=2476"
guide: "[[work-data-modules]]"
order: 20
---

# Overview: Configuration API in Drupal

## Content

Drupal stores the settings that define how a site behaves as configuration data. Everything from the site name to image styles, roles, and view definitions are stored as **configuration**. The Configuration API gives modules, themes, and installation profiles a consistent way to store, retrieve, update, and provide this configuration in a structured and portable way.

In this tutorial, we'll:

- Provide a high-level overview of the features of Drupal's Configuration API
- Link to related tutorials where you can learn more and get hands-on practice working with configuration data in code.

## Goal

Get a high-level understanding of how modules use Drupal's Configuration API to store configuration as simple configuration or configuration entities.

## Prerequisites

- [Overview: Configuration Management in Drupal](https://drupalize.me/tutorial/overview-configuration-management-drupal)

## What is the Configuration API?

The Configuration API is Drupal's system for storing the information that defines **how a site works**. This includes configuration provided by modules, themes, and installation profiles, as well as configuration site builders create through the UI.

The Configuration API provides a unified way to:

- Store configuration in named configuration objects
- Retrieve configuration at runtime
- Update configuration safely
- Specify default and optional configuration shipped with an extension
- Keep configuration structured and portable so it can be exported, versioned, and synchronized across environments

Every piece of configuration lives inside a uniquely named configuration object. These objects can represent:

- **Simple configuration**: A single set of module or system settings
- **Configuration entities**: User-created items like view definitions, content types, or image styles.

Instead of worrying about where configuration is stored (database, files, or another backend), developers work with it through the Configuration API, which handles storage, overrides, and language concerns behind the scenes.

Learn more:

- [Configuration Data Types](https://drupalize.me/tutorial/configuration-data-types)

## Watch: Introduction to Configuration Entities

Sprout Video

## Default and optional configuration

Modules can ship with **default configuration**, which is installed automatically when the module is enabled. This ensures the module starts with functional baseline settings.

Modules can also provide **optional configuration**, which installs only when all of its dependencies are available. This is useful for providing examples, sample configuration, or optional features that depend on other modules.

Learn more:

- [Default Configuration in a Module](https://drupalize.me/tutorial/default-configuration-module)

## Simple configuration

Use **simple configuration** when your module needs a single set of settings for the entire site. Examples include:

- A module's global settings
- A default option or toggle
- A text value or API key
- Any configuration that has only *one* copy per site

Simple configuration is ideal for **module settings forms** and other situations where site builders need to manage a fixed set of values. As a module developer, you'll need to understand how to access an **editable configuration object** if you want to be able to update it using a form.

Learn more:

- [Provide Initial Settings with Simple Configuration](https://drupalize.me/tutorial/provide-initial-settings-simple-configuration)
- [Create a Settings Form in a Module](https://drupalize.me/tutorial/create-settings-form-module)
- [Use Simple Configuration in a Form](https://drupalize.me/tutorial/use-simple-configuration-form)

## Configuration entities

Use **configuration entities** when your module needs to store **multiple items** of the same type—items that site builders can create, edit, and manage. Examples from Drupal core include:

- Content types
- Image styles
- Views
- Roles

Configuration entities are unique because they participate in two of Drupal's APIs: Entity API and Configuration API.

Each configuration entity item is stored as its own configuration object (for example, `image.style.thumbnail`) and can be exported, imported, and synchronized across environments. Modules can provide default or optional configuration entities that install when the module is enabled.

Because configuration entities are also entities, they use the Entity API to define:

- Entity type metadata
- Canonical IDs
- Forms for creating and editing items
- List builders for administration pages
- Access handling and validation
- Dependency tracking and relationships to other configuration objects

This dual nature gives configuration entities the structure and UI integration of the Entity API along with the portability of the Configuration API. For example, to access and list configuration entities in a module, such as in a form, use the Entity API's `EntityTypeManager`.

Learn more:

- [Create a Configuration Entity Type](https://drupalize.me/tutorial/create-configuration-entity-type)
- [Add Properties to a Configuration Entity Type](https://drupalize.me/tutorial/add-properties-configuration-entity-type)
- [Use Configuration Entities in a Module's Settings Form](https://drupalize.me/tutorial/use-configuration-entities-modules-settings-form)

## Recap

Drupal's Configuration API provides a consistent way for modules, themes, and installation profiles to store the settings that define how a site works. Simple configuration handles single, site-wide values, while configuration entities represent collections of user-created items that integrate with both the Entity API and the Configuration API. Understanding these concepts will help you design modules that work cleanly with Drupal's configuration system.

## Further your understanding

- Which settings in your module represent a single site-wide value, and which might need to become user-created configuration entities?
- What default configuration would help someone start using your module immediately after enabling it?

## Additional resources

- [Concept: Configuration API](https://drupalize.me/tutorial/concept-configuration-api) (Drupalize.Me)
- [Chapter 9: Working with Data (Module Developer Guide)](https://drupalize.me/guide/drupal-module-developer-guide) (Drupalize.Me)
- [Configuration API](https://api.drupal.org/api/drupal/core%21core.api.php/group/config_api/) (api.drupal.org)
- Course: [Configuration Management in Drupal](https://drupalize.me/course/configuration-management-drupal) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Configuration Data Types](/tutorial/configuration-data-types?p=2476)

Clear History

Ask Drupalize.Me AI

close