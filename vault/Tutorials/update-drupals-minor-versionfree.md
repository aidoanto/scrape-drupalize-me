---
title: "Update Drupal's Minor Versionfree"
url: "https://drupalize.me/tutorial/update-drupals-minor-version?p=3281"
guide: "[[keep-drupal-up-to-date]]"
---

# Update Drupal's Minor Versionfree

## Content

Drupal's development has a [regular release cycle](https://www.drupal.org/core/release-cycle-overview) consisting of major, minor, and patch releases. Drupal releases use [semantic versioning](https://drupalize.me/videos/semantic-versioning) for its version numbers. Since we're committed to making sure our tutorials are kept up-to-date with the latest and greatest version of Drupal we figured it would be a good idea if you knew how to keep your Drupal site up-to-date with the latest "point" releases as well.

This tutorial will cover:

- How to determine the type of update
- The standard update procedure
- Update Drupal using Drush
- Update Drupal using Composer

This tutorial won't cover:

- How to perform a major version Drupal upgrade, for example, from Drupal 6 or 7 to the latest version of Drupal. For that, see our guide, [Learn to Migrate to Drupal](https://drupalize.me/guide/learn-migrate-drupal).

## Goal

Update Drupal core from one minor version or patch release to another, either manually or via Composer.

## Prerequisites

- We strongly recommend that you read through the entire tutorial before taking any action.
- If you used `drupal-composer/drupal-project` to install Drupal versions previous to 8.8.x, use this tutorial instead: [Update Drupal from Versions Prior to 8.8.x using Composer](https://drupalize.me/tutorial/update-drupal-versions-prior-88x-using-composer)

Note: This tutorial applies to Drupal 8.8.x and above, including the latest version of Drupal.

## Quick reference

Here's the quick version that assumes you've been sync'ing config and understand what commands [drush deploy](https://www.drush.org/12.x/deploycommand/) runs.

If you're using `drupal/core-recommended`:

```
composer update drupal/core-recommended --with-dependencies
drush deploy -y
```

If you're not using `drupal/core-recommended`:

```
composer update drupal/core --with-dependencies
drush deploy -y
```

Keep reading below for detailed instructions about the minor or patch version upgrade process.

## Overview

Updating Drupal's minor version requires the following steps:

1. Make a backup of your existing database
2. Update all Drupal core code to the latest version
3. Perform any additional steps noted in the release notes
4. Execute any require database updates via *update.php*

Depending on how you installed Drupal core the exact steps are different:

- Follow [the steps in Method #1: Update Drupal with Composer](#method1) if you installed Drupal core using Composer
- Follow [the steps in Method #2: Manual update procedure](#method2) if you installed Drupal core by downloading the code from Drupal.org.

## Understanding releases of Drupal

To understand what kind of effort it will take to get your site up-to-date, you should understand Drupal's version numbering scheme and the difference between a major upgrade and a minor update.

### Version numbers in Drupal releases

A Drupal release's version number comprises the major, minor, and patch versions. For example, for Drupal 10.1.7:

- The first digit, `10`, is the major version.
- The second digit, `1`, is the minor version.
- The third digit, 7, is the patch level.

New patch-level releases are available monthly, while minor versions are currently released every six months. [Major version upgrades will be released every 2 years](https://www.drupal.org/blog/drupal-10-will-be-supported-until-the-release-of-drupal-12-in-mid-late-2026).

### Major upgrade or minor update?

It's important to understand difference between *upgrading* and *updating*. Typically, a transition between major versions, say between Drupal 7 and Drupal 10, requires an *upgrade*. This could require a *migration*. Unlike an update, performing an upgrade can require a lot of effort. Since the migration process can be complex, we have an entire [guide including 3 courses of tutorials devoted to the migrating your site to Drupal](https://drupalize.me/guide/learn-migrate-drupal). This guide includes in-depth guidance on *upgrading* from Drupal 6 or 7 to the latest major version of Drupal.

Drupal's release cycle includes a *minor version* release every 6 months. This timeline helps organizations build their update plan into their development process. Minor releases may contain new features, but maintains a backward-compatibility layer that extends to the next major release. As a result, minor version updates are usually a relatively straightforward process.

Patch releases may occur monthly, but only contain security and bug fixes. As such, the impact of a patch release is genuinely quite minimal, but may be important to address in a timely fashion, especially in the case of a security release. The process for updating Drupal is the same for both minor and patch releases.

### Evaluating a Drupal release

Once you've determined that what you want to do is update your Drupal site's minor or patch version, it's a good idea to read the release notes, or a [Drupal blog](https://www.drupal.org/blog) post about the release. These will provide a high-level overview of the changes that have gone into the new version. With this knowledge in hand you're ready to begin the actual mechanics of the update process. There are several methods of updating your site outlined below. While I would recommend being familiar with all the methods, they accomplish the same thing.

### Tip: Backup before you update

Regardless of which method you wind up using to update your Drupal site it is always a good idea to make sure you have a fresh backup available. Functional Drupal sites are composed of 3 components: code, files and a database. Hopefully the codebase for your site is already stored in some type of version control system. If it isn't, our [Introduction to Git](https://drupalize.me/series/introduction-git-series) series would be a good place to start. There are several techniques you could use to back up the public (and private) files directories and your site's database. The [Backup and Migrate module](https://www.drupal.org/project/backup_migrate) can be used to create and download backups right from within your web browser.

## Method #1: Update Drupal with Composer

If you're using Composer to manage your codebase follow these steps to update to the latest version of Drupal core.

This also assumes you're using Drush, but you could also perform the same tasks via the UX using the methods outlined above.

## Updating a pinned (specified) version of Drupal

Check your project's *composer.json* file to see if `drupal/core-recommended`, `drupal/core-composer-scaffold`, or `drupal/core-project-message` have a **pinned** version constraint (for example, `11.0.1`), instead of a semantic version compatible (`^`) constraint, for example, `^11.0`. To update a pinned version, you will either need to run the `composer update` commands and specify a new pinned version, or unpin your core version before updating.

Learn more on Drupal.org

- [Update to a specific version of core](https://www.drupal.org/docs/updating-drupal/updating-drupal-core-via-composer#s-update-to-a-specific-version-of-core)
- [Unpinning from a specific version of core](https://www.drupal.org/docs/updating-drupal/updating-drupal-core-via-composer#s-unpinning-from-a-specific-version-of-core)

### Make a backup

Start by making a backup of your site's database. If you don't already know how, [see the resources in our Backup Your Drupal Site topic](https://drupalize.me/topic/back-your-drupal-site).

### Put your site into maintenance mode

Turn on maintenance mode using Drush, or via the UI by using the *Manage* menu to navigate to *Configuration* > *Development* (*admin/config/development/maintenance*).

```
drush state:set system.maintenance_mode 1
drush cache:rebuild
```

### Verify the required updates

Verify which dependencies will be updated with the following command:

```
composer outdated "drupal/*"
```

This will result in output like the following indicating which version is currently installed, and which new version is recommended:

```
drupal/core                   8.8.0 8.8.1 Drupal is an open source content management platform powering millions of websites and applications.
...
```

Here `8.8.0` represents the current version, and `8.8.1` represents the version you'll have after updating.

### Update Drupal core and dependencies

Note: The following steps will also work for minor and patch versions of Drupal as well.

Are you depending on `drupal/core` package or `drupal/core-recommended`? You'll need to know this to proceed. Open the *composer.json* file in the root of your project and in the `"require"` section you should see one of either `"drupal/core": "^8.8"` or `"drupal/core-recommended": "^8.8"`.

Use Composer to update whichever of the packages you have installed and any other dependencies that also need to be updated:

```
composer update drupal/core-recommended --with-dependencies
```

If this is successful you'll see a list of all the updates that happened:

```
Loading composer repositories with package information
Updating dependencies (including require-dev)
Package operations: 0 installs, 3 updates, 0 removals
  - Updating pear/archive_tar (1.4.8 => 1.4.9): Loading from cache
  - Updating drupal/core (8.8.0 => 8.8.1): Loading from cache
  - Updating drupal/core-recommended (8.8.0 => 8.8.1)
```

If you specified the wrong package, e.g.) `drupal/core` but your project uses `drupal/core-recommended` you'll see output like the following indicating there is nothing to update:

```
Loading composer repositories with package information
Updating dependencies (including require-dev)
Nothing to install or update
```

If this is unsuccessful, remove Drush with `composer remove drush/drush` and try again. If the update successfully runs, run `composer require drush/drush` to reinstate Drush.

### Run any required database updates

Run any outstanding database updates using Drush and then clear the cache:

```
drush updatedb
drush cache:rebuild
```

### Take your site out of maintenance mode

Maintenance mode can be disabled using Drush, or via the UI following the steps outlined above.

```
drush state:set system.maintenance_mode 0
drush cr
```

## Method #2: Manual update procedure

Use this method if you are not using Composer to manage your projects dependencies. This is likely the case if you started by downloading the *.zip* or *.tar.gz* file directly from Drupal.org when first installing Drupal core.

**Note:** If you started your Drupal project with 8.8.0 or greater the downloaded files already contain the configuration necessary to use Composer and you can follow the process for using Composer outlined below to update if you would like.

### Make a backup

Start by making a backup of your site's database. If you don't already know how [learn more about creating a backup](https://drupalize.me/topic/back-your-drupal-site).

### Put your site into maintenance mode

Using the *Manage* administrative menu, navigate to *Configuration* > *Development* (*admin/config/development/maintenance*), select the box to turn on maintenance mode, and submit the form.

Image

![Maintenance mode UI](../assets/images/maintenance_mode.png)

### Remove old code

With your site in maintenance mode you're now ready to update the codebase to the new release. The following steps should be run on a local development or staging site and then deployed to the live site using your regular deployment process.

After changing directories to the root of your Drupal site, remove the *core* and *vendor* directories, as well as any top level files you haven't added manually.

```
rm -rf core vendor
rm -f *.* .*
```

### Apply new code and patches

Next move the Drupal files you've downloaded for the new release into place.

With the new Drupal code in place you can now reapply any modifications you have made to files like *.htaccess*, *robots.txt*, *composer.json* or any patches you've manually applied. Our projects typically include a text file that lists these modifications or patches for quick and easy reference during an update.

### Update the database

Run updates using Drush:

```
drush updatedb
drush cache:rebuild
```

Or alternatively, use the UI:

By default, access to the *update.php* file in your codebase requires the *Administer software updates* permission. In order to run that script from a browser to complete our site update you'll need to sign in as a user with that permission. You can also explicitly allow access by editing your *settings.php*. In your *settings.php* file locate the `update_free_access` setting, change it to `TRUE` and save the file. Now you can visit *yoursite.com/update.php* in a browser and run the database update script.

Image

![Pending update](../assets/images/update_pending.png)

Once the update script has finished you'll either see confirmation that it has been completed successfully, or a series of logged errors where the update failed.

Image

![Successful update](../assets/images/update_complete.png)

With the update complete don't forget to flip the `update_free_access` setting back to `FALSE` to prevent others from being able to access your site's *update.php* through a browser.

```
$settings['update_free_access'] = FALSE;
```

### Take your site out of maintenance mode

Using the *Manage* administrative menu, navigate to *Configuration* > *Development* (*admin/config/development/maintenance*), uncheck the box to turn off maintenance mode, and submit the form.

Ta-da! You've just updated your Drupal site.

## Recap

In this tutorial we explained the difference between *updates* and *upgrades*, and *minor* versus *major* versions. Then we demonstrated 2 different approaches to updating Drupal core from 1 minor version to another. After completing one of these 2 processes you'll have performed a minor or patch update for your Drupal site.

## Further your understanding

- Learn more about how Composer works and how to manage your Drupal code base with it in our series [Introduction to Composer for Drupal Users](https://drupalize.me/series/introduction-composer-drupal-users).

## Additional resources

- [Drupal core release cycle overview](https://www.drupal.org/core/release-cycle-overview) (Drupal.org)
- [Updating Drupal core via Composer](https://www.drupal.org/docs/updating-drupal/updating-drupal-core-via-composer) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Install Drupal Locally with DDEV](/tutorial/install-drupal-locally-ddev?p=3281)

Clear History

Ask Drupalize.Me AI

close