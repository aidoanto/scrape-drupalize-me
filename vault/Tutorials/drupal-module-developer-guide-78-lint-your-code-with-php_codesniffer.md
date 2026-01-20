---
title: "Lint Your Code with PHP_CodeSniffer"
url: "https://drupalize.me/tutorial/lint-your-code-phpcodesniffer?p=3246"
guide: "[[drupal-module-developer-guide]]"
order: 78
---

# Lint Your Code with PHP_CodeSniffer

## Content

Tools like PHP\_Codesniffer (phpcs) can be used to help ensure your code adheres to Drupal's coding standards. As a module developer, you should use phpcs and its Drupal-specific rule sets on all custom module code.

In this tutorial, we'll:

- Learn about PHP\_Codesniffer (phpcs).
- Install PHP\_Codesniffer and the Drupal-specific rules.
- Use phpcs to lint our custom code.

By the end of this tutorial, you should be able to use PHP\_Codesniffer to help automate the process of adhering to Drupal's coding standards.

## Goal

Install and run phpcs and fix any coding standards violations in our custom module.

## Prerequisites

- [Concept: Coding Standards](https://drupalize.me/tutorial/concept-coding-standards)

## Video tutorial

Sprout Video

## Using PHP\_Codesniffer (phpcs)

[PHP\_Codesniffer](https://github.com/PHPCSStandards/PHP_CodeSniffer/), or *phpcs*, is a library that tokenizes PHP, JavaScript and CSS files, and detects violations of a defined set of coding standards. This process is commonly referred to as *linting*. It is widely used and supported in both Drupal and the broader PHP communities.

To use PHP\_Codesniffer for Drupal code you need to install the appropriate rule set. There are 2 rule sets for Drupal:

- `Drupal`: This rule set enforces the general standards
- `DrupalPractice`: This rule set is aimed at common mistakes made by module developers

**Note**: PHP\_Codesniffer can be installed as a Composer global in your home directory. This way you can configure your IDE with the path to phpcs once, and not have to update it for every project. See the documentation, [Installing Coder](https://www.drupal.org/node/1419988), for those instructions.

In this tutorial, we'll install PHP\_Codesniffer as a project dev-dependency and use it to lint the code in the 2 custom modules we've written in this guide.

### Install `drupal/coder`

The [Drupal Coder](https://www.drupal.org/project/coder) project contains the rules that tell PHP Codesniffer (phpcs) about the Drupal coding standards. Installing it will also install phpcs.

```
composer require --dev drupal/coder
```

### Run phpcs

Run `phpcs` and tell it to use the Drupal standards:

```
./vendor/bin/phpcs --standard=Drupal,DrupalPractice web/modules/custom/anytown/
```

The above command will check the code in the *anytown* module for coding standards violations.

### Optionally add a project specific phpcs.xml file

You can simplify running `phpcs` by adding a project-specific *phpcs.xml* file to the root of your Git repository (alongside the project's *composer.json* file).

Example *phpcs.xml*:

```
<?xml version="1.0"?>
<ruleset name="Anytown coding standards">

  <!-- Combine these rulesets. -->
  <rule ref="Drupal"/>
  <rule ref="DrupalPractice"/>

  <!-- If no paths are specified check these ones. -->
  <file>./web/modules/custom</file>
  <file>./web/themes/contrib/honey/</file>

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

This configuration file tells `phpcs` to look in *./web/modules/custom* and *./web/themes/contrib/honey* for code to examine with the `Drupal` and `DrupalPractice` rule sets. It's a good idea to scan any custom code, but ignore code installed with Composer.

With this configuration in place you can run it like this:

```
./vendor/bin/phpcs

# Or for automatic fixes.
./vendor/bin/phpcbf
```

And if you commit the *phpcs.xml* file to your Git repository everyone on the team will be using same settings.

## Recap

In this tutorial, we learned how to install PHP\_Codesniffer and the Drupal coding standards rules. Then used the `phpcs` utility to examine the custom code in our project for any violations.

## Further your understanding

- Consider adding a Composer `script`, so you can run linters on your code with `composer run code-sniff`.
- How will you and your team incorporate coding standards reviews into your process?

## Additional resources

- [Installing Coder](https://www.drupal.org/node/1419988) (Drupal.org)
- [PHP\_Codesniffer](https://github.com/PHPCSStandards/PHP_CodeSniffer/) (github.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Coding Standards](/tutorial/concept-coding-standards?p=3246)

Next
[Concept: Update Hooks](/tutorial/concept-update-hooks?p=3246)

Clear History

Ask Drupalize.Me AI

close