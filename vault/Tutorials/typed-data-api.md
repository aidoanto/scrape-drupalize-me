---
title: "Typed Data API"
url: "https://drupalize.me/tutorial/typed-data-api?p=2607"
guide: "[[work-data-modules]]"
---

# Typed Data API

## Content

The Typed Data API in Drupal helps add additional functionality to PHP's built-in data types, making working with data in Drupal much more predictable. It allows code to make intelligent guesses about the type of data that a field on an entity contains. For example, differentiating between a string of text and a string of text that represents a URL.

In this tutorial, we'll:

- Look at the 3 main types of typed data in Drupal: primitives, complex data, and lists.
- See how different data types and definitions are defined, and show how to define your own data type.
- Look at the interfaces provided by each data type to see some of the benefits of adding this abstraction layer.

By the end of this tutorial, you should have a better understanding of what the Typed Data API is, where you'll most likely encounter it, and how to use it in your code.

## Goal

Understand why Drupal has a Typed Data API and how its main pieces interact to create consistency.

## Prerequisites

- Understanding Drupal's plugin system, starting with [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins)
- [PHP Attributes](https://drupalize.me/tutorial/php-attributes)

## So, why Typed Data?

Unlike other programming languages, PHP is loosely typed. This means there are no consistent native mechanisms for knowing whether a piece of data is an integer, string, date, etc. To determine which type of data you're working with, you can use `gettype()`, but to do anything useful, you'd also need to know about a variety of helper functions (`is_string()`, `is_int()`, `is_object()`).

Drupal's Typed Data system provides a consistent mechanism for declaring and defining various types (of varying complexity). Using the Typed Data API lets developers use one set of functions to understand the data they are working with, get and set values, and perform validation. It also saves you from redundant type checking or memorizing several different functions that depend on a particular data type. In short, it provides a mechanism for describing data and a uniform interface for interacting with that data.

One of the main areas where this functionality is used by Drupal core is the (un)serialization of JSON. Since Typed Data makes Drupal aware of an object's implementation details, it can work with that data without custom code for each specific object.

## Typed Data in Drupal

There are a few different elements that come together to create Drupal's Typed Data system. Each data type is a plugin implementation. The plugins that implement typed data are managed by a service called the `typed_data_manager`. Each one of these typed data objects encapsulates the actual data, some metadata, and [provides a unified mechanism for validation](https://drupalize.me/tutorial/entity-validation-api). While typed data gives us a unified method of getting, setting, and validating values, the metadata that is available from a typed data object depends on something called the data definition. The class that is used to provide the data definition is specified for every data type.

The data types provided by core can be found in */core/lib/Drupal/Core/TypedData/Plugin/DataType*. Let's take a look at the code that describes the email data type. This data type is specified by a `\Drupal\Core\TypedData\Attribute\DataType` attribute and a class in the file `Email.php` in this directory.

```
namespace Drupal\Core\TypedData\Plugin\DataType;

use Drupal\Core\StringTranslation\TranslatableMarkup;
use Drupal\Core\TypedData\Attribute\DataType;
use Drupal\Core\TypedData\Type\StringInterface;

/**
 * The Email data type.
 *
 * The plain value of Email is the email address represented as PHP string.
 */
#[DataType(
  id: "email",
  label: new TranslatableMarkup("Email"),
  constraints: ["Email" => []],
)]
class Email extends StringData implements StringInterface {}
```

The actual implementation class here isn't too interesting. The key thing to note here is the plugin attribute `DataType`. The data type defines an `id`, a `label`, and `constraints`. Data type attributes may also specify the class responsible for the data definition. This is especially common among the more complex typed data objects (like the `ItemList`). Depending on the implementation details, there may also be a related class in the `/core/lib/Drupal/Core/TypedData/Type` directory. For our `Email` example, it inherits from the `StringData` class (which in turn extends the `PrimitiveBase` data type).

Take a look at some of the other data types defined in this directory. Some of them have additional methods that add additional metadata to the typed data object. The `TimeSpan` data type in particular implements some of this additional functionality to allow the getting and setting of duration values.

Image

![Time Span UML](/sites/default/files/styles/max_800w/public/tutorials/images/typed_data_time_span.png?itok=8f5DrmsX)

As you become familiar with the different types of Typed Data, you might notice that there are 3 main building blocks: primitive, complex, and list data.

### Primitive data

Typed data that inherits from or extends the `PrimitiveBase` class in some way can be considered primitive data. The `Email` data type we looked at earlier falls into this category. Primitive data types are often just special cases of integers or strings. They are types of data that may have a particular format or specification, like an email or a URL, but they don't require much additional metadata or functionality.

Typed data that extends the primitive data type will have `getValue()` and `setValue()` methods for working with the values. There is also a `getDefinition()` method that can be used to retrieve additional information about the typed data you're working with.

### Complex data

Complex data represents data that contains additional named properties. These named properties can themselves represent typed data objects. Because of this, complex data types can be considered similar to a map or an associative array. Drupal's Field API uses complex data types to represent the data stored by field items. You can see the implementation details of this in the `FieldItemDataDefinition` class.

Complex typed data will have `get()` and `set()` methods.

### List data

The list data type represents ordered lists of items (all the same type). Since lists are ordered data, they can be used to sort and organize the items they contain. A list data type could be used to store the RGB values of a color. This data type would be composed of 3 integers, each between 0 and 255, that represent a red, green, or blue value.

In addition to the expected `get()` and `set()` methods, list-typed data will also have an `offsetGet()` method that helps us determine which position in the order a particular piece of data has.

## Using the Typed Data Manager

Once we have described our Typed Data to Drupal, we can then take advantage of the unified interface we've mentioned for interacting with it. Let's say we'd like to use the Serialization API to return some JSON to a web service. Without the Typed Data API, we'd have to write code that knows how to encode JSON, format strings, and iterate over potentially complex objects. Thanks to the Typed Data definitions, Drupal knows how to return values based on the particular data type we're working with.

```
// Serialize Email Typed Data into JSON.
$listDefinition = \Drupal::typedDataManager()->createListDataDefinition('email');

$list = \Drupal::typedDataManger()->create($listDefinition, ['[email protected]', '[email protected]', '[email protected]']);
// *Note*: This assumes we have the serialization module enabled!
$serializer = \Drupal::service('serializer');

var_dump($serializer->serialize($list, 'json'));
```

Image

![Serialized Typed Data](/sites/default/files/styles/max_800w/public/tutorials/images/typed_data_serialization.png?itok=wgJLesJD)

## Recap

In this tutorial, we saw how Drupal used the Typed Data API to provide a unified interface for interacting with different types of data objects. Using typed data, we can rely on getting, setting, and validating values without worrying about the implementation details surrounding the type of data we're working with.

## Further your understanding

- What other types of Typed Data are provided by Drupal core? Can you think of another data type that would be useful to add?
- How would you go about using Typed Data in your code?

## Additional resources

- [The Typed Data API, by example](https://mglaman.dev/blog/typed-data-api-example) (mglaman.dev)
- [Typed Data API](https://api.drupal.org/api/drupal/core%21core.api.php/group/typed_data) (Drupal.org)
- [Typed Data API handbook pages](https://www.drupal.org/docs/drupal-apis/typed-data-api) (Drupal.org)
- [Understanding Drupal's data model](https://www.drupal.org/node/1795854) (Drupal.org)
- [Examples' project Field Example module](https://git.drupalcode.org/project/examples/-/tree/3.x/modules/field_example) (drupalcode.org)
- [Change record: Configuration entities are now supported by the typed data system](https://www.drupal.org/node/2954182) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Entity Access Control](/tutorial/entity-access-control?p=2607)

Clear History

Ask Drupalize.Me AI

close