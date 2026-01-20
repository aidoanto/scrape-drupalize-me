---
title: "Field Types"
url: "https://drupalize.me/tutorial/field-types?p=2628"
guide: "[[work-data-modules]]"
order: 15
---

# Field Types

## Content

Drupal's field system provides us with a flexible system of adding different types of discrete data to content types. This enables us to create rich content models. The Field API allows us to define these distinct field types by creating a new plugin. These plugins specify a `FieldType` attribute. In this tutorial, we'll look at these attributes in detail. We'll look at the implementations of field types from Drupal core. Also, we'll see what a new custom field type would look like.

By the end of this tutorial, you should be able to:

- Understand how field type definitions are created and exposed to Drupal
- Identify the various field types provided by Drupal core
- Understand the requirements for providing a specification for a new field type

## Goal

Identify and locate in code Drupal's core field types. Following an example, provide in code a unique custom field type for your Drupal site.

## Prerequisites

- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins)
- [PHP Attributes](https://drupalize.me/tutorial/php-attributes)
- [Discover Existing Plugin Types](https://drupalize.me/tutorial/discover-existing-plugin-types)
- [Field API Overview](https://drupalize.me/tutorial/field-api-overview)

## Discover field types in a Drupal site

When learning a new Drupal subsystem, looking at the various implementations in core files is often a great way to get started. Trying to identify the field types provided by Drupal core can be done in a number of ways.

### Using the administrative UI

Probably the easiest method is to visit the module administration page at */admin/modules* and look under the *Field Types* group. Here is what that looks like out of the box with the standard installation profile:

Image

![Field type modules provided by Drupal core.](../assets/images/field_types.png)

### Using Drush and the command line

Drush provides the following command for getting info about field types:

```
drush field:types --format=list
```

Other valid formats include: `json`, `list`, `php`, `print-r`, `var_dump`, `var_export`, `yaml`

For example, here's the info you'll get about the `boolean` field type using `drush field:types --format=var_dump`:

```
"boolean" => array:5 [
      "id" => "boolean"
      "label" => "Boolean"
      "default_widget" => "boolean_checkbox"
      "default_formatter" => "boolean"
      "settings" => array:2 [
        "on_label" => Drupal\Core\StringTranslation\TranslatableMarkup^ {#3657}
        "off_label" => Drupal\Core\StringTranslation\TranslatableMarkup^ {#3658}
      ]
    ]
```

Since we know that field types are plugin types, you can use the techniques described in the tutorial, [Discover Existing Plugin Types](https://drupalize.me/tutorial/discover-existing-plugin-types) to find examples of field types in a Drupal site.

For example, when you run:

```
drush ev 'foreach (\Drupal::getContainer()->getServiceIds() as $id) { $a[$id] = is_object(\Drupal::service($id)) ? get_class(\Drupal::service($id)) : ""; } dump($a);' | grep plugin
```

You'll discover the name of the plugin manager service for field types: `plugin.manager.field.field_type`.

Which you can then use to find all instances:

```
drush ev "dump(\Drupal::service('plugin.manager.field.field_type')->getDefinitions())"
```

For example, here's the info you'll get about the `boolean` field type with the above command:

```
"boolean" => array:17 [
    "class" => "Drupal\Core\Field\Plugin\Field\FieldType\BooleanItem"
    "provider" => "core"
    "id" => "boolean"
    "label" => Drupal\Core\StringTranslation\TranslatableMarkup^ {#3590
      #string: "Boolean"
      #arguments: []
      #translatedMarkup: null
      #options: []
      #stringTranslation: null
    }
    "description" => Drupal\Core\StringTranslation\TranslatableMarkup^ {#3591
      #string: "Field to store a true or false value."
      #arguments: []
      #translatedMarkup: null
      #options: []
      #stringTranslation: null
    }
    "category" => "general"
    "weight" => 0
    "default_widget" => "boolean_checkbox"
    "default_formatter" => "boolean"
    "no_ui" => false
    "list_class" => "\Drupal\Core\Field\FieldItemList"
    "cardinality" => null
    "constraints" => []
    "config_dependencies" => []
    "column_groups" => []
    "serialized_property_names" => []
    "module" => null
  ]
```

## Core field types plugin classes

Out-of-the-box, Drupal provides many field types, located both in core and module-specific namespaces.

| Plugin ID | Plugin class |
| --- | --- |
| boolean | Drupal\Core\Field\Plugin\Field\FieldType\BooleanItem |
| changed | Drupal\Core\Field\Plugin\Field\FieldType\ChangedItem |
| comment | Drupal\comment\Plugin\Field\FieldType\CommentItem |
| created | Drupal\Core\Field\Plugin\Field\FieldType\CreatedItem |
| datetime | Drupal\datetime\Plugin\Field\FieldType\DateTimeItem |
| decimal | Drupal\Core\Field\Plugin\Field\FieldType\DecimalItem |
| email | Drupal\Core\Field\Plugin\Field\FieldType\EmailItem |
| entity\_reference | Drupal\Core\Field\Plugin\Field\FieldType\EntityReferenceItem |
| file | Drupal\file\Plugin\Field\FieldType\FileItem |
| float | Drupal\Core\Field\Plugin\Field\FieldType\FloatItem |
| image | Drupal\image\Plugin\Field\FieldType\ImageItem |
| integer | Drupal\Core\Field\Plugin\Field\FieldType\IntegerItem |
| language | Drupal\Core\Field\Plugin\Field\FieldType\LanguageItem |
| link | Drupal\link\Plugin\Field\FieldType\LinkItem |
| list\_float | Drupal\options\Plugin\Field\FieldType\ListFloatItem |
| list\_integer | Drupal\options\Plugin\Field\FieldType\ListIntegerItem |
| list\_string | Drupal\options\Plugin\Field\FieldType\ListStringItem |
| map | Drupal\Core\Field\Plugin\Field\FieldType\MapItem |
| password | Drupal\Core\Field\Plugin\Field\FieldType\PasswordItem |
| path | Drupal\path\Plugin\Field\FieldType\PathItem |
| string | Drupal\Core\Field\Plugin\Field\FieldType\StringItem |
| string\_long | Drupal\Core\Field\Plugin\Field\FieldType\StringLongItem |
| text | Drupal\text\Plugin\Field\FieldType\TextItem |
| text\_long | Drupal\text\Plugin\Field\FieldType\TextLongItem |
| text\_with\_summary | Drupal\text\Plugin\Field\FieldType\TextWithSummaryItem |
| timestamp | Drupal\Core\Field\Plugin\Field\FieldType\TimestampItem |
| uri | Drupal\Core\Field\Plugin\Field\FieldType\UriItem |
| uuid | Drupal\Core\Field\Plugin\Field\FieldType\UuidItem |

The best way to get a sense of what each of these field types do is to examine their code and to try adding them to a content type on a development site. Most field types are relatively straightforward to conceptualize. It's easy to imagine how an `image` field is different from an `email` field for example. However, it may not be obvious how `text_long` differs from `text_with_summary`. It's also worth looking at the three `list` field types to understand their differences.

We can identify these plugins as field types because each plugin class listed above is accompanied by a `FieldType` attribute. Let's look at the attribute for the boolean field in more detail. The `BooleanItem` class can be found in */core/lib/Drupal/Core/Field/Plugin/Field/FieldType/BooleanItem.php*.

```
/**
 * Defines the 'boolean' entity field type.
 */
#[FieldType(
  id: "boolean",
  label: new TranslatableMarkup("Boolean"),
  description: new TranslatableMarkup("Field to store a true or false value."),
  default_widget: "boolean_checkbox",
  default_formatter: "boolean",
)]
```

A `FieldType` attribute needs to provide a *unique id* for the field type, a *label* which is used in the user interface, and a *default widget* and *default formatter*. The *description* is optional and used primarily as help text.

## Create a custom field type

Occasionally, you may find yourself limited by what field types core provides, and you need to create your own custom field type. In order to do so, you will need to define a new field type plugin via a `FieldType` attribute.

Here's an example from the [Examples project's](https://www.drupal.org/project/examples) [Field Example module](https://git.drupalcode.org/project/examples/-/tree/4.0.x/modules/field_example), updated here to use attributes instead of annotations. This module provides a new RGB field type that gives users a variety of methods of storing an RGB color value. Locate the code that defines this field type plugin in */modules/examples/field\_example/src/Plugin/Field/FieldType/RbgItem.php*.

```
/**
 * Plugin implementation of the 'field_example_rgb' field type.
 */
#[FieldType(
  id: "field_example_rgb",
  label: new TranslatableMarkup("Example Color RGB"),
  description: new TranslatableMarkup("Demonstrates a field composed of an RGB color."),
  default_widget: "field_example_text",
  default_formatter: "field_example_simple_text",
  module: "field_example"
)]
```

The attribute that provides metadata for this field type plugin should accompany a class that implements the `FieldItemInterface` interface. Typically, this is done by extending the `FieldItemBase` class (as is done in this case).

You should be aware of a few especially important methods in a field type class. We can see these implemented in the `RgbItem` class.

The first is the `schema()` method. This is used to tell Drupal how to store the data for the custom field type. (You can read more about the types of possible data that can be used here in the [documentation for the Schema API on drupal.org](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Database%21database.api.php/group/schemaapi)). If your field involves complex configuration, or if you'd like your field settings to be exposed to the configuration management system, it's also important to create a `schema.yml` file. You can read more about [providing configuration schema metadata](https://www.drupal.org/docs/drupal-apis/configuration-api/configuration-schemametadata#use) here.

```
public static function schema(FieldStorageDefinitionInterface $field_definition) {
  return [
    'columns' => [
      'value' => [
        'type' => 'text',
        'size' => 'tiny',
        'not null' => FALSE,
      ],
    ],
  ];
}
```

Second is the `isEmpty()` method which helps Drupal determine whether the field is actually empty.

```
public function isEmpty() {
  $value = $this->get('value')->getValue();
  return $value === NULL || $value === '';
}
```

The last method implemented in our example code is the `propertyDefinitions` method. This is used to tell Drupal about the field's properties. In some cases, such as entity reference fields, the data stored in a field may represent a complex data structure. The field properties defined in this method create a map between the Typed Data definition for the data structure and human-readable labels that are used in the user interface. You can read more about [complex and computed field properties on drupal.org](https://www.drupal.org/docs/drupal-apis/entity-api/dynamicvirtual-field-values-using-computed-field-property-classes). In this example we're storing a single RGB value which will have the label "Hex value".

```
public static function propertyDefinitions(FieldStorageDefinitionInterface $field_definition) {
  $properties['value'] = DataDefinition::create('string')
    ->setLabel(t('Hex value'));

  return $properties;
}
```

With these key pieces in place we can see the new field type in action by adding it to a content type. If we want to add a background color field to the page content type we can navigate to *admin/structure/types/manage/page/fields* and click the **Add field** button.

Image

![RGB Field provided by the field example module](../assets/images/example_rgb_field.png)

## Recap

Drupal core provides several different types of fields out of the box. We can use Drush and other command-line tools to discover which field type plugins are already available and the classes that define their behavior. Each of these field type classes implements the `FieldItemInterface` interface and is associated with a `FieldType` attribute. Our field type implementation is also responsible for telling Drupal how to store our field values by implementing the `schema()` method in our plugin class.

## Further your understanding

- Can you find a field type provided by core that uses a schema that stores multiple values? What is the file naming convention for configuration schema files?
- What are the main reasons for choosing among the `list_float`, `list_integer` and `list_string` field types?
- Are there other methods from the `FieldItemInterface` interface that would be useful to override in our example?

## Additional resources

- [Field Types API](https://api.drupal.org/api/drupal/core%21modules%21field%21field.api.php/group/field_types) (Drupal.org)
- [Examples project field module](https://git.drupalcode.org/project/examples/-/tree/3.x/modules/field_example) (git.drupalcode.org)
- [Schema API](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Database%21database.api.php/group/schemaapi) (Drupal.org)
- [Configuration Data Types](https://drupalize.me/tutorial/configuration-data-types) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Field API Overview](/tutorial/field-api-overview?p=2628)

Next
[Field Widgets](/tutorial/field-widgets?p=2628)

Clear History

Ask Drupalize.Me AI

close