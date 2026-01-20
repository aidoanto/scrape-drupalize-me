---
title: "Plugin Factories and Mappers"
url: "https://drupalize.me/tutorial/plugin-factories-and-mappers?p=2765"
guide: "[[alter-drupal-modules]]"
order: 15
---

# Plugin Factories and Mappers

## Content

Learn how the Plugin API takes a given plugin ID and uses it to instantiate and return a fully configured plugin object. In this tutorial we'll look at:

- What factories are, and the role they serve in the Plugin API
- The factories available in core
- Using mappers to dynamically load a plugin when you don't know the ID of the specific plugin you need.

## Goal

Understand the use case for each of the plugin factories provided by Drupal core.

## Prerequisites

- A factory is per [plugin type](https://drupalize.me/tutorial/drupal-plugin-types)
- [Plugin Discovery](https://drupalize.me/tutorial/plugin-discovery)
- And the factory used is determined by the [plugin manager](https://drupalize.me/tutorial/plugin-managers)

## Contents

- [What are plugin factories?](#factories)
- [Default factory](#default)
- [Container factory](#container)
- [Reflection factory](#reflection)
- [Mappers](#mappers)

Sprout Video

## What are plugin factories?

A plugin manager needs to be able to respond to requests for a plugin with a given ID by returning an instance of the instantiated plugin. When I request the `system_powered_by_block` plugin from the block manager I expect that it will return an instance of the `Drupal\system\Plugin\Block\SystemPoweredByBlock` class and that I can get right down to displaying the content of that block without having to bother loading any files or classes or knowing anything about how to instantiate the `SystemPoweredByBlock`.

This is the domain of the plugin factory: a system for generically requesting an instance of a plugin without having to know anything about how that plugin type is handled. Just like with plugin discovery, Drupal core provides a handful of useful implementations of the `FactoryInterface` that we can use in our own plugin manager to instantiate plugin instances.

It really boils down to this: given a unique plugin ID, what class should I instantiate and what arguments should I use when doing so?

To accomplish this the plugin API uses the [factory design pattern](https://en.wikipedia.org/wiki/Factory_(object-oriented_programming)). And the plugin manager proxies the request to a factory class.

Factories provide the plugin manager with a `MyPluginManager::createInstance()` method which proxies the request to the selected factory class, which, in turn, can instantiate and return the specified plugin instance.

The factories described below are provided by Drupal core. You can always write your own, but these should serve most use cases and provide some baked-in goodness like caching to help speed up the system. In order to describe how these work we'll take a look at what happens for each factory type when you call the plugin managers `MyPluginManager::createInstance()` method.

Plugin factories implement `\Drupal\Component\Plugin\Factory\FactoryInterface`.

## The default factory

**Note:** Default is listed first here because it's the most basic. However, the container factory is the one that is actually used by default in Drupal core, and most likely the one you'll want to use.

The simplest factory is provided by the `Drupal\Component\Plugin\Factory\DefaultFactory` class, which simply answers the questions: What class should I instantiate? What arguments should I pass to it? The discovery component takes care of locating the plugin and providing the manager with a class name. The default factory then maps a plugin ID to a class, instantiates a copy of that class with a set of common arguments, and returns it. The arguments consist of any additional configuration passed to the `createInstance()` method when it is called, along with the ID of the plugin being instantiated, and the definition of the plugin as returned by the discovery mechanism. In most cases this would be the metadata contained in the attributes for your plugin.

Example return from `DefaultFactory::createInstance()` for the plugin class `HamSandwich`:

```
// Arguments passed to __construct() method:
// - $configuration (array): Passed to the createInstance() method from caller.
// - $plugin_id (string): Unique ID of the plugin being instantiated.
// - $plugin_definition (array): Plugin metadata read from the attributes.
return new HamSandwich($configuration, $plugin_id, $plugin_definition);
```

Use this when you're sure that the plugin instances will be fully self-contained.

## The container factory

Contrary to what the name implies, this is actually the default and recommended factory for most use cases.

The `Drupal\Core\Plugin\Factory\ContainerFactory` class extends the `Drupal\Component\Plugin\Factory\DefaultFactory` class and as such does the same things with one major addition: it injects a copy of the Drupal services container by calling the plugin's `::create()` method and performing constructor injection. This is useful if plugins managed by your new plugin manager need to have access to the services container in order to do whatever it is they do.

The container factory is also smart enough to recognize when a particular instance of a plugin doesn't use the container injection pattern (that is, doesn't implement a `::create()` method) and falls back to instantiating the plugin just like the `DefaultFactory`. This is nice because then each individual instance of a plugin can decide on its own whether it needs the service container or not. It also makes the `ContainerFactory` likely the best choice if you can't decide.

Example return from `ContainerFactory::createInstance()` for the plugin class `CheeseSandwich`.

```
// Arguments passed to create() method:
// - $container: A copy of the Drupal service container.
// - $configuration (array): Passed to the createInstance() method from caller.
// - $plugin_id (string): Unique ID of the plugin being instantiated.
// - $plugin_definition (array): Plugin metadata read from the attributes.
return CheeseSandwich::create(\Drupal::getContainer(), $configuration, $plugin_id, $plugin_definition);
```

Use this whenever plugin instances might need to use other services available in the service container to perform their functionality.

## The reflection factory

If you need a bit more flexibility and want to allow plugins handled by your plugin manager to be able to allow for a variable or unknown set of arguments in their constructor you can use the `Drupal\Component\Plugin\Factory\ReflectionFactory` class. This factory will perform some introspection on the class that it's about to instantiate and derive the list of arguments to pass to the constructor based on the method signature of the constructor itself.

## Mappers

Mappers provide an additional layer of abstraction around plugin factories. Similar to [decorators for discovery](https://drupalize.me/tutorial/plugin-discovery), they allow for extra processing to take place prior to creating an instance of a plugin. Mappers are used when the plugin manager needs to locate a plugin instance based on application context instead of via a unique ID. This is useful when the calling code knows it needs a plugin but doesn't necessarily know which one. Mappers provide the plugin manager with a `::getInstance()` method that can return the correct plugin based on additional logic.

An example use case for mappers includes the *mail manager*, responsible for sending email from Drupal. As a developer, I just want to send an email and don't want to specify how it is sent. The plugin manager, however, needs to allow for the possibility that there are many different methods for sending an email with PHP. So, when I call the manager's `getInstance()` method the mail manager will first look up in my applications configuration which mail system it should use, load the relevant plugin, and return an instance of that plugin ready for me to make use of.

Because the `PluginManagerInterface` extends the `MapperInterface` the presence of a `getInstance()` method is already expected. Should you want to provide a custom mapper for your plugin manager the best way is to override this method with your custom logic in `MyManager::getInstance()`.

Check out the example from `\Drupal\Core\Field\FormatterPluginManager::getInstance()` to get an idea of how this might work.

## Recap

Instances of a plugin object are instantiated via a plugin factory. Which factory is used is determined by the plugin manager. The most common factory, `ContainerFactory`, allows individual plugin instances to opt-in to having elements from the service container injected into their constructor by implementing `\Drupal\Core\Plugin\ContainerFactoryPluginInterface`.

Mappers allow for loading a plugin instance based on application's state and configuration instead of via its unique ID. This is useful when you need to infer the plugin to use based on contextual data.

## Further your understanding

- What is the primary difference between the default and container factories? When should you use each one?
- Can you give an example of when a custom mapper might be useful when defining a new plugin type?

## Additional resources

- [ContainerFactory](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Plugin!Factory!ContainerFactory.php/class/ContainerFactory) (api.drupal.org)
- [ContainerFactoryPluginInterface](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Plugin%21ContainerFactoryPluginInterface.php/interface/ContainerFactoryPluginInterface/) (api.drupal.org)
- [FormatterPluginManager::getInstance](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Field%21FormatterPluginManager.php/function/FormatterPluginManager%3A%3AgetInstance/) (api.drupal.og)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Plugin Discovery](/tutorial/plugin-discovery?p=2765)

Next
[Plugin Derivatives](/tutorial/plugin-derivatives?p=2765)

Clear History

Ask Drupalize.Me AI

close