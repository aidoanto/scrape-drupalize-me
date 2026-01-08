---
title: "Form API Life Cycle"
url: "https://drupalize.me/tutorial/form-api-life-cycle?p=2734"
guide: "[[develop-forms-drupal]]"
---

# Form API Life Cycle

## Content

This tutorial will help you understand the complete life cycle of a Drupal form: receiving the request from a browser, displaying a page with a form, rendering the form as HTML, handling the submitted form, validating input, handling errors, and processing data. We'll point out the common places that module developers might want to inject additional functionality into the process. And we'll link to tutorials with more details about each integration point in a form's life cycle.

In this tutorial, we'll:

- List the steps of the life cycle of a Drupal form.
- Describe how Drupal determines which form to display, and which form handles an HTTP POST request.
- Understand the role of `FormStateInterface` in the life cycle of a form.

By the end of this tutorial, you should have a solid understanding of the life cycle of a form within Drupal.

## Goal

Learn about the life cycle of a form in a Drupal site, so that you understand how forms are created, processed, and at which points they can be altered.

## Prerequisites

- [Form API Overview](https://drupalize.me/tutorial/form-api-overview)
- [Routing](https://drupalize.me/topic/routes)
- [Controllers](https://drupalize.me/topic/controllers)

## The `FormBuilder` service

Life cycle orchestration is handled by the `\Drupal\Core\Form\FormBuilder` service. Base classes such as `\Drupal\Core\Form\FormBase` provide convenient starting points for creating custom forms.

## The life cycle of a form

Unraveling the flow that a form goes through can be helpful when it comes to better understanding what code is getting called when. In order to do this it helps to step back a little bit and include Drupal, the user, and their browser in the scope of what we're looking at. Here's the typical life cycle of a form at a high level:

Image

![Life cycle of a form described below](/sites/default/files/styles/max_800w/public/tutorials/images/form_api-life-cycle.png?itok=qXFG518T)

1. **Request:** A user visits a page on your site like *<https://example.com/survey>*
2. **Routing:** Drupal's routing system determines that the path */survey* will display a form provided by the class `Drupal\example\Form\Survey` and invokes the form builder service with this information. The form builder (`\Drupal\Core\Form\FormBuilder`) retrieves the information it needs in order to display the HTML form from the form controller class and by executing various hooks
3. **Display:** Drupal renders the HTML for the page, and the user's browser displays the HTML form
4. **Submit:** The user fills in the form and submits it, causing their browser to issue an HTTP POST request to the same path the form was displayed at, i.e. */survey*. As before, the routing system dispatches to the form builder service. This time the request object contains POST data so the form builder calls the validation handlers from the controller which in turn check the user input for any errors
5. **Validate:** If an error is found it's flagged, and the form builder re-renders the form, this time with default values set for any fields previously filled in and information about the errors. It returns the HTML form again so that the user can correct the errors.
6. **Error handling:** If no errors are encountered, or after the errors are corrected and the form is submitted again, the form builder calls the appropriate submission processing handlers from the form controller which process the user input and perform any necessary actions
7. **Process:** Finally, the form controller dictates to the form builder what to do next. For example, redirect the user to another page like */survey/thank-you*, or display the form on */survey* again with a message at the top saying, "Thanks. Would you like to add another record?"

## Form controllers

Each form is defined as a class that implements `\Drupal\Core\Form\FormInterface` and is often referred to as the *form controller*. The form builder service takes care of calling the appropriate methods on the form controller in order to build, validate, and process submission of a form. From the perspective of a form controller, there are 3 main phases you'll need to write code for.

### Phase 1: Build

`MyFormController::buildForm()`

- Triggered when a user requests a page that contains a form.

In this phase, the form controller builds the initial `$form` array representing the form to display to the user.

Learn more about building a form.

- [Define a New Form Controller and Route](https://drupalize.me/tutorial/define-new-form-controller-and-route).
- [Inject Services into a Form Controller](https://drupalize.me/tutorial/inject-services-form-controller)
- [Add Input Elements to a Form](https://drupalize.me/tutorial/add-input-elements-form)
- [Form Element Reference](https://drupalize.me/tutorial/form-element-reference)
- [Provide Default Values for Form Elements](https://drupalize.me/tutorial/provide-default-values-form-elements)
- [Create a Dependent Dropdown with Ajax](https://drupalize.me/tutorial/create-dependent-dropdown-ajax)
- [Use Ajax to Submit a Form](https://drupalize.me/tutorial/use-ajax-submit-form)

### Phase 2: Validate

`MyFormController::validateForm()`

- Triggered when the user submits a form.

In this phase, the form controller can perform any logic required to validate the user input collected by the form and optionally raise errors and request things get corrected. This phase is also often used to perform required data transformations where the code needs to do some additional processing of data before making use of it, but where that processing might result in an error that you want the user to correct before proceeding. For example: handling file uploads or looking up the unique ID of an entity associated with a user-entered string.

Learn more validating a form.

- [Validate Form Input](https://drupalize.me/tutorial/validate-form-input)
- [Validate a Form via the Form Controller](https://drupalize.me/tutorial/validate-form-form-controller)
- [Add a Validation Callback to an Existing Form](https://drupalize.me/tutorial/add-validation-callback-existing-form)
- [Validate a Single Form Element](https://drupalize.me/tutorial/validate-single-form-element)

### Phase 3: Submit

`MyFormController::submitForm()`

- Triggered when a user submits a form, and after it has passed validation with no errors. In this phase, the form controller performs any final processing of collected data. Examples include saving it to the database, updating configuration, or posting via an API to a third party service.

Controllers are not the only code that affects the way a form works. Individual elements in the `$form` array can have callbacks associated with them that handle element specific validation and/or submission processing. In addition, [form alter hooks](https://drupalize.me/tutorial/alter-existing-form-hookformalter) can be used to add to or modify the `$form` array created by any form controller, allowing other modules to influence the behavior of a form.

Learn more about processing form data.

- [Handle Submitted Form Data](https://drupalize.me/tutorial/handle-submitted-form-data)
- [Process Submitted Form Data with a Callback](https://drupalize.me/tutorial/process-submitted-form-data-callback)
- [Process Submitted Form Data via the Form Controller](https://drupalize.me/tutorial/process-submitted-form-data-form-controller)
- [Use Ajax to Submit a Form](https://drupalize.me/tutorial/use-ajax-submit-form)

## Render an HTML form

When a user sees a form in their browser they are looking at HTML. But how does that HTML get generated?

This starts by invoking the *form builder* service, an implementation of `\Drupal\Core\Form\FormBuilderInterface`, in this case provided by `\Drupal\Core\Form\FormBuilder`. The invocation can happen in one of 2 ways:

1. The routing system allows form classes to be provided as route handlers, in which case the routing system takes care of instantiating the form builder service and invoking the proper methods on the form controller. [Learn more about routes](https://drupalize.me/topic/routes).
2. Since forms are defined as renderable arrays, any time you've got existing code that is returning a renderable array you can use the form builder service manually and request the specific form you want to use. The form builder service will handle retrieving the relevant renderable array and processing the submitted form as needed.

A form controller's `buildForm()` method defines what will be shown in the UI by creating and returning a renderable array. It's often referred to as a "Form API array", or just "`$form` array". The `$form` array is inserted into the page array and converted to HTML as part of the process of rendering a response. Read more about how Drupal converts render arrays into HTML in the [Render Pipeline](https://drupalize.me/tutorial/render-pipeline) tutorial.

During this rendering process the Form API will also generate and insert some additional information into the form definition. This includes, among other things:

- `form_id`: The unique ID of the form as defined by the form controller. It is used to identify which form is being submitted.
- `form_token` and `form_build_id`: A unique token and build ID that are specific to this rendering of this form. These values are used when the form is submitted in order to prevent against things like cross site request forgeries (CSRF) and local modification attacks.
- `op`: It is used as part of the process of figuring out which button was clicked when submitting a form.

These values are all inserted and processed automatically. In general, you won't need to do anything with them yourself.

Learn more about displaying a form.

- [Retrieve and Display Forms](https://drupalize.me/tutorial/retrieve-and-display-forms)
- [Theming Drupal Forms with Twig](https://drupalize.me/tutorial/theming-drupal-forms-twig)

## Alter a form

During the process of building and processing forms numerous hooks are invoked that allow module developers to make alterations to a form provided by another module without having to modify the code of the form controller. This is primarily accomplished by allowing hooks to alter the `$form` array before it's passed to the renderer. These hooks can add new elements to a form or make alterations to existing elements, add validation logic, and even add additional processing of submitted form data.

An example of this might be adding a terms of service text and corresponding checkbox to the user registration form. Then verifying that the user has checked the checkbox before allowing them to complete the registration process. This fundamentally alters how Drupal registers a new user but without modifying the existing code.

This is one of the most powerful aspects of the Drupal Form API and is worth taking the time to understand completely.

Learn more about altering existing forms.

- [Alter Existing Forms with hook\_form\_alter()](https://drupalize.me/tutorial/alter-existing-form-hookformalter)

## Form state

Also known as `$form_state`.

Form state refers to the object used to control the life cycle of a specific instance of a specific form. It is an implementation of `\Drupal\Core\Form\FormStateInterface` and is commonly referred to by the standard name of the variable containing this object, `$form_state`.

Form state is responsible for moving a form through the various stages in the life cycle of a form, keeping track of which stages have already been completed and which is next.

This object is passed to all form-related code and can be used to:

- Examine what in the form changed when the form submission process is complete.
- Retrieve values of form elements in the submitted form for during validation and submission handling.
- Raise or retrieve errors for specific elements or an entire form during validation.
- Get information about which element on the page triggered the submission of a form. For example, which of the buttons on a form with multiple buttons was clicked.
- Get information about the HTTP method (GET or POST) of a form.
- Store information related to the processed data in the form, which will persist across page requests when the "cache" or "rebuild" flag is set.
- Tell a form to redirect to another URL after it's completed processing submitted data.
- And many other things which we'll cover in other tutorials.

Learn more about using form state.

- [Validate User Input](https://drupalize.me/tutorial/validate-form-input)
- [Process Submitted Data](https://drupalize.me/tutorial/handle-submitted-form-data)

## Form cache

In order to allow the `$form_state` data to persist across multiple requests Drupal uses a form cache. When a user first views a page with a form on it, a copy of that form and its state are entered into the cache. Subsequent requests will retrieve the cached data as part of processing. This helps to speed up the process and also allows the use of `$form_state` to store data in scenarios like a multi-step/multi-page form.

Learn more about handling multi-step forms.

- [Handle Submitted Form Data](https://drupalize.me/tutorial/handle-submitted-form-data)
- [Use Ajax to Submit a Form](https://drupalize.me/tutorial/use-ajax-submit-form)
- Examples for Developers: [MultistepForm.php](https://git.drupalcode.org/project/examples/-/blob/d4af2e55cdbedd92cd7f6313b5e1670832e31819/modules/form_api_example/src/Form/MultistepForm.php)

The form cache also has the additional benefit of allowing Drupal to perform some extra validation. When the user's browser submits a form, Drupal compares the version sent from the browser with the version stored in the cache and ensures that they match. This prevents local modification, a potential security risk, where someone uses the web inspector in their browser to for example edit the allowed values in a `<select>` list to include one that wasn't there originally.

Because not all information in `$form_state` is persistent, form processing should not depend on whether the form is cached or not. Your form and code using `$form_state` should be written to work regardless of whether it's a fresh build of the form or one retrieved from cache. In practice, this is rarely an issue but take note.

Read the implementation in `\Drupal\Core\Form\FormCache` for more information about form caching.

## Complete life cycle of a form

For a more detailed look at how forms are processed take a look at this flow chart.

Image

![Detailed flow chart of the Drupal Form API Life Cycle](/sites/default/files/styles/max_800w/public/tutorials/images/fapi-lifecycle-drawio-diagram.png?itok=kiKE0SuR)

[View the full resolution image](https://drupalize.me/sites/default/files/styles/max_1600w/public/tutorials/images/fapi-lifecycle-drawio-diagram.png)

At DrupalCon Prague 2022 Ricardo Sanz presented the diagram below, which contains even more details than the one above. It has since been added to [the offical documentation](https://www.drupal.org/docs/drupal-apis/form-api/form-api-internal-workflow) and shared with a CC BY-SA 2.0 license. We've copied it here with no modifications for reference. And recommend [reading Ricardo's detailed explanation](https://metadrop.net/en/articles/form-api-drupalcon-prague).

Image

![Form API workflow diagram by Ricardo Sanz](/sites/default/files/styles/max_800w/public/tutorials/images/fapi_workflow_complete_v2_md.png?itok=P7y57NW8)

[View the full resolution image](https://drupalize.me/sites/default/files/styles/max_1600w/public/tutorials/images/fapi_workflow_complete_v2_md.png).

## Recap

In this tutorial, we looked at the life cycle of a form from the initial request to display the form through validation and processing of user input. Understanding this flow will help you make better-informed decisions about how to use the Form API and where you can influence the way that a form in Drupal operates.

## Further your understanding

- What are the stages of a form's life cycle that the form controller class is responsible for handling?
- What role does `$form_state` play in the life cycle of a form? How does extending `\Drupal\Core\Form\FormBase` as the starting point for your form change this?
- How does a module other than the one that initially defined a form modify an existing form?

## Additional resources

- [The form API at the DrupalCon Prague (2022)](https://metadrop.net/en/articles/form-api-drupalcon-prague) (metadrop.net)
- [DrupalCon Austin 2014: Fun with Forms in Drupal 8](https://www.youtube.com/watch?v=WRW8qNiPTHk) by Joe Shindelar (YouTube.com)

Downloads

[Life cycle of a form](/sites/default/files/sproutvideo_thumbnails/770sAqb6jTSunSnAErMXizlKxOvZjDwQL6BkAN6L9bg.jpg.jpg "770sAqb6jTSunSnAErMXizlKxOvZjDwQL6BkAN6L9bg.jpg.jpg")

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Form API Overview](/tutorial/form-api-overview?p=2734)

Next
[Define a New Form Controller and Route](/tutorial/define-new-form-controller-and-route?p=2734)

Clear History

Ask Drupalize.Me AI

close