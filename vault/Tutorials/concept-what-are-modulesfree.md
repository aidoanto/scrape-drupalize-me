---
title: "Concept: What Are Modules?free"
url: "https://drupalize.me/tutorial/concept-what-are-modules?p=3234"
guide: "[[drupal-module-developer-guide]]"
---

# Concept: What Are Modules?free

## Content

Modules enable developers to customize Drupal without modifying the core software. To ensure a stable and upgradeable core system, Drupal defines integration points and patterns that developers can use to customize the system. Modules contain code (PHP, JavaScript, Twig, CSS, YAML, etc.) that can extend, alter, and enhance Drupal's features and functionality.

In this tutorial, you'll learn:

- What Drupal modules are and their role in Drupal architecture
- How modules interact with Drupal core to extend or alter site functionality
- About the types of modules: core, contributed, and custom

By the end of this tutorial, you should be able to explain what modules are in Drupal, and understand their role in defining a Drupal site's functionality.

## Goal

Define what modules are and their role in extending, altering, and enhancing Drupal.

## Prerequisites

- None.

## What are modules in Drupal?

*Modules* are packages of code that use integration points or well-defined patterns to alter, extend, and enhance a Drupal site.

From an end-user perspective, modules add or change functionality of a Drupal site. Administrative users can install modules through Drupal's *Extend* administrative interface.

Learn more about how site builders use modules.

