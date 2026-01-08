---
title: "Run Functional JavaScript Testsfree"
url: "https://drupalize.me/tutorial/run-functional-javascript-tests?p=3263"
guide: "[[test-drupal-sites-automated-tests]]"
---

# Run Functional JavaScript Testsfree

## Content

In order to run functional tests that require JavaScript be executed for the feature to work, the tests need to be run in a browser that supports JavaScript. This is accomplished by using the WebDriver API in combination with an application like [ChromeDriver](https://chromedriver.chromium.org/) or [Selenium](https://www.selenium.dev/), which can remotely control a browser.

The exact setup for running functional tests is dependent on your development environment. We'll walk through a couple of common examples including using Docker (via DDEV) and stand-alone applications.

In this tutorial we'll:

- Learn how to install and run ChromeDriver and other necessary tools either in a Docker environment, or locally.
- Configure the relevant PHPUnit environment variables so they contain values appropriate for our specific environment.
- Execute Drupal's functional JavaScript tests via the `phpunit` command.

By the end of this tutorial you should be able to install the applications required to run functional JavaScript tests in a browser, and know how to configure PHPUnit to make use of them.

## Goal

Run Drupal's functional JavaScript tests with WebDriver.

## Prerequisites

- [A Drupal development site](https://drupalize.me/tutorial/install-drupal-locally-ddev)
- Command-line/terminal access to the development site
- The site needs to have the development dependencies installed. See [Install Drupal Development Requirements with Composer](https://drupalize.me/tutorial/install-drupal-development-requirements-composer).
- [Introduction to Testing in Drupal](https://drupalize.me/tutorial/introduction-testing-drupal)
- [Software Testing Overview](https://drupalize.me/tutorial/software-testing-overview)
- [Frameworks for Testing in Drupal](https://drupalize.me/tutorial/frameworks-testing-drupal)
- MacOS: Homebrew
- Linux/Windows: npm

Note: The best place to run tests is on a development site. Generally speaking, it's a bad idea to run tests on a production site.

## Set up dev environment to run functional JavaScript tests

Drupal provides a way to run JavaScript from within the test environment. Tests which use this framework are called *functional JavaScript tests*. You can learn more about this framework in [Frameworks for Testing in Drupal](https://drupalize.me/tutorial/frameworks-testing-drupal).

To run a functional JavaScript test using WebDriver you need to:

- Have a web server and database that can run Drupal. Generally whatever you use for development should work fine. We've found using PHP's built-in server and sqlLite easy to set up.
- Install ChromeDriver, Selenium, or another WebDriver API-compatible application for driving a browser.
- Configure PHP unit to use the correct web host, and connect it with your WebDriver tool of choice.

WebDriver is a W3C API that allows processes, like ChromeDriver, or Selenium, to control browsers like Firefox and Chrome. We've found the easiest way is to use ChromeDriver. Though Selenium works as well and will allow you to drive browsers other than Chrome.

We're going to walk through 2 different setups below:

- Using the Docker environment, [DDEV](https://ddev.readthedocs.io/en/stable/users/install/ddev-installation/)
- Running everything on your local machine

## Run functional JavaScript tests in DDEV

While you can set up any environment to run tests (and we outline how below) we're fans of DDEV for local development. As a Docker-based development environment, we can add a container with the required tools already installed and use that.

We'll be using the [ddev/ddev-selenium-standalone-chrome](https://github.com/ddev/ddev-selenium-standalone-chrome) DDEV service for running standalone Chrome. It can be used with any project type (not just a Drupal project).

### Install the DDEV service

```
ddev get ddev/ddev-selenium-standalone-chrome
```

For more information, [consult the *ddev/ddev-selenium-standalone-chrome* project README](https://github.com/ddev/ddev-selenium-standalone-chrome).

### Restart DDEV

```
ddev restart
```

### Ensure you have `drupal/core-dev` installed

See [Install Drupal Development Requirements with Composer](https://drupalize.me/tutorial/install-drupal-development-requirements-composer) for instructions.

### Run a Drupal core FunctionalJavaScript test

To see this in action, run the following command from the root of your project

```
ddev exec -d /var/www/html/web "../vendor/bin/phpunit -v -c ./core/phpunit.xml.dist ./core/modules/system/tests/src/FunctionalJavascript/FrameworkTest.php"
```

### Watch tests run in real time

1. Run `ddev describe` and note the `selenium-chrome` URL. It should start with `https://`, then your DDEV site name, and end with `:7900`, which is the port to access noVNC, for example `https://drupal.ddev.site:7900`. (The noVNC service allows you to view what's happening in this container.)
2. Copy the `selenium-chrome` URL and open it into your browser. (Don't forget the port.)
3. Enter the password `secret`.
4. Edit the file *.ddev/config.selenium-standalone-chrome.yaml* and on the line that sets the arguments for `MINK_DRIVER_ARGS_WEBDRIVER`, delete `\"--headless\",`. This will launch the browser when the tests are run instead of keeping it in the background.
5. Run `ddev restart`.
6. Arrange your workspace, so you can see both your browser and Terminal. Run a FunctionalJavascript test again (see previous step) and watch it run in the browser.

## Run functional tests in other Docker-based environments

A similar approach should work with any other Docker environment, the important steps are:

- Use a Docker image like `seleniarm/standalone-chromium` or `drupalci/chromedriver:production` with a WebDriver compatible browser.
- Ensure the Docker container is accessible from the container that hosts your Drupal application.
- [Configure PHPUnit](https://drupalize.me/tutorial/create-phpunit-config-file-your-project) with the appropriate `SIMPLETEST_DB`, `SIMPLETEST_BASE_URL`, and `MINK_DRIVER_ARGS_WEBDRIVER` settings for your specific environment.

## Install ChromeDriver on your host machine

You can also install and execute ChromeDriver on your host machine instead of in a container. You might find it easier to configure it more quickly via the *phpunit.xml* than via a container's YAML file, which often do override those environment variables.

### Install ChromeDriver

Download and install the version of ChromeDriver that matches the version of the Chrome browser you have installed: <https://chromedriver.chromium.org/downloads>

Or, install it via the command line.

#### MacOS

```
brew install selenium-server-standalone
brew install chromedriver
```

Note: for macOS Catalina and later you may see a message about chromedriver being from an untrusted developer when you first try and launch it. [Learn how to bypass this warning here](https://stackoverflow.com/questions/60362018/macos-catalinav-10-15-3-error-chromedriver-cannot-be-opened-because-the-de/64019725).

#### Linux or Windows

```
npm install chromedriver -g
```

### (optional) Install Selenium

If you want to be able to drive other browsers for testing, like Firefox. You can use Selenium with the WebDriver API.

#### MacOS

```
brew install selenium-server-standalone
```

#### Linux or Windows

```
npm install selenium-standalone@latest -g
selenium-standalone install
```

### Start ChromeDriver / Selenium

In a new terminal window (you need to keep it running in the background) start ChromeDriver:

```
chromedriver
```

Note: the default ChromeDriver port is 9515.

Or Selenium:

```
selenium-server -port 4444
```

### Start your webserver

Next, you'll need to start your webserver. If you're using something like MAMP, go ahead and start it if it's not already running.

Or, use [PHP's built-in webserver](https://www.php.net/manual/en/features.commandline.webserver.php) and sqlLite.

In a new terminal window run the following command from the root of your Drupal codebase:

```
php -S 127.0.0.1:8000 .ht.router.php
# Related base url:
# http://127.0.0.1:8000
# Related database connection string:
# sqlite://localhost/sites/default/files/.ht.sqlite
```

The important thing here is that you have the server running, and you know the URL that someone would use to access the site, and the database connection string.

### Set up testing environment variables

If you haven't already, copy *core/phpunit.xml.dist* to *core/phpunit.xml*.

```
cp core/phpunit.xml.dist core/phpunit.xml
```

Edit *core/phpunit.xml* and adjust the following lines, replacing `http://localhost:8000` in the `SIMPLETEST_BASE_URL` value with your local environment's URL. And the `SIMPLETEST_DB` value with your database credentials. Your local setup might be different than the example below. See also [Create a PHPUnit Config File for Your Project](https://drupalize.me/tutorial/create-phpunit-config-file-your-project).

```
<env name="SIMPLETEST_BASE_URL" value="http://localhost:8000"></env>
<env name="SIMPLETEST_DB" value="sqlite://localhost/sites/default/files/.ht.sqlite"></env>
```

For ChromeDriver (add/remove `--headless` depending on if you want the Chrome browser to open so you can see it):

```
<env name="MINK_DRIVER_ARGS_WEBDRIVER" value='["chrome", {"browserName":"chrome","chromeOptions":{"args":["--disable-gpu", "--no-sandbox", "--headless"]}}, "http://127.0.0.1:9515"]'/>
```

For Selenium:

```
<env name="MINK_DRIVER_ARGS_WEBDRIVER" value='["chrome", null, "http://localhost:4444/wd/hub"]'/>
```

### Execute a test with PHPUnit

Run the following command to execute the `JSWebAssertTest` functional JavaScript tests:

```
../vendor/bin/phpunit -v -c ./core core/tests/Drupal/FunctionalJavascriptTests/Tests/JSWebAssertTest.php
```

Expected result:

```
PHPUnit 9.5.28 by Sebastian Bergmann and contributors.

Runtime:       PHP 8.1.13
Configuration: ./core/phpunit.xml.dist

Testing Drupal\FunctionalJavascriptTests\Tests\JSWebAssertTest
.                                                                   1 / 1 (100%)

Time: 00:10.633, Memory: 4.00 MB

OK (1 test, 24 assertions)

HTML output was generated
https://functional-js-testing.ddev.site/sites/simpletest/browser_output/Drupal_FunctionalJavascriptTests_Tests_JSWebAssertTest-1-81901143.html
https://functional-js-testing.ddev.site/sites/simpletest/browser_output/Drupal_FunctionalJavascriptTests_Tests_JSWebAssertTest-2-81901143.html
```

You should also see Chrome browser open, perform the tests, and close again.

### Stop ChromeDriver / Selenium server

When you're done running tests you can stop the `chromedriver` or `selenium-server` process.

## Recap

In this tutorial, we learned how to set up our local development environment to run functional JavaScript tests using WebDriver API and Chromedriver or Selenium. We walked through 2 different setups: one using DDEV and a DDEV service which installs a standalone Chromedriver container that we can access and use with a local DDEV site. And, a second setup where we installed Chromedriver or Selenium locally on our machine.

## Further your understanding

- What types of behavior on your site might be worth writing functional JavaScript tests for?
- Learn about other Drupal testing frameworks: [Frameworks for Testing in Drupal](https://drupalize.me/tutorial/frameworks-testing-drupal) (Drupalize.Me).
- Read [*core/tests/README.md*](https://git.drupalcode.org/project/drupal/-/blob/10.1.x/core/tests/README.md) for additional/alternative methods and hints, including running legacy tests with PhantomJS.

## Additional resources

- [ChromeDriver](https://chromedriver.chromium.org/) (chromedriver.chromium.org)
- [Selenium](https://www.selenium.dev/) (selenium.dev)
- [MDN web docs: WebDriver](https://developer.mozilla.org/en-US/docs/Web/WebDriver) (developer.mozilla.org)
- [Running Drupal's FunctionalJavascript tests on DDEV](https://glamanate.com/blog/running-drupals-functionaljavascript-tests-ddev) (glamanate.com)
- [Debug any of Drupal's PHPUnit tests in PhpStorm with a DDEV Environment](https://drupalize.me/blog/debug-any-drupals-phpunit-tests-phpstorm-ddev-environment) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Set Up a Functional Test](/tutorial/set-functional-test?p=3263)

Next
[Functional JavaScript Testing with Nightwatch.js](/tutorial/functional-javascript-testing-nightwatchjs?p=3263)

Clear History

Ask Drupalize.Me AI

close