---
title: "Update Drupal from Versions Prior to 8.8.x using Composerfree"
url: "https://drupalize.me/tutorial/update-drupal-versions-prior-88x-using-composer?p=3282"
guide: "[[keep-drupal-up-to-date]]"
---

# Update Drupal from Versions Prior to 8.8.x using Composerfree

## Content

Drupal 8.8.0 introduced a bunch of new features intended to make it easier over the long-term to maintain a Drupal project using Composer. In doing so it establishes some new best practices, and moves into Drupal core solutions that were previously maintained by the community. This is all good news. But, it means if you're using Composer to update from Drupal 8.7.x or lower to 8.8.0 or higher you'll need to do a bit of additional work to untangle everything.

This tutorial is especially useful if you started your Drupal project using the `drupal-composer/drupal-project` template and would like to convert to use the new templates (i.e. `drupal/recommended-project` or `drupal/legacy-project`) included with Drupal 8.8.x core.

In this tutorial we'll:

- Convert our project to use the new `drupal/core-recommended`, and `drupal/core-dev` Composer packages
- Explain which commonly used Composer packages are deprecated, and which new ones replace them
- Learn how to use the `drupal/core-composer-scaffold` Composer plugin
- Cover tips for troubleshooting updates

Furthermore, in order to [Upgrade to Drupal 9](https://drupalize.me/tutorial/upgrade-drupal-9) from Drupal 8, you will first need to update your Drupal 8 site to at least version 8.8, as the [upgrade paths for Drupal 8 site from before Drupal 8.8.0 have been removed from Drupal 9](https://www.drupal.org/node/3098327).

By the end of this tutorial you should be able to update your Drupal projects using Drupal core 8.7.x or lower to Drupal core 8.8.0 or higher using Composer. And be ready for an upgrade to Drupal 9.

## Goal

Update from an older version of Drupal core to Drupal 8.8.0 or later using Composer.

## Prerequisites

- If you're following this tutorial, we assume you're already using Composer to manage your Drupal site dependencies. But if you're looking for a general introduction to Composer, we recommend [The Wonderful World of Composer](https://drupalize.me/videos/wonderful-world-composer).

## Before you get started

You probably won't need to do all of these steps, and some of them may not be exactly right for your use-case, but we'll do our best to explain what's changing and why so that hopefully you can get it all working.

We recommend reading through this whole tutorial first and determining which elements apply to you before proceeding with updating.

Prior to Drupal 8.8.0 many sites used the [drupal-composer/drupal-project](https://github.com/drupal-composer/drupal-project) as the basis for their projects. If you did, there are some additional steps you'll need to take to update to Drupal 8.8.0 or higher.

## Why do I need to do this?

Previously, the recommended way to install Drupal with Composer was the following command:

```
composer create-project drupal-composer/drupal-project:8.x-dev some-dir --no-interaction
```

**Note:** You can still use `drupal-composer/drupal-project` for **starting a new project**. It's already been updated with to reflect these changes. [Learn more about installing Drupal with Composer](https://drupalize.me/tutorial/use-composer-your-drupal-project).

What the command above does is download all the files in [the drupal-composer/drupal-project repository](https://github.com/drupal-composer/drupal-project) and then run `composer install`. You've now got a starting point for your project, but there is no link to the original template. From here on out all of those files are your responsibility. The idea is to provide some scaffolding for common configuration that most any Drupal project would want. And to save you a few keystrokes every time you start a new project.

The `drupal-composer/drupal-project` template made use of some packages that are now deprecated in favor of new ones that are provided by Drupal core. And as part of updating to Drupal 8.8.0+ you'll want to switch from using these now deprecated packages to the new recommended ones.

Since your project is no longer connected to the upstream template, you'll need to make these changes yourself.

**Note**: Running many of the commands included below can impact the code that's installed for your project, and can have unintended consequences. It's a good idea to make a backup before trying any of these. And to test on a development environment first.

## Use the drupal/core-recommended meta package

When installing Drupal core with Composer you should require `drupal/core-recommended` instead of `drupal/core`. *Recommended* in this case means that this specific version of Drupal core and these specific versions of its dependencies have passed all the automated tests and are deemed suitable for release.

It's possible, though rare, that if you use different versions of one of Drupal core's dependencies than the one that was tested for the release that there might be bugs. By using `drupal/core-recommended` you can prevent dependency versions from drifting upwards, and ensure that you always get the same dependencies that were used in the release. You can be more confident when deploying your application knowing that the combination of core and dependencies is verified to work.

Prior to Drupal 8.8.0 the `drupal/core-recommended` package did not exist and many Drupal sites used the `webflo/drupal-core-strict` meta package which locked dependencies to exact versions. For example, it might use `drupal/core: "8.8.1"` instead of `drupal/core: "^8.8"`. The former would only ever resolve to 8.8.1 while the later might resolve to 8.8.1 or 8.8.0.

As of Drupal 8.8.0 using the `drupal/core-recommended` meta package provides this dependency locking and `webflow/drupal-core-strict` is no longer necessary.

**Caveat:** It's possible (though rare) that a contributed module might explicitly require a different version of a Symfony component than the one that is pinned in your current version of `drupal/core-recommended`. If that's the case you can still use `drupal/core` which has a more lenient set of dependency version constraints.

Our rule of thumb: if it works for your set of required contributed modules and other Composer packages, use `drupal/core-recommended` and enjoy the extra confidence. But if it doesn't, use `drupal/core`. That's why the package is named *recommended* and not *required*.

### Switch to `drupal/core-recommended`

If your existing *composer.json* contains a record for `drupal/core` replace it with `drupal/core-recommended: "^8.8"`.

The following commands will convert from `drupal/core` to `drupal/core-recommended`. These commands will modify your *composer.json* file, but not remove, or download, any code because of the `--no-update` flag:

```
composer remove drupal/core --no-update
composer require composer/installers:^1.7 --no-update
composer require drupal/core-recommended:^8.8 --no-update
```

You can also edit the *composer.json* file manually instead of using the command above.

**Important caveat:** If Drupal is installed in the root directory of your project, and not in a subdirectory like *web/* (is the Drupal *core/* directory in the root of your project?) you should refer to the [drupal/legacy-project template](https://github.com/drupal/legacy-project) instead. The latter assumes the current best practice of using a *web/* subdirectory.

To use the `drupal/legacy-project` template, you will also need to require `drupal/core-vendor-hardening: "^8.8"`. So the Composer commands to update your requirements to match the `drupal/legacy-project` template would be:

```
composer remove drupal/core --no-update
composer require composer/installers:^1.7 --no-update
composer require drupal/core-recommended:^8.8 --no-update
composer require drupal/core-vendor-hardening: ^8.8 --no-update
```

If you're migrating from `webflo/drupal-core-strict`, to `drupal/core-recommended` you need to remove your project's dependency on the legacy package. You can do so with the following `composer` command:

```
composer remove webflo/drupal-core-strict --no-update
```

## Use the drupal/core-dev meta package

The `drupal/core-dev` package contains all the optional development specific core dependencies. For example, the code required to run automated tests. This package can either be left out, or added to the `"require-dev"` section of your *composer.json* file as they're only needed for development.

This package replaces `webflo/drupal-core-require-dev` if you were previously using that you can remove it with:

```
composer remove webflo/drupal-core-require-dev --dev --no-update
```

And then add the new one:

```
composer require drupal/core-dev:^8.8 --no-update
```

## Dealing with scaffolding

There are certain files in every Drupal install that are required for the project to work, but don't necessarily always have to live in the same place. Files like *index.php* and *.htaccess* for example. And optional example files like *.editorconfig*, *.gitignore*, *sites/example.settings.local.php* that are included with the project to serve as an example, but might need to be placed in a different location depending on the specific structure of your codebase. These are known as *scaffold* files.

And you need to teach Composer where to put them.

This is accomplished using the `drupal/core-composer-scaffold` Composer plugin. Which, replaces the `drupal-composer/drupal-scaffold` package if you were using it.

If you were using `drupal-composer/drupal-scaffold`, first remove the requirement:

```
composer remove drupal-composer/drupal-scaffold --no-update
```

Add the new core scaffolding plugin:

```
composer require drupal/core-composer-scaffold:^8.8 --no-update
```

And then configure it by editing your *composer.json* file to include the necessary configuration in the `"extra"` section:

```
"extra": {
  "drupal-scaffold": {
      "locations": {
          "web-root": "web/"
      }
  },
}
```

The `web-root` key allows you configure which directory contains the Drupal core installation. And will result in for example *web/index.php* and *web/.htaccess*. If you use a different sub-directory like *docroot/* you can change that here.

Sometimes you might want to make changes to scaffold files, and use your modified version instead of the default. This is accomplished by copying the file you want to change into its normal location. Committing the changed version. And then configuring the plugin to stop replacing that particular file.

[Learn more about additional configuration options for drupal/core-composer-scaffold](https://www.drupal.org/docs/develop/using-composer/using-drupals-composer-scaffold).

## Run `composer update`

After making all the necessary changes to your *composer.json* file you'll run `composer update` to get all the correct files and most importantly update your *composer.lock* file.

If you want to update only the required files and not also update things like contributed modules at the same time use `composer update --lock`.

## Update settings.php

As of Drupal 8.8.0 the configuration sync directory is now defined as `$settings['config_sync_directory']` instead of `$config_directories`. ([Change record](https://www.drupal.org/node/3018145)). This setting is used to tell Drupal where the configuration files for your site are stored on disk. And needs to be updated if it's used.

Open your *settings.php* file and change:

```
$config_directories['sync'] = 'my/config/dir';
```

To:

```
$settings['config_sync_directory'] = 'my/config/dir';
```

You may also need to update the configuration for the temporary files directory. Also in *settings.php*, change:

```
$config['system.file']['path']['temporary'] = 'my/temp/dir';
```

To:

```
$settings['file_temp_path'] = 'my/temp/dir';
```

## Run database updates

At this point you should have the code for your project up-to-date, and you'll need to run the database updates. This process is the same regardless of what version you're updating from. See [Update Drupal's Minor Version](https://drupalize.me/tutorial/update-drupals-minor-version) for more information.

## Troubleshooting

The update process will likely vary a bit for everyone as a lot depends on changes that you made to your Drupal installation after the initial setup. Below are some useful tips if you're running into issues.

Compare your *composer.json* to the one from the new `drupal/recommended-project` template which can be found here <https://github.com/drupal/recommended-project/blob/8.8.x/composer.json>.

If running `composer install`, or `composer update` is resulting in an uninstallable set of dependencies you can try the nuclear option:

```
rm composer.lock
rm -r vendor/
composer install
```

This can result in unintended updates. For example contributed modules that you installed will all be updated to the latest version allowed by *composer.json* which may differ from the version currently installed via *composer.lock*.

You can also use `composer prohibits drupal/core:8.8.0` to learn more about what is preventing the update from resolving to a useable set of dependencies.

If you're experiencing permissions issues [see this tip in the documentation](https://www.drupal.org/docs/develop/using-composer/starting-a-site-using-drupal-composer-project-templates#s-troubleshooting-permission-issues-prevent-running-composer).

## Recap

In order to update to Drupal core 8.8.x from previous versions you might need to replace some new deprecated Composer packages with the new community supported ones. This especially if you started out using the `drupal-composer/drupal-project` Composer template. Doing so requires updating your *composer.json* file with some new dependencies and new configuration. Then testing it all to make sure it still results in a usable set of dependencies.

## Further your understanding

- Does your project have customizations to scaffold files like *.htaccess* or *robots.txt*? Take some time to [read about using the scaffold plugins configuration](https://www.drupal.org/docs/develop/using-composer/using-drupals-composer-scaffold) to make it easier to maintain these changes going forward.
- While you're at it it's not a bad idea to update and test the contributed modules your site uses.
- [Upgrade to Drupal 9](https://drupalize.me/tutorial/upgrade-drupal-9).

## Additional resources

- [Change record: Upgrade paths for Drupal 8 site from before Drupal 8.8.0 have been removed from Drupal 9](https://www.drupal.org/node/3098327) (drupal.org/list-changes)
- [Update Core via Composer](https://www.drupal.org/docs/updating-drupal/updating-drupal-core-via-composer) (Drupal.org)
- [Guide to the Drupal 8.8 Update](https://www.palantir.net/blog/guide-drupal-8-8-update) (palantir.net)
- [Updating to Drupal 8.8.0 Beta with Composer](https://www.previousnext.com.au/blog/updating-drupal-880-beta-composer) (previousnext.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Upgrade to Drupal 9](/tutorial/upgrade-drupal-9?p=3282)

Next
[Install a Contributed Module with No Drupal 9 Release](/tutorial/install-contributed-module-no-drupal-9-release?p=3282)

Clear History

Ask Drupalize.Me AI

close