---
title: "Create a Custom Drush Code Generator"
url: "https://drupalize.me/tutorial/create-custom-drush-code-generator?p=2593"
guide: "[[command-line-tools-drupal]]"
order: 20
---

# Create a Custom Drush Code Generator

## Content

In addition to using one of the existing generators, developers can write their own Drush generator commands. This can help speed up repetitive tasks and reduce the use of boilerplate code that is prone to human error.

Generators are provided through Drush's integration with the [Drupal Code Generator project](https://github.com/Chi-teck/drupal-code-generator). Writing new generators isn't specific to Drush, though if you're creating generators for Drupal it is definitely easiest with Drush as a wrapper.

Similar to Drush commands, generators can be supplied by a Drupal module or declared globally. If you have a feature-specific functionality, it's best to ship your custom generator within the custom module. Otherwise, a global generator can be declared and used.

In this tutorial we'll:

- Explain the anatomy of a Drush generator
- Write a custom Drush generator for handling a site's *development.services.yml* file, and use it in a project

By the end of this tutorial you should understand how to create, or customize, a Drush code generator and use it in your project.

## Goal

Create a global code generator to automate creating a *development.services.yml* file.

## Prerequisites

- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)
- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)
- [Develop Drupal Modules Faster with Drush Code Generators](https://drupalize.me/tutorial/develop-drupal-modules-faster-drush-code-generators)

**Note:** This tutorial is compatible with v2.x of the Drupal Code Generator library that is listed as a dependency of Drush 11.

## Problem overview

It's common to create a *sites/development.services.yml* file that contains configuration to make development on local environments more efficient. For example, turning off caching while working on a theme's template files, so you can view your changes without having to clear Drupal's cache first.

Drupal's recommended Composer scaffolding project (`drupal/recommended-project`) comes with a *development.services.yml* file. This means the file is overridden every time the user runs the `composer install` or `composer update` commands. Any changes you make to the file for your needs are lost. There are ways to stop this from happening by updating a section of the *composer.json* file and setting the file mapping to *false*, like shown below:

```
"drupal-scaffold": {
    "file-mapping": {
        "[web-root]/sites/development.services.yml": false
    }
}
```

This, however, creates another problem where the file isn't generated for a fresh local site installation. You can read about this problem in this [drupal.org issue](https://www.drupal.org/forum/support/post-installation/2016-09-15/composer-update-overwrites-developmentservicesyml). In this tutorial, we'll create a global Drush generator for *development.services.yml* files so that a developer can run the generator after the initial site installation to create the necessary file.

A similar approach can be used for CI scripts, Git hooks or other generic and common project files.

## Create a new code generator

### Initial setup

Custom generators may be provided by modules (preferred) or live globally in the project root. In this tutorial, we'll put the code for our generator in a custom module. (If you'd rather provide a global generator, refer to the [Drush documentation on Global Generators](https://www.drush.org/latest/generators/).)

**Tip:** If you don't already have a custom module, ensure you have *contrib* and *custom* folders inside *modules*, and run `drush generate module`. (You only really need a name here, and you can enter "no" for all the customization questions.)

Custom Drush generators live inside the *src/Generators* folder of your Drupal module. Inside this folder, create a PHP file named *DevservicesGenerator.php*. Your generator file name needs to end with *Generator.php*, and you can add just *one* other capitalized word in front of the *Generator.php* -- otherwise your class won't be registered. Your folder structure may look like the one below:

*PROJECT\_ROOT/DRUPAL\_ROOT/*:

```
modules
├── contrib
└── custom
    └── mymodule
        ├── mymodule.info.yml
        └── src
            └── Generators
                ├── DevservicesGenerator.php
```

### Define a generator class

Inside the file that we just created, define a class named `DevservicesGenerator`. Notice that the 2 "words" in our class name are capitalized, there are only 2 "words", the second word is "Generator", and the class name matches the filename (without the *.php* extension).

Since our generated code will not be part of a Drupal extension and doesn't require any Drupal context, extend the `Generator` class. Add a `use DrupalCodeGenerator\Command\Generator;` statement above your class declaration. The class we're extending is an abstract class and contains 1 abstract method which must implement: `generate()`.

Example *drush/Generators/DevservicesGenerator.php*:

```
<?php

namespace Drupal\accordion\Generators;

use DrupalCodeGenerator\Command\Generator;

class DevservicesGenerator extends Generator {

  /**
   * {@inheritdoc}
   */
  protected function generate(array &$vars): void { }

}
```

#### Which generator should you extend in your custom class?

If you're creating your own custom code generator, you have a choice of which "Generator" class to extend. But which one should you extend? Here are some tips to help you decide:

- **Generator**: If the generated code won't be part of a Drupal extension (module, theme, profile) and it doesn't need any Drupal context, extend `DrupalCodeGenerator\Command\Generator`.
- **DrupalGenerator**: If the generated code could live in any Drupal extension (module, theme, profile) or may need Drupal context, extend `DrupalCodeGenerator\Command\DrupalGenerator`.
- **ModuleGenerator**: If the generated code will be a component of a module, extend `DrupalCodeGenerator\Command\ModuleGenerator`.
- **ThemeGenerator**: If the generated code will be a component of a theme, extend `DrupalCodeGenerator\Command\ThemeGenerator`.

#### Generator

Extend `DrupalCodeGenerator\Command\Generator` if the files generated will not live inside a Drupal extension (module, theme, or profile) and doesn't need any Drupal context.

- The abstract base class for all the other generators listed here.
- Defines common properties: `$api`, `$name`, `$description`, `$alias`, `$label`, `$templatePath`, `$directory`. **You will define values for these properties in your custom class**.
- When you extend this class, your class must implement abstract method `generate()`.

#### DrupalGenerator

Extend `DrupalCodeGenerator\Command\DrupalGenerator` (which extends `Generator`) if your generated code will live inside any type of extension (module, theme, or profile). Or if your code requires Drupal to be fully bootstrapped in order to use some Drupal context.

- Includes properties from `DrupalCodeGenerator\Command\Generator`.
- Overrides/Adds properties to use generic "extension" and allow for Drupal context: `$nameQuestion = 'Extension name'`, `$machineNameQuestion = 'Extension machine name'`, `$isNewExtension`, `$extensionType`, `$drupalContext`.
- Asks "default question" (`collectDefault()` method) about machine name of the component and the machine name of the extension it will belong to.
- When you extend this class, your class must implement abstract method `generate()`.

#### ModuleGenerator

Extend `DrupalCodeGenerator\Command\ModuleGenerator` (which extends `DrupalGenerator`) if your generated code will live inside a module.

- Includes properties from `Generator` and `DrupalGenerator`
- Overrides properties to assume "module" is the type of extension: `$nameQuestion = 'Module name'`, `$machineNameQuestion = 'Module machine name'`, `$extensionType = self::EXTENSION_TYPE_MODULE`
- Asks "default questions" (`collectDefault()` method) about the component name and the module machine name it will belong to.
- Asks about optional services and schema files
- See [Drush's woot module's ExampleGenerator.php](https://github.com/drush-ops/drush/blob/11.x/tests/fixtures/modules/woot/src/Generators/ExampleGenerator.php))
- When you extend this class, your class must implement abstract method `generate()`.

#### ThemeGenerator

- Includes properties from `Generator` and `DrupalGenerator`
- Overrides properties to assume "theme" is the type of extension: `$nameQuestion = 'Theme name'`, `$machineNameQuestion = 'Theme machine name'`, `$extensionType = self::EXTENSION_TYPE_THEME`
- Asks "default questions" (`collectDefault()` method) from `DrupalGenerator`.
- When you extend this class, your class must implement abstract method `generate()`.

#### Find the code

You can browse the code for these classes in your project's *vendor/chi-teck/drupal-code-generator/src/Command* folder (assuming you ran `composer require drush/drush`) or [browse the code repository on GitHub](https://github.com/Chi-teck/drupal-code-generator).

#### You must implement the `generate()` method

Regardless of which of the Generator classes you extend, you must implement the `generate()` method. Since all other classes ultimately inherit from this class, and because it is an [abstract method](https://drupalize.me/videos/enforce-functionality-abstract-methods?p=2379), you must implement it if you extend any of the generator classes. If you're using an IDE such as PhpStorm, when you extend any of these classes, it will prompt you to implement the required `generate()` method and ask if you want PhpStorm to add the scaffolding for the method to your class.

The file our generator will create will not be associated with or placed inside any theme or module, and it doesn't need to ask the "default questions", that's why our `DevservicesGenerator` class extends `DrupalCodeGenerator\Command\Generator`.

### Add some require properties

We need to add properties to the class that define the generator parameters that'll be displayed inside by command line interface: name, description and alias. We also add properties that specify base paths to the generated code destination folder and template directory. The properties may be defined as follows:

```
...
class DevservicesGenerator extends Generator {

  protected string $name = 'services-dev-file';
  protected string $description = 'Generates a development.services.yml Drupal file';
  protected string $alias = 'dev-services';
  protected string $templatePath = __DIR__;
  protected string $destination = 'sites/default/';
...
}
```

**Note:**: We're using `__DIR__` for the `$templatePath`, which means we'll place our code-generator template in the same directory as this class. The `$destination` is relative to the Drupal root.

See the comments in `\DrupalCodeGenerator\Command\Generator` for definition of what each property is used for.

## Collect information from the user

The required `generate()` method takes a reference of `$vars`, which may be a familiar pattern if you've implemented preprocess functions. In it, we'll define questions by defining a new key for the `$vars` array and implementing an appropriate parent class method, depending on the kind of question you want to ask. Then we'll use that input in our template to generate some code.

Question-asking methods in `\DrupalCodeGenerator\Command\Generator`:

- `ask(string $question, ?string $default = NULL, $validator = NULL)`-- Asks a question with a default answer and an optional validator.
- `confirm(string $question, bool $default = TRUE): bool`-- Asks question that asks for confirmation.
- `choice(string $question, array $choices, ?string $default = NULL, bool $multiselect = FALSE)`-- Asks a multiple-choice question, with a default answer, and whether to allow multiple selections.

**Note:** The `DrupalCodeGenerator\Command\DrupalGenerator` class defines a `collectDefault()` method that asks for the machine name of the module associated with the file(s) you want to generate, so if that use case applies to you, you should extend this class instead and add the line `$this->collectDefault($vars);` to your `generate()` implementation.

The method doesn't return any values, but it generates the file via the `addFile()` parent class method and uses a specifically-defined template. Your final code for the method may look something like below:

```
/**
 * {@inheritdoc}
 */
protected function generate(array &$vars): void {
  $vars['cacheability_headers'] = $this->confirm('Set debug cacheability headers?', FALSE);
  $vars['twig_debug'] = $this->confirm('Enable Twig debug', TRUE);
 
  $this->addFile($this->destination . 'development.services.yml', 'development.services.twig');
 }
```

In this code we ask 2 "confirmation" questions by calling `$this->confirm()`. Confirmation questions allow users to answer *Yes* or *No*. We also pass default values to in the second parameter. When the generator is run, the user will be prompted to answer these questions at the command line.

If you'd like to collect free-form information instead of *Yes/No* answers, implement `$this-ask()` instead. For example:

```
protected function generate(&$vars): void
{
  $vars['color'] = $this->ask('Favorite color', 'blue');
}
```

### Generate the file

Finally, we'll call the `addFile()` method to generate a file from a Twig template (we'll create that next), and name this file *development.services.yml*. The generated file will be placed under the path defined in the `$destination` property we declared at the top of the class.

### Create a template for the generated file

In the step above, we specified that the generator should use *development.services.twig* as its template. Template files need to be in Twig format and provide generated code output.

In the directory where we defined the generator class (*mymodule/src/Generators*), add a file named *development.services.twig*.

*PROJECT\_ROOT/DRUPAL\_ROOT/*:

```
modules
├── contrib
└── custom
    └── mymodule
        ├── mymodule.info.yml
        └── src
            └── Generators
                ├── DevservicesGenerator.php
                └── development.services.twig
```

The markup of the file should look something like the following:

```
# Local development services included by the settings.local.php file.
{% if not cacheability_headers %}
  {% set  cacheability_headers = "false" %}
{% else  %}
  {% set  cacheability_headers = "true" %}
{% endif %}
{% if not twig_debug %}
  {% set  twig_debug = "false" %}
{% else  %}
  {% set twig_debug = "true" %}
{% endif %}
parameters:
  http.response.debug_cacheability_headers: {{ cacheability_headers }}
  twig.config:
    debug: {{ twig_debug }}
    auto_reload: true
    cache: false
services:
  cache.backend.null:
    class: Drupal\Core\Cache\NullBackendFactory
```

This template replicates the content of a typical *development.services.yml* file with the exception of the conditional block at the top. The block transforms *TRUE* / *FALSE* values of the user input variables that we gathered into strings. Then these variables are used in the snippet to populate values for `http.response.debug_cacheability_headers` property and Twig debug. The names of the variables in the Twig template file correspond to the keys of the `$vars` array in the `generate()` method we defined earlier.

### Create or add to your module's *drush.services.yml*

In order for our generator class to be called, we need to register it as a Drush service in our custom module's *drush.services.yml* file. In the root directory of your module, create the file *drush.services.yml* with the following YAML-formatted code:

```
services:
devservices.generator:
  class: Drupal\mymodule\Generators\DevservicesGenerator
  tags:
    -  { name: drush.generator.v2 }
```

Here's the final structure of all our custom code generator files:

*PROJECT\_ROOT/DRUPAL\_ROOT/*:

```
modules
├── contrib
└── custom
    └── mymodule
        ├── mymodule.info.yml
        ├── drush.services.yml
        └── src
            └── Generators
                ├── DevservicesGenerator.php
                └── development.services.twig
```

### Test the generator

First, rebuild the cache (`drush cr`) and run `drush generate`:

```
drush cr
drush generate
```

You should now see the new generator in the list under the *\_global* category:

```
Available commands:                                                                                               
_global:                                                                                                          
  composer (composer.json)                                       Generates a composer.json file                   
  controller                                                     Generates a controller                           
  dev-services-yml (dev-services)                                Generates a development.services.yml Drupal file
  field                                                          Generates a field                                
  hook                                                           Generates a hook                                 
  install-file                                                   Generates an install file                        
  javascript                                                     Generates Drupal JavaScript file                 
  layout                                                         Generates a layout                               
  migration                                                      Generates the yml and PHP class for a Migration  
  module                                                         Generates Drupal module                          
  module-file                                                    Generates a module file                          
  phpstorm-metadata                                              Generates PhpStorm metadata                      
  render-element                                                 Generates Drupal render element                  
  service-provider                                               Generates a service provider 
...
```

Now that we see our generator on the list, we can test it out. Run `drush generate dev-services-yml` and answer the questions:

```
drush generate dev-services-yml

 Welcome to dev-services generator!
––––––––––––––––––––––––––––––––––––

 Set debug cacheability headers? [No]:
 ➤ 

 Enable Twig debug [Yes]:
 ➤ 

 The file sites/default/development.services.yml already exists. Would you like to replace it? [Yes]:
 ➤ Yes

 The following directories and files have been created or updated:
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
 • sites/default/development.services.yml
```

Verify it worked by navigating to the *sites/default* directory and opening the *development.services.yml* that you should see there. Your file may look something like the following, depending on the answers to the questions above:

```
# Local development services included by the settings.local.php file.
parameters:
  http.response.debug_cacheability_headers: false
  twig.config:
    debug: true
    auto_reload: true
    cache: false
services:
  cache.backend.null:
    class: Drupal\Core\Cache\NullBackendFactory
```

## Recap

Developers can define their own generators in case they have special use cases that are not covered by the existing code generators that come with Drush core and the Drupal Code Generator project. Custom generators can be provided by modules, or defined for a specific project.

Generators consist of a class that (at the minimum) extends one of the 4 generator classes, `Generator`, `DrupalGenerator`, `ModuleGenerator`, or `ThemeGenerator`. It sets values for protected properties for the name, description, alias, template path, and destination of the generated files. It defines an `generate()` method which adds keys to the `$vars` array reference, defining questions and default answers. It calls the `addFile()` method to define where the generated file(s) should go. Generators also have to provide a Twig template that defines the generated code. User input gathered through the command-line questionnaire is passed to the Twig templates as variables and can be used to dynamically change the generated code.

## Further your understanding

- We extended the `DrupalCodeGenerator\Command\Generator` class with a pretty generic code generator. Which class would you extend if you wanted to place your generated files inside a module?
- Familiarize yourself with the other "parent" generator classes in *vendor/chi-teck/drupal-code-generator/src/Command* -- *Generator.php*, *DrupalGenerator.php*, *ModuleGenerator.php*, and *ThemeGenerator.php*.

## Additional resources

- [Drush official documentation](https://www.drush.org) (drush.org)
- [Drush Generator Authoring documentation](https://www.drush.org/latest/generators/) (drush.org)
- [Drush's woot module's example generator](https://github.com/drush-ops/drush/tree/11.x/tests/fixtures/modules/woot/src/Generators) (github.com)
- [Drush Git repository](https://github.com/drush-ops/drush) (github.com)
- [Drupal Code Generator project](https://github.com/Chi-teck/drupal-code-generator) (github.com)
- [Introduction to Abstract Classes](https://drupalize.me/videos/introduction-abstract-classes?p=2379) (Drupalize.Me)
- [Enforce Functionality with Abstract Methods](https://drupalize.me/videos/enforce-functionality-abstract-methods?p=2379) (Drupalize.Me)
- [Extend Abstract Classes](https://drupalize.me/videos/extend-abstract-classes?p=2379) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Develop Drupal Modules Faster with Drush Code Generators](/tutorial/develop-drupal-modules-faster-drush-code-generators?p=2593)

Next
[Overview: Creating Your Own Custom Drush Commands](/tutorial/overview-creating-your-own-custom-drush-commands?p=2593)

Clear History

Ask Drupalize.Me AI

close