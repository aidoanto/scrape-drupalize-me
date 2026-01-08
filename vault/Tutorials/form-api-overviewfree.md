---
title: "Form API Overviewfree"
url: "https://drupalize.me/tutorial/form-api-overview?p=2734"
guide: "[[develop-forms-drupal]]"
---

# Form API Overviewfree

## Content

Drupal's Form API is a set of interfaces, utility classes, and conventions that when combined together allow module developers to create forms that collect, validate, and process user-submitted data. The Form API is closely related to the [Render API](https://drupalize.me/topic/render-api-how-output-content). It uses [Render Arrays](https://drupalize.me/tutorial/what-are-render-arrays) to define forms, and adds an additional level of [workflow and processing](https://drupalize.me/tutorial/form-api-life-cycle) to enhance the Render API with some features specific to handling forms.

Given that forms are one of the primary means of interacting with a Drupal site via the UI, understanding how the Form API works is a critical part of learning to develop modules for Drupal. While you may not need to know all the nitty-gritty details, every Drupal module developer is likely to encounter aspects of the Form API at some point. Understanding the basics should be considered required knowledge.

Theme developers are also likely to encounter some aspects of the Form API, as forms are inherently part of the look and feel of a site. Knowing how to make changes to the UX of a form is an important skill.

In this tutorial we'll:

- Describe what forms are and how they are used in Drupal
- Explain the relationship between Form API and the Render API
- List some of the benefits of using the Form API over generic HTML forms

By the end of this tutorial you should have a solid understanding of the role of the Form API in Drupal.

## Goal

Provide a high-level introduction to the Drupal Form API and an overview of what you'll need to learn to master it.

## Prerequisites

