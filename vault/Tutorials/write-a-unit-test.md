---
title: "Write a Unit Test"
url: "https://drupalize.me/tutorial/write-unit-test?p=3245"
guide: "[[drupal-module-developer-guide]]"
---

# Write a Unit Test

## Content

Unit tests are the simplest among Drupal's test types, ideal for verifying code that performs computations. This tutorial guides through writing unit tests for the *anytown* module, focusing on the `ForecastClient` service, and illustrates how to use mocks for dependencies.

In this tutorial, we'll:

- List potential unit tests for the *anytown* module.
- Write tests for `ForecastClient` service logic.
- Demonstrate how to mock services in unit tests.

By the end of this tutorial you should be able to write PHPUnit Unit tests for logic in the *anytown* module.

## Goal

Write unit tests for the `ForecastClient` weather API forecast service class.

## Prerequisites

- [Concept: Testing](https://drupalize.me/tutorial/concept-testing)
- [Configure Environment to Run Tests](https://drupalize.me/tutorial/configure-your-environment-run-tests)
- [Define a Weather Forecast Service](https://drupalize.me/tutorial/define-weather-forecast-service)

## Video tutorial

Sprout Video

## What are we testing?

To make sure that our custom module continues to function when we add additional new features in the future, we should write some tests for it. The `Drupal\anytown\ForecastClient` class offers 2 prime candidates for unit testing:

- `ForecastClient::kelvinToFahrenheit`: Simple logic for temperature conversion.
- `ForecastClient::getForecastData()`: Error logging during API connection issues.

## Add unit tests to the Anytown module

### Scaffold a new unit test class

Unit tests live in the *tests/src/Unit/* subdirectory of the module and are namespaced with the pattern, `namespace Drupal\Tests\MODULE_NAME\Unit`. Test class names should end with `Test`.

Create the file *tests/src/Unit/ForecastClientTest.php*.

### Add the unit test

Add the following code to *anytown/tests/src/Unit/ForecastClientTest.php*:

```
<?php

namespace Drupal\Tests\anytown\Unit;

use Drupal\anytown\ForecastClient;
use Drupal\Core\Cache\CacheBackendInterface;
use Drupal\Core\Logger\LoggerChannelFactoryInterface;
use Drupal\Tests\UnitTestCase;
use GuzzleHttp\Client;
use GuzzleHttp\Exception\TransferException;
use Psr\Log\LoggerInterface;

/**
 * Unit tests for ForecastClient service.
 */
class ForecastClientTest extends UnitTestCase {

  /**
   * Tests the kelvinToFahrenheit method.
   *
   * @covers \Drupal\anytown\ForecastClient::kelvinToFahrenheit()
   */
  public function testKelvinToFahrenheit() {
    // Example test cases.
    $testCases = [
      // Absolute zero.
      [
        'f' => -460,
        'k' => 0,
      ],
      // Freezing point of water.
      [
        'f' => 32,
        'k' => 273.15,
      ],
    ];

    foreach ($testCases as $case) {
      $fahrenheit = ForecastClient::kelvinToFahrenheit($case['k']);
      $this->assertEquals($case['f'], $fahrenheit, "Kelvin to Fahrenheit conversion failed for {$case['k']}K");
    }
  }

  /**
   * Tests getForecastData with an API failure.
   *
   * @covers \Drupal\anytown\ForecastClient::getForecastData()
   */
  public function testGetForecastDataApiFailure() {
    // Mocking the dependencies.
    $httpClientMock = $this->createMock(Client::class);
    $loggerFactoryMock = $this->createMock(LoggerChannelFactoryInterface::class);
    $loggerMock = $this->createMock(LoggerInterface::class);
    $cacheBackendMock = $this->createMock(CacheBackendInterface::class);

    // Setting up the httpClientMock to throw a GuzzleException.
    $httpClientMock->method('get')->willThrowException(new TransferException('API Request Failed'));

    // Configure the logger factory mock to return the logger mock.
    $loggerFactoryMock->method('get')->willReturn($loggerMock);

    // Expect the logger to record a warning.
    $loggerMock->expects($this->once())
      ->method('warning')
      ->with($this->equalTo('API Request Failed'));

    // Creating an instance of ForecastClient with mocked dependencies.
    $forecastClient = new ForecastClient($httpClientMock, $loggerFactoryMock, $cacheBackendMock);

    // Calling getForecastData and expecting NULL due to API failure.
    $result = $forecastClient->getForecastData('http://example.com/api', TRUE);
    $this->assertNull($result, 'Expected NULL on API request failure');
  }

}
```

This test verifies that `ForecastClient` correctly converts temperatures from Kelvin to Fahrenheit and handles API request failures as expected. By mocking dependencies, the tests remain focused on the PHP logic in the class, and not the integration with the dependencies.

Important things to note in this code:

- The test class name ends with the word, `Test`.
- The test class extends `Drupal\Tests\UnitTestCase`.
- There are 2 public methods whose names start with `test`. These are test cases and will be automatically called by the test runner after the testing environment has been bootstrapped.
- The `testKelvinToFahrenheit` uses predefined test cases representing known Kelvin to Fahrenheit conversions. Because the `kelvinToFahrenheit` method is static, we can call it without having to initialize the class. The `assertEquals()` method is used to compare values and register a testing failure if the actual output does not match the expected output.
- The `testGetForecastDataApiFailure()` method tests the `getForecastData` method's behavior when an API request fails. It mocks necessary dependencies such as the HTTP client, logger, and cache backend to simulate an API request failure. And it ensures the method handles the failure gracefully by logging a warning and returning NULL.

### Run the tests

Run the new tests with the following command:

```
./vendor/bin/phpunit -c web/core/ web/modules/custom/anytown/tests/src/Unit/ForecastClientTest.php
```

## Key concepts used in our test

We used several **key concepts** in this test class:

### Mocking

Dependencies of the ForecastClient (HTTP client, logger, and cache backend) are *mocked* using PHPUnit's `createMock` method. This isolates the test environment from external systems and ensures the tests are focused on the logic within the `ForecastClient` class. It also allows the test to run without a functioning Drupal environment. This is made possible because of our use of [dependency injection](https://drupalize.me/tutorial/concept-dependency-injection).

### Exception simulation

The mock HTTP client is configured to throw a `TransferException` to simulate an API request failure, testing the error handling logic of `ForecastClient`.

### Assertions

*Assertions* in PHPUnit (`assertEquals` and `assertNull`) are used to verify that the method outputs match the expected results under different conditions (correct conversions and handling of API failures).

### Annotations

The `@covers` *annotation* indicates which method each test is targeting, improving clarity and test coverage analysis.

## Recap

In this tutorial, we demonstrated how to write and execute a PHPUnit-Unit test in a custom Drupal module. We wrote test cases for 2 of the methods on the `Drupal\anytown\ForecastClient` service class. Running these tests will help ensure that as the code evolves, it continues to work as expected. In the process, we learned where to place unit test code, the types of logic unit tests are good for, and how to use mock objects to simulate the Drupal-provided services our code relies on, without requiring a fully-functional Drupal environment.

## Further your understanding

- Can you find a list of the other assertion methods available in a unit test class?
- The `testGetForecastDataApiFailure()` method only tests for failures. Can you update the test class to also test the "happy path" where the API returns a result and that result is properly returned by the `getForecastData()` method?
- How would you write a test that verifies caching is working in the `ForecastClient` code?

## Additional resources

- [Implement a Unit Test in Drupal](https://drupalize.me/tutorial/implement-unit-test-drupal) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Configure Your Environment to Run Tests](/tutorial/configure-your-environment-run-tests?p=3245)

Next
[Write a Kernel Test](/tutorial/write-kernel-test?p=3245)

Clear History

Ask Drupalize.Me AI

close