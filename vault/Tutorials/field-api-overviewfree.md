---
title: "Field API Overviewfree"
url: "https://drupalize.me/tutorial/field-api-overview?p=2628"
guide: "[[work-data-modules]]"
order: 14
---

# Field API Overviewfree

## Content

If you've ever created or edited a piece of content on a Drupal site you have already interacted with the Field API. The Field module (along with its user interface counterpart) is responsible for providing the forms and data components used to build up the content model that make up a Drupal site. Understanding how Drupal fields work and how they're constructed via the Field API is an important part of understanding how Drupal works.

In this tutorial, we're going to look at the main components that make up the Field API at a high level. We'll see how the Field UI module exposes the field types included in core. We'll also look at the three main pieces that compose fields: types, widgets and formatters.

## Goal

Be able to explain at a high-level how field types, field widgets, and field formatters are defined in Drupal's Field API.

## Prerequisites

- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins)
- [PHP Attributes](https://drupalize.me/tutorial/php-attributes)
- [Plugin Discovery](https://drupalize.me/tutorial/plugin-discovery)

## Field Types

If you've ever visited the content administration screen of a Drupal site (*admin/content*) or the content type administration screen (*admin/structure/content*) you've seen the by-products of the Field API. While the entity system and the node module are responsible for defining the content type system, it is the Field API that is responsible for defining the individual components that make each content type unique. These individual components are called *fields*. You see Drupal's fields in action every time you create or edit a piece of content. Both the title and body fields of every node form are there because of Field API. Because the standard Drupal installation profile also enables the Field UI module, you can visit the content type administration screen to see this in action (*admin/structure/content*).

From this screen you're able to further examine the field configuration of a particular content type. The screenshot below is of the field management page for the Article content type provided by core.

Image

![Article field configuration settings](../assets/images/field_configuration.png)

From this page you can either add new fields or edit the configuration of those that already exist. Core modules that implement the Field API hooks provide us with a variety of data types out of the box, including:

- boolean
- date
- email
- link
- number (integer, float, decimal)
- file
- image
- text (plain, formatted, long with summary)

Using the field UI to configure the variety of settings provided by core is often enough to develop a complex data model. When the existing field types don't provide the functionality your project requires, the Field API allows developers to interact with existing field types or create their own from scratch.

## Primary components of the Field API

In constructing a custom field type, there are three main components that collectively make up fields: *types*, *widgets*, and *formatters*. All three are types of plugins and are initially specified by creating an [attribute-based plugin](https://drupalize.me/tutorial/implement-plugin-using-php-attributes).

### Types

*Field types* enable you to store different types of data. You describe, define, and expose a field type to Drupal via a `FieldType` attribute. We'll go into each of these attributes in more depth in separate tutorials. The `\Drupal\Core\Field\Attribute\FieldType` attribute that defines the boolean field type can be found in */core/lib/Drupal/Core/Field/Plugin/Field/FieldType/BooleanItem.php*. It provides a unique id as well as a human-readable label and description.

- Learn more about field types in our [Field Types tutorial](https://drupalize.me/tutorial/field-types).

### Widgets

Once we have our field type defined we need to define the *field widget*. Field widgets help determine how Drupal should render the field on the edit form. They are specified with a `\Drupal\Core\Field\Attribute\FieldWidget` attribute. The widget for the boolean field can be found in */core/lib/Drupal/Core/Field/Plugin/Field/FieldWidget/BooleanCheckboxWidget.php*.
Again, this attribute provides a unique id as well as a human-readable label. It also provides metadata about which field types it supports and whether it allows multiple values. Notice how the id of this attribute matches the *default\_widget* specified by the field type.

- Learn more about field widgets in our [Field Widgets tutorial](https://drupalize.me/tutorial/field-widgets).

### Formatters

The last main component to Field API is a *field formatter*. Field formatters provide the code responsible for the final rendered output of the field for the end user. These are specified by a `\Drupal\Core\Field\Attribute\FieldFormatter` attribute. The formatter for the boolean field can be found in */core/lib/Drupal/Core/Field/Plugin/Field/FieldFormatter/BooleanFormatter.php*. By now this pattern should be quite familiar. The formatter attribute also provides a unique id and human-readable label. Like the widget, it also includes a list of supported field types.

- Learn more about field formatters in our [Field Formatters tutorial](https://drupalize.me/tutorial/field-formatters).

While attributes alone aren't enough to create a new field from scratch, understanding these plugins can help us find and identify fields, widgets and formatters provided by our codebase.

## Recap

With an understanding of how the field type, widget and formatter fit together, we're well on our way to understanding how the Field API in Drupal works to provide support for various types of data structures. In this tutorial we took a brief look at the three main components that make up a field definition in Drupal and the plugins that are required to define them.

## Further your understanding

- Can you locate the type, widget and formatter plugins for the Email field?
- Based on what you already know about attributes, can you write a type, widget or formatter attribute from scratch?
- From what you know after reading the [Discover Existing Plugin Types](https://drupalize.me/tutorial/discover-existing-plugin-types) tutorial can you find a list of the type, widget and formatter plugins provided by Drupal core?

## Additional resources

- [PHP Attributes](https://drupalize.me/tutorial/php-attributes) (Drupalize.Me)
- [Discover Existing Plugin Types](https://drupalize.me/tutorial/discover-existing-plugin-types) (Drupalize.Me)
- [Drupal User Guide: Chapter 6 Setting Up Content Structure](https://drupalize.me/series/user-guide/content-structure-chapter) (Drupalize.Me)
- [Working with content types and fields (Drupal 7 and later)](https://www.drupal.org/docs/7/nodes-content-types-and-fields/working-with-content-types-and-fields-drupal-7-and-later) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Field Types](/tutorial/field-types?p=2628)

Clear History

Ask Drupalize.Me AI

close