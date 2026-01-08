---
title: "Concept: Drupal Development Environment"
url: "https://drupalize.me/tutorial/concept-drupal-development-environment?p=3234"
guide: "[[drupal-module-developer-guide]]"
---

# Concept: Drupal Development Environment

## Content

A development environment is any copy of your site that operates separately from the live site. Development environments allow you to make changes, try new modules, write new code, and test new ideas on a copy of your site instead of the real thing. Using a development environment ensures any changes you make happen in a sandbox where you’re not affecting anyone trying to use the live version of your application. As a module developer, it's common practice to set up a copy of your Drupal application on your own computer for development and testing purposes.

In this tutorial we'll learn:

- What a development environment is and why it's needed
- The specific requirements for Drupal, and a recommendation (DDEV) for those seeking a straightforward solution
- Other commonly-used extras that enhance the development experience

By the end of this tutorial you should be able to describe the requirements of a Drupal development environment and know how to get started setting one up for yourself.

## Goal

Know how to get started setting up a Drupal development environment for custom module development.

## Prerequisites

- None.

## What is a development environment?

A development environment in the context of web development, including Drupal, is a setup where you can write, test, and debug code in isolation from the live site. It usually consists of a web server, database, and programming tools that mimic the production environment but allows for safe testing and experimentation. This setup can exist entirely on the local machine, in the cloud, or some combination of the two.

### Why do I need one?

- **Safe testing**: A development environment lets you test new features or updates without affecting your live website.
- **Debugging**: It provides tools to debug your code, ensuring that everything works as expected before going live.
- **Learning and experimentation**: It's a sandbox where you can learn new skills or try out new ideas without any risk.
- **Isolation**: Test features like sending emails, or integrating with payment gateways, without performing real transactions.

## Requirements of a Drupal development environment

The following is a list of the minimum set of services and tools you'll want to have in your development environment:

1. **Web server with PHP runtime**: Typically Apache or Nginx to serve Drupal pages, with a PHP runtime that meets the [PHP version requirements](https://www.drupal.org/docs/getting-started/system-requirements/php-requirements) for your version of Drupal. ([Requirements](https://www.drupal.org/docs/getting-started/system-requirements/web-server-requirements))
2. **Database**: MySQL or MariaDB to store Drupal's content and configuration data that meets the version requirements for your version of Drupal. ([Requirements](https://www.drupal.org/docs/getting-started/system-requirements/database-server-requirements))
3. **Composer**: Drupal uses the PHP package manager [Composer](https://getcomposer.org/). It's required to install Drupal and its dependencies.
4. **Your Drupal codebase**: The code for your project. Usually a Git repository with a combination of Composer required dependencies like Drupal core itself, and the custom code that is specific to your application.
5. **Code editor/IDE**: Tools like Visual Studio Code or PHPStorm to write and debug code.
6. **Git**: Version control for your code.

View a list of documented environment requirements for different versions of Drupal at [System requirements](https://www.drupal.org/docs/getting-started/system-requirements).

## Recommended Drupal development environment

For those seeking a straightforward recommendation, [DDEV](https://ddev.readthedocs.io/en/stable/) is a Docker-based tool that's easy to set up and use. It provides a per-project environment, making it suitable for working on multiple Drupal projects. DDEV automatically handles the setup of Apache, MySQL, PHP, and other necessary components, streamlining the process of getting your development environment operational. It's commonly used by members of the Drupal community and is well-supported.

After we [set up our development environment](https://drupalize.me/tutorial/set-your-development-environment), the rest of this guide will assume the use of DDEV. Any environment will work, but you might need to modify commands depending on your setup.

## Recap

In this tutorial, we explained why a development environment is necessary. It ensures that you can test new features, debug a problem, learn or experiment, and run test processes in isolation. Your development and testing work shouldn't affect the live site or its users, which is why we use a development environment. A development environment's components include a web server with a PHP runtime, database, Composer, a Drupal codebase, code editor or IDE, and Git for version control.

While it's possible to create a custom environment that meets Drupal's system requirements, the actively-supported tool, DDEV, provides a straightforward, Docker-based solution that meets all those requirements, works on all major operating systems, and robustly supports Drupal. We recommend DDEV as a local development environment, and we'll be using it in this guide.

## Further your understanding

- How does a development environment differ from a production environment?
- What are the requirements of a Drupal development environment? And what are some potential extras that might make development easier for you personally?

## Additional resources

- [Official DDEV Documentation](https://ddev.readthedocs.io/en/stable/) (ddev.readthedocs.io)
- [Drupal Development Tools](https://www.drupal.org/docs/develop/development-tools) (Drupal.org)
- [Setting Up a Local Development Environment](https://www.drupal.org/docs/develop/local-server-setup) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Finding Drupal Documentation](/tutorial/concept-finding-drupal-documentation?p=3234)

Next
[Concept: Tools for Module Developers](/tutorial/concept-tools-module-developers?p=3234)

Clear History

Ask Drupalize.Me AI

close