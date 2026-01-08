---
title: "Process Submitted Form Data with a Callback"
url: "https://drupalize.me/tutorial/process-submitted-form-data-callback?p=3256"
guide: "[[develop-forms-drupal]]"
---

# Process Submitted Form Data with a Callback

## Content

Sometimes you need to add additional processing of input to forms where your module doesn't implement the form controller. In order to do this you can use the `#submit` property of the root level `$form` element, or of a specific button on a form, to add one or more callbacks. These functions, or methods, will be automatically called when the Form API is processing a submitted form and give your custom code an opportunity to do whatever it needs to do.

In this tutorial we'll:

- Look at alternative ways to affect the submission handling of a form like `#submit` callbacks

By the end of this tutorial you should know how to add a `#submit` callback to an entire form, or a specific button in a form.

## Goal

Add a `#submit` callback to a form, or a button on a form.

## Prerequisites

- [Form API Life Cycle](https://drupalize.me/tutorial/form-api-life-cycle)
- [Define a New Form Controller and Route](https://drupalize.me/tutorial/define-new-form-controller-and-route) - We'll be expanding on the form started in this tutorial.
- [Handle Submitted Form Data](https://drupalize.me/tutorial/handle-submitted-form-data)
- [Render API Callback Properties](https://drupalize.me/tutorial/render-api-callback-properties)

## Where do I put the code?

There are two ways to add a `#submit` callback to a form. Both `'#type' => 'form'`, and `'#type' => 'submit'` elements can make use of the `#submit` property. Common use cases are:

- When using `hook_form_alter()` to influence an existing form, you can add additional callbacks to the `#submit` property of the top level `$form` array, or to any `'#type' => 'submit'` elements.
- You can use `#submit` callbacks on secondary buttons defined in your form to call alternate methods on the form controller.

This tutorial will show examples of performing the same logic using each of these different approaches.

## Processing data with a `#submit` callback

Another way to add custom logic to a form is by adding a `#submit` callback to the root `$form` element or an individual button in the form.

### Add a `#submit` handler to the entire form

Either in your `formBuild()` method, or more likely in an [implementation of `hook_form_alter()`](https://drupalize.me/tutorial/alter-existing-form-hookformalter), add a callback to the `#submit` property of the root `$form` element. This callback will be called whenever this form is submitted, regardless of which button is clicked. This is a great way to tie into the submission processing of a form created by another module so that your custom code can also react whenever that form is submitted.

```
function form_api_example_form_alter(&$form, &$form_state, $form_id) {
  if ($form_id == 'form_api_example_simple_form') {
    // A form can have more than one #submit handler. So we want to make
    // sure that we are adding to the existing array rather than overwriting it.
    // The value can be either the name of a PHP function, or the method on a
    // class, that should be called.
    //
    // If using a function name it's a good idea to keep this unique by
    // prefixing them with the name of your module. A common pattern is:
    // {MODULE}_{FORM ID}_submit().
    //
    // The arguments for the callback are $form, and $form_state.
    $form['#submit'][] = 'form_api_example_simple_form_submit';
  }
}
```

### Define the corresponding callback

Then in your module define the function that will be called when the form is submitted, and add your custom input processing logic to the function.

```
function form_api_example_simple_form_submit($form, FormStateInterface $form_state) {
  \Drupal::messenger()->addStatus('Called form_api_example_simple_form_submit');
}
```

Another option is to attach an alternate submission handler to a specific button in a form. This will allow you to set up a scenario where different code is invoked depending on which button a user clicks.

### Add a `#submit` callback to a button

Either in your `formBuild()` method, or in an implementation of `hook_form_alter()`, add a new button with a `#submit` property, or adjust the `#submit` property of an existing button.

**Note:** This only works for elements where `'#type' => 'submit'`.

```
// This callback is only called if the button that it is attached to
// is the one used to submit the form.
$form['alternate_button'] = [
  '#type' => 'submit',
  '#value' => $this->t('Do alternate thing'),
  // Note that when you specify a submit handler like this only those defined
  // in this array of callbacks will be called. If it's not specified, the default
  // ::submitForm() method will not be called.
  '#submit' => ['::alternateFormSubmit']
];
```

### Define the corresponding callback

Then, define the corresponding callback method or function.

```
public function alternateFormSubmit(array &$form, FormStateInterface $form_state) {
  $this->messenger()->addStatus($this->t('The alternate submit button was pressed.'));
}
```

Just like with the `submitForm()` method on our controller we can use either of these options as an opportunity to call `$form_state->setRedirect()` in order to influence what happens after the form has been submitted.

Submit callbacks are also useful when defining new form element types. Checkout the ManagedFile form element for a good example of using a `#submit` callback on a specific button.

## Recap

In this tutorial we looked at examples of how you can use `hook_form_alter()` in conjunction with the `#submit` property to have additional, or alternate, code called to handle form submission.

## Further your understanding

- What happens if you attach more than one callback to a button? What order are they executed in?
- Can you create a button that calls a custom submit handler and skips, or limits, validation?
- Explore the *form\_api\_example/src/Form/BuildDemo.php* example in the [Examples for Developers project](https://www.drupal.org/project/examples).

## Additional resources

- [Documentation for `FormStateInterface`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Form%21FormStateInterface.php/interface/FormStateInterface/) (api.drupal.org)
- [Examples for Developers project](https://www.drupal.org/project/examples) (Drupal.org)
- [What Are Hooks?](https://drupalize.me/tutorial/what-are-hooks) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Handle Submitted Form Data](/tutorial/handle-submitted-form-data?p=3256)

Next
[Process Submitted Form Data via the Form Controller](/tutorial/process-submitted-form-data-form-controller?p=3256)

Clear History

Ask Drupalize.Me AI

close