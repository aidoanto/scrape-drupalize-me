---
title: "Concept: Routesfree"
url: "https://drupalize.me/tutorial/concept-routes?p=3236"
guide: "[[drupal-module-developer-guide]]"
order: 13
---

# Concept: Routesfree

## Content

As a module developer, you use routes defined in a module to add new URLs and tell Drupal which code to execute to build content for the page at those URLs. Central to this process is Drupal's routing system, built upon Symfony's Routing component.

In this tutorial, we'll:

- Introduce Drupal's routing system.
- Learn how modules can define new routes.
- Describe the roles that routes serve in a module.

By the end of this tutorial, you should understand each parameter of a route definition in a module's *MODULE\_NAME.routing.yml* file.

## Goal

Understand the role of Drupal's routing system plays in enabling developers to create custom pages within a module.

## Prerequisites

- [Guiding Scenario](https://drupalize.me/tutorial/guiding-scenario)

## Adding a custom URL with a module

In your work on the Anytown Farmer's Market site, you have been tasked with creating a new page at the path, */weather*. Visitors will use this page to view the weather forecast for the upcoming weekend, helping them decide whether to attend the market.

One option is to add a new *Basic page* node and set the URL alias to */weather*, allowing an editor to update the page. However, this approach requires frequent data updates. A more efficient solution is to use a third-party weather API to provide an up-to-date forecast.

To implement this, you need to inform Drupal that your module will handle the */weather* page and instruct it to call your custom code, which will retrieve and display the weather forecast.

## Understanding Drupal's routing system

Defining new URLs (or paths) with a module involves creating a route. Drupal uses a routing system based on Symfony's Routing component to match URLs with corresponding response-generating code. Drupal's routing system includes specific features that enhance Symfony's component. (You don't need experience with routing in Symfony to set up a route in Drupal.)

Routes define a *path*. A *path* is the portion of the URL after the TLD (Top-Level Domain). For example, in the URL, `https://drupal.org/weather`, the `/weather` portion is the path. A route's definition includes handling route parameters, access control, and specifying which code (known as a *controller*) to execute. We'll discuss controllers, responsible for returning page content, in [Concept: Controllers](https://drupalize.me/tutorial/concept-controllers).

## Anatomy of a route

Routes are typically defined using YAML in a module’s *MODULE\_NAME.routing.yml* file. It's also possible to define dynamic routes with PHP classes. In this guide, we'll use a routing file to define a route.

A route definition includes:

- **Path**: The URL the route responds to, possibly containing placeholders or wildcards passed as arguments to the controller.
- **Defaults**: Default values for the route, such as a `_controller` or `_form` for the response, a `_title` for the page, and optional arguments for the called code.
- **Requirements**: Conditions for route accessibility, often including permission checks.

A single routing YAML file can contain multiple route definitions.

In [Create a Route for the Weather Page](https://drupalize.me/tutorial/create-route-weather-page), we'll add a route for the */weather* URL to the *anytown* module. And we'll get hands-on practice defining a route in [Create a Route and Controller](https://drupalize.me/tutorial/create-route-and-controller).

## Recap

This tutorial introduced the basics of Drupal's routing system. We learned about route components and how Drupal uses Symfony's routing component to manage HTTP requests and create dynamic content.

## Further your understanding

- What role do routes play in custom modules?
- How do [permissions](https://drupalize.me/tutorial/user-guide/user-concept?p=2441) affect route access?

## Additional resources

- [Overview: Routes, Controllers, and Responses](https://drupalize.me/tutorial/overview-routes-controllers-and-responses) (Drupalize.Me)
- [Routing System Overview](https://www.drupal.org/docs/drupal-apis/routing-system/routing-system-overview) (Drupal.org)
- [Routing API](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Routing%21routing.api.php/group/routing/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Concept: PHP Namespaces and PSR-4](/tutorial/concept-php-namespaces-and-psr-4?p=3236)

Clear History

Ask Drupalize.Me AI

close