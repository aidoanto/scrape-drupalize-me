---
title: "Create a PHPUnit Config File for Your Project"
url: "https://drupalize.me/tutorial/create-phpunit-config-file-your-project?p=3262"
guide: "[[test-drupal-sites-automated-tests]]"
order: 6
---

# Create a PHPUnit Config File for Your Project

## Content

When running tests with PHPUnit we need to specify a *phpunit.xml* file that contains the configuration that we want to use. Often times (and in much of the existing documentation) the recommendation is to copy the *core/phpunit.xml.dist* file to *core/phpunit.xml* and make your changes there. And this works fine, until something like a `composer install` or `composer update` ends up deleting your modified file. Instead, you should copy the file to a different location in your project and commit it to your version control repository.

In this tutorial we'll:

- Learn how to move, and modify, the *phpunit.xml.dist* file provided by Drupal core
- Understand the benefits of doing so
- Demonstrate how to run `phpunit` with an alternative configuration file

By the end of this tutorial you should be able to commit your *phpunit.xml* configuration file to your project's Git repository and ensure it doesn't get accidentally deleted.

## Goal

Create a *phpunit.xml* configuration file for your project that will not get erased every time `drupal/core` gets updated.

## Prerequisites

- [Run Drupal Tests with PHPUnit](https://drupalize.me/tutorial/run-drupal-tests-phpunit)

## Run PHPUnit with a configuration file

When executing `phpunit` the `-c` flag can be used to specify the location of an XML configuration file or a directory that contains either a *phpunit.xml* or *phpunit.xml.dist* file (in that order).

Most times when you see documentation about running PHPUnit tests for Drupal core you'll see the command executed like so: `phpunit -c core/ {args}`. This will use the configuration file *core/phpunit.xml.dist*, or if you've copied that and modified it, the *core/phpunit.xml* file. Knowing this, we can copy that file to a different location so that it'll get committed to our repo, and then change it.

### Copy the existing *phpunit.xml.dist* file

In a typical Drupal project you might have a repository with the following layout, with Drupal installed in the *web/* directory:

```
.
├── composer.json
├── composer.lock
├── drush
├── vendor
└── web
    ├── core
        ├── phpunit.xml.dist
```

Start by copying the existing *web/core/phpunit.xml.dist* file do a different location in your repo. We frequently put ours in the project root directory like so:

```
.
├── composer.json
├── composer.lock
├── drush
├── phpunit.xml.dist
├── vendor
└── web
```

### Update the relative paths in the configuration file

Open the copied *phpunit.xml* file and update it so that all the relative paths point the appropriate locations. In our case this will mean adding `./web/core/` to most of the existing paths.

Copy of the *phpunit.xml.dist* file from core with paths updated:

```
<?xml version="1.0" encoding="UTF-8"?>

<!-- TODO set checkForUnintentionallyCoveredCode="true" once https://www.drupal.org/node/2626832 is resolved. -->
<!-- PHPUnit expects functional tests to be run with either a privileged user
 or your current system user. See core/tests/README.md and
 https://www.drupal.org/node/2116263 for details.
-->
<phpunit bootstrap="./web/core/tests/bootstrap.php" colors="true"
         beStrictAboutTestsThatDoNotTestAnything="true"
         beStrictAboutOutputDuringTests="true"
         beStrictAboutChangesToGlobalState="true"
         printerClass="\Drupal\Tests\Listeners\HtmlOutputPrinter">
  <php>
    <!-- Set error reporting to E_ALL. -->
    <ini name="error_reporting" value="32767"/>
    <!-- Do not limit the amount of memory tests take to run. -->
    <ini name="memory_limit" value="-1"/>
    <!-- Example SIMPLETEST_BASE_URL value: http://localhost -->
    <env name="SIMPLETEST_BASE_URL" value=""/>
    <!-- Example SIMPLETEST_DB value: mysql://username:password@localhost/databasename#table_prefix -->
    <env name="SIMPLETEST_DB" value=""/>
    <!-- Example BROWSERTEST_OUTPUT_DIRECTORY value: /path/to/webroot/sites/simpletest/browser_output -->
    <env name="BROWSERTEST_OUTPUT_DIRECTORY" value=""/>
    <!-- To have browsertest output use an alternative base URL. For example if
     SIMPLETEST_BASE_URL is an internal DDEV URL, you can set this to the
     external DDev URL so you can follow the links directly.
    -->
    <env name="BROWSERTEST_OUTPUT_BASE_URL" value=""/>
    <!-- To disable deprecation testing completely uncomment the next line. -->
    <!-- <env name="SYMFONY_DEPRECATIONS_HELPER" value="disabled"/> -->
    <!-- Example for changing the driver class for mink tests MINK_DRIVER_CLASS value: 'Drupal\FunctionalJavascriptTests\DrupalSelenium2Driver' -->
    <env name="MINK_DRIVER_CLASS" value=''/>
    <!-- Example for changing the driver args to mink tests MINK_DRIVER_ARGS value: '["http://127.0.0.1:8510"]' -->
    <env name="MINK_DRIVER_ARGS" value=''/>
    <!-- Example for changing the driver args to phantomjs tests MINK_DRIVER_ARGS_PHANTOMJS value: '["http://127.0.0.1:8510"]' -->
    <env name="MINK_DRIVER_ARGS_PHANTOMJS" value=''/>
    <!-- Example for changing the driver args to webdriver tests MINK_DRIVER_ARGS_WEBDRIVER value: '["chrome", { "chromeOptions": { "w3c": false } }, "http://localhost:4444/wd/hub"]' For using the Firefox browser, replace "chrome" with "firefox" -->
    <env name="MINK_DRIVER_ARGS_WEBDRIVER" value=''/>
  </php>
  <testsuites>
    <testsuite name="unit">
      <file>./web/core/tests/TestSuites/UnitTestSuite.php</file>
    </testsuite>
    <testsuite name="kernel">
      <file>./web/core/tests/TestSuites/KernelTestSuite.php</file>
    </testsuite>
    <testsuite name="functional">
      <file>./web/core/tests/TestSuites/FunctionalTestSuite.php</file>
    </testsuite>
    <testsuite name="functional-javascript">
      <file>./web/core/tests/TestSuites/FunctionalJavascriptTestSuite.php</file>
    </testsuite>
    <testsuite name="build">
      <file>./web/core/tests/TestSuites/BuildTestSuite.php</file>
    </testsuite>
  </testsuites>
  <listeners>
    <listener class="\Drupal\Tests\Listeners\DrupalListener">
    </listener>
    <!-- The Symfony deprecation listener has to come after the Drupal listener -->
    <listener class="Symfony\Bridge\PhpUnit\SymfonyTestsListener">
    </listener>
  </listeners>
  <!-- Filter for coverage reports. -->
  <filter>
    <whitelist>
      <directory>./web/core/includes</directory>
      <directory>./web/core/lib</directory>
      <!-- Extensions can have their own test directories, so exclude those. -->
      <directory>./web/core/modules</directory>
      <exclude>
        <directory>./web/core/modules/*/src/Tests</directory>
        <directory>./web/core/modules/*/tests</directory>
      </exclude>
      <directory>./web/modules</directory>
      <exclude>
        <directory>./web/modules/*/src/Tests</directory>
        <directory>./web/modules/*/tests</directory>
        <directory>./web/modules/*/*/src/Tests</directory>
        <directory>./web/modules/*/*/tests</directory>
      </exclude>
      <directory>./web/sites</directory>
     </whitelist>
  </filter>
</phpunit>
```

The important thing here is that these paths in the `bootstrap`, `<testsuites>`, and `<filter>` sections of the *phpunit.xml* file are relative to the file itself. You'll need to update them, so they still point to the correct locations.

### Commit the new configuration file

You can now commit the new *phpunit.xml.dist* configuration file to your project. And share it with everyone on your team.

This is useful if you use standardized development environments like DDEV or others based on Docker where the configuration in the file can be specific to the development environment and work without modifications for everyone.

This also still allows individuals to override their local configuration by copying the file to */phpunit.xml* and making the changes they need.

Now, when you run `phpunit` use the `-c` flag to specify the configuration file itself, or the directory that contains it.

## PHPUnit 10 configuration options have changed

From [Changes required for PHPUnit 10 compatibility](https://www.drupal.org/node/3365413):

The schema of *phpunit.xml* has changed between PHPUnit 9 and PHPUnit 10. If you had a custom *phpunit.xml* you need to run `vendor/bin/phpunit --migrate-configuration` to automatically upgrade your configuration.

If you are developing for both Drupal 10 and 11, in some cases it may be easier to use the default *phpunit.xml.dist* configuration file provided by core and override settings via environment variables, which avoids switching configurations or maintaining 2 custom *phpunit.xml* files.

## Recap

In this tutorial we copied the default *phpunit.xml.dist* configuration file from Drupal core into our project repository and made changes to it so that it'll still work. This allows us to commit the file to the repo and not have to worry about it getting accidentally deleted or updated when `drupal/core` gets updated.

## Further your understanding

- What other project specific modifications could you make to the *phpunit.xml.dist* file to make it easier for you and your team to execute tests?
- How does this effect, and potentially benefit, CI/CD workflows?

## Additional resources

- [PHPUnit configuration file documentation](https://phpunit.readthedocs.io/en/9.5/configuration.html) (phpunit.readthedocs.io)
- [Debug any of Drupal's PHPUnit tests in PhpStorm with a DDEV Environment](https://drupalize.me/blog/debug-any-drupals-phpunit-tests-phpstorm-ddev-environment) (Drupalize.Me)
- [Changes required for PHPUnit 10 compatibility](https://www.drupal.org/node/3365413) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Organize Test Files](/tutorial/organize-test-files?p=3262)

Clear History

Ask Drupalize.Me AI

close