---
title: "Install Drupal Development Requirements with Composer"
url: "https://drupalize.me/tutorial/install-drupal-development-requirements-composer?p=3262"
guide: "[[test-drupal-sites-automated-tests]]"
---

# Install Drupal Development Requirements with Composer

## Content

In order to run tests, your Drupal site needs additional development requirements installed using Composer.

By default, when you download Drupal as a zip file or tarball, these packages will not be installed, since they're used for development purposes.

In this tutorial, we'll walk through the steps to make sure we've got Composer available. Next we'll install the dependencies. Then we'll talk about why you shouldn't have development dependencies available on your production site. Thankfully, Composer can help make this easy to manage.

## Goal

- Install Composer if it's not already available
- Install Composer-based development requirements for running and developing Drupal tests
- Learn when and how to remove the development requirements

## Prerequisites

- [A Drupal codebase installed locally with Composer](https://drupalize.me/tutorial/install-drupal-locally-ddev). We don't need the site to be fully installed. But make sure it's not a production site.
- Command line access to the system
- Internet access

## Why do we need Composer to install development requirements?

The `drupal/core-recommended` Composer project does not include development dependencies. Neither does the latest version of Drupal that you can [download as a tarball or zip file](https://www.drupal.org/download) from Drupal.org.

Development dependencies include tools for running tests such as PHPUnit. We need to make sure that all the tools we need to run tests are installed.

If you use a Composer-based build process already for your site, some of this may already be familiar to you. But if not, let's take a look at why this is set up this way.

## Why aren't development requirements available?

There's one big reason in particular: *security*. When Composer's *vendor/* directory is stored in the web server's document root, as it is in Drupal by default, it inherits the security problems of any Composer package stored there. This is why non-essential packages are not shipped with the Drupal download tarball. A security issue affecting any one of Drupal's dependencies with code in the vendor directory is an issue that will affect our site and needs to be managed properly. If we can minimize the number of dependencies in our site we minimize the number of potential security issues of this type that might pop up.

Now, let's take a look at how you can get the development requirements installed on a local copy of your site.

### Install Composer on your machine

**Note:** If you're using a [local environment](https://drupalize.me/topic/development-environments) such as DDEV, Composer is available through the `ddev composer` command. You can skip this step.

To install Composer, your machine must already have PHP installed. See [Composer System Requirements](https://getcomposer.org/doc/00-intro.md#system-requirements) for more detail.

Follow the [Composer installation instructions](https://getcomposer.org/doc/00-intro.md#system-requirements) and return here when you’re finished!

If you’re a [Homebrew](https://brew.sh/) user on OSX, you can use `brew install composer`.

For the rest of the tutorial, we'll assume you have Composer installed within the root directory of your Drupal site, and we'll refer to it as `composer`.

### Install `drupal/core-dev`

Now that we have Composer successfully installed, we can use the `require` command to tell Composer to install all the dependencies listed in the `drupal/core-dev` package. This package provides the testing tools we'll need.

```
composer require --dev drupal/core-dev
```

### Verify `phpunit/phpunit` is up-to-date

You should now have all development dependencies installed. Verify this by checking for the existence of the PHPUnit library.

```
composer show phpunit/phpunit
```

You should see a bunch of information about the `phpunit/phpunit` library output to the screen starting with something like this:

```
name     : phpunit/phpunit
descrip. : The PHP Unit Testing framework.
keywords : phpunit, testing, xunit
versions : * 10.5.38
type     : library
...
```

Congratulations! You've installed development dependencies and are ready to set up your test runners.

Wait! Before you move on, let's talk about how `composer install` works with development dependencies in the future.

## How `composer install` handles dev packages

Composer allows projects to put requirements into a special category for development. This allows for specifying development packages, like testing tools.

By default, Composer installs development requirements when you tell it to install dependencies. That means we can issue the [`install`](https://getcomposer.org/doc/03-cli.md#install-i) command, and it will give us the development requirements once we have required the `drupal/core-dev` package.

You can tell Composer to install all the packages, as we did above. Or you can tell Composer to exclude the development packages by adding the `--no-dev` option to the command line.

If you don't, then you probably already had them installed. You can check by asking Composer to show you details about PHPUnit using `composer show phpunit/phpunit`.

If you see info about `phpunit/phpunit` output, your Drupal codebase already includes all the development dependencies and is ready to use tools like PHPUnit.

## Removing development requirements

At some point prior to deploying your code on a production environment, we'll want to remove the development requirements.

Why? First, they're not needed in a production site, so why include them? But more importantly, they represent a significant security concern. (Drupal's security team issued a [security alert related to development requirements](https://www.drupal.org/SA-2017-001) in the tarball package.)

To **remove** dev requirements, we need to tell Composer to `install` with the `--no-dev` flag:

```
composer install --no-dev
```

Composer should tell you that it's removing those packages. It will look something like this:

```
Installing dependencies from lock file
Verifying lock file contents can be installed on current platform.
Package operations: 0 installs, 0 updates, 82 removals
  - Removing webmozart/assert (1.11.0)
  - Removing theseer/tokenizer (1.2.3)
  - Removing tbachert/spi (v1.0.2)
  - Removing symfony/polyfill-php82 (v1.31.0)
  - Removing symfony/polyfill-php80 (v1.31.0)
  - Removing symfony/polyfill-php73 (v1.31.0)
  - Removing symfony/lock (v7.1.6)
  - Removing symfony/dom-crawler (v7.1.6)
  - Removing symfony/css-selector (v7.1.6)
  - Removing symfony/browser-kit (v7.1.6)
  - Removing squizlabs/php_codesniffer (3.10.3)
...
```

Note that you'll still need these packages while you're running tests, or following the testing tutorials.

If you deploy Drupal with the *vendor/* directory in the codebase, then you'll definitely want to have Composer remove the development dependencies. Or if you have an automated deployment that uses Composer, you'll want it to include `--no-dev` in its Composer phase.

You should also remove *composer.phar*, if it exists, from your codebase when you deploy.

## Recap

We learned:

- How to use Composer to install development requirements
- How to uninstall the development requirements for production
- Why we should not have development requirements on our production site

## Further your understanding

What steps will you need to take to ensure that development dependencies are not included when you deploy to a production site? What tools can you utilize to help with this? (e.g. *.gitignore*, scripts, etc.)

## Additional resources

- [Composer documentation](https://getcomposer.org/) (getcomposer.org)
- [Using Composer with Drupal](https://www.drupal.org/docs/develop/using-composer/using-composer-with-drupal) (Drupal.org)
- [What Is Composer?](https://drupalize.me/tutorial/what-composer) (Drupalize.Me)
- [Using Composer to Install Drupal and Manage Dependencies](https://www.drupal.org/docs/develop/using-composer/using-composer-to-install-drupal-and-manage-dependencies) (Drupal.org)
- [Debug any of Drupal's PHPUnit tests in PhpStorm with a DDEV Environment](https://drupalize.me/blog/debug-any-drupals-phpunit-tests-phpstorm-ddev-environment) (Drupalize.Me)
- [Changes required for PHPUnit 10 compatibility](https://www.drupal.org/node/3365413) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Frameworks for Testing in Drupal](/tutorial/frameworks-testing-drupal?p=3262)

Next
[Organize Test Files](/tutorial/organize-test-files?p=3262)

Clear History

Ask Drupalize.Me AI

close