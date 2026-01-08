---
title: "Concept: Controllers"
url: "https://drupalize.me/tutorial/concept-controllers?p=3236"
guide: "[[drupal-module-developer-guide]]"
---

# Concept: Controllers

## Content

Controllers are where you place the custom logic to dynamically generate the content of a page that a visitor sees when they visit a URL. When Drupal receives an incoming request, the HttpKernel identifies the appropriate route for the requested path, and the routing system matches this route with a controller. Controllers generate responses to these requests.

In this tutorial, we'll:

- Understand what a controller is in PHP and in the context of a Drupal module.
- Learn how to identify and interpret the role of a controller class.

By the end of this tutorial, you should be able to identify a controller class in a Drupal module and understand its role in generating responses.

## Goal

Understand the purpose and function of controller classes in Drupal modules and their relationship to routes.

## Prerequisites

- [Concept: Routes](https://drupalize.me/tutorial/concept-routes)
- [Concept: PHP Namespaces and PSR-4](https://drupalize.me/tutorial/concept-php-namespaces-and-psr-4)

## What is a controller?

After defining a route for the */weather* page in [Concept: Routes](https://drupalize.me/tutorial/concept-routes), we need a place to put our custom code that will call the third-party weather API and generate the weather forecast to display on the page. This is the job of a *controller*.

Controllers are PHP classes that serve as the callback for a route. When a route matches a request, the corresponding controller executes and generates the content for the page. This involves querying a database, processing data, performing calculations, and preparing the information for display.

In Drupal, controllers collect and process data but stop short of determining how to display it. Instead, controllers in Drupal return a response. The returned response might be HTML content in the form of a renderable array, JSON data, error codes, or an HTTP redirect.

## Identifying controller classes

Controllers in a Drupal module are located in the *src/Controller* or *src/Form* subdirectory, [adhering to PSR-4 standards for namespacing and autoloading](https://drupalize.me/tutorial/concept-php-namespaces-and-psr-4). For instance, a controller class for the */weather* route might be located in *src/Controller/WeatherPageController.php*.

The class maps to a route in the module's *MODULE\_NAME.routing.yml* file, specified under the `defaults` key with a `_controller` attribute.

Forms in Drupal are also defined using controllers, with slight variations. Form controllers handle the HTML form submission workflow (including validation), displaying errors, and handling submitted data. This guide will cover form controllers in more depth starting in [Concept: Form Controllers and the Form Life Cycle](https://drupalize.me/tutorial/concept-form-controllers-and-form-life-cycle).

## Controller arguments

Routes can pass arguments, known as route parameters or slugs, from the URL to the controller. This allows a single route and controller to handle responses dynamically, such as retrieving a node from the database based on an ID in the URL. In this guide, we'll demonstrate this concept in [Add a Parameter to a Route](https://drupalize.me/tutorial/add-parameter-route).

## Thin controllers

Your controller's code should focus on retrieving and assembling content for the page, like pulling information from the database or formatting a response from a third-party API call. Business logic, such as making requests to third-party APIs or performing complex calculations, should be written as *services*. This keeps your controllers *thin* and easier to test. This guide will cover creating services to encapsulate business logic in [Concept: Custom Services](https://drupalize.me/tutorial/concept-creating-custom-services).

## Recap

In this tutorial, we explored the role of controllers in Drupal. Controllers are where modules put custom code to generate the content of a page. We learned that routes map URLs to controllers, which then generate the content. Controllers can also return other types of responses, like redirects and errors.

## Further your understanding

- Can you find an example of a controller in a Drupal module and explain what it does?

## Additional resources

- [Overview: Routes, Controllers, and Responses](https://drupalize.me/tutorial/overview-routes-controllers-and-responses) (Drupalize.Me)
- [Routing System Overview](https://www.drupal.org/docs/drupal-apis/routing-system/routing-system-overview) (Drupal.org)
- [Routing API](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Routing%21routing.api.php/group/routing/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: PHP Namespaces and PSR-4](/tutorial/concept-php-namespaces-and-psr-4?p=3236)

Next
[Create a Route for the Weather Page](/tutorial/create-route-weather-page?p=3236)

Clear History

Ask Drupalize.Me AI

close