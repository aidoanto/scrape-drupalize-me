---
title: "Validate a Form via the Form Controller"
url: "https://drupalize.me/tutorial/validate-form-form-controller?p=3255"
guide: "[[develop-forms-drupal]]"
order: 12
---

# Validate a Form via the Form Controller

## Content

When your module defines the form and the form controller, you can add your validation logic as part of the form controller. This is done via the implementation of a `validateForm()` method. The `FormBuilder` service will automatically invoke this method at the appropriate time during the process of submitting a form. While the `validateForm()` method is required by `\Drupal\Core\Form\FormInterface`, an empty method will fulfill that requirement. It's up to you to provide appropriate validation code inside the method.

In this tutorial we'll:

- Use the `validateForm()` method of a form controller to verify user input
- Demonstrate how to raise errors on a form element when it doesn't pass validation

By the end of this tutorial you should know how to validate your custom forms.

## Goal

Validate that the value entered into the *textfield* of a form is at least 5 characters in length unless the user has chosen the *skip validation* option.

## Prerequisites

- [Form API Life Cycle](https://drupalize.me/tutorial/form-api-life-cycle)
- [Define a New Form Controller and Route](https://drupalize.me/tutorial/define-new-form-controller-and-route) - We'll be expanding on the form started in this tutorial.

## Where do I put the code?

If your module defines the form controller you can place your custom validation logic into the `validateForm()` method of the controller. See `\Drupal\Core\Form\FormInterface::validateForm()`.

Remember our form has the following two fields:

```
$form['title'] = [
  '#type' => 'textfield',
  '#title' => $this->t('Title'),
  '#description' => $this->t('Title must be at least 5 characters in length.'),
  '#required' => TRUE,
];

$form['skip_validation'] = [
  '#type' => 'checkbox',
  '#title' => $this->t('Skip validation'),
  '#description' => $this->t('Allow the use of a title with fewer than 5 characters.'),
];
```

We're going to check the length of the *title* field to ensure that it is at least 5 characters in length, unless the user has opted to skip this validation using the *skip\_validation* checkbox.

## Perform validation in the form controller

This is the most common method of form validation.

### Add a `validateForm` method

If your controller doesn't already have one, define a new method named `validateForm()`.

### Validate input with PHP logic

Use any PHP logic to validate the input. In this case, check the length of the string, but not if the user checked the skip validation checkbox.

### Raise errors with `$form_state`

Raise an error and set a message to display using `$form_state->setErrorByName()`.

#### Example

```
public function validateForm(array &$form, FormStateInterface $form_state) {
  // Get the value of the skip_validation checkbox. Defaults to 0 if
  // unchecked. 1 if checked.
  $skip_length_validation = $form_state->getValue('skip_validation');
  // Get the user-entered value of the 'title' field.
  $title = $form_state->getValue('title');
  if (!$skip_length_validation && strlen($title) < 5) {
    // Set an error for the form element with a key of "title".
    $form_state->setErrorByName('title', $this->t('The title must be at least 5 characters long.'));
  }
}
```

## Recap

In this tutorial we learned how to add custom validation logic to our forms by implementing a `validateForm()` method on our form controller.

## Further your understanding

- Can you explain why when your form controller extends `FormBase` the `validateForm()` method is optional even though it's required by `FormInterface`?
- Learn about other validation techniques including [Add a Validation Callback to an Existing Form](https://drupalize.me/tutorial/add-validation-callback-existing-form) or [Validate a Single Form Element](https://drupalize.me/tutorial/validate-single-form-element).

## Additional resources

- [Documentation for `FormStateInterface`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Form%21FormStateInterface.php/interface/FormStateInterface/) (api.drupal.org)
- [Inline Form Errors Module](https://www.drupal.org/docs/8/core/modules/inline-form-errors) (Drupal.org)
- [Examples for Developers project](https://www.drupal.org/project/examples) (Drupal.org)
- [What Are Hooks?](https://drupalize.me/tutorial/what-are-hooks) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Validate Form Input](/tutorial/validate-form-input?p=3255)

Next
[Add a Validation Callback to an Existing Form](/tutorial/add-validation-callback-existing-form?p=3255)

Clear History

Ask Drupalize.Me AI

close