---
title: "Add a Validation Callback to an Existing Form"
url: "https://drupalize.me/tutorial/add-validation-callback-existing-form?p=3255"
guide: "[[develop-forms-drupal]]"
order: 13
---

# Add a Validation Callback to an Existing Form

## Content

When working with forms that are not created by your code, where you're not implementing the form controller but rather interacting with the form via implementations of `hook_form_alter()`, you can use the `#validate` property of the root form element to add additional validation logic in the form of a callback function or method.

In this tutorial we'll:

- Implement a `#validate` callback that raises an error if specific conditions are not met

By the end of this tutorial you should know how to add custom validation logic to any form in Drupal by using a `#validate` callback.

## Goal

Add validation to a form via `hook_form_alter()` and validate that the value entered into the *textfield* of a form is at least 5 characters in length unless the user has chosen the *skip validation* option.

## Prerequisites

- [Form API Life Cycle](https://drupalize.me/tutorial/form-api-life-cycle)
- [Validate Form Input](https://drupalize.me/tutorial/validate-form-input)
- [Define a New Form Controller and Route](https://drupalize.me/tutorial/define-new-form-controller-and-route) - We'll be expanding on the form started in this tutorial.
- [Render API Callback Properties](https://drupalize.me/tutorial/render-api-callback-properties)

## Perform validation using a `#validate` callback

When using `hook_form_alter()` to influence an existing form you can add additional callbacks to the `#validate` property of the top level `$form` array. Validation callbacks can be attached either to the root `$form` element, or to a `'#type' => 'submit'` button. In the latter case, they are only called if that button triggers submission of the form.

The `#validate` property is an array of validation callbacks, meaning that a form can specify more than one.

You might do this when:

- Your validation logic requires knowledge of the values of more than one element in the form, and you don't own the form controller
- You've added new fields into an existing form and you want to provide validation for those new fields
- You want to add additional validation logic to an existing form

**Note:** This example adds validation to the form we defined in [Define a New Form Controller and Route](https://drupalize.me/tutorial/define-new-form-controller-and-route). It is the same validation we add in the other form validation tutorials, just via a different approach, so if you've added it elsewhere you might want to remove it before proceeding with this tutorial.

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

We're going to check the length of the *title* field to ensure that it at is least 5 characters in length, unless the user has opted to skip this validation using the *skip\_validation* checkbox.

### Add a validation callback

In your module's *MYMODULE.module* file, add an implementation of `hook_form_alter()`. Use it to modify the `$form` array, and add a new callback to the list of validation callbacks. These will be called when validating the form in top down order.

```
/**
 * Implements hook_form_alter().
 */
function form_api_example_form_alter(&$form, &$form_state, $form_id) {
  if ($form_id == 'form_api_example_simple_form') {
    // A form can have more than one validation handler. So we want to make
    // sure that we are adding to the existing array rather than overwriting it.
    // The value can be either the name of a PHP function, or the method on a
    // class, that should be called to perform validation.
    //
    // If using a function name it's a good idea to keep this unique by
    // prefixing them with the name of your module. A common pattern is:
    // {MODULE}_{FORM ID}_validate().
    $form['#validate'][] = 'form_api_example_simple_form_validate';
  }
}
```

Read more about [implementing hook\_form\_alter()](https://drupalize.me/tutorial/alter-existing-form-hookformalter).

### Define the callback

Define the new callback function or method. Whether calling a function, or a method on a class, you need to ensure that that code exists. Failure to do so will cause an error. Arguments for the callback are `$form`, and `$form_state`. This is typically done in a *.module* file. However, the only requirement is that it's in a location where the code will be loaded when the form in question is submitted.

```
/**
 * Form validation callback.
 */
function form_api_example_simple_form_validate($form, FormStateInterface &$form_state) {
  // Validation code goes here.
}
```

Read more about the use of [callbacks as the value for Render API element properties](https://drupalize.me/tutorial/render-api-callback-properties).

### Validate the user input

Finally, validate input with PHP logic and raise errors using `$form_state->setErrorByName()`.

```
/**
 * Form validation callback.
 */
function form_api_example_simple_form_validate($form, FormStateInterface &$form_state) {
  $skip_validation = $form_state->getValue('skip_validation');
  $title = $form_state->getValue('title');
  if (!$skip_validation && strlen($title) < 5) {
    // Set an error for the form element with a key of "title".
    $form_state->setErrorByName('title', $this->t('The title must be at least 5 characters long.'));
  }
}
```

## Recap

In this tutorial we learned how to add custom validation logic to our forms by adding the `#validate` property to the root `$form` element and specifying a callback function. Additionally, we noted that this can also work to attach button-specific validation callbacks.

## Further your understanding

- How would you add additional validation logic to the password field for a user registration form that requires the password to be 12 characters or more?
- Can you find an example in core of a button that uses a `#validate` callback? What is it using it for?
- Learn about other validation techniques including [Validate a Form via the Form Controller](https://drupalize.me/tutorial/validate-form-form-controller), or [Validate a Single Form Element](https://drupalize.me/tutorial/validate-single-form-element).

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
[Validate a Form via the Form Controller](/tutorial/validate-form-form-controller?p=3255)

Next
[Validate a Single Form Element](/tutorial/validate-single-form-element?p=3255)

Clear History

Ask Drupalize.Me AI

close