---
title: "3.6. Using Composer to Download and Update Files"
url: "https://drupalize.me/tutorial/user-guide/install-composer?p=2368"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
order: 23
---

# 3.6. Using Composer to Download and Update Files

## Content

### Goal

Use Composer to download or update files and dependencies in the core software, or in add-on modules and themes.

### Prerequisite knowledge

[Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools")

### Site prerequisites

If you want to use Composer, it must be installed either on a local development server or your live site. See [Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools").

### Steps

Sprout Video

If you are unable to install the Composer tool on your live server, you can follow the steps in any of the sections below on your local server, and then transfer any updated or added files to your live server. The recommended procedure is to make an archive or zip file of the new and changed directories, transfer the archive to your live server, delete the directories that have changed, and extract the archive. Make sure to check for updates and additions to the following files, in the root of your installation:

- *vendor* directory
- *autoload.php*
- *composer.json*
- *composer.lock*

#### Using Composer to download the core software

Follow these steps if you have not yet downloaded or installed the core software, and you want to use Composer to download both the core software and its external dependencies:

1. At the command line, change to one level above the directory where you want the software to reside.
2. Enter this command, where *mydir* is the directory you want to create:

   ```screen
   composer create-project drupal/recommended-project mydir
   ```
3. The latest release of the core software will be downloaded to the *mydir/web* sub-directory.

#### Using Composer to download a module or theme

Follow these steps if you are already using Composer to manage the core software, and you want to use Composer to add a contributed module or theme with its dependencies.

1. Each time you want to add a contributed module or theme, determine the project’s short name. This is the last part of the URL of the project page; for example, the Geofield module, at <https://www.drupal.org/project/geofield>, has short name `geofield`.
2. To download the contributed module or theme, along with its external dependencies, enter the following command at the root of your site (substituting the short name of the module or theme for `geofield`):

   ```screen
   composer require drupal/geofield
   ```

#### Using Composer to update previously-downloaded files

Follow these steps to update the files for the core software or a contributed module or theme, after having already started to manage dependencies with Composer:

1. Determine the short name of the project you want to update. For the core software, it is *core*. For contributed modules and themes, it is the last part of the URL of the project page; for example, the Geofield module, at <https://www.drupal.org/project/geofield>, has short name `geofield`.
2. If you want to update to the latest stable release, use the following command, substituting the short name of the project to be updated for `geofield`:

   ```screen
   composer update drupal/geofield --with-dependencies
   ```
3. If you need a specific version, determine how to enter the version number you want to update to. For example, for version 8.x-1.16 of a contributed module, you would enter just the 1.16, and for the core software version 9.0.7, you would enter 9.0.7. Then enter the following command at the root of your site (substituting the short name of the project for `geofield` and the correct version number):

   ```screen
   composer require drupal/geofield:1.16
   ```

### Expand your understanding

You can learn more about Composer commands by using Composer’s built-in help system. For example, to learn more about the `create-project` command, enter `composer help create-project` in your command window.

### Additional resources

- [*Drupal.org* community documentation page "Using Composer to manage Drupal site dependencies"](https://www.drupal.org/docs/develop/using-composer/using-composer-to-manage-drupal-site-dependencies)
- [*Drupal.org* community documentation page "Update Drupal core via Composer"](https://www.drupal.org/docs/updating-drupal/update-drupal-core-via-composer)
- [*Drupal.org* community documentation page "Add Composer to an existing site"](https://www.drupal.org/docs/installing-drupal/add-composer-to-an-existing-site)

**Attributions**

Adapted by [Jennifer Hodgdon](https://www.drupal.org/u/jhodgdon), [Hans Fredrik Nordhaug](https://www.drupal.org/u/hansfn), and [Joe Shindelar](https://www.drupal.org/u/eojthebrave) at [Drupalize.Me](https://drupalize.me) from ["Using Composer to manage Drupal site dependencies"](https://www.drupal.org/docs/develop/using-composer/using-composer-to-manage-drupal-site-dependencies), copyright 2000-2026 by the individual contributors to the [Drupal Community Documentation](https://www.drupal.org/documentation).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[3.5. Setting Up an Environment with DDEV](/tutorial/user-guide/install-ddev?p=2368)

Next
[3.7. Running the Interactive Installer](/tutorial/user-guide/install-run?p=2368)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close