---
title: "Introduction to Testing in Drupalfree"
url: "https://drupalize.me/tutorial/introduction-testing-drupal?p=3262"
guide: "[[test-drupal-sites-automated-tests]]"
order: 1
---

# Introduction to Testing in Drupalfree

## Content

In this gentle introduction to testing, we'll walk through what testing is and why it's important to your project. Then we'll define some terms you'll be likely to see while working with tests so that we're all on the same page. After reading through this tutorial you'll understand enough of the basic vocabulary to get started running (and eventually writing) tests for your Drupal site.

## Goal

Become familiar with the terminology around testing.

## Prerequisites

- None, other than an interest to learn more about testing in Drupal.

## What is a test?

A test is some code you write to prove things. What kinds of things might you need to prove?

- Whether or not a feature is implemented
- Whether or not an integration works correctly
- Whether or not a complex computation works the way you think it should work

The obvious next question is: Why would I need to prove things? It turns out there are a bunch of reasons why this is useful. You might need to show a client that something works the way they wanted it to work. You might need to prove to your manager that you did the work you said you'd do. And you might need to prove that some code still works even after you changed it.

So there are a bunch of different scopes for proving things and a bunch of different ways to write a test. These tutorials focus on Drupal (and its related technology). So we're going to show you how to be able to prove things in Drupal.

## Features of automated testing in Drupal

- Drupal uses a testing framework called PHPUnit. PHPUnit allows for very fine-grained testing. Its main purpose is for unit testing. But there are other Drupal frameworks built on top of it, such as, `KernelTestBase`, `BrowserTestBase` and `WebDriverTestBase`. These other frameworks allow you to perform different types of tests using Drupal. For instance, `BrowserTestBase` focuses on performing HTTP requests against the site under test in a consistent way.
- Drupal uses `phpunit` to run tests. Functional JavaScript tests are run with Chromedriver or Selenium.
- Drupal has standards about setting up tests, allowing test runners to always be able to find tests, as well as allow you to specify different types of tests to run.

You'll learn about test runners in these tutorials:

