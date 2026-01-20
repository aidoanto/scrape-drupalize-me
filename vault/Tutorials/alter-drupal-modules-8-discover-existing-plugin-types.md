---
title: "Discover Existing Plugin Types"
url: "https://drupalize.me/tutorial/discover-existing-plugin-types?p=2765"
guide: "[[alter-drupal-modules]]"
order: 8
---

# Discover Existing Plugin Types

## Content

Knowing which plugin types exist and the use case for each is important when it comes to writing modules that extend Drupal's existing functionality. If you want to add additional functionality, you need to first know which plugin type provides that functionality.

In this tutorial, we'll list some of the more commonly-used plugin types and their use case, show where you can find a more complete list of plugin types provided by core, and provide several methods for discovering existing plugins in your Drupal codebase.

## Goal

Understand the various techniques for figuring out what plugin types exist for a given application so that you can know what options you have available to implement.

## Prerequisites

- You'll need to know what [plugin types](https://drupalize.me/tutorial/drupal-plugin-types) are
- Understanding how [plugin managers](https://drupalize.me/tutorial/plugin-managers) work is useful, but not required

Find plugin types:

- [Using Drush](#using-drush)
- [Based on PHP attributes](#based-on-attributes)
- [Based on annotations](#based-on-annotations)
- [Based on plugin managers](#look-for-plugin-manager-services)

## Using Drush

While there isn't a specific Drush command that provides a list of plugins in a Drupal site, you can get close using:

```
drush ev 'foreach (\Drupal::getContainer()->getServiceIds() as $id) { $a[$id] = is_object(\Drupal::service($id)) ? get_class(\Drupal::service($id)) : ""; } dump($a);' | grep plugin
```

Using `drush ev`, you can pass in PHP code for Drush to evaluate/run (`ev`), the output of which is piped (`|`) to [grep](https://drupalize.me/videos/using-grep-command?p=1149) which looks for services in the container that have the word `plugin` in their name. This gives you a list of services in the service container that are plugins.

Once you know the ID of the plugin manager service that defines a plugin type, you can use Drush to find all instances of that plugin type in your site using a command like the following. Substitute `plugin.manager.field.formatter` for the ID of the appropriate plugin manager service:

```
drush ev "dump(\Drupal::service('plugin.manager.field.formatter')->getDefinitions())"
```

## Based on PHP attributes

Almost all plugin types use PHP attributes for class discovery. As such, you can look at the list of classes in the `Drupal\**\Attribute` namespace; and get a pretty good idea of available plugin types.

View the list of attribute classes on <api.drupal.org> by going to this search page <https://api.drupal.org/api/drupal/classes/> and filtering the list to only classes with Attribute in the namespace.

Learn more about [how PHP Attributes work](https://drupalize.me/tutorial/php-attributes).

## Based on annotations

Prior to the introduction of PHP attributes for plugins in Drupal 10.3/11.0 most plugins used annotated class discovery. And at this time some still do.

Annotations in Drupal are currently only used for the plugin system. As such, you can look at the list of annotation classes and get a pretty good idea of available plugin types.

View the [list of annotation classes on api.drupal.org](https://api.drupal.org/api/drupal/core%21core.api.php/group/annotation).

**Note:** For backwards compatibility annotations are still support so plugin types will often have both an attributes class and an annotation class. If attributes are supported you should use that approach instead.

Learn more about [how annotations work](https://drupalize.me/tutorial/annotations).

There are a handful of plugin types that use YAML discovery. The best way I know of to discover which those are right now is to search for all usages of `\Drupal\Core\Plugin\Discovery\YamlDiscovery` in your code base. This should help you discover the plugin manager class, and its associated plugin type.

## Look for plugin manager services

You can use the [list of services here](https://api.drupal.org/api/drupal/services) and search for any prefixed with `plugin.manager.`. This isn't foolproof because there is no requirement that a plugin manager is named with this prefix, but it is a best practice. That should point you to the plugin manager class, and thereby the plugin type.

## Recap

You can get a list of all plugin types available for your application by using Drush, or by digging into the code. Both methods require at least a high-level understanding of [how plugin types are defined](https://drupalize.me/tutorial/define-new-plugin-type).

## Further your understanding

- Can you get a list of all the plugin types available for your Drupal application?
- Once you know the plugin type that you want to implement, learn how to [Implement Any Plugin Type](https://drupalize.me/tutorial/implement-plugin-any-type).

## Additional resources

- [Using the grep command](https://drupalize.me/videos/using-grep-command?p=1149) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Define a New Plugin Type](/tutorial/define-new-plugin-type?p=2765)

Next
[Implement a Plugin of Any Type](/tutorial/implement-plugin-any-type?p=2765)

Clear History

Ask Drupalize.Me AI

close