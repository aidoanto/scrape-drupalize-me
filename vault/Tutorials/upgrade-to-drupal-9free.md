---
title: "Upgrade to Drupal 9free"
url: "https://drupalize.me/tutorial/upgrade-drupal-9?p=3282"
guide: "[[keep-drupal-up-to-date]]"
---

# Upgrade to Drupal 9free

## Content

There’s no one-size-fits-all path to upgrade from Drupal 8 to Drupal 9, but there is a set of common tasks that everyone will need to complete.

In this tutorial we’ll:

- Explain the differences between Drupal 8 and Drupal 9 that affect the upgrade path.
- Walk through the high-level steps required to upgrade from Drupal 8 to Drupal 9.
- Provide resources to help you create an upgrade checklist and start checking items off the list.

By the end of this tutorial you should be able to explain the major differences between Drupal 8 and 9, audit your existing Drupal 8 projects for Drupal 9 readiness, estimate the level of effort involved, and start the process of upgrading.

## Goal

Create a Drupal 9 upgrade checklist, and understand what’s required to complete the items on the list.

## Prerequisites

- [What Is Deprecated Code?](https://drupalize.me/tutorial/what-deprecated-code)

## Differences between Drupal 8 and Drupal 9

From a technical perspective Drupal 9.0.0 is Drupal 8.9.0 with all the [deprecated code](https://drupalize.me/tutorial/what-deprecated-code) removed. There are no significant schema changes, or feature additions, that would require a complex upgrade. As long as all the code in your project is using the current APIs the transition from Drupal 8.9.0 to Drupal 9.0.0 shouldn’t be any more complex than the move from 8.8.x to 8.9.0.

Image

![Drupal 9 API is Drupal 8 API with deprecated code removed and 3rd party dependencies updated](../assets/images/drupal9-api-graphic.png)

*Credit:* [Gábor Hojtsy](https://slides.com/gaborhojtsy/state-of-drupal9#/4/6)

Drupal 9 also includes major version updates to many of Drupal core’s dependencies, including Symfony and Twig. If you’ve got code in your project that relies on an older version of these dependencies that code will need to be updated, too. This is less likely to impact you directly, but it’s good to be aware of this change.

Also, in Drupal 9, the *Place Blocks* and *SimpleTest* modules have been removed and replaced with *Layout Builder* and *PHPUnit*, respectively.

Since Drupal 9 is Drupal 8.9 with the deprecated code removed, a module that's not using any deprecated APIs, and has added the required content to its info file to declare that it's compatible with Drupal 9, should work with either major version. If you've used Drupal for a while this is new, and not how upgrades have worked in the past. But, it's so much better.

## When should I upgrade to Drupal 9?

Short answer: when your code is ready.

The primary consideration should be whether the contributed modules you rely on, and your own custom modules, are Drupal 9 compatible. Once they are, there is no reason to not upgrade.

If you're using Drupal 8 you have until November 2021 to complete your upgrade. At that point, Drupal 8.9.x will be unsupported and Drupal 8 will have reached its end of life, which is also Symfony 3's end of life. [Drupal 7 community support will be provided until January 5, 2025](https://www.drupal.org/psa-2023-06-07). Read more about [Drupal 9's release date and what it means](https://www.drupal.org/docs/understanding-drupal/drupal-9-release-date-and-what-it-means).

We like this article as a guide to figuring out when to upgrade: [When to Upgrade from Drupal 8 to Drupal 9](https://www.lullabot.com/articles/when-upgrade-drupal-8-drupal-9)

## Drupal 9 upgrade checklist

Make sure you can check off all the items in the list before you upgrade to Drupal 9.0.0:

### Update to Drupal 8.8.x or 8.9.x

Before you upgrade to Drupal 9 you need to be on the latest version of Drupal 8.

[Learn how to perform a minor version update](https://drupalize.me/tutorial/update-drupals-minor-version).

### Update all your contributed projects

**You should update all your contributed modules and themes to Drupal 9 compatible versions while you're still on Drupal 8.**

It's a good idea to update all your contributed modules and themes to their latest versions as well. Before you can upgrade Drupal core to version 9, you'll need to ensure that all of your contributed projects are **already Drupal 9 compatible**. In most cases this will mean updating to the latest version. In some cases this may require additional work if the module isn't already Drupal 9 ready.

- [13.6 Updating a Module](https://drupalize.me/tutorial/user-guide/security-update-module)
- [13.7 Updating a Theme](https://drupalize.me/tutorial/user-guide/security-update-theme)

Look at the project's page on Drupal.org for more details about compatibility:

Image

![Screenshot of project info data from the Consumers project page with info about Drupal 9 highlighted](../assets/images/drupal9-project-info-example.png)

Acquia has created [a useful tool for checking compatibility](https://dev.acquia.com/drupal9/deprecation_status).

These are good for getting an estimate of what's going to be involved for your project.

When you're ready to start working on the Drupal 9 readiness of the modules installed on your site, use the [Upgrade Status](https://www.drupal.org/project/upgrade_status) on your current site to generate a report. And help fix some common issues. [Learn more about using Upgrade Status](https://drupalize.me/blog/start-drupal-9-readiness-do-list-using-upgrade-status).

If a module isn't Drupal 9 compatible you've got a few options:

- Update it yourself. This is similar to updating custom code. See below.
- Wait for a future release of an updated Drupal 9-compatible version.
- Hire someone to do the updates for you.

We recommend starting with your custom code. And once that's done, come back to your contributed modules and figure out which ones are the most critical for your project and see what you can do to help update them for Drupal 9. In many cases there's likely a patch already available and waiting for community members to test it out.

### Update your custom code

If your project has custom modules or themes, it's your responsibility to ensure that that code is compatible with Drupal 9.

You can use [Upgrade Status](https://www.drupal.org/project/upgrade_status) to scan these projects as well. And then you'll need to remove all use of deprecated APIs. [Learn more about what deprecated code is and how to deal with it](https://drupalize.me/tutorial/what-deprecated-code).

**Tip:** Even if you're not planning to upgrade to Drupal 9 now you should start doing this. It'll save time in the future, and since Drupal 9 is backward-compatible with Drupal 8.9 it shouldn't affect your existing site.

### Verify your hosting meets the new requirements

The [hosting environment requirements for Drupal 9](https://www.drupal.org/docs/9/how-drupal-9-is-made-and-what-is-included/environment-requirements-of-drupal-9) have changed. You'll want to make sure your web server, PHP, and MySQL/MariaDB are all running compatible versions.

## Upgrade Drupal core

These instructions assume you that your Drupal 8 project is using Composer to manage dependencies, and that you either started from the `drupal/recommended-project` Composer template or you've updated your *composer.json* to use the `drupal/recommended-project`'s approach to scaffolding. If you're unsure look for an entries like `"drupal/core-recommended": "^8.8"`, and `"drupal/core-composer-scaffold": "^8.8"` in your *composer.json* file. This is a good indication that you're using the current recommend approach.

You can learn more about making these changes in [Update Drupal from Versions Prior to 8.8.x using Composer](https://drupalize.me/tutorial/update-drupal-versions-prior-88x-using-composer).

**Note:** Using the `--no-update` flag updates the *composer.json* entries, without attempting to resolve and download any files. This allows us to batch updates to projects and avoid a "chicken-or-egg first"-type of issues with shared dependencies. Alternatively, you can edit the version constraints in *composer.json* manually.

If you have the `drupal/core-dev` dependencies installed you'll need to update those:

```
composer require drupal/core-dev:~9.0.0@dev --dev --no-update --update-with-dependencies
```

Then update the `drupal/core-recommended` and `drupal/core-composer-scaffold` projects:

```
composer require drupal/core-recommended:~9.0.0@dev drupal/core-composer-scaffold:~9.0.0@dev --no-update --update-with-dependencies
```

Then tell Composer to try and resolve and download all the new code:

```
composer update
```

If this is successful, you'll see a line like the following in the output:

```
  - Updating drupal/core-dev (8.8.7 => 9.0.0)
```

If you get any errors you'll need to troubleshoot what's causing the issue. We've tried to provide guidance on some common ones below.

## Troubleshooting a Drupal 9 upgrade

### Problem: Permission denied updating files in *sites/default/*

In some cases you may need to modify the permissions on the *sites/default/* directory, and files within it, so that they can be modified.

**Solution:** Set them to something more permissive:

```
chmod 777 web/sites/default
find web/sites/default -name "*settings.php" -exec chmod 777 {} \;
find web/sites/default -name "*services.yml" -exec chmod 777 {} \;
```

**Important!:** Remember to set permissions back after completing the update:

```
chmod 755 web/sites/default
find web/sites/default -name "*settings.php" -exec chmod 644 {} \;
find web/sites/default -name "*services.yml" -exec chmod 644 {} \;
```

### Problem: Composer can't install packages

If running `composer update` results in message saying, "Your requirements could not be resolved to an installable set of packages.", there's a good chance that one or more of your contributed modules isn't Drupal 9 compatible. (Or at least the current release version of the project isn't.)

**Solution:** Look for lines like this in the output:

```
- drupal/recurly 1.5.0 requires drupal/core ~8.0 -> satisfiable by drupal/core[8.8.6, 8.0.0, 8.0.0-beta10, ...
```

This indicates that the `drupal/recurly` project requires Drupal 8.x, but we're asking for Drupal 9.x, therefore resulting in an incompatible set of dependencies.

If there's a `-dev` version of the module that you know is compatible with Drupal 9 you could try installing that.

Example:

```
composer require drupal/recurly:1.x-dev --no-update
```

If there's a patch in the issue queue see the next tip.

### Problem: Contributed module only has a patch

Often times modules without a Drupal 9 compatible release will have a patch in the issue queue that makes the module work with Drupal 9, but hasn't been committed by the project maintainers yet.

This can result in a sort of race condition, where Composer can't download the required module because it's not presenting as Drupal 9 compatible, so you need to apply a patch, but Composer can't apply the patch if it can't resolve the dependency tree first.

There is now an officially supported way to handle this using Composer. See [Install a Contributed Module with No Drupal 9 Release](https://drupalize.me/tutorial/install-contributed-module-no-drupal-9-release).

## Recap

In this tutorial we looked at what's involved in making the transition from Drupal 8 to Drupal 9. This included going over the differences between the two, auditing your custom and contributed modules for compatibility, learning how to make things Drupal 9 compatible while still using Drupal 8. And then finally upgrading Drupal core once everything else is ready, and some troubleshooting tips for common problems.

## Further your understanding

- Most of the Composer commands above can be replicated by directly editing your *composer.json* file, and then running `composer update`.
- If you're using Drupal 7, upgrading to Drupal 9 still requires a major migration. See our [Learn to Migrate to Drupal guide](https://drupalize.me/guide/learn-migrate-drupal).

## Additional resources

- [Guide to Drupal 9](https://drupalize.me/drupal9) (Drupalize.Me)
- [Upgrading from Drupal 8 to Drupal 9 (or higher)](https://www.drupal.org/docs/upgrading-drupal/upgrading-from-drupal-8-to-drupal-9-or-higher) (Drupal.org)
- [Preparing Your Drupal 8 Site for Drupal 9](https://www.lullabot.com/articles/preparing-your-drupal-8-site-drupal-9) (Lullabot.com)
- [Use Composer with Your Drupal Project](https://drupalize.me/tutorial/use-composer-your-drupal-project) (Drupalize.Me)
- [Troubleshoot Common Composer Issues](https://drupalize.me/tutorial/troubleshoot-common-composer-issues) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Upgrade to Drupal 10](/tutorial/upgrade-drupal-10?p=3282)

Next
[Update Drupal from Versions Prior to 8.8.x using Composer](/tutorial/update-drupal-versions-prior-88x-using-composer?p=3282)

Clear History

Ask Drupalize.Me AI

close