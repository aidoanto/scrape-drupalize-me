---
title: "Install Drush Using Composerfree"
url: "https://drupalize.me/tutorial/install-drush-using-composer?p=2593"
guide: "[[command-line-tools-drupal]]"
order: 10
---

# Install Drush Using Composerfree

## Content

[Drush](https://drush.org/) is the command line shell and Unix scripting interface for Drupal. The most common way to install Drush is to install it on a per-project basis using Composer. We'll walk through the steps to do that, as well as how to make it possible to execute Drush commands without having to specify a full path to the executable every time.

In this tutorial we'll:

- Install Drush
- Verify it worked
- Look at options for adding Drush to your `$PATH`

By the end of this tutorial, you should be able to install Drush and verify that it is working.

## Goal

Install Drush and verify it's working.

## Prerequisites

- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)
- [Install Composer and Try it Out](https://drupalize.me/tutorial/install-composer-and-try-it-out)
- [3.5. Using Composer to Download and Update Files](https://drupalize.me/tutorial/user-guide/install-composer?p=3074)

## Install Drush using Composer

This assumes that your Drupal codebase is managed using Composer. The current recommendation is to install Drush on a per-project basis. This allows for having different versions of Drush installed for different projects. This is a best practice because different versions of Drush are compatible with a particular set of Drupal versions.

For older versions of Drupal and to learn which version of Drush is compatibile with your Drupal version, see the [Drush](https://www.drush.org/) documentation on installing and upgrading Drush.

### Run composer require

From the root directory of your project run the following command:

```
composer require drush/drush
```

Once that's completed run the command `./vendor/bin/drush --version` to verify it worked.

```
./vendor/bin/drush --version
# > Drush Commandline Tool 13.3.1.0
```

## Using the Drush command

The standard way to invoke Drush is by using the full path to the executable. For example, running `./vendor/bin/drush <command>` from the root directory of your Drupal project. How exactly you call the `drush` command will depend on your local environment and its specific configuration.

If you're using DDEV, you can invoke Drush from outside the container with `ddev drush <command>`, or inside the web container (after running `ddev ssh`) with a plain `drush <command>`.

In other local environments, you may need to configure your `$PATH` environment variable to include `./vendor/bin`, to avoid having to type the full path every time.

The important thing to be aware of is that if you copy/paste Drush commands, you might need to adjust the path to the Drush executable for your specific environment.

## Should I install Drush as a development dependency?

You can install Drush with or without the `--dev` flag, and both work for local development.

The distinction becomes important when deploying your code to production. Most build pipelines will run Composer with the `--no-dev` flag like `composer install --no-dev`. This will exclude any `--dev` dependencies from being installed, which is a good thing. When building for a production environment, you should only install the packages necessary for the live site to run.

Drush is generally expected to be present on production because it's often used to clear the cache, import configuration changes, and perform other Drupal site administration tasks.

## Recap

In this tutorial we learned how to use Composer to install Drush.

## Further your understanding

- Run the `drush` command with no arguments to see a list of available Drush commands.

## Additional resources

- [Drush documentation](https://www.drush.org/) (drush.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[What Is Drush?](/tutorial/what-drush-0?p=2593)

Next
[Enable, Update, and Manage Modules and Themes with Drush](/tutorial/enable-update-and-manage-modules-and-themes-drush?p=2593)

Clear History

Ask Drupalize.Me AI

close