---
title: "Define a New Plugin Type"
url: "https://drupalize.me/tutorial/define-new-plugin-type?p=2765"
guide: "[[alter-drupal-modules]]"
order: 7
---

# Define a New Plugin Type

## Content

Knowing how to define a new plugin type will allow you to write modules that are more extensible, and more configurable. In doing so you'll learn more about best practices in decoupling code within your module, and get an in-depth look at how the plugin system works. Even if you're not defining a new plugin type in your own module, understanding how the system works will give you more insight into how many parts of Drupal work. This is essential knowledge for anyone developing modules for Drupal.

By the end of this tutorial you should be able to determine if defining a new plugin type is the right solution to your problem, and then understand the steps involved in doing so.

## Goal

Create a new `Sandwich` plugin type following best practices for defining a plugin manager and related classes and interfaces.

## Prerequisites

- [Overview: Info Files for Drupal Modules](https://drupalize.me/tutorial/overview-info-files-drupal-modules)
- [PHP Attributes](https://drupalize.me/tutorial/php-attributes)
- [Annotations](https://drupalize.me/tutorial/annotations)
- [Drupal Plugin Types](https://drupalize.me/tutorial/drupal-plugin-types)

We assume that you have a custom module directory and info file created already. If you don't, create one in *DRUPALROOT/modules/custom/*. For example, for a module with the machine name, *plugin\_type\_example*, create *DRUPALROOT/modules/custom/plugin\_type\_example*. (The *custom* subdirectory is optional.) Then, create an info file (*plugin\_type\_example.info.yml*) in the root of your new module's directory.

For example: *modules/custom/plugin\_type\_example/plugin\_type\_example.info.yml*

```
name: Plugin Type Example Module
type: module
description: Example module to learn the Plugin API
package: Custom
core_version_requirement: ^10 || ^11
```

## Contents

In this tutorial we'll cover how to:

- [Decide if you should create a new plugin type](#new-plugin-type)
- [Create a plugin manager and define it as a service](#define-plugin-manager)
- [Define an attribute class for collecting and documenting metadata about our plugins](#define-attribute)
- [Define an interface for plugins of the new type to implement](#define-interface)
- [Make your plugin manager a service](#services)
- [Provide an abstract base class as a starting point for anyone implementing our plugin type](#define-base-class)
- [Create two example plugins of the new plugin type](#create-examples)

Some of the example code in this tutorial is based off the *plugin\_type\_example* in the [Examples for Developers project](https://www.drupal.org/project/examples) available to download on Drupal.org.

## Watch: Define a New Plugin Type

Sprout Video

**Note**: The video version of this tutorial demonstrates how to define a plugin type using annotations instead of PHP attributes. It's still relevant, but if you're creating a new plugin type for Drupal 11+ you should use [PHP attributes](https://drupalize.me/tutorial/php-attributes). Also, use Drush to scaffold a plugin type instead of Drupal Console, which is now obsolete. (See instructions in the written tutorial below.)

## Should I define a new plugin type?

You'll want to define a new plugin type in your module if:

- You want users of your module to choose among multiple, configurable features
- You want to allow other developers to provide new functionality compatible with your module without having to modify your module.

As a rule of thumb, anytime you want to provide a list of different choices for accomplishing the same task you should probably be considering plugins.

## Using Drush's plugin code generation tools

You can get a huge head start on this process using [Drush](https://drupalize.me/tutorial/what-drush-0) and its [code generation tools](https://drupalize.me/tutorial/develop-drupal-modules-faster-drush-code-generators), like `generate plugin:TYPE`. Run `drush generate` and look under the `plugin:` group to see all **plugin-scaffolding commands**.

You can create a plugin based on plugin types that already exist in core, e.g. block, field formatter, migrate process, views field plugins. Or, to create your own custom plugin type, use `generate plugin:manager`. You'll be given the option to choose the discovery type: annotation, attribute, YAML, or Hook. If you're already familiar with the plugin system and just want to create a new plugin type based on core or purely custom, this is the most efficient way to do so.

```
drush generate plugin:manager

Welcome to plugin-manager generator!
––––––––––––––––––––––––––––––––––––––

Module machine name:
➤ plugin_type_example

Module name [plugin_type_example]:
➤

Plugin type [sandwich]:
➤

Discovery type [Annotation]:
[1] Annotation
[2] Attribute
[3] YAML
[4] Hook
➤ 2

The following directories and files have been created or updated:
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
• /var/www/html/web/modules/custom/plugin_type_example/plugin_type_example.services.yml
• /var/www/html/web/modules/custom/plugin_type_example/src/SandwichInterface.php
• /var/www/html/web/modules/custom/plugin_type_example/src/SandwichPluginBase.php
• /var/www/html/web/modules/custom/plugin_type_example/src/SandwichPluginManager.php
• /var/www/html/web/modules/custom/plugin_type_example/src/Attribute/Sandwich.php
• /var/www/html/web/modules/custom/plugin_type_example/src/Plugin/Sandwich/Foo.php
```

## Define a plugin manager

A plugin manager describes how plugins of a given type will be located, instantiated, and generally what they’ll do. By creating a new plugin manager you're also creating a new plugin type, which other modules can implement. [Read more about the role a plugin manager fills](https://drupalize.me/tutorial/plugin-managers), and how to use existing plugin managers.

For this example we'll define a new class that extends `\Drupal\Core\Plugin\DefaultPluginManager`. The `DefaultPluginManager` uses `AttributeDiscoveryWithAnnotations` and `ContainerDerivativeDiscoveryDecorator` for discovery, and `ContainerFactory` for plugin instantiation by default. In most cases there is no reason to change this. Read more about [plugin discovery](https://drupalize.me/tutorial/plugin-discovery) and [plugin factories](https://drupalize.me/tutorial/plugin-factories-and-mappers).

If you want to use something different, set the `DefaultPluginManager::$discovery` and `DefaultPluginManager::$factory` properties to use one of the alternate discovery or factory classes instead and then let the `DefaultPluginManager` take care of delegating to those classes.

Example plugin manager definition, *plugin\_type\_example/src/SandwichPluginManager.php*:

```
<?php

namespace Drupal\plugin_type_example;

use Drupal\Core\Cache\CacheBackendInterface;
use Drupal\Core\Extension\ModuleHandlerInterface;
use Drupal\Core\Plugin\DefaultPluginManager;
use Drupal\plugin_type_example\Annotation\Sandwich as SandwichAnnotation;
use Drupal\plugin_type_example\Attribute\Sandwich as SandwichAttribute;

/**
 * A plugin manager for sandwich plugins.
 *
 * The SandwichPluginManager class extends the DefaultPluginManager to provide
 * a way to manage sandwich plugins. A plugin manager defines a new plugin type
 * and how instances of any plugin of that type will be discovered, instantiated
 * and more.
 *
 * Using the DefaultPluginManager as a starting point sets up our sandwich
 * plugin type to use PHP attributes for discovery with a fallback to
 * annotations for backwards compatibility.
 *
 * The plugin manager is also declared as a service in
 * plugin_type_example.services.yml so that it can be easily accessed and used
 * anytime we need to work with sandwich plugins.
 */
class SandwichPluginManager extends DefaultPluginManager {

  /**
   * Creates the discovery object.
   *
   * @param \Traversable $namespaces
   *   An object that implements \Traversable which contains the root paths
   *   keyed by the corresponding namespace to look for plugin implementations.
   * @param \Drupal\Core\Cache\CacheBackendInterface $cache_backend
   *   Cache backend instance to use.
   * @param \Drupal\Core\Extension\ModuleHandlerInterface $module_handler
   *   The module handler to invoke the alter hook with.
   */
  public function __construct(\Traversable $namespaces, CacheBackendInterface $cache_backend, ModuleHandlerInterface $module_handler) {
    // We replace the $subdir parameter with our own value.
    // This tells the plugin manager to look for Sandwich plugins in the
    // 'src/Plugin/Sandwich' subdirectory of any enabled modules. This also
    // serves to define the PSR-4 namespace in which sandwich plugins will live.
    // Modules can put a plugin class in their own namespace such as
    // Drupal\{module_name}\Plugin\Sandwich\MySandwichPlugin.
    $subdir = 'Plugin/Sandwich';

    // The name of the interface that plugins should adhere to. Drupal will
    // enforce this as a requirement. If a plugin does not implement this
    // interface, Drupal will throw an error.
    $plugin_interface = SandwichInterface::class;

    // The name of the attribute class that contains the plugin definition.
    $plugin_definition_attribute_name = SandwichAttribute::class;

    // The name of the annotation class that contains the plugin definition.
    // This is provided for backwards compatibility. If you are defining a new
    // plugin that will only ever need to work with Drupal 11+ than you do not
    // need to provide an annotation class. If you're updating an existing
    // plugin manager that already has an annotation class then you should
    // provide an annotation class here. This will ensure that existing plugin
    // instances that use annotations for discovery will still work.
    $plugin_definition_annotation_name = SandwichAnnotation::class;

    parent::__construct($subdir, $namespaces, $module_handler, $plugin_interface, $plugin_definition_attribute_name, $plugin_definition_annotation_name);

    // This allows the plugin definitions to be altered by an alter hook. The
    // parameter defines the name of the hook, thus: hook_sandwich_info_alter().
    // In this example, we implement this hook to change the plugin definitions:
    // see plugin_type_example_sandwich_info_alter().
    $this->alterInfo('sandwich_info');

    // This sets the caching method for our plugin definitions. Plugin
    // definitions are discovered by examining the $subdir defined above, for
    // any classes with a $plugin_definition_annotation_name. The annotations
    // are read, and then the resulting data is cached using the provided cache
    // backend. The second argument is a cache key prefix. Out of the box Drupal
    // with the default cache backend setup will store our plugin definition in
    // the cache_default table using the sandwich_info key. All that is
    // implementation details, however; all we care about it is that caching for
    // our plugin definition is taken care of by this call.
    $this->setCacheBackend($cache_backend, 'sandwich_info', ['sandwich_info']);
  }

}
```

In summary, this code defines a new `Sandwich` plugin type, instances of which are in the `VENDORNAME\Plugin\Sandwich` namespace. Or more verbosely: `Drupal\MODULENAME\Plugin\Sandwich`. These plugins are all implementations of the `Drupal\plugin_type_example\SandwichInterface`, and they use attributes (with a fallback to annotations) for metadata defined by and documented in `Drupal\plugin_type_example\Attribute\Sandwich`.

Next up, we need to create the 2 classes we just referenced.

## Define your plugin type's attribute class

In our `SandwichPluginManager` class we declared that the class to use for attributes is `Drupal\plugin_type_example\Attribute\Sandwich`, so let's make sure there's some code that defines this class.

The attribute serves two purposes. It allows our plugin type to use a specific `#[Sandwich]` attribute instead of just `#[Plugin]`. And it provides a place for us to document the configuration options that someone might define in an `#[Sandwich]` attribute.

Our attribute class should implement the `\Drupal\Component\Plugin\Attribute\AttributeInterface` and should do so by extending `\Drupal\Component\Plugin\Attribute\Plugin`, which does most of the work for us.

*plugin\_type\_example/src/Attribute/Sandwich.php*:

```
<?php

namespace Drupal\plugin_type_example\Attribute;

use Drupal\Component\Plugin\Attribute\Plugin;
use Drupal\Core\StringTranslation\TranslatableMarkup;

/**
 * Defines a Sandwich attribute class.
 *
 * Provides an example of how to define a new attribute type for use in
 * defining a plugin type. Demonstrates documenting the arguments for the class
 * constructor to help developers understand how to configure plugin instances.
 *
 * When defining attributes for a plugin type start by extending the existing
 * Drupal\Component\Plugin\Attribute\Plugin class. Then create a __construct()
 * method whose arguments are the configuration options for the plugin type.
 *
 * Classes that extend the Plugin class should always accept $id, $deriver
 * arguments. Developers can add any additional required, or optional, arguments
 * necessary to configure their specific plugin type.
 *
 * The #[\Attribute(\Attribute::TARGET_CLASS)] line says that the class, Block,
 * defines a #[Block()] attribute, and that the block attribute can only be used
 * on classes. Or put another way, the code that the #[Block()] attribute is
 * annotating must be a class, or it won’t validate.
 *
 * @see \Drupal\plugin_type_example\SandwichPluginManager
 * @see plugin_api
 */
#[\Attribute(\Attribute::TARGET_CLASS)]
class Sandwich extends Plugin {

  /**
   * Construct a sandwich attribute.
   *
   * @param string $id
   *   The plugin ID.
   * @param \Drupal\Core\StringTranslation\TranslatableMarkup|null $description
   *   (optional) Description of the sandwich.
   * @param float|null $calories
   *   (optional) Number of calories in the sandwich.
   * @param class-string|null $deriver
   *   (optional) The deriver class.
   */
  public function __construct(
    public readonly string $id,
    public readonly ?TranslatableMarkup $description = NULL,
    public readonly ?float $calories = NULL,
    public readonly ?string $deriver = NULL,
  ) {}

}
```

### A note about annotations

Prior to Drupal 11 we used annotations for metadata. They are still used for a few core plugin types which haven't yet transitioned to attributes. And, for backwards compatibility, it is common to support the use of both attributes and annotations in the same plugin type. This will ensure that plugin instances in code that hasn't been updated yet will continue to function.

If you are defining a new plugin type, and the related code will only ever be used with Drupal 11+ sites, you can skip the inclusion of annotations. If you're upgrading an existing plugin manager for Drupal 11 support and need to allow for backwards compatibility you should include an annotation definition like below.

The Annotation class should implement the `Drupal\Component\Annotation\AnnotationInterface` and should do so by extending `Drupal\Component\Annotation\Plugin`, which does most of the work for us.

*plugin\_type\_example/src/Annotation/Sandwich.php*:

```
<?php
/**
 * @file
 * Contains \Drupal\plugin_type_example\Annotation\Sandwich.
 *
 * Provides an example of how to define a new annotation type for use in
 * defining a plugin type. Demonstrates documenting the various properties that
 * can be used in annotations for plugins of this type.
 */

namespace Drupal\plugin_type_example\Annotation;

use Drupal\Component\Annotation\Plugin;

/**
 * Defines a Sandwich annotation object.
 *
 * @see \Drupal\plugin_type_example\SandwichPluginManager
 * @see plugin_api
 *
 * Note that the "@ Annotation" line below is required and should be the last
 * line in the docblock. It's used for discovery of Annotation definitions.
 *
 * @Annotation
 */
class Sandwich extends Plugin {

  /**
   * The plugin ID.
   *
   * @var string
   */
  public $id;

  /**
   * A brief, human-readable, description of the sandwich type.
   *
   * This property is designated as being translatable because it will appear
   * in the user interface. This provides a hint to other developers that they
   * should use the Translation() construct in their annotation when declaring
   * this property.
   *
   * @var \Drupal\Core\Annotation\Translation
   *
   * @ingroup plugin_translatable
   */
  public $description;

  /**
   * The number of calories per serving of this sandwich type.
   *
   * This property is a float value, so we indicate that to other developers
   * who are writing annotations for a Sandwich plugin.
   *
   * @var int
   */
  public $calories;

}
```

## Define an interface for sandwich plugins

An interface allows us to define the methods that any code interacting with any plugin of your new plugin type can call, and be assured are there. This is a critical part of the process because it allows a developer to ask any plugin manager factory for an instance of a plugin handled by that plugin manager and -- without knowing any other details about the specific instance that was returned -- be able to make use of it. For example: `$plugin_instance->doSomethingAwesome();`

In our `SandwichPluginManager` we declared that sandwich plugins are all going to be implementations of the `Drupal\plugin_type_example\SandwichInterface`. So what can you do with a sandwich?

*plugin\_type\_example/src/SandwichInterface.php*:

```
<?php
/**
 * @file
 * Provides \Drupal\plugin_type_example\SandwichInterface.
 *
 * When defining a new plugin type you need to define an interface that all
 * plugins of the new type will implement. This ensures that consumers of the
 * plugin type have a consistent way of accessing the plugin's functionality. It
 * should include access to any public properties, and methods for accomplishing
 * whatever business logic anyone accessing the plugin might want to use.
 *
 * For example, an image manipulation plugin might have a "process" method that
 * takes a known input, probably an image file, and returns the processed
 * version of the file.
 *
 * In our case we'll define methods for accessing the human readable description
 * of a sandwich and the number of calories per serving. As well as a method for
 * ordering a sandwich.
 */

namespace Drupal\plugin_type_example;

/**
 * An interface for all Sandwich type plugins.
 */
interface SandwichInterface {

  /**
   * Provide a description of the sandwich.
   *
   * @return string
   *   A string description of the sandwich.
   */
  public function description();

  /**
   * Provide the number of calories per serving for the sandwich.
   *
   * @return float
   *   The number of calories per serving.
   */
  public function calories();

  /**
   * @param array $extras
   *   An array of extra ingredients to include with this sandwich.
   *
   * @return mixed
   */
  public function order(array $extras);
}
```

## Make your plugin manager a service

In order to facilitate the use of your plugin manager within other code in your application it should be defined as a service. This is done by adding a record to your module's *MODULENAME.services.yml* file.

Example, *plugin\_type\_example/plugin\_type\_example.services.yml*:

```
# This declares the plugin manager to the service container. For background
# information on the service container, see https://www.drupal.org/node/2133171.
# Changes here require that the cache be cleared in order to have Drupal notice
# them.
services:
  # The machine name of the service. This is the string that must be passed to
  # Drupal::service() to get the instantiated plugin manager.
  plugin.manager.sandwich:
    # This tells the service container the name of our plugin manager class.
    class: Drupal\plugin_type_example\SandwichPluginManager
    parent: default_plugin_manager
```

It is common practice to prefix the name of a plugin manager service with `plugin.manager.` instead of the normal prefix which is generally the module's name.

## Provide a base class

Although strictly-speaking not required, it is generally a good idea to provide a base class for your plugin type that anyone wishing to provide an instance of your plugin type can extend. Most plugins will contain a fair amount of boilerplate code that is the same for almost all plugins of that type; things like `description()`, and `calories()` are likely pretty universal across all `Sandwich` plugins -- just read the data from the provided annotation and return it. By providing a base class we can eliminate the need for code duplication and make it even easier for other module developers to provide new `Sandwich` plugins.

In order to facilitate this best practice, core provides the `Drupal\Component\Plugin\PluginBase` that we can extend to create our own plugin type specific base class. The `PluginBase` class also implements the `PluginInspectionInterface`, and the `DerivativeInspectionInterface`, eliminating all sorts of boilerplate code that we would otherwise have to put in our `SandwichBase` class.

*plugin\_type\_example/src/SandwichBase.php*:

```
<?php

namespace Drupal\plugin_type_example;

use Drupal\Component\Plugin\PluginBase;

/**
 * A base class to help developers implement their own sandwich plugins.
 *
 * This is a helper class which makes it easier for other developers to
 * implement sandwich plugins in their own modules. In SandwichBase we provide
 * some generic methods for handling tasks that are common to pretty much all
 * sandwich plugins. Thereby reducing the amount of boilerplate code required to
 * implement a sandwich plugin.
 *
 * In this case both the description and calories properties can be read from
 * the #[Sandwich] attribute. In most cases it is probably fine to just use that
 * value without any additional processing. However, if an individual plugin
 * needed to provide special handling around either of these things it could
 * just override the method in that class definition for that plugin.
 *
 * We intentionally declare our base class as abstract, and don't implement the
 * order() method required by \Drupal\plugin_type_example\SandwichInterface.
 * This way even if they are using our base class, developers will always be
 * required to define an order() method for their custom sandwich type.
 *
 * @see \Drupal\plugin_type_example\Attribute\Sandwich
 * @see \Drupal\plugin_type_example\SandwichInterface
 */
abstract class SandwichBase extends PluginBase implements SandwichInterface {

  /**
   * {@inheritdoc}
   */
  public function description() {
    // Retrieve the description property from the attribute and return it.
    return $this->pluginDefinition['description'];
  }

  /**
   * {@inheritdoc}
   */
  public function calories() {
    // Retrieve the calories property from the attribute and return it.
    return (float) $this->pluginDefinition['calories'];
  }

  /**
   * {@inheritdoc}
   */
  abstract public function order(array $extras);

}
```

At this point you've successfully defined a new plugin type. Go you!

I'm not going to go into it in this tutorial, but you can read about using a plugin manager to do things like get a list of all plugins, and instantiate instances of a plugin, in the [Plugin Managers](https://drupalize.me/tutorial/plugin-managers) tutorial.

## Add some example sandwich plugins

You probably went through the effort of creating a new plugin type because you had some functionality that you wanted to encapsulate into a plugin. With all of the above in place you can provide a new sandwich plugin by creating a new class in the `Drupal\MODULENAME\Plugin\Sandwich` namespace, that implements the `Drupal\plugin_type_example\SandwichInterface`, with an attribute that uses `Drupal\plugin_type_example\Attribute\Sandwich`.

Here's an example:

*plugin\_type\_example/src/Plugin/Sandwich/ExampleHamSandwich.php*:

```
<?php

namespace Drupal\plugin_type_example\Plugin\Sandwich;

use Drupal\Core\StringTranslation\TranslatableMarkup;
use Drupal\plugin_type_example\Attribute\Sandwich;
use Drupal\plugin_type_example\SandwichBase;

/**
 * Provides a ham sandwich.
 */
#[Sandwich(
  id: "ham_sandwich",
  description: new TranslatableMarkup('Ham, mustard, rocket, sun-dried tomatoes.'),
  calories: 426
)]
class ExampleHamSandwich extends SandwichBase {

  /**
   * Place an order for a sandwich.
   *
   * This is just an example method on our plugin that we can call to get
   * something back.
   *
   * @param array $extras
   *   Array of extras to include with this order.
   *
   * @return string
   *   A description of the sandwich ordered.
   */
  public function order(array $extras) {
    $ingredients = ['ham, mustard', 'rocket', 'sun-dried tomatoes'];
    $sandwich = array_merge($ingredients, $extras);
    return 'You ordered an ' . implode(', ', $sandwich) . ' sandwich. Enjoy!';
  }

}
```

You can learn more about implementing plugins in our [Implement a Plugin of Any Type](https://drupalize.me/tutorial/implement-plugin-any-type) tutorial.

## Recap

Whenever you need to present the option for someone to choose among one or more plugins from a list of options to fulfill a specific objective you should define a new plugin type.

Defining a new plugin type requires:

- Defining a plugin manager and deciding on a discovery mechanism -- generally attribute class discovery
- Create a new attribute class to document your plugin type's attributes
- Create an interface that all instances of your new plugin type should implement
- Define a base class that others can extend when creating new plugins
- Create one or more instances of plugins of your new plugin type

## Further your understanding

- Learn to [use your new plugin manager](https://drupalize.me/tutorial/plugin-managers) to list, and instantiate available plugins.
- Learn how to [Implement a Plugin of Any Type](https://drupalize.me/tutorial/implement-plugin-any-type)
- Drupal core has over a dozen different plugin managers. Exploring their code, and how the rest of the system makes use of the plugins they provide is a great way to gain more insight into the types of problems you can solve by defining a new plugin type. Examples include, [`BlockManager`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Block%21BlockManager.php/class/BlockManager), [`MigrationPluginManager`](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21MigrationPluginManager.php/class/MigrationPluginManager/), and [`ImageEffectManager`](https://api.drupal.org/api/drupal/core%21modules%21image%21src%21ImageEffectManager.php/class/ImageEffectManager/)

## Additional resources

- The *plugin\_type\_example* in [the Examples project](https://www.drupal.org/project/examples) has some great sample code.
- [DrupalCon Los Angeles 2015: An Overview of the Drupal 8 Plugin System - by Joe Shindelar](https://www.youtube.com/watch?v=gd6s4wC_bP4) (The last third of the presentation covers creating a new plugin type.)
- [Plugin API overview](https://www.drupal.org/docs/drupal-apis/plugin-api/plugin-api-overview) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Drupal Plugin Types](/tutorial/drupal-plugin-types?p=2765)

Next
[Discover Existing Plugin Types](/tutorial/discover-existing-plugin-types?p=2765)

Clear History

Ask Drupalize.Me AI

close