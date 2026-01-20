---
title: "Validate a Single Form Element"
url: "https://drupalize.me/tutorial/validate-single-form-element?p=3255"
guide: "[[develop-forms-drupal]]"
order: 14
---

# Validate a Single Form Element

## Content

When defining a new `FormElement` plugin, or if your constraints are only relevant for a single element, you can use the `#element_validate` property of an individual element to specify additional validation callbacks.

In this tutorial we'll:

- Add an `#element_validate` callback to a single element in a form to perform validation of just that element.

By the end of this tutorial you should know how to add `#element_validate` callbacks to any form element in Drupal.

## Goal

Validate that the value entered into the *textfield* of a form is at last 5 characters in length unless the user has chosen the *skip validation* option.

## Prerequisites

- [Form API Life Cycle](https://drupalize.me/tutorial/form-api-life-cycle)
- [Define a New Form Controller and Route](https://drupalize.me/tutorial/define-new-form-controller-and-route) - We'll be expanding on the form started in this tutorial.
- [Render API Callback Properties](https://drupalize.me/tutorial/render-api-callback-properties)

## When do I use this?

The most common use case for element-specific validation callbacks is when you're defining a new, reusable, `FormElement` type. For example, the FiveStar module might add a new form element, `'#type' => 'fivestar'` that the FiveStar module, and any other module, could use when defining a form. In order to ensure that the validation logic is triggered whenever the element is used, regardless of what form it's contained in, you'll need to attach that logic to the element itself, not the containing form.

This can also be useful when using `hook_form_alter()` to add additional *new* validation logic to a specific element. Though, you could also opt to [use a `#validate` callback](https://drupalize.me/tutorial/add-validation-callback-existing-form) on the form, depending on your needs.

Remember that in this example our form has the following two fields:

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

Unlike in the other two examples where we check the value of both the *title* and *skip\_validation* fields in our validation logic, in this example we can only reliably validate values contained within a single element. This is because we cannot anticipate the ways that our element will be used, so we can't ensure that there will always be a matching *skip\_validation* element to go with our *title* element.

Check out `\Drupal\Core\Render\Element\Number` for an example of using an `#element_validate` callback when defining a new form element type.

## Perform validation using an `#element_validate` callback

Remember that in this case, you don't always know what context your element is going to be used in, so you can not always rely on the `$form` or `$form_state` object containing other fields or information that you are not explicitly defining. So in this example we'll just validate the length of the *title* field.

### Add an `#element_validate` callback

Either in the element definition or in an implementation of `hook_form_alter`, add a callback to the `#element_validate` property.

```
$form['title'] = [
  '#type' => 'textfield',
  '#title' => $this->t('Title'),
  '#description' => $this->t('Title must be at least 5 characters in length.'),
  '#required' => TRUE,
  '#element_validate' => [[$this, 'validateLength']],
];
```

### Define your callback

```
/**
 * Element specific validation callback.
 */
public function validateLength($element, FormStateInterface $form_state, $form) {
  $title = $form_state->getValue('title');
  if (strlen($title) < 5) {
    // Set an error for the form element with a key of "title".
    $form_state->setError($element, $this->t('The title must be at least 5 characters long.'));
  }
}
```

Read more about [defining new element types](https://drupalize.me/tutorial/define-new-render-element-type).

## Recap

In this tutorial we learned how to add an `#element_validate` validation callback to a specific element in a form. This can be done either when the form element is added to the `$form` array, via an implementation of `hook_form_alter()`, or by the `FormElement` definition.

## Further your understanding

- Find a couple of examples of `#element_validate` being used in Drupal core and see if you can explain what they are doing. Can you find any instances of `#element_validate` being used outside of the context of defining a new `FormElement`?

## Additional resources

- [Documentation for `FormStateInterface`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Form%21FormStateInterface.php/interface/FormStateInterface/) (api.drupal.org)
- [Examples for Developers project](https://www.drupal.org/project/examples) (Drupal.org)
- [What Are Hooks?](https://drupalize.me/tutorial/what-are-hooks) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add a Validation Callback to an Existing Form](/tutorial/add-validation-callback-existing-form?p=3255)

Clear History

Ask Drupalize.Me AI

close