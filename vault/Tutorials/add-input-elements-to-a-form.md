---
title: "Add Input Elements to a Form"
url: "https://drupalize.me/tutorial/add-input-elements-form?p=2734"
guide: "[[develop-forms-drupal]]"
---

# Add Input Elements to a Form

## Content

Module developers can add new elements to a form by adding their definition to the `$form` array in the `buildForm()` method of their controller or via an implementation of `hook_form_alter()`. Doing so requires knowing the element `#type`, and details about any element-type-specific properties.

In this tutorial we'll:

- Determine the element type to use for the HTML input element we want to use
- Consult the documentation for the two form element types we're using
- Add a checkbox and a select list to our form via the `buildForm()` method of our form controller

By the end of this tutorial you'll know how to add new elements to an existing `$form` array in order to collect additional data from users.

## Goal

Update the form created in [Define a New Form](https://drupalize.me/tutorial/define-new-form-controller-and-route) to add a checkbox and a select list.

## Prerequisites

- [Define a New Form](https://drupalize.me/tutorial/define-new-form-controller-and-route)
- [What Are Render Elements?](https://drupalize.me/tutorial/what-are-render-elements)

## Code examples

The code for the examples in this tutorial may be found in the [Examples for Developers'](https://www.drupal.org/project/examples) *form\_api\_example* module.

## Adding input elements to a form

New elements are added to the `$form` array in the `buildForm()` method of a form controller, or via implementations of `hook_form_alter()`.

Some things to keep in mind:

- The `#type` property must be set. It determines what kind of `<input>` element will be used, and what HTML will be generated.
- The `#title` property must be set.
- Using `#required` is an easy way to ensure that a form field has a value when submitted. Drupal will automatically check required elements and raise an error if they are left empty.
- Some elements (*textfield*, *tel*, *password*, *email*, and *url*) support the `#pattern` property. Set this to a regular expression that should be used to validate the element, both client side and sever side.
- The key of the array used to describe an element is the name used to access the element's value later in the `$form_state` object.
- Elements can be nested in the `$form` array. For some, like textfields in a `#fieldset`, this is the expected behavior. This can be a nice way to help keeps things organized when forms get really large.

See examples of existing element types and learn more about how to locate and consume the documentation for element types in the [Form Elements Reference](https://drupalize.me/tutorial/form-element-reference) tutorial.

### Choose an element `#type`

Start by choosing the type of element, or elements, that you want to add. This will dictate the value of the `#type` property.

We'll use [checkbox](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Checkbox.php/class/Checkbox) and [select](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Select.php/class/Select). The value to use for `#type` can be determined by checking the PHP attributes for the class that defines the element, or by looking at the list of elements here: <https://api.drupal.org/api/drupal/elements>.

Image

![Screenshot of documentation for Checkbox class with annotation highlighted to show where it is on the page.](/sites/default/files/styles/max_800w/public/tutorials/images/form_api-form-element-annotation.png?itok=8WigUMGI)

Note that when constructing forms, render elements (extend `RenderElementBase`) will produce just HTML output, while form elements (extend `FormElementBase`) will produce both HTML output in the form of some kind of widget, and allow for collection and processing of user data input into that widget.

### Check the documentation

Consult the documentation for the selected element. This will provide information about any element-type-specific properties you need to be aware of. You will also see usage examples in most cases.

Image

![Screenshot showing documentation for checkbox element with custom properties highlighted](/sites/default/files/styles/max_800w/public/tutorials/images/form-api_element-documentation-properties.png?itok=f_ptQDHs)

The best place to look for documentation is the primary `@docblock` for the class that implements the form element type in question. We've found that in some cases the documentation there isn't great, but that you can often dig into the various methods for the class and find more documentation, especially with "processing" methods.

### Add the element to the `$form` array

In the `buildForm()` method of your controller or in your implementation of `hook_form_alter()`, add a new entry to the `$form` array that defines the new element(s) you want to add.

Example building on the controller created in [Define a New Form](https://drupalize.me/tutorial/define-new-form-controller-and-route):

```
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

  // Add a new checkbox element.
  $form['skip_validation'] = [
    '#type' => 'checkbox',
    '#title' => $this->t('Skip validation'),
    '#description' => $this->t('Allow the use of a title with fewer than 5 characters.'),
  ];

  // Add a new select element.
  $form['direction'] = [
    '#type' => 'select',
    '#title' => $this->t('Choose a direction'),
    // #options is a select element-type-specific property
    // that defines the options that should be available in
    // the select list. The key is the value that will be used
    // when the form is submitted, and the value is what will
    // be shown to the user.
    '#options' => [
      'right' => $this->t('Right'),
      'left' => $this->t('Left'),
    ],
  ];

  $form['actions'] = [
    '#type' => 'actions',
  ];

  $form['actions']['submit'] = [
    '#type' => 'submit',
    '#value' => $this->t('Submit'),
  ];

  return $form;
}
```

The result should look like this:

Image

![Screenshot of the form generated by the code above showing the new checkbox and select elements](/sites/default/files/styles/max_800w/public/tutorials/images/form-api_simple-form-with-extras.png?itok=gTNVvOT9)

In our experience the best way to familiarize yourself with the various element types available and their properties is through experimentation. So we highly encourage you to create a form and start playing around, or start hacking on the examples in the *[form\_api\_example](https://www.drupal.org/project/examples)* module.

## Recap

In this tutorial we added a checkbox and a select list to an existing form. We did so by first determining the value to use for the `#type` key of the array defining the new element. Then we looked up details about the element in the documentation. And finally we added two entries to the `$form` array returned by our controller.

Next: [Learn how to add additional validation to your form](https://drupalize.me/tutorial/validate-form-input).

## Further your understanding

- Install the *form\_api\_example* module and view the **Common input elements** example form. Then inspect the related code.
- Check out the list of `FormElements` provided by core here <https://api.drupal.org/api/drupal/elements>.
- Can you identify a couple of elements that don't directly correspond to a standard HTML `<input>` element? What do they do?

## Additional resources

- [Provide Default Values for Form Elements](https://drupalize.me/tutorial/provide-default-values-form-elements) (Drupalize.Me)
- [Define a New Render Element Type](https://drupalize.me/tutorial/define-new-render-element-type) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Define a New Form Controller and Route](/tutorial/define-new-form-controller-and-route?p=2734)

Next
[Inject Services into a Form Controller](/tutorial/inject-services-form-controller?p=2734)

Clear History

Ask Drupalize.Me AI

close