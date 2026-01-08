---
title: "Cache Data Retrieved from the Weather API"
url: "https://drupalize.me/tutorial/cache-data-retrieved-weather-api?p=3244"
guide: "[[drupal-module-developer-guide]]"
---

# Cache Data Retrieved from the Weather API

## Content

We can enhance our site's performance by using Drupal's cache backend service to cache and reuse results from an external API request. We can cache the results of weather forecast API queries within a custom service. This will give us an opportunity to practice implementing Drupal's caching capabilities and optimize the performance of our module.

In this tutorial, we'll:

- Inject the cache backend service into our forecast API service class.
- Implement caching to store and reuse weather forecast API results locally.

By the end of this tutorial, you'll understand how to use Drupal's cache backend service for data caching.

## Goal

Speed up weather forecast data retrieval by caching API query results.

## Prerequisites

- [Concept: Caching](https://drupalize.me/tutorial/concept-caching)
- [Define a Weather Forecast Service](https://drupalize.me/tutorial/define-weather-forecast-service)

## Video tutorial

Sprout Video

## Caching weather forecast data

The custom service we developed for querying the weather forecast API makes an HTTP request each time data is requested. Given that weather forecasts do not change significantly over short periods of time, caching these results can improve our module's performance.

### Inject the cache backend service

Each instance of the cache backend service is associated with a specific cache bin. For most use cases using the *default* bin is fine.

Update the *anytown.services.yml* file:

```
services:
  anytown.forecast_client:
    class: Drupal\anytown\ForecastClient
    arguments: ['@http_client', '@logger.factory', '@cache.default']
```

This update adds the `@cache.default` service to the list of arguments for the `anytown.forecast_client` service.

### Update the `ForecastClient` service

Modify the `ForecastClient` service to check for cached data before initiating new API requests.

Update the code in *src/ForecastClient.php*:

```
<?php

declare(strict_types=1);

namespace Drupal\anytown;

use Drupal\Core\Cache\CacheBackendInterface;
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
   * Caching service.
   *
   * @var \Drupal\Core\Cache\CacheBackendInterface
   */
  protected $cache;

  /**
   * Construct a forecast API client.
   *
   * @param \GuzzleHttp\ClientInterface $httpClient
   *   Guzzle HTTP client.
   * @param \Drupal\Core\Logger\LoggerChannelFactoryInterface $logger_factory
   *   Logger factory service.
   * @param \Drupal\Core\Cache\CacheBackendInterface $cacheBackend
   *   Caching service.
   */
  public function __construct(ClientInterface $httpClient, LoggerChannelFactoryInterface $logger_factory, CacheBackendInterface $cacheBackend) {
    $this->httpClient = $httpClient;
    $this->logger = $logger_factory->get('anytown');
    $this->cache = $cacheBackend;
  }

  /**
   * {@inheritDoc}
   */
  public function getForecastData(string $url, bool $reset_cache = FALSE) : ?array {
    // Create a unique cache ID using the URL.
    $cache_id = 'anytown:forecast:' . md5($url);

    // Look for an existing cache record.
    $data = $this->cache->get($cache_id);

    // If we find one, we can use the cached data, unless specifically asked not
    // to.
    if (!$reset_cache && $data) {
      $forecast = $data->data;
    }
    // If not, we need to request fresh data from the API.
    else {
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

      // Store the calculated data in the cache for next time, or until it's
      // more than 1 hour old.
      $this->cache->set($cache_id, $forecast, strtotime('+1 hour'));
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
   *   Temperature in Fahrenheit, rounded to the nearest int.
   */
  public static function kelvinToFahrenheit(float $kelvin) : float {
    return round(($kelvin - 273.15) * 9 / 5 + 32);
  }

}
```

This update:

- Updates the constructor to accept the `CacheBackendInterface $cacheBackend` service and assign it to a local variable.
- Changes the `getForecastData()` method signature to include a `$reset_cache` argument. This ensures that consumers of the service can bypass the cache and force the client to request fresh data from the API if they need to.
- Calculates a unique ID for the cached data. If cached data is stored as key/value pairs this is the key. In this case adding the URL of the request to the key ensures that if the URL changes, we'll assume the results changed, too, and the cached data will be stored with a different key.
- Refactors the code in `getForecastData()`, so that it checks to see if there is a record for this query in the cache already (or if the reset flag is set). If it finds a result, it returns the cached data and skips the rest of the logic in the method. If there's no cached data or the existing data has been invalidated, then it queries the forecast API, saves the results to the cache for next time, and then returns the data. This is a common pattern for implementing caching.
- Sets a cache duration of 1 hour. This ensures that data from the forecast API is never more than 1 hour old. Figuring out an appropriate duration depends on your use case. Aim to set this for as long as possible within the constraints of your application. Or, when applicable, use a different cache invalidation strategy. For example, if the data can be cached *forever* as long as the parameters of the configuration form don't change, you could add some logic to the submit handler of the form that invalidates this cached data if the configuration changes.

### Update the `ForecastClientInterface`

Since we modified the signature of the `getForecastData()` method, we need to update the interface to reflect this.

Edit *src/ForecastClientInterface.php* so that it contains the following:

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
   * @param boolean $reset_cache
   *   If TRUE always retrieve fresh data from the API and do not used cached
   *   data.
   *
   * @return array|null
   *   An array containing the formatted data for the forecast, or null.
   */
  public function getForecastData(string $url, bool $reset_cache): ?array;

}
```

### Verify it works

No noticeable changes should appear on the */weather* page; however, cached data should now speed up content rendering. Confirm by searching the `{cache_default}` table for `anytown:forecast:` keys or by inserting debug statements like `var_dump('cache-hit')` in the `getForecastData()` method.

## Recap

In this tutorial, we added caching to the forecast API client using Drupal's cache backend service. By caching previously fetched data for future use, we enhanced the performance of our custom */weather* page. This is a standard practice for enhancing performance. The same pattern can be applied to many different slow processes like CPU-heavy computation, or slow queries.

## Further your understanding

- Consider the use of static variables for optimizing performance when `getForecastData()` is invoked multiple times within a single request.
- Reflect on potential use cases for the `$reset_cache` parameter.

## Additional resources

- [Cache API Overview](https://drupalize.me/tutorial/cache-api-overview) (Drupalize.Me)
- [Overview: Drupal's Caching System](https://drupalize.me/tutorial/overview-drupals-caching-system) (Drupalize.Me)
- [Debug Drupal Cache Misses and Low Hit Rates](https://drupalize.me/tutorial/debug-drupal-cache-misses-and-low-hit-rates) (Drupalize.Me)
- [Cache API](https://api.drupal.org/api/drupal/core%21core.api.php/group/cache/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Caching](/tutorial/concept-caching?p=3244)

Next
[Add Cache Context and Tags to Renderable Arrays](/tutorial/add-cache-context-and-tags-renderable-arrays?p=3244)

Clear History

Ask Drupalize.Me AI

close