---
title: "Frameworks for Testing in Drupal"
url: "https://drupalize.me/tutorial/frameworks-testing-drupal?p=3262"
guide: "[[test-drupal-sites-automated-tests]]"
---

# Frameworks for Testing in Drupal

## Content

In this tutorial, we will look at the various types of tests and testing frameworks included in Drupal core. We'll also provide an overview of how the different frameworks operate and the types of situations where each of the different frameworks is useful.

## Goal

- Know about the kinds of tests and testing frameworks included with the core Drupal software.

## Prerequisites

- None.

## Drupal's testing frameworks

Drupal has 4 different types of testing frameworks. There is some overlap in functionality between the different frameworks.

| Test Framework | phpunit --testsuite |
| --- | --- |
| `UnitTestCase` | `unit` |
| `KernelTestBase` | `kernel` |
| `BrowserTestBase` | `functional` |
| `JavascriptTestBase` | `functional-javascript` |

## Which testing framework should I use?

When trying to decide which testing framework you need to work with, there are 2 main factors to consider:

1. What are you testing and *why*? This is by far the most important reason to choose one framework over another. If a framework gives you the tools to test the thing you're testing, then that's probably the one to use.
2. The second consideration is more of a rule of thumb. One of the major pain points with having a comprehensive test suite is that they often take a long time to run. In general, you want to consume as few system resources as possible per test in order to make the overall test suite as fast as possible. With that guideline in mind, we should choose our framework based on our needs.

Image

![Graph of how to choose a Drupal testing framework.](/sites/default/files/styles/max_800w/public/tutorials/images/frameworks-which.png?itok=woBZlCYU)

- Can you test the behavior in a unit test without stubbing or mocking a lot of core functions or global constants? If yes, you want to write a *unit test*.
- If you need to stub or mock a large amount of core behavior, can you test the behavior without performing HTTP requests? If so, then you want to write a *kernel test*.
- If you need to stub and mock core behavior *and* you need to perform HTTP requests, then write a *functional test*.
- If you're testing AJAX-type behavior within the browser, then write a *functional JavaScript test*.

## Unit tests

Drupal unit tests (i.e. `PHPUnit-Unit` or `unit`) inherit from the `\Drupal\Tests\UnitTestCase` class.

`UnitTestCase` gives you some convenient mocking methods and manages some presumed dependencies, such as resetting the container in `\Drupal` for each test method.

Write a unit test when you know you'll be handling *all* of the dependencies. Unit tests are great for testing some very fine-grained behavior with few or no dependencies. If you don't need any of the behavior and convenience methods from the kernel test framework, write a unit test. Since unit tests don't have to set anything up, they run very quickly.

