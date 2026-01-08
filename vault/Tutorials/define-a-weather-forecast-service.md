---
title: "Define a Weather Forecast Service"
url: "https://drupalize.me/tutorial/define-weather-forecast-service?p=3238"
guide: "[[drupal-module-developer-guide]]"
---

# Define a Weather Forecast Service

## Content

The logic for retrieving and processing a weather forecast is hard-coded into the `WeatherPage` controller. To make our code more reusable, maintainable, and organized, we can refactor this code into a custom weather forecast API service.

In this tutorial, we'll:

- Define a PHP interface for a weather forecast API service and write an implementation of that service.
- Create a service definition file to inform Drupal about our new service and its dependencies.
- Refactor the `WeatherPage` controller to use the new service, which will clean up duplicate code.

By the end of this tutorial, you'll be able to define and use a custom service in a Drupal module.

## Goal

Define a new weather forecast API service and refactor the `WeatherPage` controller to use this service.

## Prerequisites

- [Concept: Creating Custom Services](https://drupalize.me/tutorial/concept-creating-custom-services)
- [Use a Service in a Controller](https://drupalize.me/tutorial/use-service-controller)
- [Concept: PHP Namespaces and PSR-4](https://drupalize.me/tutorial/concept-php-namespaces-and-psr-4)

## Video tutorial

Sprout Video

## Extract custom logic from the `WeatherPage` controller

To maintain a thin `WeatherPage` controller and enable reuse of the custom weather forecast code, we'll extract the custom logic into a service. This service will be responsible for retrieving the latest forecast from the API, handling errors, caching responses, and preparing the JSON data for use. After this extraction, we can refactor the `WeatherPage` controller to use the new service. Later in the guide, we'll write unit tests for the service logic.

To define a new service, we need to:

- Create a PHP interface for the service.
- Write a class that implements the interface.
- Tell Drupal's service container about the service with a *MODULE\_NAME.services.yml* file.

The custom service's PHP code should use PSR-4 namespacing, and live in the `namespace Drupal\anytown` (within the module's *src/* directory). The services YAML file lives in the module's root directory, alongside *MODULE\_NAME.info.yml*.

### Create the interface

Begin by creating an interface to define the service's functionality. This will inform other code, such as the `WeatherPage` controller, about the service object's available methods and expected outcomes. If you're not sure what the interface should include, it can be helpful to draft the service implementation class first, use it, and then create the interface based on practical application.

For our service, we require a method to retrieve and return a forecast. The data should be returned in a manageable structure, and leave formatting in HTML (or some other format) to the controller.

Create the file *anytown/src/ForecastClientInterface.php* with the following code:

```
<?php 

declare(strict_types=1);

namespace Drupal\anytown;

/**
 * Forecast retrieval API client.
 */
interface ForecastClientInterface {

  /**
   * Get the current forecast.
   *
   * @param string $url
   *   URL to use to retrieve forecast data.
   *
   * @return array|null
   *   An array containing the formatted data for the forecast, or null.
   */
  public function getForecastData(string $url): ?array;

}
```

This interface guarantees that any service implementation will have a `getForecastData()` method that returns a forecast.

### Create the `ForecastClient` class

Write a class that fulfills the `ForecastClientInterface`. This class will provide the `getForecastData()` method.

Create the file *anytown/src/ForecastClient.php* with the following code:

```
<?php 

declare(strict_types=1);

namespace Drupal\anytown;

use Drupal\Core\Logger\LoggerChannelFactoryInterface;
use GuzzleHttp\ClientInterface;
use GuzzleHttp\Exception\GuzzleException;

/**
 * Forecast retrieval API client.
 */
class ForecastClient implements ForecastClientInterface {

  /**
   * Guzzle HTTP client.
   *
   * @var \GuzzleHttp\ClientInterface
   */
  protected $httpClient;

  /**
   * Logger channel.
   *
   * @var \Psr\Log\LoggerInterface
   */
  protected $logger;

  /**
   * Construct a forecast API client.
   *
   * @param \GuzzleHttp\ClientInterface $httpClient
   *    Guzzle HTTP client.
   * @param \Drupal\Core\Logger\LoggerChannelFactoryInterface $logger_factory
   *   Logger factory service.
   */
  public function __construct(ClientInterface $httpClient, LoggerChannelFactoryInterface $logger_factory) {
    $this->httpClient = $httpClient;
    $this->logger = $logger_factory->get('anytown');
  }

  /**
   * {@inheritDoc}
   */
  public function getForecastData(string $url) : ?array {
    try {
      $response = $this->httpClient->get($url);
      $json = json_decode($response->getBody()->getContents());
    }
    catch (GuzzleException $e) {
      $this->logger->warning($e->getMessage());
      return NULL;
    }

    $forecast = [];
    foreach ($json->list as $day) {
      $forecast[$day->day] = [
        'weekday' => ucfirst($day->day),
        'description' => $day->weather[0]->description,
        'high' => $this->kelvinToFahrenheit($day->main->temp_max),
        'low' => $this->kelvinToFahrenheit($day->main->temp_min),
        'icon' => $day->weather[0]->icon,
      ];
    }

    return $forecast;
  }

  /**
   * Helper to convert temperature values form Kelvin to Fahrenheit.
   *
   * @param float $kelvin
   *   Temperature in Kelvin.
   *
   * @return float
   *   Temperature in Fahrenheit.
   */
  public static function kelvinToFahrenheit(float $kelvin) : float {
    return round(($kelvin - 273.15) * 9 / 5 + 32);
  }

}
```

This class, `Drupal\anytown\ForecastClient`, does the following:

- Implements dependency injection for the HTTP client and logging services via the constructor.
- Transfers the weather forecast retrieval logic from the `WeatherPage` controller to the `getForecastData()` method.
- Converts the logic for temperature conversion from Kelvin to Fahrenheit into a helper method, `kelvinToFahrenheit()`.

### Declare the new service to Drupal

If it doesn't exist, create the file *anytown.services.yml* with:

```
services:
  anytown.forecast_client:
    class: Drupal\anytown\ForecastClient
    arguments: ['@http_client', '@logger.factory']
  Drupal\anytown\ForecastClientInterface: '@anytown.forecast_client'
```

This code:

- Assigns `anytown.forecast_client` as the service's unique identifier.
- Defines the service's class. (Note: it points to the implementation not the interface.)
- Specifies the class' dependencies in the `arguments` array. Service names are prefixed with `@` denoting it's a *service* and **not** a string or other parameter.

When an instance of the `anytown.forecast_client` service is requested from the service container, it will use this definition to figure out which class to use and what argument values to pass to the class constructor.

### Refactor the `WeatherPage` controller

With the new service available, we can now refactor the `WeatherPage` controller to integrate the service.

Modify *anytown/src/Controller/WeatherPage.php*:

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
    if ($forecast_data) {
      $forecast = '<ul>';
      foreach ($forecast_data as $item) {
        [
          'weekday' => $weekday,
          'description' => $description,
          'high' => $high,
          'low' => $low,
        ] = $item;
        $forecast .= "<li>$weekday will be <em>$description</em> with a high of $high and a low of $low.</li>";
      }
      $forecast .= '</ul>';
    }
    else {
      $forecast = '<p>Could not get the weather forecast. Dress for anything.</p>';
    }

    $output = "<p>Check out this weekend's weather forecast and come prepared. The market is mostly outside, and takes place rain or shine.</p>";
    $output .= $forecast;
    $output .= '<h3>Weather related closures</h3></h3><ul><li>Ice rink closed until winter - please stay off while we prepare it.</li><li>Parking behind Apple Lane is still closed from all the rain last week.</li></ul>';

    return [
      '#markup' => $output,
    ];
  }

}
```

We refactored the `WeatherPage` controller by:

- Injecting the `ForecastClient` service into the `WeatherPage` controller
- Adjusting the `build` method to use the service for fetching forecast data

The `ForecastClient` service now encapsulates HTTP request responsibilities, and makes our code more modular and maintainable.

### Verify it works

Ensure the following files in the *anytown* module have been created or modified:

- *anytown.services.yml*
- *src/ForecastClientInterface.php*
- *src/ForecastClient.php*
- *src/Controller/WeatherPage.php*

[Clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) so Drupal can discover any new or updated service definitions.

Then, visit the */weather* page to confirm functionality. The page's content should remain unchanged as our changes focused on refactoring code to follow to best practices rather than changing functionality.

## Recap

This tutorial guided you through defining a custom service in a Drupal module and using it in a controller. We migrated logic from the controller to a service, making the logic reusable by other code. This required creating an interface, a class implementing the interface, and declaring the service in a definition file.

## Further your understanding

- How can you refine `Drupal\anytown\ForecastClientInterface::getForecastData` to standardize returned data regardless of the API used?
- Why and how would services integrate a third-party Composer library with Drupal?

## Additional resources

- [Services and Dependency Injection Container](https://api.drupal.org/api/drupal/core%21core.api.php/group/container/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Creating Custom Services](/tutorial/concept-creating-custom-services?p=3238)

Clear History

Ask Drupalize.Me AI

close