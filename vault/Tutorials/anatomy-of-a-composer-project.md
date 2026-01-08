---
title: "Anatomy of a Composer Project"
url: "https://drupalize.me/tutorial/anatomy-composer-project?p=2467"
guide: "[[command-line-tools-drupal]]"
---

# Anatomy of a Composer Project

## Content

Every Composer project is made up of a few standard files and directories. This tutorial provides an overview of the anatomy of a Composer project, and the essential files and directories used by Composer, including:

- What are *composer.json* and *composer.lock* files?
- What is in a *composer.json* file?
- What is the */vendor* directory?

By the end of this tutorial you should be able to recognize the standard files and directories in a Composer project and know what they are each used for.

## Goal

Learn the anatomy of a Composer-managed application.

## Prerequisites

- [What Is Composer?](https://drupalize.me/tutorial/what-composer)

## The *composer.json* file

The *composer.json* file is the most important Composer file in your project. It contains a JSON array that defines your project's metadata, requirements, and configuration.

The placement of this file is very important. In most cases, it should live in your project's root (top-most) directory. Its location dictates the placement of all other Composer files.

When you execute Composer commands, you should execute them inside the directory that contains *composer.json*. In other words, your [working directory](http://www.linfo.org/current_directory.html) should contain your project's *composer.json* file.

Let's look at the most commonly used keys in the [*composer.json* schema](https://getcomposer.org/doc/04-schema.md).

### `require`

This key contains an array of the packages required for your application to run in a production environment. *It should not include any development tools* (see `require-dev`). Values are defined in the form `"[vendor]/[package-name]": "[version constraint]"`. For instance:

```
    "require": {
        "monolog/monolog": "^1.23"
    }
```

For more information on version constraints, see [Specify the Version of a Composer Package](https://drupalize.me/tutorial/specify-version-composer-package).

These dependencies are installed when you execute `composer install`.

### `require-dev`

This key contains an array of the packages required to develop (build, validate, debug, test, etc.) your application. *It should not include any packages required in production* (see `require`). Values are defined in the form `"[vendor]/[package-name]": "[version constraint]"`. For instance:

```
    "require-dev": {
        "phpunit/phpunit": "^5"
    }
```

For more information on version constraints, see [Specify the Version of a Composer Package](https://drupalize.me/tutorial/specify-version-composer-package).

These dependencies are installed when you execute `composer install`, but they are **not** installed when you execute `composer install --no-dev`. See [Deploy to a Hosting Environment](https://drupalize.me/tutorial/deploy-hosting-environment) for more information on excluding development tools.

### `repositories`

By default Composer just uses the [Packagist repository](https://packagist.org/) to search for the packages defined in `require` and `require-dev`. By specifying `repositories` you can get packages from elsewhere, such as a private GitHub repository or Drupal.org.

```
"repositories": {
    "drupal": {
      "type": "composer",
      "url": "https://packages.drupal.org/8"
    }
}
```

> **The `repositories` key is essential for Drupal applications**. It is used to instruct Composer to search Drupal.org for packages (modules, themes, etc.). See [Composer Configuration for Drupal](https://drupalize.me/tutorial/composer-configuration-drupal) for more information.

### `extra`

This array contains extra configuration information. It is typically used to house miscellaneous configuration required by your dependencies.

```
"extra": {
    "installer-paths": {
        "docroot/core": ["type:drupal-core"],
        "docroot/modules/contrib/{$name}": ["type:drupal-module"],
        ...
    }
}
```

> **The `extra` key is essential for Drupal applications**. It is used to define the installation locations for Drupal modules, themes, etc.

See [Composer Configuration for Drupal](https://drupalize.me/tutorial/composer-configuration-drupal) for more information.

### `minimum-stability`

This defines the minimum required stability for packages.

If you intend to use development versions of Drupal modules, you should set this to `"minimum-stability": "dev"`. If you do, then you should also set `"prefer-stable": "true"` to prevent development versions from being downloaded by default.

See [Composer Configuration for Drupal](https://drupalize.me/tutorial/composer-configuration-drupal) for more information.

### `prefer-stable`

When this is enabled, Composer will prefer more stable packages over unstable ones when finding compatible stable packages is possible. E.g., Composer will default to download beta rather than dev, stable rather than beta, etc.

If you set `"minimum-stability": "dev"`, you should also set `"prefer-stable"` to `true` to prevent development versions from being downloaded by default.

See [Composer Configuration for Drupal](https://drupalize.me/tutorial/composer-configuration-drupal) for more information.

## The *composer.lock* file

The *composer.lock* file is very important. The purpose of the lock file is to record the exact versions of packages that are installed for your application. Its contents are automatically managed by Composer--it should never be directly edited.

> The existence of *composer.lock* fundamentally alters the behavior of the `composer install` command.

When *composer.lock* does **not** exist, the `composer install` command will attempt to download the **most recent, interoperable versions** of all dependencies in accordance with your *composer.json* file. It will then generate a *composer.lock*.

When *composer.lock* **does** exist, the `composer install` command will simply install the **exact versions** of dependencies recorded in the *composer.lock* file.

To understand why **this is so important**, first consider that Composer best practices dictate that you **commit** *composer.lock* and **do not commit** *vendor/* to your Git repository. There are multiple reasons for these conventions. In short, these conventions ensure that:

- The same exact dependency versions are used on all machines (local, dev, ci, stage, prod, etc.)
- The source Git repository is not bloated
- Git diffs and history are not overwhelmed by noise
- Development dependencies are not installed in production
- Production autoloading is optimized
- Various Git-related edge cases are avoided

For an in-depth explanation, see [Should I commit the dependencies in my vendor directory?](https://getcomposer.org/doc/faqs/should-i-commit-the-dependencies-in-my-vendor-directory.md) and [Commit Your *composer.lock* File to Version Control](https://getcomposer.org/doc/01-basic-usage.md#commit-your-composer-lock-file-to-version-control).

With that background knowledge held in mind, suppose the following.

*composer.lock* does not yet exist for your application. Your *composer.json* requires `"monolog/monolog": "^1.23"` (a minimum version of 1.23). When you execute `composer install`, Composer will find the appropriate version of `monolog/monolog` to install. Let's say that is `1.27.2`. After installing `monolog/monolog`, Composer will record in the *composer.lock* that `monolog/monolog` `1.27.2` was installed.

You commit *composer.lock* to your application's Git repository (and do not commit *vendor/*). You push your changes upstream, and another developer pulls those changes down.

When that other developer executes `composer install` on their machine, the packages installed on their machine will match yours exactly. If you had not committed *composer.lock*, then that other developer may have ended up installing different versions! Now imagine this occurring on your testing or production servers rather than on another developer's machine. Yikes! If your application is not identical on all environments, you've got a big problem.

For continued conversation on this topic, see [Composer: It’s All About the Lock File](https://www.engineyard.com/blog/composer-its-all-about-the-lock-file).

## *vendor/*

The vendor directory is the conventional location for all third-party code in a project. If you are using [Drupal-specific configuration](https://drupalize.me/tutorial/composer-configuration-drupal) for Composer, then Composer will install Drupal core, modules, themes, etc. to the correct Drupal locations (not *vendor/*).

Within the *vendor/* directory, packages are organized by [vendor-name] and [package-name]. In our example from [Install Composer and Try It Out](https://drupalize.me/tutorial/install-composer-and-try-it-out), you would end up with the Monolog source files in `vendor/monolog/monolog`. If Monolog listed any dependencies, those would also be in directories under *vendor/*.

The vendor directory also contains *autoload.php*. Drupal core requires *vendor/autoload.php* for you in [core's *autoload.php*](http://cgit.drupalcode.org/drupal/tree/autoload.php?h=8.4.3#n1) and [*index.php*](http://cgit.drupalcode.org/drupal/tree/index.php?h=8.4.3#n14), so you don't need to worry about requiring this file yourself.

Lastly, *vendor/* contains a *bin* subdirectory, which contains all of your [dependencies' binary files](https://getcomposer.org/doc/articles/vendor-binaries.md) (where relevant). For instance, if you require `phpunit/phpunit` then you will find the PHPUnit executable file at *vendor/bin/phpunit*. This is extremely useful, as it allows you to ship your development tools with your project and find them in a predictable location.

## Recap

In this tutorial, we looked at a few of the most popular keys in the *composer.json* schema.

We also learned about the *composer.lock* file and *vendor/* directory, and discussed best practices for committing these to your application's git repository.

## Further your understanding

- What is the difference between the `require` and `require-dev` keys in *composer.json*?
- What is the purpose of the *composer.lock* file?
- Should you commit *vendor/* and/or *composer.lock* to your Git repository?
- What types of files will you find in *vendor/bin* ?

## Additional resources

- [The composer.json Schema](https://getcomposer.org/doc/04-schema.md) (getcomposer.org)
- [Installing Without `composer.lock`](https://getcomposer.org/doc/01-basic-usage.md#installing-without-composer-lock) (getcomposer.org)
- [Installing With `composer.lock`](https://getcomposer.org/doc/01-basic-usage.md#installing-with-composer-lock) (getcomposer.org)
- [Composer: It’s All About the Lock File](https://www.engineyard.com/blog/composer-its-all-about-the-lock-file) (engineyard.com)
- [Should I commit the dependencies in my vendor directory?](https://getcomposer.org/doc/faqs/should-i-commit-the-dependencies-in-my-vendor-directory.md) (getcomposer.org)
- [Commit Your `composer.lock` File to Version Control](https://getcomposer.org/doc/01-basic-usage.md#commit-your-composer-lock-file-to-version-control) (getcomposer.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Install Composer and Try It Out](/tutorial/install-composer-and-try-it-out?p=2467)

Next
[Specify the Version of a Composer Package](/tutorial/specify-version-composer-package?p=2467)

Clear History

Ask Drupalize.Me AI

close