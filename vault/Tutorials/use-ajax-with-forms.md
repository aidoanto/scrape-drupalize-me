---
title: "Use Ajax with Forms"
url: "https://drupalize.me/tutorial/use-ajax-forms?p=2730"
guide: "[[develop-forms-drupal]]"
order: 18
---

# Use Ajax with Forms

## Content

Asynchronous JavaScript And XML (**Ajax**) is a programming practice for building more complex, dynamic webpages using a technology known as XMLHttpRequest. It allows you to asynchronously perform server-side operations without requiring a refresh, thus allowing for more complex user interaction and, in some cases, improved user experience.

In this tutorial we'll:

- Define what Ajax is
- Look at how Ajax is implemented in the Drupal Form API
- Provide links to additional resources to learn more about implementing Ajax in your own forms

By the end of this tutorial you should be able to explain what Ajax is, when you might want to use it, and how to get started doing so with Drupal's Form API.

## Goal

Learn about what Ajax is, and how to implement it using Drupal's Form API.

## Prerequisites

- [What Are Render Elements?](https://drupalize.me/tutorial/what-are-render-elements)

## What is Ajax?

Ajax is the process of dynamically updating parts of the page's DOM based on data retrieved from the server using a background request. This is typically done by writing JavaScript that listens for a specific event such as a 'click' on a button, or a 'value change' on a textfield. When the action is detected, JavaScript makes a background HTTP request to the server, retrieves some additional information, and then inserts that new data into the DOM -- all without requiring a page reload.

Common examples include:

- Autocomplete fields
- Files being uploaded in the background while you continue to fill in the node-editing form
- Submitting a form that contains a poll and displaying the results without a page refresh

Drupal's Form API allows you to add Ajax features to a form without having to write any corresponding JavaScript. Instead, you use the `#ajax` property of a form element in a $form array, and Drupal will handle the rest for you.

Among other things, this ensures that Ajax is handled in a consistent way throughout Drupal, allowing anyone familiar with the system to quickly get up to speed with someone else's code. It also helps to avoid a lot of boilerplate code duplication. Much of the JavaScript you would write to perform an Ajax request is relatively boilerplate. If every module developer had to write their own implementation you would quickly end up with dozens of almost the same but slightly different implementations. This would be harder to test, harder to maintain, and ultimately harder for each of us to understand.

That doesn't mean you can't write your own JavaScript code to perform Ajax functionalities. And indeed you might need to in some cases where the built in API doesn't do everything you need. But, our recommendation is to always start by implementing the API, and only write your own when you really need to.

## Ajax for forms

When dealing with forms and Ajax it's important to keep in mind that you can do one of two things:

- Alter the form by adding, removing, or updating parts of the form. This results in an altered form that is still eventually submitted with a traditional HTTP POST request. Examples include: updating the content of a city dropdown after someone has chosen a value in the country dropdown; adding an additional textfield for collecting a person's name when the user clicks an 'Add person' button.
- Submit a complete form sending the HTTP POST request as an Ajax request -- triggering the validation and submission handling of the form. One examples: submitting a user's vote for a poll when they click the submit button and then displaying the aggregated results (instead of the form) after tallying their vote.

## `#ajax` works with any form element

The `#ajax` property is a base property for any form render element -- that is, any element type that extends the `FormElementBase` base class. So, it can be used with just about any element in a form.

The basic implementation process includes:

- Add the `#ajax` property to a form element in your form array
- Write a PHP function or method that is called when the defined event occurs. This callback processes the input and responds with special commands that existing JavaScript can interpret into client-side actions

By default, the system will attempt to choose the most appropriate event for the element: submit buttons will use 'mousedown', textfields use 'blur', and checkboxes use 'change.' This is, of course, configurable. (See `\Drupal\Core\Render\Element\RenderElementBase::preRenderAjaxForm`) But not all events are applicable for all elements.

The `#ajax` property is an array with the following possible keys:

- **callback**: The callback to invoke on the server side to handle the Ajax request.
- **wrapper**: The HTML 'id' attribute of the area where the content returned by the callback should be placed. Note that 'wrapper' is only used if the callback returns content and not when it returns JavaScript commands.
- **method**: The jQuery method for placing the new content (used with'wrapper'). Valid options are 'replaceWith' (default), 'append', 'prepend', 'before', 'after', or 'html'. See <http://api.jquery.com/category/manipulation/> for more information on these methods.
- **effect**: The jQuery effect to use when placing the new HTML (used with'wrapper'). Valid options are 'none' (default), 'slide', or 'fade'.
- **speed**: The effect speed to use (used with 'effect' and 'wrapper'). Valid options are 'slow' (default), 'fast', or the number of milliseconds the effect should run.
- **event**: The JavaScript event to respond to. This is selected automatically for the type of form element; provide a value to override the default.
- **prevent**: A JavaScript event to prevent when the event is triggered. For example, if you use event 'mousedown' on a button, you might want to prevent 'click' events from also being triggered.
- **progress:** An array indicating how to show Ajax processing progress. Can contain one or more of these elements:
  - **type**: Type of indicator: 'throbber' (default) or 'bar'.
  - **message**: Translated message to display.
  - **url**: For a bar progress indicator, URL path for determining progress.
  - **interval**: For a bar progress indicator, how often to update it.
- **url**: A [\Drupal\Core\Url](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Url.php/class/Url/) to which to submit the Ajax request. If omitted, defaults to either the same URL as the form or link destination is for someone with JavaScript disabled, or a slightly modified version (e.g., with a query parameter added, removed, or changed) of that URL if necessary to support Drupal's content negotiation. It is recommended to omit this key and use Drupal's content negotiation rather than using substantially different URLs between Ajax and non-Ajax.

From the list above, 'callback' and 'wrapper' are the two you'll use most. The others use sensible defaults but can be adjusted as required.

The best way to learn more about how this all works is through some examples. Check out these tutorials where we demonstrate:

- [Use Ajax to Submit a Form](https://drupalize.me/tutorial/use-ajax-submit-form)
- [Create a Dependent Dropdown with Ajax](https://drupalize.me/tutorial/create-dependent-dropdown-ajax)

## Recap

In this tutorial we briefly discussed what Ajax is, then looked at how form elements in Drupal use the `#ajax` property to allow forms to use Ajax without requiring developers to write any JavaScript.

## Further your understanding

- Can you give some examples of Ajax that you've seen used on other sites?
- What are the benefits of using `#ajax` instead of writing the JavaScript yourself?

## Additional resources

- [Ajax API](https://api.drupal.org/api/drupal/core%21core.api.php/group/ajax/) (api.drupal.org)
- [Difference Between Synchronous and Asynchronous Messaging?](http://peoplesofttutorial.com/difference-between-synchronous-and-asynchronous-messaging/) (peoplesofttutorial.com)
- [XMLHttpRequest](https://en.wikipedia.org/wiki/XMLHttpRequest) (wikipedia.org)
- [Drupal 8 Day: Demystifying AJAX Callback Commands in Drupal 8](https://www.youtube.com/watch?v=6YhJq01jlpY) by Mike Miles (youtube.com)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Create a Dependent Dropdown with Ajax](/tutorial/create-dependent-dropdown-ajax?p=2730)

Clear History

Ask Drupalize.Me AI

close