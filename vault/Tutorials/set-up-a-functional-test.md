---
title: "Set Up a Functional Test"
url: "https://drupalize.me/tutorial/set-functional-test?p=3263"
guide: "[[test-drupal-sites-automated-tests]]"
order: 8
---

# Set Up a Functional Test

## Content

In this tutorial, we'll walk through the process of setting up a functional test. Then, we'll learn how to run it using two different test runners. This setup process allows us to be sure we're not getting false positives from the test runners. We'll be working on a functional test, but these techniques apply with minimum modification to all the Drupal PHPUnit-based tests.

By the end of this tutorial, you should be able to set up and run functional tests in Drupal using two different test runners.

## Goal

Set up and run functional tests using *phpunit*.

## Prerequisites

- [Introduction to Testing in Drupal](https://drupalize.me/tutorial/introduction-testing-drupal)
- [Software Testing Overview](https://drupalize.me/tutorial/software-testing-overview)
- A [local Drupal development site](https://drupalize.me/tutorial/install-drupal-locally-ddev). This should *not* be a production site.
- [Install Drupal Development Requirements with Composer](https://drupalize.me/tutorial/install-drupal-development-requirements-composer)
- Access to the command line and your site's file system.

Sprout Video

## Test setup

In this tutorial we're going to be writing a functional test. The Drupal test runners organize all the different types of tests into different directories (and thus namespaces) within *tests/src/*.

So for a functional test, like we're writing, we'd add a directory called *tests/src/Functional*. If there is not already a directory called `Functional` in *tests/src/* then create it.

For more information about the organization of test types see [Organize Test Files](https://drupalize.me/tutorial/organize-test-files).

First, we're going to set up a bare-bones test to run, and make sure it's in the right place.

### Locate your module

As a starting point, we're using the skeleton test from the Examples for Developers project's *testing\_example* module. For this tutorial, we'll create a demo module and place it in *modules/custom/my\_testing\_module*.

Open this module (or your own) in an IDE or editor.

### Check for a *tests/src/* directory

In the module directory, there might already be a *tests/src/* directory. If not, we need to add it.

All PHPUnit-based Drupal tests should live in the *tests/src/* directory. This is so the test classes won't be autoloaded during normal non-test requests.

### Add a file for the test class

Our test class is going to be called `SkeletonTest`.

The class name must end in `Test` in order for the test runner to find it. It also has to be a PHP file, with a *.php* file extension.

So inside the *tests/src/Functional/* directory, add a file called *SkeletonTest.php*.

#### Assumed project structure

Here's the project structure we're assuming for this tutorial. You will need to adjust code examples and commands if you are using a different structure or custom module name.

```
# PROJECT ROOT
├── composer.json
├── composer.lock
├── vendor
│   ├── bin
│       ├── phpunit
└── web
    # DRUPAL ROOT
│   ├── core
│       ├── phpunit.xml.dist
│   ├── index.php
│   ├── modules
│   └── custom
│       └── my_testing_module
│           ├── my_testing_module.info.yml
│           └── tests
│               └── src
│                   └── Functional
│                       └── SkeletonTest.php
```

### Add some code scaffolding

Let's start adding some code scaffolding.

The test runners need the following things:

- The `<?php` tag
- A namespace declaration
- A `use` statement for our testing framework
- A `@group` annotation.
- A class declaration

We'll leave the namespace aside until the next step but let's add everything else to our file.

We're writing a functional test, which in Drupal means we're going to subclass `Drupal\Tests\BrowserTestBase`.

The `@group` annotation is required by the test runners. They will abort if the test does not have at least one. You can add as many groups as you'd like. The test runners allow you to specify a group when you run them, which is an easy way to filter for only the tests you want to run.

You should at least include the module name as a `@group` annotation.

```
<?php

// @TODO Add namespace

use Drupal\Tests\BrowserTestBase;

/**
 * Skeleton functional test.
 *
 * @group demo
 * @group skeleton
 */
class SkeletonTest extends BrowserTestBase {

}
```

### Add a namespace

Namespaces often require further explanation, so we're adding it in a separate step.

The test runners will find your test based on 2 things:

1. The test file's **location** in the file system
2. The **namespace** specified in the test file

We've already placed the file where it belongs within the module, in *tests/src/Functional/SkeletonTest.php*.

PHPUnit-based Drupal tests need to be in the proper namespace, so let's do that now.

For modules, test file namespaces follow this pattern:

```
Drupal\Tests\[module name]\[test type]
```

The test type value could be one of:

- `Functional`
- `FunctionalJavascript`
- `Kernel`
- `Unit`.

Since we're writing a functional test, let's declare the following namespace in our test file:

```
Drupal\Tests\testing_example\Functional
```

After adding it to our test file, our code should look something like this:

```
<?php

namespace Drupal\Tests\my_testing_module\Functional;

use Drupal\Tests\BrowserTestBase;

/**
 * Skeleton functional test.
 *
 * @group demo
 * @group skeleton
 */
class SkeletonTest extends BrowserTestBase {

}
```

### Declare a default theme property (`$defaultTheme`)

When functional tests are run a new instance of Drupal is installed by the test runner, and all the tests are run against the new site. By default, the *testing* profile is used to install Drupal. The profile doesn't install any theme. We need to specify which theme to install via the `$defaultTheme` property. (See also this change record: [The 'testing' install profile's setting of a default theme (Classy) is now deprecated](https://www.drupal.org/node/3083055).)

Our recommendation: If your tests don't rely on any specific markup, which is usually the best practice, set the `$defaultTheme` to `'stark'`. Otherwise, if your tests rely on core-provided markup use `'stable9'`. If you're testing site-specific features install the theme you use for your site.

```
<?php

namespace Drupal\Tests\testing_example\Functional;

use Drupal\Tests\BrowserTestBase;

/**
 * Skeleton functional test.
 *
 * @group demo
 * @group skeleton
 */
class SkeletonTest extends BrowserTestBase {
  /**
   * {@inheritdoc}
   */
  protected $defaultTheme = 'stark';

}
```

### Add a failing test

Let's add a failing test method. Why?

When we run the tests and there's a failure, we'll know that the test runner found our test.

This illustrates an important point about testing: You learn things when there's a test failure, so make sure your tests will fail for the best reasons.

Test methods always start with `test`, such as `testThatAThingHappens()`. If you have a method on your test class that isn't supposed to run as a test, make sure its name does not start with `test`.

*Note*: In the sample code in *testing\_example* (Examples for Developers project), this method does not fail. You'll need to modify it to fail. Follow the instructions there.

So here's our demo class with failing test method added:

```
<?php

namespace Drupal\Tests\testing_example\Functional;

use Drupal\Tests\BrowserTestBase;

/**
 * Skeleton functional test.
 *
 * @group demo
 * @group skeleton
 */
class SkeletonTest extends BrowserTestBase {

  /**
   * {@inheritdoc}
   */
  protected $defaultTheme = 'stark';

  /**
   * This test method fails, so we can be sure our test is discovered.
   */
  public function testFail() {
    $this->fail('The test runner found our test and failed it. Yay!');
  }

}
```

After we've verified that the test runner can find our test, we'll update it to test what we want to test.

### Figure out your `SIMPLETEST_BASE_URL`

In order to run a functional test, PHPUnit needs to know the base URL of the site being tested.

We can modify core's PHPUnit configuration to automatically provide this information, but for now, we'll pass it in as an environmental variable. You can consult [Run Drupal Tests with PHPUnit](https://drupalize.me/tutorial/run-drupal-tests-phpunit) to learn how to set this configuration.

Drupal's functional tests need this environmental variable: `SIMPLETEST_BASE_URL`. We need to set it to the URL for the installed Drupal site, so it can perform HTTP requests.

For example, if you're using DDEV, the base URL would be: `http://localhost`

When we run the test, we'll be adding this environmental variable to the command that runs the test. For us, this will look like:

```
SIMPLETEST_BASE_URL=http://localhost
```

The method you use to set environment variables may be different depending on your local development setup.

### Run the test with PHPUnit

Now comes the moment of truth. We will use the *phpunit* tool to run our new test. Will it work? Keep in mind that we set the test to fail, so when it works, you'll see a failing test.

*Note:* If you are using an installation of Drupal that you downloaded as an archive from Drupal.org, you'll also need to [use Composer to install the dev tools](https://drupalize.me/tutorial/install-drupal-development-requirements-composer).

Let's run the test by typing the following into your command line. We're assuming that you're running these commands from the root of your project, and that the *web* directory is the Drupal root directory (where *core* lives).

```
SIMPLETEST_BASE_URL=http://localhost ./vendor/bin/phpunit -c web/core/ --testsuite functional --group skeleton
```

If all went well, you'll see something like this:

```
PHPUnit 9.6.15 by Sebastian Bergmann and contributors.

Testing 
F                                                                   1 / 1 (100%)

Time: 00:01.864, Memory: 40.00 MB

There was 1 failure:

1) Drupal\Tests\my_testing_module\Functional\SkeletonTest::testFail
The test runner found our test and failed it. Yay!

/var/www/html/web/modules/custom/my_testing_module/tests/src/Functional/SkeletonTest.php:23
/var/www/html/vendor/phpunit/phpunit/src/Framework/TestResult.php:728

FAILURES!
Tests: 1, Assertions: 2, Failures: 1.
```

Did you see an error about `SIMPLETEST_BASE_URL`? If so, then check the previous step of this tutorial and make sure you're using the correct URL to your local web server and try again.

Let's walk through what the options in this command mean. Here's the command we ran from the root of our project:

```
./vendor/bin/phpunit -c web/core/ --testsuite functional --group skeleton
```

**Note:** Each path assumes this [project structure](#project-structure). You may need to use a different path depending on your project structure and in which directory you're running the command.

- `./vendor/bin/phpunit` is how we start *phpunit*.
- `-c web/core/` tells *phpunit* to use the configuration file that's located in the *web/core/* directory. [If *phpunit.xml* is present](https://drupalize.me/tutorials/testing/), it will use that. Otherwise, it will use *phpunit.xml.dist*.
- `--testsuite functional` tells *phpunit* to only work with functional tests. Other allowed values: `functional-javascript`, `kernel`, or `unit`. We could leave this option off the command line, but it's nice to know that the test is discovered for the proper test suite and not accidentally by another one.
- `--group skeleton` gives us all the tests with `@group` annotation for that group. This proves that our group annotation works.

We could also just specify the full path to the test file on the command line like this:

```
./vendor/bin/phpunit -c web/core/ ./modules/custom/my_testing_module/tests/src/Functional/SkeletonTest.php
```

This has the advantage of not requiring *phpunit* to do any discovery, which speeds things up. For running tests during subsequent development, this is fine. But for now, we want to make sure the test suite and group options work properly.

Now you've written a test class you know the test runners can find and run.

You can substitute other types of tests in these steps. For instance, if you wanted to write a kernel test, then inherit from `Drupal\KernelTests\KernelTestBase`, place your module in `module_name/tests/src/Kernel/`, and give it a namespace of `Drupal\Tests\module_name\Kernel\MyKernelTest`. When it comes time to verify that it's discovered properly, with phpunit, specify `--testsuite kernel`.

## Recap

We learned:

- To place our Drupal tests in different directories in the module, under *tests/src/*.
- Our tests have to be *.php* files and the class name has to end with `Test`.
- Our test needs to have the `<?php` tag and `@group` annotation.
- We can specify types of tests to run on the command line, using `--testsuite` or `--types`.

## Further your understanding

- Learn how to [Implement a Functional Test](https://drupalize.me/tutorial/implement-functional-test).
- Try setting up a failing kernel or unit test and run it from the command line. Learn more about how to do this in the [Organize Test Files](https://drupalize.me/tutorial/organize-test-files) tutorial.
- Try running your test from phpunit using only the `--testsuite` and `--filter` options. Learn more about this in [Run Drupal Tests with PHPUnit](https://drupalize.me/tutorial/run-drupal-tests-phpunit).
- Learn [how to set up your local environment with selenium-server and Chromedriver](https://drupalize.me/tutorial/run-functional-javascript-tests), so you can run a functional JavaScript test.

## Additional resources

- [Organize Test Files](https://drupalize.me/tutorial/organize-test-files) (Drupalize.Me)
- [PHPUnit in Drupal](https://www.drupal.org/docs/automated-testing/phpunit-in-drupal) (Drupal.org)
- [Functional JavaScript Testing with WebDriver](https://drupalize.me/tutorial/run-functional-javascript-tests) (Drupalize.Me)
- Change record: [The 'testing' install profile's setting of a default theme (Classy) is now deprecated](https://www.drupal.org/node/3083055) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Run Drupal Tests with PHPUnit](/tutorial/run-drupal-tests-phpunit?p=3263)

Next
[Run Functional JavaScript Tests](/tutorial/run-functional-javascript-tests?p=3263)

Clear History

Ask Drupalize.Me AI

close