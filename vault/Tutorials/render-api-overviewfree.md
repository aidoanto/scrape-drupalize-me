---
title: "Render API Overviewfree"
url: "https://drupalize.me/tutorial/render-api-overview?p=2775"
guide: "[[output-and-format-data-code]]"
---

# Render API Overviewfree

## Content

The Render API consists of two parts: structured arrays that provide data and hints about how that data should be rendered, and a rendering pipeline that can be used to render these arrays into various output formats. Understanding at least the basics of how the Render API works, the difference between elements and properties, and the concept of callback functions is an integral part of learning Drupal.

In this tutorial we'll:

- Look at the fundamentals of the Drupal Render API
- Point to additional material to provide more detail about the inner workings of the Render API and how content is output in Drupal

## Goal

- Understand at a high-level what the Render API is, when you'll encounter it, and the main components of the system.

## Prerequisites

- None.

## Watch: Render API Overview

Sprout Video

## Contents

- [What is the Render API?](#what)
- [Render arrays](#render-arrays)
- [Render elements](#render-elements)
- [Render pipeline](#render-pipeline)
- [Render caching](#render-caching)

## What is the Render API?

In order to ensure that a theme can completely customize the markup of a page, we module developers should avoid writing strings of HTML markup for pages, blocks, and other user-visible output in our modules. Instead we should return structured content in the form of *render arrays*. This structured data provides hints about what type of information it contains, and how it should be converted to HTML, but leaves the actual rendering of HTML to the theme layer, ensuring that themes get the last say in how the data is actually output.

Doing this also increases usability by ensuring that the markup used for similar functionality on different areas of the site is the same. This gives users fewer user interface patterns to learn. For example, forms describe their input elements and buttons using the Render API. When those elements are converted to HTML it ensures that every `<textfield>`, `<tel>`, or `<submit>` button is presented using the same consistent template. You don't end up with one-offs or variations throughout your application that end up not looking correct.

Drupal's Render API comprises render arrays, render elements, the render pipeline, and render caching.

## Render arrays

Render arrays are the core structure of the Render API. As module and theme developers, you're likely to spend most of your time working with render arrays. If you've looked at the code for any controller or other content-producing system in Drupal you've probably seen a render array before. Here's an example:

```
$build['table'] = [
  '#type' => 'table',
  '#caption' => $this->t('Our favorite colors.'),
  '#header' => [$this->t('Name'), $this->t('Favorite color')],
  '#rows' => [
    [$this->t('Amber'), $this->t('teal')],
    [$this->t('Addi'), $this->t('green')],
    [$this->t('Blake'), $this->t('#063')],
    [$this->t('Enid'), $this->t('indigo')],
    [$this->t('Joe'), $this->t('green')],
  ],
];
```

These structured arrays are used to provide data and hints as to how that data should be rendered. For example, you might use a render array to represent the content of a field -- including not only the value entered into the field by an editor but also information about the type of field, the entity the field is attached to, and some suggestions as to which Twig template file to use when outputting the content.

As a module developer you should use render arrays to define the content that your module would like to output to the page. As a theme developer you'll manipulate render arrays in order to modify the way that content is rendered and what the final HTML output contains.

[Learn more about render arrays](https://drupalize.me/tutorial/what-are-render-arrays).

## Render elements

Render elements, or **element types**, are essentially prepackaged render arrays, with a bunch of sane defaults for common properties allowing for a sort of shorthand for describing a chunk of data. Similar to the idea of web components, they can be used to define a common pattern in a way that is easy to reuse.

Render elements are defined by modules and Drupal core subsystems. The most common use case is in the creation of elements for use in defining forms. A form, for example, is defined as a render array that consists of various render elements like text fields, a file upload field, and a submit button.

The use of render elements isn't limited to forms; they're also commonly used to encapsulate complex display logic, especially that which involves possible user interactivity.

As a module developer you'll use render elements extensively when defining forms, as well as occasionally when describing the content your module outputs. As a theme developer you'll primarily alter render elements within an existing render array in order to change the resulting HTML output, such as adding class attributes to specific fields on a form.

[Learn more about render elements](https://drupalize.me/tutorial/what-are-render-elements).

## Render pipeline

The render pipeline is the process that Drupal goes through to convert an HTTP request into a valid response. This involves getting an HTTP request, matching it to a route, returning a render array from the defined controller, converting that array to HTML or another output format, and then returning a response. As a module developer this mostly happens behind the scenes, but understanding the process will help you to better understand how to use render arrays in your own code.

[Learn more about the render pipeline](https://drupalize.me/tutorial/render-pipeline), and [the use of Renderers](https://drupalize.me/tutorial/render-api-renderers) to convert arrays to HTML.

## Render caching

Image

![Render API caching flow diagram](../assets/images/render-api-lookup-flow.png)

Covering the full extent of how caching works with the Render API is beyond the scope of this tutorial. However, it is worth mentioning at least briefly.

As you might expect, some Render API elements can become fairly complex, and the calculation of what the final HTML output should look like often involves looking up content in the database, checking multiple conditions, and various other tasks. This can cause turning a render array into HTML to become quite expensive. In order to speed up this process, whenever possible the Render API will cache the HTML created by rendering an element and re-use it on future requests.

Information about an individual element's cacheability, the various contexts in which it is rendered, and how it affects any child elements or the parent element are contained within the `#cache` property.

[Learn more about caching and render arrays](https://drupalize.me/tutorial/add-cache-metadata-render-arrays).

## Recap

In this tutorial we got a high-level overview of the components that make up the Render API, including render arrays, render elements, the render pipeline, caching, and the overall use-case for the system. We also noted that as a module developer any time your code is outputting content intended to be displayed for users it should do so using the Render API.

## Further your understanding

- [Learn more about render elements](https://drupalize.me/tutorial/what-are-render-elements)
- [Learn more about render arrays](https://drupalize.me/tutorial/what-are-render-arrays)
- [Learn more about the render pipeline](https://drupalize.me/tutorial/render-pipeline)
- [Learn more about render caching](https://drupalize.me/tutorial/add-cache-metadata-render-arrays)

## Additional resources

- This DrupalCon NOLA session, ["Aha! Understanding and Using Render Arrays in Drupal 8"](https://events.drupal.org/neworleans2016/sessions/aha-understanding-and-using-render-arrays-drupal-8), provides a good overview of the Render API, its use case, and a little history. (events.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[What Are Render Arrays?](/tutorial/what-are-render-arrays?p=2775)

Clear History

Ask Drupalize.Me AI

close