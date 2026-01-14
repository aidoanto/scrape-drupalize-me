---
title: "Convert Tests from Simpletest to PHPUnit"
url: "https://drupalize.me/tutorial/convert-tests-simpletest-phpunit?p=3264"
guide: "[[test-drupal-sites-automated-tests]]"
order: 15
---

# Convert Tests from Simpletest to PHPUnit

## Content

Simpletest has been removed from Drupal 9. If you're preparing to upgrade your site to the latest version of Drupal and you have Simpletests in your codebase that extend `WebTestBase` you'll need to update them to use PHPUnit's `BrowserTestBase` class instead. This will ensure your tests don't depend on a deprecated testing framework. By the end of this tutorial, you should be able to convert `WebTestBase`-based tests to use PHPUnit's `BrowserTestBase` class instead.

## Goal

Be able to convert a Simpletest based on `WebTestBase` test to a PHPUnit test based on `BrowserTestBase`.

## Prerequisites

- A [local development site](https://drupalize.me/tutorial/install-drupal-locally-ddev) with the [development dependencies installed via Composer](https://drupalize.me/tutorial/install-drupal-development-requirements-composer).
- Command-line access.
- Passing Simpletest-based tests to convert. (It's important that the tests pass before we start). We'll be using the *testing\_example* module from the [Examples for Developers project](https://www.drupal.org/project/examples) as our tests to convert in this tutorial.
- [Run Drupal Tests with PHPUnit](https://drupalize.me/tutorial/run-drupal-tests-phpunit)

## Overview of the conversion process

The most basic assumption of this entire tutorial is that the test is already passing. If you're looking at a Simpletest-based test and it's not passing, make it pass before performing the conversion. We want the conversion process to be as easy as possible, so let's look at the steps we'll use in order to convert the test.

## Test conversion: what not to change

When converting tests we shouldn't change the underlying code we're testing. It's also a bad idea to change the data sets in the test, unless we're absolutely sure that we have a good reason to do so. In essence, don't change your production code to make the tests pass. Always fix the tests first.

## Naive conversion

The first phase is relatively easy and is often all it takes to convert a test. We'll call this the "naive" conversion. All we do is move some files around, rename some things, and hope for the best. With these modifications in place we can then run the test and find out if that was enough by seeing if the test passes or fails.

If our naive conversion succeeds, we can move on to converting other deprecated code in our tests.

For this step, we'll be using the `NaiveConversionTest` class from the [*testing\_example* module](https://git.drupalcode.org/project/examples/-/tree/3.x/modules/testing_example). You can substitute your own module name and test class if you're working on a module other than *testing\_example*.

The steps we'll perform:

- Move the test class file from *testing\_example/src/Tests/NaiveConversionTest.php* to *testing\_example/tests/src/Functional/NaiveConversionTest.php*.
- Change the namespace from `Drupal\testing_example\Tests\NaiveConversionTest` to `Drupal\Tests\testing_example\Functional\NaiveConversionTest`.
- Replace `use Drupal\simpletest\WebTestBase;` with `use Drupal\Tests\BrowserTestBase;`.
- Change the superclass from `WebTestBase` to `BrowserTestBase`.
- Run the test to see if it fails (or breaks).

Let's walk through that in more detail:

### Re-organize files

We start with a Simpletest-based test file at a path like this:

*testing\_example/src/Tests/NaiveConversionTest.php*

We move it to a path like this:

*testing\_example/tests/src/Functional/NaiveConversionTest.php*

If the subdirectory *tests/src/Functional* doesn't exist, create it.

This is the first step towards helping Drupal with the auto-discovery of your newly converted functional test. Now we need to rename a few things by editing the test file we just moved.

### Change the namespace

Since we moved the file, we've changed its [PSR-4 namespace](https://drupalize.me/blog/201408/preparing-drupal-8-psr-4-autoloading).

In this case, we have to adjust the namespace declaration near the top of our file.

Originally, it was:

```
<?php

namespace Drupal\testing_example\Tests;
```

Change it to:

```
<?php

namespace Drupal\Tests\testing_example\Functional;
```

### Update the `use` statement

We don't want to use `WebTestBase` anymore. Instead we'll use `BrowserTestBase`.

Find the `use Drupal\simpletest\WebTestBase;` statement in your test class file and change it to use `use Drupal\Tests\BrowserTestBase;`.

Before:

```
use Drupal\simpletest\WebTestBase;
```

After:

```
use Drupal\Tests\BrowserTestBase;
```

### Change the superclass

In order to complete our naive conversion, we have to change our test class to extend `BrowserTestBase` instead of `WebTestBase`.

Before:

```
class NaiveConversionTest extends WebTestBase {
```

After:

```
class NaiveConversionTest extends BrowserTestBase {
```

Save the file.

Congratulations! You just performed a naive test conversion.

### Run the test

Now we can check whether we did enough work or whether we have more to do.

We'll run the test using PHPUnit's `--testsuite` and `--filter` options. We'll use these to make sure that the test runner can find the test correctly.

Also, since this is a functional test, we need to make sure we have a `SIMPLETEST_BASE_URL` environmental variable set, either in our *phpunit.xml* file or on the command line. We'll specify it on the command line here for simplicity's sake. These options are covered in more detail in [Run Drupal Tests with the run-tests.sh Script](https://drupalize.me/tutorial/run-drupal-tests-run-testssh-script).

The environmental variable `SIMPLETEST_BASE_URL` should be the URL to your local development web server. For example, using MAMP, we'd need to make sure MAMP is running and that we add `SIMPLETEST_BASE_URL=http://localhost/` before we invoke PHPUnit. Your local site's URL might be different and depend on your setup.

Let's change directories on the command line to be in the root of the Drupal installation.

```
cd path/to/your/drupal/root
```

Now let's run the test. (Note: you should substitute your test class name if it's different from `NaiveConversionTest`.)

```
SIMPLETEST_BASE_URL=http://localhost/ ./vendor/bin/phpunit -c core/ --testsuite functional --filter NaiveConversionTest --stop-on-error
```

Did the test run and pass? If it did, you're essentially done, and you can move on to converting another test. Optionally, you can make sure the test doesn't use deprecated assertions.

If the test didn't run at all, then the test runner might not have found it. Try running it like this:

```
SIMPLETEST_BASE_URL=http://localhost/ ./vendor/bin/phpunit -c core/ path/to/your/test/YourTest.php --stop-on-error
```

If that runs the test (whether it passes or fails), it's an indication that Drupal had trouble autoloading your test class. You probably need to make sure you didn't skip moving the test to *module\_name/tests/src/Functional/* or updating the namespace correctly. Once you've checked on those tasks, try running the test again with `--testsuite` and `--filter`.

Did the test run but fail? That's good, too, but a naive conversion isn't enough in this case. Proceed with the next section.

## Address and fix failures

At this point, we have performed a basic, naive conversion, changing our original Simpletest into a PHPUnit test that depends on the `WebTestBase` class. We've also run our newly converted test and have some messages that will help us figure out why our test failed.

For many tests, performing the naive conversion will be enough. But for some tests, moving to `BrowserTestBase` will be more of a challenge. That's because not every `WebTestBase` method is represented in `BrowserTestBase`. So we have to fill in the gaps.

Often, there's a similar method, but we have to find out what it is. For instance, `drupalGet()` takes a slightly different set of arguments depending on the test type.

Let's explore the compatibility layer and Mink, and then explore the different HTTP client models so we can fill the gap when the compatibility layer doesn't help us.

## Learn more about the compatibility layer

`BrowserTestBase` uses composition to build its behavior. That means it uses a lot of traits.

The one we care about right now is [`Drupal\FunctionalTests\AssertLegacyTrait`](https://git.drupalcode.org/project/drupal/-/blob/9.5.7/core/tests/Drupal/FunctionalTests/AssertLegacyTrait.php). `AssertLegacyTrait` implements a lot of the assertions in `WebTestBase` in order to deprecate them.

This trait is essentially the compatibility layer between `WebTestBase` and `BrowserTestBase`. If your test calls a `WebTestBase` method that is not in this trait or in `BrowserTestBase`, then you'll need to figure out the comparable way of doing the same task. See the cheat sheet later for some clues.

You can also learn a little bit about how `BrowserTestBase` interacts with Mink by looking at these replacement implementations.

Let's dive into Mink a little more.

## The Mink framework

`WebTestBase` manages HTTP requests itself. It does this using the CURL extension. You can see the implementation in detail in [`WebTestBase::curlExec()`](https://git.drupalcode.org/project/drupal/-/blob/8.8.x/core/modules/simpletest/src/WebTestBase.php#L589). Looking at this code, you'll see that it's 100+ lines of complex code. The fact that it's complex is one of the reasons it was replaced with Mink in Drupal 9.

`BrowserTestBase` uses a framework called [Mink](http://mink.behat.org/) to perform HTTP requests. Mink comes out of the [Behat](http://behat.org/) testing community, and supports a simulated web browser. It does a bunch of the heavy-lifting for our `BrowserTestBase` class, without having to maintain the complex custom CURL implementation, among other benefits.

Mink can also support multiple different types of drivers. `BrowserTestBase` configures it to use the [Goutte](https://github.com/FriendsOfPHP/Goutte) driver (rhymes with "boot"). The fact that we can change drivers allows us to use WebDriver API in `WebDriverTestBase`.

So you have two different models: `WebTestBase` with its native CURL implementation and `BrowserTestBase`, which glues together various frameworks. For the most part, `BrowserTestBase` has the compatibility layer to help map between these two different models. But it can help to know how the Mink model works in order to make a better conversion between the two. It also helps us to write better tests later.

In `BrowserTestBase`, we have two kinds of sessions with similar accessor methods. This can be a little confusing, so let's walk through it.

## The Mink session object

Let's look at `BrowserTestBase::drupalGetHeaders()`. This method is a leftover from `WebTestBase` and was marked as deprecated in Drupal 8.

Here's how it's implemented:

```
  /**
   * Returns all response headers.
   *
   * @return array
   *   The HTTP headers values.
   *
   * @deprecated Scheduled for removal in Drupal 9.0.0.
   *   Use $this->getSession()->getResponseHeaders() instead.
   */
  protected function drupalGetHeaders() {
    return $this->getSession()->getResponseHeaders();
  }
```

See how it gets the current session and then makes a proper fluent OOP request against it?

Calling `getSession()` gives you a `\Behat\Mink\Session` object. You can use this to make all kinds of queries about the status of page transport, such as HTTP status code, page contents, and even response headers, as we see above.

Using the Mink session object to gather those types of values does not make a test assertion. If you need to test against them, you must wrap them in an appropriate assertion. Like this:

```
  $session = $this->getSession();
  $this->assertEquals(200, $session->getStatusCode());
```

The Mink session is also how `BrowserTestBase` tells Mink to perform an HTTP request, with its `visit()` method. But you should resist the urge to use the session to perform HTTP requests and use the various navigation methods available in `BrowserTestBase` instead. This includes, for instance, `drupalGet()`, `click()`, and `clickLink()`. We'll see why you should avoid using these methods directly later in this tutorial.

## Assertion session

We also have another type of session: the assertion session. This is a wrapper around the page contents that allows you to make assertions against it. You get ahold of this object using `BrowserTestBase::assertionSession()`.

Within `BrowserTestBase`, this method will give you a `Drupal\Tests\WebAssert` object, and then you can use that object to assert against static page content.

So let's dissect one of the compatibility layers for a common `WebTestBase` assertion: `assertLinkByHref()`. This method lets you assert that an anchor tag exists on the page by the `href` attribute it has.

In `BrowserTestBase`, this method is replicated by `AssertLegacyTrait::assertLinkByHref()`. However, the `WebAssert` class has a method called `linkByHrefExists()` that performs the same function.

So let's do both, side by side:

```
  public function testHref() {
    // These two assertions are identical.
    $this->assertLinkByHref('node/');
    $this->assertSession()->linkByHrefExists('node/');
  }
```

It might look like `assertLinkByHref()` is preferable but it isn't because it's deprecated.

So if you want to avoid re-converting your tests before Drupal 9, when the compatibility trait is removed, then you should perform this kind of conversion while you're looking at it.

If you have an IDE like PHPStorm, it will show you that the methods are deprecated automatically. This IDE feature can help you with this type of conversion.

## Review: session types

There are two types of sessions available to your tests:

- The Mink session is available from `$this->getSession()`. It gives you information about the transport layer of the HTTP request. This includes status code, cookies, and headers. Retrieving these values does not perform an assertion.
- The assertion session is available from `$this->assertionSession()`. It gives you a way to make assertions about the content of the request.

## HTTP requests

To make arbitrary HTTP requests, use `BrowserTestBase::getHttpClient`. As explained in its docblock:

- Use this method for arbitrary HTTP requests to the site under test. For most tests, you should not get the HTTP client and instead use navigation methods such as `drupalGet()` and `clickLink()` in order to benefit from assertions.
- Subclasses that substitute a different Mink driver should override this method and provide a Guzzle client if the Mink driver provides one.

You can also follow the example of [`Drupal\Tests\history\Functional\HistoryTest::markNodeAsRead()`](https://git.drupalcode.org/project/drupal/-/blob/10.1.x/core/modules/history/tests/src/Functional/HistoryTest.php#L94). This method ensures that all the proper cookies are set in the HTTP client:

```
  protected function markNodeAsRead($node_id) {
    $http_client = $this->getHttpClient();
    $url = Url::fromRoute('history.read_node', ['node' => $node_id], ['absolute' => TRUE])->toString();

    return $http_client->request('POST', $url, [
      'cookies' => $this->getSessionCookies(),
      'http_errors' => FALSE,
    ]);
  }
```

## Cheat sheet: Convert `WebTestBase` to `BrowserTestBase`

Finally, here's a cheat sheet for `WebTestBase` methods not directly supported in `BrowserTestBase`.

This cheat sheet was created by looking through the various issues referred to in [this issue](https://www.drupal.org/node/2735005) and compiling the details.

| `WebTestBase` | `BrowserTestBase` |
| --- | --- |
| Failing assertions do not stop test execution. | Failing assertions DO halt execution within that test method. |
| `$this->getRawContent()` | `$this->getSession()->getPage()->getContent()` |
| `$this->parse()` returns SimpleXML DOM. | `$this->getSession()->getPage()` returns `Behat\Mink\Element\DocumentElement` which has rich content query system. |
| `drupalPost()` | See the previous section about HTTP requests. |
| `xpath()` | Now returns an array of `Behat\Mink\Element\NodeElement` objects which has an OOP interface. E.G. `NodeElement->getText()` |
| `xpath()` works with XML | Mink's `xpath()` only works with HTML. Use `$this->getSession()->getPage()->getContent()` and parse with SimpleXML. |
| `$this->url` | `$this->getUrl()` |
| `$this->drupalGetWithFormat()` | `$this->drupalGet($path, ['query' => ['_format' => 'json']]);` |
| `$json = $this->drupalGetJSON()` | `$json = Json::decode($this->drupalGet($path, ['query' => ['_format' => 'json', 'etc' => 'etc']]))` |
| `$this->curlClose()` | `$this->mink->resetSessions()` |
| `$this->assertFieldByName($id)` | `$this->assertSession()->fieldExists($id)` |

## Recap

In this tutorial, we:

- Attempted to perform a "naive" conversion.
- Learned a bit about how `BrowserTestBase` uses Mink to help us perform conversions.
- Walked through a cheat sheet to guide us through a more complex conversion.

## Further your understanding

- Do you have any remaining Simpletests that need converting? Make a list and plan to convert them to future-proof your Drupal testing suite.

## Additional resources

- Change record: [New PHPUnit based classes added for testing: BrowserTestBase and JavascriptTestBase](https://www.drupal.org/node/2469723) (Drupal.org)
- Drupal core is converting all its tests to `BrowserTestBase` in [the PHPUnit Initiative](https://www.drupal.org/node/2807237) (Drupal.org)
- [Drupal core simpletest conversion meta issue](https://www.drupal.org/node/2735005) (Drupal.org)
- [Preparing for Drupal 8: PSR-4 Autoloading](https://drupalize.me/blog/201408/preparing-drupal-8-psr-4-autoloading) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Implement a Unit Test in Drupal](/tutorial/implement-unit-test-drupal?p=3264)

Clear History

Ask Drupalize.Me AI

close