---
title: "Implement a Plugin Using PHP Attributes"
url: "https://drupalize.me/tutorial/implement-plugin-using-php-attributes?p=2765"
guide: "[[alter-drupal-modules]]"
order: 10
---

# Implement a Plugin Using PHP Attributes

## Content

As of Drupal 10.2, most plugin types use [PHP attributes](https://drupalize.me/tutorial/php-attributes) for discovery and metadata.

In this tutorial, we'll:

- Provide a recipe for implementing PHP attribute-based plugins.
- Demonstrate how to figure out where the code and metadata should live for PHP attribute-based plugins.

By the end of this tutorial you should have a recipe for getting started with implementing PHP attribute-based plugins, and a better understanding of how to figure out the details required to implement a given plugin type.

## Goal

Learn a recipe and a process for implementing plugins that are based on PHP attributes.

## Prerequisites

- [What Are Plugins](https://drupalize.me/tutorial/what-are-plugins)
- [PHP Attributes](https://drupalize.me/tutorial/php-attributes)

Drupal's Plugin API builds on a number of other Drupal APIs and PHP design patterns. Understanding how these work will make it easier to implement custom plugins, and to recognize which parts of the implementation are specific to the Plugin API.

- [Object-Oriented PHP](https://drupalize.me/topic/object-oriented-php)
- PHP *class inheritance* and *interfaces* are used extensively in the Plugin API.
- Implementing plugins requires that you understand [the PSR-4 standard and how it's used in Drupal](https://drupalize.me/blog/201408/preparing-drupal-8-psr-4-autoloading).
- Most plugin implementations use [dependency injection](https://drupalize.me/topic/dependency-injection) to make use of [services](https://drupalize.me/topic/services). Specifically, they use the [factory injection pattern](https://www.lullabot.com/articles/injecting-services-in-your-d8-plugins).

It can also be helpful, but not required, to understand:

- How to [Discover Existing Plugin Types](https://drupalize.me/tutorial/discover-existing-plugin-types),
- How [Plugin Discovery](https://drupalize.me/tutorial/plugin-discovery) works.

## Many plugins still require annotations

Prior to Drupal 10.2, most plugin implementations required the use of annotations alongside a PHP class. Now Drupal supports and recommends the use of PHP attributes instead. But during the transition, most developers will still need to know how to recognize and implement annotation-based plugins.

**Important:** The plugin manager (for the plugin type you're trying to implement) needs to have been updated to support PHP attributes. Most Drupal core plugin types have been updated with **custom entity types as the notable exception**.

How do I know if the plugin type I want to implement has been updated to support the use of PHP attributes? Find an existing instance, preferably provided by the same project (e.g. Drupal core or a contributed module) that defines the plugin type, see which approach it is using, and copy that.

Need to use annotations? See [Implement a Plugin Using Annotations](https://drupalize.me/tutorial/implement-plugin-using-annotations).

## Implement a plugin using PHP attributes

Here's what you'll need to know to get started with attribute-based plugins:

1. What is the plugin type I need to implement? You can get a list of all available plugin types using one of the techniques defined in [Discover Existing Plugin Types](https://drupalize.me/tutorial/discover-existing-plugin-types).
2. What is the PHP attribute I need to provide?
3. What is the PSR-4 subdirectory for the plugin type?
4. What PHP interface should I implement, and is there a base class I can extend?

In most cases, the easiest way to figure this out is by looking at an existing implementation of the plugin type and copy what it does.

For example, if I wanted to implement a field formatter plugin, I might out check out this example from the `TelephoneLinkFormatter` plugin provided by the *telephone* module in Drupal core in the file *core/modules/telephone/src/Plugin/Field/FieldFormatter/TelephoneLinkFormatter.php*:

```
namespace Drupal\telephone\Plugin\Field\FieldFormatter;

use Drupal\Core\Field\Attribute\FieldFormatter;
use Drupal\Core\Field\FormatterBase;
use Drupal\Core\StringTranslation\TranslatableMarkup;

/**
 * Plugin implementation of the 'telephone_link' formatter.
 */
#[FieldFormatter(
  id: 'telephone_link',
  label: new TranslatableMarkup('Telephone link'),
  field_types: [
    'telephone',
  ],
)]
class TelephoneLinkFormatter extends FormatterBase {
```

Looking at the top few lines of the file, we can figure out all the pieces we need.

### What is the plugin type?

From this line, `#[FieldFormatter(`, we know the plugin type is **FieldFormatter**, and the attribute class (derived by removing the `#[`, or looking at the `use` statement) is `\Drupal\Core\Field\Attribute\FieldFormatter`. We'll use this to figure out what we can enter as metadata for our custom plugin. Start by copy/pasting the example you found.

### What is the plugin's namespace?

The namespace is `namespace Drupal\telephone\Plugin\Field\FieldFormatter;`. If you remove `Drupal\MODULENAME` (e.g. `Drupal\telephone`) you get the PSR-4 subdirectory `Plugin\Field\FieldFormatter`. So, your custom code will live in the *src/Plugin/Field/FieldFormatter/{CLASS\_NAME}.php* file, and you can copy/paste this namespace, and replace `telephone` with the machine name of your module.

### Is there a base class or interface?

There's base class we can extend, `Drupal\Core\Field\FormatterBase`. That base class implements `\Drupal\Core\Field\FormatterInterface` which is the interface for the plugin type that we need to adhere to.

### What did we discover about implementing this plugin type?

To summarize, the plugin type is `FieldFormatter`, metadata is provided via an `FieldFormatter` attribute, the code needs to live in the `_src/Plugin/Field/FieldFormatter/` directory, and the interface to implement is `FormatterInterface`. With that info you can write a new `FieldFormatter` plugin.

### Plugin implementation example code

Here's an example of a complete new `FieldFormatter` plugin written using this info, *src/Plugin/Field/FieldFormatter/LolSpeak.php*:

```
<?php

namespace Drupal\lolspeak\Plugin\Field\FieldFormatter;

use Drupal\Core\Field\FormatterBase;
use Drupal\Core\Field\FieldItemListInterface;

/**
 * Formatter plugin that returns 'lol' instead of the field text.
 */
#[FieldFormatter(
  id: 'lol_speak',
  label: new TranslatableMarkup('Lol Speak formatter'),
  field_types: [
    'telephone',
  ],
)]
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

The best way to know what methods to implement, and what they should do, is to look at the *interface* that the plugin class is implementing, `\Drupal\Core\Field\FormatterInterface`, in this case. Read the documentation for each method on the interface. This should give you a good idea of what you *could* implement in your plugin. If you're extending a base class, often you won't need to implement all the methods. In the example above, we only override one of the many different methods of `FormatterInterface`, because it's all we needed.

It can be helpful to take a look at the code in the base class that you're extending. And to override its methods to customize the features.

Look for existing implementations of the plugin type for inspiration. (Don't forget to look at contributed modules, too). And, because plugins are based on classes, if there's an existing implementation that does most of what you need, you can extend that class instead of the base class, and override just the parts that you want to change.

## What goes in the metadata attribute?

Usually after copying and pasting an existing example of the plugin type, my first question is "What's supposed to be in this attribute?". In the example above, `label` is pretty clear, as is `id`, but `field_types` is obviously an array of *something*. I wonder what else could go in that array?

## Where are PHP attribute arguments documented?

PHP attributes, and their corresponding arguments, are documented by a class in the `Drupal\{module}\Attribute` namespace. You should be able to track this down from the `use` statement in your plugin file. From there, look at the class constructor (`__construct()`) for detailed documentation. For example, we can see that the `field_types` argument is documented as "an array of field types". There is an assumption here that *field\_types* are the ids of the `FieldType` plugins. We could verify that assumption by looking at example implementations of `FormatterInterface`.

Example from *core/lib/Drupal/Core/Field/Attribute/FieldFormatter.php*:

```
/**
 * Constructs a FieldFormatter attribute.
 *
 * @param string $id
 *   The plugin ID.
 * @param \Drupal\Core\StringTranslation\TranslatableMarkup|null $label
 *   (optional) The human-readable name of the formatter type.
 * @param \Drupal\Core\StringTranslation\TranslatableMarkup|null $description
 *   (optional) A short description of the formatter type.
 * @param string[] $field_types
 *   (optional) An array of field types the formatter supports.
 * @param int|null $weight
 *   (optional) An integer to determine the weight of this formatter.
 *   Weight is relative to other formatters in the Field UI when selecting a
 *   formatter for a given field instance.
 * @param class-string|null $deriver
 *   (optional) The deriver class.
 */
public function __construct(
  public readonly string $id,
  public readonly ?TranslatableMarkup $label = NULL,
  public readonly ?TranslatableMarkup $description = NULL,
  public readonly array $field_types = [],
  public readonly ?int $weight = NULL,
  public readonly ?string $deriver = NULL,
) {}
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

Looking at the code in the `__construct()` method of the plugin manager, you should be able to identify the key components necessary to answer the questions above. The `DefaultPluginManager` uses *php attribute class discovery*, so that means formatter plugins will be annotated PHP classes. This is by far the most likely discovery method you'll encounter. But also check the rest of the plugin manager class for an implementation of the `getDiscovery()` method which is used to switch to something like YAML discovery.

Take a look at this line:

```
parent::__construct('Plugin/Field/FieldFormatter', $namespaces, $module_handler, 'Drupal\Core\Field\FormatterInterface', FieldFormatter::class, 'Drupal\Core\Field\Annotation\FieldFormatter');
```

It tells us a bunch of useful information:

- The first argument `'Plugin/Field/FieldFormatter'` is which subdirectory of a module's *src/* directory to look in, which also gives us the PSR-4 namespace, `Drupal\MODULENAME/Plugin/Field/FieldFormatter`. Put that together, and you'll know formatter plugins should live in *MODULENAME/src/Plugin/Field/FieldFormatter/LolSpeakFormatter.php*.
- The fourth argument, `'Drupal\Core\Field\FormatterInterface'` tells you which interface the plugin needs to implement.
- The fifth argument, `FieldFormatter::class` tells you which PHP attribute class is used,
- The sixth argument, `'Drupal\Core\Field\Annotation\FieldFormatter'` tells you which annotation to use.
- The base class (when it exists) can usually be found somewhere in the *MODULENAME/src/* directory of the module providing the plugin manager.

Once you've gathered that information you should be ready to start defining a new instance of this plugin type by creating a new PHP class in the appropriate PSR-4 namespace that implements the necessary interface.

- If there's an existing base class for the plugin type, **you should extend it**.
- If you need to use an existing service in your plugin code, you should use dependency injection, and make your class implement the `ContainerFactoryPluginInterface` interface. This requires defining a `__construct()` and `create()` method on your class. The plugin manager will be smart about using the `create()` method to instantiate your plugin if it can.
- Look at existing implementations of the given plugin type for guidance.

## Recap

Being able to implement a plugin using PHP attributes requires being able to answer the following questions:

- What plugin manager is being used?
- Where should I put code and metadata?
- What functionality is the plugin expected to provide?

The quickest way to figure it out is look for an existing implementation and copy that. If that doesn't work, the answers to the second 2 questions can always be figured out by looking at the code in the plugin manager.

## Further your understanding

- Can you answer the questions above for *Block* plugins? What about for *Field formatter* plugins?
- Having a better understanding of how [plugin discovery](https://drupalize.me/tutorial/plugin-discovery) works makes it easier to implement plugins.

## Additional resources

- [Implement a Plugin Using Annotations](https://drupalize.me/tutorial/implement-plugin-using-annotations) (Drupalize.Me)
- [Plugins (Plugin API)](https://drupalize.me/topic/plugins-plugin-api) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Implement a Plugin of Any Type](/tutorial/implement-plugin-any-type?p=2765)

Next
[Implement a Plugin Using Annotations](/tutorial/implement-plugin-using-annotations?p=2765)

Clear History

Ask Drupalize.Me AI

close