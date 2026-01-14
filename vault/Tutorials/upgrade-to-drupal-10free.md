---
title: "Upgrade to Drupal 10free"
url: "https://drupalize.me/tutorial/upgrade-drupal-10?p=3282"
guide: "[[keep-drupal-up-to-date]]"
order: 5
---

# Upgrade to Drupal 10free

## Content

There’s no one-size-fits-all path to upgrade from Drupal 9 to Drupal 10, but there is a set of common tasks that everyone will need to complete.

In this tutorial we’ll:

- Explain the differences between Drupal 9 and Drupal 10 that affect the upgrade path.
- Walk through the high-level steps required to upgrade from Drupal 9 to Drupal 10.
- Provide resources to help you create an upgrade checklist and start checking items off the list.

By the end of this tutorial you should be able to explain the major differences between Drupal 9 and 10, audit your existing Drupal 9 projects for Drupal 10 readiness, estimate the level of effort involved, and start the process of upgrading.

## Goal

Create a Drupal 10 upgrade checklist, and understand what’s required to complete the items on the list.

## Prerequisites

- [What Is Deprecated Code?](https://drupalize.me/tutorial/what-deprecated-code)
- You may need to first [Update Drupal's Minor Version](https://drupalize.me/tutorial/update-drupals-minor-version) to ensure your site is on Drupal 9.4.4 or, at best, the latest version of Drupal 9.5.x.

## Drupal 10 released December 14, 2022

Drupal 10 (and Drupal 9.5.0) was released on December 14, 2022. [Learn more about what's included in Drupal 10](https://www.drupal.org/about/10). Use [Upgrade Status module](https://www.drupal.org/project/upgrade_status) on your Drupal 9 site to help you plan your upgrade.

**Note:** You *can* upgrade to Drupal 10 from Drupal 9.4.4 or later, but **it's best practice to upgrade from the latest version of Drupal 9.5.x to 10**.

## Quickstart

Here's the quick version, keep reading below for more details about dealing with deprecated modules and other gotchas.

```
composer require 'drupal/core-recommended:^10' 'drupal/core-composer-scaffold:^10' 'drupal/core-project-message:^10' --update-with-dependencies --no-update
# If you have drupal/core-dev installed
composer require 'drupal/core-dev:^10' --dev --update-with-dependencies --no-update
# If you have Drush installed (check recommended version)
composer require 'drush/drush:^12' --no-update
# Now, actually perform the update to the code itself.
composer update

# Then run any updates.
drush cr -y
drush updb

# Export configuration changes (and don't forget to commit the changes).
drush cex -y
```

## Differences between Drupal 9 and Drupal 10

From a technical perspective Drupal 10.0.0 is Drupal 9.5.0 with all the [deprecated code](https://drupalize.me/tutorial/what-deprecated-code) removed.

Drupal 10 also includes major version updates to many of Drupal core’s dependencies, including CKEditor, Symfony, and Twig. If you’ve got code in your project that relies on an older version of these dependencies that code will need to be updated, too.

### Updated major 3rd-party dependencies

| Drupal 9 | Drupal 10 |
| --- | --- |
| CKEditor 4 | CKEditor 5 |
| Symfony 4 | Symfony 6 |
| Twig 2 | Twig 3 |

### Updates to themes in Drupal 10

Drupal now ships with a new default theme, Olivero, and a new administrative theme, Claro. Drupal 10 also ships with a Starterkit theme generator, which you can use for new themes. Classy and Stable (base theme) have been deprecated in Drupal 9 and have been removed in Drupal 10; they are available as a contributed projects. In the case of Stable, you can either use the contributed project or the Stable 9 replacement base theme ([change record](https://www.drupal.org/node/3309392)).

#### Removed themes in Drupal 10

These themes were deprecated in Drupal 9 and removed in Drupal 10.

- Bartik
- Classy
- Seven
- Stable

### Updates to modules in Drupal 10

Removed modules were either deprecated in Drupal 9 and removed in Drupal 10 are now obsolete. If your site is using a deprecated core module, you should switch to a supported module. [Upgrade Status](https://www.drupal.org/project/upgrade_status) module can give you recommendations on alternative modules. In most cases, the alternative is a contributed module, in which the core module was ported over as a contributed project.

#### Removed modules

These modules were deprecated in Drupal 9 and removed in Drupal 10.

- Aggregator
- CKEditor (upgrade to CKEditor 5 core module)
- Color
- HAL
- Quick Edit
- RDF

#### Obsolete modules

- Migrate Drupal Multilingual (functionality provided by Migrate Drupal module)
- Entity Reference (can be safely uninstalled; functionality provided by core pre-8.0.0)
- SimpleTest ([Convert Tests from SimpleTest to PHPUnit](https://drupalize.me/tutorial/convert-tests-simpletest-phpunit))

Learn more about [deprecated and obsolete extensions and what to if your site uses them](https://www.drupal.org/docs/core-modules-and-themes/deprecated-and-obsolete).

## When should I upgrade to Drupal 10?

Short answer: when your code is ready.

The primary consideration should be whether the contributed modules you rely on, and your own custom modules, are Drupal 10 compatible. Once they are, there is no reason to not upgrade.

If you're using Drupal 9 you have until November 2023 to complete your upgrade, since that is when Symfony 4 reaches its end-of-life. At that point, Drupal 9.5.x will be unsupported and Drupal 8 will have reached its end-of-life. There is also the [current Drupal 7 end-of-life date, January 5, 2025](https://www.drupal.org/psa-2023-06-07).

## Drupal 10 upgrade checklist

Make sure you can check off all the items in the list before you upgrade to Drupal 10.0.0:

### Update to Drupal 9.4.4 or later

Before you can upgrade your site to Drupal 10 it needs to be on **9.4.4 or 9.5.x**. It's best practice to update to the most recent release of Drupal 9 before upgrading to Drupal 10. But, upgrades from 9.4.4 are supported (in addition to 9.5.x), which is unique to Drupal 9-to-10 upgrades.

If you need to update your Drupal 9 site first [learn how to perform a minor version update](https://drupalize.me/tutorial/update-drupals-minor-version), then come back to this tutorial.

### Update to CKEditor 5

If your site is using CKEditor 4, you will need to first ensure your site is on at least Drupal 9.4.4. (See previous step.) The data upgrade path from CKEditor 4 to 5 is not available before 9.4.4.

- Updating to CKEditor 5 is a manual process, but with upgrade paths.
- Most sites using CKEditor 4 should update to CKEditor 5. See also [Recommendations for Deprecated Modules: CKEditor](https://www.drupal.org/docs/core-modules-and-themes/deprecated-and-obsolete#s-recommendations-for-deprecated-modules).
- If the site has additional installed Drupal modules that provide CKEditor 4 plugins with no CKEditor 5 equivalent as of yet, then you can install the [CKEditor 4 contributed module](https://www.drupal.org/project/ckeditor), as a stop-gap until your CKEditor suite of plugins is CKEditor 5-compatible. See [Upgrade coordination for modules providing CKEditor 4 plugins](https://www.drupal.org/docs/core-modules-and-themes/core-modules/ckeditor-5-module/upgrade-coordination-for-modules-providing-ckeditor-4-plugins). **Note:** CKEditor 4 will reach its end-of-life at the end of 2023.

Having considered the above points, here's how to upgrade from CKEditor 4 to CKEditor 5:

1. Upgrade to Drupal 9.4.4 or higher.
2. Create a database snapshot as a precaution.
3. Update modules that provide additional CKEditor 4 plugins to the latest release of the major version you're on. Modules that have added CKEditor 5 support *should* provide support for *both* CKEditor 4 and 5, and provide an automated upgrade path for toolbar items and plugin settings from 4 to 5.
4. Enable the CKEditor 5 module.
5. Convert text formats to use CKEditor 5. Text formats must be updated one at a time, but switching the editor to **CKEditor 5** will automatically migrate your text format configuration to CKEditor 5.
6. Using the *Manage* administrative menu, navigate to *Configuration* > *Content authoring* > *Text formats and editors*. In the column labeled **Text editor**, you can tell which text formats are using **CKEditor**.
7. For each text format that uses **CKEditor**, under the **Operations** column, select **Configure**.
8. On the configuration page for the text format, under **Text editor**, select **CKEditor 5**. Status messages will appear letting you know what changed.

   Image

   ![Screenshot of Basic HTML text format configuration page after selecting CKEditor 5 as the text editor.](../assets/images/ckeditor5_textformat_update.png)
9. Scroll to the end of the configuration page and click **Save configuration**.

After you have updated all **CKEditor** text formats to **CKEditor 5**, on the *Text formats* administrative page, you should see **CKEditor 5** listed next to each text format you updated.

Image

![Screenshot of text formats page after updating each text format that used CKEditor to use CKEditor 5](../assets/images/textformats_after_ckeditor5_update.png)

#### QA your content

**Important!** After you have manually updated each text format that was using **CKEditor** to use **CKEditor 5**, it's a good idea to check a representative sample of content that uses the new CKEditor 5 text format to ensure that all tags and content are intact.

#### Uninstall CKEditor (deprecated)

After you have ensured your site's text format updates were a success, uninstall the deprecated CKEditor module:

1. Using the *Manage* administrative menu, navigate to *Extend* > *Uninstall*.
2. Select CKEditor (Deprecated).
3. Scroll to the end of the page and click **Uninstall**.

See also [How to upgrade from from CKEditor 4 to CKEditor 5](https://www.drupal.org/docs/core-modules-and-themes/deprecated-and-obsolete#s-how-to-upgrade-from-from-ckeditor-4-to-ckeditor-5).

### Update all your contributed projects

**Important note:** You should update all your contributed modules and themes to Drupal 10 compatible versions while you're still on Drupal 9.

It's a good idea to update all your contributed modules and themes to their latest versions as well. Before you can upgrade Drupal core to version 10, you'll need to ensure that all of your contributed projects are **already Drupal 10 compatible**. In most cases this will mean updating to the latest version. In some cases this may require additional work if the module isn't already Drupal 10 ready.

- [13.6 Updating a Module](https://drupalize.me/tutorial/user-guide/security-update-module)
- [13.7 Updating a Theme](https://drupalize.me/tutorial/user-guide/security-update-theme)

Look at the project's page on Drupal.org for more details about compatibility:

Image

![Screenshot of project info data from the Consumers project page with info about Drupal 10 highlighted](../assets/images/drupal10-project-info-example.png)

Acquia has created [a useful tool for checking compatibility](https://dev.acquia.com/drupal10/deprecation_status).

These are good for getting an estimate of what's going to be involved for your project.

**Tip**: Check *Extend* > *Uninstall* for any deprecated modules (they will be listed at the top). Only uninstall *CKEditor (deprecated)* after you have performed the manual process of upgrading your CKEditor-using text formats (see previous step).

#### Use Upgrade Status module

When you're ready to start working on the Drupal 10 readiness of the modules installed on your site, use the [Upgrade Status](https://www.drupal.org/project/upgrade_status) module on your current site to generate a report. Use the 4.x version for Drupal 9 to 10 upgrades. You will need to install a version of [Drupal's developer dependencies (`drupal/core-dev`)](https://drupalize.me/tutorial/install-drupal-development-requirements-composer) that matches your current Drupal 9 site's version. *Note:* With some older versions of `drupal/core-dev`, you will first need to `composer remove drush/drush` (if you have Drush already installed).

Here's an example of installing Upgrade Status on a Drupal 9.4.9 site that has Drush installed. See the [Upgrade Status](https://www.drupal.org/project/upgrade_status) for more information on the current 4.x release and how to install it.

```
composer show drupal/core | grep versions
# versions : * 9.4.9
composer remove drush/drush
composer require --dev drupal/core-dev:9.4.9 --update-with-all-dependencies
composer require 'drupal/upgrade_status:^4.0@alpha' # See project page for current version in 4.x branch
composer require drush/drush
drush en upgrade_status
```

**Note**: Replace `9.4.9` with your site's Drupal 9 version from the `composer show drupal/core | grep versions` output.

Then, using the *Manage* administrative menu, navigate to *Reports* > *Upgrade status* to see the report and take action.

Image

![Screenshot of an example Upgrade Status report](../assets/images/upgrade_status_example_report.png)

If a module isn't Drupal 10 compatible you've got a few options:

- Update it yourself. This is similar to updating custom code. (See below.)
- Wait for a future release of an updated Drupal 10-compatible version.
- Hire someone to do the updates for you.

We recommend starting with your custom code. And once that's done, come back to your contributed modules and figure out which ones are the most critical for your project and see what you can do to help update them for Drupal 10. In many cases there's likely a patch already available and waiting for community members to test it out.

### Update your custom code

If your project has custom modules or themes, it's your responsibility to ensure that that code is compatible with Drupal 10. Using an IDE with support for the `@deprecated` annotation can help you identify [deprecated code](https://drupalize.me/tutorial/what-deprecated-code). Drupal core deprecations (and new features) will have change records in [Change records for Drupal core](https://www.drupal.org/list-changes/drupal).

You can use [Upgrade Status](https://www.drupal.org/project/upgrade_status) to scan these projects as well. And then you'll need to remove all use of deprecated APIs. [Learn more about what deprecated code is and how to deal with it](https://drupalize.me/tutorial/what-deprecated-code).

**Tip:** Even if you're not planning to upgrade to Drupal 10 now you should start doing this. It'll save time in the future, and since Drupal 10 is backward-compatible with Drupal 9.5.x it shouldn't affect your existing site.

### Verify your hosting meets the new requirements

The [system requirements for Drupal](https://www.drupal.org/docs/system-requirements) have changed. You'll want to make sure your web server, PHP, and MySQL/MariaDB are all running compatible versions. Upgrade Status will indicate if the **Environment is incompatible** on its report as well. (This is only useful if the environment on which you're running Upgrade Status is the same as the environment in which you'll be hosting your Drupal 10 site.)

### Check the Upgrade Status report

Using the *Manage* administrative menu, navigate to *Reports* > *Upgrade status* and, if necessary, click the *Check available updates* link under the **Gather data** column.

Once you have addressed all the blockers to a Drupal 10 upgrade, you will see "N/A" in the **Fix incompatibilities** column and "100%" in the **Relax** column (along with other information).

Image

![Screenshot of Upgrade Status report when site is Drupal 10-ready](../assets/images/upgrade_status_green_drupal10_ready.png)

## Upgrade Drupal core

Sites running Drupal 9.3.x or earlier **must first update to at least 9.4.4** before updating to Drupal 10. Since 9.5.x is available as well, it's best to first upgrade to the latest version of Drupal 9.5.x. See [Update Drupal's Minor Version](https://drupalize.me/tutorial/update-drupals-minor-version).

These instructions below assume you that your Drupal 9 project is using Composer to manage dependencies, and that you either started from the `drupal/recommended-project` Composer template or you've updated your *composer.json* to use the `drupal/recommended-project`'s approach to scaffolding. If you're unsure look for entries like `"drupal/core-recommended": "^9.4"`, and `"drupal/core-composer-scaffold": "^9.4"` in your *composer.json* file. This is a good indication that you're using the current recommend approach.

**Note:** Using the `--no-update` flag updates the *composer.json* entries, without attempting to resolve and download any files. This allows us to batch updates to projects and avoid a "chicken-or-egg first"-type of issues with shared dependencies. Alternatively, you can edit the version constraints in *composer.json* manually.

### Update `drupal/core-dev` (if applicable)

If you have the `drupal/core-dev` dependencies installed you'll need to update those with:

```
composer require drupal/core-dev:^10.0 --dev --no-update --update-with-dependencies
```

### Update `drupal/core-*` projects

Then update the `drupal/core-recommended`, `drupal/core-composer-scaffold`, and `drupal/core-project-message` projects:

```
composer require drupal/core-recommended:^10.0 drupal/core-composer-scaffold:^10.0 drupal/core-project-message:^10.0 --no-update --update-with-all-dependencies
```

### Run `composer update`

Then tell Composer to try and resolve and download all the new code:

```
composer update
```

If this is successful, you'll see a line like the following in the output:

```
  - Upgrading drupal/core-dev (9.4.9 => 10.0.4)
```

If you get any errors you'll need to troubleshoot what's causing the issue. We've tried to provide guidance on some common ones below.

### Deploy your code and put site in maintenance mode

Deploy your code and put your site in maintenance mode in order to run database updates.

**Important:** Remember to make a backup first. These next few steps will change your database schema and are not reversible.

```
drush state:set system.maintenance_mode 1
drush cache:rebuild
```

Or, using the administrative UI:

- **Maintenance mode**: *Configuration* > *Development* > *Maintenance mode* (*admin/config/development/maintenance*)
- **Clear caches**: *Configuration* > *Performance* (*admin/config/development/performance*)

### Check for and run database updates

If Composer was successful at upgrading your site's dependencies to Drupal 10, then check for database updates.

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

### Celebrate! You've upgraded to Drupal 10!

Congratulations! You've upgraded your site to Drupal 10!

Image

![Screenshot of Available updates page showing Drupal 10.0.4 installed](../assets/images/available_updates_drupal10.png)

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

If running `composer update` results in message saying, "Your requirements could not be resolved to an installable set of packages.", there's a good chance that one or more of your contributed modules isn't Drupal 10 compatible. (Or at least the current release version of the project isn't.)

**Solution:** Look for lines like this in the output:

```
- drupal/recurly 1.5.0 requires drupal/core ~8.0 -> satisfiable by drupal/core[8.8.6, 8.0.0, 8.0.0-beta10, ...
```

This indicates that the `drupal/recurly` project requires Drupal 8.x, but we're asking for Drupal 9.x, therefore resulting in an incompatible set of dependencies.

(While this is an example from upgrading from 8 to 9, you may encounter a similar situation for a particular project when you upgrade from 9 to 10.)

If there's a `-dev` version of the module that you know is compatible with Drupal 10 you could try installing that.

Example:

```
composer require drupal/recurly:1.x-dev --no-update
```

If there's a patch in the issue queue see the next tip.

### Problem: Contributed module only has a patch

Often times modules without a Drupal 10 compatible release will have a patch in the issue queue that makes the module work with Drupal 10, but hasn't been committed by the project maintainers yet.

This can result in a sort of race condition, where Composer can't download the required module because it's not presenting as Drupal 10 compatible, so you need to apply a patch, but Composer can't apply the patch if it can't resolve the dependency tree first.

**Solution:** Try the [Lenient Composer Plugin](https://github.com/mglaman/composer-drupal-lenient).

In the transition from Drupal 8 to 9, a [lenient Composer endpoint](https://drupalize.me/tutorial/install-contributed-module-no-drupal-9-release) was created to remove this barrier. For the same situation for Drupal 9 to 10 upgrades, a Composer plugin was created: [Lenient Composer Plugin](https://github.com/mglaman/composer-drupal-lenient).

## Recap

In this tutorial we looked at what's involved in making the transition from Drupal 9 to Drupal 10. This included going over the differences between the two, auditing your custom and contributed modules for compatibility, learning how to make things Drupal 10 compatible while still using Drupal 9. And then finally upgrading Drupal core once everything else is ready, and some troubleshooting tips for common problems.

## Further your understanding

- Most of the Composer commands above can be replicated by directly editing your *composer.json* file, and then running `composer update`.
- If you're using Drupal 7, upgrading to Drupal 10 still requires a major migration. See our [Learn to Migrate to Drupal guide](https://drupalize.me/guide/learn-migrate-drupal).

## Additional resources

- [Drupal 10.0.0 release notes](https://www.drupal.org/project/drupal/releases/10.0.0) (Drupal.org)
- [Preparing your site to upgrade to a newer major version](https://www.drupal.org/docs/upgrading-drupal/prepare-major-upgrade) (Drupal.org)
- [Upgrading from Drupal 9 to Drupal 10](https://www.drupal.org/docs/upgrading-drupal/upgrading-from-drupal-8-or-later/upgrading-from-drupal-9-to-drupal-10) (Drupal.org)
- [Deprecated and obsolete extensions](https://www.drupal.org/docs/core-modules-and-themes/deprecated-and-obsolete) (Drupal.org)
- [Use Composer with Your Drupal Project](https://drupalize.me/tutorial/use-composer-your-drupal-project) (Drupalize.Me)
- [Troubleshoot Common Composer Issues](https://drupalize.me/tutorial/troubleshoot-common-composer-issues) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Upgrade to Drupal 11](/tutorial/upgrade-drupal-11?p=3282)

Next
[Upgrade to Drupal 9](/tutorial/upgrade-drupal-9?p=3282)

Clear History

Ask Drupalize.Me AI

close