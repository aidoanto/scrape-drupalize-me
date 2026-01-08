---
title: "Add a Template File"
url: "https://drupalize.me/tutorial/add-template-file?p=3239"
guide: "[[drupal-module-developer-guide]]"
---

# Add a Template File

## Content

Template files are used by modules when they need to add custom HTML to the content they output. The most common example is wrapping your output in one or more `<div>` tags to give it additional structure and context. Using custom template files in a Drupal module requires defining a new theme hook, creating the template file, an associating the appropriate data with the template file via a render array.

In this tutorial, we'll:

- Learn how to add a custom Twig template file to a module.
- Update the `WeatherPage` controller to use the new template file.

By the end of this tutorial you should be able to create and use custom template files in a module.

## Goal

Create a template file for the weather page content and update the `WeatherPage` controller to use it.

## Prerequisites

- [Concept: Template Files](https://drupalize.me/tutorial/concept-template-files)
- [Output Content Using Render API](https://drupalize.me/tutorial/output-content-using-render-api)

## Video tutorial

Sprout Video

## Add structure to output with a template

After completing the steps in [Output Content Using Render API](https://drupalize.me/tutorial/output-content-using-render-api), we're using Drupal-provided render elements inside a render array to build the content of the */weather* page.

We want to add some additional styling and structure to the page by adding HTML markup and classes that we can use to target parts of the page with CSS and JavaScript. To accomplish this, we'll create a new Twig template file which contain the markup.

Then, we'll update the render array in the `WeatherPage` controller to point to the template and pass in our dynamic weather forecast data to the template.

Here's an overview of the process we'll use:

- Define a new theme hook.
- Create a Twig template file.
- Associate the data in our render array with the new theme hook.

### Add a theme hook with `hook_theme()`

Create the file *src/Hook/AnytownTheme.php* in the root of the *anytown* module directory and add the following code:

```
<?php

declare(strict_types=1);

namespace Drupal\anytown\Hook;

use Drupal\Core\Hook\Attribute\Hook;

/**
 * Hooks related to theming and content output.
 */
class AnytownTheme {

  /**
   * Implements hook_theme().
   */
  #[Hook('theme')]
  public function theme() : array {
    return [
      'weather_page' => [
        'variables' => [
          'weather_intro' => '',
          'weather_forecast' => '',
          'short_forecast' => '',
          'weather_closures' => '',
        ],
      ],
    ];
  }

}
```

Hook implementation for Drupal 11.0.x and earlier

Prior to Drupal 11.1.x hooks were implemented as functions. If you're using an older version of Drupal, place the following code in the file *anytown.module*:

```
<?php

/**
* Implements hook_theme().
*/
function anytown_theme() {
return [
 'weather_page' => [
   'variables' => [
     'weather_intro' => '',
     'weather_forecast' => '',
     'short_forecast' => '',
     'weather_closures' => '',
   ],
 ],
];
}
```

This code:

- Implements `hook_theme()`. In this hook implementation, we define a new *theme hook* named `weather_page`. (More on hooks in [Concept: What Are Hooks?](https://drupalize.me/tutorial/concept-what-are-hooks).)
- Because there is no `'template'` key, the default behavior is to associate the theme hook with a template that uses the theme hook name, `weather_page`, with all the underscores (`_`) converted to hyphens (`-`). In this case, the resulting template file will be *templates/weather-page.html.twig*.
- Declares the 4 variables that will be passed to the template file.

With this setup, you can use this theme hook in a render array like this: `'#theme' => 'weather_page'`, and then provide values for each of the defined variables.

### Create the *weather-page.html.twig* template file

Template files in modules go in their *templates/* subdirectory. Create the file *templates/weather-page.html.twig* in the root of the *anytown* module directory with the following code:

```
{#
/**
 * @file
 * Default theme implementation for anytown weather_page.
 *
 * Available variables:
 * - weather_intro: Any messages to display.
 * - weather_forecast: Table with weekend forecast.
 * - short_forecast: A summary of the forecast.
 * - weather_closures: Any weather related closures, might be null.
 *
 * @ingroup themeable
 */
#}

<div class="weather_page">
  <div class="weather_page--messages">
    {{ weather_intro }}
  </div>
  <div class="weather_page--forecast">
    <h2>Weekend forecast</h2>
    <div class="short">
      {{ short_forecast }}
    </div>
    <div class="long">
      {{ weather_forecast }}
    </div>
  </div>
  {% if weather_closures is not null %}
    <div class="weather_page--closures">
      {{ weather_closures }}
    </div>
  {% endif %}
</div>
```

This Twig template file contains:

- Basic HTML structure for the weather page, including some CSS classes for styling specific sections of the page.
- Documentation of the variables passed into the template. Note that the variable names correspond to the names used in the implementation of `hook_theme()` in the previous step.
- Twig logic that outputs the content of the variables into the appropriate places in the template.

### Update the `WeatherPage` controller's render array

The final step is to update the render array returned from the `WeatherPage` controller to use the new theme hook.

Modify the *src/Controller/WeatherPage.php* file to match the following:

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

    $table_rows = [];
    $highest = 0;
    $lowest = 0;
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

        // Create one table row for each day in the forecast.
        $table_rows[] = [
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

        $highest = max($highest, $high);
        $lowest = min($lowest, $low);
      }

      // Extended forecast as a table.
      $weather_forecast = [
        '#type' => 'table',
        '#header' => [
          'Day',
          '',
          'Forecast',
        ],
        '#rows' => $table_rows,
        '#attributes' => [
          'class' => ['weather_page--forecast-table'],
        ],
      ];

      // Summary forecast.
      $short_forecast = [
        '#type' => 'markup',
        '#markup' => "The high for the weekend is {$highest} and the low is {$lowest}.",
      ];

    }
    else {
      // Or, display a message if we can't get the current forecast.
      $weather_forecast = ['#markup' => '<p>Could not get the weather forecast. Dress for anything.</p>'];
      $short_forecast = NULL;
    }

    $build = [
      // Which theme hook to use for this content. See anytown_theme().
      '#theme' => 'weather_page',
      // When passing a render array to Twig template file any top level array
      // element that starts with a '#' will be a variable in the template file.
      // Example: {{ weather_intro }}.
      '#weather_intro' => [
        '#markup' => "<p>Check out this weekend's weather forecast and come prepared. The market is mostly outside, and takes place rain or shine.</p>",
      ],
      '#weather_forecast' => $weather_forecast,
      '#short_forecast' => $short_forecast,
      '#weather_closures' => [
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

This code update:

- Refactors the weather page content into 4 distinct elements: page intro text, a short weather forecast, an extended weather forecast, and a list of weather related closures. Each element is represented by its own renderable array.
- Creates a new top-level renderable array associated with the new `weather_page` theme hook via the `#theme` property.
- Populates each of the 4 variables for the template file using the new content elements.

Some things to note:

- The variable names in the render array such as `#weather_intro` and `#short_forecast` correspond with the variable names defined in the `hook_theme()` implementation. And, also with those being output in the *weather-page.html.twig* template file.
- The variables passed to Twig can be renderable arrays. This works because Drupal adds some additional logic to Twig that will recognize that `{{ short_forecast }}` contains a renderable array instead of a string. It will convert the array to HTML before inserting it into the template.

Now, when the content for the */weather* page is rendered, it'll use the *weather-page.html.twig* template file.

### Verify it works

[Clear the cache](https://drupalize.me/tutorial/clear-drupals-cache), so that changes you made are found by Drupal.

Open */weather* in your browser. View the source for the page. Notice that it's using the HTML defined in your Twig template file. Optionally, [enable theme debugging mode](https://drupalize.me/tutorial/configure-your-environment-theme-development), clear the cache again, and Drupal will show you which template file it's currently using for each part of the page.

## Recap

In this tutorial, we updated our module to use a Twig template file to wrap the page's content with some additional structural HTML. To do this, we defined a new theme hook via `hook_theme()`, created a new Twig template file for the theme hook, and updated the render array output in the `WeatherPage` controller to use our new theme hook.

## Further your understanding

- Why create a custom template file instead of adding the HTML we need as `#markup` elements in the render array?
- What would you need to do if you wanted the template file name to be different from the theme hook?
- Learn how to [Add New Theme Hook Suggestions](https://drupalize.me/tutorial/add-new-theme-hook-suggestions) to further enhance the ways a theme can customize the template file.

## Additional resources

- [Output Content with a Template File](https://drupalize.me/tutorial/output-content-template-file) (Drupalize.Me)
- [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Template Files](/tutorial/concept-template-files?p=3239)

Next
[Concept: Asset Libraries](/tutorial/concept-asset-libraries?p=3239)

Clear History

Ask Drupalize.Me AI

close