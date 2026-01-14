---
title: "Write a Kernel Test"
url: "https://drupalize.me/tutorial/write-kernel-test?p=3245"
guide: "[[drupal-module-developer-guide]]"
order: 74
---

# Write a Kernel Test

## Content

Kernel tests in Drupal enable module integration testing with Drupal core systems in a bootstrapped environment. Kernel tests bridge the gap between unit and functional tests. This tutorial focuses on writing kernel tests for the *anytown* module, specifically to test the `ForecastClient` service's caching logic and custom username validation.

In this tutorial, we'll:

- Explore the parts of a kernel test.
- Write kernel tests for *anytown* module features.
- Use mocks and the Drupal container in kernel tests.

By the end of this tutorial, you should be able to get started writing kernel tests to verify your module's integration with Drupal core.

## Goal

Write kernel tests for the `ForecastClient` service's caching logic and custom username validation constraints.

## Prerequisites

- [Concept: Testing](https://drupalize.me/tutorial/concept-testing)
- [Configure Environment to Run Tests](https://drupalize.me/tutorial/configure-your-environment-run-tests)
- [Add Custom Validation to User Entities](https://drupalize.me/tutorial/add-custom-validation-user-entities)
- [Cache Data Retrieved from the Weather API](https://drupalize.me/tutorial/cache-data-retrieved-weather-api)

## Video tutorial

Sprout Video

## Introduction to kernel testing

Kernel tests verify module integration with Drupal's core systems within a minimally bootstrapped Drupal environment. For example, you can test database interactions and service container usage with kernel tests.

### Kernel test environment details

Kernel tests create a minimal Drupal environment with:

- A functional database.
- The Drupal service container for core service usage and dependency injection.
- Specified modules and schemas without running the full module installation process.
- A balance in test execution speed between unit and functional tests.

## Testing the *anytown* module

Candidates for kernel testing in the *anytown* module include:

- Caching of API responses in the `ForecastClient` service. We can mock the API calls, then call `ForecastClient::getForecastData()` twice, and assert subsequent calls using cached data.
- In a kernel test we can enable the user module, create user entities, and make assertions about the custom username validation constraints.

## Testing the caching of `ForecastClient`

### Scaffold a new kernel test class

Kernel tests live in the *tests/src/Kernel/* subdirectory of the module and are namespaced using the pattern, `namespace Drupal\Tests\MODULE_NAME\Kernel`. Test class names should end with `Test`.

Create the file *tests/src/Kernel/ForecastClientCacheTest.php*.

### Write the tests

Add this code to *tests/src/Kernel/ForecastClientCacheTest.php*:

```
<?php

namespace Drupal\Tests\anytown\Kernel;

use Drupal\anytown\ForecastClient;
use Drupal\KernelTests\KernelTestBase;
use GuzzleHttp\Client;
use GuzzleHttp\Psr7\Response;

/**
 * Tests the caching of the getForecastData method in ForecastClient.
 *
 * @group anytown
 * @covers \Drupal\anytown\ForecastClient::getForecastData()
 */
class ForecastClientCacheTest extends KernelTestBase {

  /**
   * Modules to enable.
   *
   * @var array
   */
  protected static $modules = ['system', 'anytown'];

  /**
   * Test the caching of forecast data.
   */
  public function testForecastDataCaching() {
    // Mock the HTTP client.
    $testData = '{
    "list": [
      {
        "day": "friday",
        "main": {
          "temp_min": 272.15,
          "temp_max": 279.15
        },
        "weather": [
          {
            "description": "light snow",
            "icon": "https://raw.githubusercontent.com/erikflowers/weather-icons/master/svg/wi-day-snow.svg"
          }
        ]
      }
    ]}';
    $httpClientMock = $this->createMock(Client::class);
    $httpClientMock
      // The get method should only be called once, even though we request the
      // data twice. This is because the request should used cached data.
      ->expects($this->once())
      ->method('get')
      ->willReturn(new Response(200, [], $testData));

    // Create the ForecastClient instance.
    $forecastClient = new ForecastClient($httpClientMock, $this->container->get('logger.factory'), $this->container->get('cache.default'));

    // URL for the API call.
    $apiUrl = 'http://example.com/api';

    // First call - should fetch data from the API.
    $initialData = $forecastClient->getForecastData($apiUrl, TRUE);
    $this->assertNotEmpty($initialData, 'Initial API call should return data.');

    // Second call - should retrieve data from the cache.
    $cachedData = $forecastClient->getForecastData($apiUrl);
    $this->assertEquals($initialData, $cachedData, 'Data should be retrieved from the cache on subsequent calls.');

    // Re-create the ForecastClient instance, and the httpClient mock so that we
    // can make a 3rd call with the cache reset flag set to TRUE, which should
    // trigger calling the get method again.
    $httpClientMock = $this->createMock(Client::class);
    $httpClientMock
      ->expects($this->once())
      ->method('get')
      ->willReturn(new Response(200, [], $testData));
    $forecastClient = new ForecastClient($httpClientMock, $this->container->get('logger.factory'), $this->container->get('cache.default'));
    // First one should get cached data, and not make a 'get' call.
    $forecastClient->getForecastData($apiUrl);
    // Second one should bypass the cache and make a 'get' call.
    $forecastClient->getForecastData($apiUrl, TRUE);
  }

}
```

This test verifies that the `ForecastClient` correctly caches API responses. By mocking the HTTP client service we can simulate an API response, and we can track how many times the API data was requested.

Important things to note in this code:

- Extending `KernelTestBase` provides a minimal Drupal environment, including a functional database and the service container.
- Kernel tests run in the context of a Drupal install, but without a web browser. To keep the test performant, every test needs to specify which parts of Drupal need to be enabled. The line `protected static $modules` specifies which Drupal modules are required for the test.
- Mocking the `Client` simulates API calls, allowing us to control responses without external dependencies.
- The test verifies caching by ensuring the mocked API call is made only once, despite multiple calls to `getForecastData()`.

### Verify it works

Run the new tests to confirm they work:

```
./vendor/bin/phpunit -c web/core/ web/modules/custom/anytown/tests/src/Kernel/ForecastClientCacheTest.php
```

## Testing custom username validation

Kernel tests can validate integration with Drupal's Entity API, such as applying custom validation constraints to prevent creating user entities with specific usernames.

### Add a new kernel test class

Create *tests/src/Kernel/UsernameConstraintTest.php* in the *anytown* module.

### Write the tests

Add this code to *tests/src/Kernel/UsernameConstraintTest.php*:

```
<?php

namespace Drupal\Tests\anytown\Kernel;

use Drupal\KernelTests\KernelTestBase;
use Drupal\user\Entity\User;

/**
 * Tests the username validation constraint.
 *
 * @group anytown
 * @coversClass \Drupal\anytown\Plugin\Validation\Constraint\UserNameConstraint
 * @coversClass \Drupal\anytown\Plugin\Validation\Constraint\UserNameConstraintValidator
 */
class UsernameConstraintTest extends KernelTestBase {

  /**
   * Modules to enable.
   *
   * @var array
   */
  protected static $modules = ['user', 'anytown'];

  /**
   * {@inheritdoc}
   */
  protected function setUp(): void {
    parent::setUp();

    // Install required schemas for the User module. This will create the
    // database tables required when creating a new user entity.
    $this->installEntitySchema('user');

    // You can also install configuration if necessary.
    // $this->installConfig(['user']);.
  }

  /**
   * Tests the username validation constraint.
   */
  public function testUsernameValidation() {
    // Create a user entity.
    $user = User::create();

    // Set the username to the restricted value.
    $user->setUsername('anytown');

    // Validate the user entity.
    $violations = $user->validate();

    // Check that there is a violation for the username field.
    $this->assertCount(1, $violations->getByField('name'));
    $this->assertEquals('Invalid user name. Cannot use "anytown" as the user name.', $violations->getByField('name')[0]->getMessage());
  }

}
```

This test verifies that the code in `UserNameConstraintValidator` and `UserNameConstraint` which where added in [Add Custom Validation to User Entities](https://drupalize.me/tutorial/add-custom-validation-user-entities) correctly reject the username `anytown` when creating a new user entity.

Important things to note in this code:

- The `setUp()` method prepares the testing environment. To keep the test-run fast, only modules specified by `$modules` are installed. All the services provided by the listed modules are available, but none of their database tables, or default configuration. Those have to be manually installed if we need them. To create user entities, we need to set up the necessary database tables.
- Entity API interactions, like creating and validating user entities, are fully supported.
- It validates custom constraints applied to entities, ensuring module logic extends core behavior correctly.

### Verify it works

Run the new tests to confirm they work:

```
./vendor/bin/phpunit -c web/core/ web/modules/custom/anytown/tests/src/Kernel/UsernameConstraintTest.php
```

## Recap

Kernel tests in Drupal provide a powerful way to do integration testing without the overhead of a full Drupal web environment. We showed how we could test integration with specific parts of Drupal's API, without fully bootstrapping Drupal. We tested caching logic and our entity validation constraint with the username field.

## Further your understanding

- Identify additional scenarios where testing code integration with Drupal APIs is advantageous.
- Consider writing a kernel test for the `HelloWorldBlock` block plugin to verify it includes the current user's name.

## Additional resources

- [Setup tasks in Kernel tests](https://www.drupal.org/docs/automated-testing/phpunit-in-drupal/setup-tasks-in-kernel-tests) (Drupal.org)
- [testing\_example | Examples for Developers project](https://git.drupalcode.org/project/examples/-/tree/4.0.x/modules/testing_example?ref_type=heads) (git.drupalcode.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Write a Unit Test](/tutorial/write-unit-test?p=3245)

Next
[Write a Functional Test](/tutorial/write-functional-test?p=3245)

Clear History

Ask Drupalize.Me AI

close