- [Run Drupal Tests with PHPUnit](https://drupalize.me/tutorial/run-drupal-tests-phpunit)
- [Set up a Functional Test](https://drupalize.me/tutorial/set-functional-test)
- [Run Functional JavaScript Tests](https://drupalize.me/tutorial/run-functional-javascript-tests)

## Automated testing terminology

Every area of specialization has its own terminology and testing is no exception. Before you head into the more in-depth tutorials, you should at least skim through these terms so you are familiar them, as they will be used frequently in related testing tutorials.

### Assertion

An *assertion* is how you tell the test to compare expectation versus reality. In PHPUnit, for instance, you can assert that two strings should be the same with `$this->assertEquals($expected_string, $test_string);`

Why don't we just say this is a "test" of the string? Because we're probably not testing whether these two strings are equal. We're probably testing a behavior that results in the string we expect. It's this kind of hair-splitting that makes testing fun. It's also why we have a word for *assertion*.

### Behavior

A *behavior* is the thing you're testing.

What happens when the user clicks on a specific link? Well, let's write a test of that behavior. The test will simulate clicking on a link, and then something will happen. We can check what happened by making assertions about the result.

There's an **expected** behavior and there's an **actual** behavior. Maybe your test expects a certain behavior but that's not the actual behavior. In which case, the test should fail. If the test doesn't fail even though the expectation and actual behavior don't match up, then it's a bad test.

### Dependency

A *dependency* is something that is needed in order for the test to perform properly. As you analyze the behavior you want to test, there may be other things that are needed to perform the test. Those are dependencies.

For instance, if we're going to test what happens when we look at the home page of a Drupal site, then the test has a dependency on an installed Drupal site -- and everything it depends on -- to run.

Sometimes dependencies are other parts of the code under test. For instance, in a strict unit test, you might be testing a method that depends on another method by calling it. So dependencies aren't always servers or other software packages.

### Expectation

An *expectation* should describe the intended outcome of the code. You expect behaviors to happen a certain way. You would expect that the site would show you the front page when you visit the domain URL, not a 404 error page. Saying that the site should show you the front page is your expectation. Testing for this expectation but receiving a 404 error instead should fail the test.

Note that your expectations can be wrong. You might think code is supposed to do something, but it's really supposed to do something else. In this situation you should find out what it is that you don't know so that you can write a better test.

### Fixture

A *fixture* is a fixed set of dependencies. For some tests, we'll need to have a minimum set of consistent dependencies available. This set is the fixture.

For instance, if we're implementing an entity type for Drupal, we'd want to create some of these entities in order to test their behavior. We'd want the creation method to be consistent across all the tests, so we know that we're testing the entity implementation, not the method of creation.

### Mock

See *Test Double* below.

### Regression

A *regression* happens when you re-introduce a previously-fixed problem or break a working solution. You wrote the code and it did what you expected. Now you've changed something and it doesn't work any more. You've introduced a regression. If you'd written a falsifiable test, then you'd have known that the change broke your expectations.

### Test Double

A *test double* is a part of the test that is created in order to isolate the test from its dependencies.

Test doubles are generally used in unit tests, in order to make absolutely sure that we're in control of dependencies, down to the lines-of-code level.

These include such colorfully-named types as Dummy, Fake, Stub, Spy, and Mock. If you venture into the realm of testing theory it's important to know that there are strongly held opinions on what term to use for a test double.

For the purposes of these tutorials, we'll generally use the term "mock" to generically refer to test doubles.

### Test types vs. suites

The Drupal testing ecosystem has some confusing terminology overlap. It's important to understand how Drupal uses a few keys terms.

There are *test suites* and *test types* which are generally synonymous. We use these terms based on different contexts, which is mostly a function of which test runner we're using at the time.

If we use the *run-tests.sh* script (removed in Drupal 9) to run tests, we tell it which `--types` we want to run.

These are the same as when we tell `phpunit` which `--testsuites` to run.

Another point of confusion is that the *run-tests.sh* script (removed in Drupal 9) and PHPUnit test suites have different names for the same thing. Each suite or type maps to a Drupal testing framework. Here's a chart to help clarify:

| Test Framework | run-tests.sh --type | phpunit --testsuite |
| --- | --- | --- |
| `UnitTestCase` | `PHPUnit-Unit` | `unit` |
| `KernelTestBase` | `PHPUnit-Kernel` | `kernel` |
| `BrowserTestBase` | `PHPUnit-Functional` | `functional` |
| `JavascriptTestBase` | `PHPUnit-FunctionalJavascript` | `functional-javascript` |

For the tutorials in this series, we'll use the term **test suites**.

Drupal also has tests for JavaScript using Nightwatch.js. See the tutorial [Functional JavaScript Testing with Nightwatch.js](https://drupalize.me/tutorial/functional-javascript-testing-nightwatchjs) for instructions on setting up and running tests using Nightwatch.

## Recap

In this tutorial, we learned about how testing works in Drupal. We defined a number of common terms and concepts in testing. You should now have a basic vocabulary for understanding the terminology used in the Drupal testing tutorials.

## Further your understanding

- To what extent do you write or use tests in your developer workflow?
- What goals do you have around implementing tests?

## Additional resources

- [PHPUnit documentation](https://phpunit.de/documentation.html) (phpunit.de)
- [Drupal PHPUnit documentation](https://www.drupal.org/docs/automated-testing/phpunit-in-drupal) (Drupal.org)
- [Drupal testing documentation](https://www.drupal.org/docs/automated-testing) (Drupal.org
- Recommended book: [XUnitPatterns.com](http://xunitpatterns.com/index.html) (xunitpatterns.com)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Software Testing Overview](/tutorial/software-testing-overview?p=3262)

Clear History

Ask Drupalize.Me AI

close