- [Concept: Modules](https://drupalize.me/tutorial/user-guide/understanding-modules)
- [Extending and Customizing Your Site](https://drupalize.me/course/user-guide/extend-chapter)

Each module has a specific purpose, ranging from feature enhancements to complex system integrations.

From a developer's perspective, modules are packages of code (mostly PHP) that extend Drupal to add new features or alter existing functionality. Modules can be installed to enable their features, and uninstalled to turn features off.

All modules are written in the same way and use the same patterns. Their exact implementation will vary depending on the intended use. A module intended for a specific project can take liberties and hard-code assumptions like a field's configuration options. A module intended for a global audience will need to be generic or configurable.

A module developer can contribute and maintain their modules as a project hosted on Drupal.org. These modules are available for others to download, use, and collaboratively improve. The ecosystem of contributed modules is a key part of why Drupal is successful.

## Types of modules in Drupal

As a developer, you'll work with *core*, *contributed*, and *custom modules*.

### Core modules

- Modules included with Drupal core.
- Live in the */core/modules* directory.
- Examples: Block, Comment, Field UI, Views

Core modules provide Drupal's primary feature set, and contain many of the APIs that you'll engage with as a module developer. You'll work with these when you want to implement one of the APIs, use one of the services they provide, fix a bug in Drupal core, or help contribute to an upstream feature.

### Contributed modules

- Modules downloaded from Drupal.org that are not part of Drupal core.
- Typically placed in the */modules/contrib* directory.
- Examples: Admin Toolbar, Devel

Contributed modules are written to be generic and reusable. They are usually configurable with a settings form, and allow you to tailor their features to your specific use case. You'll work with these when you want to help fix a bug, maintain a module you've developed, and extend or alter a contributed module's features to meet the needs of your use case.

Learn more about contributing modules.

Work with the community to help maintain and improve contributed modules.

- [Concept: Using and Helping Contributed Modules](https://drupalize.me/tutorial/concept-using-and-improving-contributed-modules)
- [Concept: Contributing Your Custom Modules](https://drupalize.me/tutorial/concept-contributing-your-custom-modules).

While not required, module contribution is an important part of the Drupal community ethos and a great way to learn.

### Custom modules

- Project-specific modules that you or another developer wrote specifically for your application.
- Typically placed in the */modules/custom* directory.

Custom modules are specific to a project and make application-specific tweaks to features provided by other modules. You'll work with these to define business-specific application logic. Custom modules are a place to create novel solutions that use APIs and integration points of existing core and contributed modules.

Common use cases for custom modules:

- Site-specific SEO enhancements
- Custom form processing and data validation rules
- Integration with 3rd-party APIs, especially internal ones
- Unique business logic
- Custom reporting and analytics

## Don't hack core!

The Drupal community follows the mantra, "Don't hack core". Following this principle ensures your Drupal site remains extensible and maintainable. If you alter code that is part of Drupal's core software, you will potentially face the following problems:

- **Loss of changes**: Any modifications will be overwritten during core software updates, which can lead to loss of functionality.
- **Missing critical security updates**: If you're unable or reluctant to perform core updates because of code modifications to the core software within a project, your site could miss critical security updates and become vulnerable to attack.
- **Compatibility issues**: Custom changes might conflict with other subsystems or contributed modules, leading to unexpected behavior or errors.
- **Maintenance challenges**: Custom changes to the core software make it difficult for other developers or even your future self to understand and maintain the site.

Read more about the "don't hack core" philosophy in [this insightful Drupal Answers post](https://drupal.stackexchange.com/a/59066).

### What about bug fixes?

Bug fixes are regularly included in patch or minor updates to Drupal core and contributed modules. Which is why [keeping your Drupal site up-to-date](https://drupalize.me/topic/minor-version-and-security-updates) is important. But, the fact is that sometimes fixing a bug in Drupal core or a contributed module does require "hacking" code that doesn't belong to you. This can be true when a bug fix is available through a patch contributed to an issue, but the patch is not yet part of the official release. Perhaps a better mantra would be **"don't hack core, but when you do, use a patch."**

The [Composer Patches plugin](https://github.com/cweagans/composer-patches) makes Composer an ideal tool for tracking, downloading, and applying these patches.

Learn more about patching projects using Composer.

- [Composer Configuration for Drupal: Patching core and contributed modules](https://drupalize.me/tutorial/composer-configuration-drupal?p=0#toc-patching-c-0ghm0yp5) (Drupalize.Me)
- [Composer Patches plugin](https://github.com/cweagans/composer-patches) (GitHub.com)
- [Patching projects using Composer](https://www.drupal.org/docs/develop/using-composer/manage-dependencies#patches) (Drupal.org)

## Plugins, services, events, and hooks

Modules interact with the Drupal software through 4 primary patterns: *plugins*, *services*, *events*, and *hooks*. **As a developer, these are the patterns that you'll need to learn to implement and apply in order to create custom modules.**

- **Plugins**: These are like the individual parts used to assemble a machine. They provide new features in a way that allows a Drupal administrator to choose one option from a list of many. For example, choosing specific blocks or field types when building your site makes the site unique.
- **Services**: Think of services as specialized tools that can be swapped out. They handle specific tasks like sending emails or integrating with databases. You might have a drawer full of hammers, and they operate the same way, but you choose the right one depending on the job.
- **Events**: These are like triggers that react to certain actions or conditions within Drupal, such as entity validation or dynamic routing.
- **Hooks**: Hooks are like customizable attachment points in Drupal where you can "hook in" your own code to alter behavior or extend functionality.

In this guide, we'll explain and use each of these patterns as we develop custom modules for the [Anytown Farmers Market site](https://drupalize.me/tutorial/guiding-scenario).

## Recap

*Modules* are packages of code that use integration points or well-defined patterns to alter, extend, and enhance a Drupal site. Modules can be installed or uninstalled by administrative users to add or remove functionality. Core modules live in the *core/modules* directory and provide Drupal's primary features. Contributed modules typically live in *modules/contrib* and available for download on Drupal.org. Custom modules live in *modules/custom*, provide application-specific business logic, and integrate with other core and contributed modules. If you need to alter, enhance, or provide new features to a Drupal site, you should use modules instead of "hacking core". But, if you need to fix a bug, use Composer Patches if the fix is not yet part of an official release and a patch is available.

## Further your understanding

- Have you encountered modules (sometimes called plugins, or extensions) in other CMS platforms or frameworks?
- Why would you want to be able to modify the way Drupal works without altering Drupal's code?

## Additional resources

- [List of contributed modules](https://www.drupal.org/project/project_module?f%5B0%5D=&f%5B1%5D=&f%5B2%5D=&f%5B4%5D=sm_field_project_type%3Afull&f%5B5%5D=&text=&solrsort=iss_project_release_usage%20desc&op=Search) (Drupal.org)
- [1.2. Concept: Modules](https://drupalize.me/tutorial/user-guide/understanding-modules) (Drupal User Guide)
- [Chapter 11. Extending and Customizing Your Site](https://drupalize.me/course/user-guide/extend-chapter) (Drupal User Guide)
- [DrupalCon New Orleans 2016: Altering, Extending, and Enhancing Drupal 8](https://www.youtube.com/watch?v=tMM-I70ksQA) (YouTube.com)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Concept: How Drupal Builds a Page](/tutorial/concept-how-drupal-builds-page?p=3234)

Clear History

Ask Drupalize.Me AI

close