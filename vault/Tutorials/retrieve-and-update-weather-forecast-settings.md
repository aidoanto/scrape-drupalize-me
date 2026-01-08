---
title: "Retrieve and Update Weather Forecast Settings"
url: "https://drupalize.me/tutorial/retrieve-and-update-weather-forecast-settings?p=3243"
guide: "[[drupal-module-developer-guide]]"
---

# Retrieve and Update Weather Forecast Settings

## Content

Modules in Drupal often rely on the Configuration API to adapt their behavior based on administrator-defined settings. This involves both reading values from configuration objects in custom code and enabling administrators to modify these values with a settings form.

In this tutorial, we'll:

- Demonstrate accessing configuration data with the `config.factory` service.
- Examine the module's settings form's interaction with the Configuration API.
- Adjust the `WeatherPage` controller's behavior based on administrator-defined configuration.

By the end of this tutorial, you should be able to read and output simple configuration data within a module.

## Goal

Use configuration data from the module's settings form in the `WeatherPage` controller.

## Prerequisites

- [Concept: Configuration API](https://drupalize.me/tutorial/concept-configuration-api)
- [Create a Settings Form For the Anytown Module](https://drupalize.me/tutorial/create-settings-form-anytown-module)
- [Concept: Dependency Injection](https://drupalize.me/tutorial/concept-dependency-injection)

## Video tutorial

Sprout Video

## Reading and writing configuration data

Retrieve configuration data using the `config.factory` service, accessible either through dependency injection or the `\Drupal::configFactory()` global. The shorthand `\Drupal::config('name')` is equivalent to `\Drupal::configFactory()->get('name')`.

This service offers 2 methods for retrieving configuration data:

- `get()` for a read-only version
- `getEditable()` for a mutable version

Drupal provides both immutable and mutable configuration objects to balance flexibility with performance. Immutable objects are cacheable and ensure stability, while mutable objects allow for adjustments based on input from administrative users.

In [Create a Settings Form for the Anytown Module](https://drupalize.me/tutorial/create-settings-form-anytown-module), we designed a settings form for administrators to specify a location for weather forecasts. These settings are stored as simple configuration data. Let's revisit the code in *anytown/src/Form/SettingsForm.php* and examine how we're using the Configuration API:

```
<?php 

declare(strict_types=1);

namespace Drupal\anytown\Form;

use Drupal\Core\Form\ConfigFormBase;
use Drupal\Core\Form\FormStateInterface;

/**
 * Configure Anytown settings for this site.
 */
final class SettingsForm extends ConfigFormBase {

  /**
   * Name for module's configuration object.
   */
  const SETTINGS = 'anytown.settings';

  /**
   * {@inheritdoc}
   */
  public function getFormId(): string {
    return self::SETTINGS;
  }

  /**
   * {@inheritdoc}
   */
  protected function getEditableConfigNames(): array {
    return [self::SETTINGS];
  }

  /**
   * {@inheritdoc}
   */
  public function buildForm(array $form, FormStateInterface $form_state): array {
    $form['display_forecast'] = [
      '#type' => 'checkbox',
      '#title' => $this->t('Display weather forecast'),
      '#default_value' => $this->config(self::SETTINGS)->get('display_forecast'),
    ];

    $form['location'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Market zip-code'),
      '#description' => $this->t('Used to determine weekend weather forecast.'),
      '#default_value' => $this->config(self::SETTINGS)->get('location'),
      '#placeholder' => '90210',
    ];

    $form['weather_closures'] = [
      '#type' => 'textarea',
      '#title' => $this->t('Weather related closures'),
      '#description' => $this->t('List one closure per line.'),
      '#default_value' => $this->config(self::SETTINGS)->get('weather_closures'),
    ];
    return parent::buildForm($form, $form_state);
  }

  /**
   * {@inheritdoc}
   */
  public function validateForm(array &$form, FormStateInterface $form_state): void {
    parent::validateForm($form, $form_state);

    // Verify that the location field contains an integer and that it is 5
    // digits long.
    $location = $form_state->getValue('location');
    $value = filter_var($location, FILTER_VALIDATE_INT);
    if (!$value || strlen((string) $value) !== 5) {
      // Set an error on the specific field. This will halt form processing
      // and re-display the form with errors for the user to correct.
      $form_state->setErrorByName('location', $this->t('Invalid zip-code'));
    }

  }

  /**
   * {@inheritdoc}
   */
  public function submitForm(array &$form, FormStateInterface $form_state) {
    $this->config(self::SETTINGS)
      ->set('display_forecast', $form_state->getValue('display_forecast'))
      ->set('location', $form_state->getValue('location'))
      ->set('weather_closures', $form_state->getValue('weather_closures'))
      ->save();

    $this->messenger()->addMessage($this->t('Anytown configuration updated.'));
  }

}
```

## Naming configuration objects

Every simple configuration object needs a unique name. It's common to prefix your module's configuration with the module's name. A module can have more than one configuration object if there's a logical reason to do so. We chose to store the name in a constant, which we'll reference using `self::SETTINGS` within our class' methods.

We gave our module's configuration object the name, `anytown.settings`.

```
const SETTINGS = 'anytown.settings';
```

## Retrieving configuration

When building the form, we retrieved a stored configuration value by referencing a key within the configuration object:

```
$this->config(self::SETTINGS)->get('display_forecast')
```

- The call to `config()` loads the `anytown.settings` configuration object from the active configuration store, and then `get('display_forecast')` retrieves the value of a specific key from that object.

## Getting editable configuration objects

By default, when you load a config object it's immutable, or read only. In order to update configuration data when the form is submitted, we need to load a mutable version of the configuration object. We do this by listing the specific configuration objects that we want to make editable in `getEditableConfigNames()`, which in our case is `anytown.settings`.

```
protected function getEditableConfigNames(): array {
 return [self::SETTINGS];
}
```

- This tells the config factory service (`$this->config()`) that it should supply a mutable (editable) version of the `anytown.settings` configuration object.
- By retrieving a mutable configuration object, this means in the `submitForm()` method, we can use the `set()` method of the config factory to update the values in the configuration object with values entered in the form by the user.

After saving, the `anytown.settings` configuration might look like this:

```
anytown.settings:
   display_forecast: true
   location: '81623'
   weather_closures: "Location one\r\nAnother location"
```

## Use configuration values in a controller

Let's use these stored values in the `WeatherPage` controller to specify the location of the weather forecast we want to display, and to show any configured weather related closures. Update the code in *anytown/src/Controller/WeatherPage.php* to the following:

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

    // Get the configuration object from the configuration factory service.
    $settings = $this->config('anytown.settings');

    // This is hypothetical, because our API is mocked, but shows how you could
    // use the location setting in constructing the API query.
    $url = 'https://module-developer-guide-demo-site.ddev.site/modules/custom/anytown/data/weather_forecast.json';
    if ($location = $settings->get('location')) {
      $url .= '?location=' . $location;
    }

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
        '#title' => 'Weather related closures',
        '#items' => explode(PHP_EOL, $settings->get('weather_closures')),
      ],
    ];

    return $build;
  }

}
```

This update:

- Uses the configured `location` setting to pass an `?location=` parameter to the forecast API.
- Replaces the hard-coded weather closure list with values from the configuration object.

## Verify it works

1. [Clear the cache](https://drupalize.me/tutorial/clear-drupals-cache).
2. Open the */weather* page in your browser. You should see the weather closures section of the page displays whatever values were included in the configuration.

If you update the settings using the form, you'll have to clear the cache again to see the new values reflected on the */weather* page. In [Add Cache Context and Tags to Renderable Arrays](https://drupalize.me/tutorial/add-cache-context-and-tags-renderable-arrays), we'll learn about adding the configuration object as dependency to the page's output, so that when the configuration changes the page cache is invalidated.

## Recap

This tutorial illustrated reading and writing simple configuration data within a module, enabling administrators to customize a module's functionality.

## Further your understanding

- Identify scenarios that justify a settings form in custom modules.
- Explore Drupal core for simple configuration usage examples.
- Discuss the rationale behind immutable and mutable configuration objects in Drupal.

## Additional resources

- [Use Simple Configuration in a Form](https://drupalize.me/tutorial/use-simple-configuration-form) (Drupalize.Me)
- [Configuration Management course](https://drupalize.me/course/configuration-management) (Drupalize.Me)
- [Configuration API](https://api.drupal.org/api/drupal/core%21core.api.php/group/config_api) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Configuration API](/tutorial/concept-configuration-api?p=3243)

Next
[Define a Configuration Schema and Default Values](/tutorial/define-configuration-schema-and-default-values?p=3243)

Clear History

Ask Drupalize.Me AI

close