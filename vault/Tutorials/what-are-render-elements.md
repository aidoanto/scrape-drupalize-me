---
title: "What Are Render Elements?"
url: "https://drupalize.me/tutorial/what-are-render-elements?p=2775"
guide: "[[output-and-format-data-code]]"
---

# What Are Render Elements?

## Content

One of the central components of Drupal's Render API is render elements. You can think of them as prepackaged [render arrays](https://drupalize.me/tutorial/what-are-render-arrays) or shortcuts you can use to describe common things, like tables, links, and form elements, in a consistent way. In this tutorial we'll take a more in-depth look at the use of the `#type` property in render arrays in order to answer questions like:

- What are render elements, and what is their use case?
- Where can I find more information about available element types?

By the end of this tutorial you should be able to identify individual render element types within a larger render array, find the relevant documentation for specific types of render elements, and explain the use case for render elements.

## Goal

Explain the concept of render elements and how they relate to Drupal's Render API.

## Prerequisites

- [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays)
- Render elements are [plugins](https://drupalize.me/tutorial/what-are-plugins), so you'll want to know how to define new plugins.

Sprout Video

## What are render elements?

Render elements, or **element types**, are essentially prepackaged [render arrays](https://drupalize.me/tutorial/what-are-render-arrays), with a bunch of sane defaults for common properties allowing for a sort of shorthand for describing a chunk of data.

For example, when creating a render array you might write something like the following:

```
$form['file_example_fid'] = array(
  '#title' => t('Image'),
  '#type' => 'managed_file',
  '#description' => t('Upload your picture.'),
  '#upload_location' => 'public://example_files/',
);
```

When the renderer encounters this element with the `#type => 'managed_file'` property it will treat it as a render element of the type `#managed_file`, which corresponds to the `\Drupal\file\Element\ManagedFile` plugin. During the rendering process the plugin will expand the provided definition to include any default properties set by the `\Drupal\file\Element\ManagedFile` element type. This includes things like `#pre_render` and `#post_render` callbacks that are used to expand what started out as a `#managed_file` element into a handful of elements—including a file upload field, a submit button, and a preview of any previously uploaded file if present. The beauty is, you can change the way any of those defaults work, or you can leave everything as-is and get a standard AJAX-enabled file upload widget without having to code it from scratch every time.

Image

![Diagram showing process of converting a render array with a managed_file element in a custom module to HTML by expanding the definition to include defaults from the element type, executing preprocess callbacks to split the element into multiple sub-elements, and then converting it all to HTML](/sites/default/files/styles/max_800w/public/tutorials/images/render-api-rendering-an-element.png?itok=7Gn1hocO)

[View full size](https://drupalize.me/sites/default/files/tutorials/images/render-api-rendering-an-element.png).

Take a look at [`\Drupal\file\Element\ManagedFile`](https://api.drupal.org/api/drupal/core%21modules%21file%21src%21Element%21ManagedFile.php/class/ManagedFile/) to see this in action. The [`\Drupal\file\Element\ManagedFile::getInfo()`](https://api.drupal.org/api/drupal/core%21modules%21file%21src%21Element%21ManagedFile.php/function/ManagedFile%3A%3AgetInfo/) and [`\Drupal\file\Element\ManagedFile::processManagedFile()`](https://api.drupal.org/api/drupal/core%21modules%21file%21src%21Element%21ManagedFile.php/function/ManagedFile%3A%3AprocessManagedFile/) are particularly informative.

This pattern can be applied to other complex display elements as well. Examples include:

- Five star voting widgets
- Table elements that can format an array of data into an HTML table
- A placeholder that is dynamically replaced by a list of user-configured content

Render elements powerfully encapsulate complex logic. Once you understand them, they become shortcuts that are easy to remember and reuse.

## More than just markup

Many render elements contain additional functionality beyond just displaying some content as HTML. The HTML, CSS, and JavaScript that make up the user-facing portion of the element often works in tandem with PHP on the back-end to create interactive elements, validate input for form fields, and more.

The `#managed_file` element, for example, also encapsulates the logic required to process a file uploaded via a form, validate its size and mime-type, turn it into a valid file entity, and present the newly created entity object to the code handling the form submission -- all things that a module developer would otherwise need to hand-code.

## Why render elements?

- Render elements allow for encapsulation of complex display logic into components that can be reused by others without having to fully understand the underlying parts.
- Using a library of elements to define common components on a page allows for consistent display and handling of those elements, in the same way a front-end developer might create a pattern library, or a UX designer might create a style guide.

## Types of render elements

There are 2 types of render element plugins:

1. **Generic elements:** Generic render element types encapsulate logic for generating HTML and attaching relevant CSS and JavaScript to the page. These include things like link, table, and drop button elements.
2. **Form input elements:** Most of the render element types provided by core represent the various widgets you might use on a form. Text fields, password fields, file upload buttons, and vertical tabs, to name a few. These elements are intended to be used in conjunction with a form controller class and have additional properties such as `#required` and `#element_validate`, related to their use as part of a form.

## Documentation of render elements and their properties

You can find a complete list of the render element types provided by Drupal core at <https://api.drupal.org/api/drupal/elements>. When defining a `#type` element in a render array you will use a combination of element type-specific properties, and generic properties that apply to all elements.

Clicking the link for any element in that list will take you to the documentation for the class defining the element, including documentation for any element type-specific properties as well as code examples.

You can find a complete list of properties common to all elements in our [Render Arrays](https://drupalize.me/tutorial/what-are-render-arrays) tutorial.

## Define a new render element type

Modules can define new render element types by [creating new plugins](https://drupalize.me/tutorial/implement-plugin-using-php-attributes). Doing so adds another potential value that someone could use when setting the `#type` property in a render array. This is useful for modules that want to provide user-facing widgets with some amount of interactivity, especially if they want to allow other modules to reuse, and customize, the widget.

Generic render element plugins:

- Implement `\Drupal\Core\Render\Element\ElementInterface`
- Use `\Drupal\Core\Render\Attribute\RenderElement` attributes
- Go in plugin namespace, `Element`
- Usually extend the `\Drupal\Core\Render\Element\RenderElementBase` base class

Render elements representing form input elements:

- Implement `\Drupal\Core\Render\Element\FormElementInterface`
- Use `\Drupal\Core\Render\Attribute\FormElement` attributes
- Go in plugin namespace, `Element`
- Usually extend the `\Drupal\Core\Render\Element\FormElementBase` base class

## Recap

In this tutorial, we said that render elements, indicated by use of the `#type` property in a render array, are prepackaged definitions for complex render array elements. They are defined as plugins, and can be either a generic HTML-producing render element, or a form element intended for use as part of the form generation and submission process.

## Further your understanding

- Create a render array that uses the `'#type' => 'table'` element type to display a table with columns for first name, last name, and age. Then include all the members of your family in the table.
- Take some time to walk through the code that defines the `#managed_file` render element, especially the `\Drupal\file\Element\ManagedFile::processManagedFile()` method which demonstrates how a render element can expand itself into multiple child elements.

## Additional resources

- [Learn more about callback properties like `#pre_render`](https://drupalize.me/tutorial/render-api-callback-properties) (Drupalize.Me)
- [A list of available element types in core](https://api.drupal.org/api/drupal/elements) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[What Are Render Arrays?](/tutorial/what-are-render-arrays?p=2775)

Next
[Define a New Render Element Type](/tutorial/define-new-render-element-type?p=2775)

Clear History

Ask Drupalize.Me AI

close