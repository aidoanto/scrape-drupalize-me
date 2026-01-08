---
title: "Use Ajax to Submit a Form"
url: "https://drupalize.me/tutorial/use-ajax-submit-form?p=2730"
guide: "[[develop-forms-drupal]]"
---

# Use Ajax to Submit a Form

## Content

Using Ajax allows you to create forms that are submitted to the server, and processed, without requiring a page reload.

In this tutorial we'll:

- Use `#ajax` with a `'#type' => 'submit'` button in order to submit a form via Ajax
- Look at how form build, validation, and processing are used when submitting a form via Ajax
- Use the form's internal storage to track data across multiple requests
- Discuss some best practices to keep in mind when using Ajax for form submissions

By the end of this tutorial you should know how to update an existing form so that it is submitted via Ajax and no longer requires a page refresh to work.

## Goal

Submit a form using Ajax. After successfully processing the submitted form, update the page with new content without requiring a refresh.

## Prerequisites

- [Use Ajax with Forms](https://drupalize.me/tutorial/use-ajax-forms)
- [Render API Callback Properties](https://drupalize.me/tutorial/render-api-callback-properties)

## Overview

This tutorial shows an example of submitting a complete form sending the HTTP POST request as an XHttpRequest, resulting in triggering the validation and submission handling of the form. Example: submitting a user's vote in a poll when they click the submit button and then displaying the aggregated results (instead of the form) after tallying their vote -- all without refreshing the page.

To learn about altering a form see [Create a Dependent Dropdown with Ajax](https://drupalize.me/tutorial/create-dependent-dropdown-ajax).

## Submit a form via Ajax

This example is based on the code in *modules/contrib/examples/ajax\_example/src/Form/SubmitDriven.php* from the [Examples for Developers project](https://www.drupal.org/project/examples). It is easiest to read this example as complete code, so we'll outline the steps required to add Ajax to a form, and then display the completed form controller class with inline comments below.

### Define the form to add Ajax to

Start by creating a form and getting it working without Ajax first. Set up your form controller class and define build, validate, and submit functions that work with a non-Ajax form submission. See [Define a New Form Controller and Route](https://drupalize.me/tutorial/define-new-form-controller-and-route).

Doing this helps to ensure that your form will work even if the client doesn't support JavaScript.

### Add `#ajax` to the submit button

Modify your already-working form and add an `#ajax` property to the submit button. At a minimum you'll need to define a *callback* and a *wrapper*. Learn more about other possible values you can use in [Use Ajax with Forms](https://drupalize.me/tutorial/use-ajax-forms).

Before:

```
$form['submit'] = [
  '#type' => 'submit',
  '#value' => $this->t('Submit'),
];
```

After:

```
$form['submit'] = [
  '#type' => 'submit',
  '#ajax' => [
    // The Ajax callback method that is responsible for responding to the
    // Ajax HTTP request.
    'callback' => '::promptCallback',
    // The ID of the DOM element whose content will be replaced with
    // whatever is returned from the above callback.
    'wrapper' => $ajax_wrapper_id,
  ],
  '#value' => $this->t('Submit'),
];
```

### Add an Ajax callback method

In your form controller, define the method you declared in `'callback'` above. Form processing logic should remain in the existing build, validate, and submit methods; this new callback should deal only with returning a response to the Ajax request.

The method receives two arguments: `array &$form` and `FormStateInterface $form_state`. It should return either a render array or an Ajax command.

Learn more about Ajax commands in this presentation, [Drupal 8 Day: Demystifying AJAX Callback Commands in Drupal 8](https://www.youtube.com/watch?v=6YhJq01jlpY), by Mike Miles.

### Update `submitForm()`

You'll likely want to make some modifications to your submit handler. These include:

- Saving processed data into the the `$form_state`'s internal storage for later use, either in the Ajax callback or during form building in `buildForm()`
- Setting the rebuild flag with `$form_state->setRebuild()` so that the form's `buildForm()` method is called again before handing control to the Ajax callback method

### Update `buildForm()`

You might also want to make changes to your `buildForm()` method that take into account data collected when the form is submitted. When submitting a form via Ajax, remember that your `buildForm()` method is responsible for determining what is displayed both before and after the form has been submitted.

You'll also likely need to make some modifications here to provide a unique ID that corresponds to the *wrapper* key used in your `#ajax` definition. When dealing with submitting forms via Ajax, we recommend starting by wrapping the entire form, and only adjusting that if required.

Example:

```
$form['#prefix'] = '<div id="' . $ajax_wrapper_id . '">';
$form['#suffix'] = '</div>';
```

## Complete example

Note, this example is based on the `SubmitDriven` code in the *ajax\_example* module in the [Examples for Developers project](https://www.drupal.org/project/examples), but we've modified it for clarity. If you want to see it in action, copy and paste the code below into *modules/contrib/examples/ajax\_example/src/Form/SubmitDriven.php* after installing the Examples for Developers project.

```
<?php

namespace Drupal\ajax_example\Form;

use Drupal\Component\Utility\Html;
use Drupal\Core\Form\FormBase;
use Drupal\Core\Form\FormStateInterface;

/**
 * Submit a form without a page reload.
 */
class SubmitDriven extends FormBase {

  /**
   * {@inheritdoc}
   */
  public function getFormId() {
    return 'ajax_example_autotextfields';
  }

  /**
   * {@inheritdoc}
   */
  public function buildForm(array $form, FormStateInterface $form_state) {
    // Generate a unique wrapper HTML ID.
    $ajax_wrapper_id = Html::getUniqueId('box-container');

    // Add a wrapper around the <form> with a unique ID. The content of this DOM
    // element will be replaced by whatever is returned from the Ajax request.
    $form['#prefix'] = '<div id="' . $ajax_wrapper_id . '">';
    $form['#suffix'] = '</div>';

    // The logic in our buildForm method needs to determine which version of the
    // form to display: the one we want to show users initially, or the one that
    // we want to show them after the form has been submitted and processed.
    // Keeping all of this logic inside of our buildForm() method helps to ensure
    // that this form will function properly even if JavaScript is disabled or
    // if the form is submitted by other means.
    //
    // In this case, our submit handler will save a value to the 'string' key of
    // the form's persistent storage. So we can assume that if that value is
    // present that the form has been submitted and passed validation, in which
    // case we display the "success" message.
    //
    // Additionally, putting this logic in the buildForm() method allows us to
    // optionally skip to this state depending on other logic. For example, if
    // this was a poll and the user had already voted on the poll, instead of
    // showing them the form again we could just display the results.
    if ($form_state->has('string')) {
      // Build the content we want to display after the form was submitted.
      $form['box'] = [
        '#markup' => '<p>' . $this->t('You clicked submit on @date', ['@date' => date('c')]) . '</p>'
      ];

      $form['item'] = [
        '#markup' =>  '<p>' . t('You submitted %string which results in %reversed when reversed.', ['%string' => $form_state->get('string'), '%reversed' => $form_state->get('reversed_string')]) . '</p>',
      ];
    }
    // Otherwise this is the user first coming to the page so we need to
    // display the form in its initial state. Or, the form was submitted but
    // failed validation so we need to re-display the form and allow the user
    // to correct any errors.
    else {
      // The box contains some markup that we can change on a submit request.
      $form['box'] = [
        '#type' => 'markup',
        '#markup' => '<h1>Initial markup for box</h1>',
      ];

      // A plain textfield we can use to collect a value from the user.
      $form['item'] = [
        '#type' => 'textfield',
        '#required' => TRUE,
        '#title' => $this->t('Enter some text'),
        '#description' => $this->t('Must be at least 5 characters.'),
      ];

      // The button for submitting the form. Configured to use Ajax to submit
      // the form via the #ajax property.
      $form['submit'] = [
        '#type' => 'submit',
        // Use the #ajax property to declare this button should trigger an Ajax
        // request.
        '#ajax' => [
          // The Ajax callback method that is responsible for responding to the
          // Ajax HTTP request.
          'callback' => '::promptCallback',
          // The ID of the DOM element whose content will be replaced with
          // whatever is returned from the above callback.
          'wrapper' => $ajax_wrapper_id,
        ],
        '#value' => $this->t('Submit'),
      ];
    }

    return $form;
  }

  /**
   * {@inheritdoc}
   */
  public function validateForm(array &$form, FormStateInterface $form_state) {
    // This demonstrates that the form's validation method is called when the
    // form is submitted by Ajax. Try submitting the form with a string that
    // has fewer than 5 characters to see how errors are handled.
    $title = $form_state->getValue('item');
    if (strlen($title) < 5) {
      // Set an error for the form element with a key of "title".
      $form_state->setErrorByName('item', $this->t('The text must be at least 5 characters long.'));
    }
  }

  /**
   * {@inheritdoc}
   */
  public function submitForm(array &$form, FormStateInterface $form_state) {
    // Here you can do something with the submitted form data just like you
    // would if the form was submitted without Ajax.
    $string = $form_state->getValue('item');

    // In order to pass any results of processing that happens in the submit
    // handler you can use $form_state's persistent storage. Setting values here
    // ensures they'll be available for use in the #ajax callback which doesn't
    // get triggered until after the submission handler is done.
    $form_state->set('string', $string);
    $form_state->set('reversed_string', strrev($string));

    // Tell the form to rebuild (call buildForm()) after all submit handling
    // logic is completed but before the Ajax callback is invoked. This 
    // effectively results in an updated $form array being passed to the callback.
    $form_state->setRebuild();
  }

  /**
   * Ajax callback for "Submit" button.
   *
   * This callback is called regardless of what happens in validation and
   * submission processing. It needs to return the content that will be used to
   * replace the DOM element identified by the '#ajax' properties 'wrapper' key.
   *
   * @return array
   *   Renderable array (the box element)
   */
  public function promptCallback(array &$form, FormStateInterface $form_state) {
    // When dealing with forms submitted via Ajax we want to just return the
    // complete $form array. All of the logic for figuring out what should be in
    // the form is contained in buildForm().
    //
    // The one thing we will add here is any errors that were generated when
    // trying to validate the form. This snippet checks to see if there are any
    // errors, and if so creates a render array that will retrieve and display
    // the status messages, then renders it to HTML and tacks it onto the
    // beginning of the form.
    if ($form_state->hasAnyErrors()) {
      $renderer = \Drupal::service('renderer');
      $status_messages = ['#type' => 'status_messages'];
      $form['#prefix'] .= $renderer->renderRoot($status_messages);
    }

    return $form;
  }

}
```

It's relatively easy to configure a button on a form to submit the form via an Ajax request. However, it can get complex pretty quickly when dealing with anything other than the simplest of forms. Here are some things to keep in mind when submitting forms with Ajax.

### Buttons vs. submit buttons

Non-submit buttons, `'#type' => 'button'`, when clicked will trigger the form's validation handlers, any submit handlers explicitly attached to the button with `#submit`, and finally the Ajax callback.

Submit buttons, `'#type' => 'submit'`, when clicked will trigger the form's validation handlers, all submit handlers for the form (e.g. `$form['#submit']`), any submit handlers explicitly attached to the button with `#submit`, and finally the Ajax callback. In most cases the difference will be whether or not the `submitForm()` method of the form controller is called.

### A note about the rebuild flag

The "rebuild" flag can be set with: `$form_state->setRebuild(TRUE)`.

Normally, after form processing is completed and submit handlers have been executed, a form is considered to be done and will redirect the user to a new page using a GET request. This is usually either the page specified by `$form_state->setRedirect()` or the same page the form was submitted from. However, if the internal "rebuild" flag has been set to `TRUE` with `$form_state->setRebuild(TRUE)`, then a new copy of the form is immediately built and sent to the browser, instead of a redirect. This is used for multi-step forms, such as wizards and confirmation forms. Normally, the "rebuild" flag is set by a submit handler, since it is usually logic within a submit handler that determines whether a form is done or requires another step. However, a validation handler may have already set "rebuild" to TRUE to cause the form processing to bypass submit handlers and rebuild the form instead, even if there are no validation errors.

Another way to think about this is to consider the order methods are called when submitting a form via Ajax:

1. `buildForm()`
2. `validateForm()`
3. `submitForm()`
4. `buildForm()` (But **only** if the rebuild flag was set before this point.)
5. `ajaxCallbackMethod()`

### Error handling

When a form is submitted via Ajax, validation handlers function like normal and can raise errors on any element in the form. Regardless of whether or not validation passes, the Ajax callback is triggered. This can lead to some interesting problems.

If you're not careful, an Ajax request that removes one or more form elements from the page can lead to a scenario where the element with an error isn't displayed and thus the user doesn't know there's an error to correct. For example, a submit button could submit a textfield and the Ajax request would replace that field with the text that was submitted. If there's an error on the textfield, you would need to ensure that the callback returns the textfield -- and not just the submitted text.

For this reason, we recommend that in most cases you keep your logic for determining what to display inside of the `buildForm()` method. Add a wrapper to the entire `$form` array using `#prefix` and `#suffix`, and then always return the complete `$form` array from your Ajax callback. This will result in the complete form being updated every time, and the display of errors can function just like it would with non-Ajax forms.

## Recap

In this tutorial, we looked at how you can use the `#ajax` property of a `'#type' => 'submit'` button in a form to cause the form to submit without a page refresh using Ajax. This requires defining a *callback* method that will provide a response to the Ajax request, and a *wrapper* ID indicating which DOM element to modify. We also discussed some best practices and other things to keep in mind when creating Ajax forms.

## Further your understanding

- Why is it best practice to keep all the logic related to what is displayed in the `buildForm()` method?
- Why do we use `$form_state->get()` or `$form_state->set()` to read/write the form's internal storage in this example?
- There are lots of examples of using `#ajax` with forms in the [Examples for Developers project](https://www.drupal.org/project/examples). We recommend browsing through those to further your understanding.

## Additional resources

- [How to Build a Simple Form Using Ajax and Drupal 8](http://valuebound.com/resources/blog/how-to-build-a-simple-form-using-ajax-drupal-8) (valuebound.com)
- [Checklist of things to consider when working with Ajax](https://drupal.stackexchange.com/questions/188730/how-can-i-implement-ajax-form-submission) (drupal.stackexchange.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Create a Dependent Dropdown with Ajax](/tutorial/create-dependent-dropdown-ajax?p=2730)

Clear History

Ask Drupalize.Me AI

close