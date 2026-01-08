---
title: "Plugin Discovery"
url: "https://drupalize.me/tutorial/plugin-discovery?p=2765"
guide: "[[alter-drupal-modules]]"
---

# Plugin Discovery

## Content

In order for a plugin manager to locate instances of individual plugins within the Drupal code base it needs to know where to look, and how to interpret the data that it finds. This process is called plugin discovery and can be accomplished in several ways.

In this tutorial, we'll look at what plugin discovery is doing at a high level, and then talk about the plugin discovery methods you can choose from when defining a new plugin type.

## Goal

Understand the use case for each of the plugin discovery methods provided by Drupal core.

## Prerequisites

- Discovery is per [plugin type](https://drupalize.me/tutorial/drupal-plugin-types)
- The mechanism used is determined by the [plugin manager](https://drupalize.me/tutorial/plugin-managers)

## Plugin discovery

- [What is plugin discovery?](#discovery)
- [PHP attributes class discovery](#php-attributes)
- [Annotated class discovery](#annotations)
- [YAML discovery](#yaml)
- [Hook discovery](#hook)
- [Static discovery](#static)

Sprout Video

## What is plugin discovery?

Plugin discovery is the process of locating the metadata for all plugins of a specific type.

One of the main responsibilities of the [plugin manager](https://drupalize.me/tutorial/plugin-managers) is to locate--or discover--any implementations of the plugin type that it's responsible for. Consider block plugins for example. Any module that's enabled can provide a new block to Drupal in the form of a plugin. The `BlockPluginManager` needs to know which modules are enabled and where to find any block plugins those modules provide in order to do things like add them to the list of blocks that can be placed via the block administration screen.

At its most basic, this works because the `BlockPluginManager` has defined a pattern that any module can follow that includes where to place the PHP code that implements the block plugin and where to find metadata about any block plugin. As a module developer you simply follow that pattern and your block plugins will be located by the `BlockPluginManager`.

Here are the plugin discovery mechanisms that core supports. And while you could certainly write your own, don't underestimate the additional features like caching that you get for free when using one these existing components.

All discovery mechanisms are implementations of `\Drupal\Component\Plugin\Discovery\DiscoveryInterface`, and provide `getDefinitions()`, `getDefinition()` and, `hasDefinition($plugin_id)` methods.

A plugin manager can define which method is used by overriding the `DefaultPluginManager::getDiscovery()` method and choosing a new method.

**Note:** Of the methods listed below, PHP attributes, and YAML are the most commonly used. Annotations, while still supported, should be considered deprecated as of Drupal 10.3/11.0. When determining which method to use for your plugin type, default to PHP attributes unless you have a good reason not to.

## PHP attributes class discovery

Provided by the `\Drupal\Component\Plugin\Discovery\AttributeClassDiscovery` class, this is the most commonly used discovery component in core, and the recommended method to use when creating a new plugin manager. Plugins are discovered by using the [PSR-4 standard](https://drupalize.me/blog/201408/preparing-drupal-8-psr-4-autoloading) to locate a file that contains the definition of the plugin in the form of a class, and [PHP attributes](https://drupalize.me/tutorial/php-attributes) to provide metadata to the plugin manager.

Developers wishing to use PHP attributes class discovery need to provide:

- A PHP sub-namespace and class that extends the `\Drupal\Component\Plugin\Attribute\Plugin` class
- A constructor method that defines the information that should be entered into the attributes for a plugin of this type

The following example looks for any class in the `Drupal\MODULENAME\Plugin\Block` namespace with an attribute based on the `Drupal\block\Attribute\Block` class. Any classes found with the appropriate attribute, in the appropriate PSR-4 namespace, are treated as block plugins.

```
MyPluginManager::discovery = new AttributeClassDiscovery(‘Plugin/Block’, $namespaces, 'Drupal\block\Attribute\Block');
```

**Note:** While annotations are being phased out in favor of PHP attributes, they are still supported, and you'll often see `\Drupal\Core\Plugin\Discovery\AttributeDiscoveryWithAnnotations` used for discovery. Provided for backward compatibility, this class will find plugins that use *either* PHP attributes or annotations, as long as they are in the correct namespace.

## Annotated class discovery

This discovery method used to be the most common but is being phased out in favor of PHP attributes. It is good to be aware of it since you'll likely encounter annotated class discovery in existing code bases. But if you're starting a new plugin manager, PHP attributes class discovery is recommended.

Provided by the `\Drupal\Core\Plugin\Discovery\AnnotatedClassDiscovery` class, plugins are discovered by using the [PSR-4 standard](https://drupalize.me/blog/201408/preparing-drupal-8-psr-4-autoloading) to locate a file that contains the definition of the plugin in the form of a class, and [annotations in the @docblock for the class](https://drupalize.me/tutorial/annotations) to provide metadata to the plugin manager.

Developers wishing to use annotated class discovery need to provide:

- A PHP sub-namespace and class that extends the `Drupal\Components\Annotations\Plugin` class
- Metadata in the class' annotation that defines the necessary information for a plugin of this type

The following example looks for any class in the `Drupal\MODULENAME\Plugin\Block` namespace with an annotation that follows the form provided by `Drupal\block\Annotation\Block`. Any classes found with the appropriate annotation, in the appropriate PSR-4 namespace, are treated as block plugins.

```
MyPluginManager::discovery = new AnnotatedClassDiscovery(‘Plugin/Block’, $namespaces, 'Drupal\block\Annotation\Block');
```

## YAML discovery

Provided by the `\Drupal\Core\Plugin\Discovery\YamlDiscovery` class, YAML discovery uses a *.yml* file with a special name located in the root directory of any enabled module to get a list of plugins of the given type provided by that module as well as metadata for those plugins. YAML discovery is used for things like the definition of menu items, breakpoints, and contextual links. The plugin itself can be instantiated and used simply from the metadata provided in the YAML file. No custom PHP based processing is necessary at the individual module level.

The following example would look for a file named *MODULENAME.sandwich.yml* in the root directory of any enabled modules, and use the information contained in the *.yml* file to generate a list of plugins of the given type and their metadata.

```
MyPluginManager::discovery = new YamlDiscovery('sandwich', $module_handler->getModuleDirectories());
```

In this case a single *.yml* file can define one or more plugin instances.

There is also `\Drupal\Core\Plugin\Discovery\YamlDirectoryDiscovery` which can be used to allow for individual plugin instances to reside in their own *.yml* files. One plugin per *.yml* file.

## Hook discovery

Hook-based discovery is provided in order to allow for the gradual transition from Drupal 7 era info hooks to annotated class discovery. It is no longer used anywhere in Drupal core. But, for the sake of completeness, here is how it works.

Provided by the `\Drupal\Core\Plugin\Discovery\HookDiscovery` class, hook-based discovery is similar to the Drupal 7 info hook pattern in which all PHP functions that follow a specific naming convention are called and expected to return an associative array that tells the system where to find plugins of the given type. Hook based discovery is less common and is primarily used for legacy support.

The following example looks for any `MODULENAME_block_info()` functions, calls them, and aggregates their return value into a list of block plugins. That list can then be used to locate any individual plugin instance.

```
MyPluginManager::discovery = new HookDiscovery($this->moduleHandler, 'block_info');
```

## Static discovery

Provided by the `\Drupal\Component\Plugin\Discovery\StaticDiscovery` class, static discovery allows plugin definitions to be manually registered rather than dynamically discovered like the other three methods. This requires any module that wishes to implement a plugin of the given type to manually register their provided plugin instance with the plugin manager. Static discovery is currently only used for tests, and you'll rarely if ever use this mechanism in your own module. It's kind of like if the customer showed up at your sandwich shop, and handed you a ham sandwich, and then asked if you had any ham sandwiches.

Example:

```
MyPluginManager::discovery = new StaticDiscovery();
```

## Recap

Plugin discovery is the process of locating the metadata for individual plugin instances so that the plugin manager can be aware of what plugins are available. Drupal core provides a handful of different methods for discovery, with PHP attribute class discovery being the preferred mechanism for most use cases. A plugin manager can determine which discovery method to use, and sets some basic patterns like the PSR-4 namespace classes should reside in, or the name to use for YAML files.

## Further your understanding

- [Plugin Derivatives](https://drupalize.me/tutorial/plugin-derivatives) allow a single generic plugin instance to stand in for many dynamic plugins during the discovery process.

## Additional resources

- [Drupal Plugin Discovery](https://www.drupal.org/docs/drupal-apis/plugin-api/drupal-plugin-discovery) (Drupal.org)
- [`DiscoveryInterface`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Component%21Plugin%21Discovery%21DiscoveryInterface.php/interface/DiscoveryInterface/) (api.drupal.org)
- [Overview of the Drupal 8 Plugin System](https://amsterdam2014.drupal.org/session/overview-drupal-8-plugin-system.html) - DrupalCon presentation that covers plugin discovery mechanisms (amsterdam2014.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Plugin Managers](/tutorial/plugin-managers?p=2765)

Next
[Plugin Factories and Mappers](/tutorial/plugin-factories-and-mappers?p=2765)

Clear History

Ask Drupalize.Me AI

close