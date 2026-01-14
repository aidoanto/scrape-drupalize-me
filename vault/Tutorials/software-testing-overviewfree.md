---
title: "Software Testing Overviewfree"
url: "https://drupalize.me/tutorial/software-testing-overview?p=3262"
guide: "[[test-drupal-sites-automated-tests]]"
order: 2
---

# Software Testing Overviewfree

## Content

This tutorial will clarify some basic ideas about software testing. We'll give some strategies for testing and illustrate types of tests and when and why you'd use them. This document is written with Drupal in mind, but the concepts apply for other development environments you'll encounter as well. The tools will be different, but the ideas apply universally. By the end of this tutorial, you should understand what testing is for and how different types of tests support different purposes and outcomes.

## Goal

Understand why we do software testing and recognize common categories of tests.

## Prerequisites

- None.

## Purpose of testing

Why write tests? What are tests for?

We write tests because we see that it helps us in the future. We write tests on anything: from in-depth, in-house technical requirements, all the way to a need for human-readable tests that you can show a client.

Tests are part of a process. If your development process is set up to demand tests, then you'll write them. Some of the testing strategies listed below almost emphasize tests more than production code.

Some tests fill needs at a very high level, such as client requirements. You know you'll have to prove them to the client, so it's easy to realize you need a test for it.

Or, if your development team is working on system integrations and you don't want future development to introduce regressions, you'd write an integration or functional test to prove that no regression has occurred. This test then makes your life easier when it fails, showing you that there was a regression.

Some styles of testing produce more readily-maintainable code. For instance, if your project includes important behavior in a class, you can adapt this class to be more easily unit-tested. The easier it is to write a unit test for the code, the easier it will be to maintain it over time.

In these examples, the common thread is that the tests make your life easier. Put another way, these tests make it easier to maintain both your expectations about the project, and also maintain the behavior of the code.

## Testing strategies

You don't want to test without a reason. That's because tests themselves are code which must be maintained. Eventually, you'll need to fix tests as you change the code or the expectations.

Therefore it's a good idea to develop an overall testing strategy for the project. The goal of your testing strategy should be to move the project towards quality code that's maintainable.

You can adopt some or all of the following strategies to suit your project.

### Test-driven development

Some teams use a strategy called Test-Driven Development, or TDD. This strategy emphasizes having a test as soon as possible in the development process, often to the point of writing the test first and then writing production code that will make the test pass.

This has the advantage of knowing that the production code works while you're writing it. Another advantage is that you end up with a lot of tests.

### Automated testing

Automated testing means that the tests can be started without a lot of manual interaction.

In an ideal world, all tests can be automated. This way you can allow tests to run and then get a result back without much intervention or expense. This makes it easier to run all the tests as frequently as possible during development.

One advantage of having automated tests is that they'll be repeatable. A test run today should have the same result as a test run tomorrow, all things being equal. Automating tests will remove test runner errors introduced by manual testing.

Having repeatable automated testing instead of manual testing should be a goal for every development team.

### Continuous integration (CI)

An obvious extension of the idea of automated testing is the idea of continuous integration. This is a strategy where changes made to the project automatically trigger a test run and allow you to know as quickly as possible whether the change is acceptable or not.

