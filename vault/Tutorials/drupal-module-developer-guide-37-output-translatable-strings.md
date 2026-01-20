---
title: "Output Translatable Strings"
url: "https://drupalize.me/tutorial/output-translatable-strings?p=3239"
guide: "[[drupal-module-developer-guide]]"
order: 37
---

# Output Translatable Strings

## Content

It's a Drupal best practice to always use Drupal's internationalization utilities for any user interface strings in your code. This includes the PHP `t()` function and `StringTranslationTrait` trait, the Twig `t` filter, and the JavaScript `Drupal.t()` function. This makes it possible for our module's interface to be localized.

In this tutorial, we'll:

- Edit the `WeatherPage` controller and use the `t()` method from the `StringTranslationTrait` trait for all UI strings.
- Update the *weather-page.html.twig* template file to use the Twig `t` filter.
- Modify the JavaScript in our *forecast.js* code to use the `Drupal.t()` function for UI strings.

By the end of this tutorial you should be able to update the PHP, Twig, and JavaScript code in your module to ensure that any user interface strings they output are translatable.

## Goal

Update all the user interface strings in the *anytown* module, so they can be localized.

## Prerequisites

- [Concept: Internationalization (i18n)](https://drupalize.me/tutorial/concept-internationalization-i18n)

## Video tutorial

Sprout Video

### Update the `WeatherPage` controller

The `WeatherPage` controller has a couple of user interface strings in the renderable array that it outputs. We can update those to use the `$this->t()` method, so these strings can be localized. Since we wrapped the `$description` variable in `<em></em>` HTML tags, we can use the `%`-prefix for that placeholder, which wraps the placeholder text in `<em></em>` tags. For the other variables, we'll use the `@`-prefix for the placeholder.

The `t` method is already available in the `WeatherPage` class because we extended `ControllerBase`. In other scenarios we could access it including the `StringTranslationTrait` trait in our class, or by injecting the translation service.

Edit *src/Controller/WeatherPage.php* so that it contains the following code:

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
              '#markup' => $this->t('%description with a high of @high and a low of @low',
                [
                  '%description' => $description,
                  '@high' => $high,
                  '@low' => $low,
                ]
              ),
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
        '#markup' => '<p>' . $this->t('The high for the weekend is @highest and the low is @lowest.',
          [
            '@highest' => $highest,
            '@lowest' => $lowest,
          ]
        ) . '</p>',
      ];

    }
    else {
      // Or, display a message if we can't get the current forecast.
      $weather_forecast = ['#markup' => '<p>' . $this->t('Could not get the weather forecast. Dress for anything.') . '</p>'];
      $short_forecast = NULL;
    }

    $build = [
      // Which theme hook to use for this content. See anytown_theme().
      '#theme' => 'weather_page',
      // Attach the CSS and JavaScript for the page.
      '#attached' => [
        'library' => ['anytown/forecast'],
      ],
      // When passing a render array to Twig template file any top level array
      // element that starts with a '#' will be a variable in the template file.
      // Example: {{ weather_intro }}.
      '#weather_intro' => [
        '#markup' => "<p>" . $this->t("Check out this weekend's weather forecast and come prepared. The market is mostly outside, and takes place rain or shine") . "</p>",
      ],
      '#weather_forecast' => $weather_forecast,
      '#short_forecast' => $short_forecast,
      '#weather_closures' => [
        '#theme' => 'item_list',
        '#title' => $this->t('Weather related closures'),
        '#items' => [
          $this->t('Ice rink closed until winter - please stay off while we prepare it.'),
          $this->t('Parking behind Apple Lane is still closed from all the rain last weekend.'),
        ],
      ],
    ];

    return $build;
  }

}
```

### Update the *weather-page.html.twig* template file

Edit the file, *templates/weather-page.html.twig*, and use the Twig `t` filter for hard-coded strings.

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
    <h2>{{ "Weekend forecast"|t }}</h2>
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

### Update the *js/forecast.js* code

We can also update the user interface strings in our JavaScript code and use the `Drupal.t()` function to make them translatable.

Edit *js/forecast.js* so that it contains the following code:

```
(function (Drupal, once) {
  Drupal.behaviors.forecastToggle = {
    attach: function (context, settings) {
      // Use 'once' to ensure this runs only once per context
      once('forecast-toggle', 'div.weather_page--forecast', context).forEach(function (el) {
        // Initialize: hide 'div.long' and show 'div.short'.
        const long = el.querySelector('.long');
        const short = el.querySelector('.short');
        long.classList.add('visually-hidden');

        // Create and configure a button to toggle between thet wo.
        const toggleButton = document.createElement('button');
        toggleButton.textContent = Drupal.t('Toggle extended forecast');
        toggleButton.addEventListener('click', function () {
          long.classList.toggle('visually-hidden');
          short.classList.toggle('visually-hidden');
        });

        // Append the button to the page.
        document.querySelector('.weather_page--forecast').appendChild(toggleButton);
      });
    }
  };
})(Drupal, once);
```

## Recap

In this tutorial, we updated all the user interface strings hard-coded into our module to use Drupal's internationalization utilities. While this doesn't have any immediate impact on how things look on our site, it does ensure that if someone wanted to translate the user interface to another language that they could do so without having to modify our code at all.

## Further your understanding

- Why use the internationalization features of Drupal's API if your site is only in English?
- Why are some strings wrapped with `t()` and other utilities but not all?

## Additional resources

- [Translation API overview](https://www.drupal.org/docs/8/api/translation-api/overview) (Drupal.org)
- [Internationalization](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Language%21language.api.php/group/i18n) (api.drupal.org)
- [Make Strings Translatable](https://drupalize.me/tutorial/make-strings-translatable) (Drupalize.Me)
- [Use Drupal.t() for Translatable Strings in JavaScript](https://drupalize.me/tutorial/use-drupalt-translatable-strings-javascript) (Drupalize.Me)
- [Make Your Theme Translatable](https://drupalize.me/tutorial/make-your-theme-translatable) (Drupalize.Me)
- [function FormattableMarkup::placeholderFormat - See this page for descriptions of types of placeholders](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Component%21Render%21FormattableMarkup.php/function/FormattableMarkup%3A%3AplaceholderFormat/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Internationalization (i18n)](/tutorial/concept-internationalization-i18n?p=3239)

Clear History

Ask Drupalize.Me AI

close