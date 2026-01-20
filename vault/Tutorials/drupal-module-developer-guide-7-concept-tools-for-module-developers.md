---
title: "Concept: Tools for Module Developers"
url: "https://drupalize.me/tutorial/concept-tools-module-developers?p=3234"
guide: "[[drupal-module-developer-guide]]"
order: 7
---

# Concept: Tools for Module Developers

## Content

There are a number of tools that help make your Drupal development experience enjoyable and efficient. They aren't required, only recommended. We'll introduce 5 tools: PhpStorm, Devel, Xdebug, Drush, and the Stage File Proxy module. Each tool serves a unique purpose, from streamlining coding processes to improving local site performance.

In this tutorial we'll learn:

- The purpose and benefits of using PhpStorm in Drupal development.
- How Devel provides valuable debugging and development assistance.
- The role of Xdebug in code debugging and analysis.
- The importance of Drush for command-line site management.
- How the Stage File Proxy module optimizes local development environments.

By the end of this tutorial, you should be able to understand how these tools contribute to the Drupal module developer experience.

## Goal

Introduce 5 tools designed to improve the Drupal module developer experience.

## Essential tools for Drupal development

This list includes commonly used and recommended tools for efficient Drupal module development. While these are some of the most widely used tools in Drupal development, there are many others available within the Drupal community. Links to topic pages list Drupalize.Me and external resources where you can learn more.

### PhpStorm

Topic: [PhpStorm](https://drupalize.me/topic/phpstorm)

PhpStorm is a popular Integrated Development Environment (IDE) among Drupal developers. It offers a comprehensive suite of coding tools, including intelligent code assistance, debugging support, and seamless integration with version control systems. PhpStorm is known for its deep understanding of PHP and Drupal-specific code, which helps in writing code, identifying and fixing errors quickly, navigating through code efficiently, and automating routine tasks. Its robustness makes it a top choice for professional Drupal development.

If you use DDEV for your local environment, the [DDEV Integration](https://plugins.jetbrains.com/plugin/18813-ddev-integration) plugin allows you to use common features from within the IDE, and provides shortcuts for setting up and using Xdebug. To use it, you will need to configure PhpStorm to point to DDEV's private docker-compose executable. See DDEV's documentation, [PhpStorm Setup > Prerequisite](https://ddev.readthedocs.io/en/latest/users/install/phpstorm/#prerequisite) for instructions.

### Devel

Topic: [Devel](https://drupalize.me/topic/devel)

The Devel module provides a suite of utilities and functions that assist in the development and debugging of Drupal sites. Devel allows you to configure variable inspection tools and web-based interfaces for executing PHP scripts or SQL queries. Its dummy content and user generator module, Devel Generate, makes it ideal for testing.

### Xdebug

Topic: [Xdebug](https://drupalize.me/topic/xdebug)

Xdebug significantly enhances PHP's default debugging capabilities. It integrates with many IDEs, including PhpStorm, allowing developers to step through code, inspect variables, and interactively debug PHP scripts. Xdebug's profiling features are invaluable for identifying performance bottlenecks in code.

### Drush

Topic: [Drush](https://drupalize.me/topic/drush)

Drush, short for the *Drupal Shell*, is a command-line utility that streamlines many Drupal administrative tasks. From managing modules and themes to interacting with the database, Drush offers a range of commands that make site maintenance more efficient. It's particularly useful for scripting and automating repetitive tasks, enabling developers to manage their Drupal sites quickly and effectively.

This guide will assume you have Drush installed, and will recommend the use of Drush commands to complete certain tasks.

### Stage File Proxy

Project: [Stage File Proxy Module](https://www.drupal.org/project/stage_file_proxy)

The Stage File Proxy module is a practical tool for local Drupal development. It saves disk space and bandwidth by serving file assets (like images and documents) from a production environment instead of requiring them to be stored locally. This approach is beneficial when working with large sites, as it allows developers to work on a lightweight version of the site, which speeds up the development process.

## Recap

In this tutorial, we introduced 5 tools that can improve your Drupal developer experience: PhpStorm, Devel, Xdebug, Drush, and Stage File Proxy. While these tools are not required, they can help you become an efficient and effective module developer as you code, troubleshoot, and work locally on a Drupal site.

## Further your understanding

- What features in PhpStorm make it particularly suitable for Drupal development?
- After installing the Devel module, visit the configuration page and configure your variable dumping tool. You may want to install Kint with Composer so that you can select it as your tool of choice.
- What is the use case for the Stage File Proxy module?

## Additional resources

- [PhpStorm Drupal Development](https://drupalize.me/topic/phpstorm) (Drupalize.Me)
- [Devel Module Overview](https://drupalize.me/topic/devel) (Drupalize.Me)
- [Using Xdebug for PHP Development](https://drupalize.me/topic/xdebug) (Drupalize.Me)
- [Drush Command Line Tool](https://drupalize.me/topic/drush) (Drupalize.Me)
- [Stage File Proxy Module](https://www.drupal.org/project/stage_file_proxy) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Drupal Development Environment](/tutorial/concept-drupal-development-environment?p=3234)

Next
[Set Up Your Development Environment](/tutorial/set-your-development-environment?p=3234)

Clear History

Ask Drupalize.Me AI

close