Examples of useful CI services include [Travis CI](https://www.travis-ci.com/), [CircleCI](https://circleci.com/) and [Bamboo](https://www.atlassian.com/software/bamboo), and also [DrupalCI on drupal.org](https://www.drupal.org/drupalorg/docs/drupal-ci). Organizations with technical know-how can set up their own CI system, as well. These systems will do things like email you if your test build failed. The point is to get feedback as soon as possible on the changes.

**Continuous Delivery**: An extension of the CI idea. Instead of telling you that a change was wrong when the tests fail, the change is always considered good if the tests don't fail. In this strategy, a passing CI build is considered ready to deploy or release.

**Continuous Deployment**: If the continuous delivery strategy tells you that the project *could* be deployed, then the continuous deployment strategy automates the deployment and release based on the passing test build.

These strategies all rely on the quality of the tests themselves. So if you have a continuous deployment process but poor tests, then you might very well end up deploying poor code.

## Types of tests

Let's talk about some basic categories of tests.

The way we think about these categories has more to do with their scope and what type of systems they touch, rather than what specific tool is used to perform them.

This is not an exhaustive list. We'll concentrate on 3 types of test that easily map to Drupal's testing frameworks.

### Behavioral tests

Behavioral tests verify a high-level abstract behavior.

If you can describe the test by saying something like: "If I look at the web site I should see the welcome message," then your test is likely a behavioral test.

Behavioral tests seldom address which specific technologies or configurations are present, and focus on what is happening, or what the user does.

Strictly speaking, Drupal does not have a behavioral test framework. `BrowserTestBase` can be used for these purposes, but the tests themselves end up being tied to specific site configuration, such as which modules are enabled or which theme is being used for display. Tools such as [Behat](https://docs.behat.org/en/latest/) are more suited to this type of testing.

### Functional tests

Functional tests verify interactions between systems or sub-systems.

For instance, if you want to know how your module's code interacts with a specific type of database, then you would write a functional test. In this case, the functional test would not be testing whether the code works or whether the database works, but how the code and database interact.

Functional tests tend to be specific to technology and configuration, but can also be more generalized. They might seem similar to behavioral tests. For instance, if you write a Drupal module that specifies a new permission, you'd also write a test to verify that a user logged-in without that permission can not perform a given task. However, we're not actually testing what the user does, we're testing what the systems do, and whether they limit the abilities of users without that permission.

In Drupal terms, we have two options for functional tests: `BrowserTestBase` and `KernelTestBase`.

- `BrowserTestBase`: Allows you to specify a lot of configuration within the test itself and emphasizes behavior that happens during HTTP requests.
- `KernelTestBase`: Functional tests which do not require nor allow HTTP requests. We can use kernel tests for a more fine-grained test of subsystem interactions without requiring an HTTP output.

### Unit

Strictly speaking, a unit test is a test of the smallest unit of executable code. In PHP that's a method or function. In a less strict sense, unit tests have as few dependencies as possible in order to test expectations about a very limited part of the code.

So if you make a class, you'd write a unit test for each of the methods of that class which you want to be sure has a specific behavior.

Generally, unit tests are there to prove that an atomic-level behavior is correct. In a trivial example, if you have a function named `add()` that adds numbers, you'd write a unit test to test only the behavior of this method and nothing else. Interactions with other systems or configuration would be minimized in order to make sure you're only testing the behavior of the `add()` method.

- `UnitTestCase`: A base class which provides a very thin layer on top of PHPUnit's base class. It gives us a few useful mock helpers and also manages the `\Drupal` pseudo-global for us.
- `KernelTestBase`: Provides some unit-like tests which have dependencies which are difficult or awkward to mock. Generally, though, we'd consider `KernelTestBase` to be more useful for functional tests. The awkward scenarios which can be solved by `KernelTestBase` have more to do with Drupal core's legacy codebase than they do with the test framework.

## Recap

Testing is a part of the development process that should have the goal of making your project more maintainable. Your choice of testing strategies and test types should depend on your goals for maintainability.

## Further your understanding

- What types of changes to your development process would you have to make to be able to support continuous deployment?
- What types of tests will you need to write for your project to test your custom code?

## Additional resources

- [DrupalCI](https://www.drupal.org/drupalorg/docs/drupal-ci) (Drupal.org)
- [Travis CI](https://www.travis-ci.com/) (<https://www.travis-ci.com/>)
- [CircleCI](https://circleci.com/) (circleci.com)
- [Bamboo](https://www.atlassian.com/software/bamboo) (atlassian.com)
- [Behat](https://docs.behat.org/en/latest/) (docs.behat.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Introduction to Testing in Drupal](/tutorial/introduction-testing-drupal?p=3262)

Next
[Frameworks for Testing in Drupal](/tutorial/frameworks-testing-drupal?p=3262)

Clear History

Ask Drupalize.Me AI

close