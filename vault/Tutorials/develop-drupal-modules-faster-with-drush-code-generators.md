---
title: "Develop Drupal Modules Faster with Drush Code Generators"
url: "https://drupalize.me/tutorial/develop-drupal-modules-faster-drush-code-generators?p=2593"
guide: "[[command-line-tools-drupal]]"
---

# Develop Drupal Modules Faster with Drush Code Generators

## Content

Every Drupal module needs a *\*.info.yml file*; the basic structure of a form controller class and related routing is the same for every form; and much of the code required to create a custom content entity type is boilerplate annotations and extending base classes. Wouldn't it be nice if there was a way to automate some of that repetitive work? Drush can be used to speed up module development by generating scaffolding code for event subscribers, forms, services, module files, routing, and much more. These generators are provided by the Drupal Code Generator project. They're neatly bundled up in Drush under the `drush generate` command.

In this tutorial we'll:

- Learn about the [Drupal Code Generator project](https://github.com/Chi-teck/drupal-code-generator)
- Learn how Drush integrates with this project
- Demonstrate the `drush generate` command and its options

By the end of this tutorial, you'll know how to use the `drush generate` command to speed up development for your Drupal modules.

## Goal

Introduce the `drush generate` command and Drupal Code Generator project to developers and illustrate some common use cases.

## Prerequisites

- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)
- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)
- [Drupal Code Generator project](https://github.com/Chi-teck/drupal-code-generator)

## The Drupal Code Generator project

The [Drupal Code Generator project](https://github.com/Chi-teck/drupal-code-generator) is a command line code generator for Drupal. It can generate code for Drupal 7-9. In order to make it easier to discover and use, it's been integrated with Drush (as of Drush 9) under the `drush generate` command. You *can* use it stand-alone, but generally it'll be easier to use when bundled with Drush.

### A note on version compatibility

Drush 11 integrates with Drupal Code Generator version 2. This version of the code generator is compatible with Drupal 7 and 9 (not 8). To get snippets for Drupal 8, you need Drupal Code Generator version 1. If needed, you can run Drupal Code Generator without Drush. Refer to the [Drupal Code Generator project documentation](https://github.com/Chi-teck/drupal-code-generator) for more details about how to install and run it without Drush.

**Note:** since the Drupal Code Generator project is a dependency of Drush, you may run into Composer dependency conflicts and will need to resolve those if you'd like to use a version other than what is installed as a dependency of your installed version of Drush.

Drupal Code Generator version 2 is a dependency for Drush 11 and is installed together with it when Drush is installed via Composer -- so you don't need to install anything extra to start using the `generate` command.

## Generators available through Drush

To see all available generator options, run `drush generate` in the command line from the root of your Drupal project. The output of the initial command will be a list of all available generator commands. Each generator command is responsible for one scaffold that is described in the right column of the output.

All generators are grouped into the following categories. As of Drush 11, the categories are:

- *\_global* - Frequently-used generators that can be used in many contexts within the Drupal projects, such as module, controller, layout, etc.
- *drush* - Drush-specific generators
- *entity* - Configuration entity, content entity, and bundle class for content entity generators
- *form* - Form-related generators
- *misc* - Apache, Nginx, Composer project, and simple HTML page generators
- *plugin* - Scaffolds for various plugin types: blocks, views, migrations, etc.
- *service* - Scaffolds for service classes
- *test* - Test class generators
- *theme* - Theme scaffolding generators
- *yml* - Drupal-specific YAML file generators for breakpoints, services, routing, etc.

To generate code, run `drush generate [generator_name]` with the name of the generator from the list. After that, Drush will ask generator-specific questions so that the generated code is as polished as possible. After generating, Drush lists the files that were created.

Let's walk through a couple of examples to see it in action.

## Scaffold a custom module

To create a standard custom module scaffold, run `drush generate module`. Drush will ask you questions about the module. The output should look something like the following:

```
 Welcome to module generator!
––––––––––––––––––––––––––––––

 Module name [Web]:
 ➤ test

 Module machine name [test]:
 ➤

 Module description [Provides additional functionality for the site.]:
 ➤ The description.

 Package [Custom]:
 ➤

 Dependencies (comma separated):
 ➤

 Would you like to create module file? [No]:
 ➤

 Would you like to create install file? [No]:
 ➤

 Would you like to create libraries.yml file? [No]:
 ➤

 Would you like to create permissions.yml file? [No]:
 ➤

 Would you like to create event subscriber? [No]:
 ➤

 Would you like to create block plugin? [No]:
 ➤

 Would you like to create a controller? [No]:
 ➤

 Would you like to create settings form? [No]:
 ➤

 The following directories and files have been created or updated:
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
 • modules/custom/test/test.info.yml
```

Notice how Drush asks questions relevant to new module scaffolding, like, do you want to include an *.install* file, or, does your module have any dependencies, etc. The generator automatically places generated files in the *custom* modules directory for your project, following best practices, but **only if** you have already created *modules/custom*.

**Tip:** On a fresh project, create *modules/contrib* and *modules/custom* before downloading contributed modules or generating custom modules with Drush.

If you navigate to this folder, you should see a new module folder (in our example named *test*), and *test.info.yml* and *test.module* files.

```
├── test
│   ├── test.info.yml
```

To verify that the module is working, run `drush en test`.

```
$ drush en test
 [success] Successfully enabled: test
```

## Generate a routing file with Drush

During the generation process Drush asked questions that would help generate common module files such as a block plugin, install file, and an event subscriber.

It didn't ask to generate a routing file which is another common file for a Drupal module. However, there is a generator that helps to automate this task. It's located in the *yml* category and is called *yml-routing*.

Run `drush generate yml:routing` in the command line. Then, when prompted, enter the machine name of the module for which you need the file to be generated.

```
Welcome to routing generator!
–––––––––––––––––––––––––––––––––––

 Module machine name:
 ➤ test

 The following directories and files have been created or updated:
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
 • modules/custom/test/test.routing.yml
```

The resulting file is automatically placed in the correct folder of the module. It comes with 2 predefined routes that can be altered by developers later: a basic controller route and a route to the settings form.

```
test.reports:
  path: '/admin/reports/test'
  defaults:
    _controller: '\Drupal\test\Controller\TestController::build'
    _title: 'test report'
  requirements:
    _permission: 'access site reports'
test.settings:
  path: '/admin/config/test/settings'
  defaults:
    _form: 'Drupal\test\Form\SettingsForm'
    _title: 'test settings'
  requirements:
    _permission: 'administer test configuration'
```

## Further examples

If you want to see more in-depth examples of generator usage, check out the following tutorials.

- [Scaffold a Custom Content Entity Type with Drush Generators](https://drupalize.me/tutorial/scaffold-custom-content-entity-type-drush-generators)
- [Create a Custom Drush Code Generator](https://drupalize.me/tutorial/create-custom-drush-code-generator)

## Where to find the generator code

It may come in handy to have an understanding of where the generated code comes from. Since the Drupal Code Generator project is a Drush dependency, it gets installed in the *vendor* folder in the root of your Drupal application when Drush is installed.

The code is placed in the *vendor/chi-teck* folder. All the Drupal code generators are located in the *chi-teck/drupal-code-generator/src/Command/* directory. We recommend browsing through this code to get a better understanding of how generators are put together.

## When you should use a generator

Generators are good for speeding things up and setting you off to a good start. They can also serve as a way to learn about how different APIs and systems work. However, it's advisable to take the time to understand what exactly the generated code is doing and not just trust it blindly. Think of generators as a way to speed up common tasks like creating a *block plugin* once you know how to do it manually.

Generators are great as a starting point -- but rarely a completely fleshed out solution. For example, it'll generate an *\*.info.yml* file for you, but there's a lot of things info files can do that are not going to be automatically dealt with. It'll generate an `Entity` class and extend a *good base class*, but there are other base classes you could extend that might be a better fit depending on your use-case.

Throughout this site we often use the `drush generate` command in our code examples when we want to do something like skip the work of creating a custom module and jump right to explaining how a specific hook works. We're assuming you already know about *\*.info.yml* files, and *\*.module* files, and want to skip right to a specific example that is the focus of a particular tutorial. But, when we're trying to generically explain how an *\*.info* file works we'll code it by hand, so we can provide more details.

## Recap

Drush integrates with the Drupal Code Generator project and wraps its generators in a Drush command that allows it to generate scaffolding code for the majority of common code tasks such as plugins, modules, themes, services, controllers, and common YAML files. Developers can use the `drush generate` command to speed up repetitive and tedious module development tasks. It's a good tool for learning about how all the pieces of a Drupal module fit together.

## Further your understanding

- We created a routing file; can you create a menu links file for our new module?
- We used generators with the Drush wrapper; is it possible to use generators without Drush? Can you think of any reasons you might want to?
- What happens if you try to generate code for an existing module? Would that result in overriding/updating an existing file?

## Additional resources

- [Drush official documentation](https://www.drush.org) (drush.org)
- [Drush Git repository](https://github.com/drush-ops/drush) (github.com)
- [Drupal Code Generator project](https://github.com/Chi-teck/drupal-code-generator) (github.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Drush Configuration](/tutorial/drush-configuration?p=2593)

Next
[Create a Custom Drush Code Generator](/tutorial/create-custom-drush-code-generator?p=2593)

Clear History

Ask Drupalize.Me AI

close