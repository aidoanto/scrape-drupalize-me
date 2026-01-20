---
title: "Add a Parameter to a Route"
url: "https://drupalize.me/tutorial/add-parameter-route?p=3236"
guide: "[[drupal-module-developer-guide]]"
order: 18
---

# Add a Parameter to a Route

## Content

Route parameters enable a single route and controller to handle multiple URLs by passing dynamic values from the URL to the controller. This allows for more versatile and responsive page content generation.

In this tutorial, we'll:

- Understand the function of route parameters.
- Update the `anytown.weather_page` route to include parameters.
- Modify the `WeatherPage` controller to use these parameters.

By the end of this tutorial, you'll know how to use route parameters to pass dynamic values to controllers.

## Goal

Enhance the `anytown.weather_page` route to accept parameters, allowing the controller to display different types of weather forecasts based on these parameters.

## Prerequisites

- [Create a Route for the Weather Page](https://drupalize.me/tutorial/create-route-weather-page)
- [Create a Controller for the Weather Page](https://drupalize.me/tutorial/create-controller-weather-page)

## Video tutorial

Sprout Video

Using parameters allows a single controller to serve multiple different pages. In our case we want to have pages at both `/weather/extended` and `/weather/short`. We could create 2 routes, and 2 controllers. But that would result in duplicate code. Instead, we'll use parameters to pass a value of `extended` or `short` to the controller as arguments. In the controller, we can implement custom PHP logic to vary the output based on the argument's value.

### Update the route with a parameter

Modify the `anytown.weather_page` route in *anytown.routing.yml* as follows:

```
# Route definitions for the anytown module.

# Each route needs a unique identifier. We recommend prefixing the route name
# with the name of your module. Indented under the route name is the definition
# of the route. A routing.yml file can contain any number of routes.
anytown.weather_page:
  # The URL path where this page will be displayed. {style} represents a
  # placeholder and will be populated by whatever is entered into that position
  # of the URL. Its value is passed the controller's build method.
  path: '/weather/{style}'
  defaults:
    # Title of the page used for things like <title> tag.
    _title: 'Weather at the market'
    # Defines which method, on which class, should be called to retrieve the
    # content of the page.
    _controller: '\Drupal\anytown\Controller\WeatherPage::build'
    # Default value for {style} if it's not present.
    style: 'short'
  requirements:
    # What permissions a user needs to have in order to view this page.
    _permission: 'access content'
```

This updated route:

- Adds a `{style}` placeholder in the `path`, allowing for URLs like `/weather/extended` or `/weather/short`. Values from the placeholder get passed to the controller as arguments.
- Uses `defaults.style` to provide a fallback when no specific style is mentioned in the URL.

### Modify the controller to accept the parameter

In *src/Controller/WeatherPage.php*, revise the `build()` method to use the `$style` parameter:

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
  public function build(string $style): array {
    // Style should be one of 'short', or 'extended'. And default to 'short'.
    $style = (in_array($style, ['short', 'extended'])) ? $style : 'short';

    $build['content'] = [
      '#type' => 'markup',
      '#markup' => '<p>The weather forecast for this week is sunny with a chance of meatballs.</p>',
    ];

    if ($style === 'extended') {
      $build['content_extended'] = [
        '#type' => 'markup',
        '#markup' => '<p><strong>Extended forecast:</strong> Looking ahead to next week we expect some snow.</p>',
      ];
    }

    return $build;
  }

}
```

This updated `WeatherPage` controller now takes a `$style` argument as input to the `build()` method and changes the output depending on the passed in value. The `$style` variable is populated with the value extracted from the URL in the place of the `{style}` placeholder. The argument name is important, and must match the slug name from the route's path.

### Clear the cache

Route definitions are cached, so we need to [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) since we've edited the `anytown.weather_page` route.

### Test the updated route and controller

Visit both */weather/extended* and */weather/short* in your browser. You should see different content at each path.

## Recap

In this tutorial, we added a parameter to the `anytown.weather_page` route that allows the same route and controller to generate content at multiple paths. We learned that parameters are created by adding a slug to the route's path, and a corresponding argument to the controller. The parameters value is populated with content extracted from the URL.

## Further your understanding

- Imagine a route for displaying specific content items, like `/content/{id}`. How would parameters be used in this scenario?
- Explore what happens with different URL inputs, such as `/weather/random-text`, and understand how the controller handles them.

## Additional resources

- [Detailed guide on route parameters](https://drupalize.me/tutorial/overview-parameters-and-value-upcasting-routes) (Drupalize.Me)
- [Practical examples of route parameters](https://drupalize.me/tutorial/use-parameters-route) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Create a Controller for the Weather Page](/tutorial/create-controller-weather-page?p=3236)

Next
[Concept: Menu Items and Links](/tutorial/concept-menu-items-and-links?p=3236)

Clear History

Ask Drupalize.Me AI

close