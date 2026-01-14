---
title: "Alter an Existing Form with hook_form_alter()"
url: "https://drupalize.me/tutorial/alter-existing-form-hookformalter?p=2734"
guide: "[[develop-forms-drupal]]"
order: 8
---

# Alter an Existing Form with hook_form_alter()

## Content

You'll often need to make minor, or major, alterations to an existing form provided by another module. The Form API allows you to alter any existing form through a series of hooks without having to change the existing module's code at all. This is probably one of the most powerful features of the Drupal Form API. Knowing how to implement and leverage `hook_form_alter()` and its variations is an essential skill for any module developer.

In this tutorial we'll:

- Learn how to implement `hook_form_alter()` and `hook_form_FORM_ID_alter()` in a module
- Modify existing elements, or add new elements, to a form provided by another module
- Understand how to add new validation and submission handlers when altering an existing form

By the end of this tutorial you should know how to alter almost everything about the way any form in Drupal works without having to hack the module that provides the form.

## Goal

Alter the existing user registration form: add a terms and conditions statement and a checkbox that users must click to verify they have read it.

## Prerequisites

- [Form API Life Cycle](https://drupalize.me/tutorial/form-api-life-cycle)
- [What Are Hooks?](https://drupalize.me/tutorial/what-are-hooks)

## Alter, don't hack

The rule of thumb when writing code for Drupal is that you shouldn't ever modify the code of Drupal core or a contributed module -- unless you're fixing a bug, or adding a new feature, that you intend to contribute back. Instead, you should use a hook or one of the various other methods for altering existing functionality. This is true of forms as well, and it's one of the biggest strengths of the Form API.

With forms, alteration is typically accomplished by implementing one of two hooks:

1. `hook_form_alter(&$form, \Drupal\Core\Form\FormStateInterface $form_state, $form_id)`
2. `hook_form_FORM_ID_alter(&$form, \Drupal\Core\Form\FormStateInterface $form_state, $form_id)`.

The arguments for both are the same:

- **$form**: Nested array of form elements that comprise the form.
- **$form\_state**: The current state of the form. The arguments that `\Drupal::formBuilder()->getForm()` was originally called with are available in the array `$form_state->getBuildInfo()['args']`.
- **$form\_id**: String representing the name of the form itself. Typically this assigned by the `::getFormId()` method of the class that defines the form.

The first one (`hook_form_alter`) is executed for all forms, and is useful when you want to make an alteration to more than one form. The latter (`hook_form_FORM_ID_alter`) allows you to target one specific form by replacing `FORM_ID` in the hook name with the actual ID of the form you want to alter.

[Learn about implementing hooks](https://drupalize.me/tutorial/implement-any-hook).

There is also a `hook_form_BASE_FORM_ID_alter()` hook -- it's worth pointing out that themes can alter forms as well. The complete call set would look something like this:

1. `{MYMODULE}_form_alter()`
2. `{MYMODULE}_form_BASE_FORM_ID_alter()`
3. `{MYMODULE}_form_FORM_ID_alter()`
4. `{MYMODULE_TWO}_form_alter()`
5. ... repeat for all enabled modules
6. `{MYTHEME}_form_alter()`
7. `{MYTHEME}_form_BASE_FORM_ID_alter()`
8. `{MYTHEME}_form_FORM_ID_alter()`

It's super common for a developer to want to alter an existing form provided by another module. Much of Drupal core's flexibility is achieved with these hooks. Even many of the systems within Drupal core use form alter hooks to work together. Dig around in the core code and you'll find all kinds of informative examples.

## Modify the user registration form

For this example we're going to add a checkbox, and some extra text, to the form displayed at *user/registration*. We're implementing a terms of service system, so the text will be our TOS, and the checkbox will be used to verify that a user has read the TOS before they can register. Doing this involves:

- Implementing `hook_form_alter()`
- Figuring out the ID of the form we want to alter
- Adding two new elements to the existing form
- Adding some additional validation to the existing form

### Find the ID of the form you want to alter

If you already know the ID of the form you want to alter, great. If not, here are a couple of ways to find out:

1. Find the class that defines the form, and look for the `::getFormId()` method. The string that it returns is the Form ID you can use
2. Start with an implementation of `hook_form_alter()`, and print out the `$form_id` variable. Then visit a page that contains the form in question.

```
  function form_api_example_form_alter(&$form, FormStateInterface $form_state, $form_id) {
    var_dump($form_id);
  }
```

### Add an implementation of `hook_form_FORM_ID_alter()`

In the *\*.module* file for your module, add an implementation of `hook_form_FORM_ID_alter()`. Replace `hook` with the machine name of your module. In this example, our module is `form_api_example`. Replace `FORM_ID` with the ID of the form you discovered in the previous step. In our case: `user_register_form`.

```
/**
 * Implements hook_form_alter().
 */
function form_api_example_form_user_register_form_alter(&$form, FormStateInterface $form_state, $form_id) {
	// Add your form-altering code here ...
}
```

### Alter the existing `$form`

Add a new checkbox field to confirm people have read the terms of service, and a markup element to display the text of the terms of service. Wrap them both in a fieldset for styling.

```
/**
 * Implements hook_form_alter().
 */
function form_api_example_form_user_register_form_alter(&$form, FormStateInterface $form_state, $form_id) {
  $form['tos'] = [
    '#type' => 'fieldset',
    '#title' => t('Terms of service'),
    '#weight' => -100,
  ];

  $form['tos']['tos_text'] = [
    '#markup' => t('Terms of service ... blah blah blah ...'),
    '#prefix' => '<p>',
    '#suffix' => '</p>',
  ];

  $form['tos']['tos_agree'] = [
    '#type' => 'checkbox',
    '#title' => t('I agree to the terms of service'),
  ];

  // Add a validation handler where we'll check the checkbox above.
  $form['#validate'][] = 'form_api_example_user_register_form_validate';
}
```

The `$form` array here works just like the `$form` array you would define in the `buildForm()` method of a form controller. You can add new elements, or make modifications to existing ones by altering or adding properties.

Note the addition of a validation handler. `$form['#validate'][] = 'form_api_example_user_register_form_validate';`. This will ensure that when someone submits this form a function named `form_api_example_user_register_form_validate()` will be called if it exists.

### Define the validation handler

In your *\*.module* file, define the function that will handle validation of the checkbox added in the previous step.

```
/**
 * Validate that the user has read the TOS during registration.
 */
function form_api_example_user_register_form_validate($form, FormStateInterface $form_state) {
  $tos_agree = $form_state->getValue('tos_agree');
  if ($tos_agree !== 1) {
    $form_state->setErrorByName('tos_agree', t('You must agree to the terms of service to continue.'));
  }
}
```

[Learn more about validation callbacks](https://drupalize.me/tutorial/add-validation-callback-existing-form).

### Test it out

Go register for a new account and confirm that the registration form displays the new fields above. Also test what happens if you leave the checkbox unchecked.

Image

![Screenshot of form showing the new terms of service fields added to the top of the registration form](../assets/images/form_api-tos_example.png)

## Recap

In this tutorial we learned how to alter an existing form using `hook_form_alter()` or one of its variants. We added a checkbox and some new text to the user registration form, as well as a validation handler that checks to ensure the checkbox was checked when the form is submitted -- all without making any changes to the original form controller.

## Further your understanding

- Explore the code in Drupal core [looking for implementations of `hook_form_alter()`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Form%21form.api.php/function/implementations/hook_form_alter/). It's a great way to be inspired and better understand the kinds of changes you can make.
- What's the difference between `hook_form_alter()` and `hook_form_FORM_ID_alter()`. When should you choose one over the other?
- What would happen if you implemented `hook_form_alter()` in a theme's *\*.theme* file and removed or added a `#required` property to an element?

## Additional resources

- [hook\_form\_alter() documentation](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Form%21form.api.php/function/hook_form_alter/) (api.drupal.org)
- [Using Drupal 8's Address Field in Custom Forms](https://atendesigngroup.com/blog/using-drupal-8s-address-field-custom-forms) (atendesigngroup.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Form Element Reference](/tutorial/form-element-reference?p=2734)

Next
[Retrieve and Display Forms](/tutorial/retrieve-and-display-forms?p=2734)

Clear History

Ask Drupalize.Me AI

close