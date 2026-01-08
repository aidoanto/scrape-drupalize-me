---
title: "Concept: Altering Existing Forms"
url: "https://drupalize.me/tutorial/concept-altering-existing-forms?p=3242"
guide: "[[drupal-module-developer-guide]]"
---

# Concept: Altering Existing Forms

## Content

One of the most powerful features of Drupal's Form API is the ability to alter nearly any aspect of the build, validate, or submit workflow in your custom code. Implementing `hook_form_alter` is a common task for Drupal module developers, allowing them to modify forms to customize administrative or user-facing interfaces.

In this tutorial, we'll:

- Explore the purpose and use case for `hook_form_alter` and related hooks.
- Learn how to target specific forms.
- Discover how to identify the form you wish to alter.

By the end of this tutorial, you should be able to select and implement the appropriate form alter hook to modify any form in Drupal.

## Goal

Learn to use form alter hooks to modify existing forms.

## Prerequisites

- [Overview: Drupal's Form API](https://drupalize.me/tutorial/overview-drupals-form-api)
- [Concept: What Are Hooks?](https://drupalize.me/tutorial/concept-what-are-hooks)
- [Implement hook\_help()](https://drupalize.me/tutorial/implement-hookhelp)

## What is `hook_form_alter`?

The hook, `hook_form_alter` (and its variants), allow a module to modify forms provided by any other module including Drupal core. Invoked during Drupal's form generation process, form alter hooks let you adjust the `$form` array and change how a form is rendered or processed. This hook is frequently used by developers due to its versatility.

## Use cases for altering forms

Altering forms can significantly improve functionality and user experience. Let's take a look at some practical examples.

### Adding or removing form fields

Collect extra information on the user registration form by adding a "Phone number" field. For example:

```
function mymodule_form_user_register_form_alter(&$form, \Drupal\Core\Form\FormStateInterface $form_state, $form_id) {
 $form['phone_number'] = [
   '#type' => 'tel',
   '#title' => t('Phone number'),
   '#required' => TRUE,
 ];
}
```

### Changing default values or display options

Customize options in a dropdown based on user roles. For example:

```
function mymodule_form_node_article_form_alter(&$form, \Drupal\Core\Form\FormStateInterface $form_state, $form_id) {
 if (in_array('editor', \Drupal::currentUser()->getRoles())) {
   // Pre-select the 'Featured' option for editors.
   $form['field_article_type']['#default_value'] = 'featured';
 }
}
```

### Altering form validation or submission

Add custom validation callbacks, such as checking for existing usernames in an external CRM. For example:

```
function mymodule_form_user_register_form_alter(&$form, \Drupal\Core\Form\FormStateInterface $form_state, $form_id) {
 $form['#validate'][] = 'mymodule_custom_user_validation';
}
```

These examples illustrate how form alterations can customize Drupal forms to meet specific requirements, improving data collection, user interaction, and system integration.

## Implementing `hook_form_alter`

Choose between `hook_form_alter` for all forms or `hook_form_FORM_ID_alter` for a specific form. For the latter, replace `FORM_ID` with the form's unique ID from its controller's `getFormId()` method.

Compare how the same form is targeted using either `hook_form_alter()` or `hook_form_FORM_ID_alter()`:

```
// hook_form_alter()
function mymodule_form_alter(&$form, \Drupal\Core\Form\FormStateInterface $form_state, $form_id) {
  if ($form_id === 'specific_form_id') {
    // Alterations to the specific $form.
  }
}

// hook_form_FORM_ID_alter()
function mymodule_form_specific_form_id_alter(&$form, \Drupal\Core\Form\FormStateInterface $form_state) {
  // Alterations to the specific $form.
}
```

### `$form` is passed by reference

The `$form` variable is [passed by reference](https://www.php.net/manual/en/language.references.pass.php), allowing direct modifications to the `$form` array. This means you need to ensure that the leading `&` is included in your implementation.

## Identifying forms to alter

To alter a form, find its ID using one of the methods below:

1. Check the `getFormId()` method in the form controller class.
2. Inspect the HTML source for the `form` tag's `id` attribute.
3. Implement `hook_form_alter()` and add `var_dump($form_id)` at the top of the function, then navigate to a page containing the form.

## Theme's can alter forms

Themes can also implement `hook_form_alter` in their *THEMENAME.theme* file. Changes to the form made in a theme should be restricted to presentation only, because the code in the *THEMENAME.theme* file may not be loaded during all phases of form processing.

## Recap

Drupal's `hook_form_alter()` and its variants are vital for customizing forms. These hooks provide a powerful method for customizing form behavior and appearance, enhancing the site's functionality and user experience.

## Further your understanding

- How could you use `hook_form_alter` to add a custom validation function to a form?
- What impact does the call order of hooks have when multiple modules alter the same form?

## Additional resources

- [Alter an Existing Form with hook\_form\_alter()](https://drupalize.me/tutorial/alter-existing-form-hookformalter) (Drupalize.Me)
- [hook\_form\_alter() documentation](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Form%21form.api.php/function/hook_form_alter/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Save Form Data Submitted by a User](/tutorial/save-form-data-submitted-user?p=3242)

Next
[Alter the User Registration Form](/tutorial/alter-user-registration-form?p=3242)

Clear History

Ask Drupalize.Me AI

close