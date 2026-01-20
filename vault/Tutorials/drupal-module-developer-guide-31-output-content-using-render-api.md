---
title: "Output Content Using Render API"
url: "https://drupalize.me/tutorial/output-content-using-render-api?p=3239"
guide: "[[drupal-module-developer-guide]]"
order: 31
---

# Output Content Using Render API

## Content

Controllers in Drupal should return renderable arrays that contain the content to display for the page. Doing so makes it easier for the theme layer to override the output and customize it for a specific site.

In this tutorial, we'll:

- Convert the `WeatherPage` controller to use a renderable array instead of hard-coded HTML for displaying the weather forecast.
- Verify our updates.

By the end of this tutorial, you should understand how to structure content as a render array within a controller.

## Goal

Update the `WeatherPage` controller to use a renderable array instead of hard-coded HTML.

## Prerequisites

- [Concept: Themeable Output](https://drupalize.me/tutorial/concept-themeable-output)
- [Concept: Render API](https://drupalize.me/tutorial/concept-render-api)

## Video tutorial

Sprout Video

## Modules should output content using Render API

A controller returning page content should use a renderable array. Our current `WeatherPage` controller returns a simple renderable array that embeds HTML inside a generic `'#type' => 'markdown'` render element. Although functional, we can improve this by adding more structure to the array.

This adjustment will allow for easier theme layer customizations. For bespoke code, you'll need to figure out the right balance between adherence to Drupal standards and the recognition that the code may only be used on a single site, and thus not require theme overrides.

### Update the `WeatherPage` controller

Modify the `WeatherPage` controller in *src/Controller/WeatherPage.php* as follows:

```
<?php

declare(strict_types=1);

namespace Drupal\anytown\Controller;

use Drupal\anytown\ForecastClientInterface;
use Drupal\Core\Controller\ControllerBase;
use Symfony\Component\DependencyInjection\ContainerInterface;

/**
 * Controller for anytown.weather_page route.
 */
class WeatherPage extends ControllerBase {

  /**
   * Forecast API client.
   *
   * @var \Drupal\anytown\ForecastClientInterface
   */
  private $forecastClient;

  /**
   * WeatherPage controller constructor.
   *
   * @param \Drupal\anytown\ForecastClientInterface $forecast_client
   *   Forecast API client service.
   */
  public function __construct(ForecastClientInterface $forecast_client) {
    $this->forecastClient = $forecast_client;
  }

  /**
   * {@inheritDoc}
   */
  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('anytown.forecast_client')
    );
  }

  /**
   * Builds the response.
   */
  public function build(string $style): array {
    // Style should be one of 'short', or 'extended'. And default to 'short'.
    $style = (in_array($style, ['short', 'extended'])) ? $style : 'short';

    $url = 'https://module-developer-guide-demo-site.ddev.site/modules/custom/anytown/data/weather_forecast.json';
    $forecast_data = $this->forecastClient->getForecastData($url);

    $rows = [];
    if ($forecast_data) {
      // Create a table of the weather forecast as a render array. First loop
      // over the forecast data and create rows for the table.
      foreach ($forecast_data as $item) {
        [
          'weekday' => $weekday,
          'description' => $description,
          'high' => $high,
          'low' => $low,
          'icon' => $icon,
        ] = $item;

        $rows[] = [
          // Simple text for a cell can be added directly to the array.
          $weekday,
          // Complex data for a cell, like HTML, can be represented as a nested
          // render array.
          [
            'data' => [
              '#markup' => '<img alt="' . $description . '" src="' . $icon . '" width="200" height="200" />',
            ],
          ],
          [
            'data' => [
              '#markup' => "<em>{$description}</em> with a high of {$high} and a low of {$low}",
            ],
          ],
        ];
      }

      $weather_forecast = [
        '#type' => 'table',
        '#header' => [
          'Day',
          '',
          'Forecast',
        ],
        '#rows' => $rows,
        '#attributes' => [
          'class' => ['weather_page--forecast-table'],
        ],
      ];

    }
    else {
      // Or, display a message if we can't get the current forecast.
      $weather_forecast = ['#markup' => '<p>Could not get the weather forecast. Dress for anything.</p>'];
    }

    $build = [
      'weather_intro' => [
        '#markup' => "<p>Check out this weekend's weather forecast and come prepared. The market is mostly outside, and takes place rain or shine.</p>",
      ],
      'weather_forecast' => $weather_forecast,
      'weather_closures' => [
        '#theme' => 'item_list',
        '#title' => 'Weather related closures',
        '#items' => [
          'Ice rink closed until winter - please stay off while we prepare it.',
          'Parking behind Apple Lane is still closed from all the rain last weekend.',
        ],
      ],
    ];

    return $build;
  }

}
```

This refactoring transforms the `build()` method to use a structured render array, including:

- A table for the weather forecast (`'#type' => 'table'`).
- A list of weather-related closures (`'#theme' => 'item_list'`).
- Text paragraphs (`'#markup'`).

### Verify it works

[Clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) to ensure you're getting a fresh version of the page.

Open */weather* in your browser to see the forecast displayed as an HTML table.

## Recap

In this tutorial, we converted the `WeatherPage` controller output to a render array instead of using hard-coded HTML.

## Further your understanding

- How might you update the render array to define weather icon images as a render element instead of using hard-coded `<img>` tags?
- What approach could dynamically populate the "Weather related closures" list?

## Additional resources

- [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays) (Drupalize.Me)
- [Output a Table](https://drupalize.me/tutorial/output-table) (Drupalize.Me)
- [Output a List of Items](https://drupalize.me/tutorial/output-list-items) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Render API](/tutorial/concept-render-api?p=3239)

Next
[Concept: Template Files](/tutorial/concept-template-files?p=3239)

Clear History

Ask Drupalize.Me AI

close