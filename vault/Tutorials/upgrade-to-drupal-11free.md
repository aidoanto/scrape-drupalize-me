---
title: "Upgrade to Drupal 11free"
url: "https://drupalize.me/tutorial/upgrade-drupal-11?p=3282"
guide: "[[keep-drupal-up-to-date]]"
---

# Upgrade to Drupal 11free

## Content

There’s no one-size-fits-all path to upgrade from Drupal 10 to Drupal 11, but there is a set of common tasks that everyone will need to complete.

In this tutorial we’ll:

- Explain the differences between Drupal 10 and Drupal 11 that affect the upgrade path.
- Walk through the high-level steps required to upgrade from Drupal 10 to Drupal 11.
- Provide resources to help you create an upgrade checklist and start checking items off the list.

By the end of this tutorial you should be able to:

- Explain the major differences between Drupal 10 and 11.
- Audit your existing Drupal 10 projects for Drupal 11 readiness, and estimate the level of effort involved.
- Start the process of upgrading your site from Drupal 10 to Drupal 11.

## Goal

Create a Drupal 11 upgrade checklist, and understand what’s required to complete the items on the list.

## Prerequisites

- [What Is Deprecated Code?](https://drupalize.me/tutorial/what-deprecated-code)
- You may need to first [Update Drupal's Minor Version](https://drupalize.me/tutorial/update-drupals-minor-version) to ensure your site is on Drupal 10.3.x or higher.

## Drupal 11 released August 2, 2024

Drupal 11 was released on August 2, 2024. [Learn more about what's included in Drupal 11](https://www.drupal.org/about/11) and read the [Drupal 11.0.0 release notes](https://www.drupal.org/project/drupal/releases/11.0.0).

Use [Upgrade Status module](https://www.drupal.org/project/upgrade_status) on your Drupal 10 site to help you plan your upgrade. This module provides a report of what modules on your site have a Drupal 11-compatible release.

**Note:** Your site must be on **Drupal 10.3.0 or later** to upgrade to Drupal 11. Update your Drupal 10.x site to the latest version of Drupal 10.3.x or later before upgrading to Drupal 11. See [Update Drupal's Minor Version](https://drupalize.me/tutorial/update-drupals-minor-version).

## Quickstart

Here's the quick version; keep reading below for more details.

```
composer require 'drupal/core-recommended:^11' 'drupal/core-composer-scaffold:^11' 'drupal/core-project-message:^11' --update-with-dependencies --no-update
# If you have drupal/core-dev installed
composer require 'drupal/core-dev:^11' --dev --update-with-dependencies --no-update
# If you have Drush installed (check recommended version)
composer require 'drush/drush:^13' --no-update
# Now, actually perform the update to the code itself.
composer update

# Then run any updates.
drush cr -y
drush updb

# Export configuration changes (and don't forget to commit the changes).
drush cex -y
```

## Differences between Drupal 10 and Drupal 11

From a technical perspective Drupal 11.0.0 is Drupal 10.3.0 with all [deprecated code](https://drupalize.me/tutorial/what-deprecated-code) removed.

Drupal 11 also includes updates to many of Drupal core’s dependencies, including CKEditor, Symfony, Twig, jQuery, and [others](https://www.drupal.org/project/drupal/releases/11.0.0). If you’ve got code in your project that relies on an older version of these dependencies, that code will need to be updated, too.

### Notable 3rd-party dependency updates

| Drupal 10 | Drupal 11 |
| --- | --- |
| CKEditor 5.x | CKEditor 5 v42.0.2 |
| Symfony 6.x | Symfony 7.1.1 |
| Twig 3.5.0 | Twig 3.9.3 |
| jQuery 4.x | jQuery 4.0.0-beta2 |

### Replace or uninstall deprecated core modules

Core modules that were marked as deprecated in Drupal 10 were removed in Drupal 11 and are now considered obsolete in Drupal 11. If your Drupal 10 site is using a deprecated core module, you should switch to a module that is compatible with Drupal 11. [Upgrade Status](https://www.drupal.org/project/upgrade_status) module can give you recommendations on alternative modules. In most cases, the deprecated core module was ported to a contributed project. And so, you can install the ported contributed module as a replacement. If you have a deprecated module installed but your site is not using it, you should uninstall it before attempting to upgrade.

#### Removed modules

These core modules were deprecated in Drupal 10 and removed in Drupal 11.

- [Actions UI](https://www.drupal.org/docs/core-modules-and-themes/deprecated-and-obsolete#s-actions-ui)
- [Activity Tracker](https://www.drupal.org/docs/core-modules-and-themes/deprecated-and-obsolete-modules-and-themes#s-activity-tracker)
- [Book](https://www.drupal.org/docs/core-modules-and-themes/deprecated-and-obsolete-modules-and-themes#s-book)
- [Forum](https://www.drupal.org/docs/core-modules-and-themes/deprecated-and-obsolete-modules-and-themes#s-forum)
- [Statistics](https://www.drupal.org/docs/core-modules-and-themes/deprecated-and-obsolete-modules-and-themes#s-statistics)
- [Tour](https://www.drupal.org/docs/core-modules-and-themes/deprecated-and-obsolete-modules-and-themes#s-tour)

Learn more about [deprecated and obsolete extensions and what to do if your site uses them](https://www.drupal.org/docs/core-modules-and-themes/deprecated-and-obsolete).

## When should I upgrade to Drupal 11?

Short answer: when your code is ready.

The primary consideration should be whether the contributed modules you rely on, and your own custom modules, are Drupal 11 compatible. Once they are, there is no reason to not upgrade.

If you're using Drupal 10 [you have until mid-late 2026](https://www.drupal.org/blog/drupal-10-will-be-supported-until-the-release-of-drupal-12-in-mid-late-2026) to complete your upgrade. At that point, Drupal 12 will be released, Drupal 10.5.x will be unsupported, and Drupal 10 will have reached its end-of-life. There is also the [current Drupal 7 end-of-life date: January 5, 2025](https://www.drupal.org/psa-2023-06-07).

Refer to the [Drupal core release schedule](https://www.drupal.org/about/core/policies/core-release-cycles/schedule) for details and potential updates to these dates.

## Drupal 11 upgrade checklist

Make sure you can check off all the items in the list before you upgrade to Drupal 11.x:

### Update to Drupal 10.3.x (or later)

Before you can upgrade your site to Drupal 11 it needs to be on **10.3.0 or later**. Update your site to the latest release of Drupal 10 before upgrading to Drupal 11.

If you need to update your Drupal 10 site, first [learn how to perform a minor version update](https://drupalize.me/tutorial/update-drupals-minor-version), then come back to this tutorial.

### Update all your contributed projects

**Important note:** You should update all your contributed modules and themes to Drupal 11 compatible versions while you're still on Drupal 10.

It's a good idea to update all your contributed modules and themes to their latest versions as well. Before you can upgrade Drupal core to version 11, you'll need to ensure that all of your contributed projects are **already Drupal 11 compatible**. In most cases this will mean updating to the latest version. In some cases this may require additional work if the module isn't already Drupal 11 ready.

- [13.6 Updating a Module](https://drupalize.me/tutorial/user-guide/security-update-module)
- [13.7 Updating a Theme](https://drupalize.me/tutorial/user-guide/security-update-theme)

Look at the project's page on Drupal.org for more details about compatibility:

Image

![Screenshot of project info data from the Consumers project page with info about Drupal 10 highlighted](/sites/default/files/styles/max_800w/public/tutorials/images/drupal11-project-info-example.png?itok=JeWkqm6J)

Acquia has created [a useful tool for checking compatibility](https://dev.acquia.com/drupal11/deprecation_status).

These are good for getting an estimate of what's going to be involved for your project.

**Tip**: Check *Extend* > *Uninstall* for any deprecated modules (they will be listed at the top).

#### Use Upgrade Status module

When you're ready to start working on the Drupal 11 readiness of the modules installed on your site, use the [Upgrade Status](https://www.drupal.org/project/upgrade_status) module on your **current Drupal 10 site** to generate a report. Use the 4.x version for Drupal 10 to 11 upgrades.

See the [Upgrade Status](https://www.drupal.org/project/upgrade_status) project page for instructions on how to update development dependencies and download the project with Composer.

After downloading the module with Composer, install the module with `drush en upgrade_status` or via the *Extend* administrative page.

Use the *Manage* administrative menu, navigate to *Reports* > *Upgrade status* to see the report and take action.

Image

![Screenshot of an example Upgrade Status report](/sites/default/files/styles/max_800w/public/tutorials/images/upgrade_status_example_report_d11.png?itok=U5Ft3sbA)

If a module isn't Drupal 11 compatible you've got a few options:

- Update it yourself. This is similar to updating custom code. (See below.)
- Wait for a future release of an updated Drupal 11-compatible version.
- Hire someone to do the updates for you.

We recommend starting with your custom code. And once that's done, come back to your contributed modules and figure out which ones are the most critical for your project and see what you can do to help update them for Drupal 11. In many cases there's likely a patch already available and waiting for community members to test it out.

### Update your custom code

If your project has custom modules or themes, it's your responsibility to ensure that that code is compatible with Drupal 11. Using an IDE with support for the `@deprecated` annotation can help you identify [deprecated code](https://drupalize.me/tutorial/what-deprecated-code). Drupal core deprecations (and new features) will have change records in [Change records for Drupal core](https://www.drupal.org/list-changes/drupal).

You can use [Upgrade Status](https://www.drupal.org/project/upgrade_status) to scan these projects as well. And then you'll need to remove all use of deprecated APIs. [Learn more about what deprecated code is and how to deal with it](https://drupalize.me/tutorial/what-deprecated-code).

**Tip:** Even if you're not planning to upgrade to Drupal 11 now, you should start doing this. It'll save time in the future, and since Drupal 11 is backward-compatible with Drupal 10.3.0, it shouldn't affect your existing site.

### Verify your hosting meets the new requirements

The [system requirements for Drupal](https://www.drupal.org/docs/system-requirements) have changed. (See also the "Platform requirements changes" heading in the [release notes](https://www.drupal.org/project/drupal/releases/11.0.0).) You'll want to make sure your web server, PHP, and MySQL/MariaDB are all running compatible versions. Upgrade Status will indicate if the **Environment is incompatible** on its report as well. (This is only useful if the environment on which you're running Upgrade Status is the same as the environment in which you'll be hosting your Drupal 11 site.)

### Check the Upgrade Status report

Using the *Manage* administrative menu, navigate to *Reports* > *Upgrade status* and, if necessary, click the *Check available updates* link under the **Gather data** column.

Once you have addressed all blockers to a Drupal 10 upgrade, you will see "N/A" in the **Fix incompatibilities** column and "100%" in the **Relax** column (along with other information).

Image

![Screenshot of Upgrade Status report when site is Drupal 11-ready](/sites/default/files/styles/max_800w/public/tutorials/images/upgrade_status_green_drupal11_ready.png?itok=wNz4n0GB)

## Upgrade Drupal core

Sites running Drupal 10.2.x or earlier **must first update to at least 10.3.x** before updating to Drupal 11. See [Update Drupal's Minor Version](https://drupalize.me/tutorial/update-drupals-minor-version).

The instructions below assume you that your Drupal 10 project is using Composer to manage dependencies, and that you either started from the `drupal/recommended-project` Composer template or you've updated your *composer.json* to use the `drupal/recommended-project`'s approach to scaffolding. If you're unsure, look for entries like `"drupal/core-recommended": "^10.3"`, and `"drupal/core-composer-scaffold": "^10.3"` in your *composer.json* file. This is a good indication that you're using the current recommend approach.

**Note:** Using the `--no-update` flag updates the *composer.json* entries without attempting to resolve and download any files. This allows us to batch updates to projects and avoid a "chicken-or-egg first"-type of issues with shared dependencies. You can also edit the version constraints in *composer.json* manually.

### Update `drupal/core-dev` (if applicable)

If you have the `drupal/core-dev` dependencies installed you'll need to update those with:

```
composer require drupal/core-dev:^11.0 --dev --no-update --update-with-dependencies
```

### Update `drupal/core-*` projects

Then update the `drupal/core-recommended`, `drupal/core-composer-scaffold`, and `drupal/core-project-message` projects:

```
composer require drupal/core-recommended:^11.0 drupal/core-composer-scaffold:^11.0 drupal/core-project-message:^11.0 --no-update --update-with-all-dependencies
```

### Run `composer update`

Then tell Composer to try and resolve and download all the new code:

```
composer update
```

If this is successful, you'll see lines like the following in the output:

```
  - Upgrading drupal/core-dev (10.3.5 => 11.0.5)
  - Upgrading drupal/core (10.3.6 => 11.0.5): Extracting archive
  - Upgrading drupal/core-recommended (10.3.6 => 11.0.5)
```

If you get any errors you'll need to troubleshoot what's causing the issue. We've tried to provide guidance on some common errors below.

### Put your site in maintenance mode

Put your site in maintenance mode before continuing. If you don't, you may end up with a backup you can't revert to.

```
drush state:set system.maintenance_mode 1
drush cache:rebuild
```

Or, using the administrative UI:

- **Maintenance mode**: *Configuration* > *Development* > *Maintenance mode* (*admin/config/development/maintenance*)
- **Clear caches**: *Configuration* > *Performance* (*admin/config/development/performance*)

### Make a backup

Back up the database, as the next steps will make changes to your database schema and are not reversible.

### Deploy your code

Deploy your code per your normal workflow.

### Check for and run database updates

Assuming Composer was successful at upgrading your site's dependencies to Drupal 11, check for database updates. (If Composer was not successful, you need to deal with those errors before continuing. See below for troubleshooting tips.)

Using Drush:

```
drush updatedb
```

Or navigate to */update.php* and navigate through the Drupal database update wizard.

### Take your site out of maintenance mode

After database updates have successfully run, take your site out of maintenance mode and rebuild caches.

```
drush state:set system.maintenance_mode 0
drush cache:rebuild
```

### Celebrate! You've upgraded to Drupal 11!

Congratulations! You've upgraded your site to Drupal 11!

Image

![Screenshot of Available updates page showing Drupal 11.0.5 installed](/sites/default/files/styles/max_800w/public/tutorials/images/available_updates_drupal11.png?itok=GkPmPrVe)

## Troubleshooting a Drupal 10 upgrade to Drupal 11

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

If running `composer update` results in message saying, "Your requirements could not be resolved to an installable set of packages.", there's a good chance that one or more of your contributed modules isn't Drupal 11 compatible. (Or at least the current release version of the project isn't.)

**Solution:** Look for lines like this in the output:

```
- drupal/recurly 1.5.0 requires drupal/core ~8.0 -> satisfiable by drupal/core[8.8.6, 8.0.0, 8.0.0-beta10, ...
```

This indicates that the `drupal/recurly` project requires Drupal 8.x, but we're asking for Drupal 9.x, therefore resulting in an incompatible set of dependencies.

(While this is an example from upgrading from 8 to 9, you may encounter a similar situation for a particular project when you upgrade from 10 to 11.)

If there's a `-dev` version of the module that you know is compatible with Drupal 11 you could try installing that.

Example:

```
composer require drupal/recurly:1.x-dev --no-update
```

If there's a patch in the issue queue see the next tip.

### Problem: Contributed module only has a patch

Often times modules without a Drupal 11-compatible release will have a patch in the issue queue that makes the module work with Drupal 11, but hasn't been committed by the project maintainers yet.

This can result in a sort of race condition, where Composer can't download the required module because it's not presenting as Drupal 11 compatible, so you need to apply a patch, but Composer can't apply the patch, if it can't resolve the dependency tree first.

**Solution:** Try the [Lenient Composer Plugin](https://github.com/mglaman/composer-drupal-lenient).

In the transition from Drupal 8 to 9, a [lenient Composer endpoint](https://drupalize.me/tutorial/install-contributed-module-no-drupal-9-release) was created to remove this barrier. For the same situation for Drupal 9 to 10 and 10 to 11 upgrades, a Composer plugin was created: [Lenient Composer Plugin](https://github.com/mglaman/composer-drupal-lenient).

## Recap

In this tutorial, we looked at what's involved in making the transition from Drupal 10 to Drupal 11. This included going over the differences between the two, auditing your custom and contributed modules for compatibility, learning how to make things Drupal 11 compatible while still using Drupal 10. And then finally upgrading Drupal core once everything else is ready, and some troubleshooting tips for common problems.

## Further your understanding

- Most of the Composer commands above can be replicated by directly editing your *composer.json* file, and then running `composer update`.
- If you're using Drupal 7, upgrading to Drupal 11 still requires a major migration. See our [Learn to Migrate to Drupal guide](https://drupalize.me/guide/learn-migrate-drupal).

## Additional resources

- [Drupal 11.0.0 release notes](https://www.drupal.org/project/drupal/releases/11.0.0) (Drupal.org)
- [Drupal 10 will be supported until the release of Drupal 12 in mid-late 2026](https://www.drupal.org/blog/drupal-10-will-be-supported-until-the-release-of-drupal-12-in-mid-late-2026) (Drupal.org)
- [How to upgrade from Drupal 10 to Drupal 11](https://www.drupal.org/docs/upgrading-drupal/upgrading-from-drupal-8-or-later/how-to-upgrade-from-drupal-10-to-drupal-11) (Drupal.org)
- [Preparing your site to upgrade to a newer major version](https://www.drupal.org/docs/upgrading-drupal/prepare-major-upgrade) (Drupal.org)
- [Deprecated and obsolete extensions](https://www.drupal.org/docs/core-modules-and-themes/deprecated-and-obsolete) (Drupal.org)
- [Use Composer with Your Drupal Project](https://drupalize.me/tutorial/use-composer-your-drupal-project) (Drupalize.Me)
- [Troubleshoot Common Composer Issues](https://drupalize.me/tutorial/troubleshoot-common-composer-issues) (Drupalize.Me)
- [Drupal Lenient Composer Plugin](https://github.com/mglaman/composer-drupal-lenient) (GitHub.com)
- [Changes required for PHPUnit 10 compatibility](https://www.drupal.org/node/3365413) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[What Is Deprecated Code?](/tutorial/what-deprecated-code?p=3282)

Next
[Upgrade to Drupal 10](/tutorial/upgrade-drupal-10?p=3282)

Clear History

Ask Drupalize.Me AI

close