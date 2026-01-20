---
title: "Annotations"
url: "https://drupalize.me/tutorial/annotations?p=3292"
guide: "[[develop-drupal-sites]]"
order: 4
---

# Annotations

## Content

Annotations are specially-formatted PHP docblock comments that are used for class discovery and metadata description. While it is technically possible to use annotations for other purposes, at the moment Drupal only uses them for the [plugin system](https://drupalize.me/tutorial/what-are-plugins).

In this tutorial we'll look at:

- What annotations are
- The use case for annotations
- How to figure out what you can put into an annotation

By the end of this tutorial you should understand how annotations are used in Drupal and how to write them in your own code.

## Goal

Understand what annotations are, the problem they are solving, and how to write an annotation for your custom code.

## Prerequisites

- None.

## Annotations versus PHP Attributes

Drupal now supports the use of PHP attributes, and when supported, they should be used instead of annotations. Look at an existing instance of the plugin type in question to see what is currently used.

Prior to Drupal 10.2 the plugin system used Doctrine annotations to accomplish exactly the same thing that PHP attributes are used for now. And, at the moment, Drupal will continue to support the use of both annotations and PHP attributes. Eventually the use of annotations will be phased out completely.

For now there are a few questions to consider when choosing annotations versus PHP attributes:

- Does your code need to support a version of Drupal prior to 10.2?
- If you're using annotations/PHP attributes to implement a plugin type, has the plugin type manager been updated to support the use of attributes?
- Are you implementing an entity type? Plugin types in core have largely been converted to support attributes except when declaring entity types. For now, if you're defining a custom entity type, via plugins, you'll need to continue to use annotations. See [#3396166](https://www.drupal.org/project/drupal/issues/3396166).

Learn more about PHP attributes in Drupal

- Learn how to use [PHP attributes](https://drupalize.me/tutorial/php-attributes).
- Read more about why Drupal is converting to PHP Attributes in this blog post we wrote about it: [PHP Attributes for Drupal Plugins](https://drupalize.me/blog/php-attributes-drupal-plugins).

## What are annotations?

Annotations are specially-formatted PHP docblock (*@docblock*) comments that can be parsed and used to retrieve metadata about, and/or provide configuration for, a PHP class.

Here's an example of a typical *@docblock* with an annotation:

```
/**
 * Provides a ham sandwich.
 *
 * Combine some ham, mustard, and a healthy helping of rocket together into a
 * ham sandwich plugin.
 *
 * @Sandwich(
 *   id = "ham_sandwich",
 *   description = @Translation("Ham, mustard, rocket, sun-dried tomatoes."),
 *   calories = 426,
 * )
 */
class ExampleHamSandwich extends SandwichBase {

}
```

The annotation in this *@docblock* is relatively easy to spot. It starts with the keyword `Sandwich` prefixed with an `@` character. The content above that is just standard comments. the `@Sandwich` keyword and everything within the parentheses is part of the Sandwich annotation. And for the most part, this is what you should expect to find in Drupal.

This annotation is read by [the Doctrine annotation parser](https://www.doctrine-project.org/projects/doctrine-annotations/en/1.6/index.html), and turned into an object that PHP can use. The metadata in this annotation can then be used for things like creating a list of all sandwich plugins in the UI.

## Why annotations?

In Drupal, annotations are used as part of the Plugin API.

Annotations allow metadata to be collected in an efficient manner, and for plugin classes to only be loaded into memory and instantiated when their functionality is needed.

There is a performance bonus to using annotations as it makes Drupal use less memory when discovering plugins. The alternative would be requiring every class to implement a `getInfo()` method, then loading each class into memory to get its information. That memory is not freed until the end of the request and thus greatly increases the peak memory requirement for PHP. The annotation parser tokenizes the text of the file without including it as a PHP file and so memory use is minimized.

In contrast to other discovery mechanisms, the annotation metadata lives in the same file and is an integral part of the class that implements the plugin. This makes it easier to find and easier to create a new custom plugin by simply copying an existing one.

## The annotation syntax

In a nutshell, annotations are inherently key/value data structures, with support for nesting.

The annotations syntax comes from the Doctrine project (for details, see the [documentation](https://www.doctrine-project.org/projects/doctrine-annotations/en/1.6/index.html)), though Drupal has a slightly different coding style, such as a new line after each value and a trailing comma on lists, so that will be used here.

### Quotation marks

Keys on the root level may use **double quotes or no quotes**. Generally we recommend skipping the quotes unless the key name contains spaces. Keys in sublevels *must* use double quotes.

**No single quotes**. You cannot use single quotes in annotations at all for keys or values.

Available data types for values are:

### Strings

**Strings:** Use double quotes. If your string includes a double quote character, use a pair of double quotes to escape it.

```
/**
 * @Annotation(
 *   key = "foo",
 *   key_2 = "Use ""a pair of double quotes"" to escape double quotes",
 * )
 */
```

### Numbers

**Numbers:** Must not use quotes. Will be parsed as a string if quotes are used.

```
/**
 * @Annotation(
 *   key = 42,
 * )
 */
```

### Booleans

**Booleans:** Must **not** use quotes. Will be parsed as a string if quotes are used.

```
/**
 * @Annotation(
 *   key = TRUE,
 * )
 */
```

### Lists

**Lists:** Use curly brackets: `{}`.

```
/**
 * @Annotation(
 *   key = {
 *     "foo",
 *     "bar",
 *   }
 * )
 */
```

### Maps

**Maps:** Use curly brackets (`{}`) and an equality sign (`=`) to separate the key and the value.

```
/**
 * @Annotation(
 *   key = {
 *     "foo" = "bar",
 *   }
 * )
 */
```

## Translatable text in annotations

Sometimes an annotation defines values that are displayed in the user interface. In order to ensure those can be translated, we need to use a special syntax. Translatable strings should be wrapped in the `@Translation()` annotation.

```
/**
 * @Annotation(
 *   label = @Translation("Greatest taco ever"),
 * )
 */
```

To provide replacement values for placeholders, use the `arguments` array.

```
/**
 * @Annotation(
 *   label = @Translation("Hello !name", arguments = {"!name" = "Joe"}),
 * )
 */
```

It is also possible to provide a context with the text, similar to `t()`.

```
/**
 * @Annotation(
 *   label = @Translation("Greatest taco ever", context = "Validation"),
 * )
 */
```

Learn more about [annotations for translatable text](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Annotation%21Translation.php/group/plugin_translatable/).

## Documenting annotations

How do you know what to put in your annotation? Well, that depends on the type of annotation you're using. In Drupal, this will correspond with the type of plugin you're implementing.

Annotations, and their corresponding key value pairs, are documented in Drupal by providing an empty class in the `Drupal\{module}\Annotation` namespace which implements `\Drupal\Component\Annotation\AnnotationInterface`, and adding a *@docblock* that contains the `@Annotation` annotation.

Here's an example:

```
namespace Drupal\plugin_type_example\Annotation;

use Drupal\Component\Annotation\Plugin;

/**
 * Defines a Sandwich annotation object.
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
   * @var \Drupal\Core\Annotation\Translation
   *
   * @ingroup plugin_translatable
   */
  public $description;

  /**
   * The number of calories per serving of this sandwich type.
   *
   * @var int
   */
  public $calories;

}
```

The annotation class should contain a property, and associated documentation, for each possible key in the annotation.

## Examples from core

Here are a couple of examples of annotations used in core to help illustrate the concept:

- [Drupal\user\Plugin\Block\UserLoginBlock](https://api.drupal.org/api/drupal/core%21modules%21user%21src%21Plugin%21Block%21UserLoginBlock.php/class/UserLoginBlock/) - Shows a typical block plugin annotation
- [Drupal\node\Entity\Node](https://api.drupal.org/api/drupal/core%21modules%21node%21src%21Entity%21Node.php/class/Node/) - Demonstrates a complex content entity annotation
- [Drupal\link\Plugin\Field\FieldFormatter\LinkFormatter](https://api.drupal.org/api/drupal/core%21modules%21link%21src%21Plugin%21Field%21FieldFormatter%21LinkFormatter.php/class/LinkFormatter/) - Shows a typical field formatter plugin annotation

## Recap

Annotations are specially-formatted docblock comments that provide metadata, and/or configuration, for a PHP class that be obtained without loading the class into memory. In Drupal, they are used for plugin discovery, metadata, and configuration.

## Further your understanding

- See [a list of all annotations in Drupal core](https://api.drupal.org/api/drupal/core%21core.api.php/group/annotation/).
- Read more about [the Doctrine Annotation parser](https://www.doctrine-project.org/projects/doctrine-annotations/en/1.6/index.html).
- [This presentation](https://www.youtube.com/watch?v=TqyWGbQUPGM) by @rdohms is the most in-depth explanation of the use of annotations in PHP that we're currently aware of. If you're curious about the background, or a bit more about how they work under-the-hood, this is for you.

## Additional resources

- [A list of all annotations in Drupal core](https://api.drupal.org/api/drupal/core%21core.api.php/group/annotation/)
- [Annotations-based plugins](https://www.drupal.org/node/1882526)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[PHP Attributes](/tutorial/php-attributes?p=3292)

Next
[Best Practice Drupal Development](/tutorial/best-practice-drupal-development?p=3292)

Clear History

Ask Drupalize.Me AI

close