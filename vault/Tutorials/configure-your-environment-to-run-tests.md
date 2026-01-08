---
title: "Configure Your Environment to Run Tests"
url: "https://drupalize.me/tutorial/configure-your-environment-run-tests?p=3245"
guide: "[[drupal-module-developer-guide]]"
---

# Configure Your Environment to Run Tests

## Content

Before you can run tests, you'll need to configure your local environment. This setup involves Drupal-specific configuration for PHPUnit and ensuring your environment supports Functional JavaScript tests with a WebDriver client and a compatible browser. The setup process varies based on the development environment. In this tutorial, we're using DDEV as the local environment.

In this tutorial, we'll:

- Install all required dependencies.
- Configure PHPUnit specific to our environment.
- Validate the setup by running a Drupal core test.

By the end of this tutorial, you'll be equipped to run Drupal's PHPUnit tests locally using DDEV.

## Goal

Prepare your DDEV local environment for running Drupal's PHPUnit tests.

## Prerequisites

- [Set Up Your Development Environment](https://drupalize.me/tutorial/set-your-development-environment)
- [Concept: Testing](https://drupalize.me/tutorial/concept-testing)

## Video tutorial

Sprout Video

## Install and configure the required utilities

To run Drupal module tests, you need:

- `drupal/core-dev` installed via Composer.
- PHPUnit's configuration updated for your environment. (See *core/phpunit.xml.dist*).
- Selenium/Chromedriver and a browser setup for Functional JavaScript tests.
- To verify your setup by executing a Drupal core test.

This guide covers configuring DDEV to run automated tests for a Drupal site.

### Install `drupal/core-dev`

First, ensure `drupal/core-dev` is installed, as it includes PHPUnit and other testing dependencies. It should be installed with Composer as a development dependency (`--dev`) to prevent deploying test tools to production.

```
composer require --dev drupal/core-dev
```

### Install Selenium and Chrome via DDEV add-ons

Functional JavaScript tests require a headless browser like Chrome and a WebDriver interface such as Selenium or Chromedriver. For DDEV users, install these dependencies using the `ddev/ddev-selenium-standalone-chrome` add-on:

```
ddev get ddev/ddev-selenium-standalone-chrome
ddev restart
```

This command adds a Docker container with Selenium and Chrome to your project. Review and consider committing the added files, *./ddev/docker-compose.selenium-chrome.yaml* and *./ddev/config.selenium-standalone-chrome.yaml*, to version control.

### Configure PHPUnit

Drupal's default PHPUnit configuration is in *core/phpunit.xml.dist*, but it requires environment-specific adjustments. The `ddev/ddev-selenium-standalone-chrome` add-on provides necessary configurations, typically requiring no further changes. Review *.ddev/config.selenium-standalone-chrome.yaml* for details.

Ensure the following options are correctly set for your environment:

- `SIMPLETEST_BASE_URL`: The URL for accessing your Drupal site locally.
- `SIMPLETEST_DB`: Database connection string for your local environment.
- `BROWSERTEST_OUTPUT_DIRECTORY`: Local directory for PHPUnit to save debug output.
- `MINK_DRIVER_ARGS_WEBDRIVER`: WebDriver configuration, indicating which browser to use and connection details.

For Chromedriver usage outside DDEV, see [Functional JavaScript Testing](https://drupalize.me/tutorial/run-functional-javascript-tests).

### Run an example test

Verify your setup by running a Drupal core functional JavaScript test:

```
# Inside the DDEV web container (ddev ssh).
./vendor/bin/phpunit -c web/core/ web/core/modules/block/tests/src/FunctionalJavascript/BlockAddTest.php
```

This command:

- Runs the tests in the file *web/core/modules/block/tests/src/FunctionalJavascript/BlockAddTest.php*.
- Tells `phpunit` to use the configuration it finds in the `web/core/` directory (*core/phpunit.xml.dist* in this case). The environment variables set in *./ddev/config.selenium-standalone-chrome.yaml* override some of the values from that file.

Example successful output:

```
./vendor/bin/phpunit -c web/core/ web/core/modules/block/tests/src/FunctionalJavascript/BlockAddTest.php
PHPUnit 9.6.13 by Sebastian Bergmann and contributors.

Testing Drupal\Tests\block\FunctionalJavascript\BlockAddTest
.                                                                   1 / 1 (100%)

Time: 00:04.448, Memory: 4.00 MB

OK (1 test, 6 assertions)

HTML output was generated
https://module-developer-guide.ddev.site/sites/simpletest/browser_output/Drupal_Tests_block_FunctionalJavascript_BlockAddTest-4-97369036.html
https://module-developer-guide.ddev.site/sites/simpletest/browser_output/Drupal_Tests_block_FunctionalJavascript_BlockAddTest-5-97369036.html
https://module-developer-guide.ddev.site/sites/simpletest/browser_output/Drupal_Tests_block_FunctionalJavascript_BlockAddTest-6-97369036.html
joe@module-developer-guide-web:/var/www/html$
```

You can run all the tests in a module by specifying the path to the module instead of a specific test class.

The following example will run all tests that can be discovered in the *anytown* module:

```
 ./vendor/bin/phpunit -c web/core/ web/modules/custom/anytown
```

Learn more about running tests, and groups of tests, in [Run Drupal Tests with PHPUnit](https://drupalize.me/tutorial/run-drupal-tests-phpunit).

## Recap

This tutorial detailed setting up a DDEV-based development environment for running Drupal's functional JavaScript tests, effectively preparing you for all types of test executions. We verified our setup by running tests from the core Block module.

## Further your understanding

- Explore running other unit and kernel tests in Drupal core.
- Review `ddev/ddev-selenium-standalone-chrome` documentation for additional configurations and noVNC test execution monitoring.

## Additional resources

- [Create a PHPUnit Config File for Your Project](https://drupalize.me/tutorial/create-phpunit-config-file-your-project) (Drupalize.Me)
- [Run Drupal Tests with PHPUnit](https://drupalize.me/tutorial/run-drupal-tests-phpunit) (Drupalize.Me)
- [ddev/ddev-selenium-standalone-chrome documentation and configuration options](https://github.com/ddev/ddev-selenium-standalone-chrome) (github.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Testing](/tutorial/concept-testing?p=3245)

Next
[Write a Unit Test](/tutorial/write-unit-test?p=3245)

Clear History

Ask Drupalize.Me AI

close