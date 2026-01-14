---
title: "Drupal Code Standards: Object-Oriented Programmingfree"
url: "https://drupalize.me/tutorial/drupal-code-standards-object-oriented-programming?p=2458"
guide: "[[develop-drupal-sites]]"
order: 9
---

# Drupal Code Standards: Object-Oriented Programmingfree

## Content

Drupal core uses object-oriented programming (OOP). This method of programming introduces new coding standards to the project. In this tutorial we'll cover the Drupal coding standards that relate to object-oriented PHP code.

By the end of this tutorial you should know how to implement the Drupal coding standards related to OOP, and where to find more information when you've got questions about the standards.

## Goal

Write OOP code for Drupal that follows recommend coding standards guidelines.

## Prerequisites

- [What Are Coding Standards?](https://drupalize.me/tutorial/what-are-drupal-code-standards)

If you’re not yet familiar with OOP, you may want to learn more about that first, because we’re going over best practices and formatting here, and not the concepts. You can take a look at our [Object-oriented PHP topical page](https://drupalize.me/topic/object-oriented-php) for more information.

## Contents

- [What is object-oriented programming (OOP)?](#oop)
- [Declaring classes](#classes)
- [Namespaces](#namespaces)
- [Indenting and whitespace](#whitespace)
- [Naming conventions](#naming)
- [Interfaces](#interfaces)
- [Visibility](#visibility)
- [Type hinting](#type-hinting)
- [Chaining](#chaining)
- [Constructors and instantiation](#constructors)

## What is object-oriented programming (OOP)?

OOP is way of organizing your code to be more efficient, and it takes advantage of some really nice features in modern versions of PHP. One of the basic concepts of OOP is, not surprisingly, an object. Objects have properties, which hold data, and methods, which execute functions. After an object is created, or instantiated, it can be used over and over again. OOP allows for a lot of reuse and convenience that procedural programming does not.

## Best practices

Drupal has a set of coding standards [just for object-oriented code](https://www.drupal.org/docs/develop/coding-standards/object-oriented-code). As with other standards, most of these are based on common PHP coding conventions, and decided on by the Drupal community. This post will cover most of the object-oriented coding conventions you’ll run into. All of these examples are from Drupal's codebase.

## Declaring classes

There should be only one [class](https://www.php.net/manual/en/language.oop5.basic.php), [interface](https://www.php.net/manual/en/language.oop5.interfaces.php), or [trait](https://www.php.net/manual/en/language.oop5.traits.php) per file. Name the file after the class or interface. Here’s an example from the [CTools contributed module](https://www.drupal.org/project/ctools):

```
EntityFormWizardBase.php

<?php

namespace Drupal\ctools\Wizard;

use Drupal\Core\DependencyInjection\ClassResolverInterface;
use Drupal\Core\Entity\EntityManagerInterface;
use Drupal\Core\Form\FormBuilderInterface;
use Drupal\Core\Form\FormStateInterface;
use Drupal\Core\Routing\RouteMatchInterface;
use Drupal\ctools\Event\WizardEvent;
use Drupal\user\SharedTempStoreFactory;
use Symfony\Component\EventDispatcher\EventDispatcherInterface;

/**
 * The base class for all entity form wizards.
 */

abstract class EntityFormWizardBase extends FormWizardBase implements EntityFormWizardInterface {
```

The file is called `EntityFormWizardBase.php`.
The class is called `EntityFormWizardBase`.

This is straightforward, and probably something you’ve already been doing if you’ve been creating any class files.

Class naming is important for autoloading. Autoloading allows for classes to be loaded on demand, instead of a long list of `require` statements. The [Drupal.org handbook](https://www.drupal.org/node/608152#declaring) states:

> In Drupal, classes are autoloaded based on the [PSR-4](http://www.php-fig.org/psr/psr-4/) namespacing convention.
>
> In core, the PSR-4 'tree' starts under `core/lib/`.
>
> In modules, including contrib, custom and those in core, the PSR-4 'tree' starts under `modulename/src`.
>
> Defining a class in your module's .module file is only possible if the class does not have a superclass which might not be available when the .module file is loaded. It's best practice to move such classes into a PSR-4 source directory.

Most of what matters here is how you name and arrange your files and directories; the rest is happening behind the scenes. The [PSR-4 Autoloader documentation](http://www.php-fig.org/psr/psr-4/), which is quite brief and worth looking over, explains:

> This PSR describes a specification for [autoloading](https://www.php.net/autoload) classes from file paths... This PSR also describes where to place files that will be autoloaded according to the specification.

So all that’s going on here is that PSR-4 is telling you how to create your file paths so that classes can be autoloaded. To learn more about autoloading you can read our [Preparing for Drupal 8: PSR-4 Autoloading](https://drupalize.me/blog/201408/preparing-drupal-8-psr-4-autoloading) blog post.

### A note on the file docblock

The current Drupal standards state:

> The `@file` doc block MUST be present for all PHP files, with one exception: files that contain a namespaced class/interface/trait, whose file name is the class name with a .php extension, and whose file path is closely related to the namespace (under PSR-4 or a similar standard), SHOULD NOT have a @file documentation block.

Be sure to include a blank line at the beginning and end of a `/** @file */` block. For example:

```
<?php

/**
 * @file
 * Contains Drupal\metatag\Command\GenerateGroupCommand.
 */

namespace Drupal\metatag\Command;
```

## Namespaces

If you’re not familiar with namespaces, you can start with the [PHP Namespaces in 120 Seconds video](https://drupalize.me/videos/php-namespaces-120-seconds) or the [documentation on PHP.net](https://www.php.net/manual/en/language.namespaces.rationale.php). Namespaces are a way of organizing codebases. [Drupal’s coding standards regarding namespaces](https://www.drupal.org/node/1353118) are detailed, so we’ll go over the most important points here.

First, let’s look at an example of a namespace from the [Metatag contributed module](https://www.drupal.org/project/metatag).

```
<?php

/**
 * @file
 * Contains Drupal\metatag\Command\GenerateGroupCommand.
 */

namespace Drupal\metatag\Command;

use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Output\OutputInterface;
use Drupal\Console\Command\GeneratorCommand;
use Drupal\Console\Command\Shared\ContainerAwareCommandTrait;
use Drupal\Console\Command\Shared\ModuleTrait;
use Drupal\Console\Command\Shared\FormTrait;
use Drupal\Console\Command\Shared\ConfirmationTrait;
use Drupal\Console\Style\DrupalStyle;
use Drupal\metatag\Generator\MetatagGroupGenerator;

/**
 * Class GenerateGroupCommand.
 *
 * Generate a Metatag group plugin.
 *
 * @package Drupal\metatag
 */

class GenerateGroupCommand extends GeneratorCommand {

  use ContainerAwareCommandTrait;
  use ModuleTrait;
  use FormTrait;
  use ConfirmationTrait;
```

The file doc block tells us that this file contains a class called `Drupal\metatag\Command\GenerateGroupCommand`, and then we see the namespace declaration for `Drupal\metatag\Command`. Now look at the directory structure and that’s what we’ll see:

```
  -metatag
    -config
    -metatag_google_plus
    -metatag_open_graph
    -metatag_twitter_cards
    -metatag_verification
    -src
      -Annotation
      -Command
        GenerateGroupCommand.php
        GenerateTagCommand.php
```

If you remember, we learned just above that the PSR-4 directory tree starts *under* `src/`, which is why it’s not included in the namespace itself.

When creating a Drupal module, you should follow this directory structure - `<modulename>/src/<namespace>`.

You can also see a list of classes to be *used* in this file. Any class or interface with a backslash in it must be declared like this at the top of the file. These are called "fully-qualified namespaces" and they now can be referred to by just the last part of the namespace - the fully-qualified namespace may no longer be used inside the code. Take a look at the above code, in the class `GenerateGroupCommand` - the `use` statements there refer to the same namespaces used at the top of the file, but here we don’t `use` the entire name (no backslash).

If you have two classes with the same name, that’s a collision, and we fix it by *aliasing* the namespace. Use the next higher portion of the namespace to create the alias.

Here’s an example from [Drupal core](https://api.drupal.org/api/drupal/core%21modules%21views%21src%21Plugin%21views%21field%21Url.php/11.x):

```
<?php

<?php

namespace Drupal\views\Plugin\views\field;

use Drupal\Core\Form\FormStateInterface;
use Drupal\Core\Link;
use Drupal\Core\Url as CoreUrl;
use Drupal\views\ResultRow;
```

Here, an alias for `Drupal\Core\Url` is created, to be clear about *which* `Url` class is being used.

There should only be one class per use statement.

An exception to `use` statements is if you are using a global class. In that case, you don’t need to `use` anything.

Here’s an example from the [Devel contributed module](https://www.drupal.org/project/devel):

```
/**
 * Formats a time.
 *
 * @param integer|float $time A raw time
 *
 * @return float The formatted time
 *
 * @throws \InvalidArgumentException When the raw time is not valid
 */

private function formatTime($time) {
  if (!is_numeric($time)) {
    throw new \InvalidArgumentException('The time must be a numerical value');
  }

  return round($time, 1);
}
```

The  `\InvalidArgumentException` is not declared anywhere in the file, because it’s a global class.

## Indenting and whitespace

For all the formatting basics, refer to the [Code Standards Formatting tutorial](https://drupalize.me/tutorial/drupal-code-standards-formatting). Those are the base standards, but there are some specific OOP conventions as well.

There should be an empty line between the start of a class or interface definition and a property or method definition.

Here’s an example from the [Token contributed module](https://www.drupal.org/project/token):

```
<?php

/**
 * @file
 * Contains \Drupal\token\TokenEntityMapperInterface.
 */

namespace Drupal\token;

interface TokenEntityMapperInterface {

  /**
   * Return an array of entity type to token type mappings.
   *
   * @return array
   *   An array of mappings with entity type mapping to token type.
   */
  public function getEntityTypeMappings();
```

This code declares an interface, `TokenEntityMapperInterface`, and leaves a blank line before the function declaration.

There should be an empty line between a property definition and a method definition. Here’s another example from the [Token contributed module](https://www.drupal.org/project/token):

```
/**
 * @var array
 */
protected $entityMappings;

public function __construct(EntityTypeManagerInterface $entity_type_manager, ModuleHandlerInterface $module_handler) {
  $this->entityTypeManager = $entity_type_manager;
  $this->moduleHandler = $module_handler;
}
```

This code declares a property, `$entityMappings`, and leaves a blank line before the function definition.

There should also be a blank line between the end of a method definition and the end of a class definition - so a blank line between the ending curly braces.

Again from the Token module, here we can see that there is a blank line after the last function:

```
  /**
   * Resets metadata describing supported tokens.
   */
  public function resetInfo() {
    $this->tokenInfo = NULL;
    $this->cacheTagsInvalidator->invalidateTags([static::TOKEN_INFO_CACHE_TAG]);
  }

}
```

## Naming conventions

You can find [a list of detailed naming conventions on Drupal.org](https://www.drupal.org/node/608152#naming), but we’ll go over some basics.

- When declaring a class or interface, use UpperCamel.
- When declaring a method or class property, use lowerCamel.
- Class names shouldn’t include "drupal" or “class.”
- Interfaces should end with "Interface."
- Test classes should end with "Test."

Here’s an example from the core *block* module (*core/modules/block/src/Plugin/Derivative/ThemeLocalTask.php*):

```
<?php

namespace Drupal\block\Plugin\Derivative;

use Drupal\Component\Plugin\Derivative\DeriverBase;
use Drupal\Core\Extension\ThemeHandlerInterface;
use Drupal\Core\Plugin\Discovery\ContainerDeriverInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;

/**
 * Provides dynamic tabs based on active themes.
 */
class ThemeLocalTask extends DeriverBase implements ContainerDeriverInterface {
```

In the above code, note the naming convention of the extended base class and the interface, as well as the capitalization.

## Interfaces

For flexibility reasons, it is strongly encouraged that you create interface definitions and implement them in separate classes. The [Drupal.org documentation](https://www.drupal.org/node/608152#interfaces) states:

> The use of a separate interface definition from an implementing class is strongly encouraged because it allows more flexibility in extending code later. A separate interface definition also neatly centralizes documentation making it easier to read. All interfaces should be fully documented according to [established documentation standards](https://www.drupal.org/node/1354#classes).

If there is even a remote possibility of a class being swapped out for another implementation at some point in the future, split the method definitions off into a formal Interface. A class that is intended to be extended must always provide an Interface that other classes can implement rather than forcing them to extend the base class.

Here’s an example of an interface and a class implementation from the [CTools contributed module](https://www.drupal.org/project/ctools):

```
<?php

/**
 * @file
 * Contains \Drupal\ctools\ConstraintConditionInterface.
 */

namespace Drupal\ctools;

interface ConstraintConditionInterface {

  /**
   * Applies relevant constraints for this condition to the injected contexts.
   *
   * @param \Drupal\Core\Plugin\Context\ContextInterface[] $contexts
   *
   * @return NULL
   */

  public function applyConstraints(array $contexts = array());

  /**
   * Removes constraints for this condition from the injected contexts.
   *
   * @param \Drupal\Core\Plugin\Context\ContextInterface[] $contexts
   *
   * @return NULL
   */

  public function removeConstraints(array $contexts = array());

}
```

In this code, we can see a simple interface declared, `ConstraintConditionInterface`, with two functions, `applyConstraints` and `removeConstraints`.

```
<?php

/**
 * @file
 * Contains \Drupal\ctools\Plugin\Condition\NodeType.
 */

namespace Drupal\ctools\Plugin\Condition;

use Drupal\node\Plugin\Condition\NodeType as CoreNodeType;
use Drupal\ctools\ConstraintConditionInterface;

class NodeType extends CoreNodeType implements ConstraintConditionInterface {

  /**
   * {@inheritdoc}
   *
   * @param \Drupal\Core\Plugin\Context\ContextInterface[] $contexts
   */

  public function applyConstraints(array $contexts = array()) {
    // Nullify any bundle constraints on contexts we care about.
    $this->removeConstraints($contexts);
    // If a single bundle is configured, we can set a proper constraint.
    if (count($this->configuration['bundles']) == 1) {
      $bundle = array_values($this->configuration['bundles']);
      foreach ($this->getContextMapping() as $definition_id => $context_id) {
        $contexts[$context_id]->getContextDefinition()->addConstraint('Bundle', ['value' => $bundle[0]]);
      }
    }
  }

  /**
   * {@inheritdoc}
   *
   * @param \Drupal\Core\Plugin\Context\ContextInterface[] $contexts
   */
  public function removeConstraints(array $contexts = array()) {
    // Reset the bundle constraint for any context we've mapped.
    foreach ($this->getContextMapping() as $definition_id => $context_id) {
      $constraints = $contexts[$context_id]->getContextDefinition()->getConstraints();
      unset($constraints['Bundle']);
      $contexts[$context_id]->getContextDefinition()->setConstraints($constraints);
    }
  }
}
```

In this code, we have a class, `NodeType`, which implements `ConstraintConditionInterface`. It also provides an implementation for both of the classes in the interface - `applyConstraints` and `removeConstraints` both get fleshed out here. (Another note here, the implemented functions use the `{@inheritdoc}` notation, because the parameters have not changed, so documentation can be referred to the interface.) You can see how the interface could be implemented differently in a different class, but still adhere to the original interface.

If you’re familiar with the OOP concept of [polymorphism](http://code.tutsplus.com/tutorials/understanding-and-applying-polymorphism-in-php--net-14362), it applies here. Polymorphism allows for classes to implement different functionality while sharing a common interface. If you’re not familiar with this, [the OOP Examples project](https://www.drupal.org/project/oop_examples) is a great place to start.

From the 8.x version of the project, example 8, here is a very simple interface that returns a color:

```
/**
 * Color interface.
 */

interface ColorInterface {
  /**
   * Returns color of the object.
   */
  public function getColor();

}
```

Here’s a class that implements the color interface:

```
/**
 * Fruit class.
 */
class Fruit implements ColorInterface {
  /**
   * Returns color of the object.
   */
  public function getColor() {
    return t('green');
  }
}
```

And another completely different class, which also implements the color interface:

```
/**
 * Vehicle class.
 */

class Vehicle implements ColorInterface {

  /**
   * The vehicle color.
   *
   * @var string
   *
   * Default color translation t() is set up in class constructor because
   * expression is not allowed as field default value like:
   * public $color = t('red');
   */
  public $color;

  /**
   * Class constructor.
   */
  public function __construct() {
    $this->color = t('red');
  }

  /**
   * Returns class type description.
   */
  public function getClassTypeDescription() {
    $s = t('a generic vehicle');
    return $s;
  }

  /**
   * Returns class description.
   */
  public function getDescription() {
    $s = t('This is') . ' ';
    $s .= $this->getClassTypeDescription();
    $s .= ' ' . t('of color') . ' ';
    $s .= $this->color;
    $s .= '.';
    return $s;
  }

  /**
   * Implements ColorInterface.
   */
  public function getColor() {
    return $this->color;
  }
}
```

These are just a couple parts of the examples, but it helps to show how flexible interfaces are and why we use them.

## Visibility

All methods and properties of classes must have their visibility declared. They can be public, protected, or private. Public properties are strongly discouraged. Here’s an example from the [Metatag contributed module](https://www.drupal.org/project/metatag):

```
/**
 * Token handling service. Uses core token service or contributed Token.
 */

class MetatagToken {
  /**
   * Token service.
   *
   * @var \Drupal\Core\Utility\Token
   */
  protected $token;

  /**
   * Constructs a new MetatagToken object.
   *
   * @param \Drupal\Core\Utility\Token $token
   *   Token service.
   */
  public function __construct(Token $token) {
    $this->token = $token;
  }
```

This code declares a protected property, `$token`, and a public function, `__construct`.

## Type hinting

Type-hinting is optional, but recommended, as it can be a great debugging tool. If an object of the incorrect type is passed, an error will be thrown. If a method’s parameters expect a certain interface, specify it. Do not specify a class as a type, only an interface. This ensures that you are checking for a type, but keeps your code fluid by not adhering rigidly to a class. This is another instance where polymorphism comes into play. We can keep our code reusable by checking only for the interface and not the class, allowing the classes to differ.

Here’s an example from the [Pathauto contributed module](https://www.drupal.org/project/pathauto):

```
/**
 * Extends the default PathItem implementation to generate aliases.
 */
class PathautoItem extends PathItem {

  /**
   * {@inheritdoc}
   */
  public static function propertyDefinitions(FieldStorageDefinitionInterface $field_definition) {
    $properties = parent::propertyDefinitions($field_definition);
    $properties['pathauto'] = DataDefinition::create('integer')
      ->setLabel(t('Pathauto state'))
      ->setDescription(t('Whether an automated alias should be created or not.'))
      ->setComputed(TRUE)
      ->setClass('\Drupal\pathauto\PathautoState');
    return $properties;
  }
```

In this code, we can see that the `propertyDefinitions` function has the parameter `$field_definition` with the type hint `FieldStorageDefinitionInterface`.

## Chaining

Chaining allows you to immediately call a function on a returned object. You’ve probably most often seen or used this with database objects. Here’s an example from the [Devel Node Access contributed module](https://www.drupal.org/project/devel):

```
 // How many nodes are not represented in the node_access table?
  $num = db_query('SELECT COUNT(n.nid) AS num_nodes FROM {node} n LEFT JOIN {node_access} na ON n.nid = na.nid WHERE na.nid IS NULL')->fetchField();
```

Without chaining, you’d have set the results of that query into an object like `$result`, and *then* you could use the `fetchField()` function in another statement.

Additionally, to allow for chaining whenever possible, methods that don’t return a specific value should return `$this`. Especially in methods that set a state or property on an object, returning the object itself is more useful than returning a boolean or NULL.

Here are some chaining examples from the [Google Analytics contributed module](https://www.drupal.org/project/google_analytics), where configuration is set and saved:

```
$this->config('google_analytics.settings')->set('account', $ua_code)->save();
// Show tracking on "every page except the listed pages".
$this->config('google_analytics.settings')->set('visibility.request_path_mode', 0)->save();
// Disable tracking on "admin*" pages only.
$this->config('google_analytics.settings')->set('visibility.request_path_pages', "/admin\n/admin/*")->save();
// Enable tracking only for authenticated users only.
$this->config('google_analytics.settings')->set('visibility.user_role_roles', [AccountInterface::AUTHENTICATED_ROLE => AccountInterface::AUTHENTICATED_ROLE])->save();
```

## Constructors and instantiation

Drupal’s coding standards [discourage directly creating classes](https://www.drupal.org/node/608152#instantiation). Instead, it is ideal to create a factory to instantiate the object and return it. Two reasons are given for this:

1. The function can be written to be reused to return different objects with the same interface as needed. As we discussed above when reviewing interfaces, this relies on polymorphism: the idea that we have classes that implement different functionality while sharing a common interface. If the function is written to return objects with the same interface and not limited to a class, it can be reused more widely in our code.
2. You cannot chain constructors in PHP, but you can chain the returned object from a function. Chaining is very useful, as you’ve already read above.

Here’s an example from the [Metatag contributed module](https://www.drupal.org/project/metatag):

```
/**
 * {@inheritdoc}
 */

protected function createGenerator() {
  return new MetatagTagGenerator();
}
```

This is a function that returns a new instance of a `MetatagTagGenerator`. The `createGenerator()` function is declared in an interface that is implemented by this class.

## Recap

This is a lot of information -- and if you’re not especially familiar with Drupal or OOP, it may not make a lot of sense yet -- but it will! It can take a lot of time and practice to change the way you program, and the way you think about a system like Drupal and how it works, but keep your chin up and your code clean, and you’ll get there.

## Further your understanding

- Can you find examples in core of a class that has a factory method, and a function or method that uses type hinting?
- Why do some PHP files that contain a class have a `@file` tag while some do not?

## Additional resources

- [Object-oriented code](https://www.drupal.org/docs/develop/coding-standards/object-oriented-code) (Drupal.org) - Official OOP coding standards
- [Namespaces](https://www.drupal.org/docs/develop/coding-standards/namespaces) (Drupal.org) - Official namespacing standards
- [Relax requirement for @file when using OO Class or Interface per file](https://www.drupal.org/node/2304909) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Drupal Code Standards: Documentation](/tutorial/drupal-code-standards-documentation?p=2458)

Next
[Drupal Code Standards: The t() Function](/tutorial/drupal-code-standards-t-function?p=2458)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

Drupal Training Resources by Alanna Burke of [Chromatic](https://chromatichq.com) are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://chromatichq.com/blog>.

Clear History

Ask Drupalize.Me AI

close