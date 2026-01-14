---
title: "How to Implement Drupal Code Standardsfree"
url: "https://drupalize.me/tutorial/how-implement-drupal-code-standards?p=2458"
guide: "[[develop-drupal-sites]]"
order: 12
---

# How to Implement Drupal Code Standardsfree

## Content

Once you know what code standards are and why you should use them, you need to learn how to implement Drupal coding standards in your projects. This tutorial will walk through some of the steps you can take to make this as easy as possible. We'll cover:

- Configuring your editor or IDE to warn you of coding standards violations
- Setting up the Coder module and phpcs to scan and review your code
- Performing team code reviews

By the end of this tutorial you should be able to configure your development environment and implement processes in your workflow that help to ensure your code meets Drupal's coding standards guidelines.

## Goal

Configure your editor or IDE, and install Coder + phpcs to aid in reviewing code for coding standards compliance.

## Prerequisites

- [What Are Coding Standards?](https://drupalize.me/tutorial/what-are-drupal-code-standards)

## Contents

- [Configure your editor](#editors)
- [Review your code with PHP Code Sniffer](#phpcs)
- [Team code reviews](#teams)

## Quickstart

If you're already familiar with phpcs, and are just trying to remember what packages you need to install here you go:

```
# Install coder.
composer require --dev drupal/coder

# Scan some code.
./vendor/bin/phpcs --standard=Drupal,DrupalPractice web/modules/custom/my_module/
```

Keep reading to learn more about setting your environment up for easier implementation of the Drupal coding standards.

## Read the coding standards and keep them handy

It’s a good idea to read over the [Drupal coding standards](https://www.drupal.org/coding-standards) so you have an idea of what’s expected. Even if you’re familiar with them, refresh your knowledge. They’re also a living document, so there’s a good chance something may have been changed or added since the last time you read them. Use this tutorial as a reason to read them again, if you've read them before. Make sure you have them bookmarked for reference, as well.

## Set your editor up for success

The easiest way to keep your code clean and up to par is by having your editor do the work. There are a lot of editors out there, and even the ones that don’t have many bells and whistles can be set up to help you keep standards in mind when you’re coding. We'll take a look at the settings for two popular editors that work across all the major operating systems: Sublime Text and PhpStorm. If you’re using another editor, you can see if it’s listed in the [Drupal.org Development tools overview](https://www.drupal.org/node/147789).

### Visual Studio Code

[Visual Studio Code](https://drupalize.me/%5Bhttps%3A//www.sublimetext.com/%5D%28https%3A//code.visualstudio.com/%29) is a text and code editor that allows for a lot of customization through its extensions system.

The Drupal.org handbook has a page all about [Configuring Visual Studio Code](https://www.drupal.org/node/2918206/). Here you can find recommended extensions for PHP, Drupal, Twig, Composer, YAML, and JavaScript, including "snippets" for code scaffolding. The doc also provides recommended general editor settings and Drupal code standards configuration.

### phpStorm

[phpStorm](https://confluence.jetbrains.com/display/PhpStorm/Welcome) is a full integrated development environment (IDE) by JetBrains that provides text editing as well as additional tools for debugging your code.

The JetBrains website has [extensive instructions for getting set up with Drupal configuration](https://confluence.jetbrains.com/display/PhpStorm/Drupal+Development+using+PhpStorm#DrupalDevelopmentusingPhpStorm-CoderandPHPCodeSnifferIntegration).

## Review your own code

The easiest way to make sure you’re conforming to coding standards is to use a program like [PHP CodeSniffer](https://github.com/PHPCSStandards/PHP_CodeSniffer/) (phpcs). You can install [Coder](https://www.drupal.org/project/coder), which is a Drupal module that allows you to check your code from the command line using custom rules and PHP CodeSniffer. Here’s an example of what you might see:

Example phpcs output:

```
joe:/var/www/html$ ./vendor/bin/phpcs
E.EE.E..EE 10 / 10 (100%)

FILE: /var/www/html/web/modules/custom/anytown/anytown.module
---------------------------------------------------------------------------------------------------------------------
FOUND 1 ERROR AFFECTING 1 LINE
---------------------------------------------------------------------------------------------------------------------
 119 | ERROR | Description for the @return value is missing
     |       | (Drupal.Commenting.FunctionComment.MissingReturnComment)
---------------------------------------------------------------------------------------------------------------------

FILE: /var/www/html/web/modules/custom/anytown/src/Controller/Attending.php
---------------------------------------------------------------------------
FOUND 1 ERROR AFFECTING 1 LINE
---------------------------------------------------------------------------
 9 | ERROR | Doc comment is empty (Drupal.Commenting.DocComment.Empty)
---------------------------------------------------------------------------
```

Let’s walk through getting this set up to scan your custom code.

### Install phpcs

First, you'll need to install phpcs. This is the command line tool that will scan our code and looking for coding standards violations.

```
composer require --dev squizlabs/php_codesniffer
```

### Install drupal/coder

The contributed [Coder project](https://www.drupal.org/project/coder) contains rules for phpcs that teach it what the Drupal coding standards are.

```
composer require --dev drupal/coder
```

The `drupal/coder` project is not a module, and will be installed into the *vendor/* directory, not the *modules/* directory. The project contains the `Drupal`, and `DrupalPractice` rule sets for phpcs.

- `Drupal`: This one is set of sniffs that conform to the Drupal coding standards.
- `DrupalPractice`: This set contains sniffs for "best practices". Things that are not necessarily coding standards violations, but the community considers it a best practice. For example; A module's .info.yml isn't required to have a `description` key, but it's considered standard to add one.

### Run phpcs using the Drupal standard

To run phpcs using the Drupal standards you need to specify which rules to use, and what code to scan.

Example:

```
./vendor/bin/phpcs --standard=Drupal,DrupalPractice web/modules/my_custom_module/
```

### (optional) Add a *phpcs.xml* configuration file

You can add a *phpcs.xml* configuration file to the root directory of your project, alongside your *composer.json* file. This will contain configuration options that you want phpcs to use by default if you don't specify any others.

Example *phpcs.xml*:

```
<?xml version="1.0"?>
<ruleset name="Project coding standards">

  <!-- Combine these rulesets. -->
  <rule ref="Drupal"/>
  <rule ref="DrupalPractice"/>

  <!-- If no paths are specified check these ones. -->
  <file>./web/modules/custom</file>
  <file>./web/themes/my_custom_theme/</file>

  <!-- Ignore any files in these paths. -->
  <exclude-pattern>*/.git/*</exclude-pattern>
  <exclude-pattern>*/config/*</exclude-pattern>
  <exclude-pattern>*/css/*</exclude-pattern>
  <exclude-pattern>*/js/*</exclude-pattern>
  <exclude-pattern>*/icons/*</exclude-pattern>
  <exclude-pattern>*/vendor/*</exclude-pattern>
  <exclude-pattern>*/node_modules/*</exclude-pattern>
  <exclude-pattern>*rules_export.txt</exclude-pattern>

  <arg name="extensions" value="php,module,inc,install,test,profile,theme,css,info" />

  <!-- For colored cli output -->
  <arg name="colors"/>
  <!-- To show rule names. Equivalent to "phpcs -s" -->
  <arg value="sp"/>

  <!-- Depending on your project, you may need to ignore specific rules until
       they can be fixed one at a time. Here is an example of how to ignore a
       specific rule. -->

  <!-- Class name must be prefixed with the module name. -->
  <!--
  <rule ref="DrupalPractice.General.ClassName.ClassPrefix">
    <severity>0</severity>
  </rule>
  -->

</ruleset>
```

Now, when you run `./vendor/bin/phpcs` with no additional arguments it will default to scanning the *web/modules/custom/* and *web/themes/my\_custom\_theme/* directories. We recommend defaulting to only scanning your custom code, and not code in Drupal core or contributed modules which is only going to end up returning warnings for code that you're not in control of anyway.

Generally, you want to run phpcs every time you make a change to your custom code, and before you commit your code or submit a merge request for a contributed module. This way, you’re always writing clean code, and anyone reviewing your code can concentrate on reviewing it for content, not style. Of course, everyone is human and we all make mistakes. Sometimes you’ll push up a tiny change without running phpcs, and not realize there was a style issue. That’s why team code reviews are so important.

## Team code reviews

If you are working with a team, you have another valuable tool in your arsenal. The most successful teams build in time to review one another’s code. There’s no substitute for code reviews by another person, and you should view them as an essential part of your process. The same is true for reviews on drupal.org as well. When planning time and resources for a project, make sure that there is time set aside for code reviews. When you’re working on contributed projects, make sure you take a look at issues marked "Needs Review" and test them. If you want a way to dive into a project, or just Drupal and contributed work in general, reviewing patches is a great way to get acclimated. You get exposed to other people’s code, and if you find something that needs to be corrected, that will stick with you and you’ll remember it.

Two things to remember when reviewing other people’s code, or when receiving reviews of your own:

1. Treat others as you would like to be treated. Be kind, courteous, respectful, and constructive. Be aware of your tone. It’s easy to come off more harshly than you intended, especially when working quickly. Take just a second to re-read your comments, especially if you’re communicating with someone you’re not acquainted with.
2. Take everything in stride, and don’t take it personally. Those reviewing your code want it to be good, and corrections aren’t a personal attack. This can be especially hard when you start out, but even after years, some comments might hurt your feelings. Don’t dwell on it! Thank them, make the corrections, submit the corrected code, and chances are, they’ll thank you, too.

## Recap

Now you know what code standards are, why they’re important, and how you can get started implementing them in your code.

## Further your understanding

- What IDE or Editor do you use for development? Are you able to configure it to work with Drupal's coding standards?
- Install PHP CodeSniffer and the Coder module and then run it on the files in either a custom module or one downloaded from Drupal.org. What, if any, violations did it point out?
- PHP CodeSniffer comes with two binaries, `phpcs`, and `phpcbf`. What does `phpcbf` do?

## Additional resources

- [Coder module](https://www.drupal.org/project/coder) (Drupal.org)
- [PHP CodeSniffer](https://github.com/PHPCSStandards/PHP_CodeSniffer/) (github.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Drupal Code Standards: Twig](/tutorial/drupal-code-standards-twig?p=2458)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

Drupal Training Resources by Alanna Burke of [Chromatic](https://chromatichq.com) are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://chromatichq.com/blog>.

Clear History

Ask Drupalize.Me AI

close