---
title: "Create a Controller for the Weather Page"
url: "https://drupalize.me/tutorial/create-controller-weather-page?p=3236"
guide: "[[drupal-module-developer-guide]]"
---

# Create a Controller for the Weather Page

## Content

We need a place to put the custom PHP code for our */weather* page. In Drupal, *controllers* encapsulate the custom PHP logic that generates the content of a page. A basic controller might output a hard-coded response, or perform a simple calculation in PHP. Complex controllers make database requests, query third-party APIs, and format complex data using injected services and custom PHP logic.

In this tutorial, we'll:

- Create a new controller class following the PSR-4 standard.
- Define the `Drupal\anytown\Controller\WeatherPage` class with a `build()` method that returns the page's content.
- Verify that our route and controller are working.

By the end of this tutorial, you should be able to navigate to */weather* in your browser and see the output from our custom controller.

## Goal

Define a new controller that will be responsible for generating the content response for the weather page.

## Prerequisites

- [Create a Route for the Weather Page](https://drupalize.me/tutorial/create-route-weather-page)
- [Concept: Controllers](https://drupalize.me/tutorial/concept-controllers)
- [Concept: PHP Namespaces and PSR-4](https://drupalize.me/tutorial/concept-php-namespaces-and-psr-4)

## Video tutorial

Sprout Video

## Create a controller

Based on the route defined in [Create a Route for the Weather Page](https://drupalize.me/tutorial/create-route-weather-page), we know that we need to create the controller `Drupal\anytown\Controller\WeatherPage` with a `build()` method that returns the content of the weather page. Follow these steps to define the controller:

### Create a new *WeatherPage.php* file

Create the file, *src/Controller/WeatherPage.php*. This filename follows the PSR-4 standard, `Drupal\anytown\Controller\WeatherPage`, which corresponds to the value of the `_controller` key we specified in our route definition for the */weather* path.

### Define a namespace for the controller

In the *src/Controller/WeatherPage.php* we need to ensure the proper namespace. Use `Drupal\anytown\Controller` for the namespace, and `WeatherPage` for the new class name.

### Add code to the WeatherPage controller

Add the following code to *src/Controller/WeatherPage.php*:

```
<?php

declare(strict_types=1);

namespace Drupal\anytown\Controller;

use Drupal\Core\Controller\ControllerBase;

/**
 * Controller for anytown.weather_page route.
 */
class WeatherPage extends ControllerBase {

  /**
   * Builds the response.
   */
  public function build(): array {

    $build['content'] = [
      '#type' => 'markup',
      '#markup' => '<p>The weather forecast for this week is sunny with a chance of meatballs.</p>',
    ];

    return $build;
  }

}
```

This code:

- Creates the class `Drupal\anytown\Controller\WeatherPage` with a publicly-accessible `build()` method.
- The `WeatherPage` class extends the core-provided `Drupal\Core\Controller\ControllerBase` class, which contains utility methods and access to the service container. It's not required to extend this base class, but it's helpful in our case because it provides boilerplate code that we'd otherwise have to write ourselves.
- The `build()` method returns the content to display. Controllers in Drupal typically return their response as a renderable array, a Drupal-specific data structure that allows for content to be defined independent of the HTML (or other formatting) of the content. You'll learn more about renderable arrays in [Concept: Render API](https://drupalize.me/tutorial/concept-render-api), later in this guide.

### Clear the cache

Now that we've created both the route definition and controller for the *weather* page, we need to [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache).

### Verify the weather page works

With the controller above, and the route from the previous tutorial, you should now be able to load the page */weather* in your browser and see the content in the middle of the page, surrounded by the rest of the regions (and their block content) provided by the current theme.

> The weather forecast for this week is sunny with a chance of meatballs.

This initial version of the controller code only displays a hard-coded string of text. But it is enough to verify that our routes and controllers are working. And we can expand on it to include code that generates a dynamic weather forecast, which we'll do later in this guide.

## Using Drush to generate a route and controller

Now that you understand how to manually create a route and controller, you can speed up the process using [Drush](https://drupalize.me/tutorial/install-drush) to scaffold the necessary files and code. Learn how in the video below:

Sprout Video

## Recap

In this tutorial, we created and implemented a controller for our weather page route in the *anytown* module. The controller we created, `WeatherPage`, returns a simple message as a renderable array, demonstrating how controllers in Drupal can be used to generate the content of a page dynamically.

## Further your understanding

- How do you know where to put the code for the controller class within the *anytown* module?
- Why do you think a controller returns structured data instead of HTML?

## Additional resources

- [Create a Route and Controller](https://drupalize.me/tutorial/create-route-and-controller) (Drupalize.Me)
- [Introductory Drupal 8 routes and controllers example](https://www.drupal.org/docs/drupal-apis/routing-system/introductory-drupal-8-routes-and-controllers-example) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Create a Route for the Weather Page](/tutorial/create-route-weather-page?p=3236)

Next
[Add a Parameter to a Route](/tutorial/add-parameter-route?p=3236)

Clear History

Ask Drupalize.Me AI

close