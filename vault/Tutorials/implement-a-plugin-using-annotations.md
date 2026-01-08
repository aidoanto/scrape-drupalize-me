---
title: "Implement a Plugin Using Annotations"
url: "https://drupalize.me/tutorial/implement-plugin-using-annotations?p=2765"
guide: "[[alter-drupal-modules]]"
---

# Implement a Plugin Using Annotations

## Content

Prior to Drupal 10.2 most plugin implementations required the use of annotations alongside a PHP class. Now Drupal supports and recommends the use of [PHP attributes](https://drupalize.me/tutorial/php-attributes) instead. During the transition, most developers will still need to know how to recognize and implement annotation-based plugins.

In this tutorial we'll:

- Provide a recipe for implementing annotation-based plugins.
- Demonstrate how to figure out where the code and metadata should live for annotation-based plugins.

By the end of this tutorial you should have a recipe for getting started with implementing annotation-based plugins, and a better understanding of how to figure out the details required to implement a given plugin type.

## Goal

Learn a recipe for, and walk through the process of, implementing plugins that are based on annotations.

## Prerequisites

- [What Are Plugins](https://drupalize.me/tutorial/what-are-plugins)
- [Annotations](https://drupalize.me/tutorial/annotations)

The Plugin API builds on a number of other Drupal APIs and PHP design patterns. Understanding how these work will make it easier to implement custom plugins, and to recognize which parts of the implementation are specific to the Plugin API.

- PHP [class inheritance](https://drupalize.me/videos/introduction-inheritance-php?p=2379) and [interfaces](https://drupalize.me/videos/introduction-interfaces?p=2379) are used extensively in the Plugin API.
- Implementing plugins requires that you understand [the PSR-4 standard and how it's used in Drupal](https://drupalize.me/blog/201408/preparing-drupal-8-psr-4-autoloading).
- Most plugin implementations use [dependency injection](https://drupalize.me/topic/dependency-injection) to make use of [services](https://drupalize.me/topic/services). Specifically, Drupal plugins use the [factory injection pattern](https://www.lullabot.com/articles/injecting-services-in-your-d8-plugins).

It can also be helpful, but not required, to understand:

- How to [Discover Existing Plugin Types](https://drupalize.me/%28/tutorial/discover-existing-plugin-types%29),
- How [Plugin Discovery](https://drupalize.me/tutorial/plugin-discovery) works.

## Use PHP attributes instead

As of Drupal 10.2, in most cases, you'll want to use PHP attributes-based plugins instead of annotation-based plugins. If you know you want PHP attributes, skip to [Implement a Plugin Using PHP Attributes](https://drupalize.me/tutorial/implement-plugin-using-php-attributes).

Drupal is standardizing on the use of PHP attributes in place of Doctrine annotations. And is currently in the middle of that transition. For the time being, Drupal core provides a backwards compatibility layer that allows plugin managers that have update to attributes to continue to support annotations. As a developer, this means your code using annotations will continue to work.

To future-proof your code you should use, or update to, PHP attributes unless:

- You need to support Drupal 10.1 or earlier.
- You are defining a new custom *entity type*, which still only supports annotations.
- The plugin type you're implementing hasn't been updated to support attributes yet.

How do I know if the plugin type I want to implement has been updated to support the use of PHP attributes? Find an existing instance, preferably provided by the same project (e.g. Drupal core or a contributed module) that defines the plugin type, and see which approach it is using, and copy that.

Still need to use annotations? Keep reading!

## Video

Sprout Video

## Implement a plugin using annotations

Here's what you'll need to know to get started with annotation-based plugins:

1. What is the plugin type I need to implement? You can get a list of all available plugin types using one of the techniques defined in [Discover Existing Plugin Types](https://drupalize.me/tutorial/discover-existing-plugin-types).
2. What is the annotation I need to provide?
3. What is the PSR-4 subdirectory for the plugin type?
4. What PHP interface should I implement, and is there a base class I can extend?

In most cases the easiest way to figure this out is by looking at an existing implementation of the plugin type and copying what it does.

For example, if I wanted to implement a field formatter plugin I might out check out this example from the `TelephoneLinkFormatter` plugin provided by the *telephone* module in Drupal core, file *core/modules/telephone/src/Plugin/Field/FieldFormatter/TelephoneLinkFormatter.php*:

```
<?php

namespace Drupal\telephone\Plugin\Field\FieldFormatter;

use Drupal\Core\Field\FormatterBase;
use Drupal\Core\Field\FieldItemListInterface;
use Drupal\Core\Form\FormStateInterface;
use Drupal\Core\Url;

/**
 * Plugin implementation of the 'telephone_link' formatter.
 *
 * @FieldFormatter(
 *   id = "telephone_link",
 *   label = @Translation("Telephone link"),
 *   field_types = {
 *     "telephone"
 *   }
 * )
 */
class TelephoneLinkFormatter extends FormatterBase {}
```

Looking at the top few lines of the file, we can figure out all the pieces we need.

### What is the plugin type?

From this line in the comment `@FieldFormatter` we know the plugin type is **FieldFormatter**, and the annotation class (derived by removing the `@`) is `\Drupal\Core\Field\Annotation\FieldFormatter`. This tells us what we can enter into our custom plugin's annotation. Start by copy/pasting the example you found.

### What is the plugin's namespace?

The namespace is `namespace Drupal\telephone\Plugin\Field\FieldFormatter;`. If you remove `Drupal\MODULENAME` (e.g. `Drupal\telephone`) you get the PSR-4 subdirectory `Plugin\Field\FieldFormatter`. So your custom code will live in the *src/Plugin/Field/FieldFormatter/{CLASS\_NAME}.php* file, and you can copy/paste this namespace and replace `telephone` with the machine name of your module.

### Is there a base class or interface?

There's base class we can extend, `Drupal\Core\Field\FormatterBase`, and that base class implements `\Drupal\Core\Field\FormatterInterface` which is the interface for the plugin type that we need to adhere to.

### What did we discover about implementing this plugin type?

To summarize, the plugin type is `FieldFormatter`, they are annotated with `@FieldFormatter` annotations, the code needs to live in the `_src/Plugin/Field/FieldFormatter/` directory, and the interface to implement is `FormatterInterface`. With that info you can write a new `FieldFormatter` plugin.

Here's an example of a complete new `FieldFormatter` plugin written using this info, *src/Plugin/Field/FieldFormatter/LolSpeak.php*:

```
<?php

namespace Drupal\lolspeak\Plugin\Field\FieldFormatter;

use Drupal\Core\Field\FormatterBase;
use Drupal\Core\Field\FieldItemListInterface;

/**
 * Formatter plugin that returns 'lol' instead of the field text.
 *
 * @FieldFormatter(
 *   id = "lol_speak",
 *   label = @Translation("Lol Speak formatter"),
 *   field_types = {
 *     "string",
 *     "text",
 *     "text_long",
 *   }
 * )
 */
class LolSpeakFormatter extends FormatterBase {

/**
   * {@inheritdoc}
   */
  public function viewElements(FieldItemListInterface $items, $langcode) {
    $element = [];
    foreach ($items as $delta => $item) {
      $element[$delta] = [
        '#type' => 'markup',
        '#markup' => $this->t('lol!'),
      ];
    }
    return $element;
  }

}
```

In many cases that might be enough to get you on your way to implementing the plugin. But if you're stuck, or need more info about the specific plugin type, keep reading.

## How do I know what methods to implement on my plugin class?

The best way to know what methods to implement and what they should do is to look at the interface that the plugin class is implementing, `\Drupal\Core\Field\FormatterInterface` in this case. Reading the documentation for each method on the interface should give you a good idea of what you *could* implement in your plugin. But you often don't need to implement them all if you're extending a base class. In the example above, we only override one of the many different methods of `FormatterInterface`, because it's all we needed.

It can be helpful to take a look at the code in the base class that you're extending. And to override its methods to customize the features.

Look for existing implementations of the plugin type for inspiration (don't forget to look at contributed modules, too). And, because plugins are based on classes, if there's an existing implementation that does most of what you need, you can extend that class instead of the base class and override just the parts that you want to change.

## What goes in the annotation?

Usually after copying and pasting an existing example of the plugin type my first question is "What is supposed to be in this annotation?". In the example above, `label` is pretty clear, as is `id`, but `field_types` is obviously an array of *something*, I wonder what else could go in that array?

Annotations, and their corresponding key value pairs, are documented in Drupal by providing an empty class in the `Drupal\{module}\Annotation` namespace which implements `\Drupal\Component\Annotation\AnnotationInterface`, and adding a *@docblock* that contains the `@Annotation` annotation. That class name also corresponds to the annotation itself. In the case of `@FieldFormatter`, if you remove the `@`, you can find the class by searching for `FieldFormatter` in the `\Annotation` namespace. From there you'll find the following documentation that lets you know the `field_types` keys in the annotation is an array of field types. And *field types* are the ids of the `@FieldType` plugins.

```
/**
 * An array of field types the formatter supports.
 *
 * @var array
 */
public $field_types = [];
```

## What if I can't find an existing implementation to copy?

If you can't find an existing implementation of the plugin type to gather this information from, you can look at the code in the plugin manager. Once you know the plugin type, you should also be able to figure out which plugin manager class is responsible for the plugin type. In the vast majority of cases the plugin manager class will be an extension of the `\Drupal\Core\Plugin\DefaultPluginManager`. Take a look at the `__construct()` method of the plugin manager in question. This is where the PSR-4 subdirectory, annotation, and interface, for a plugin type are set.

For example, here's code from the plugin type manager for field formatters defined in `\Drupal\Core\Field\FormatterPluginManager`:

```
class FormatterPluginManager extends DefaultPluginManager {

  public function __construct(\Traversable $namespaces, CacheBackendInterface $cache_backend, ModuleHandlerInterface $module_handler, FieldTypePluginManagerInterface $field_type_manager) {
    parent::__construct('Plugin/Field/FieldFormatter', $namespaces, $module_handler, 'Drupal\Core\Field\FormatterInterface', FieldFormatter::class, 'Drupal\Core\Field\Annotation\FieldFormatter');

    $this->setCacheBackend($cache_backend, 'field_formatter_types_plugins');
    $this->alterInfo('field_formatter_info');
    $this->fieldTypeManager = $field_type_manager;
  }

}
```

Looking at the code in the `__construct()` method of the plugin manager, you should be able to identify the key components necessary to answer the questions above. The `DefaultPluginManager` uses *php attribute class discovery*, which also has a fallback to *annotated class discovery*, so that means formatter plugins will use PHP attributes by default, but can also be annotated PHP classes. This is by far the most likely discovery method you'll encounter. But also check the rest of the plugin manager class for an implementation of the `getDiscovery()` method which is used to switch to something like YAML discovery.

Take a look at this line:

```
parent::__construct('Plugin/Field/FieldFormatter', $namespaces, $module_handler, 'Drupal\Core\Field\FormatterInterface', FieldFormatter::class, 'Drupal\Core\Field\Annotation\FieldFormatter');
```

It tells us a bunch of useful information:

- The first argument `'Plugin/Field/FieldFormatter'` is which subdirectory of a module's *src/* directory to look in, which also gives us the PSR-4 namespace, `Drupal\MODULENAME/Plugin/Field/FieldFormatter`. Put that together, and you'll know formatter plugins should live in *MODULENAME/src/Plugin/Field/FieldFormatter/LolSpeakFormatter.php*.
- The 4th argument, `'Drupal\Core\Field\FormatterInterface'` tells you which interface the plugin needs to implement.
- The 5th argument, `FieldFormatter::class` tells you which PHP attribute class is used,
- The 6th argument, `'Drupal\Core\Field\Annotation\FieldFormatter'` tells you which annotation to use.
- The base class (when it exists) can usually be found somewhere in the *MODULENAME/src/* directory of the module providing the plugin manager.

Once you've gathered that information you should be ready to start defining a new instance of this plugin type by creating a new PHP class in the appropriate PSR-4 namespace and implementing the necessary interface.

- If there's an existing base class for the plugin type **you should extend it**.
- If you need to use an existing service in your plugin code, you should use dependency injection, and make your class implement the `ContainerFactoryPluginInterface` interface. This requires defining a `__construct()` and `create()` method on your class. The plugin manager will be smart about using the `create()` method to instantiate your plugin if it can.
- Look at existing implementations of the given plugin type for guidance.

## Recap

Being able to implement a plugin using annotations requires being able to answer the following questions:

- What plugin manager is being used?
- Where should I put code and metadata?
- What functionality is the plugin expected to provide?

The quickest way to figure it out is look for an existing implementation and copy that. If that doesn't work, the answers to the second 2 questions can always be figured out by looking at the code in the plugin manager.

## Further your understanding

- Can you answer the questions above for block plugins? What about for field formatter plugins?
- Dig into how [plugin discovery](https://drupalize.me/tutorial/plugin-discovery) works. It can make it easier to understand how to implement plugins.

## Additional resources

- [DrupalCon Los Angeles 2015: An Overview of the Drupal 8 Plugin System](https://www.youtube.com/watch?v=gd6s4wC_bP4) (YouTube.com)
- [Drupal’s Plugin API – an introduction through examples](https://manifesto.co.uk/drupal-plugin-api-examples-tutorial/) (manifest.co.uk)
- [Plugins (Plugin API)](https://drupalize.me/topic/plugins-plugin-api) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Implement a Plugin Using PHP Attributes](/tutorial/implement-plugin-using-php-attributes?p=2765)

Next
[Implement a YAML Plugin](/tutorial/implement-yaml-plugin?p=2765)

Clear History

Ask Drupalize.Me AI

close