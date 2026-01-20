---
title: "Field Formatters"
url: "https://drupalize.me/tutorial/field-formatters?p=2628"
guide: "[[work-data-modules]]"
order: 17
---

# Field Formatters

## Content

Of the 3 main components of the field system -- types, widgets and formatters -- only 1 has an impact on the actual display of content for end users: field formatters. Field formatters are responsible for taking the data stored by a field and transforming it into the markup that is sent to the browser when an end user views your site.

In this tutorial we'll:

- Look at the role field formatters play in the Field API
- Identify the main components that make up a field formatter

By the end of this tutorial you should be able to define the role of a field formatter plugin.

## Goal

Explain what field formatters are and how they are used by the Field API.

## Prerequisites

- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins)
- [PHP Attributes](https://drupalize.me/tutorial/php-attributes)
- [Discover Existing Plugin Types](https://drupalize.me/tutorial/discover-existing-plugin-types)
- [Configuration Data Types](https://drupalize.me/tutorial/configuration-data-types)
- [Field API Overview](https://drupalize.me/tutorial/field-api-overview)

## Using field formatters to display content

If you want to learn how to use or configure an existing field formatter to modify the way a field looks when displayed see [6.11. Changing Content Display](https://drupalize.me/tutorial/user-guide/structure-content-display).

## What are field formatters?

Field formatters specify how to display a field's content when the entity to which the field is attached is displayed. For example, long text fields can be displayed trimmed or full-length, and taxonomy term reference fields can be displayed as plain text or linked to the taxonomy term page. Users configure field formatters via the *Manage display* page of fieldable entity types.

Example:

Image

![Screenshot of the manage display page for an article content type showing an image field with the field formatter settings UI open.](../assets/images/field_formatter_ui_example.png)

Field formatters are specific to [field types](https://drupalize.me/tutorial/field-types). Though many work with multiple field types. And a field type can have multiple formatters. Though only one is active at a time per view mode.

An entity reference field, for example, can be configured to display the title of the referenced entity as a link in the *teaser* view mode. And as a rendered entity in the *full* [view mode](https://drupalize.me/tutorial/user-guide/structure-view-modes).

Formatters are configured for each view mode in each entity type where a field is used.

Field formatters are [plugins](https://drupalize.me/tutorial/what-are-plugins), with an `\Drupal\Core\Field\Attribute\FieldFormatter` [attribute](https://drupalize.me/tutorial/php-attributes), that implement `\Drupal\Core\Field\FormatterInterface`. They generally extend the `\Drupal\Core\Field\FormatterBase` base class. The custom code in each formatter is responsible for taking the data loaded from storage by the associated field type and transforming it into a [renderable array](https://drupalize.me/tutorial/what-are-render-arrays).

Field formatters can have configuration settings which allow an administrator to modify the output. For example, choosing which image style to use when displaying an image, or setting the number of characters to display for a trimmed summary.

Much of what field formatters accomplish can also be done [via a theme](https://drupalize.me/tutorial/what-are-template-files). The benefit of using a field formatter to modify output instead of doing so via the theme layer is a more generic solution that can be easily reused across multiple fields. For example, you could [create a Twig template file](https://drupalize.me/tutorial/override-template-file) to output a list of taxonomy terms separated by a comma instead of as an unordered list. But then if you want to apply that same formatting to another taxonomy field you would need to duplicate the template. Or, you could [author a custom formatter plugin](https://drupalize.me/tutorial/define-field-formatter-plugin) and reuse it for both fields.

## Field formatters provided by Drupal core

Core provides formatters for all the core provided field types. Often, custom formatters can extend one of these existing core field formatter plugins as a starting point rather than implementing one from scratch.

You can get a list of all the field formatters for any site by executing the following [Drush](https://drupalize.me/tutorial/what-drush-0) command:

```
drush ev "dump(\Drupal::service('plugin.manager.field.formatter')->getDefinitions())"
```

This will generate output like below from which you can figure out the plugin ID, the class that provides it, and the types of fields it works with.

Example:

```
^ array:47 [
  // ... <snip> ...
  "datetime_time_ago" => array:6 [
    "field_types" => array:1 [
      0 => "datetime"
    ]
    "id" => "datetime_time_ago"
    "label" => Drupal\Core\StringTranslation\TranslatableMarkup^ {#885
      #string: "Time ago"
      #arguments: []
      #translatedMarkup: null
      #options: []
      #stringTranslation: null
    }
    "class" => "Drupal\datetime\Plugin\Field\FieldFormatter\DateTimeTimeAgoFormatter"
    "provider" => "datetime"
  ]
  "field_example_color_background" => array:6 [
    "field_types" => array:1 [
      0 => "field_example_rgb"
    ]
    "id" => "field_example_color_background"
    "label" => Drupal\Core\StringTranslation\TranslatableMarkup^ {#884
      #string: "Change the background of the output text"
      #arguments: []
      #translatedMarkup: null
      #options: []
      #stringTranslation: null
    }
    "class" => "Drupal\field_example\Plugin\Field\FieldFormatter\ColorBackgroundFormatter"
    "provider" => "field_example"
  ]
  // ... <snip> ...
];
```

The core-provided plugins are great examples of how to author a formatter. They also provide code you can extend to create your own custom plugin, if what you need is a variation of a core-provided field formatter.

## Recap

In this tutorial, we looked at how field formatter plugins are defined and how they can be used to determine how data from fields is rendered. We learned how to specify `FieldFormatter` attributes for our plugins, and about the `FormatterInterface` interface required by field formatter implementations. Finally, we learned how to find the list of Drupal core-provided field formatter plugins using Drush.

## Further your understanding

- Where are field formatters used?
- Can you give an example of a contributed module that provides a custom field formatter?
- Learn how to [Define a Field Formatter Plugin](https://drupalize.me/tutorial/define-field-formatter-plugin).

## Additional resources

- [6.10. Concept: View Modes and Formatters](https://drupalize.me/tutorial/user-guide/structure-view-modes)
- [6.11. Changing Content Display](https://drupalize.me/tutorial/user-guide/structure-content-display)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Field Widgets](/tutorial/field-widgets?p=2628)

Next
[Define a Field Formatter Plugin](/tutorial/define-field-formatter-plugin?p=2628)

Clear History

Ask Drupalize.Me AI

close