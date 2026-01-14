---
title: "What Is Composer?free"
url: "https://drupalize.me/tutorial/what-composer?p=2467"
guide: "[[command-line-tools-drupal]]"
order: 1
---

# What Is Composer?free

## Content

Composer is the preferred dependency management solution for PHP. List your project's dependencies in a *composer.json* file and, after issuing a few commands in the CLI, Composer will automatically download your project's dependencies and set up autoloading for you. Composer is analogous to NPM in the Node.js world, or Bundler in the Ruby world.

Drupal core uses Composer to manage non-Drupal dependencies like Guzzle and PHPUnit. An increasing number of contributed modules also use Composer to integrate third party PHP libraries into Drupal.

This series provides guidance for Drupal developers and site builders who would like to learn to use Composer to build and maintain a Drupal application.

It covers high-level concepts about Composer and walks you step-by-step through creating a new application, downloading PHP libraries, and implementing them using Composer!

It also covers Drupal-specific Composer configuration and provides guidance for accomplishing common Drupal tasks like updating core and installing a new module.

In this tutorial we'll:

- Familiarize ourselves with the general concepts of dependency management
- Learn about Composer and the role it plays in a PHP/Drupal project
- Learn about some advantages and disadvantages of using Composer

By the end of this tutorial you should be able to explain what Composer is, what it's used for, and make the case for using it in your own projects.

## Goal

Familiarize yourself with the general concept of dependency management, the purpose of Composer, and its users, use cases, advantages, and drawbacks.

## Prerequisites

- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)

## What is Composer?

[Composer](https://getcomposer.org/) is a dependency management tool for PHP. It allows you to install, update, and load the PHP libraries that your PHP application depends on.

Suppose you have a Drupal application that depends on a number of Drupal modules and non-Drupal PHP libraries (root dependencies). Some of those modules and libraries depend on other modules and libraries (recursive dependencies).

Composer enables you to declare the PHP libraries (core, modules, themes, libraries, etc.) that your application depends on, and it:

- Finds out which versions of which libraries can and need to be installed (dependency resolution)
- Downloads all required dependencies (root and recursive)
- Makes those dependencies available to Drupal (autoloading)

It also allows you to update, remove, and patch those libraries, and even “hook into” and customize the process.

## Who uses Composer?

Composer is the de facto dependency management tool for the entire PHP community. It is widely used across the world of PHP. According to [Packagist statistics](https://packagist.org/statistics) as of early 2018, there are over **168,000 packages available** via Composer, and they have cumulatively been installed over **seven billion** times.

In terms of Drupal roles, Composer is an invaluable tool for developers, site builders, and site architects.

If you need to download and install PHP libraries (core, modules, themes, libraries, etc.) then you should be using Composer!

## Why do we use Composer?

Composer is one of the larger forces responsible for the recent [PHP Renaissance](https://www.oreilly.com/ideas/the-new-php).

It enables the PHP community to easily share and implement open-source libraries. It promotes standardization, collaboration, and contribution, allowing developers to mix and match reliable pre-made components and avoid “reinventing the wheel.”

If you use Drupal, you’re already benefiting from Composer. Drupal itself has embraced Composer internally in Drupal core. This has allowed Drupal to “get off the island” and take advantage of libraries used by the larger PHP community, like [Symfony](https://symfony.com/).

We use Composer because it helps us find, install, and update application dependencies better than any other tool in the PHP community.

## Acknowledgement of limitations

Let’s be honest; while using Composer has many advantages, it is not without its drawbacks. Composer has gotten a bad rap in some parts of the Drupal community, and that’s not without cause.

Let’s briefly discuss the top three types of Composer “problems” that users most frequently encounter.

### The conceptual hurdle

For many Drupalists, the idea of dependency management is new, and it can be a difficult concept to wrap one’s head around.

We have traditionally used very cut-and-dry methods for downloading and updating dependencies in the Drupal community, like downloading tarballs, manually decompressing and moving them into a given directory. More advanced Drupal users may have used [Drush](http://www.drush.org/) or even [Drush make](http://docs.drush.org/en/7.x/make/).

While these methods have the advantage of simplicity, they lack some of the most powerful aspects of Composer such as recursive dependency resolution, semantic versioning, and autoloading (these topics will be covered later in the tutorial), or simply wider (non-Drupal) community adoption.

This series will help you get over that hurdle.

### Resolving conflicts

Composer is great at finding interoperable versions of dependencies, but sometimes it’s just not possible.

Your application’s declared dependencies, or the subsidiary dependencies declared by your dependencies, may simply not be interoperable in the requested versions. Typically, this can be resolved by tweaking the version constraint of one or more of your application’s dependencies.

However, the process of discovering exactly which dependencies are in conflict and finding a suitable tweak can be frustrating, and Composer is decidedly poor at explaining root cause clearly. It is not fun to debug.

We’ve included a Troubleshooting addendum in this series to help you resolve some of the more common Composer problem scenarios.

### CLI only

Composer is a command line tool. For many Drupalists, this alone can be intimidating.

But don’t worry! We will walk you through Composer usage step-by-step. **You can do this**.

And, if you really love your [GUI](https://en.wikipedia.org/wiki/Graphical_user_interface)s, then you’re free to explore some of the unofficial GUIs for Composer:

- <https://www.getcomposercat.com/>
- <https://github.com/mglaman/conductor>

However, this tutorial will exclusively use the command-line interface. Check out our [Command Line Basics](https://drupalize.me/series/command-line-basics-series) tutorials if you're new to the CLI or if you'd just like a refresher.

## Recap

In this tutorial, we explored the concept of dependency management and learned about Composer at a high, conceptual level. In particular, we learned about Composer, its purpose, use cases, users, advantages and drawbacks.

## Further your understanding

- Why is dependency management useful for Drupal applications?
- How does Composer differ from tools like `apt-get` and `yum`?
- What does Composer do that Drush does not?

## Additional resources

- [Composer](https://drupalize.me/topic/composer) - An overview of Composer plus links to learning resources. (Drupalize.Me)
- [Command Line Basics](https://drupalize.me/series/command-line-basics-series) (Drupalize.Me)
- [Composer Introduction](https://getcomposer.org/doc/00-intro.md#introduction) (getcomposer.org)
- [Packagist](https://packagist.org/) (packagist.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Install Composer and Try It Out](/tutorial/install-composer-and-try-it-out?p=2467)

Clear History

Ask Drupalize.Me AI

close