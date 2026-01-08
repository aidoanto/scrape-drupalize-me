---
title: "Validate Form Input"
url: "https://drupalize.me/tutorial/validate-form-input?p=3255"
guide: "[[develop-forms-drupal]]"
---

# Validate Form Input

## Content

When a form is submitted you'll need to check the data input by the user to ensure that it matches certain constraints, and to raise errors when necessary. Is the email address in the proper format? Is the title field long enough? Does the ASIN ID entered match a valid Amazon product? This process is called validation and is handled by a combination of the `validateForm()` method of a form controller, and validation callbacks.

In this tutorial we'll:

- Explain the use case for both the `validateForm()` method of a form controller, and validation callbacks
- Discuss additional uses for validation handlers beyond just checking the length of a text field, or format of a phone number field

By the end of this tutorial you should know how to start adding custom validation logic to any form in Drupal.

## Goal

Understand the role of Form API validation handlers, and at a high level understand how to implement validation for your forms.

## Prerequisites

- [Form API Life Cycle](https://drupalize.me/tutorial/form-api-life-cycle)
- [Define a New Form Controller and Route](https://drupalize.me/tutorial/define-new-form-controller-and-route) - We'll be expanding on the form started in this tutorial.
- [Render API Callback Properties](https://drupalize.me/tutorial/render-api-callback-properties)

## A note on entities

If you're validating data related to an entity, either content or configuration, it is best practice to use the [Entity Validation API](https://drupalize.me/tutorial/entity-validation-api). This ensures that entities created via web services or other means are all subject to the same set of constraints.

## Where do I put the code?

There are a couple of ways you can tell Drupal what code you want to execute when validating a form.

- If your module defines the form controller, you can place your custom validation logic into the `validateForm()` method of the controller. [Learn how to do this](https://drupalize.me/tutorial/validate-form-form-controller).
- When using `hook_form_alter()` to influence an existing form, you can add additional callbacks to the `#validate` property of the top level `$form` array. This is useful when your validation logic requires knowledge of the values of more then one element in the form. [Learn how to do this](https://drupalize.me/tutorial/add-validation-callback-existing-form).
- When defining a new `FormElement`, or if your constraints are only relevant for a single element, you can use the`#element_validate` property of an individual element to specify additional validation callbacks. [Learn how to do this](https://drupalize.me/tutorial/validate-single-form-element).

## Inspecting values and raising errors

The `$form_state` object passed into your validation method or callback is responsible for controlling the flow and processing of the current form. It can be used to access the collected user input, and to raise errors on one or more elements if they fail to validate.

### Access user input via `$form_state`

Use `$form_state->getValue('element name')` to retrieve the value of a specific form element, where **element name** is the key used when adding the element to the `$form` array, as illustrated.

Image

![Screenshot of $form array in buildForm method with arrows pointing to keys of the array to show which ones are element names.](/sites/default/files/styles/max_800w/public/tutorials/images/form-api_element-name-example.png?itok=7yDPBatG)

### Log errors during validation with `$form_state`

Use `$form_state->setErrorByName($name, $message)` to raise an error for a specific element during validation, where `$name` is the name of the element, and `$message` is the error message you would like to display to the end user. Any time this method is called prevents the form from entering the submission phase, and instead redisplays the form to the user with errors highlighted. The Form API will call all validation handlers and aggregate the complete set of errors before redisplaying the form.

## Updating values during validation

Another common thing to do in a validate handler is initial data processing.

For example, imagine a form with a text field that collects a post to submit to the Twitter API. When the form is submitted the message should be posted, the ID of the new post collected, and finally, that post ID should be stored in Drupal. In this scenario you could use the validation callback to submit the data to the Twitter API and retrieve the new post ID, which allows you to raise an error on the form if anything doesn't work. For example, if the API is down, or the post doesn't pass the Twitter API validation. You could even pass along the error message from Twitter to the user.

The general rule of thumb is that by the time you get to the submission processing portion of the form's life cycle, all of the data in `$form_state` should be considered valid and complete.

When doing this, you can use the `$form_state->setValue($key, $value);` method to modify the value of an element.

This is a hypothetical example intended to demonstrate the concept:

```
public function validateForm(array &$form, FormStateInterface $form_state) {
  $twitter_account = $form_state->getValue('account');
  $twitter_post = $form_state->getValue('post');
  $continue = TRUE;

  if (empty($twitter_account)) {
    $form_state->setErrorByName('account', $this->t('Twitter account name is required.'));
    $continue = FALSE;
  }

  if (empty($twitter_post) || strlen($twitter_post) > 280) {
    $form_state->setErrorByName('post', $this->t('Twitter is required and must be less than 280 characters.'));
    $continue = FALSE;
  }

  if ($continue) {
    $twitter = new TwitterClient();
    $result = $twitter->post($twitter_account, $twitter_post);
    if (isset($result['errors'])) {
      $form_state->setError($form, $this->t('Unable to post to Twitter: @error', ['@errors' => $result['errors']->message]));
    }
    else {
      // Set the value of the post element to the returned UUID. The submit
      // handler can then store this in the DB.
      $form_state->setValue('post', $result['post']->uuid);
    }
  }
}
```

## Recap

In this tutorial we learned about the different ways you can add custom validation logic to a form. We looked at using an implementation of the `validateForm()` method on our form controller, as well as callback properties like `#validate` and `#element_validate`. We also saw examples of additional processing you may want to perform during the validation of a form.

Next, read about how to implement these different techniques:

- [Validate a Form via the Form Controller](https://drupalize.me/tutorial/validate-form-form-controller)
- [Add a Validation Callback to an Existing Form](https://drupalize.me/tutorial/add-validation-callback-existing-form)
- [Validate a Single Form Element](https://drupalize.me/tutorial/validate-single-form-element)

## Further your understanding

- Can you explain why when your form controller extends `FormBase` the `validateForm()` method is optional even though it's required by `FormInterface`?
- Learn more about the [Entity Validation API](https://drupalize.me/tutorial/entity-validation-api) for handling data stored as entities.
- Can you give an example use case (other than the one provided in this tutorial) where you might want to perform data processing beyond just simple validation in the validation handler for a form?

## Additional resources

- [Documentation for `FormStateInterface`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Form%21FormStateInterface.php/interface/FormStateInterface/) (api.drupal.org)
- [Inline Form Errors Module](https://www.drupal.org/docs/8/core/modules/inline-form-errors) (Drupal.org)
- [Examples for Developers project](https://www.drupal.org/project/examples) (Drupal.org)
- [What Are Hooks?](https://drupalize.me/tutorial/what-are-hooks) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Validate a Form via the Form Controller](/tutorial/validate-form-form-controller?p=3255)

Clear History

Ask Drupalize.Me AI

close