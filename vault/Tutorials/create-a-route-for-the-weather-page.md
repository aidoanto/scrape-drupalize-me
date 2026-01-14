---
title: "Create a Route for the Weather Page"
url: "https://drupalize.me/tutorial/create-route-weather-page?p=3236"
guide: "[[drupal-module-developer-guide]]"
order: 16
---

# Create a Route for the Weather Page

## Content

Routes map URLs to the code that generates the content for display. As module developers, we create routes whenever we want to add a new URL with code. Our task is to create a route for a page displaying the weekend weather forecast. We start by defining the route, then add the corresponding controller.

In this tutorial, we'll:

- Create a routing YAML file for a custom weather page.
- Define a route instructing Drupal to point the path */weather* to our custom code.

By the end of this tutorial, you will have defined a route for your weather page, including the path and a reference to the controller managing the content.

## Goal

Define a route for a new page at the URL */weather* in the *anytown* module.

## Prerequisites

- [Concept: Routes](https://drupalize.me/tutorial/concept-routes)
- A custom module named *anytown*, which we started in [Create an Info File for a Module](https://drupalize.me/tutorial/create-info-file-module-mdg).

## Video tutorial

Sprout Video

## Create a route

Our task is to add a new page to the Anytown Farmer's Market site that displays the weather forecast for the upcoming weekend. To add a new page at the URL */weather* in a custom module, we first need to define a [route](https://drupalize.me/tutorial/concept-routes).

### Create a routing YAML file

Inside the *anytown* module directory, create a file (if it doesn't already exist) named *anytown.routing.yml*. Place this file in the same directory as the *anytown.info.yml* file.

### Define the route

Open the *anytown.routing.yml* file in a text editor and add the following YAML code which defines the route for our weather page:

```
# Route definitions for the anytown module.

# Each route needs a unique identifier. We recommend prefixing the route name
# with the name of your module. Indented under the route name is the definition
# of the route. A routing.yml file can contain any number of routes.
anytown.weather_page:
  # The URL path where this page will be displayed.
  path: '/weather'
  defaults:
    # Title of the page used for things like <title> tag.
    _title: 'Weather at the market'
    # Defines which method, on which class, should be called to retrieve the
    # content of the page.
    _controller: '\Drupal\anytown\Controller\WeatherPage::build'
  requirements:
    # What permissions a user needs to have in order to view this page.
    _permission: 'access content'
```

This code defines a route with the following elements:

- **Path**: The URL path for the page (`/weather`).
- **Defaults**: Specifies the page title and the controller class method (`WeatherPage::build`) that will return the content.
- **Requirements**: Sets the permission needed to access this route (`access content`).

Route definitions are cached, so you'll need to clear the cache before Drupal will find your new route or any changes to existing routes. But, if you do so before creating the controller referenced in the route, you'll get an error. We'll hold off clearing the cache until we [create our controller](https://drupalize.me/tutorial/create-controller-weather-page).

A route definition won't do much by itself. Next, in [Create a Controller for the Weather Page](https://drupalize.me/tutorial/create-controller-weather-page), we'll create the controller associated with our new route.

## Recap

In this tutorial, we created a route for a weather page in our custom Drupal module. We specified the URL path and mapped it to not-yet-created controller method responsible for generating the page content.

## Further your understanding

- Why define a new page via a route instead of creating a page node with the URL alias, */weather*?
- How do you know where the custom code generating a response for this route should be located?
- We will explore more complex route definitions in later tutorials in this guide. For a full reference, see [Overview: Routes, Controllers, and Responses](https://drupalize.me/tutorial/overview-routes-controllers-and-responses).

## Additional resources

- [Structure of Routes](https://www.drupal.org/docs/drupal-apis/routing-system/structure-of-routes) (Drupal.org)
- [Routes](https://drupalize.me/topic/routes) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Controllers](/tutorial/concept-controllers?p=3236)

Next
[Create a Controller for the Weather Page](/tutorial/create-controller-weather-page?p=3236)

Clear History

Ask Drupalize.Me AI

close