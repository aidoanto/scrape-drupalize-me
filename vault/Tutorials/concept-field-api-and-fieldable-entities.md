---
title: "Concept: Field API and Fieldable Entities"
url: "https://drupalize.me/tutorial/concept-field-api-and-fieldable-entities?p=3243"
guide: "[[drupal-module-developer-guide]]"
---

# Concept: Field API and Fieldable Entities

## Content

In Drupal, content entities can have fields. Field data is entered using widgets and displayed with formatters. The Field API provides developers with means to customize fields, widgets, and formatters. Which gives site builders tools to build flexible, extensible sites using customized data models.

In this tutorial, we'll:

- Learn what it means for an entity to be *fieldable*.
- Define what field types, widgets, and formatters are and give examples of each.
- Explore the differences between base fields and user-defined fields.
- Define the concept of field instances.

By the end of this tutorial you should be able to define the main components of the Field API and understand how developers leverage the Field API to alter and enhance Drupal.

## Goal

Explain the role of the Field API and fieldable entities for module developers.

## Prerequisites

- [Concept: Data Types in Drupal](https://drupalize.me/tutorial/concept-data-types-drupal)
- [Concept: Entity API and Data Storage](https://drupalize.me/tutorial/concept-entity-api-and-data-storage)
- [2.3. Concept: Content Entities and Fields](https://drupalize.me/tutorial/user-guide/planning-data-types) (Drupal User Guide)

## Fieldable entities

A *fieldable entity* allows a user to add and define fields to a content entity in order to change a Drupal site's content structure to suit a specific purpose. While some entities have a fixed structure, fieldable entities empower users to define custom data models by adding fields. This flexibility allows you to define anything from blog posts to complex user profiles.

## Field API components

The Field API consists of 3 main components, all of which are defined by plugins, with individual instances configurable by an administrative user.

- **Field types**: Definition of the type of data to collect, and how it should be stored. For example, a binary file stored on disk and a path to the file stored in the database.
- **Field widgets**: Determine how Drupal should render the field as a form element. They are responsible for the UI that someone interacts with to enter data. For example, an Ajax-enabled file upload widget.
- **Field formatters**: Determine how the data is displayed. For example, an image rendered at 3 different resolutions using a `<picture>` tag.

Modules can define new types, widgets, and formatters in order to provide site builders with new options to choose from when configuring the fieldable entities on their site. Using the Field API as a wrapper around your custom features is a good way to provide flexibility and reusability.

Also keep in mind that you can define new widgets, or formatters, for existing types. An Amazon ASIN product number is technically a string and could be stored as a text field. A custom formatter could make an API call to AWS to get and display product details in place of the ASIN string in the text field. And then site builder could configure that field to display it as a product widget on a public-facing page, or a standard string of text in a Views-generated report.

## Base fields versus user-defined fields

In order to standardize the API for managing field data associated with entities, the entity API allows for *base fields* and *user-defined fields*. Both use the same field types, widgets, and formatters. The difference is in how they are configured and attached to an entity type.

### Base fields

Base fields are defined in code as part of the entity type plugin definition. They can not be removed from the entity type. They define the field name, type, widget, and formatter. Though widgets and formatters can be optionally marked as configurable.

Base fields store data that is required for every entity of the given type to have in order for other parts of the system to be able to make assumptions about their existence, and to hard code logic related to their values.

The Node entity type's *title*, *authored by*, *status*, and *created date* fields are all examples of base fields.

### User-defined fields

User-defined fields are fields added to a fieldable entity type via the UI.

- Their definition is stored as configuration
- Their presence, name, and exact configuration, are specific to the site.

Module developers should be cautious about writing code that makes assumptions about any of these things. For example, 2 different site builders could create 2 different event content types: one with an `event_start_date` field and another with a `start_date` field. As a module developer, you would want to be careful about writing any code that makes assumptions like `$node->get('start_date');`. Though there are use cases which we'll discuss in [Add Fields to the Vendor Content Type](https://drupalize.me/tutorial/add-fields-vendor-content-type).

## Field instances

In Drupal's Field API, field instances refer to the specific application of a field to an entity bundle. While a field defines a type of data that can be attached to an entity (like a text field, image field, or date field), a field instance is the application of that field within the context of a particular entity type or bundle.

Each field instance can have its own set of configurations, such as label, description, required status, and settings for how the field data should be displayed and stored. These settings can vary from one instance of the field to another, even if they are instances of the same field type. For example, an image field on an "Article" bundle might be configured to allow multiple images and display them in a carousel, while the same image field on a "Product" bundle might be limited to a single image with a different display format.

Field instances enable Drupal site builders to use the same field type across different entities and bundles in a flexible way, meeting the needs of each specific context within the site.

## Working with field values

Interacting with field values typically involves accessing the field via the entity it's attached to. Here are some common examples:

### Get the field instance

Get the field instance itself as an implementation of `\Drupal\Core\Field\FieldItemListInterface`. This gives you access to both the content of the field, and the definition of the field.

```
$field = $node->get('field_custom_text');
// You can also use the magic __get() and __set() methods provided by
// ContentEntityBase as shorthand for the above example.
$field = $node->field_custom_text;
```

### Check if a field is empty

```
$node->get('field_custom_text')->isEmpty();
```

### Access the raw value of a field

```
$value = $node->get('field_custom_text')->value;
```

### Traverse an entity reference field

```
$author_name = $node->uid->entity->name->value;
```

## Recap

In this tutorial we learned about the 3 main components of the Field API; types, widgets, and formatters. And the differences between base fields, and user-defined fields. We also looked at some examples of working with field data in code using the Field API.

## Further your understanding

- Give an example of an essential data point that would require the use of base fields on a custom entity type.
- What is an example use case for defining a new field widget plugin for an existing field type?

## Additional resources

- [Field API Overview](https://drupalize.me/tutorial/field-api-overview) (Drupalize.Me)
- [Field Types](https://drupalize.me/tutorial/field-types) (Drupalize.Me)
- [Field Widgets](https://drupalize.me/tutorial/field-widgets) (Drupalize.Me)
- [Field Formatters](https://drupalize.me/tutorial/field-formatters) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Entity API and Data Storage](/tutorial/concept-entity-api-and-data-storage?p=3243)

Next
[Add Fields to the Vendor Content Type](/tutorial/add-fields-vendor-content-type?p=3243)

Clear History

Ask Drupalize.Me AI

close