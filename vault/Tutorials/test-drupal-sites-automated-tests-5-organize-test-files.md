---
title: "Organize Test Files"
url: "https://drupalize.me/tutorial/organize-test-files?p=3262"
guide: "[[test-drupal-sites-automated-tests]]"
order: 5
---

# Organize Test Files

## Content

In order for Drupal to be able to locate and run the tests you create, the files need to be put in the correct place. In this tutorial, we'll take a look at the different types of test frameworks that are included along with core. We'll also see how Drupal expects our test files to be organized so that the test runners can find them.

## Goal

Learn how to organize test files so the test runners can locate them.

## Prerequisites

- The Drupal codebase to browse through. You can get it from [the Drupal.org download page](https://www.drupal.org/download) or browse through it [on the web](https://git.drupalcode.org/project/drupal).
- Understand how [PSR-4](https://drupalize.me/blog/201408/preparing-drupal-8-psr-4-autoloading) works to autoload classes.
- [Introduction to Testing in Drupal](https://drupalize.me/tutorial/introduction-testing-drupal)
- [Software Testing Overview](https://drupalize.me/tutorial/software-testing-overview)
- [Frameworks for Testing in Drupal](https://drupalize.me/tutorial/frameworks-testing-drupal)

## Why organize test files?

Drupal includes [4 testing frameworks](https://drupalize.me/tutorial/frameworks-testing-drupal). Each one has a different set of dependencies and serves a different purpose. Drupal's tests have a few other guiding principles to keep in mind as well, including:

- Autoload as few classes as possible
- Ensure each test runs in isolation

In order to make all that happen, we have to organize where the tests are so that Drupal can find them and run them with the appropriate testing framework.

## Test file organization

The test runners will try to find your test code by looking in certain places in the file system depending on the type of test.

A full complement of tests is organized in a directory structure like this:

```
module_name/
  tests/
    modules/
      mock_module/
        mock_module.info.yml
    src/
      Functional/
        PleaseConvertYourSimpletestHereTest.php
      FunctionalJavascript/
        FunctionalJavascriptTest.php
      Kernel/
        KernelTest.php
      Unit/
        Plugin/
          MyPlugin/
            MyPluginTest.php
        UsedOnlyByUnitTestsTrait.php
      Traits/
        UsedByAllTestTypesTrait.php
```

These directories will map to namespaces like this:

| Type | Module Directory | Namespace |
| --- | --- | --- |
| unit | *tests/src/Unit/* | `Drupal\Tests\module_name\Unit` |
| kernel | *tests/src/Kernel/* | `Drupal\Tests\module_name\Kernel` |
| functional | *tests/src/Functional/* | `Drupal\Tests\module_name\Functional` |
| functional | *tests/src/FunctionalJavascript/* | `Drupal\Tests\module_name\FunctionalJavascript` |
| Traits | *tests/src/Traits/* | `Drupal\Tests\module_name\Traits` |

Read on to learn more about each type of test and how it should be organized.

## Test files directory structure

All tests should follow a pattern of: *module\_name/tests/src/[framework\_name]/YourTest.php*. This maps to a [PSR-4-style class name](https://drupalize.me/blog/201408/preparing-drupal-8-psr-4-autoloading) of `\Drupal\Tests\module_name\[framework_name]\YourTest`.

For example, a functional test would be *module\_name/tests/src/Functional/YourTest.php* and have a name of `\Drupal\Tests\module_name\Functional\YourTest`.

Image

![Image of a file directory for Functional tests](../assets/images/frameworks-organizing-functional.jpg)

## Traits

[Traits](https://www.php.net/manual/en/language.oop5.traits.php) are a PHP feature that are sort of like an extra subclass, except they exist outside of the class hierarchy. This makes them useful for adding behavior to, and reusing code across, all the different test types. If you wanted to have a special set of mocks for all your different types of tests, you could implement that as a trait and use the trait in all of your tests.

If you're not already familiar with traits, they are a method of reusing code across your project. You can learn more about traits [in this blog post](https://drupalize.me/blog/201503/dependency-injection-traits-drupal-8) or this [video tutorial](https://drupalize.me/videos/traits-horizontal-reuse?p=2696).

When Drupal's test suite loader goes about discovering these tests, it looks for those framework-based directory names. It won't allow autoloading of any test classes outside of those directories, with one exception: traits.

So in addition to directories such as `Functional/` and `Kernel/`, we can add a `Traits/` directory where test traits are located.

*module\_name/Traits/MyTrait.php* which would map to a namespace like this: `Drupal\Tests\module_name\Traits\MyTrait`

If you need to use a trait across different testing frameworks, it should go into *module\_name/tests/src/Traits/YourTrait.php* This maps to a PSR-4-style name of `\Drupal\Tests\module_name\Traits\YourTrait`.

## Example: CKEditor test file organization

Let's take a look at the CKEditor module included in Drupal's *core/modules* directory. This module is a good example because it has tests written in each of the frameworks (with the exception of Simpletest).

Here is CKEditor module's directory structure (inside *core/modules*):

```
tree ckeditor/tests/src/
ckeditor/tests/src/
├── Functional
│   ├── CKEditorAdminTest.php
│   ├── CKEditorLoadingTest.php
│   ├── CKEditorStylesComboAdminTest.php
│   └── CKEditorToolbarButtonTest.php
├── FunctionalJavascript
│   ├── AjaxCssTest.php
│   └── CKEditorIntegrationTest.php
├── Kernel
│   └── Plugin
│       └── CKEditorPlugin
│           └── InternalTest.php
└── Unit
    ├── CKEditorPluginManagerTest.php
    └── Plugin
        └── CKEditorPlugin
            └── LanguageTest.php

8 directories, 9 files
```

You'll see that for the PHPUnit-based tests, under *ckeditor/tests/src*, the tests are first organized by the framework they run under: *Functional*, *FunctionalJavascript*, *Kernel*, and *Unit*. Under that, they are generally organized by the namespace of the thing being tested or by topic.

Unit and kernel tests are organized by the namespace of the class they're testing. So a unit test of a class named `Drupal\module\Category\Item` would be in a file like *tests/src/Unit/Category/ItemTest.php*.

You will need to emulate this pattern of test file organization in your own module if you want Drupal to be able to automatically discover your tests.

## Directories + PSR-4 = namespaces

The directories that we saw in the CKEditor module example above map to [PSR-4-style](http://www.php-fig.org/psr/psr-4/) namespaces. For example, the following path:

*module\_name/tests/src/Kernel/Plugin/ModulePlugin/PluginTest.php*

...maps to the namespace:

`Drupal\Tests\module_name\Kernel\Plugin\ModulePlugin\PluginTest`

What is a PSR-4 namespace? It means that the autoloader will assume that a file directory has a namespace prefix. So when the autoloader needs to figure out where to find a class with that prefix, it knows to look in that directory.

For instance, if the autoloader needs to find a class named `Drupal\Tests\module_name\Unit\Namespace\SuperAwesomeTest`, it will know that the `Drupal\Tests\module_name` part maps to the `module_name/tests/src/` path. Then it will check if `Unit/Namespace/SuperAwesomeTest.php` exists in that directory. If it does, it will be loaded.

You could also use this handy chart, which illustrates the PSR-4 prefixes for the test framework namespaces. Substitute your module name for *module\_name*.

| Suite | Directory (inside `module_name`) | Namespace |
| --- | --- | --- |
| unit | *tests/src/Unit/* | `Drupal\Tests\module_name\Unit` |
| kernel | *tests/src/Kernel/* | `Drupal\Tests\module_name\Kernel` |
| functional | *tests/src/Functional/* | `Drupal\Tests\module_name\Functional` |
| functional | *tests/src/FunctionalJavascript/* | `Drupal\Tests\module_name\FunctionalJavascript` |

## Mock module organization

Some tests need to enable mock modules. For instance, in core, the [System module has lots of these](https://git.drupalcode.org/project/drupal/-/tree/8.4.x/core/modules/system/tests/modules). They're enabled by Simpletest, functional, or kernel tests in order to test integrations of various APIs. As an example, [action\_test](https://git.drupalcode.org/project/drupal/-/tree/8.4.x/core/modules/system/tests/modules/action_test) implements some Action plugins. Tests can then enable this module and get a known behavior from the mock module's implementation without all of the side-effects and overhead of using the Action module.

The standard place to put mock modules is in *module\_name/tests/modules/test\_module\_name/*. You can find all of the System test mock modules in a similarly named directory, waiting to be enabled by tests.

If your module needs a mock module for testing, you need to do two things:

1. Put your mock module in *tests/modules/mock\_module*.
2. Make sure your *module\_name.info.yml* file belongs to the Testing package by including the line `package: Testing` in its info file.

For example, here's what the *core/modules/system/tests/modules/action\_test/action\_test.info.yml* looks like:

```
name: 'Action test'
type: module
description: 'Support module for action testing.'
package: Testing
version: VERSION
core_version_requirement: ^8 || ^9 || ^10
```

Setting the `package` key to `Testing` ensures that it won't be shown to the user on the module admin page and accidentally enabled by mistake.

## Recap

A full complement of tests is organized in a directory structure like this:

```
module_name/
  tests/
    modules/
      mock_module/
        mock_module.info.yml
    src/
      Functional/
        PleaseConvertYourSimpletestHereTest.php
      FunctionalJavascript/
        FunctionalJavascriptTest.php
      Kernel/
        KernelTest.php
      Unit/
        Plugin/
          MyPlugin/
            MyPluginTest.php
        UsedOnlyByUnitTestsTrait.php
      Traits/
        UsedByAllTestTypesTrait.php
```

These directories will map to namespaces like this:

| Type | Module Directory | Namespace |
| --- | --- | --- |
| unit | *tests/src/Unit/* | `Drupal\Tests\module_name\Unit` |
| kernel | *tests/src/Kernel/* | `Drupal\Tests\module_name\Kernel` |
| functional | *tests/src/Functional/* | `Drupal\Tests\module_name\Functional` |
| functional | *tests/src/FunctionalJavascript/* | `Drupal\Tests\module_name\FunctionalJavascript` |
| Traits | *tests/src/Traits/* | `Drupal\Tests\module_name\Traits` |

## Further your understanding

- Practice organizing a functional test suite in the tutorial, [Set up a Functional Test in Drupal](https://drupalize.me/tutorial/set-functional-test) tutorial.
- Learn how to convert Simpletests in [Convert Tests from Simpletest to PHPUnit](https://drupalize.me/tutorial/convert-tests-simpletest-phpunit).

## Additional resources

- [Preparing for Drupal 8: PSR-4 Autoloading](https://drupalize.me/blog/201408/preparing-drupal-8-psr-4-autoloading) (Drupalize.Me)
- [A Peek at Traits in Drupal 8](https://drupalize.me/blog/201503/dependency-injection-traits-drupal-8) (Drupalize.Me)
- [PHPUnit in Drupal](https://www.drupal.org/docs/automated-testing/phpunit-in-drupal) (Drupal.org)
- [Automated testing (guide)](https://www.drupal.org/docs/develop/automated-testing) (Drupal.org)
- [Change record about defining test suites and trait behavior](https://www.drupal.org/node/2799437) (Drupal.org)
- [Change record: Organizing tests](https://www.drupal.org/node/1543796) (Drupal.org)

### Testing examples in Examples for Developers

- [Testing Example](https://git.drupalcode.org/project/examples/-/tree/3.x/modules/testing_example) (drupalcode.org)
- [PHPUnit Example](https://git.drupalcode.org/project/examples/-/tree/3.x/modules/phpunit_example) (drupalcode.org)
- [Simpletest Example](http://cgit.drupalcode.org/examples/tree/simpletest_example) (drupalcode.org)
- Full [Examples for Developers Project](https://www.drupal.org/project/examples) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Install Drupal Development Requirements with Composer](/tutorial/install-drupal-development-requirements-composer?p=3262)

Next
[Create a PHPUnit Config File for Your Project](/tutorial/create-phpunit-config-file-your-project?p=3262)

Clear History

Ask Drupalize.Me AI

close