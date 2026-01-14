---
title: "Plugin Managers"
url: "https://drupalize.me/tutorial/plugin-managers?p=2765"
guide: "[[alter-drupal-modules]]"
order: 13
---

# Plugin Managers

## Content

A plugin manager is responsible for both the definition of a new plugin type, and for listing and instantiating instances of plugins of the defined type.

In this tutorial we'll:

- Define what a plugin manager is.
- Create a list of all plugins of a specific type.
- Load and instantiate specific plugin instances, so we can use them in our code.

## Goal

Understand the role that a plugin manager fills, and how to access and use a plugin manager's features.

- [What is a plugin manager?](#what-is-a-plugin-manager)
- [Use a plugin manager](#use-a-plugin-manager)
- [Plugin manager class inheritance diagram](#plugin-manager-class-inheritance-diagram)
- [List all plugins of a specific type](#list-all-plugins-of-a-specific-type)
- [Get the definition of a specific plugin instance](#get-the-definition-of-a-specific-plugin-instance)
- [Instantiate an instance of a plugin by ID](#instantiate-an-instance-of-a-plugin-by-ID)

## Prerequisites

- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins)

## What is a plugin manager?

A plugin manager is the central controlling class that defines how the plugins of a particular type will be discovered and instantiated. This class is called directly in any module wishing to invoke a plugin type. By creating a new plugin manager you're also creating a new plugin type.

Plugin managers determine what method will be used for [plugin discovery](https://drupalize.me/tutorial/plugin-discovery), and thus where an individual plugin instance's metadata will be defined.

Plugin managers determine what [plugin factory](https://drupalize.me/tutorial/plugin-factories-and-mappers) is used, and thus how specific plugin instances will be instantiated.

All plugin managers are implementations of the `\Drupal\Component\Plugin\PluginManagerInterface`, which extends the `\Drupal\Component\Plugin\Discovery\DiscoveryInterface`, `\Drupal\Component\Plugin\Factory\FactoryInterface` and, `\Drupal\Component\Plugin\Mapper\MapperInterface`. That grouping forms the basis for any new plugin manager. While a custom plugin manager could implement all the methods of the component interfaces it's more likely for plugin managers to use the methods defined by these respective components, and directly implement only the additional functionality needed by the specific pluggable system.

Image

![PluginManagerInterface inheritance diagram](../assets/images/PluginManagerInterface-diagram.png)

Core already provides various implementations of these component interfaces, and when writing your own custom plugin manager you're more likely to make use of these existing components and just wire them together with information about your specific plugin type. The best way to do that is by extending `\Drupal\Core\Plugin\DefaultPluginManager`, and using that as the basis for your custom plugin manager.

Learn more about defining a new plugin manager in [Define a New Plugin Type](https://drupalize.me/tutorial/define-new-plugin-type).

## Use a plugin manager

Start by locating the machine name of the plugin manager service that represents the plugin manager you want to use. [Learn more about discovering existing services](https://drupalize.me/tutorial/discover-and-use-existing-services).

**Tip:** Plugin manager services are generally prefixed with `plugin.manager.*`.

Then request a copy of the plugin manager from the service container like so:

```
$sandwich_manager = \Drupal::service('plugin.manager.sandwich');
```

The best way to do this is to inject the plugin manager service into your controller. Here is an example:

```
<?php

namespace Drupal\plugin_type_example\Controller;

use Drupal\Core\Controller\ControllerBase;
use Drupal\plugin_type_example\SandwichPluginManager;
use Symfony\Component\DependencyInjection\ContainerInterface;

/**
 * Controller for our example pages.
 */
class PluginTypeExampleController extends ControllerBase {

  /**
   * The sandwich plugin manager.
   *
   * We use this to get all the sandwich plugins.
   *
   * @var \Drupal\plugin_type_example\SandwichPluginManager
   */
  protected $sandwichManager;

  /**
   * Constructor.
   *
   * @param \Drupal\plugin_type_example\SandwichPluginManager $sandwich_manager
   *   The sandwich plugin manager service. We're injecting this service so that
   *   we can use it to access the sandwich plugins.
   */
  public function __construct(SandwichPluginManager $sandwich_manager) {
    $this->sandwichManager = $sandwich_manager;
  }

  /**
   * {@inheritdoc}
   *
   * Override the parent method so that we can inject our sandwich plugin
   * manager service into the controller.
   *
   * For more about how dependency injection works read https://www.drupal.org/node/2133171
   */
  public static function create(ContainerInterface $container) {
    // Inject the plugin.manager.sandwich service that represents our plugin
    // manager as defined in the plugin_type_example.services.yml file.
    return new static($container->get('plugin.manager.sandwich'));
  }

}
```

## Plugin manager class inheritance diagram

Image

![Diagram showing SandwichPluginManager methods and which class they are inherited from.](../assets/images/SandwichPluginManager-diagram.png)

## List all plugins of a specific type

Call the `getDefinitions()` method to get information about all defined plugins.

When using the `DefaultPluginManager`, data is retrieved from cache when available. Otherwise, control is delegated to the [discovery handler](https://drupalize.me/tutorial/plugin-discovery) which locates all plugin definitions of the type in question within all enabled modules.

Usage example:

```
// Get the list of all the sandwich plugins defined on the system from the
// plugin manager. Note that at this point, what we have is *definitions* of
// plugins, not the plugins themselves.
$sandwich_plugin_definitions = $this->sandwichManager->getDefinitions();

// Let's output a list of the plugin definitions we now have.
$items = array();
foreach ($sandwich_plugin_definitions as $sandwich_plugin_definition) {
  // Here we use various properties from the plugin definition. These values
  // are defined in the attributes at the top of the plugin class: see
  // \Drupal\plugin_type_example\Plugin\Sandwich\ExampleHamSandwich.
  $items[] = t("@id (calories: @calories, description: @description )", array(
    '@id' => $sandwich_plugin_definition['id'],
    '@calories' => $sandwich_plugin_definition['calories'],
    '@description' => $sandwich_plugin_definition['description'],
  ));
}

// Add our list to the render array.
$build['plugin_definitions'] = array(
  '#theme' => 'item_list',
  '#title' => 'Sandwich plugin definitions',
  '#items' => $items,
);
```

This method is useful anytime you want to get a list of all the plugins of a given type. In practice this is mostly commonly used to display a list to an administrator (like in the Block layout UI), or to populate a select list element in a form to allow an administrator to choose from a list of defined plugins (like in the field type selection form).

## Get the definition of a specific plugin instance

Call the `getDefinition($plugin_id)` method, and pass in the unique ID of a plugin, to retrieve the definition for just that plugin.

Usage example:

```
// If we want just a single plugin definition, we can use getDefinition().
// This requires us to know the ID of the plugin we want. This is set in the
// attributes on the plugin class: see \Drupal\plugin_type_example\Plugin\Sandwich\ExampleHamSandwich.
$ham_sandwich_plugin_definition = $this->sandwichManager->getDefinition('meatball_sandwich');
```

This is useful when you want to retrieve the metadata for a single plugin instance and already know the ID. Continuing the example from above, if the administrator already choose specific plugin from the list, and we stored the ID in configuration we can now retrieve more information about the selected plugin instance on demand.

## Instantiate an instance of a plugin by ID

Use the `createInstance($plugin_id)` method to instantiate, and then use, individual plugin objects.

The **DefaultPluginManager's** `createInstance()` method is a **wrapper** around the [chosen factory class'](https://drupalize.me/tutorial/plugin-factories-and-mappers) `createInstance()` method. It works by first looking up what factory class should be used, then calling its `createInstance()` and passing in a plugin ID. The factory uses the definition of the specific plugin to figure out what class represents the plugin, then instantiates it and returns the result.

Usage example:

```
// To get an instance of a plugin, we call createInstance() on the plugin
// manager, passing the ID of the plugin we want to load. Let's output a
// list of the plugins by loading an instance of each plugin definition and
// collecting the description from each.
$items = array();
// The array of plugin definitions is keyed by plugin id, so we can just use
// that to load our plugin instances.
$sandwich_plugin_definitions = $this->sandwichManager->getDefinitions();
foreach ($sandwich_plugin_definitions as $plugin_id => $sandwich_plugin_definition) {
  // We now have a plugin instance. From here on it can be treated just as
  // any other object; have its properties examined, methods called, etc.
  $plugin = $this->sandwichManager->createInstance($plugin_id);
  $items[] = $plugin->description();
}
```

Any time you want to make use of an individual plugin object you should use the plugin manager to instantiate the object rather than doing so directly.

## Recap

In this tutorial we said that a plugin manager is a class that glues together a discovery mechanism, and a method for instantiating plugin instances in order to define a new plugin type. Once the new type is defined the plugin manager class can be used to list and instantiate plugins of the defined type.

Plugin managers should be defined as services, and accessed via the dependency injection container.

We showed how to inject a plugin manager into a controller, and then we looked at using the two most common methods, `getDefinitions()`, and `createInstance()`.

## Further your understanding

- Look at the documentation for additional public methods of the `DefaultPluginManager` class to get a sense of what others exist.
- See if you can combine your understanding of using plugin managers with Drupal's [configuration management system](https://drupalize.me/series/configuration-management) to [create a settings form](https://drupalize.me/tutorial/create-settings-form-module) that allows an administrator to choose one from a list of plugins, and then on another page instantiate and call the selected plugin.

## Additional resources

- [class PluginManager](https://api.drupal.org/api/drupal/core!modules!system!tests!modules!lazy_route_provider_install_test!src!PluginManager.php/class/PluginManager) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Implement a YAML Plugin](/tutorial/implement-yaml-plugin?p=2765)

Next
[Plugin Discovery](/tutorial/plugin-discovery?p=2765)

Clear History

Ask Drupalize.Me AI

close