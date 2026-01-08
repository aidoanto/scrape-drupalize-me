---
title: "Form Element Referencefree"
url: "https://drupalize.me/tutorial/form-element-reference?p=2734"
guide: "[[develop-forms-drupal]]"
---

# Form Element Referencefree

## Content

Drupal core provides a couple dozen different input `#type` elements that can be added to forms. This includes one for every standard HTML5 input element, and some Drupal-specific ones that encapsulate more complex interactions like uploading files. But how can you know what elements exist? Where do you find information about what Render API properties each element uses?

In this tutorial we'll:

- Define what `FormElements` are and how they relate to the Render API
- Find a list of all available input element types, additional documentation and usage examples
- See examples of the most common element types

By the end of this tutorial you should be able to discover the different types of elements you can add to a `$form` array and find usage examples for each.

## Goal

Provide a reference page for quickly finding information about available form element types.

## Prerequisites

- [What Are Render Elements?](https://drupalize.me/tutorial/what-are-render-elements)
- [Form API Overview](https://drupalize.me/tutorial/form-api-overview)

## Element types

List of form element types:

- [Button](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Button.php/class/Button) (`#type => 'button'`): Provides an action button form element.
- [Checkbox](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Checkbox.php/class/Checkbox/) (`#type => 'checkbox'`): Provides a form element for a single checkbox.
- [Checkboxes](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Checkboxes.php/class/Checkboxes/) (`#type => 'checkboxes'`): Provides a form element for a set of checkboxes.
- [Color](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Color.php/class/Color/) (`#type => 'color'`): Provides a form element for choosing a color.
- [Container](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Container.php/class/Container/) (`#type => 'container'`): Provides a render element that wraps child elements in a container.
- [Date](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Date.php/class/Date/) (`#type => 'date'`): Provides a form element for date selection.
- [Datelist](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Datetime%21Element%21Datelist.php/class/Datelist/) (`#type => 'datelist'`): Provides a datelist element which consists of a set of select elements pre-configured for choosing a date.
- [Datetime](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Datetime%21Element%21Datetime.php/class/Datetime/) (`#type => 'datetime'`): Provides a datetime element.
- [Email](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Email.php/class/Email/) (`#type => 'email'`): Provides a form input element for entering an email address.
- [EntityAutocomplete](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21Element%21EntityAutocomplete.php/class/EntityAutocomplete/) (`#type => 'entity_autocomplete'`): Provides an entity autocomplete form element.
- [File](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21File.php/class/File/) (`#type => 'file'`): Provides a form element for uploading a file.
- [Hidden](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Hidden.php/class/Hidden/) (`#type => 'hidden'`): Provides a form element for an HTML 'hidden' input element.
- [ImageButton](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21ImageButton.php/class/ImageButton/) (`#type => 'image_button'`): Provides a form element for a submit button with an image.
- [Item](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Item.php/class/Item/) (`#type => 'item'`): Provides a display-only form element with an optional title and description.
- [LanguageConfiguration](https://api.drupal.org/api/drupal/core%21modules%21language%21src%21Element%21LanguageConfiguration.php/class/LanguageConfiguration/)(`#type => 'language_configuration'`): Defines an element for language configuration for a single field.
- [LanguageSelect](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21LanguageSelect.php/class/LanguageSelect/) (`#type => 'language_select'`): Provides a form element for selecting a language.
- [MachineName](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21MachineName.php/class/MachineName/) (`#type => 'machine_name'`): Provides a machine name form element that consists of a textfield for human-readable input, and another textfield that automatically generates a machine name based on the input.
- [ManagedFile](https://api.drupal.org/api/drupal/core%21modules%21file%21src%21Element%21ManagedFile.php/class/ManagedFile/) (`#type => 'managed_file'`): Provides an AJAX/progress aware widget for uploading and saving a file. Files are saved as entities and managed by Drupal.
- [Markup](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Markup.php/class/Markup/) (`#type => 'markup'`): Provides a render element that passes through (without modification) any HTML provided. Most other element types are eventually coerced into a markup element.
- [Number](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Number.php/class/Number/) (`#type => 'number'`): Provides a form element for numeric input, with special numeric validation.
- [Password](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Password.php/class/Password/) (`#type => 'password'`): Provides a form element for entering a password, with hidden text.
- [PasswordConfirm](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21PasswordConfirm.php/class/PasswordConfirm/) (`#type => 'password_confirm'`): Provides a form element for double-input of passwords.
- [PathElement](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21PathElement.php/class/PathElement/) (`#type => 'path'`): Provides a form element to enter a path which can be optionally validated and stored as either a `\Drupal\Core\Url` value object or an array containing a route name and route parameters pair.
- [Radio](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Radio.php/class/Radio/) (`#type => 'radio'`): Provides a form element for a single radio button.
- [Radios](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Radios.php/class/Radios/) (`#type => 'radios'`): Provides a form element for a set of radio buttons.
- [Range](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Range.php/class/Range/) (`#type => 'range'`): Provides a slider for input of a number within a specific range.
- [Search](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Search.php/class/Search/) (`#type => 'search'`): Provides an HTML5 input element with type of "search".
- [Select](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Select.php/class/Select/) (`#type => 'select'`): Provides a form element for a drop-down menu or scrolling selection box.
- [Submit](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Submit.php/class/Submit/) (`#type => 'submit'`): Provides a form submit button.
- [Table](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Table.php/class/Table/) (`#type => 'table'`): Provides a render element for a table.
- [Tableselect](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Tableselect.php/class/Tableselect/) (`#type => 'tableselect'`): Provides a form element for a table with radios or checkboxes in left column.
- [Tel](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Tel.php/class/Tel/) (`#type => 'tel'`): Provides a form element for entering a telephone number.
- [Textarea](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Textarea.php/class/Textarea/) (`#type => 'textarea'`): Provides a form element for input of multiple-line text.
- [Textfield](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Textfield.php/class/Textfield/) (`#type => 'textfield'`): Provides a one-line text field form element.
- [Token](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Token.php/class/Token/) (`#type => 'token'`): Stores token data in a hidden form field. This is generally used to protect against cross-site forgeries. A token element is automatically added to each Drupal form, so you generally do not need to add one yourself.
- [Url](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Url.php/class/Url/) (`#type => 'url'`): Provides a form element for input of a URL, with built in validation for URL formatting.
- [Value](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Value.php/class/Value/) (`#type => 'value'`): Provides a form element for storage of internal information.
- [VerticalTabs](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21VerticalTabs.php/class/VerticalTabs/) (`#type => 'vertical_tabs'`): Provides a render element for vertical tabs in a form.
- [Weight](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21Weight.php/class/Weight/) (`#type => 'weight'`): Provides a form element for input of a weight. Weights are integers used to indicate ordering, with larger numbers later in the order.

## Form elements explained

The `buildForm(array $form, FormStateInterface $form_state)` method of a form controller returns an associative array, usually named `$form`, that defines the markup and input elements your form is composed of. Each element in the array consists of a set of properties, and possible nested child elements, that define the details Drupal uses to generate the HTML version of the form.

### Example form render array

```
$form['phone_number'] = array(
  '#type' => 'tel',
  '#title' => $this->t('Example phone'),
  '#default_value' => '867-5309',
);
```

These arrays are known as render arrays, and it's a good idea to be familiar with [their structure](https://drupalize.me/tutorial/what-are-render-arrays), and the related terminology.

Render arrays that define a form can make use of all standard Render API render element types, as well as the Form API-specific form element types. The latter are used primarily to define input and control elements on a form. These are used for the `#type` key of elements in a `$form` array, and also dictate which additional properties can be used for that element.

In addition to the set of default properties available for all render elements, form elements all have the following properties, as well as element-type-specific properties.

| Type | Description |
| --- | --- |
| **#after\_build** (array) | Array of callables or function names, which are called after the element is built. Arguments: `$element`, `$form_state`. |
| **#ajax** (array) | Array of elements to specify Ajax behavior. See the [Ajax API topic](https://api.drupal.org/api/drupal/core%21core.api.php/group/ajax/) for more information. |
| **#array\_parents** (string, read-only) | Array of names of all the element's parents (including itself) in the render array. See also `#parents`, `#tree`. |
| **#default\_value** | Default value for the element. See also `#value`. |
| **#description** (string) | Help or description text for the element. In an ideal user interface, the `#title` should be enough to describe the element, so most elements should not have a description. If you do need one, make sure it is translated. If it is not already wrapped in a safe markup object, it will be filtered for XSS safety. |
| **#disabled** (bool) | If `TRUE`, the element is shown but does not accept user input. |
| **#element\_validate** (array) | Array of callables or function names, which are called to validate the input. Arguments: `$element`, `$form_state`, `$form`. |
| **#field\_prefix** (string) | Prefix to display before the HTML input element. Should be translated, normally. If it is not already wrapped in a safe markup object, it will be filtered for XSS safety. |
| **#field\_suffix** (string) | Suffix to display after the HTML input element. Should be translated, normally. If it is not already wrapped in a safe markup object, will be filtered for XSS safety. |
| **#input** (bool, internal) | Whether or not the element accepts input. |
| **#parents** (string, read-only) | Array of names of the element's parents for purposes of getting values out of `$form_state`. See also `#array_parents`, `#tree`. |
| **#process** (array) | Array of callables or function names, which are called during form building. Arguments: `$element`, `$form_state`, `$form`. |
| **#processed** (bool, internal) | Set to `TRUE` when the element is processed. |
| **#required** (bool) | Whether or not input is required on the element. |
| **#states** (array) | Information about JavaScript states, such as when to hide or show the element based on input on other elements. |
| **#title** (string) | Title of the form element. Should be translated. |
| **#title\_display** (string) | Where and how to display the `#title`. Possible values: **before**: Label goes before the element (default for most elements). **after**: Label goes after the element (default for radio elements). **invisible**: Label is there but is made invisible using CSS. **attribute**: Make it the title attribute (hover tooltip). |
| **#tree** (bool) | `TRUE` if the values of this element and its children should be hierarchical in `$form_state`; `FALSE` if the values should be flat. See also `#parents`, `#array_parents`. |
| **#value\_callback** (callable) | Callable or function name, which is called to transform the raw user input to the element's value. Arguments:`$element`, `$input`, `$form_state`. |

You can find a complete list of the render element types provided by Drupal core at <https://api.drupal.org/api/drupal/elements>. Pay special attention to `FormElement` types, and note that you can click through to the class that defines the element type for additional documentation on element type specific properties and in most cases a usage example.

## Recap

In this tutorial we listed all the form element types provided by Drupal core and linked to the documentation for each. We also looked at the list of properties that are available for all form elements regardless of type. View the documentation for each individual element type to see documentation of type-specific properties.

## Further your understanding

- Check out the list of properties that are available for all render element types. Remember, those also apply to form elements.

## Additional resources

- [Element type list](https://api.drupal.org/api/drupal/elements) (api.drupal.org)
- [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Provide Default Values for Form Elements](/tutorial/provide-default-values-form-elements?p=2734)

Next
[Alter an Existing Form with hook\_form\_alter()](/tutorial/alter-existing-form-hookformalter?p=2734)

Clear History

Ask Drupalize.Me AI

close