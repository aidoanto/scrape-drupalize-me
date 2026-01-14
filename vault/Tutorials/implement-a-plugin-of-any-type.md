---
title: "Implement a Plugin of Any Type"
url: "https://drupalize.me/tutorial/implement-plugin-any-type?p=2765"
guide: "[[alter-drupal-modules]]"
order: 9
---

# Implement a Plugin of Any Type

## Content

Drupal uses plugins for a lot of different scenarios. Blocks, field types, menu items, breakpoints, and migrations are all examples of plugins. There are a couple of different types of plugins. Before you can create a new plugin of any type, you'll need to figure out where the plugin implementation and its metadata should live in the code base, so that the [plugin manager](https://drupalize.me/tutorial/plugin-managers) can [find plugins](https://drupalize.me/tutorial/plugin-discovery), and examine what functionality instances of the plugin type are expected to provide.

In this tutorial we'll:

- Demonstrate how to figure out what *type* of plugin you're dealing with.
- Point to additional resources showing how to implement the specific plugin type once it has been determined.

By the end of this tutorial you should have a better understanding of how to figure out the details required to implement any given plugin type.

## Goal

Guide learners to tutorials on implementing plugins based specifically on the plugin type's discovery mechanism.

## Prerequisites

The Plugin API builds on a number of other Drupal APIs and PHP design patterns. Understanding how these work will make it easier to implement custom plugins, and to recognize which parts of the implementation are specific to the Plugin API.

- PHP [class inheritance](https://drupalize.me/videos/introduction-inheritance-php?p=2379) and [interfaces](https://drupalize.me/videos/introduction-interfaces?p=2379) are used extensively in the Plugin API.
- Implementing Plugins requires that you understand [the PSR-4 standard and how it's used in Drupal](https://drupalize.me/blog/201408/preparing-drupal-8-psr-4-autoloading).
- Most plugin types that you'll implement in custom code use [PHP attributes](https://drupalize.me/tutorial/php-attributes).
- Prior to Drupal 11 [annotations](https://drupalize.me/tutorial/annotations) were commonly used for plugins.
- Most plugin implementations use [dependency injection](https://drupalize.me/topic/dependency-injection) to make use of [services](https://drupalize.me/topic/services). Specifically, Drupal plugins use the [factory injection pattern](https://www.lullabot.com/articles/injecting-services-in-your-d8-plugins).

## Implement a plugin once you know what type it is

Once you know what type of plugin you're dealing with, follow the corresponding tutorial:

- [Implement a Plugin Using PHP Attributes](https://drupalize.me/tutorial/implement-plugin-using-php-attributes)
- [Implement a Plugin Using Annotations](https://drupalize.me/tutorial/implement-plugin-using-annotations)
- [Implement a Plugin Using YAML](https://drupalize.me/tutorial/implement-yaml-plugin)

## Figure out what type of plugin you're dealing with

If you don't know which of the above plugin types you're dealing with, here's how to figure it out.

### Find an existing example in use

Start by finding an example in use. Since plugins are most often used in the scenario where Drupal allows an administrator to choose one from a list of options first, find the existing list in the UI. Make note of the name of one of the existing options (this is most likely the "Label" of the plugin instance).

Or see if you can figure out the ID of the existing plugin instance. Look at the URL and inspect the source of any `<select>` elements on the page for clues.

### Locate the code for the existing instance

Once you know the label or ID, search the codebase for that string. It might help to search for the string inside of quotations marks to narrow it down. Example: `"User login"`. Look for instance of this string in a class that's in the `Plugin\*` namespace.

### Inspect the existing code

Once you've found the code that implements the existing instance you should be able to figure what type of plugin it is. Refer to the plugin type specific tutorials above to continue.

## Look at the plugin manager

To get exact details about a plugin types discovery mechanism, look at the [plugin manager](https://drupalize.me/tutorial/plugin-managers). The plugin manager service will be a class that extends `DefaultPluginManager` and provides implementation details like the PSR-4 sub-namespace, which class is used for attributes (or annotations), and the interface that plugin instances implement.

## More examples of implementing plugins

For some practical examples of implementing plugins see these tutorials:

- [Define a New Render Element Type](https://drupalize.me/tutorial/define-new-render-element-type)
- [Field Formatters](https://drupalize.me/tutorial/field-formatters), [Field Widgets](https://drupalize.me/tutorial/field-widgets), and [Field Types](https://drupalize.me/tutorial/field-types)
- [Create a Custom Content Entity](https://drupalize.me/tutorial/create-custom-content-entity)
- [Create a Configuration Entity Type](https://drupalize.me/tutorial/create-configuration-entity-type)

## Recap

Being able to implement a plugin requires first figuring out what discovery mechanism is being used and then following the pattern, so your plugin code can be discovered. The quickest way to do that is to look for an existing implementation and copy that. If that doesn't work, the exact details can always be figured out by looking at the code in the plugin manager.

## Additional resources

- [DrupalCon Los Angeles 2015: An Overview of the Drupal 8 Plugin System](https://www.youtube.com/watch?v=gd6s4wC_bP4) (YouTube.com)
- [Drupal’s Plugin API – an introduction through examples](https://manifesto.co.uk/drupal-plugin-api-examples-tutorial/) (manifest.co.uk)
- [Plugins (Plugin API)](https://drupalize.me/topic/plugins-plugin-api) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Discover Existing Plugin Types](/tutorial/discover-existing-plugin-types?p=2765)

Next
[Implement a Plugin Using PHP Attributes](/tutorial/implement-plugin-using-php-attributes?p=2765)

Clear History

Ask Drupalize.Me AI

close