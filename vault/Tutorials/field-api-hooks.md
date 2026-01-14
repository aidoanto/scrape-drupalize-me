---
title: "Field API Hooks"
url: "https://drupalize.me/tutorial/field-api-hooks?p=2628"
guide: "[[work-data-modules]]"
order: 19
---

# Field API Hooks

## Content

Drupal's Field API specifies the implementation details for field types, widgets and formatters. It also provides several hooks that allow custom code to alter these implementation details. In this tutorial we'll take a look at these Field API hooks and see how they can be used to change field types, widgets and formatters.

By the end of this lesson, you should be able to:

- Identify existing Field API hooks for manipulating field behavior
- Understand the proper method for changing the behavior of a field type, widget or formatter
- Know where to find the documentation for these API functions, and how to find their implementations

## Goal

Find and implement appropriate hooks to alter existing field types, field widgets, or field formatters.

## Prerequisites

- [Field API Overview](https://drupalize.me/tutorial/field-api-overview)
- [What Are Hooks?](https://drupalize.me/tutorial/what-are-hooks)
- [Implement Any Hook](https://drupalize.me/tutorial/implement-any-hook)
- [Discover Existing Hooks](https://drupalize.me/tutorial/discover-existing-hooks)

## Where to find Field API hooks

Drupal convention specifies that each subsystem, or module, that provides an API should include a *MODULE.api.php* file in its root directory with documentation outlining the hooks it provides. The Field API is no different. This documentation file can be found bundled with the Field module in */core/modules/field/field.api.php*. This file includes code comments that outline the major pieces that make up the field system. It points to the classes and plugin types that define field types, widgets and formatters. It then provides an example implementation of each of the hooks invoked by the field system which allow us to manipulate the classes providing functionality from other modules. Let's take a look at each of these in turn starting with field types.

## Change existing field types

Field API provides a single hook that enables the modification of basic field information, [`hook_field_info_alter`](https://api.drupal.org/api/drupal/core%21modules%21field%21field.api.php/function/hook_field_info_alter). This field allows us to alter any of the information gathered by Drupal's plugin system to change the basic behavior of a field. Using this hook we can change any of the classes responsible for implementing the field. It's also possible to change the label, id, description or any other metadata associated with a field type.

```
/**
 * Perform alterations on Field API field types.
 *
 * @param $info
 *   Array of information on field types as collected by the "field type" plugin
 *   manager.
 */
function hook_field_info_alter(&$info) {
  // Change the default widget for fields of type 'foo'.
  if (isset($info['foo'])) {
    $info['foo']['default widget'] = 'mymodule_widget';
  }
}
```

## Modify existing field widgets

In the example implementation of `hook_field_info_alter` above we can see a module changing the default widget used for a particular field type. What if instead of changing the default widget we just want to modify the behavior of an existing widget? Thankfully, the Field API provides [several hooks](https://api.drupal.org/api/drupal/core%21modules%21field%21field.api.php/group/field_widget) for doing just that. There are two primary hooks for working with field widgets: `hook_field_widget_info_alter` and `hook_field_widget_form_alter`.

Much like the field info hook we've already seen, [`hook_field_widget_info_alter`](https://api.drupal.org/api/drupal/core%21modules%21field%21field.api.php/function/hook_field_widget_info_alter) allows us to change any of the implementation details of field widgets. Drupal's [plugin discovery](https://drupalize.me/tutorial/plugin-discovery) mechanism gathers the information for each `FieldWidget` attribute and passes it as an array to this alter hook.

In the following example implementation, we're adding support for the `options_select` widget to a new field type.

```
function hook_field_widget_info_alter(array &$info) {
  // Let a new field type re-use an existing widget.
  $info['options_select']['field_types'][] = 'my_field_type';
}
```

Instead of altering the field widget implementation information we may find ourselves needing to change the actual form that generates the field widget. In that case we can make use of [`hook_field_widget_complete_form_alter`](https://api.drupal.org/api/drupal/core!modules!field!field.api.php/function/hook_field_widget_complete_form_alter/).

**Note**: The hooks, `hook_field_widget_form_alter` (`hook_field_widget_WIDGET_TYPE_form_alter`), have been marked as deprecated and were removed in Drupal 10 ([change record](https://www.drupal.org/node/3180429)).

```
/**
 * Alter the complete form for field widgets provided by other modules.
 *
 * @param $field_widget_complete_form
 *   The field widget form element as constructed by
 *   \Drupal\Core\Field\WidgetBaseInterface::form().
 * @param $form_state
 *   The current state of the form.
 * @param $context
 *   An associative array containing the following key-value pairs:
 *   - form: The form structure to which widgets are being attached. This may be
 *     a full form structure, or a sub-element of a larger form.
 *   - widget: The widget plugin instance.
 *   - items: The field values, as a
 *     \Drupal\Core\Field\FieldItemListInterface object.
 *   - delta: The order of this item in the array of subelements (0, 1, 2, etc).
 *   - default: A boolean indicating whether the form is being shown as a dummy
 *     form to set default values.
 *
 * @see \Drupal\Core\Field\WidgetBaseInterface::form()
 * @see \Drupal\Core\Field\WidgetBase::form()
 * @see hook_field_widget_complete_WIDGET_TYPE_form_alter()
 * @see https://www.drupal.org/node/3180429
 */
function hook_field_widget_complete_form_alter(&$field_widget_complete_form, \Drupal\Core\Form\FormStateInterface $form_state, $context) {
  $field_widget_complete_form['#attributes']['class'][] = 'my-class';
}
```

While this technique works for altering the field widget form it requires first checking to make sure that the field type matches a particular widget. Once you know the id of the field widget you need to alter you can also use the more specific [`hook_field_widget_complete_WIDGET_TYPE_form_alter`](https://api.drupal.org/api/drupal/core!modules!field!field.api.php/function/hook_field_widget_complete_WIDGET_TYPE_form_alter/) function. This allows the encapsulation of code that modifies a particular type of widget.

```
/**
 * Alter the complete form for a specific widget provided by other modules.
 *
 * Modules can implement hook_field_widget_complete_WIDGET_TYPE_form_alter()
 * to modify a specific widget form, rather than using
 * hook_field_widget_complete_form_alter() and checking the widget type.
 *
 * @param $field_widget_complete_form
 *   The field widget form element as constructed by
 *   \Drupal\Core\Field\WidgetBaseInterface::form().
 * @param $form_state
 *   The current state of the form.
 * @param $context
 *   An associative array containing the following key-value pairs:
 *   - form: The form structure to which widgets are being attached. This may be
 *     a full form structure, or a sub-element of a larger form.
 *   - widget: The widget plugin instance.
 *   - items: The field values, as a
 *     \Drupal\Core\Field\FieldItemListInterface object.
 *   - delta: The order of this item in the array of subelements (0, 1, 2, etc).
 *   - default: A boolean indicating whether the form is being shown as a dummy
 *     form to set default values.
 *
 * @see \Drupal\Core\Field\WidgetBaseInterface::form()
 * @see \Drupal\Core\Field\WidgetBase::form()
 * @see hook_field_widget_complete_form_alter()
 * @see https://www.drupal.org/node/3180429
 */
function hook_field_widget_complete_WIDGET_TYPE_form_alter(&$field_widget_complete_form, \Drupal\Core\Form\FormStateInterface $form_state, $context) {
  $field_widget_complete_form['#attributes']['class'][] = 'my-class';
}
```

## Alter existing field formatters

It's probably not surprising that the Field API also provides hooks for [altering the behavior of field formatters](https://api.drupal.org/api/drupal/core%21modules%21field%21field.api.php/group/field_formatter). In particular there is one main hook for changing formatter behavior: [`hook_field_formatter_info_alter`](https://api.drupal.org/api/drupal/core%21modules%21field%21field.api.php/function/hook_field_formatter_info_alter). This hook also gathers the information provided by `FieldFormatter` plugins and allows custom code to make changes to the implementation details. In the example below we are allowing a new field type to re-use an existing field formatter.

```
/**
 * @defgroup field_formatter Field Formatter API
 * @{
 * Define Field API formatter types.
 *
 * Field API formatters specify how fields are displayed when the entity to
 * which the field is attached is displayed. Fields of a given
 * @link field_types field type @endlink may be displayed using more than one
 * formatter. In this case, the Field UI module allows the site builder to
 * choose which formatter to use.
 *
 * Formatters are Plugins managed by the
 * \Drupal\Core\Field\FormatterPluginManager class. A formatter is a plugin
 * attributed with class \Drupal\Core\Field\Attribute\FieldFormatter that
 * implements \Drupal\Core\Field\FormatterInterface (in most cases, by
 * subclassing \Drupal\Core\Field\FormatterBase). Formatter plugins need to be
 * in the namespace \Drupal\{your_module}\Plugin\Field\FieldFormatter.
 *
 * @see field
 * @see field_types
 * @see field_widget
 * @see plugin_api
 */

/**
 * Perform alterations on Field API formatter types.
 *
 * @param array $info
 *   An array of information on existing formatter types, as collected by the
 *   plugin discovery mechanism.
 */
function hook_field_formatter_info_alter(array &$info) {
  // Let a new field type re-use an existing formatter.
  $info['text_default']['field_types'][] = 'my_field_type';
}
```

## Recap

In this tutorial, we looked at the documentation provided by the Field module about the API it provides for manipulating the field types, widgets and formatters provided by other modules. Making use of this API requires the implementation of hooks in a custom module. We looked at the documentation of, and example implementations for, these hooks from the */core/modules/field/field.api.php* file.

## Further your understanding

- The only use of `hook_field_info_alter` provides support for content translation. Can you find this implementation?
- One of the Field API hooks we didn't examine in detail allows us to respond to the deletion of a field. Which hook is this?

## Additional resources

- [Plugin Discovery](https://drupalize.me/tutorial/plugin-discovery) (Drupalize.Me)
- [Field API](https://api.drupal.org/api/drupal/core%21modules%21field%21field.module/group/field) (Drupal.org)
- [Field Types API](https://api.drupal.org/api/drupal/core%21modules%21field%21field.api.php/group/field_types) (Drupal.org)
- [Field Widget API](https://api.drupal.org/api/drupal/core%21modules%21field%21field.api.php/group/field_widget) (Drupal.org)
- [Field Formatter API](https://api.drupal.org/api/drupal/core%21modules%21field%21field.api.php/group/field_formatter) (Drupal.org)
- Change record: [Streamline field widget hooks](https://www.drupal.org/node/3180429)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Define a Field Formatter Plugin](/tutorial/define-field-formatter-plugin?p=2628)

Clear History

Ask Drupalize.Me AI

close