- [Render API Overview](https://drupalize.me/tutorial/render-api-overview)
- [Introduction to Interfaces](https://drupalize.me/videos/introduction-interfaces)

## Forms

Forms are how users interact with your Drupal application beyond just clicking on links. They allow users to do things like:

- Provide the necessary data to register an account
- Provide the ability to turn features on and off via checkboxes or sets of radio buttons in the user interface
- Change the color of the site header using a color picker widget

When we use the term *forms*, we mean: **the HTML that is provided to the user's browser for collecting input and the logic that happens on the backend to process that input when a user submits the form.**

As a module developer you'll build forms to collect data you want to store in the database. You might modify forms provided by other modules to add additional validation logic, or application-specific handling of collected data. And you'll use data collected via configuration forms to determine the context in which code in other portions of the application is executed.

Forms are a fundamental component of creating web applications.

## What is the Form API?

Drupal's Form API is an abstraction layer around standard HTML forms and HTTP form handling. It controls the life cycle of a form including form definition, display, validation, and processing. It provides helper utilities to make it easier for module developers to make use of HTTP POST data, sanitize user input, and encapsulate complex widgets into reusable components.

Any time you write code in a Drupal module or theme that creates or interacts with a form you'll use the Form API to do so.

Introduced in Drupal 4.7, conceptually, the current version of the Form API remains largely the same, though it's gotten both more capable and more complex over time as well as moving to a more object-oriented approach.

In Drupal, each form starts its life as a class that implements `\Drupal\Core\Form\FormInterface`. This class is often referred to as the *form controller*. A form controller provides an initial definition of the form via its `buildForm()` method and validation and submission handling via its `validateForm()` and `submitForm()` methods, respectively.

Additional modules can alter the base form definition through a series of [form alter hooks](https://drupalize.me/tutorial/alter-existing-form-hookformalter). Through hooks, modules can add new elements, modify existing ones, and insert additional handling logic for validation and submission.

Life cycle orchestration is handled by the `\Drupal\Core\Form\FormBuilder` service. In addition, various base classes such as `\Drupal\Core\Form\FormBase` provide convenient starting points for creating custom forms.

## Form arrays are render arrays

Form, or more precisely, `$form` arrays are render arrays.

The visual portions of all forms in Drupal are defined as [renderable arrays](https://drupalize.me/tutorial/what-are-render-arrays). In the case of a form this is commonly referred to as the `$form` array. These arrays are standard render arrays, and as such, you can use all the capabilities of render arrays to influence what the HTML output of an element looks like.

Forms also have some additional processing features that won't work for a standard content array. [Render elements](https://drupalize.me/tutorial/what-are-render-elements) of the type `FormElement` are intended for use within a `$form` array. These elements have some form-processing-specific properties like `#required`, and `#element_validate` in addition to the default set of properties provided for all renderable elements.

In addition, the Form API needs to handle incoming HTTP POST requests resulting from a form being submitted. So the API provides low-level handling of the data. It defines a set of conventions that allow you to declare how a form's data should be validated and what to do with the input once it's been collected.

Despite these differences, the two systems are closely related. Having a firm understanding of [Render Arrays](https://drupalize.me/tutorial/what-are-render-arrays) and [Render Elements](https://drupalize.me/tutorial/what-are-render-elements) will go a long way towards helping you better understand the nuances of the Form API.

[Learn more about defining `$form` arrays](https://drupalize.me/tutorial/add-input-elements-form).

## Benefits of using the Form API

Some of the benefits that you get from Drupal's Form API include:

### Automatic workflow

The Form API provides a lot of the boilerplate code that is required to output an HTML form and safely process an incoming request. For the most part, all you'll need to do is define the relevant methods from `\Drupal\Core\Form\FormInterface`. Drupal will take care of calling them and executing your code at the appropriate points.

Additionally, HTTP POST data is generally pretty flat and unorganized. Drupal makes it easier to work with the POST data by performing some initial processing and encapsulating it into handy objects. This makes it easier for you as a developer to access and manipulate form data.

[Learn more about the life cycle of a Drupal form.](https://drupalize.me/tutorial/form-api-life-cycle)

### Security

Any time you're dealing with user input, you need to make sure it's sanitized and safe for the operation in which you want to use that input. The Form API handles some basic sanitization automatically and provides helpers that make it easy to deal with the rest. It also benefits from the fact that many different developers using dozens of different browsers, who have encountered hundreds of possible edge cases over the years, have contributed to ensuring the Form API is secure and robust.

### Consistent HTML output

Forms describe their input elements and buttons using the [Render API](https://drupalize.me/tutorial/render-api-overview). When those elements are converted to HTML it ensures that every `<textfield>`, `<tel>`, or `<submit>` button is presented using the same consistent template. You don't end up with one-offs or variations throughout your application that end up not looking correct.

Because it's using the Render API, it's run through Twig and Drupal's theme layer. So in the event that you do need to change the default output, you can.

[Learn more about the Render API.](https://drupalize.me/tutorial/render-api-overview)

### Ability to inject custom behaviors into any form

Drupal's form API uses [hooks](https://drupalize.me/tutorial/what-are-hooks) to allow developers to inject customizations into any form, not just the ones they create. This allows a custom module to, for example, add additional input elements and related validation and submission handling to the registration form provided by the user module without having to hack the user module.

[Learn more about altering existing forms.](https://drupalize.me/tutorial/alter-existing-form-hookformalter)

### Encapsulate complex logic into reusable components

By using the Render API to describe form elements we can create reusable widgets that are far more complex than regular HTML primitives. For example, the HTML, CSS, and JavaScript required to transform a set of five radio buttons into a five-star-rating widget can be wrapped up into a reusable component which a module developer can use with a few additional lines of code in their form controller. Core provides many of these elements as well as a way for you to define new ones yourself.

[Learn more about Render API elements.](https://drupalize.me/tutorial/what-are-render-elements)

## Recap

In this tutorial we introduced the Drupal From API at a high level, talked about the types of things you can expect to use the Form API to accomplish, and listed some of the benefits you get automatically as a result of using the Form API to handle display and processing of HTML forms.

Next: [Form API Life Cycle](https://drupalize.me/tutorial/form-api-life-cycle)

## Further your understanding

- What is the difference between a `$form` array and a render array?
- Find some examples of forms on your Drupal site. See if you can locate the code that generates those forms.

## Additional resources

- [DrupalCon Austin 2014: Fun with Forms in Drupal 8](https://www.youtube.com/watch?v=WRW8qNiPTHk) by Joe Shindelar (YouTube.com)
- [Form API](https://www.drupal.org/docs/drupal-apis/form-api) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Form API Life Cycle](/tutorial/form-api-life-cycle?p=2734)

Clear History

Ask Drupalize.Me AI

close