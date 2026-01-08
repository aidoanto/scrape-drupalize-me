---
title: "Troubleshoot Common Composer Issues"
url: "https://drupalize.me/tutorial/troubleshoot-common-composer-issues?p=2467"
guide: "[[command-line-tools-drupal]]"
---

# Troubleshoot Common Composer Issues

## Content

You will inevitably encounter Composer issues that require troubleshooting. This tutorial aims to provide some general troubleshooting advice for common Composer issues.

In this tutorial we'll look at:

- Common issues you'll encounter when using Composer
- Solutions to these common issues

By the end of this tutorial you should have some ideas of how to solve common issues that you might encounter when using Composer to manager your application's dependencies.

## Goal

Learn steps for troubleshooting common Composer issues.

## Prerequisites

- [What Is Composer?](https://drupalize.me/tutorial/what-composer)
- [Anatomy of a Composer Project](https://drupalize.me/tutorial/anatomy-composer-project)
- [Use Composer with Your Drupal Project](https://drupalize.me/tutorial/use-composer-your-drupal-project)

## Common issues

It's Composer's job to inspect the requirements and version constraints in *composer.json* and resolve them into a set of intercompatible dependencies that can be used together. Sometimes, this isn't possible.

Typically, this is due to one of the following reasons:

- Your platform (PHP version) is incompatible with your requirements
- Your application requires two packages that are incompatible with each other
- Your application requires a non-existent/invalid version of a package
- You execute a command that has too narrow a scope

Typically, you will need to do one of the following in order to resolve a dependency conflict:

- Change your system's version of PHP
- Change the version constraint for one or more of your requirements
- Change the command that you're running such that more packages can be updated at once

Below are specific examples.

### Platform requirements

Let's say that your application contains:

```
"require": {
  "phpunit/phpunit": "^7.0.1"
}
```

#### Your PHP version is too low

You have PHP 5.6 on your local machine, and you attempt to update your Composer dependencies via `composer update`.

You'll encounter this error:

```
Your requirements could not be resolved to an installable set of packages.

  Problem 1
    - phpunit/phpunit 7.0.1 requires php ^7.1 -> your PHP version (5.6.31) does not satisfy that requirement.
    - phpunit/phpunit 7.0.1 requires php ^7.1 -> your PHP version (5.6.31) does not satisfy that requirement.
    - Installation request for phpunit/phpunit ^7.0.1 -> satisfiable by phpunit/phpunit[7.0.1].
```

In this case, you need to either change your system's version of PHP to meet the minimum requirements of `phpunit/phpunit`, or else you need to change your version constraint for `phpunit/phpunit` so that a lower version can be installed.

For instance, you can change your `phpunit/phpunit` version constraint to `^5.7.27` since `phpunit/phpunit` 5.\* requires `php: ^5.6 || ^7.0`. You can visit [*phpunit/phpunit*'s page on Packagist](https://packagist.org/packages/phpunit/phpunit#5.7.27) to quickly determine its requirements.

#### Your PHP version is too high

Conversely, you may encounter a situation where your PHP version is too high. Take the following example.

You have PHP 7.1 on your local machine. You update your Composer dependencies via `composer update`. Composer installs package versions that require PHP ^7.1 and writes those versions to *composer.lock*.

A colleague of yours, who has PHP 5.6 locally, pulls down your changes to *composer.lock* and runs `composer install`. They encounter an error! Their PHP version is too low.

Rather than forcing your colleague to upgrade their version of PHP, you can instead instruct Composer to install package versions *as if you were using PHP 5.6* by adding the following to your *composer.json*:

```
    "config": {
        "platform": {
          "php": "5.6"
        }
    },
```

See [Composer's platform config documentation](https://getcomposer.org/doc/06-config.md#platform) for more information.

### Incompatible package versions

You may encounter a dependency conflict because your *composer.json* requires two packages that are incompatible with each other. Let's look at an example.

Your *composer.json* contains:

```
    "require": {
        "phpunit/phpunit": "^7.0.1",
        "phpunit/php-timer": "~1.0"
    }
```

In simplified language, that means that you have declared that your application requires a version of `phpunit/phpunit` that is 7.0.1 or higher, and a version of `phpunit/php-timer` that is less than `2.0.0`.

These requirements cannot be resolved to an installable set of dependencies because `phpunit/phpunit` versions 7.0.1 and higher require a minimum `phpunit/php-timer` version of `2.0`. See [*phpunit/phpunit*'s page on Packagist](https://packagist.org/packages/phpunit/phpunit#7.0.1).

If you execute `composer install` you will encounter the following error:

```
Your requirements could not be resolved to an installable set of packages.

  Problem 1
    - phpunit/phpunit 7.0.1 requires phpunit/php-timer ^2.0 -> satisfiable by phpunit/php-timer[2.0.0, 2.0.x-dev] but these conflict with your requirements or minimum-stability.
    - phpunit/phpunit 7.0.1 requires phpunit/php-timer ^2.0 -> satisfiable by phpunit/php-timer[2.0.0, 2.0.x-dev] but these conflict with your requirements or minimum-stability.
    - Installation request for phpunit/phpunit ^7.0.1 -> satisfiable by phpunit/phpunit[7.0.1].
```

To resolve this issue, you must change one or more of the version constraints in your *composer.json*.
Preferably, you would change your `phpunit/php-timer` version constraint to `^2.0.0` or remove it altogether.

#### Determine which packages are responsible

This is a very simple example. Sometimes, it isn't so easy to identify which package is responsible for a dependency conflict, particularly when the guilty package is a recursive dependency that you may never have explicitly required.

In this case, the `composer why` and `composer why-not` commands may be helpful.

You can run `composer why phpunit/php-timer` to determine why `phpunit/php-timer` is installed (i.e., which packages require it). This is useful when dealing with recursive dependencies and answering the question, "Where does that requirement come from?"

```
$ composer why phpunit/php-timer
__root__         -      requires  phpunit/php-timer (~1.0)
phpunit/phpunit  7.0.1  requires  phpunit/php-timer (^2.0)
```

You can also run `composer why-not phpunit/php-timer 1.0` to determine which packages prevent a `phpunit/php-timer` 1.0 from being installed.

```
$ composer why-not phpunit/php-timer 1.0
phpunit/phpunit  7.0.1  requires  phpunit/php-timer (^2.0)
```

### Command scope is too narrow

Often, it's preferable to update one package at a time. This reduces the change delta per commit and is therefore less risky.

To update a single package, you can run:

```
composer update some/package
```

This *will not* update any of the packages that `some/package` relies on. If the newer version of `some/package-one` requires, say, a new version of `some/package-two`, then the command will not complete successfully. You need to update both `some/package-one` and `some/package-two`.

If you know the specific recursive dependency that needs to be updated, you can specify them both:

```
composer update some/package-one some/package-two
```

It can be a bit annoying to determine exactly which recursive dependencies need to be updated along with `some/package-one`. To simply update `some/package-one` and also all of the packages that it depends on, execute:

```
composer update some/package-one --with-all-dependencies
```

Sometimes, even that is not sufficient. If your *composer.json* requires another `some/package-three` which is incompatible with the new version of `some/package-one` or one of its new dependencies, you can run:

```
composer update
```

This will update all of your packages and all of their dependencies.

## Recap

In this tutorial, we looked at common Composer issues and common troubleshooting steps for resolving them.

## Further your understanding

- What is a platform dependency?
- How can you update only a single package and its recursive dependencies?
- Which commands will help you determine which package(s) are responsible for a conflict?
- What steps should you take to resolve a dependency conflict?

## Additional resources

- [Composer's platform config documentation](https://getcomposer.org/doc/06-config.md#platform) (getcomposer.org)
- [Troubleshooting Composer](https://getcomposer.org/doc/articles/troubleshooting.md) (getcomposer.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Deploy to a Hosting Environment](/tutorial/deploy-hosting-environment?p=2467)

Clear History

Ask Drupalize.Me AI

close