Generally speaking, however, if you're writing a unit test and you find that the code you're testing references global constants and functions, you should convert to a kernel test. You can also work around these kinds of test dependencies with some of the advice in this documentation: [Unit testing more complicated Drupal classes](https://www.drupal.org/docs/automated-testing/phpunit-in-drupal/unit-testing-more-complicated-drupal-classes).

Drupal unit tests do not run in separate processes, by default. As with any PHPUnit test, you can have them run in a separate process by [annotating](https://drupalize.me/tutorial/annotations) the class with `@runTestsInSeparateProcesses` or annotating the method with `@runTestInSeparateProcess`. You'd do this if you are loading include files or defining constants; because, once they're loaded, they can't be unloaded.

A good example of a strict unit test in core would be [Drupal\Tests\Component\Utility\UnicodeTest](https://git.drupalcode.org/project/drupal/-/blob/10.1.x/core/tests/Drupal/Tests/Component/Utility/UnicodeTest.php). If you browse through you'll see that it uses the `@dataProvider` annotation to provide consistent tests against diverse data sets. It also uses the `@coversDefaultClass` and `@covers` annotations to specify at a very fine level what is being tested.

## Kernel tests in Drupal

Kernel tests (i.e. `PHPUnit-Kernel` or `kernel`) inherit from the `KernelTestBase` class.

Kernel tests should be used when we have some dependencies we can't or shouldn't mock, and which don't require performing HTTP requests.

`KernelTestBase` makes Drupal services and hooks available, but doesn't provide an installed site. You can provide a list of modules to enable, but they are not actually installed. Only their services and hooks are made available.

Kernel tests bootstrap a site to a state similar to the site's state in the early phases of the installation process.

This means that if you want complex dependencies, your test has to manage them. For instance, if you needed to create a specific type of entity for a kernel test, you'd have to:

- Tell the test to enable the module which defines that entity.
- Install the module's default configuration.
- Install the module's schema.
- Create the entity using Entity API.

In many cases, kernel tests that need to set up users, nodes, or other common data types can use traits to simplify the process. For instance, if you find that you need to generate users, you can use `Drupal\Tests\user\Traits\UserCreationTrait;`.

Kernel tests depend on a virtual file system, stored in memory, provided by the *vfsStream* package. They, too, run in a separate process in order to provide isolation between test methods.

Here is an example implementation of a kernel test. In it, we'll replace a service with a mocked one, so that we can test the behavior of another service that uses it:

```
  /**
   * Overrides KernelTestBase::register().
   */
  public function register(ContainerBuilder $container) {
    $mock_service = $this->prophesize(ServiceInterface::class);
    $mock_service->performService()->willReturn('some_value');
    $container->set('secondary_service', $mock_service->reveal());
  }

  public function testServiceConsumer() {
    $service = $this->container->get('primary_service');
    $this->assertSame('service_value', $service->methodThatUsesSecondaryService());
  }
```

An example of a kernel test in core would be [Drupal\Tests\block\Kernel\BlockStorageUnitTest](https://git.drupalcode.org/project/drupal/-/blob/10.1.x/core/modules/block/tests/src/Kernel/BlockStorageUnitTest.php). It requires that modules and services be available, but never makes HTTP requests. It installs different themes and manages configuration from fixture modules.

## Functional tests in Drupal

Functional tests inherit from the `BrowserTestBase` class.

Functional tests use the Mink framework to provide a virtual HTTP client. The client can perform HTTP requests against an installed Drupal site.

`BrowserTestBase` sets up a fixture Drupal site for each test method. This fixture site is managed through Drupal's multi-site feature.

The main use case for `BrowserTestBase` is integration testing, with a lot of dependencies managed by the framework.

Here's an example of using `BrowserTestBase` to test whether an admin user can see admin pages. This example shows that our test has a wide variety of core functionality available. At a very high level of abstraction, we're creating and then logging in to a user account, then visiting a page by its path.

```
  public function testAdminUser() {
    $this->drupalLogin(
      $this->drupalCreateUser(['access administration pages'])
    );
    $this->drupalGet('admin/config');
    $session = $this->assertSession();
    $session->statusCodeEquals(200);
  }
```

We can use `BrowserTestBase` for behavioral-style tests, but this is less than ideal since it relies heavily on configuration provided within the test code itself. Using a different tool like Behat might be a better fit for tests that require complex interaction behavior.

## Functional JavaScript tests in Drupal

Functional JavaScript tests inherit from `WebDriverTestBase`, which itself inherits from `BrowserTestBase`.

`WebDriverTestBase` adds the ability to perform AJAX-type requests and then assert against the result of the changed DOM.

In order to do this, `WebDriverTestBase` requires that you have selenium-server (which uses the WebDriver API) and a browser extension such as ChromeDriver installed and running on your test machine. The tutorial, [Functional JavaScript Testing with WebDriver](https://drupalize.me/tutorial/run-functional-javascript-tests), will help you with this task.

A good example of a functional JavaScript test from Drupal core can be found in the `EntityReference` module. In particular let's take a look at the code in [Drupal\FunctionalJavascriptTests\EntityReference\EntityReferenceAutocompleteWidgetTest](https://git.drupalcode.org/project/drupal/-/blob/10.1.x/core/tests/Drupal/FunctionalJavascriptTests/EntityReference/EntityReferenceAutocompleteWidgetTest.php). It uses `$this->getSession()->getDriver()->keyDown()` and `$this->assertSession->waitOnAutocomplete()` to simulate typing into an entity reference field and then it tests the result to see if autocomplete works.

```
$autocomplete_field = $assert_session->waitForElement('css', '[name="' . $field_name . '[0][target_id]"].ui-autocomplete-input');
$autocomplete_field->setValue('Test');
$this->getSession()->getDriver()->keyDown($autocomplete_field->getXpath(), ' ');
$assert_session->waitOnAutocomplete();
```

Both functional and functional JavaScript tests always run in a separate process, in order to provide isolation between test methods. The high level of abstraction available to these types of tests, and their dependency on a fixture site mean that they will also be quite resource intensive (and slow).

`WebDriverTestBase` was introduced in Drupal 8.6 as a replacement for `JavascriptTestBase` which was deprecated and is now removed from core. To refactor your tests, use `\Drupal\FunctionalJavascriptTests\WebDriverTestBase` instead of `JavascriptTestBase`. See the change record [JavascriptTestBase is deprecated in favor of WebDriverTestBase](https://www.drupal.org/node/2945059) for more details.

### Nightwatch.js functional JavaScript testing

You should also know about a non-PHP tool for functional JavaScript testing called Nightwatch.js. Nightwatch.js allows you to write tests in JavaScript and run commands in a web browser. This browser automation allows you to test the types of interactions that a typical user of your website might encounter. It also allows you to test JavaScript code using JavaScript, and execute tests in different browsers.

See the tutorial [Functional JavaScript Testing with Nightwatch.js](https://drupalize.me/tutorial/functional-javascript-testing-nightwatchjs) for instructions.

## Commonalities between testing frameworks

Unit, kernel, functional, and functional JavaScript testing frameworks (except for Nightwatch.js) inherit from PHPUnit, which means that they may use any feature of PHPUnit 8.4.

Some of these features include:

### Data providers

*[Data providers](https://phpunit.readthedocs.io/en/9.5/writing-tests-for-phpunit.html?highlight=data%20providers#data-providers)* are test methods annotated with `@dataProvider` and can accept input data.

This is great for tests where you want to be able to add data sets later. That's why we linked to the [Drupal\Tests\Component\Utility\UnicodeTest](https://git.drupalcode.org/project/drupal/-/blob/10.1.x/core/tests/Drupal/Tests/Component/Utility/UnicodeTest.php) example above. As the unicode system evolves and is maintained, it's relatively easy to add more diverse test cases.

Here's an example which will test our expectations about how other types are converted to bools:

```
class BoolTest extends UnitTestCase {

  public function boolDataProvider() {
    return [
      [FALSE, NULL],
      [FALSE, 0],
      [FALSE, ''],
      [TRUE, 1],
    ];
  }

  /**
   * @dataProvider boolDataProvider
   *
   * PHPUnit will re-run this method for each data set in the dataProvider
   * method. The data set is an array that is mapped to the method arguments
   * here.
   */
  public function testBoolTypeCast($expected, $value) {
    $this->assertSame($expected, (bool) $value);
  }

}
```

### Mocking

*[Mocking or the use of test doubles](https://phpunit.readthedocs.io/en/9.5/test-doubles.html?highlight=mocking#test-doubles)* in PHPUnit gives us a native mock system and co-exists with the [prophecy](https://github.com/phpspec/prophecy) mock system. This allows us to make objects that have an expected behavior to feed into the system under test. (See note below about Prophecy.)

Here's an example of using PHPUnit's mocking system to mock an object so that one of its utility methods return a known value. Note that we're not testing `utilityMethod()`, but we need it to return a value, so we can test `methodWeAreTesting()`.

```
public function testMockingExample() {
  // Create a mock object for the class we are testing.
  $mock_item = $this->getMockBuilder(ClassWeAreTesting::class)
    ->setMethods(['utilityMethod'])
    ->getMock();

  // Configure the mock object to return a specific value when utilityMethod is called.
  $mock_item->expects($this->once())
    ->method('utilityMethod')
    ->willReturn(['known', 'data']);

  // Test that methodWeAreTesting returns the expected mock value.
  $this->assertSame('what_we_expect', $mock_item->methodWeAreTesting());
}
```

**Note:** If your site contains a dependency on `drupal/core-dev` and you see errors similar to this when running core tests:

`PHP Fatal error: Trait 'Prophecy\PhpUnit\ProphecyTrait' not found in core/tests/Drupal/TestTools/PhpUnitCompatibility/PhpUnit9/TestCompatibilityTrait.php on line 12`

Then you need to add an extra dependency.

`composer require --dev phpspec/prophecy-phpunit:^2`

(If you installed Drupal with `drupal/core-recommended`, be sure to run the command above within your project root instead of the core directory.)

This is because PHPUnit 8 includes Prophecy integration, but PHPUnit 9 does not.

- Change record: [Updated to PHPUnit 9](https://www.drupal.org/node/3176567)

### Code coverage

*[Code coverage analysis](https://phpunit.readthedocs.io/en/9.5/code-coverage-analysis.html?highlight=code%20coverage#code-coverage-analysis)* in PHPUnit when used with XDebug can generate a coverage report. This lets us see exactly which lines of code were touched by a given test and gives us fine-grained information about complexity and estimated maintainability.

## Recap

- Drupal has the following testing frameworks built in to core: unit, kernel, functional, and functional JavaScript.
- The type of test you choose to write depends on what you're trying to test and why you're testing it, so it's important to understand the purpose, features, and scope of each type of testing framework.
- Use file organization conventions appropriate for your testing framework so that Drupal can find your tests.
- In general, it's a good idea to try to use as few system resources as possible to test. For instance, if you can write a kernel test instead of a functional test you should try to. This will also help your test suite run faster.
- All of the PHP-based core test frameworks can use PHPUnit's mocking, data provider, and code coverage features.

## Further your understanding

- What other traits can you locate in Drupal core that would make writing kernel tests a bit easier?
- Learn how to organize your test files in the tutorial [Organize Test Files](https://drupalize.me/tutorial/organize-test-files)
- Upgrading your site and need to convert your Simpletests? See [Convert Tests from Simpletest to PHPUnit](https://drupalize.me/tutorial/convert-tests-simpletest-phpunit).

## Additional resources

- [PHPUnit in Drupal](https://www.drupal.org/docs/automated-testing/phpunit-in-drupal) (Drupal.org)
- [Examples for Developers testing\_example module](https://git.drupalcode.org/project/examples/-/tree/3.x/modules/testing_example) has examples of tests in all the frameworks. (Drupal.org)
- [Data providers](https://phpunit.readthedocs.io/en/9.5/writing-tests-for-phpunit.html?highlight=data%20providers#data-providers) (phpunit.de)
- [Mocking or the use of test doubles](https://phpunit.readthedocs.io/en/9.5/test-doubles.html?highlight=mocking#test-doubles) (phpunit.de)
- [Code coverage analysis](https://phpunit.readthedocs.io/en/9.5/code-coverage-analysis.html?highlight=code%20coverage#code-coverage-analysis) (phpunit.de)
  (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Software Testing Overview](/tutorial/software-testing-overview?p=3262)

Next
[Install Drupal Development Requirements with Composer](/tutorial/install-drupal-development-requirements-composer?p=3262)

Clear History

Ask Drupalize.Me AI

close