---
title: "Implement a YAML Plugin"
url: "https://drupalize.me/tutorial/implement-yaml-plugin?p=2765"
guide: "[[alter-drupal-modules]]"
order: 12
---

# Implement a YAML Plugin

## Content

Many of Drupal's APIs that look like a bunch of configuration in a YAML file (migrations, menu links, etc.) are actually plugins in disguise. The YAML from these files is used as arguments to a generic PHP plugin class which then behaves differently depending on the provided values. As a developer, you probably don't need to know that menu links are plugins, but it can be helpful when debugging or just trying to get a better understanding of the big picture.

In this tutorial, we'll:

- Learn about how YAML-based plugins work
- Discuss how to find the implementation details for YAML-based plugins
- Walk through an example of implementing a YAML-based plugin

By the end of this tutorial, you should be able to recognize a YAML-based plugin definition, and author your own.

## Goal

Learn why YAML-based plugins are used and what you need to know to create YAML-based plugins.

## Prerequisites

- [What Are Plugins](https://drupalize.me/tutorial/what-are-plugins)
- [Plugin Discovery](https://drupalize.me/tutorial/plugin-discovery)

## Why YAML-based plugins?

There are a lot of cases where it is beneficial to be able to leverage Drupal's plugin API behind the scenes but unnecessary, or even overly complicated, to ask developers to create a custom PHP class. YAML plugins work great for instances where the static metadata about a plugin (like what would normally be collected in a PHP attribute), when fed into a generic PHP class is enough for that class to be able to provide multiple different functionalities.

A menu link is a great example. The plugin manager can read the YAML metadata for a dozen different links. And then initialize multiple instances of a single PHP class that uses the label, route, and parent menu metadata to change its behavior.

This is similar to how [plugin derivatives](https://drupalize.me/tutorial/plugin-derivatives) work, but instead of dynamically calculating the metadata it can be hard-coded into the module and committed to version control.

## Creating YAML-based plugins

YAML-based plugins typically do not involve writing PHP code. An example is [a custom migration plugin](https://drupalize.me/tutorial/write-custom-migration), or a menu link plugin. You write some YAML that provides configuration to the plugin manager, which it can then use to instantiate instances of a generic PHP class that can do all the necessary work based on configuration alone.

In our experience, you'll often write the YAML required to add a menu link, or a breakpoint, without having to know (or care) that you're actually implementing a plugin.

When you do need to dive in, start by looking for the use of `\Drupal\Core\Plugin\Discovery\YamlDiscovery`, or `YamlDirectoryDiscovery()` in either the `__construct()` or `getDiscovery()` methods of the plugin manager.

Example from `\Drupal\Core\Menu\MenuLinkManager::getDiscovery()`:

```
  protected function getDiscovery() {
    if (!isset($this->discovery)) {
      $yaml_discovery = new YamlDiscovery('links.menu', $this->moduleHandler->getModuleDirectories());
      $yaml_discovery->addTranslatableProperty('title', 'title_context');
      $yaml_discovery->addTranslatableProperty('description', 'description_context');
      $this->discovery = new ContainerDerivativeDiscoveryDecorator($yaml_discovery);
    }
    return $this->discovery;
  }
```

The first 2 arguments to `YamlDiscovery()` tell us what we need to get started. Menu link plugins are defined in YAML files named *MODULENAME.links.menu.yml* (see the first argument `'links.menu'`), located in the root directory of any enabled module.

This tells me that I'm implementing the **Menu link** plugin type, which uses **YAML** for discovery. My plugin should be placed in the file *MODULENAME.links.menu.yml*.

Use this information to find existing implementations of the plugin type that you can copy/paste from. For example, *core/modules/system/system.links.menu.yml*, in this case.

Another good example is `\Drupal\migrate\Plugin\MigrationPluginManager::getDiscovery()`. This demonstrates using `YamlDirectoryDiscovery()` to find all appropriately named *.yml* files in a defined directory.

Knowing what should live in the YAML file is a bit harder. It depends on being able to either find existing documentation, or looking at how other modules have implemented plugins of the same type.

For practical examples of implementing YAML plugins see these tutorials:

- [Define Custom Layouts in a Module or Theme](https://drupalize.me/tutorial/define-custom-layouts-module-or-theme)
- [Write a Custom Migration](https://drupalize.me/tutorial/write-custom-migration)
- [What Is a Breakpoint YAML File?](https://drupalize.me/tutorial/what-breakpoint-yaml-file)

## Recap

In this tutorial, we learned about the use case for YAML-based plugins, how to obtain detailed information about a specific YAML-based plugin type, and how to implement a YAML-based plugin in your module.

## Further your understanding

- Look for *.yml* files in Drupal core modules. Can you identify which ones are implementing YAML-based plugins?
- Come up with an example of a scenario where it would make sense to use YAML-based plugin discovery for a new custom plugin type.

## Additional resources

- [Implement a Plugin Using PHP Attributes](https://drupalize.me/tutorial/implement-plugin-using-php-attributes)
- [Implement a Plugin Using Annotations](https://drupalize.me/tutorial/implement-plugin-using-annotations)
- [Plugins (Plugin API)](https://drupalize.me/topic/plugins-plugin-api) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Implement a Plugin Using Annotations](/tutorial/implement-plugin-using-annotations?p=2765)

Next
[Plugin Managers](/tutorial/plugin-managers?p=2765)

Clear History

Ask Drupalize.Me AI

close