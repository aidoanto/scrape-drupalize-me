---
title: "PHP Attributes"
url: "https://drupalize.me/tutorial/php-attributes?p=3292"
guide: "[[develop-drupal-sites]]"
---

# PHP Attributes

## Content

PHP attributes are a native PHP language feature, introduced in PHP 8.0, that provide a way to add metadata to classes, methods, properties, and functions in PHP code.

In Drupal, this metadata is used by the [plugin system](https://drupalize.me/tutorial/what-are-plugins) to aid in the discovery and configuration of plugin instances. As a Drupal developer, it's important to understand how to recognize, read, and write PHP attributes, as you'll encounter them when working with plugins.

In this tutorial we'll look at:

- What PHP attributes are
- The use case for attributes in Drupal
- An overview of the attribute syntax

By the end of this tutorial, you should understand how attributes are used in Drupal and how to write them in your own code.

## Goal

Understand what PHP attributes are, the problem they are solving, and the attribute syntax.

## Prerequisites

- None.

**Note:** As of Drupal 10.2, new plugin implementations should use PHP attributes. If you are developing a plugin for Drupal 10.1 or older use [annotations](https://drupalize.me/tutorial/annotations) instead of attributes.

## Annotations versus PHP attributes

Prior to Drupal 10.2, the plugin system used Doctrine annotations to accomplish exactly the same thing that PHP attributes are used for now. And, at the moment, Drupal will continue to support the use of both annotations and PHP attributes. Eventually the use of annotations will be phased out completely.

For now there are a few things you'll need to consider when choosing annotations versus PHP attributes:

- Does your code need to support a version of Drupal prior to 10.2?
- If you're using annotations/PHP attributes to implement a plugin type, has the plugin type manager been updated to support the use of attributes?
- As of Drupal 11.2, [all plugin types in core have been converted to support attributes](https://www.drupal.org/project/drupal/issues/3396165). (See the *Additional resources* section below for links to change records.) If you're using a version of Drupal that doesn't use PHP attributes, you'll need to use [annotations](https://drupalize.me/tutorial/annotations) instead.

Our suggestion is to use PHP attributes whenever it is supported (look at an existing plugin instance to see what's used).

Learn more about annotations and Drupal's transition to attributes:

- Tutorial: [Annotations](https://drupalize.me/tutorial/annotations)
- Read more about why Drupal is converting from Doctrine annotations to PHP attributes in this blog post: [PHP Attributes for Drupal Plugins](https://drupalize.me/blog/php-attributes-drupal-plugins)

## What are PHP attributes?

PHP attributes are a native PHP feature that allows metadata to be attached to classes, methods, and properties in a structured manner. This metadata can then be read at runtime using the [PHP Reflection APIs](https://www.php.net/manual/en/book.reflection.php). Perhaps most importantly for the Drupal Plugin API, attributes can be read without first having to instantiate an instance of the class they describe.

Here's an example of a typical PHP attribute use you can expect to see in Drupal:

```
use Drupal\Core\StringTranslation\TranslatableMarkup;
use Drupal\sandwich_module\Attribute\Sandwich;

/**
 * Class comment goes here ...
 */
#[Sandwich(
  id: "ham_sandwich",
  description: new TranslatableMarkup("Ham, mustard, rocket, sun-dried tomatoes."),
  calories: 426
)]
class ExampleHamSandwich extends SandwichBase {
  // Code goes here...
}
```

The attribute `#[Sandwich]` is placed directly above the `ExampleHamSandwich` class definition, which directly associates the metadata with the class.

## Why PHP attributes?

In Drupal, PHP attributes are used as part of the Plugin API.

Attributes allow metadata to be collected efficiently, enabling plugin classes to be loaded only when needed. This minimizes memory usage and improves performance.

There is a performance bonus to using PHP attributes like this, as it makes Drupal use less memory when discovering plugins. The alternative would be requiring every class to do something like implement a `getInfo()` method, then loading each class into memory to get its information. That memory is not freed until the end of the request and thus greatly increases the peak memory requirement for PHP.

In contrast to other discovery mechanisms, the PHP attribute metadata lives in the same file and is an integral part of the class that implements the plugin. This makes it easier to find and easier to create a new custom plugin by simply copying an existing one.

Using PHP attributes offers some benefits over annotations because the metadata is handled natively by PHP. With attributes, PHP does not need an external parser like Doctrine, reducing the complexity and overhead of parsing metadata comments. This also makes the code cleaner and easier to maintain. And many popular IDEs support syntax highlighting and autocompletion features for PHP attributes, which creates a better developer experience.

## The PHP Attribute syntax

An attribute declaration always starts with `#[` and ends with a corresponding `]`. Inside, one or more attributes are listed. The attribute name, `Sandwich` in the above example, is a reference to the attribute class `Drupal\sandwich_module\Attribute\Sandwich`.

In a nutshell, an instance of the `Sandwich` attribute class is created and everything inside the `(` and `)` are arguments to the class constructor. The use of key/value pairs like `id: "ham_sandwich"` works thanks to PHP's named arguments syntax.

Arguments to the attribute work just like calling a method or function and type hinting works as expected.

Here's some examples you'll commonly see in Drupal.

### Strings

**Strings:** Use double quotes. If your string includes a double quote character, escape it with a backslash.

```
#[AttributeExample(
  key: "foo",
  key_2: "Use \"backslashes\" to escape double quotes inside a string."
)]
class MyClassWithAttributes {}
```

### Numbers

***Numbers:*** Must not use quotes.

```
#[AttributeExample(
  key: 42,
  float_key: 42.3333
)]
```

### Booleans

**Booleans:** Must not use quotes.

```
#[AttributeExample(
  key: true
)]
```

### Lists / Arrays

**Lists:** Use array syntax: `array()`.

```
#[AttributeExample(
  key: array("foo", "bar")
)]
```

### Maps / Associative Arrays

**Maps:** Use an arrow (`=>`) to separate the key and the value.

```
#[AttributeExample(
  key: array("foo" => "bar")
)]
```

### Translatable text in attributes

Sometimes an attribute defines values that are displayed in the user interface. In order to ensure those can be translated, use `Drupal\Core\StringTranslation\TranslatableMarkup`.

```
use Drupal\Core\StringTranslation\TranslatableMarkup;

#[Sandwich(
  id: "ham_sandwich",
  description: new TranslatableMarkup("Greatest taco ever")
)]
```

To provide replacement values for placeholders, use an associative array.

```
use Drupal\Core\StringTranslation\TranslatableMarkup;

#[Sandwich(
  id: "ham_sandwich",
  description: new TranslatableMarkup("Hello @name", ["@name" => "Joe"])
)]
```

It's also possible to provide a context with the text, similar to the `t()` function.

```
use Drupal\Core\StringTranslation\TranslatableMarkup;

#[Sandwich(
  id: "ham_sandwich",
  description: new TranslatableMarkup("Greatest taco ever", [], ['context' => 'Validation'])
)]
```

## Documenting attributes

How do you know what to put in your attribute? This depends on the type of attribute you're using. In Drupal, this corresponds with the type of plugin you're implementing.

Attributes, and their corresponding arguments, are documented by providing a class in the `Drupal\{module}\Attribute` namespace. This class specifies the structure of the attribute and the accepted keys.

Here's an example:

```
namespace Drupal\sandwich_module\Attribute;

use Drupal\Core\StringTranslation\TranslatableMarkup;

#[\Attribute(\Attribute::TARGET_CLASS)]
class Sandwich {

  /**
   * Constructs a sandwich attribute.
   *
   * @param string $id
   *   The plugin ID.
   * @param \Drupal\Core\StringTranslation\TranslatableMarkup|null $description
   *   The description of the sandwich.
   * @param int $calories
   *   Number of calories in the sandwich.
   */
  public function __construct(
    public readonly string $id,
    public readonly ?TranslatableMarkup $description = NULL,
    public readonly int $calories
  ) {}
}
```

The constructor for the attribute should document all possible arguments for the attribute.

## Examples from core

Here are a couple of examples of PHP attributes used in core to help illustrate the concept:

- [Drupal\user\Plugin\Block\UserLoginBlock](https://api.drupal.org/api/drupal/core%21modules%21user%21src%21Plugin%21Block%21UserLoginBlock.php/class/UserLoginBlock/): A typical block plugin attribute
- [Drupal\link\Plugin\Field\FieldFormatter\LinkFormatter](https://api.drupal.org/api/drupal/core%21modules%21link%21src%21Plugin%21Field%21FieldFormatter%21LinkFormatter.php/class/LinkFormatter/): A typical field formatter plugin attribute

## Recap

PHP attributes are the PHP languages native way of supporting the association of easily parsable metadata with a class. In Drupal, they are used for plugin discovery, metadata, and configuration.

## Further your understanding

- Do you define any annotation-based plugins in your custom code? How would you go about converting them to use PHP attributes?

## Additional resources

- [Attributes](https://www.php.net/manual/en/language.attributes.php) (php.net)
- [Attribute based plugins](https://www.drupal.org/docs/drupal-apis/plugin-api/attribute-based-plugins) (Drupal.org)
- [Annotations](https://drupalize.me/tutorial/annotations) (Drupalize.Me)
- [PHP Attributes for Drupal Plugins](https://drupalize.me/blog/php-attributes-drupal-plugins) (Drupalize.Me)
- [Implement a Plugin Using PHP Attributes](https://drupalize.me/tutorial/implement-plugin-using-php-attributes?p=2765) (Drupalize.Me)
- Change record: [Plugins converted from Annotations to Attributes in 11.2.0](https://www.drupal.org/node/3505424) (Drupal.org)
- Change record: [Plugins converted from Annotations to Attributes in 11.1.0](https://www.drupal.org/node/3505422) (Drupal.org)
- Change record: [Plugins converted from Annotations to Attributes in 10.3.0](https://www.drupal.org/node/3229001) (Drupal.org)
- Change record: [Tests with PHPUnit 10 attributes are now supported](https://www.drupal.org/node/3447698) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[An Introduction to YAML](/tutorial/introduction-yaml?p=3292)

Next
[Annotations](/tutorial/annotations?p=3292)

Clear History

Ask Drupalize.Me AI

close