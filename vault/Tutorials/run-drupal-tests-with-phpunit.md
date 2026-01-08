---
title: "Run Drupal Tests with PHPUnit"
url: "https://drupalize.me/tutorial/run-drupal-tests-phpunit?p=3263"
guide: "[[test-drupal-sites-automated-tests]]"
---

# Run Drupal Tests with PHPUnit

## Content

In this tutorial, we'll run tests in several different ways using the PHPUnit tools available in Drupal. We'll learn about various environment variables you'll need to supply to the test runner depending on which type of test you're running. And we'll learn various ways to get reports on the test results. By the end of this tutorial, you should understand how to run Drupal tests using PHPUnit.

## Goal

Be able to run tests in Drupal using PHPUnit.

## Prerequisites

- A [local Drupal development site](https://drupalize.me/tutorial/install-drupal-locally-ddev). This should *not* be a production site.
- [Install Drupal Development Requirements with Composer](https://drupalize.me/tutorial/install-drupal-development-requirements-composer)
- Command-line access.

If you're new to automated testing in Drupal, learn more with these concept tutorials:

- [Introduction to Testing in Drupal](https://drupalize.me/tutorial/introduction-testing-drupal)
- [Software Testing Overview](https://drupalize.me/tutorial/software-testing-overview)
- [Organize Test Files](https://drupalize.me/tutorial/organize-test-files)

Sprout Video

## PHPUnit and Drupal

In Drupal, we have the ability to use the [PHPUnit package](https://phpunit.de/) natively to run Drupal tests. This is good because the PHPUnit framework offers us a lot of features for testing. In addition, the test runner also gives us some important features such as coverage and complexity metrics.

After you've [installed development dependencies via Composer](https://drupalize.me/tutorial/install-drupal-development-requirements-composer), PHPUnit's test runner is located at *./vendor/bin/phpunit*. When you run it for Drupal purposes, you should invoke it with core's configuration, like this:

```
./vendor/bin/phpunit -c core/
```

This allows *phpunit* to discover the various Drupal test suites you'll be using. It also specifies the configuration directory, and not the XML configuration file itself. We'll see why this is later on in the tutorial.

If you are writing a test based on one of core's PHPUnit-based test frameworks, you should use the *phpunit* test runner (with `--filter`) during development to make sure it can discover and run your test. This way you know the test runner isn't giving you a false positive by skipping the test.

Let's run some tests!

## Test run of the PHPUnit test runner

The first thing to do is familiarize yourself with how to run the *phpunit* test runner.

From the command line, change to the Drupal root directory:

```
cd path/to/drupal/
```

The *phpunit* runner is installed by Composer. It lives in the *vendor/bin/* directory by default.

However, Drupal core's configuration file for *phpunit* is in the *core/* directory.

This means we have to tell *phpunit* to use the configuration file when we run it. Try it now, like this:

```
./vendor/bin/phpunit -c core/
```

You should see something like this:

```
./vendor/bin/phpunit -c core/
PHPUnit 4.8.35 by Sebastian Bergmann and contributors.

...........................................................    59 / 19986 (  0%)
[ ...etc... ]
```

(Press `control-c` to stop the test execution.)

The `-c` option on the command line interface tells *phpunit* where to find the configuration file. We can specify a directory to search for a configuration file. Drupal comes with a file in the *core/* directory called *core/phpunit.xml.dist*, and this is the file *phpunit* will find. In later steps, we'll copy and modify this file, and since we specify a directory here, *phpunit* will find our new file.

When we want to run tests in Drupal modules, we have to use Drupal core's configuration file. This is because it bootstraps the namespaces for our modules, and also specifies how *phpunit* should find tests in those modules.

## Run a single test

We can specify a test on the command line by including its pathname. Let's run a core test this way:

```
./vendor/bin/phpunit -c core/ core/tests/Drupal/Tests/Component/Plugin/DefaultFactoryTest.php
```

This will give us output like this:

```
PHPUnit 4.8.35 by Sebastian Bergmann and contributors.

..........

Time: 869 ms, Memory: 4.00MB

OK (10 tests, 18 assertions)
```

Congratulations, you now know the basics of how to run tests with *phpunit*.

## Use `--filter`

In the last step we specified a test file to run: *core/tests/Drupal/Tests/Component/Plugin/DefaultFactoryTest.php*. This has the advantage of being very quick to execute. However, the down side is that it allows *phpunit* to run our test, even if we put it in the wrong place. We might have put the wrong kind of test in the wrong location, for example.

We want to make sure the test runner can discover our test on its own. That way we know the runner will run it when we don't specify the full path to the file. If we don't at least check, we might end up with a test that never gets run again.

Let's try that with the `--filter` option. This makes *phpunit* find all the tests it can and then filter them with a regular expression which we supply. That expression can be just the test class name or as complex an expression as we'd like.

The file *core/tests/Drupal/Tests/Component/Plugin/DefaultFactoryTest.php* contains a class named `Drupal\Tests\Component\Plugin\DefaultFactoryTest`. Generally, we don't need to filter on the whole namespace, and we can just specify the class name by itself: `DefaultFactoryTest`.

Keep in mind that we're filtering on a regular expression, so we might end up with more tests running that we thought. For instance, if there's a class called `AnotherDefaultFactoryTest`, we'll end up running that, too.

We'll learn how to refine our discovery of tests in later steps, so for now we'll just filter on `DefaultFactoryTest`:

```
./vendor/bin/phpunit -c core/ --filter DefaultFactoryTest
PHPUnit 4.8.35 by Sebastian Bergmann and contributors.

..........

Time: 32.32 seconds, Memory: 124.00MB

OK (10 tests, 18 assertions)
```

We ran the same test but execution time was longer than when we specified the path to the test file. That's because when we use `--filter`, *phpunit* has to scan through the whole codebase and find all the tests and then sort through them with our filter.

We can also use `--filter` to specify a single method name. `DefaultFactoryTest` has a test method called `testGetPluginClassWithValidArrayPluginDefinition()`. We can combine the class and method name with `::` and filter against that:

```
./vendor/bin/phpunit -c core/ --filter DefaultFactoryTest::testGetPluginClassWithValidArrayPluginDefinition
PHPUnit 4.8.35 by Sebastian Bergmann and contributors.

.

Time: 32.12 seconds, Memory: 124.00MB

OK (1 test, 1 assertion)
```

## Specify a test type with `--testsuite`

PHPUnit allows you to specify a test type with the `--testsuite` flag.

Drupal core has 4 test suites we can run:

- `unit`
- `kernel`
- `functional`
- `functional-javascript`

The tests that eventually run for these suites are the four PHPUnit-based [frameworks](https://drupalize.me/tutorial/frameworks-testing-drupal) available in Drupal core: `UnitTestCase`, `KernelTestBase`, `BrowserTestBase`, and `WebDriverTestBase`.

Remember in the last step we specified a `--filter`? That caused *phpunit* to scan for all the tests before applying the filter.

What was actually happening was that *phpunit* scanned the codebase four times, one for each of the available test suites in core. If you look at the configuration file *core/phpunit.xml.dist*, you'll see the four test suites set up like this:

```
  <testsuites>
    <testsuite name="unit">
      <file>./tests/TestSuites/UnitTestSuite.php</file>
    </testsuite>
    <testsuite name="kernel">
      <file>./tests/TestSuites/KernelTestSuite.php</file>
    </testsuite>
    <testsuite name="functional">
      <file>./tests/TestSuites/FunctionalTestSuite.php</file>
    </testsuite>
    <testsuite name="functional-javascript">
      <file>./tests/TestSuites/FunctionalJavascriptTestSuite.php</file>
    </testsuite>
  </testsuites>
```

Each of these test suite objects scan for tests belonging to it. The suites are then combined to form the list of all the tests that can be run.

If we want to cut down the discovery time, we can specify a single test suite.

What if we only want to run, for example, unit tests and not any other type? You may be able to guess that we would specify `--testsuite unit`:

```
./vendor/bin/phpunit -c core/ --testsuite unit
PHPUnit 4.8.35 by Sebastian Bergmann and contributors.

...........................................................    59 / 15965 (  0%)
[ ...etc... ]
```

We can combine this with `--filter` to run only the tests we want from a specific test suite:

```
./vendor/bin/phpunit -c core/ --testsuite unit --filter DefaultFactoryTest
PHPUnit 4.8.35 by Sebastian Bergmann and contributors.

..........

Time: 14.75 seconds, Memory: 62.00MB

OK (10 tests, 18 assertions)
```

Unfortunately, PHPUnit does not have a way to specify multiple test suites per test run. You'd have to run *phpunit* multiple times to do this.

We'll have more to say about test suites later on, because all of them other than *unit* have dependencies we haven't accounted for.

## Stop running tests with `--stop-on-error` and `--stop-on-fail`

There are currently approximately 20,000 tests in Drupal core. If you run them all, it can take quite a while. Even running only the unit tests with `--testsuite unit` can give you enough time for a long coffee break.

What's worse is that if you set off a test run that's going to run a lot of tests and they all error-out because of configuration errors, you might end up hitting `control-c` to stop them before PHPUnit has reported the errors to you.

This makes it important to include the `--stop-on-error` flag in your *phpunit* command. The `--stop-on-error` flag will stop running test(s) if a test couldn't be performed at all. This could be due to any of the following:

- A PHPUnit configuration error in the options you provided in the command or in your *phpunit.xml* file.
- A PHP coding error (that triggers a PHP exception).
- PHPUnit can't access a resource it needs to run the test.

Remember in the last step we hinted that some test suites might have dependencies we hadn't talked about yet? Let's see what that means in a practical sense. We'll try to run the functional test suite before we've set up the dependencies.

```
./vendor/bin/phpunit -c core/ --testsuite functional --stop-on-error
PHPUnit 4.8.35 by Sebastian Bergmann and contributors.

E

Time: 7.46 seconds, Memory: 34.00MB

There was 1 error:

1) Drupal\FunctionalTests\Breadcrumb\Breadcrumb404Test::testBreadcrumbOn404Pages
Exception: You must provide a SIMPLETEST_BASE_URL environment variable to run some PHPUnit based functional tests.

/Users/paul/pj2/drupal/core/tests/Drupal/Tests/BrowserTestBase.php:409

FAILURES!
Tests: 1, Assertions: 0, Errors: 1.
```

Since we included `--stop-on-error`, we only had to wait 7.46 seconds to find out what went wrong. If we hadn't, it would have taken at least twenty minutes.

We can also manage what happens on test fails in a similar way. The `--stop-on-fail` option will stop the test run the first time a test fails. This can also save us some time.

The `--stop-on-fail` flag refers to the test itself, and will trigger a halt to the test-run if an expectation in the test is not met.

So, **what's the difference between `--stop-on-error` and `--stop-on-fail`?**

- `--stop-on-error`: triggered when the test can't be performed at all due to some error (PHPUnit configuration, PHP code, or unreachable resource)
- `--stop-on-fail`: triggered when the test was performed and the test failed because an expectation was not met.

## Run a test for a group with `--group`

Drupal core tests always have at least one `@group` annotation. If there's only one, it will be the machine name of the module that owns the test, or part of the namespace that the test is related to.

`@group` annotations look like this:

```
/**
 * Tests for content translation manage check.
 *
 * @coversDefaultClass \Drupal\content_translation\Access\ContentTranslationManageAccessCheck
 * @group Access
 * @group content_translation
 */
class ContentTranslationManageAccessCheckTest extends UnitTestCase {
```

*phpunit* can run tests based on a group with the `--group` option:

```
./vendor/bin/phpunit -c core/ --testsuite unit --group Plugin
PHPUnit 4.8.35 by Sebastian Bergmann and contributors.

...............................................................  63 / 177 ( 35%)
............................................................... 126 / 177 ( 71%)
...................................................

Time: 14.01 seconds, Memory: 66.00MB

OK (177 tests, 454 assertions)
```

Notice that we've specified `--testsuite unit` here. That's because there are functional tests that belong to the *Plugin* group, too, but so far we haven't talked about how to make those tests work.

Let's try to run all the unit tests in the *Plugin* group that have a "q" in their name.

## Output options

One of the great things about *phpunit* is that its output can be printed in a lot of different ways.

The previous step hints that we might be able to run only unit tests in the *Plugin* group with "q" in their name. Well, we can, with a command line like this:

```
./vendor/bin/phpunit -c core/ --testsuite unit --group Plugin --filter q
```

That's a great start, but what tests actually ran? If we run this test, we see some dots and a pass/fail result, but not much else.

## Example: TestDox

It turns out there's an interesting output type for tests called [TestDox](https://en.wikipedia.org/wiki/TestDox). TestDox comes from the Java unit testing world but it also applies to PHP. It just so happens that TestDox output is included with PHPUnit.

We can use the `--testdox` option to see the output in a totally different way:

```
./vendor/bin/phpunit -c core/ --testsuite unit --group Plugin --filter q --testdox
PHPUnit 4.8.35 by Sebastian Bergmann and contributors.

Drupal\Tests\Core\Plugin\ContextHandler
 [x] Check requirements
 [x] Apply context mapping missing required
 [x] Apply context mapping missing not required
 [x] Apply context mapping no value required
 [x] Apply context mapping no value non required

Drupal\Tests\Core\Plugin\DefaultPluginManager
 [x] Get definitions without required interface
```

These sentences are generated by taking a "camelCase" method name and splitting it up to make it look like a sentence. It appears that the q's were found in the method names and not the class names.

## Specify different output printers

TestDox in and of itself isn't all that important, but it does show something really interesting: PHPUnit can use what's called an output printer in order to show you your test results in different ways.

For instance, if you want to [see your test output as NyanCat](https://github.com/whatthejeff/nyancat-phpunit-resultprinter), here it is:

Image

![Animated image showing NyanCat output](/sites/default/files/styles/max_800w/public/tutorials/images/runners-nyan-cat.gif?itok=N_wDGaep)

Much more useful is the fact that core supplies us with a way to look at the output of our functional tests in HTML.

We'll learn more about that as we set up dependencies for more types of tests.

## Generate a report with `--log-junit`

You might be asking: "I don't care about TestDox. How do I get a useful report?"

PHPUnit can generate a few types of reports on its own:

- JUnit
- TAP
- JSON

You specify these different log types with `--log-[type]=output.file`. You can specify as many as you want, all at the same time, in fact.

JUnit is probably the most common, since it is used by other test reporting systems like Jenkins. Let's take a look at what that looks like in action.

Here is our *Plugin* group test run with a report file output:

```
./vendor/bin/phpunit -c core/ --testsuite unit --group Plugin --log-junit=report.xml
PHPUnit 4.8.35 by Sebastian Bergmann and contributors.

...............................................................  63 / 177 ( 35%)
............................................................... 126 / 177 ( 71%)
...................................................

Time: 14.25 seconds, Memory: 66.00MB

OK (177 tests, 454 assertions)
```

And here's a fragment of the JUnit XML generated by this command:

```
<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="" tests="177" assertions="454" failures="0" errors="0" time="1.358750">
    <testsuite name="unit" tests="177" assertions="454" failures="0" errors="0" time="1.358750">
      <testsuite name="unit" tests="177" assertions="454" failures="0" errors="0" time="1.358750">
        <testsuite name="Drupal\Tests\Component\Annotation\Plugin\Discovery\AnnotationBridgeDecoratorTest" file="/Users/paul/pj2/drupal/core/tests/Drupal/Tests/Component/Annotation/Plugin/Discovery/AnnotationBridgeDecoratorTest.php" tests="1" assertions="1" failures="0" errors="0" time="0.014434">
          <testcase name="testGetDefinitions" class="Drupal\Tests\Component\Annotation\Plugin\Discovery\AnnotationBridgeDecoratorTest" file="/Users/paul/pj2/drupal/core/tests/Drupal/Tests/Component/Annotation/Plugin/Discovery/AnnotationBridgeDecoratorTest.php" line="20" assertions="1" time="0.014434"/>
        </testsuite>
        <testsuite name="Drupal\Tests\Component\Plugin\Context\ContextTest" file="/Users/paul/pj2/drupal/core/tests/Drupal/Tests/Component/Plugin/Context/ContextTest.php" tests="4" assertions="10" failures="0" errors="0" time="0.036185">
          <testsuite name="Drupal\Tests\Component\Plugin\Context\ContextTest::testGetContextValue" tests="3" assertions="8" failures="0" errors="0" time="0.026246">
            <testcase name="testGetContextValue with data set #0" assertions="1" time="0.006261"/>
            <testcase name="testGetContextValue with data set #1" assertions="3" time="0.012334"/>
            <testcase name="testGetContextValue with data set #2" assertions="4" time="0.007651"/>
          </testsuite>
          <testcase name="testDefaultValue" class="Drupal\Tests\Component\Plugin\Context\ContextTest" file="/Users/paul/pj2/drupal/core/tests/Drupal/Tests/Component/Plugin/Context/ContextTest.php" line="88" assertions="2" time="0.009939"/>
        </testsuite>
```

See where `ContextTest::testGetContextValue()` ran three times with different data sets? That shows us that `testGetContextValue()` uses something called a `@dataProvider`.

But, before we get ahead of ourselves, let's think about why we might want to use `--log-json`:

```
{
    "event": "suiteStart",
    "suite": "",
    "tests": 177
}{
    "event": "suiteStart",
    "suite": "unit",
    "tests": 177
}{
    "event": "suiteStart",
    "suite": "unit",
    "tests": 177
}{
    "event": "suiteStart",
    "suite": "Drupal\\Tests\\Component\\Annotation\\Plugin\\Discovery\\AnnotationBridgeDecoratorTest",
    "tests": 1
}{
    "event": "testStart",
    "suite": "Drupal\\Tests\\Component\\Annotation\\Plugin\\Discovery\\AnnotationBridgeDecoratorTest",
    "test": "Drupal\\Tests\\Component\\Annotation\\Plugin\\Discovery\\AnnotationBridgeDecoratorTest::testGetDefinitions"
}{
    "event": "test",
    "suite": "Drupal\\Tests\\Component\\Annotation\\Plugin\\Discovery\\AnnotationBridgeDecoratorTest",
    "test": "Drupal\\Tests\\Component\\Annotation\\Plugin\\Discovery\\AnnotationBridgeDecoratorTest::testGetDefinitions",
    "status": "pass",
    "time": 0.0144650936127,
    "trace": [],
    "message": "",
    "output": ""
}
```

The JSON output format is essentially a log of all of the events available to a PHPUnit test listener. This is a semi-advanced topic, but you might be able to use the JSON output instead of writing a test listener.

## Configure PHPUnit for Drupal's dependencies

Up until now we've only dealt with unit tests in *phpunit*. That's because unit tests don't have a lot of dependencies. There's not a lot to set up and configuration in order to make them run.

But we have other types of tests: `kernel`, `functional`, and `functional-javascript`.

What other dependencies do we need to account for in order to run them?

Let's try and run a kernel test. We'll use `--stop-on-error` (because we already know there will be an error):

```
./vendor/bin/phpunit -c core/ --testsuite kernel --stop-on-error
PHPUnit 4.8.35 by Sebastian Bergmann and contributors.

E

Time: 7.42 seconds, Memory: 34.00MB

There was 1 error:

1) Drupal\KernelTests\Component\Utility\SafeMarkupKernelTest::testSafeMarkupUri with data set "routed-url" ('Hey giraffe <a href=":url">MUUUH</a>', 'route:system.admin', array(), 'Hey giraffe <a href="/admin">MUUUH</a>')
Exception: There is no database connection so no tests can be run. You must provide a SIMPLETEST_DB environment variable to run PHPUnit based functional tests outside of run-tests.sh. See https://www.drupal.org/node/2116263#skipped-tests for more information.
```

You can see from the error message that we need to set a `SIMPLETEST_DB` environment variable to run this test. As it turns out, we need that environment variable to run all kernel tests.

Let's try the same thing with a functional test:

```
./vendor/bin/phpunit -c core/ --testsuite functional --stop-on-error
PHPUnit 4.8.35 by Sebastian Bergmann and contributors.

E

Time: 7.35 seconds, Memory: 34.00MB

There was 1 error:

1) Drupal\FunctionalTests\Breadcrumb\Breadcrumb404Test::testBreadcrumbOn404Pages
Exception: You must provide a SIMPLETEST_BASE_URL environment variable to run some PHPUnit based functional tests.
```

Again, it's telling us that we need to supply a `SIMPLETEST_BASE_URL` environment variable.

The same thing happens for [`functional-javascript` tests](https://drupalize.me/tutorial/implement-functional-test), because `functional-javascript` tests are functional tests with a JavaScript component added.

We can specify these environment variables on the command line or we can specify them within the PHPUnit configuration file. We'll see examples of each in later in this tutorial.

First, let's look at what each of these environment variables means.

## Kernel tests need a database: `SIMPLETEST_DB`

Kernel tests boot up a fixture Drupal without installing it. That is, each kernel test bootstraps Drupal to a very low level. In order to operate, this Drupal kernel needs some database services. So we need to provide a database that could be used to install Drupal.

As we saw above, this requires us to tell the test runner a database URL. We do that through an environment variable called `SIMPLETEST_DB`.

### Example: Command line

We can provide an environment variable through the command line, like this:

```
SIMPLETEST_DB=mysql://root:root@localhost:8889/d8 ./vendor/bin/phpunit -c core/ --testsuite kernel --stop-on-error --filter SafeMarkupKernelTest
PHPUnit 4.8.35 by Sebastian Bergmann and contributors.

...........

Time: 36.55 seconds, Memory: 34.00MB

OK (11 tests, 22 assertions)
```

The database URL scheme is the same as for PHP's PDO. In this example, we're using MAMP, which has a MySQL database, with a user named root with *root* as a password, uses port 8889, and has a database called *d8*. So the URL looks like `mysql://root:root@localhost:8889/d8`.

Substitute your own credentials as needed. We also limited the test run to one test, through the `--filter` option, so it wouldn't take a long time to finish.

So that's one way to tell kernel tests what database to use, by including it on the command line. We can also use the PHPUnit configuration file.

### Example: Configuration file

Another way to tell kernel tests what database to use is to include it in the configuration file for PHPUnit.

To do this, first we copy and rename *core/phpunit.xml.dist* to *core/phpunit.xml*. Here's how to do it in the command line:

```
cp core/phpunit.xml.dist core/phpunit.xml
ls core/phpunit*
core/phpunit.xml	core/phpunit.xml.dist
```

Now when we run PHPUnit using the `-c core/` option, the *phpunit* tool will use *core/phpunit.xml* instead of *core/phpunit.xml.dist*.

Let's edit *core/phpunit.xml* in order to have it use our database URL.

If you search through *core/phpunit.xml*, you'll find a code comment with a template for how to make this change:

```
    <!-- Example SIMPLETEST_DB value: mysql://username:password@localhost/databasename#table_prefix -->
    <env name="SIMPLETEST_DB" value=""/>
```

So add your database credentials into the value URL. For a local MAMP setup it looks like this, but yours might well be different:

```
    <env name="SIMPLETEST_DB" value="mysql://root:root@localhost:8889/d8"/>
```

Note: If the driver adds multiple parts to the querystring, you have to manually convert the querystring separators `&` to HTML entities counterparts `&amp;`, to comply to XML syntax. See change record [Drupal core tests can be run with contributed database drivers](https://www.drupal.org/node/2896416).

Now we can run kernel tests without supplying the environment variable on the command line:

```
./vendor/bin/phpunit -c core/ --testsuite kernel --stop-on-error --filter SafeMarkupKernelTest
PHPUnit 4.8.35 by Sebastian Bergmann and contributors.

...........

Time: 36.2 seconds, Memory: 34.00MB

OK (11 tests, 22 assertions)
```

## Functional tests need a web server: `SIMPLETEST_BASE_URL`

As we saw in an earlier step, functional tests require an environment variable for the web server to make HTTP requests against: `SIMPLETEST_BASE_URL`. As with the previous step, we can provide it on the command line or in the configuration file.

### Example: Command line

Here it is on the command line, for a MAMP installation. Again, your URL might be different:

```
SIMPLETEST_BASE_URL=http://localhost:8888/ ./vendor/bin/phpunit -c core/ --testsuite functional --filter Breadcrumb404Test
PHPUnit 4.8.35 by Sebastian Bergmann and contributors.

.

Time: 10.39 seconds, Memory: 36.00MB

OK (1 test, 3 assertions)
```

### Example: Configuration file

And, like `SIMPLETEST_DB`, we can also specify it in our own *core/phpunit.xml* file.

If you haven't created one, refer to the previous step, or copy *core/phpunit.xml.dist* to *core/phpunit.xml*.

Then edit *core/phpunit.xml*:

```
    <!-- Example SIMPLETEST_BASE_URL value: http://localhost -->
    <env name="SIMPLETEST_BASE_URL" value=""/>
```

We'll add our localhost value here.

```
    <env name="SIMPLETEST_BASE_URL" value="http://localhost/"/>
```

Now we can run the same test without the environment variable on the command line:

```
./vendor/bin/phpunit -c core/ --testsuite functional --filter Breadcrumb404Test
PHPUnit 4.8.35 by Sebastian Bergmann and contributors.

.

Time: 10.06 seconds, Memory: 36.00MB

OK (1 test, 3 assertions)
```

## `Functional-Javascript` needs a `selenium-server` process

When we try to run `functional-javascript` tests in *phpunit*, we generally get a lot of skipped tests.

Since we added the `-v` option, we can see that the `functional-javascript` tests skipped because there was no available `selenium-server` instance, which we need to run tests that make use of WebDriver API.

You can learn about [installing and running selenium-server from this tutorial](https://drupalize.me/tutorial/run-functional-javascript-tests).

## Functional test output with `--printer`

You can see the HTML generated by the tests and browser through it by configuring an output printer. The test run stores the HTML generated by tests enabling you to browse through the output.

Let's see how this works and how to set it up in PHPUnit. First, run `Drupal\FunctionalTests\Image\ToolkitSetupFormTest`:

```
SIMPLETEST_BASE_URL=http://localhost:8888/ ./vendor/bin/phpunit -c core/ --testsuite functional --filter ToolkitSetupFormTest
PHPUnit 4.8.35 by Sebastian Bergmann and contributors.

.

Time: 34.97 seconds, Memory: 34.00MB

OK (1 test, 13 assertions)
```

Let's look at what this test actually does. `ToolkitSetupFormTest` sets up by logging in an admin user. It then tries to visit the image toolkit administration page, and posts forms changing the settings for that page.

As it is, this test passes, but if it didn't, we'd want to see the results of trying to get that admin page and also see what happened when we tried to post forms.

So let's figure out how to do that.

## Configure the output printer

We can configure the output printer with `--printer` and `BROWSERTEST_OUTPUT_DIRECTORY`.

We saw with the `--testdox` example above that PHPUnit can use its own plugin type called *output printers* to alter how test information is displayed. Remember the nyan cat output?

Drupal comes with its own output printer which can keep and display HTML output from tests. This is made possible by a class called `Drupal\Tests\Listeners\HtmlOutputPrinter`.

`HtmlOutputPrinter` needs a place to store files temporarily before they're presented to the user. We can assign a directory for this purpose. `HtmlOutputPrinter` learns about this directory through the environment variable `BROWSERTEST_OUTPUT_DIRECTORY`.

If you're a user running tests, `BROWSERTEST_OUTPUT_DIRECTORY` could be any writable directory. For use by a script, you'd almost certainly want to make this a directory within `/tmp`.

We can put all of this together on the command line. We provide the `BROWSERTEST_OUTPUT_DIRECTORY` environment variable, and then add the `--printer` option to the command.

Note that we also still need the `SIMPLETEST_BASE_URL` environment variable, since we're running functional tests.

```
SIMPLETEST_BASE_URL=http://localhost:8888/ BROWSERTEST_OUTPUT_DIRECTORY=browser ./vendor/bin/phpunit -c core/ --testsuite functional --filter ToolkitSetupFormTest --printer 'Drupal\Tests\Listeners\HtmlOutputPrinter'
PHPUnit 4.8.35 by Sebastian Bergmann and contributors.

.

Time: 34.86 seconds, Memory: 34.00MB

OK (1 test, 13 assertions)

HTML output was generated
http://localhost:8888/sites/simpletest/browser_output/Drupal_FunctionalTests_Image_ToolkitSetupFormTest-37-50142549.html
http://localhost:8888/sites/simpletest/browser_output/Drupal_FunctionalTests_Image_ToolkitSetupFormTest-38-50142549.html
http://localhost:8888/sites/simpletest/browser_output/Drupal_FunctionalTests_Image_ToolkitSetupFormTest-39-50142549.html
http://localhost:8888/sites/simpletest/browser_output/Drupal_FunctionalTests_Image_ToolkitSetupFormTest-40-50142549.html
http://localhost:8888/sites/simpletest/browser_output/Drupal_FunctionalTests_Image_ToolkitSetupFormTest-41-50142549.html
http://localhost:8888/sites/simpletest/browser_output/Drupal_FunctionalTests_Image_ToolkitSetupFormTest-42-50142549.html
http://localhost:8888/sites/simpletest/browser_output/Drupal_FunctionalTests_Image_ToolkitSetupFormTest-43-50142549.html
http://localhost:8888/sites/simpletest/browser_output/Drupal_FunctionalTests_Image_ToolkitSetupFormTest-44-50142549.html
http://localhost:8888/sites/simpletest/browser_output/Drupal_FunctionalTests_Image_ToolkitSetupFormTest-45-50142549.html
http://localhost:8888/sites/simpletest/browser_output/Drupal_FunctionalTests_Image_ToolkitSetupFormTest-46-50142549.html
http://localhost:8888/sites/simpletest/browser_output/Drupal_FunctionalTests_Image_ToolkitSetupFormTest-47-50142549.html
http://localhost:8888/sites/simpletest/browser_output/Drupal_FunctionalTests_Image_ToolkitSetupFormTest-48-50142549.html
http://localhost:8888/sites/simpletest/browser_output/Drupal_FunctionalTests_Image_ToolkitSetupFormTest-49-50142549.html
http://localhost:8888/sites/simpletest/browser_output/Drupal_FunctionalTests_Image_ToolkitSetupFormTest-50-50142549.html
http://localhost:8888/sites/simpletest/browser_output/Drupal_FunctionalTests_Image_ToolkitSetupFormTest-51-50142549.html
http://localhost:8888/sites/simpletest/browser_output/Drupal_FunctionalTests_Image_ToolkitSetupFormTest-52-50142549.html
http://localhost:8888/sites/simpletest/browser_output/Drupal_FunctionalTests_Image_ToolkitSetupFormTest-53-50142549.html
http://localhost:8888/sites/simpletest/browser_output/Drupal_FunctionalTests_Image_ToolkitSetupFormTest-54-50142549.html
```

Notice all those URLs at the end?

They all represent HTML output from the test.

You can copy any of them and paste them into a web browser. This will take you to the output. Here's what the first one looks like:

Image

![Output from the output printer](/sites/default/files/styles/max_800w/public/tutorials/images/runners-output-printer.png?itok=y96c9s8p)

This gives you some information about where the output came from, shows you the HTML, and then shows the headers for the request.

You might be wondering how to connect this output to a given request in the test. This is accomplished by looking at the file name in the URL. For instance, that first request has this URL:

```
http://localhost/sites/simpletest/browser_output/Drupal_FunctionalTests_Image_ToolkitSetupFormTest-37-50142549.html
```

We can see that the output comes from `Drupal\FunctionalTests\Image\ToolkitSetupFormTest`.

We can also see the request information in the output: `GET request to: http://localhost/user/login`. We can use this to deduce that the output comes from the `setUp()` method of the test, where we log in a user.

Unfortunately, that's all we get. This is useful if we are debugging a single test, because we can poke around just one piece of output.

OK, if you're tired of typing `BROWSERTEST_OUTPUT_DIRECTORY` into the command line, we can add configuration for this output printer to our configuration file.

## Set up a configuration file

If you haven't already, it's time once again to make a copy of core's *phpunit.xml.dist* file and call it *phpunit.xml*.

```
cd root/of/drupal
cp core/phpunit.xml.dist core/phpunit.xml
```

Now we edit the new file.

In previous steps, we added `SIMPLETEST_BASE_URL` to support functional tests. We can add that here since we're running functional tests.

```
    <!-- Example SIMPLETEST_BASE_URL value: http://localhost -->
    <env name="SIMPLETEST_BASE_URL" value="http://localhost:8888/"/>
```

We then change `BROWSERTEST_OUTPUT_DIRECTORY` to reflect our temporary storage directory:

```
    <!-- Example BROWSERTEST_OUTPUT_DIRECTORY value: /path/to/webroot/sites/simpletest/browser_output -->
    <env name="BROWSERTEST_OUTPUT_DIRECTORY" value="browser"/>
```

And now one thing remains. On the command line we used `--printer` to specify `HtmlOutputPrinter`. In the config file we'll add the `printerClass` property to the `phpunit` configuration, like this:

```
<phpunit bootstrap="tests/bootstrap.php" colors="true"
         beStrictAboutTestsThatDoNotTestAnything="true"
         beStrictAboutOutputDuringTests="true"
         beStrictAboutChangesToGlobalState="true"
         checkForUnintentionallyCoveredCode="false"
         printerClass="\Drupal\Tests\Listeners\HtmlOutputPrinter">
```

This is explained in the documentation block just below that section of the file.

Now we can run functional tests without `--printer` or those environment variables, and the output will always be presented to us.

This has a minor downside of making tests take longer to run, and filling the console screen with URLs. If you want to avoid this, you can take out either the `printerClass` or the `BROWSERTEST_OUTPUT_DIRECTORY` from configuration, and supply it on the command line when you do want to see the output.

## Functional JavaScript output

Let's try it with a functional JavaScript test (after [setting up our machine to run WebDriver-based tests](https://drupalize.me/tutorial/run-functional-javascript-tests)):

```
./vendor/bin/phpunit -c core/ --testsuite functional-javascript --filter AjaxFormPageCacheTest
PHPUnit 4.8.35 by Sebastian Bergmann and contributors.

..

Time: 1.06 minutes, Memory: 6.00MB

OK (2 tests, 21 assertions)

HTML output was generated
http://localhost:8888/sites/simpletest/browser_output/Drupal_FunctionalJavascriptTests_Ajax_AjaxFormPageCacheTest-1-86147148.html
http://localhost:8888/sites/simpletest/browser_output/Drupal_FunctionalJavascriptTests_Ajax_AjaxFormPageCacheTest-2-78098735.html
```

As you can see, it's much the same, but JavaScript assets will be added to the page. Of course, since the test output represents a session and that session is over, the scripted interactions in that output will not work. But you can still see the output.

## Create screenshots during test running

This is more of a debugging tool, but if you're writing and running tests, you should be aware that this is possible.

`Drupal\FunctionalJavascriptTests\WebDriverTestBase` has a method called `createScreenshot()`. You pass in a file name to this method, and rather than generating HTML, this method will take a screenshot of the virtual browser and put it in the file you specify.

We won't demonstrate it here, because core doesn't have tests that actually do this. That said, it can be a useful debugging tool if you're writing your own tests.

## Recap

In this tutorial, we learned that different test types have different requirements. Functional tests need a web server, and kernel tests need a database. Functional JavaScript tests need a Selenium Server instance running in the background.

We also learned that we can make a copy of *core/phpunit.xml.dist* called *core/phpunit.xml* and modify it. This allows us to customize environment variables so we don't have to type them every time we run our tests on the command line.

We also learned how to manage screenshots taken by WebDriver tests.

## Further your understanding

- Were you successful in installing the requirements to run the different types of functional tests?
- Were you able to successfully run functional tests? How did it go? What did you learn from the process?

## Additional resources

- [Debug any of Drupal's PHPUnit tests in PhpStorm with a DDEV Environment](https://drupalize.me/blog/debug-any-drupals-phpunit-tests-phpstorm-ddev-environment) (Drupalize.Me)
- [Frameworks for Testing in Drupal](https://drupalize.me/tutorial/frameworks-testing-drupal) (Drupalize.Me)
- [Functional JavaScript Testing with WebDriver](https://drupalize.me/tutorial/run-functional-javascript-tests) (Drupalize.Me)
- [PHPUnit in Drupal](https://www.drupal.org/docs/automated-testing/phpunit-in-drupal) (Drupal.org)
- [Running PHPUnit Tests](https://www.drupal.org/docs/automated-testing/phpunit-in-drupal/running-phpunit-tests) (Drupal.org)
- [PHPUnit JavaScript testing tutorial](https://www.drupal.org/docs/8/phpunit/phpunit-javascript-testing-tutorial) (Drupal.org)
- [PHPUnit](https://phpunit.de/) (phpunit.de)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Set Up a Functional Test](/tutorial/set-functional-test?p=3263)

Clear History

Ask Drupalize.Me AI

close