---
title: "Write a Functional Test"
url: "https://drupalize.me/tutorial/write-functional-test?p=3245"
guide: "[[drupal-module-developer-guide]]"
---

# Write a Functional Test

## Content

Functional tests simulate user interactions with Drupal applications, which enables us to test user interfaces and complex workflows. This tutorial guides you through writing functional tests for the *anytown* module, focusing on custom user registration workflow enhancements.

In this tutorial, we'll:

- Examine functional test structure.
- Test `anytown_form_user_register_form_alter()` customizations.
- Discuss the functional test execution environment.

By the end of this tutorial, you'll know how to write functional tests that emulate browser interactions with your Drupal application.

## Goal

Create a functional test to simulate user account registration and verify the "Terms of Service" enforcement.

## Prerequisites

- [Concept: Testing](https://drupalize.me/tutorial/concept-testing)
- [Configure Environment to Run Tests](https://drupalize.me/tutorial/configure-your-environment-run-tests)
- [Alter the User Registration Form](https://drupalize.me/tutorial/alter-user-registration-form)

## Video tutorial

Sprout Video

## What are functional tests?

Functional tests validate application features by simulating user interactions. Unlike code-centric tests, functional tests navigate the site as a user would, ensuring key workflows operate correctly. For critical workflows, functional tests are invaluable, offering comprehensive coverage with minimal code. Functional JavaScript tests extend this by using actual browsers for more in-depth interaction testing.

### The functional test environment

Functional tests provide:

- A complete Drupal environment with a database, service container, and web server.
- Module installation and web browser simulation for test execution.
- Slower execution due to the overhead of initializing a complete Drupal instance.
- Functional JavaScript tests use a full-featured browser suitable for testing JavaScript, images, and other UI elements.

## Testing our custom module

Let's focus on verifying the "Terms of Service" checkbox functionality on the user registration form, a feature we introduced to the *anytown* module in [Alter the User Registration Form](https://drupalize.me/tutorial/alter-user-registration-form). In our test, we'll simulate navigating to the registration page, interacting with the form, and ensuring the workflow behaves as expected.

### Scaffold a new functional test class

Functional tests reside in *tests/src/Functional/* within the module directory, following the `Drupal\Tests\MODULE_NAME\Functional` namespace convention.

Create the file, *tests/src/Functional/UserRegisterFormTest.php*.

### Implement the test

Add the following code to *anytown/tests/src/Functional/UserRegisterFormTest.php*:

```
<?php

namespace Drupal\Tests\anytown\Functional;

use Drupal\Tests\BrowserTestBase;

/**
 * Tests the user registration form alteration for Terms of Service.
 *
 * @group anytown
 * @covers anytown_form_user_register_form_alter()
 */
class UserRegisterFormTest extends BrowserTestBase {

  /**
   * Theme to use for our test.
   *
   * @var string
   */
  protected $defaultTheme = 'stark';

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

    // Change site configuration to allow user registration by visitors
    // without administrator approval.
    $this->config('user.settings')
      ->set('register', 'visitors')
      ->set('verify_mail', FALSE)
      ->save();
  }

  /**
   * Tests the user registration form for Terms of Service field.
   */
  public function testUserRegistrationForm() {
    // Visit the user registration page.
    $this->drupalGet('user/register');

    // Verify the terms of service text is on the page.
    $this->assertSession()->pageTextContains('Anytown Terms and Conditions of Use');
    // And the checkbox is present.
    $this->assertSession()->fieldExists('terms_of_use_checkbox');
    // And that it is not checked.
    $this->assertSession()->checkboxNotChecked('terms_of_use_checkbox');

    // Attempt to submit the form without agreeing to the Terms of Service.
    $edit = [
      'name' => 'testuser',
      'mail' => '[email protected]',
      'pass[pass1]' => 'password',
      'pass[pass2]' => 'password',
      // Do not check 'terms_of_service'.
    ];
    $this->submitForm($edit, 'Create new account');

    // Check that the form cannot be submitted and an error message is
    // displayed.
    $this->assertSession()->pageTextContains('I agree with the terms above field is required.');

    // Submit the form with the 'terms_of_service' checked.
    $edit['terms_of_use_checkbox'] = TRUE;
    $this->submitForm($edit, 'Create new account');

    // Verify the user registration is successful.
    $this->assertSession()->pageTextContains('Registration successful. You are now logged in.');
  }

}
```

This test ensures the "Terms of Service" functionality behaves correctly, from displaying the checkbox to enforcing its validation.

Important things to note in this code:

- We extend `BrowserTestBase` for a browser-like environment.
- The required `$defaultTheme` and `$modules` properties are used when Drupal is installed. For performance, only enable the modules you need.
- The `setUp()` method makes changes to the default configuration to prepare the testing environment.
- The test method (`testUserRegistrationForm()`) uses methods like `$this->drupalGet()` and `$this->submitForm()` to emulate user actions. Then it uses `assertSession()` to make assertions about the content of the page that the simulated browser is currently looking at.

**Tip:** Install a new Drupal site with your module using the *minimal* profile, then keep track of any configuration changes you need to make in order to get the site into the state you need it to be for testing. Complete those steps in your `setUp()` method.

### Verify it works

Run the new tests to confirm they work:

```
./vendor/bin/phpunit -c web/core/ web/modules/custom/anytown/tests/src/Functional/UserRegisterFormTest.php
```

Example output:

```
joe@module-developer-guide-web:/var/www/html$ ./vendor/bin/phpunit -c web/core/ web/modules/custom/anytown/tests/src/Functional/UserRegisterFormTest.php
PHPUnit 9.6.13 by Sebastian Bergmann and contributors.

Testing Drupal\Tests\anytown\Functional\UserRegisterFormTest
.                                                                   1 / 1 (100%)

Time: 00:01.899, Memory: 4.00 MB

OK (1 test, 9 assertions)

HTML output was generated
https://module-developer-guide.ddev.site/sites/simpletest/browser_output/Drupal_Tests_anytown_Functional_UserRegisterFormTest-21-10386313.html
https://module-developer-guide.ddev.site/sites/simpletest/browser_output/Drupal_Tests_anytown_Functional_UserRegisterFormTest-22-10386313.html
https://module-developer-guide.ddev.site/sites/simpletest/browser_output/Drupal_Tests_anytown_Functional_UserRegisterFormTest-23-10386313.html
https://module-developer-guide.ddev.site/sites/simpletest/browser_output/Drupal_Tests_anytown_Functional_UserRegisterFormTest-24-10386313.html
https://module-developer-guide.ddev.site/sites/simpletest/browser_output/Drupal_Tests_anytown_Functional_UserRegisterFormTest-25-10386313.html
```

If you've configured the PHPUnit `BROWSERTEST_OUTPUT_DIRECTORY` setting the test runner will save a snapshot of each page the simulated browser visits and provide a list of them. Viewing the page in a browser will show you what the test browser sees, and can be helpful in debugging.

Example:

Image

![Screenshot shows functional test browser output](/sites/default/files/styles/max_800w/public/tutorials/images/testing--functional-tests_browser-output-example.png?itok=E-CBRA9j)

## Recap

Functional tests mimic user interactions within a full Drupal environment, providing a powerful tool for validating user-facing features. Through a functional test, we confirmed the effectiveness of "Terms of Service" enforcement in user registration, demonstrating how a functional test can safeguard a critical user interaction.

## Further your understanding

- How might you convert this test into a Functional JavaScript test for execution in an actual browser?
- Explore testing other module features with functional tests. What benefits do they offer over unit or kernel tests?
- Consider testing the username validation constraint with a functional test. How does this compare to kernel testing?

## Additional resources

- [Set up a Functional Test](https://drupalize.me/tutorial/set-functional-test) (Drupalize.Me)
- [Implement a Functional Test](https://drupalize.me/tutorial/implement-functional-test) (Drupalize.Me)
- [Implement Drupal Functional Test Dependencies](https://drupalize.me/tutorial/implement-drupal-functional-test-dependencies) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Write a Kernel Test](/tutorial/write-kernel-test?p=3245)

Clear History

Ask Drupalize.Me AI

close