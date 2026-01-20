---
title: "Use a Service in a Controller"
url: "https://drupalize.me/tutorial/use-service-controller?p=3238"
guide: "[[drupal-module-developer-guide]]"
order: 26
---

# Use a Service in a Controller

## Content

Controllers in Drupal frequently need to use services to figure out what information to display on the page. This might include querying for a list of entities, getting information about the current user, or accessing saved configuration. It's a best practice to always use dependency injection to supply services to a controller. In the *anytown* module we can improve the `WeatherPage` controller by making it access a weather forecast API to get up-to-date data.

In this tutorial, we'll:

- Set up a mock weather forecast API.
- Refactor our `WeatherPage` controller to inject the `http_client` service.
- Update the logic in the `build()` method of our controller to use the provided service to get and display a weather forecast.

By the end of this tutorial, you should be able to use dependency injection to give a controller in a Drupal module the services it requires, and then make use of those services in building the page content.

## Goal

Use the HTTP client service (`http_client`) in the `WeatherPage` controller to access a third-party weather API via HTTP.

## Prerequisites

- [Concept: Services and the Container](https://drupalize.me/tutorial/concept-services-and-container)
- [Concept: Dependency Injection](https://drupalize.me/tutorial/concept-dependency-injection)
- You've created the `WeatherPage` controller in [Create a Controller for the Weather Page](https://drupalize.me/tutorial/create-controller-weather-page).

## Video tutorial

Sprout Video

## Set up the mock weather API

This tutorial requires some additional setup to enable a mock weather API that we can use to simulate HTTP requests that retrieve weather data. We'll use the dummy data below and make HTTP requests to retrieve the file. This simulates the response you might get from a real weather API but doesn't require us to create an account or pay for API access.

In the *anytown* module, create the file *data/weather\_forecast.json* and populate it with the data below.

Show example JSON data

```
{
  "cod": "200",
  "message": 0,
  "cnt": 40,
  "list": [
    {
      "day": "friday",
      "main": {
        "temp": 278.15,
        "feels_like": 274.85,
        "temp_min": 272.15,
        "temp_max": 279.15,
        "pressure": 1020,
        "sea_level": 1020,
        "grnd_level": 980,
        "humidity": 80,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 600,
          "main": "Snow",
          "description": "light snow",
          "icon": "https://raw.githubusercontent.com/erikflowers/weather-icons/master/svg/wi-day-snow.svg"
        }
      ],
      "clouds": {
        "all": 75
      },
      "wind": {
        "speed": 3.6,
        "deg": 320,
        "gust": 5.7
      },
      "visibility": 10000,
      "pop": 0.4,
      "snow": {
        "3h": 0.12
      },
      "sys": {
        "pod": "d"
      }
    },
    {
      "day": "saturday",
      "main": {
        "temp": 281.32,
        "feels_like": 279.15,
        "temp_min": 271.32,
        "temp_max": 281.32,
        "pressure": 1012,
        "sea_level": 1012,
        "grnd_level": 970,
        "humidity": 70,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 802,
          "main": "Clouds",
          "description": "scattered clouds",
          "icon": "https://raw.githubusercontent.com/erikflowers/weather-icons/master/svg/wi-day-sunny-overcast.svg"
        }
      ],
      "clouds": {
        "all": 40
      },
      "wind": {
        "speed": 4.1,
        "deg": 290,
        "gust": 6.7
      },
      "visibility": 10000,
      "pop": 0.1,
      "sys": {
        "pod": "d"
      }
    },
    {
      "day": "sunday",
      "main": {
        "temp": 281.32,
        "feels_like": 279.15,
        "temp_min": 278.32,
        "temp_max": 281.32,
        "pressure": 1012,
        "sea_level": 1012,
        "grnd_level": 970,
        "humidity": 70,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 802,
          "main": "Clouds",
          "description": "scattered clouds",
          "icon": "https://raw.githubusercontent.com/erikflowers/weather-icons/master/svg/wi-day-sunny-overcast.svg"
        }
      ],
      "clouds": {
        "all": 40
      },
      "wind": {
        "speed": 4.1,
        "deg": 290,
        "gust": 6.7
      },
      "visibility": 10000,
      "pop": 0.1,
      "sys": {
        "pod": "d"
      }
    }
  ],
  "city": {
    "id": 5037649,
    "name": "Minneapolis",
    "coord": {
      "lat": 44.98,
      "lon": -93.26
    },
    "country": "US",
    "population": 429606,
    "timezone": -18000,
    "sunrise": 1667745567,
    "sunset": 1667782834
  }
}
```

Next, we need to determine the URL for the mock weather API. In our example this is:

```
https://module-developer-guide-demo-site.ddev.site/modules/custom/anytown/data/weather_forecast.json
```

This breaks down to the URL of the development environment where your Drupal application can be accessed followed by the full path to the file on disk relative to the Drupal root directory. You will need to edit this URL per your environment. To test, access the URL and verify that you can view the JSON data in your browser.

If for some reason this doesn't work with your development environment, you can also use the file hosted on GitHub at this URL:

```
https://raw.githubusercontent.com/DrupalizeMe/module-developer-guide-demo-site/main/backups/weather_forecast.json
```

## Request data from the weather API

Right now the weather forecast displayed via the `WeatherPage` controller on the page at */weather* is hard-coded into the controller. Let's update the controller so that it:

- Uses the Drupal HTTP client service to make an HTTP request to a third-party weather API.
- Retrieves the current weather forecast.
- Displays the retrieved forecast on the page.
- Logs any errors to Drupal's system log.

This will require us to:

- Use dependency injection to access the HTTP client service in the controller.
- Use the HTTP client service to make an HTTP request.
- Format the data retrieved from the API as HTML, or log an error if the API returns an error.

### Determine the service name

To use a service you first need to know its unique machine name. For the HTTP client service that's `http_client`. To learn how to find a service's name see [Locate and Identify Existing Services](https://drupalize.me/tutorial/locate-and-identify-existing-services).

For type hinting you'll also need to know the class, or interface. The `http_client` service uses the interface, `GuzzleHttp\ClientInterface`.

### Inject the services into the controller

As of Drupal 10.2, the quickest way to add services to a controller is using autowiring, which inspects the type hints of the arguments passed to the controller's `__construct()` method and injects the relevant service(s). This approach simplifies controller boilerplate and aligns with modern PHP practices.

Since our `WeatherPage` controller extends `ControllerBase`, which already uses `AutowireTrait` (as of Drupal 10.2), we automatically have autowiring available without needing to explicitly add the trait.

The final code of the *WeatherPage.php* file should look like this:

```
<?php

declare(strict_types=1);

namespace Drupal\anytown\Controller;

use Drupal\Core\Controller\ControllerBase;
use Drupal\Core\Logger\RfcLogLevel;
use GuzzleHttp\ClientInterface;
use GuzzleHttp\Exception\RequestException;

/**
 * Controller for anytown.weather_page route.
 */
class WeatherPage extends ControllerBase {

  /**
   * HTTP client.
   *
   * @var \GuzzleHttp\ClientInterface
   */
  private $httpClient;

  /**
   * Logging service, set to 'anytown' channel.
   *
   * @var \Psr\Log\LoggerInterface
   */
  private $logger;

  /**
   * WeatherPage controller constructor.
   *
   * @param \GuzzleHttp\ClientInterface $http_client
   *   HTTP client.
   */
  public function __construct(ClientInterface $http_client) {
    $this->httpClient = $http_client;
    $this->logger = $this->getLogger('anytown');
  }

  /**
   * Builds the response.
   */
  public function build(string $style): array {
    // Style should be one of 'short', or 'extended'. And default to 'short'.
    $style = (in_array($style, ['short', 'extended'])) ? $style : 'short';

    $url = 'https://module-developer-guide-demo-site.ddev.site/modules/custom/anytown/data/weather_forecast.json';
    $data = NULL;

    try {
      $response = $this->httpClient->get($url);
      $data = json_decode($response->getBody()->getContents());
    }
    catch (RequestException $e) {
      $this->logger->log(RfcLogLevel::WARNING, $e->getMessage());
    }

    if ($data) {
      $forecast = '<ul>';
      foreach ($data->list as $day) {
        $weekday = ucfirst($day->day);
        $description = array_shift($day->weather)->description;
        // Convert units in Kelvin to Fahrenheit.
        $high = round(($day->main->temp_max - 273.15) * 9 / 5 + 32);
        $low = round(($day->main->temp_min - 273.15) * 9 / 5 + 32);
        $forecast .= "<li>$weekday will be <em>$description</em> with a high of $high and a low of $low.</li>";
      }
      $forecast .= '</ul>';
    }
    else {
      $forecast = '<p>Could not get the weather forecast. Dress for anything.</p>';
    }

    $output = "<p>Check out this weekend's weather forecast and come prepared. The market is mostly outside, and takes place rain or shine.</p>";
    $output .= $forecast;

    return [
      '#markup' => $output,
    ];
  }

}
```

In this updated code we've made the following changes:

- Extended `ControllerBase`, which already uses `AutowireTrait` (as of Drupal 10.2). This gives us autowiring capability without needing to explicitly add the trait. If you were creating a controller that doesn't extend `ControllerBase`, you would need to add `use Drupal\Core\DependencyInjection\AutowireTrait;` to your class.
- Added a `__construct()` method with a single argument type hinted as `\GuzzleHttp\ClientInterface`. Since the interface can be resolved automatically, Drupal's autowiring will inject the `http_client` service.
- Obtained a `$logger` channel service from the `getLogger()` method provided by `ControllerBase`.
- In the `__construct()` method, we assigned the provided services to local variables, so they can be accessed by other code in the class.
- Used the `http_client` service to make an API request with: `$response = $this->httpClient->get($url);`.
- Formatted the JSON response as an unordered list.
- **Note:** The API request is made to the URL we determined in the setup step above.
- Caught any errors returned from the API and logged them using the logger object provided by the `logger.factory` service.

When **type hinting** injected services passed into the `__construct()` method, you should use the service **interface**, and not a specific implementation class, whenever possible. This ensures that your code is coupled to what the service *can do*, not *how* it does it.

#### Use the #[Autowire] attribute

When a service cannot be resolved by its interface alone (for example, when you need a specific cache bin), use the `#[Autowire]` PHP attribute to specify the service ID manually. Here's an example:

```
use Drupal\Core\Cache\CacheBackendInterface;
use Drupal\Core\DependencyInjection\Attribute\Autowire;

public function __construct(
  #[Autowire(service: 'cache.default')]
  protected CacheBackendInterface $cache,
) {}
```

In this example, the `#[Autowire]` attribute explicitly tells Drupal to inject the `cache.default` service, even though `CacheBackendInterface` could refer to multiple cache backends.

#### Understand the legacy create() method pattern

Autowiring is relatively new (Drupal 10.2+), and while you should use it whenever possible, it's also good to understand the `create()` factory method pattern that autowiring implements, as you'll still see it used frequently in existing Drupal code. In this legacy pattern, controllers implement `ContainerInjectionInterface` so that Drupal knows to initialize the controller by calling the static `create()` method.

The `create()` method returns a new instance of the `WeatherPage` controller and uses the provided `$container` argument to initialize the required services and pass them to the controller's `__construct()` method. Here's what the code in the `WeatherPage` controller might look like without the use of autowiring:

```
  /**
   * WeatherPage controller constructor.
   *
   * @param \GuzzleHttp\ClientInterface $http_client
   *   HTTP client.
   */
  public function __construct(ClientInterface $http_client) {
    $this->httpClient = $http_client;
    $this->logger = $this->getLogger('anytown');
  }

  /**
   * {@inheritDoc}
   */
  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('http_client')
    );
  }
```

This legacy approach is still fully supported and works in all versions of Drupal. However, for Drupal 10.2 and later, using `AutowireTrait` is the recommended approach as it requires less boilerplate code.

The key takeaway from this example should be understanding that dependency injection can be accomplished either through autowiring (modern, Drupal 10.2+) or the manual `create()` method pattern (legacy but still supported). Both patterns accomplish the same goal of injecting services into the controller class.

### Verify it works

After making the updates above, navigate to the */weather* page on your site. It should now display the data retrieved from the mock weather API on the page as an HTML list. You can test the error handling by changing URL used for the request to a known 404 page and refreshing the */weather* page.

The downside of this approach is that our controller now contains logic for making an API request and formatting that data. In this setup, some of that logic, like the code that converts from Kelvin to Fahrenheit would be pretty difficult to test. And, it means that if we want to create a block that displays the weather forecast, we'll have some duplicate code. In [Define a Weather Forecast Service](https://drupalize.me/tutorial/define-weather-forecast-service) we'll look at how this code can be refactored and further improved.

## Recap

In this tutorial, we updated our `WeatherPage` controller to use the HTTP client service to make requests to a weather forecast API to get data to display on the */weather* page. We implemented dependency injection to access the required services. And learned about how to obtain a service from the service container using its machine name.

## Further your understanding

- How would you update the code in this example to inject the `current_user` service?
- Explain in your own words the difference between these 2 lines of code in the `create()` method; `$container->get('http_client')` and `$container->get('logger.factory')->get('anytown')`.

## Additional resources

- [Services](https://drupalize.me/topic/services) (Drupalize.Me)
- [Services and Dependency Injection](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection) (Drupal.org)
- [Inject Services into a Form Controller](https://drupalize.me/tutorial/inject-services-form-controller) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Locate and Identify Existing Services](/tutorial/locate-and-identify-existing-services?p=3238)

Next
[Concept: Creating Custom Services](/tutorial/concept-creating-custom-services?p=3238)

Clear History

Ask Drupalize.Me AI

close