---
title: "Specify the Version of a Composer Package"
url: "https://drupalize.me/tutorial/specify-version-composer-package?p=2467"
guide: "[[command-line-tools-drupal]]"
---

# Specify the Version of a Composer Package

## Content

Composer packages use semantic versioning to allow you to differentiate among different releases of a project. Knowing how this works, and how to specify a version constraint when requiring a Composer package are an important part of using Composer.

In this tutorial we'll:

- Get an overview of semantic versioning
- Look at how Composer version constraints work and related best practices
- Learn how to define Composer package requirements such that you can quickly update all of your application's dependencies without breaking existing functionality

By the end of this tutorial, you should understand how semantic versioning relates to Composer, and how to specify version constraints for packages in your Composer project.

## Goal

Learn the basics about semantic versioning, and best practices for defining Composer version constraints in your *composer.json* file.

## Prerequisites

- [Anatomy of a Composer Project](https://drupalize.me/tutorial/anatomy-composer-project)

## Semantic Versioning (semver)

Sprout Video

[Semantic Versioning](https://semver.org/) is a [specification](https://semver.org/#semantic-versioning-specification-semver), [used by Composer](https://getcomposer.org/doc/articles/versions.md), for "naming" package versions (e.g., 1.0.0, 2.1.2, etc.). The specification enables developers to glance at a package version and confidently determine if upgrading to that version will introduce a bug fix, new features, or (most importantly) a change that is likely to break existing application functionality.

For a bit of context as to why semantic versioning is necessary for a package management tool like Composer, let's look at an excerpt from the [introduction to the Semantic Versioning Specification](https://semver.org/#introduction):

> In the world of software management there exists a dreaded place called “dependency hell.” The bigger your system grows and the more packages you integrate into your software, the more likely you are to find yourself, one day, in this pit of despair.

> In systems with many dependencies, releasing new package versions can quickly become a nightmare. If the dependency specifications are too tight, you are in danger of version lock (the inability to upgrade a package without having to release new versions of every dependent package). If dependencies are specified too loosely, you will inevitably be bitten by version promiscuity (assuming compatibility with more future versions than is reasonable). Dependency hell is where you are when version lock and/or version promiscuity prevent you from easily and safely moving your project forward.

Combined with Composer, semantic versioning enables developers to avoid "dependency hell" and to quickly upgrade all of their application's dependencies without risking breakage. However, to do this effectively, **you must understand and correctly leverage semantic versions and Composer version constraints**.

Let's take a quick look at the specification.

### The specification

A semver version must take the format **x.y.z** where:

- **x** stands for a major version
- **y** stands for a minor version
- **z** stands for a patch

It terms of impact, a change in:

- **x** indicates a **breaking change**
- **y** indicates **new features** without breaking changes
- **z** indicates a **bug fix** without breaking changes

A "breaking change" is a change to a package's public API that will definitely break something in implementing users’ code unless they change their code to adopt it. It is also known as a "backwards incompatible change".

### Examples

#### Major version

Upgrading from **1**.0.0 to **2**.0.0 will break your application because the *public API* for that package has changed. You will need to refactor your application's implementation of the package after updating it. The term "public API" is used loosely by semver and essentially means "the declared/documented way that users implement or use the software".

#### Minor version

Upgrading from 1.**0**.0 to 1.**1**.0 will introduce new features without breaking anything. Typically, a minor release of a package is made when a part of the public API is deprecated (but not removed) or a set of new features is made available. It can also include bug fixes.

#### Patch version

Upgrading from 1.0.**0** to 1.0.**1** will introduce a non-breaking bug fix, like closing a security flaw or correcting the code to match documented behavior.

Of course, this assumes that the package you require actually adheres to the rules of the specification.

## Composer version constraints

Composer's great power comes from its ability to find and choose the right versions of your requirements for you. If you provide Composer with a set of requirements that is too specific, then you lose much of Composer's value.

This is why we use [version constraints](https://getcomposer.org/doc/articles/versions.md) rather than exact versions when defining Composer dependencies.

A version constraint is a string that provides Composer with guidelines for choosing the best version of a given package for your application. It allows you to define a minimum required version or a range of acceptable versions rather than an exact version.

For instance, the version constraint `^1.0.0` tells Composer to download the latest minor version or patch version that is inter-compatible with your other dependencies. In contrast, using the string `1.0.0` tells Composer to download exactly version `1.0.0`, which may lead to "version lock".

Using version constraints for all of your dependencies allows you to provide a set of guidelines for Composer that enables you to manage all of your dependencies easily.

A common set of rules for an application is:

- I won’t accept any breaking changes.
- I will accept new features if they’re not breaking.
- I will accept any fixes if they’re not breaking.

Use the [Packagist Semver Checker](https://semver.madewithlove.com/?package=drupal%2Fcore-recommended&constraint=%5E10.1) to visualize what your version constraints are doing. Example:

Image

![Screenshot of Semver Checker with a drupal/core-recommended:^10.1 constraint shows all drupal version with only those allowed by teh constraint highlighted.](/sites/default/files/styles/max_800w/public/tutorials/images/semver-checker.png?itok=QgOTBBCy)

Let's look at the syntax of Composer version constraints and review the current best practices.

## The best practice

When you run `composer require`, Composer will automatically write to your *composer.json* file and add a new entry to the `require` array in the format `^x.y.z`, where `x.y.z` is the latest stable version of the required package. **This is considered the best practice**.

Using the caret (`^`) with a 3-component version number tells Composer to download the latest stable version *above* `x.y.z` without downloading a new major version. This means that you cannot download a breaking change. It also sets a minimum version requirement, so that a downgrade below `x.y.z` is not possible.

## Cheat sheet

Composer provides *many* ways to define a version constraint. If you'd like a full list of the available options see [Versions and constraints](https://getcomposer.org/doc/articles/versions.md). These overlap significantly with version constraint formats used by other package managers, like [NPM](https://www.npmjs.com/), [Bower](https://bower.io/), etc.

In this section, we provide a brief overview of the most popular version constraint formats.

| Name | Example | Description |
| --- | --- | --- |
| Exact version | `1.0.2` | You can specify the exact version of a package. |
| Caret | `^1.2.3` | Equivalent to `>=1.2.3,<2.0.0`. Downloads latest minor or patch version above specified version. **Preferred**. |
| Tilde | `~1.2` | Equivalent to `>=1.2,<2.0.0`. Specifies a minimum version, but allows the last digit specified to go up. |
| git branch | `dev-master` | Using the prefix `dev` followed by a git branch name like `master` will checkout that branch. |
| Range | `>=1.0,<=1.5` | Specify a range of valid versions and combine multiple ranges with AND and OR operands. |
| Wildcard | `1.0.*` | Equivalent to `>=1.0,<1.1`. Specify a pattern with a \* wildcard. |
| stability tag | `1.0.*@beta` | Override your minimum stability setting for a specific package. |

### The tilde and the caret

Using a tilde `~` was previously the preferred syntax, but not any more. For nuanced information on a tilde/caret comparison, see:

- [Always use caret instead of tilde](https://developer.happyr.com/always-use-caret-instead-of-tilde)
- [Tilde and caret version constraints in Composer](https://blog.madewithlove.be/post/tilde-and-caret-constraints/)

## Drupal.org versions and semver

If you're a Drupal user, you may have noticed that semver versions (8.1.0) look a little different than Drupal.org project versions (8.x-1.0).

You can still use Composer to download projects from Drupal.org using semver versions. [Composer Configuration for Drupal](https://drupalize.me/tutorial/composer-configuration-drupal) will guide you through that step-by-step process, but for now let's just look at version formatting.

The Composer service on Drupal.org translates the contributed project version into a semver format that Composer can understand.

It simply removes Drupal's core version prefix **8.x-**, and adds an extra "0" on the end. For example, **8.x-1.0** would become **1.0.0**.

The major version will be specified elsewhere in your *composer.json* file. (See [Composer Configuration for Drupal](https://drupalize.me/tutorial/composer-configuration-drupal).)

You can use the same transformation to determine the correct version format for any Drupal project. The table below lists a few examples. See [official Drupal.org documentation](https://www.drupal.org/docs/develop/using-composer/using-composer-to-manage-drupal-site-dependencies#specify-version) for more detail.

| Drupal.org format | Translated semver format |
| --- | --- |
| {core.x}-{major}.{minor}-{stability} | {major}.{minor}.0-{stability} |
| 7.x-3.4-beta2 | 3.4.0-beta2 |
| 7.x-2.10-rc2 | 2.10.0-rc2 |
| 7.x-1.0-unstable3 | not available to composer |
| 7.x-1.0-alpha5 | 1.0.0-alpha5 |
| 7.x-0.1-rc2 | 0.1.0-rc2 |
| 7.x-1.x-dev | 1.x-dev |

## Recap

In this tutorial, we learned about the semantic versioning specification, its purpose, and its format. We also learned how to properly use Composer version constraints to properly leverage semver, and how to specify Drupal.org projects in a format that Composer can understand.

## Further your understanding

- What is semantic versioning?
- What is the difference between a major and a minor release?
- What is the preferred version constraint syntax for Composer?
- What are "version lock" and "version promiscuity"?

## Additional resources

- [Semantic Versioning Specification](https://semver.org/) (semver.org)
- [Composer version constraints](https://getcomposer.org/doc/articles/versions.md) (getcomposer.org)
- [NPM Blog: Why use semver](http://blog.npmjs.org/post/162134793605/why-use-semver) (blog.npmjs.org)
- [Using Composer to manage Drupal site dependencies: Specifying a version](https://www.drupal.org/docs/develop/using-composer/using-composer-to-manage-drupal-site-dependencies#specify-version) (Drupal.org)
- [Packagist Semver Checker](https://semver.mwl.be/#!?package=drush%2Fdrush&version=%5E9%20%7C%20%5E10&minimum-stability=RC) (<https://semver.mwl.be>)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Anatomy of a Composer Project](/tutorial/anatomy-composer-project?p=2467)

Next
[Composer Configuration for Drupal](/tutorial/composer-configuration-drupal?p=2467)

Clear History

Ask Drupalize.Me AI

close