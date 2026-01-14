---
title: "Plugin Derivatives"
url: "https://drupalize.me/tutorial/plugin-derivatives?p=2765"
guide: "[[alter-drupal-modules]]"
order: 16
---

# Plugin Derivatives

## Content

Plugin derivatives allow a single plugin to dynamically generate multiple plugin instances based on configuration or other data. This is useful for situations where user-entered data, or other dynamic configuration, might have an impact on available plugins. Or, put another way, any time you need to be able to dynamically generate plugin definitions.

In this tutorial we'll:

- Define what plugin derivatives are
- Understand the use case for derivatives
- Examine how core uses derivatives in order to demonstrate how you could write your own plugin deriver class

## Goal

Understand what plugin derivatives are, the problem they solve, and how to implement a plugin deriver in your own module.

## Prerequisites

- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins)
- [Drupal Plugin Types](https://drupalize.me/tutorial/drupal-plugin-types)
- [Define a Plugin Type](https://drupalize.me/tutorial/define-new-plugin-type)
- [Dependency Injection](https://drupalize.me/topic/dependency-injection)
- [Preparing for Drupal 8: PSR-4 Autoloading](https://drupalize.me/blog/201408/preparing-drupal-8-psr-4-autoloading)
- Plugin derivatives are part of the plugin discovery mechanics so [understanding how discovery works](https://drupalize.me/tutorial/plugin-discovery) is important.

Sprout Video

## What are derivative plugins?

The concept of derivatives is easiest to explain with an example. Drupal allows an administrator to create any number of menus through the UI. Since this is user-generated configuration, Drupal can't hard code a known list of all menus that a particular site might contain. Drupal also provides a block for every defined menu that can be placed via the block UI. Blocks are plugins.

If the list of possible menus is variable and we need a block for each, that means we need a way to define in code with an attribute an instance of a block plugin so that the block plugin manager can find it. Furthermore, that block plugin needs to be able to create derivative instances of itself: 1 for each configured menu. This system allows for a variable number of plugins of a given type based on application state or configuration.

This is made possible via the `\Drupal\Component\Plugin\Discovery\DerivativeDiscoveryDecorator` class which uses the [decorator design pattern](https://en.wikipedia.org/wiki/Decorator_pattern).

[New plugin types](https://drupalize.me/tutorial/define-new-plugin-type) that are based on the `DefaultPluginManager` allow for derivatives by default. And there's not really any reason to turn it off.

For a more complete example of using the `DerivativeDiscoveryDecorator`, let's take a look at how the core system module provides an individual block for each configured menu with the `\Drupal\system\Plugin\Block\SystemMenuBlock` plugin, and the `Drupal\system\Plugin\Derivative\SystemMenuBlock` deriver.

## Should I use derivatives?

**Yes:** If your module requires that you create a variable number of plugins based on some non hard-coded data then you need to use derivatives.

**No:** If there is only a single instance of the plugin, and the plugin's metadata can be hard coded, then you do not need to use derivatives.

## How derivatives work

Derivatives work by creating a base plugin definition and a deriver class. The deriver uses the base plugin as a template to dynamically register variations of the base plugin with the plugin manager.

The attribute from `SystemMenuBlock` shows the use of a deriver class. Every plugin manager using derivative discovery supports the use of a `deriver` key in the attribute that points to a deriver class which is an implementation of `\Drupal\Component\Plugin\Derivative\DeriverInterface` or `\Drupal\Core\Plugin\Discovery\ContainerDeriverInterface`, if you want to use dependency injection in your deriver. This class is responsible for doing the work of figuring out what menus have been configured by an administrator, and telling the plugin system about them.

```
/**
 * Provides a generic Menu block.
 */
#[Block(
  id: "system_menu_block",
  admin_label: new TranslatableMarkup("Menu"),
  category: new TranslatableMarkup("Menus"),
  deriver: SystemMenuBlockDeriver::class,
  forms: [
    'settings_tray' => SystemMenuOffCanvasForm::class,
  ]
)]
class SystemMenuBlock extends BlockBase implements ContainerFactoryPluginInterface {
```

During the plugin discovery process the `deriver` key in the attribute is noticed, and the `Drupal\system\Plugin\Derivative\SystemMenuBlock::getDerivativeDefinitions()` method from the deriver class is called. This dynamically generates a list of menu blocks. The metadata for each is different, i.e., what would normally appear in the attribute is dynamically derived. The plugin system treats each derivative as a unique plugin for all intents and purposes. When instantiated the same `\Drupal\system\Plugin\Block\SystemMenuBlock` class is used for each, but uses the derived metadata to look up and output a different menu depending on which menu block is being requested.

Here's the code from `Drupal\system\Plugin\Derivative\SystemMenuBlock::getDerivativeDefinitions()` to better illustrate this concept:

```
  /**
   * {@inheritdoc}
   */
  public function getDerivativeDefinitions($base_plugin_definition) {
    foreach ($this->menuStorage->loadMultiple() as $menu => $entity) {
      $this->derivatives[$menu] = $base_plugin_definition;
      $this->derivatives[$menu]['admin_label'] = $entity->label();
      $this->derivatives[$menu]['config_dependencies']['config'] = array($entity->getConfigDependencyName());
    }
    return $this->derivatives;
  }
```

This code uses `$this->menuStorage->loadMultiple()` to load every defined menu entity. It then loops through the results and adds to the `$this->derivatives` list of menus. It starts by copying the `$base_plugin_definition`, which is the attribute from `\Drupal\system\Plugin\Block\SystemMenuBlock` shown above. And then alters the `admin_label` and `config_dependencies` keys (from the attribute) for this specific menu.

Then, the list of derivative plugins is returned to the plugin manager, which treats each entry in the list as an individual plugin instance. When a specific instance is required, the plugin is loaded by its unique ID. The dynamically-generated configuration is passed into the plugin instance which can then use that configuration to tailor its functionality accordingly.

## Recap

In this tutorial we:

- Defined plugin derivatives as a mechanism for dynamically generating a list of plugin instances
- Looked at how the menu system uses derivatives to allow for the creation of one unique block plugin for each configured menu entity

## Further your understanding

- In [Define a Plugin Type](https://drupalize.me/tutorial/define-new-plugin-type) we defined a new sandwich plugin type. Can you write a sandwich plugin, and corresponding deriver, that uses a base plugin definition and a deriver to generate a list of sandwich plugins based on a list of seasonal ingredients?

## Additional resources

- [This tutorial](https://www.sitepoint.com/tutorial-on-using-drupal-8-plugin-derivatives-effectively/) (sitepoint.com) contains an example of dynamically generating block plugins based on the existing nodes, and [this tutorial](https://www.webomelette.com/dynamic-menu-links-drupal-8-plugin-derivatives) (webomelette.com) demonstrates dynamically generating menu links and items, both of which use plugin derivatives.
- [Plugin Derivatives](https://www.drupal.org/docs/drupal-apis/plugin-api/plugin-derivatives) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Plugin Factories and Mappers](/tutorial/plugin-factories-and-mappers?p=2765)

Clear History

Ask Drupalize.Me AI

close