---
title: "Provide Default Values for Form Elements"
url: "https://drupalize.me/tutorial/provide-default-values-form-elements?p=2734"
guide: "[[develop-forms-drupal]]"
---

# Provide Default Values for Form Elements

## Content

Forms are used for both collecting new data, and editing existing data. In order to allow users to modify existing data you need to pre-populate the elements on the form with the data you previously stored.

In this tutorial we'll look at the ways in which forms can be pre-populated with existing data, including:

- Providing default values for form elements which a user can edit with the `#default_value` property
- The differences between the `#value` and `#default_value` properties

By the end of this tutorial you should know how to populate forms using existing data.

## Goal

Update the form created in [Define a New Form Controller and Route](https://drupalize.me/tutorial/define-new-form-controller-and-route) so that when a user enters a value into the title field and submits the form that value is pre-populated into the form field the next time they view the form.

## Prerequisites

- [Define a New Form Controller and Route](https://drupalize.me/tutorial/define-new-form-controller-and-route)
- [Add Input Elements to A Form](https://drupalize.me/tutorial/add-input-elements-form)
- [Process Submitted Form Data via Form Controller](https://drupalize.me/tutorial/process-submitted-form-data-form-controller)

## Editable values versus immutable values

When adding elements to a `$form` array there are two ways you can specify the value that will be displayed to the user. While they appear the same to the end user, they have very different effects on the form itself.

- `#default_value`: Using the default value property allows you to assign a value that will be pre-populated into the related input element and can be edited by the user. Any changes to the default value will be present when the form is validated and submitted.
- `#value`: Using the value property allows you to assign a value that will be pre-populated into the related input element, but the value cannot be changed by the user. When the form is validated and submitted, any user-entered input will be ignored in favor of whatever is in the `#value` property.

In most cases you'll likely want to use the `#default_value` property, especially if this data is being presented so that the user can edit it. The `#value` property is useful for things like a hidden form field whose value you don't want to change no matter what. The `form_build_token` and `form_build_id` elements are good examples. We want the values to be part of the POST data submitted by the form, so they are entered as hidden input fields and not just stored on the server behind the scene. However, we also need to ensure that those fields are not subject to local modification.

## Pre-populate a form field

### Retrieve the existing data

The first thing you'll need to do is retrieve the existing data that you want to use to pre-populate the form field. Depending on the complexity of the logic required to do so you can either write the code directly into your `buildForm()` method, or you can create a new method on the controller.

In our case, we'll retrieve the data from the temp store:

```
// Retrieve previously saved data from the tempstore if it exists.
$tempstore = \Drupal::service('user.private_tempstore')->get('form_api_example');
$title = $tempstore->get('title');
```

See [Process Submitted Form Data via Form Controller](https://drupalize.me/tutorial/process-submitted-form-data-form-controller) for an explanation of how this data was saved to the temp store previously.

### Set the `#default_value` property

All form elements support the `#default_value` property. You'll often see a ternary assignment used which assigns the property a value if the associated variable contains one, or sets it to an empty string if it does not.

Example:

```
// Retrieve previously saved data from the tempstore if it exists.
$tempstore = \Drupal::service('user.private_tempstore')->get('form_api_example');
$title = $tempstore->get('title');

$form['title'] = [
  '#type' => 'textfield',
  '#title' => $this->t('Title'),
  '#description' => $this->t('Title must be at least 5 characters in length.'),
  '#required' => TRUE,
  // If $title contains a non-falsy value use that, otherwise use an empty string.
  '#default_value' => $title ? $title : '',
];
```

Now, when someone visits the form, the **Title** textfield will be pre-populated with whatever data was stored in the *form\_api\_example.title* temporary storage.

## Hidden fields

Here's an example of a hidden field, with an immutable value. No matter what changes the user might make to the value of the field in their browser, or via JavaScript, or any other client-side technology, it'll retain the value assigned in the form's definition.

```
$form['hidden_field'] = [
  '#type' => 'hidden',
  '#value' => 'you can not change me',
];
```

This will render as an `<input type="hidden" .../>` element in the HTML for the form. But, because the `#value` property is used in the `$form` array, any data submitted by the browser for that field will be marked as invalid if it doesn't match what's already in the `#value` property.

For a detailed explanation of what is happening with the `#value` property we recommend reading the code in `\Drupal\Core\Form\FormBuilder::handleInputElement`. It's a bit dense, but informative.

As an alternative, if you want to store a value for validation or processing but **never send it to the browser** you can use a [`'#type' => 'value'` element](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Value.php/class/Value/).

Example:

```
$form['internal_field'] = [
  '#type' => 'value',
  '#value' => 'This value is internal only.',
];
```

## Recap

In this tutorial we showed how you can pre-populate a form element by using the `#default_value` property, allowing a form to be used for updating existing content, not just collecting new content. We also discussed the difference between the `#default_value` and `#value` properties.

## Further your understanding

- What happens if in the example above you use `#value` instead of `#default_value`?
- Can you give an example of a use case for using the `#value` property?

## Additional resources

- [Add Input Elements to a Form](https://drupalize.me/tutorial/add-input-elements-form) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Inject Services into a Form Controller](/tutorial/inject-services-form-controller?p=2734)

Next
[Form Element Reference](/tutorial/form-element-reference?p=2734)

Clear History

Ask Drupalize.Me AI

close