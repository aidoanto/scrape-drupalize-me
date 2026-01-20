---
title: "Define a New Form Controller and Route"
url: "https://drupalize.me/tutorial/define-new-form-controller-and-route?p=2734"
guide: "[[develop-forms-drupal]]"
order: 3
---

# Define a New Form Controller and Route

## Content

Each form is defined by a controller, a class that implements the `\Drupal\Core\Form\FormInterface`. Form controllers declare the unique ID of the form, the `$form` array that describes the content of the form, how to validate the form, and what to do with the data collected.

In this tutorial we'll:

- Define a new form controller class
- Implement the required methods to describe a form
- Add a route that can be used to access our form

By the end of this tutorial you should be able to define a form that adheres to the `FormInterface` requirements and know where to find more information about how to further customize your form controller.

## Goal

Display a form with a single text input element accessible by navigating to *examples/form-api-example/simple-form*.

## Prerequisites

- [Form API Life Cycle](https://drupalize.me/tutorial/form-api-life-cycle)
- [Render Arrays](https://drupalize.me/tutorial/what-are-render-arrays)
- [Overview: Routes, Controllers, and Responses](https://drupalize.me/tutorial/overview-routes-controllers-and-responses)

## Code examples

The complete code for the examples in this tutorial may be found in the [Examples for Developers'](https://www.drupal.org/project/examples) *form\_api\_example* module.

## Use Drush Generate to scaffold forms

**Pro tip**: [Drush](https://drupalize.me/topic/drush), via [Drush Generate](https://drupalize.me/tutorial/develop-drupal-modules-faster-drush-code-generators), has commands for scaffolding 3 types of forms: general-use forms ("simple forms"), configuration, and confirmation (e.g. to confirm deletion). Once you understand the basics of the Form API, expedite defining a new form with:

- `drush generate form:simple` (alias: `form`)
- `drush generate form:config` (alias: `config-form`)
- `drush generate form:confirm` (alias: `confirm-form`)

**Note**: The first question will ask the name of the module for your form. If you don't already have a module created, specify a new machine name for a module and a new module with that name will be scaffolded as well.

## Define a new form

### Create a new form controller class

Each form is defined by a controller, a class that implements the `\Drupal\Core\Form\FormInterface`. In most cases you can start by extending `\Drupal\Core\Form\FormBase` which serves as a mid-point for dependency injection and inclusion of some generically useful traits. Our recommendation: use `FormBase` unless you can specify why you're not using it.

Form controllers are typically namespaced to `Drupal\{my_module}\Form` and live in `{my_module}/src/Form`.

### Example

From *form\_api\_examples/src/Form/SimpleForm.php*:

```
<?php

namespace Drupal\form_api_example\Form;

use Drupal\Core\Form\FormBase;
use Drupal\Core\Form\FormStateInterface;

/**
 * This example demonstrates a simple form with a singe text input element. We
 * extend FormBase which is the simplest form base class used in Drupal.
 */
class SimpleForm extends FormBase {

}
```

### Give your form a unique ID

Every form needs a unique ID. This is a string, returned from the `getFormId()` method of the form controller. The easiest way to ensure unique IDs is to prefix them with the name of your module. You'll primarily see the ID used by implementations of `hook_form_alter()` to identify which form is being altered.

#### Example

```
/**
 * Getter method for Form ID.
 *
 * @return string
 *   The unique ID of the form defined by this class.
 */
public function getFormId() {
  return 'form_api_example_simple_form';
}
```

### Describe the form you want to display

The form itself is defined as a renderable array containing `FormElement` elements for collecting user input, and typically referred to as the `$form` array. The `$form` array is defined and returned by the `buildForm()` method of your form controller.

#### Example

```
/**
 * Build the simple form.
 *
 * @param array $form
 *   Default form array structure.
 * @param \Drupal\Core\Form\FormStateInterface $form_state
 *   Object containing current form state.
 *
 * @return array
 *   The render array defining the elements of the form.
 */
public function buildForm(array $form, FormStateInterface $form_state) {
  $form['description'] = [
    '#type' => 'item',
    '#markup' => $this->t('This basic example shows a single text input element and a submit button'),
  ];

  $form['title'] = [
    '#type' => 'textfield',
    '#title' => $this->t('Title'),
    '#description' => $this->t('Title must be at least 5 characters in length.'),
    '#required' => TRUE,
  ];

  // Group submit handlers in an actions element with a key of "actions" so
  // that it gets styled correctly, and so that other modules may add actions
  // to the form. This is not required, but is convention.
  $form['actions'] = [
    '#type' => 'actions',
  ];

  // Add a submit button that handles the submission of the form.
  $form['actions']['submit'] = [
    '#type' => 'submit',
    '#value' => $this->t('Submit'),
  ];

  return $form;
}
```

The above example describes a form with a single textfield named "Title" that is required and a submit button named "Submit" that will submit the form.

Image

![Form with one input field labeled title and a submit button.](../assets/images/form_api-simple_form_screenshot.png)

The `$this->t()` method allows for translation and is available because we extended `FormBase`.

For more information about the `$form` array and how it works, see [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays) and [Use Render Element Types in a Render Array](https://drupalize.me/tutorial/use-render-element-types-render-array). For a list of available form element types see [Form Element Reference](https://drupalize.me/tutorial/form-element-reference).

### Add some validation

User input can be validated and otherwise manipulated in the form controllers `validateForm()` method. Here you can perform whatever logic is required to verify the user input meets your requirements, and optionally raise errors for the user to correct if it does not. Raising an error halts form execution. See [Form API Life Cycle](https://drupalize.me/tutorial/form-api-life-cycle).

#### Example

```
/**
 * Implements form validation.
 *
 * @param array $form
 *   The render array of the currently built form.
 * @param \Drupal\Core\Form\FormStateInterface $form_state
 *   Object describing the current state of the form.
 */
public function validateForm(array &$form, FormStateInterface $form_state) {
  $title = $form_state->getValue('title');
  if (strlen($title) < 5) {
    // Set an error for the form element with a key of "title".
    $form_state->setErrorByName('title', $this->t('The title must be at least 5 characters long.'));
  }
}
```

The above example accesses the user-provided value of the title field via the `$form_state` object and then checks to ensure that it is at least 5 characters in length. If it is not, an error is raised. Learn more about validating user input, and handling errors, in [Validate Form Input](https://drupalize.me/tutorial/validate-form-input).

The `$form_state` object controls the flow, and state, of a form. User-submitted values can be accessed via `$form_state->getValue('key')` where "key" is the name of the element whose value you would like to retrieve. This name is taken from the key used in the array that defines the element in the `buildForm()` method. So, `$form['title'] = array(...);` maps to `$form_state->getValue('title')`.

### Process collected data

Finally, add a `submitForm()` method to your controller to handle the processing of submitted data. At this point the data has been validated and is ready to be saved to the database, used for a calculation, or processed in whatever other way your custom code dictates.

#### Example

```
/**
 * Implements a form submit handler.
 *
 * @param array $form
 *   The render array of the currently built form.
 * @param \Drupal\Core\Form\FormStateInterface $form_state
 *   Object describing the current state of the form.
 */
public function submitForm(array &$form, FormStateInterface $form_state) {
  $title = $form_state->getValue('title');
  $this->messenger()->addStatus($this->t('You specified a title of %title.', ['%title' => $title]));
}
```

In the above example the user-entered (and previously validated) value of the title field is accessed via the `$form_state` object, and then printed out to the screen. The `submitForm()` method can optionally control what happens next via the `$form_state` object, for example redirecting to another page. In this case it does nothing, which results in the default action of displaying the same page again with an empty form.

Image

![Page showing message collected in title field of submitted form and an empty form with a textfield and a submit button](../assets/images/form_api-simple_form_submitted.png)

[Learn more about processing submitted data in a form controller](https://drupalize.me/tutorial/handle-submitted-form-data).

### Add a route for your form

In order to allow users to access our form we need to define a route that points to the form controller we defined above. Routes for forms use the `_form` key, instead of the standard `_controller` key, to tell Drupal that it should use the form builder service when servicing the request.

Example from *form\_api\_example.routing.yml*:

```
form_api_example.simple_form:
  path: 'examples/form-api-example/simple-form'
  defaults:
    _form: '\Drupal\form_api_example\Form\SimpleForm'
    _title: 'Simple form'
  requirements:
    _permission: 'access content'
```

The above code adds a route that maps the path *examples/form-api-example/simple-form* to our form controller `Drupal\form_api_example\Form\SimpleForm`.

The complete code for this example may be found in the [Examples for Developers](https://www.drupal.org/project/examples) *form\_api\_example* module.

## Recap

In this tutorial we created a new form controller by defining a class that extended `\Drupal\Core\Form\FormBase`, and implemented the required methods from `\Drupal\Core\Form\FormInterface`. These methods provide a unique ID for our form, define the content of the form, and handle validation and submission of user input. Finally we made our form accessible on a page by defining a route that mapped to our form controller. This demonstrates the fundamental concepts of adding a form via a module giving us a platform to build on in future tutorials.

Next: [Learn more about adding additional input elements to your form](https://drupalize.me/tutorial/add-input-elements-form).

## Further your understanding

- Try navigating to your newly created form in the browser. What happens if you enter a value into the title field that is less than 5 characters long?
- The `FormBase` class provides a `validateForm()` method which we overrode with our controller. What does `FormBase::validateForm()` do?
- [Learn how to display a form in other parts of the page](https://drupalize.me/tutorial/retrieve-and-display-forms).

## Additional resources

- [Introduction to Form API](https://www.drupal.org/node/2117411) (Drupal.org)
- [Examples for Developers](https://www.drupal.org/project/examples) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Form API Life Cycle](/tutorial/form-api-life-cycle?p=2734)

Next
[Add Input Elements to a Form](/tutorial/add-input-elements-form?p=2734)

Clear History

Ask Drupalize.Me AI

close