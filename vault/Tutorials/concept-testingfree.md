---
title: "Concept: Testingfree"
url: "https://drupalize.me/tutorial/concept-testing?p=3245"
guide: "[[drupal-module-developer-guide]]"
order: 71
---

# Concept: Testingfree

## Content

Testing ensures that code remains reliable and functional. This tutorial introduces the primary types of tests in Drupal: Unit, Kernel, Functional, and FunctionalJavascript -- all executed via PHPUnit. We'll clarify the differences between each type of test and appropriate use cases. As module developers, understanding what to test and how to write tests is vital for robust and maintainable code.

In this tutorial, we'll:

- Identify the primary test types in Drupal and their use cases.
- Emphasize the importance of functional tests in custom module development.
- Introduce the basics of authoring tests in a custom module.

By the end of this tutorial, you should recognize the different types of tests Drupal uses and when and how to use each kind.

## Goal

Understand how testing works in Drupal.

## Prerequisites

- None.

## What do we mean by "tests"?

Tests are code that validate the functionality of some other code. Essential in software development, including Drupal module development, testing verifies your code works as expected and guards against future regressions. Drupal supports several test types, each designed for specific testing scopes and purposes.

### Drupal's use of PHPUnit

Drupal employs [PHPUnit](https://phpunit.de/) for its test suite, which provides a consistent testing framework. PHPUnit is used to write and run tests in Drupal. It's widely used in other PHP frameworks as well. To use it in a Drupal site, ensure that the Composer package `drupal/core-dev` is installed, which contains testing dependencies including PHPUnit. Tests run in isolation, requiring each test to set up its environment.

Learn more in [Configure Your Environment to Run Tests](https://drupalize.me/tutorial/configure-your-environment-run-tests).

## Types of tests

Modules in Drupal can use *unit*, *kernel*, and *functional* tests. The choice of test type depends on the code aspect you're testing and how much of the Drupal system is needed to test that code. While many modules will include more than one type of test, functional tests are the most common for custom application-specific modules. Here's a brief overview:

## Unit tests

Test functions or methods in isolation.

- **Use when**: Testing small parts of code, such as utility functions or specific algorithms, without needing Drupal's API or database.
- **How**: Use PHPUnit and mock dependencies as necessary.
- **Use case**: Testing methods in the `ForecastClient` class to ensure accurate data processing without network requests.

Learn more in [Write a Unit Test](https://drupalize.me/tutorial/write-unit-test).

## Kernel tests

Test module integration with Drupal core subsystems in a lighter environment than a full Drupal bootstrap. Kernel tests are faster than functional tests but slower than unit tests.

- **Use when**: Your module interacts with Drupal core systems like databases or entities but doesn't require the entire stack.
- **How**: Extend `KernelTestBase`.
- **Use case**: Testing database interactions, entity loading, and modifications that your module performs.

Learn more in [Write a Kernel Test](https://drupalize.me/tutorial/write-kernel-test).

## Functional tests and FunctionalJavascript tests

Functional tests test modules in a complete Drupal environment. They simulate a user browsing the website. These provide a full Drupal environment and browser interaction capabilities but are the slowest types of tests.

- **Use when**: Testing user-facing functionalities like form submissions or page rendering.
- **How**: Extend `BrowserTestBase` or `WebDriverTestBase`.
- **Use case**: Testing a form provided by your module, including user feedback and validation.

Learn more in [Write a Functional Test](https://drupalize.me/tutorial/write-functional-test).

## Where to start?

- Begin with unit tests for quick, isolated tests focusing on testing parts of logic-heavy code.
- Use kernel tests for Drupal core interaction without a full site.
- Apply functional tests for comprehensive testing of user interfaces and experiences.

In this chapter, we'll walk through examples of the main test types in Drupal. You should also take the time to look at other examples to familiarize yourself with best practices for organizing tests, figuring out what to test, and seeing testing of various aspects of Drupal's code in action. Drupal core contains thousands of tests, and provides a wealth of examples to learn (and copy) from.

## Organizing your tests

There's a relationship between the location of test files within the file structure, the namespace they use, and the class which they extend. This provides context about the *type* of test, and what additional steps the test runner needs to take in order to prepare the environment in which the test cases are executed.

Place your tests in the *tests/* subdirectory of your module, with subdirectories for each type:

| Type | Module directory | Namespace |
| --- | --- | --- |
| Unit | *tests/src/Unit/* | `Drupal\Tests\module_name\Unit` |
| Kernel | *tests/src/Kernel/* | `Drupal\Tests\module_name\Kernel` |
| Functional | *tests/src/Functional/* | `Drupal\Tests\module_name\Functional` |
| FunctionalJavascript | *tests/src/FunctionalJavascript/* | `Drupal\Tests\module_name\FunctionalJavascript` |
| Traits | *tests/src/Traits/* | `Drupal\Tests\module_name\Traits` |

## What to test?

When writing tests for custom modules, it can help to remember why we write tests: to be confident that our site will work when it is used. With that in mind, it helps to think less about the code that you are testing and more about the use case that it is supporting. If you're only going to write a few tests focus on functional tests that simulate using the application in the way a user would. These tests might not tell you exactly what is broken in the same way a unit test will, but they'll at least surface the fact that something is broken.

Considering the code we've written in this guide, we could test:

- Alterations to the user registration form.
- The impact of user-provided settings on `WeatherPage` controller output.
- Custom username validation logic.
- Unit test for `\Drupal\anytown\ForecastClient::kelvinToFahrenheit`.
- Kernel tests for `\Drupal\anytown\ForecastClient::getForecastData`.

## PHPUnit tests vs. end-to-end tests

The PHPUnit tests in a custom module test that module's functionality independent of your specific Drupal application. When the tests are run, an empty Drupal site with no existing content or configuration is created. Your tests need to set up all the different content and configuration scenarios you want to test.

End-to-End (E2E) testing is the practice of testing the functionality of your entire software stack. E2E testing uses tools that simulate real users interacting with real data on your site. For example, testing the process of a user going through the checkout workflow of your site. You can explore [Drupal Test Traits](https://gitlab.com/weitzman/drupal-test-traits), [Behat](https://behat.org), and [Cypress](https://cypress.io) as possible solutions for E2E testing.

## Recap

In this tutorial, we explored Drupal's use of PHPUnit for unit, kernel, and functional tests. We discussed organizing tests within a module and how testing can enhance an application's reliability.

## Further your understanding

- What are the use cases for each test type?
- How does End-to-End (E2E) testing differ from the PHPUnit tests we discussed?
- Try using (and learning from) ChatGPT or another LLM to generate tests for your code.

## Additional resources

- [Software Testing Overview](https://drupalize.me/tutorial/software-testing-overview) (Drupalize.Me)
- [PHPUnit in Drupal](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal) (Drupal.org)
- Examples for Developers: [testing\_example](https://git.drupalcode.org/project/examples/-/tree/4.0.x/modules/testing_example?ref_type=heads) (git.drupalcode.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Configure Your Environment to Run Tests](/tutorial/configure-your-environment-run-tests?p=3245)

Clear History

Ask Drupalize.Me AI

close