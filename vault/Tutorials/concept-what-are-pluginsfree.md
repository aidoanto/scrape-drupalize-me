---
title: "Concept: What Are Plugins?free"
url: "https://drupalize.me/tutorial/concept-what-are-plugins?p=3241"
guide: "[[drupal-module-developer-guide]]"
---

# Concept: What Are Plugins?free

## Content

Plugins enable developers to extend and customize functionality through a modular and reusable system. Plugins allow for the creation of interchangeable components that can be managed dynamically at runtime. This tutorial introduces the core concepts of Drupal's Plugin API, including how plugins, such as blocks, are defined, discovered, and used within the system.

In this tutorial, we'll:

- Define plugins in Drupal's context.
- Explain the Plugin system's operation, including types, managers, discovery, and factories.
- Discuss the role of plugins in extending Drupal.

By the end of this tutorial, you should have a high-level understanding of plugins and the Plugin API in Drupal.

## Goal

Explain the essentials of Drupal's Plugin API to understand how plugins extend and enhance site functionality.

## Prerequisites

- [Concept: What Are Modules?](https://drupalize.me/tutorial/concept-what-are-modules)
- [Concept: What Are Hooks?](https://drupalize.me/tutorial/concept-what-are-hooks)
- [Concept: PHP Namespaces and PSR-4](https://drupalize.me/tutorial/concept-php-namespaces-and-psr-4)
- [Create a Custom "Hello, World!" Block](https://drupalize.me/tutorial/create-custom-hello-world-block)
- Familiarity with Drupal's block system, which uses the Plugin API. Refer to [Chapter 8: Blocks](https://drupalize.me/course/user-guide/blocks-chapter) in the Drupal User Guide.

## Understanding plugins

A plugin is a swappable piece of functionality, allowing for varied implementations under the same interface. Plugins address the need for modules to offer "things" with identical interfaces but distinct functionality. Plugins are primarily used in scenarios where a user needs to be able to choose one or more options from a list.

Examples of plugins include:

- Blocks
- Render API elements
- Actions triggered on events
- Image styles
- Field types, widgets, and formatters
- Menu items

### Plugin system components

The Plugin API includes:

- **Plugin types**: Categories for plugins; for example, blocks or field formatters.
- **Plugin manager**: A service for discovering and instantiating plugins of a specific plugin types, like the block plugin manager.
- **Plugin instances**: Functional units that conform to a plugin type's definition, like the code for an individual block.

## Plugin operation

When Drupal needs to perform an action that uses plugins, it follows this process:

1. The relevant **plugin manager** is called upon to handle a specific plugin type.
2. The manager uses its **discovery method** to find all available plugins of that type.
3. When needed, the **plugin factory** instantiates the chosen plugin instance(s), possibly with additional configuration.

### Plugin discovery

Discovery identifies and gathers metadata for all plugins of a type. The most common discovery method is PHP attributes (formerly PHP annotations), but others, like YAML and hook-based discovery, also exist. You'll need to know the discovery mechanism to know what kind of code to write for a plugin.

Plugin discovery also supports derivatives. This allows for plugin instances that are created dynamically based on records in the database or other configuration. For example, blocks created in the UI via the *Block Content* module.

### Plugin factory

The factory instantiates specific plugins, and is accessed via the plugin manager. You only need to know about plugin factories if you're implementing a new plugin type.

## Example: Creating a custom block

In [Create a Custom "Hello, World!" Block](https://drupalize.me/tutorial/create-custom-hello-world-block) we created a custom block. Creating a custom block in Drupal involves defining a new plugin of the block plugin type. The block's functionality and presentation are encapsulated within the plugin, allowing it to be added to pages via Block Layout UI. In [Implement a Block Plugin](https://drupalize.me/tutorial/implement-block-plugin), we'll revisit the "Hello, World!" block plugin we previously created, this time through the lens of the Plugin API.

## Recap

The Plugin API is a central part of Drupal's architecture. It provides a way for us to extend and customize functionality through a system of plugin types, discovery, and instantiation. By leveraging plugins, developers can create modular and reusable components that enhance Drupal's capabilities.

## Further your understanding

- Compare plugins with other Drupal extensibility mechanisms like hooks and events.
- Identify a Drupal site feature where introducing a new plugin type is beneficial.

## Additional resources

- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins) (Drupalize.Me)
- [Plugin Discovery](https://drupalize.me/tutorial/plugin-discovery) (Drupalize.Me)
- [Plugin Factory](https://drupalize.me/tutorial/plugin-factories-and-mappers) (Drupalize.Me)
- [PHP Attributes](https://drupalize.me/tutorial/php-attributes) (Drupalize.Me)
- [Annotations](https://drupalize.me/tutorial/annotations) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Implement a Block Plugin](/tutorial/implement-block-plugin?p=3241)

Clear History

Ask Drupalize.Me AI

close