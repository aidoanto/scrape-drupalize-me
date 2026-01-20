---
title: "Create an Info File for a Modulefree"
url: "https://drupalize.me/tutorial/create-info-file-module-mdg?p=3235"
guide: "[[drupal-module-developer-guide]]"
order: 11
---

# Create an Info File for a Modulefree

## Content

Every module must have an info file that provides Drupal with metadata about the module. Drupal uses this file to recognize that the directory the info file is contained within, along with the files inside it, are part of a module. Without an info file, Drupal will not recognize your code as a module, and the code will be ignored. Info files are written in YAML and contain information like the module's name, versions of Drupal it's compatible with, and a description.

In this tutorial, we'll:

- Pick a name for our custom module and create a directory for it.
- Create an *.info.yml* file with metadata about our module.
- Install our new custom module to verify Drupal can locate it.

By the end of this tutorial, you should have a directory for your custom module's code and an info file that tells Drupal this directory contains a module.

## Goal

Define an info file for a new module named *anytown*.

## Prerequisites

- [Set Up Your Development Environment](https://drupalize.me/tutorial/set-your-development-environment)
- [Concept: Anatomy of a Module](https://drupalize.me/tutorial/concept-anatomy-module)

**Tip**: In a DDEV environment, Drush commands can be run outside the `web` container by prefixing the command with `ddev`. For example, `ddev drush status`. From inside the `web` container (after running `ddev ssh`), Drush commands do not need to be prefixed (`drush status`).

## Video tutorial

Sprout Video

## Set up a new module with an info file

**Tip:** You can start a new module using the `drush generate module` command. The result will be similar to following the steps below.

### Pick a name for your module

A module's machine name should be all lowercase, must start with a letter, and can contain alphanumeric characters and underscores. When working on project-specific code, it's a good idea to prefix the module name with something unique to your project. For this example, we'll call our module *anytown*.

### Create an empty directory for your module

Create a new directory named *anytown* in the *web/modules/custom/* directory of your project which will contain the code for a custom module.

From the root of your Drupal project, run the following command:

```
mkdir -p web/modules/custom/anytown
```

### Create an info file

Add a new *anytown.info.yml* file to the directory you just created and populate it with the following content.

Example *web/modules/custom/anytown/anytown.info.yml*:

```
name: 'Anytown'
type: module
description: 'Custom code for the Anytown Farmers Market site.'
package: Custom
core_version_requirement: ^10 || ^11
```

Some of the keys in this file, like `name`, `type`, and `core_version_requirement`, are required, while others are optional. Learn more about the contents of a module's info file in [Overview: Info Files for Drupal Modules](https://drupalize.me/tutorial/overview-info-files-drupal-modules).

### Install your custom module

An info file is the only thing required to create a new module. While the module won't do anything without adding more code, at this point it should appear in Drupal's list of modules, and you can install it. Verify Drupal can find your module and install it using the UI or Drush.

To use the UI, in the *Manage* administration menu, navigate to *Extend* (*admin/extend*), find the *Anytown* module in the list, check the box next to it, then scroll to the bottom of the page, and press the button, **Install**.

To install your module with Drush:

```
drush pm:install anytown
```

You should see a message indicating the module was successfully installed.

## Recap

In this tutorial, we created a new module named *anytown* and an info file named *anytown.info.yml*. We populated the info file with basic metadata about our module. Then we verified that Drupal could find the module and that it could be enabled.

## Further your understanding

- What is the significance of the name (the part before the *.info.yml* extension) we choose for our module's info file?
- Of the data we added to the *anytown.info.yml* file, which keys are required?
- What information does an info file provide Drupal about your module?

## Additional resources

- [Overview: Info Files for Drupal Modules](https://drupalize.me/tutorial/overview-info-files-drupal-modules) (Drupalize.Me)
- [Let Drupal know about your module with an .info.yml file](https://www.drupal.org/docs/develop/creating-modules/let-drupal-know-about-your-module-with-an-infoyml-file) (Drupal.org)
- [Develop Drupal Modules Faster with Drush Code Generators](https://drupalize.me/tutorial/develop-drupal-modules-faster-drush-code-generators) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Anatomy of a Module](/tutorial/concept-anatomy-module?p=3235)

Next
[Create a Custom "Hello, World!" Block](/tutorial/create-custom-hello-world-block?p=3235)

Clear History

Ask Drupalize.Me AI

close