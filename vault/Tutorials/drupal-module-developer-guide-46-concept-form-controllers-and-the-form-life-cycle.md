---
title: "Concept: Form Controllers and the Form Life Cycle"
url: "https://drupalize.me/tutorial/concept-form-controllers-and-form-life-cycle?p=3242"
guide: "[[drupal-module-developer-guide]]"
order: 46
---

# Concept: Form Controllers and the Form Life Cycle

## Content

The life cycle of a Drupal form, from initial request to final processing, involves multiple stages. This tutorial outlines these stages and the role of form controllers, which contain custom form handling logic.

In this tutorial, we'll:

- Define the role of a form controller.
- List the phases of form processing in Drupal and how to add custom logic to each.
- See how form controllers relate to routes for displaying full-page forms.

By the end of this tutorial, you should be able to explain the role of a form controller and how to get started creating a new one.

## Goal

Learn how form controllers manage each stage of the life cycle of a form.

## Prerequisites

- [Overview: Drupal's Form API](https://drupalize.me/tutorial/overview-drupals-form-api)
- [Concept: Routes](https://drupalize.me/tutorial/concept-routes)
- [Concept: Controllers](https://drupalize.me/tutorial/concept-controllers)

## Introduction to form controllers

Form controllers in Drupal manage the life cycle of forms, from creation and display to validation and submission. These controllers are PHP classes that implement `\Drupal\Core\Form\FormInterface`, and orchestrate the form's behavior at each stage of its life cycle. A form controller *can* act as the callback for a route. It can also be used independently of the route in conjunction with the `form_builder` [service](https://drupalize.me/tutorial/concept-services-and-container). Which allows forms to be placed into blocks or anywhere else that render arrays can be used.

## The form life cycle

The life cycle of a Drupal form consists of the following phases:

1. **Routing** (optional): Drupal's routing system identifies the appropriate form controller based on the URL.
2. **Display**: The form controller builds a `$form` array that represents the form's HTML, which is rendered and displayed to the user.
3. **Submit**: Upon form submission, the form controller processes the HTTP POST request, invoking validation and submission handlers as necessary.
4. **Validation**: The form controller validates user input. If validation fails, the form is redisplayed with error messages.
5. **Processing**: After successful validation, the form controller processes the submission, performing actions such as saving data or redirecting the user.

The `FormBuilder` service handles the low-level processing of forms, such as rendering the necessary HTML and initial processing of incoming `$_POST` data. It delegates to your implementation of `FormInterface` as necessary.

## Implementing form controllers

To define a form in Drupal, create a class that implements `\Drupal\Core\Form\FormInterface`. The class must define methods for building, validating, and submitting the form. Drupal provides a couple of utility classes that can be extended for most forms. The most used is `\Drupal\Core\Form\FormBase`.

Just like regular controllers, form controllers can implement `Drupal\Core\DependencyInjection\ContainerInjectionInterface` and use the `create()` factory method pattern defined in [Concept: Dependency Injection](https://drupalize.me/tutorial/concept-dependency-injection) to access services that are not included in `FormBase`.

## Form controllers in routes

In Drupal's routing system, form controllers can be specified directly in route definitions using the `_form` key. This approach simplifies the linkage between routes and form controllers, allowing Drupal to directly render the form without specifying a separate controller method.

Example route definition using the `_form` key:

```
example.form:
   path: '/example/form'
   defaults:
      _form: '\Drupal\example\Form\ExampleForm'
   requirements:
   _permission: 'access content'
```

For more about how routes map to controllers, review [Concept: Routes](https://drupalize.me/tutorial/concept-routes).

## The form life cycle

The parts of the form life cycle that the form controller is responsible for include:

- **Phase 1: Build**: The `buildForm()` method is responsible for defining the form's structure using the Form API.
- **Phase 2: Validate**: The `validateForm()` method is called upon form submission to ensure the user's input meets specified criteria.
- **Phase 3: Submit**: The `submitForm()` method handles the form's submission logic, such as saving data or performing other actions based on the user's input.

## Understanding the `$form_state`

The `\Drupal\Core\Form\FormStateInterface` object, typically referred to as `$form_state`, tracks the form's state throughout its life cycle. It contains user input, validation errors, and other metadata, facilitating communication between the stages of the form.

## Recap

Understanding the form life cycle and the role of form controllers is fundamental for Drupal developers looking to use the Form API for custom module development. In this tutorial, we learned about the role form controllers play, how they are defined, and how they can be used as the callback for a route.

## Further your understanding

- How do form controllers differ from standard page controllers?
- Explore the `FormStateInterface` and its methods to better understand its use case.

## Additional resources

- [Form API Life Cycle](https://drupalize.me/tutorial/form-api-life-cycle) (Drupalize.Me)
- [Define a New Form Controller and Route](https://drupalize.me/tutorial/define-new-form-controller-and-route) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview: Drupal's Form API](/tutorial/overview-drupals-form-api?p=3242)

Next
[Create a Settings Form for the Anytown Module](/tutorial/create-settings-form-anytown-module?p=3242)

Clear History

Ask Drupalize.Me AI

close