---
title: "Concept: Anatomy of a Modulefree"
url: "https://drupalize.me/tutorial/concept-anatomy-module?p=3235"
guide: "[[drupal-module-developer-guide]]"
order: 10
---

# Concept: Anatomy of a Modulefree

## Content

A Drupal module encapsulates files and directories that serve a specific purpose and follow Drupal's standards and conventions. This tutorial describes the anatomy of a Drupal module, focusing on the placement and purpose of different file types.

In this tutorial, we'll:

- Explain where Drupal looks for modules and where you should place your custom module.
- Describe the standard file and directory types in a module.

By the end of this tutorial, you should be able to identify and understand the purpose of various files and directories within a Drupal module and know where to correctly place them.

## Goal

Recognize and place the files and directories that make up a Drupal module.

## Prerequisites

- [Set Up Your Development Environment](https://drupalize.me/tutorial/set-your-development-environment)

This tutorial uses `MODULE_NAME` as a placeholder. Replace it with your module's machine name. For example, if your module's name is *anytown\_status*, the file *MODULE\_NAME.info.yml* would be *anytown\_status.info.yml*.

## Where Drupal looks for modules

Put your custom module into the root *modules/* directory unless you have a specific reason to use one of the other options.

**Note:** All locations are relative to the Drupal root directory (where *index.php* lives), not the project root, often 1 level higher.

Drupal will look for modules in the following locations:

- *modules/*: The recommended location for placing custom modules.
- *core/modules/*: Contains Drupal core modules. (Never place custom modules here.)
- *sites/all/modules/*: An alternative location, used in certain multi-site setups.

Within these locations, you can organize your modules into subdirectories. A common pattern is:

- *modules/custom/*: For custom project-specific modules
- *modules/contrib/*: For contributed modules downloaded from Drupal.org

## Standard files and directories in a module

You can expect to find some or all of the following file types and directory names within a Drupal module's directory:

- *MODULE\_NAME.info.yml* (**required**): Contains metadata about the module. It's the only required file. It's located in the root of the module directory.
- *MODULE\_NAME.module*: Holds hooks and procedural PHP code. It's optional and follows a strict naming convention.
- *composer.json*: Manages the module's dependencies.
- *MODULE\_NAME.api.php*: Defines hooks for other modules.
- *\*.yml* files: Files with a *.yml* extension other than *.info.yml* are all optional, and are used to provide module-specific configuration for things like routes, asset libraries, and some YAML-based plugin systems like menu links and migrations.
- *src/* directory: Contains PHP classes, following PSR-4 standards.
- *tests/* directory: Stores automated tests, typically PHPUnit tests.
- *config/* directory: Provides default configuration and schema definitions.
- *templates/* directory: Holds Twig templates for rendering output.

## Naming conventions

Files like *MODULE\_NAME.info.yml* and *MODULE\_NAME.module* need specific names and locations for Drupal to recognize them. A module's name should be lowercase, must start with a letter, and can contain alphanumeric characters and underscores.

Code in the *src/* and *tests/* directories follows the PSR-4 autoloading standard, with namespace paths mirroring the directory structure. Drupal uses `Drupal` as the primary namespace, and the module name as the secondary namespace. A file like *src/Plugins/Block/HelloWorld.php* in the *MODULE\_NAME* module would have a PHP namespace like `namespace Drupal\MODULE_NAME\Plugins\Block`.

We'll go into more detail about [namespaces and PSR-4 later in the guide](https://drupalize.me/tutorial/concept-php-namespaces-and-psr-4).

## Recap

In this tutorial, we've explored the anatomy of a Drupal module. We learned about the essential files and directories, where to place your module, and the importance of following Drupal's naming conventions and standards.

## Further your understanding

- What issues might arise if a module's files are not named or placed correctly?

## Additional resources

- [Naming and placing your Drupal module](https://www.drupal.org/docs/develop/creating-modules/naming-and-placing-your-drupal-module) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Create an Info File for a Module](/tutorial/create-info-file-module-mdg?p=3235)

Clear History

Ask Drupalize.Me AI

close