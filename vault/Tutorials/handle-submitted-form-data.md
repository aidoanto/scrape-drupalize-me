---
title: "Handle Submitted Form Data"
url: "https://drupalize.me/tutorial/handle-submitted-form-data?p=3256"
guide: "[[develop-forms-drupal]]"
---

# Handle Submitted Form Data

## Content

You probably created a form with the intent of collecting user input and then doing something with that input. Using the `submitForm()` method of our form class we can access the validated, and sanitized, user input data and make use of it for our own needs. We might do things like save the collected data as configuration, update an entity, or use it as part of a search query.

In this tutorial we'll:

- Demonstrate how to add a `submitForm()` method to a form controller class
- Access the value(s) of form input elements via the `$form_state` object
- Set a redirect after performing processing in a form submission handler
- Look at alternative ways to affect the submission handling of a form like `#submit` callbacks

By the end of this tutorial you should know how to access the values of a submitted form, and how to write custom processing code that gets invoked when the form passes validation.

## Goal

Add custom submission processing logic to a form that displays the content input by the user on the screen.

## Prerequisites

- [Form API Life Cycle](https://drupalize.me/tutorial/form-api-life-cycle)
- [Define a New Form Controller and Route](https://drupalize.me/tutorial/define-new-form-controller-and-route) (We'll be expanding on the form started in this tutorial.)
- [Render API Callback Properties](https://drupalize.me/tutorial/render-api-callback-properties)

## Where do I put the code?

There are a couple of ways you can tell Drupal what code you want to execute when processing the data collected by a form.

- If your module defines the form controller, you can place your custom submission processing logic into the `submitForm()` method of the controller. [Learn about implementing a `submitForm()` method](https://drupalize.me/tutorial/process-submitted-form-data-form-controller).
- When using `hook_form_alter()` to influence an existing form, you can add additional callbacks to the `#submit` property of the top level `$form` array, or to any `'#type' => 'submit'` elements. This is useful when you need to provide additional input processing to an existing form, or when you're using `hook_form_alter()` to add new elements to an existing form and then also need to handle the processing of data collected by those elements. For example, when you add another option to the settings form for content types that is used to indicate whether or not your module's features are enabled for a specific content type. [Learn about using the `#submit` property](https://drupalize.me/tutorial/process-submitted-form-data-callback).
- You can use `#submit` callbacks on secondary buttons defined in your form to call alternate methods on the form controller. This is useful when you've got a form that has more than one button on it and you want different code to be executed depending on which button is pressed. For example, the widget for uploading an image to an image field contains a file select element and an upload button which when clicked uploads the image via AJAX. [Learn about using the `#submit` property](https://drupalize.me/tutorial/process-submitted-form-data-callback).

This tutorial will show examples of performing the same logic using each of these different approaches.

## Retrieving values from form fields

The `$form_state` object passed into your submit method or callback is responsible for controlling the flow and processing of the form. It can be used to access the collected user input, and to control the next steps taken by the Form API after your custom logic has completed.

Use `$form_state->getValue('element name')` to retrieve the value of a specific form element, where `element name` is the key used when adding the element to the `$form` array.

Image

![Screenshot of $form array in buildForm method with arrows pointing to keys of the array to show which ones are element names.](../assets/images/form-api_element-name-example.png)

**Note:** In the [life cycle of a form](https://drupalize.me/tutorial/form-api-life-cycle), by the time your submission logic is reached [all validation](https://drupalize.me/tutorial/validate-form-input) will have already been performed, so you can assume that the values in `$form_state` have all been validated and are ready to be used.

In some cases you might want to just grab the values of all submitted fields, and store all of them by, for example, serializing them into a single database column. In such cases, all internal Form API values and all form button elements should not be contained, and you can use the `$form_state->cleanValues()` method to retrieve an array of all values with these Form API internals removed. In addition to any button elements, `cleanValues()` also removes the `form_id`, `form_token`, `form_build_id`, and the `op` parameter.

- `$form_state->getValue($key, $default = '')`: Returns the submitted and sanitized form value for a specific key.
- `$form_state->getValues()`: Returns the submitted and sanitized form values for all elements.
- `$form_state->cleanValues()`: Similar to `getValues()` but with some important differences. `cleanValues()` returns a `FormStateInterface` object, with the Form API internal elements removed. This means that `$form_state` will be changed by calling `cleanValues()`.

## Submitted values vs. stored values

`FormStateInterface` defines methods for `get()`/`set()` and `getValue()`/`setValue()`. Which, on the surface, appear to do the same thing. But there's an important distinction. The former deals with values in the forms persistent storage, while the latter are for values submitted to the form.

### Persistent storage

The `get`, `set`, `has`, `getStorage`, and `setStorage` methods all deal with values that should be stored for the entire life time of the form. Once set they will be present regardless of what state the form is currently in.

### Submitted values

The `getValue`, `setValue`, `cleanValues`, and `getValues` methods all deal with submitted data. They will only contain the data collected from the form when it was last submitted.

To help illustrate this consider a multi-step form that collects your first and last name on the first page, and then your address on the second page. In this scenario you have values that need to persist across multiple rebuilds of the form, and you have values that are the result of a specific page of the form being submitted.

- When the form is first displayed both data stores are empty
- When the user submits the first page the submitted values store contains the first and last name data collected from the form, these can be set in the persistent store by the submit handler
- The form is rebuilt, and the new page is displayed, the submitted value store is empty, but the persistent store contains the first and last name.
- The user submits the second page of the form, the submitted values store contains the address, the persistent store still contains the first and last name, and address could be added by the submit handler
- If the user hit a "previous step" button to go back and update previously entered information at this point page one of the form would be rebuilt, the submitted value store would be empty, but the presistent store would still contain all three values
- Once the form has finally been submitted, processed, and nothing sets the rebuild trigger along the way the form is considered complete and the persistent store is finally removed

Another common use case for this would be comparing old and new values of a textfield. When the form is first displayed you could set the current value into the persistent store. When the form is submitted you can then retrieve that value and compare it to the submitted value.

## Recap

In this tutorial we got a high level overview of the different ways that a module developer can add code to perform custom processing of the data collected by a form. We learned how to retrieve user input from the Form API's `$form_state` object.

## Further your understanding

- Explore the *form\_api\_example/src/Form/BuildDemo.php* example in the [Examples for Developers project](https://www.drupal.org/project/examples).
- The documentation in both *core/lib/Drupal/Core/Form/FormStateInterface.php* and *core/lib/Drupal/Core/Form/FormState.php* provides a lot of information about how data in forms is handled internally
- [Learn about adding a `submitForm()` method to your form controller](https://drupalize.me/tutorial/process-submitted-form-data-form-controller)
- [Learn about using the `#submit` property with form elements](https://drupalize.me/tutorial/process-submitted-form-data-callback)

## Additional resources

- [Documentation for `FormStateInterface`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Form%21FormStateInterface.php/interface/FormStateInterface/) (api.drupal.org)
- [Examples for Developers project](https://www.drupal.org/project/examples) (Drupal.org)
- [What Are Hooks?](https://drupalize.me/tutorial/what-are-hooks) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Process Submitted Form Data with a Callback](/tutorial/process-submitted-form-data-callback?p=3256)

Clear History

Ask Drupalize.Me AI

close