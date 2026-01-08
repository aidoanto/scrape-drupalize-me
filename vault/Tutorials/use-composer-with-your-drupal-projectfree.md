---
title: "Use Composer with Your Drupal Projectfree"
url: "https://drupalize.me/tutorial/use-composer-your-drupal-project?p=2467"
guide: "[[command-line-tools-drupal]]"
---

# Use Composer with Your Drupal Projectfree

## Content

When managing your Drupal project with Composer you'll use Composer commands to download (require) modules and themes that you want to install, as well as issuing commands to keep those modules and themes up-to-date when new versions are released.

In this tutorial we'll:

- Cover step-by-step instructions for performing common Composer tasks for a Drupal application
- Install and update Drupal projects (core, modules, themes, profiles, etc.) using Composer
- Convert an existing application to use Composer

By the end of this tutorial you should know how to use Composer to install, and update, Drupal modules and themes.

## Goal

Create a new Composer-managed Drupal application and install some Drupal modules and themes.

## Prerequisites

- The latest version of Composer. Use `composer self-update` to update Composer.
- For existing Drupal applications, configure your *composer.json* file to work with a Drupal application, as per instructions in [Composer Configuration for Drupal](https://drupalize.me/tutorial/composer-configuration-drupal)
- For existing Drupal applications, execute all commands from your repository root directory.

**Important:** If you need to update your already "composerized" site to Drupal 8.8.x or higher, and you used the `drupal-composer/drupal-project` template to create your application originally, see this tutorial: [Update Drupal from Versions Prior to 8.8.x using Composer](https://drupalize.me/tutorial/update-drupal-versions-prior-88x-using-composer).

## Contents

- [Creating a new Drupal application](#createnew)
- ["Composerize" an existing Drupal application](#composerize)

## Creating a new Drupal application

A best practice to create a brand new Drupal application using Composer is to start from a template. Composer's `create-project` command is intended to do exactly that. When you execute `composer create-project some/project`, it will clone `some/project` and use it as a template for your new project.

Your new project *will not depend on (require) `some/project`*. Instead, *some/project* will merely be used as a starting point. For instance, the *composer.json* file in *some/project* will become the initial *composer.json* file in your new project. After that, *some/project* will effectively never influence or interact with your new project again.

**Note:** As of Drupal 8.8.0, the recommended Composer template is the "officially supported" [drupal/recommended-project](https://github.com/drupal/recommended-project). There are other popular "templates" for starting a new Drupal application with Composer, including [drupal-composer/drupal-project](https://github.com/drupal-composer/drupal-project). You can find the full list in [Using Composer to manage Drupal site dependencies](https://www.drupal.org/docs/develop/using-composer/using-composer-to-manage-drupal-site-dependencies#download-core) on Drupal.org. Note that the official `drupal/drupal` project is deprecated and not recommended. It will generate a codebase that cannot be easily upgraded via Composer. Do not use it.

In this tutorial, we will use the recommended solution, [drupal/recommended-project](https://github.com/drupal/recommended-project). This template provides a great starting point that will make maintaining your site using Composer easier in the long term. We'll also take note of some additional projects (developer tools) you might want to include when you initially create your project. Much of the configuration covered in [Composer Configuration for Drupal](https://drupalize.me/tutorial/composer-configuration-drupal) is covered by the `drupal/recommended-project` template out of the box.

**Note:** If your site is on Drupal 8.7.x or lower, and you want to upgrade your site to Drupal 8.8.x (or higher) and you had started your project using the `drupal-composer/drupal-project` template, read [Update Drupal from Versions Prior to 8.8.x using Composer](https://drupalize.me/tutorial/update-drupal-versions-prior-88x-using-composer).

To create a new Drupal application that uses `drupal/recommended-project` as a template, replace `my-drupal-project` with the name of the project directory you want to use and execute:

```
composer create-project drupal/recommended-project my-drupal-project
cd my-drupal-project
```

- This command will install the latest stable release of Drupal core by default.
- You can choose a previous version of Drupal core by specifying a version number.
- If you want to customize values in the template before `composer install` is executed, skip to the next section, "Customizing the template before install".

To specify a version of Drupal, replace `8.9.5` with the version you want and execute:

```
composer create-project drupal/recommended-project:8.9.5 my-drupal-project
```

After you've installed Drupal, you can use Composer to install additional projects, like Drush, which can be especially useful when installing Drupal.

```
composer require drush/drush
```

## Customizing the template before install

The `composer create-project` command executes `composer install` of all required projects in the template's *composer.json*. If you want to use the template as a starting point but make custom modifications to the template before `composer install` is run, use the `--no-install` flag, modify the *composer.json* according to your specifications, then run `composer install`. For example, to change the name of the `webroot` directory from *web*:

```
composer create-project --no-install drupal/recommended-project my-drupal-project
cd my-drupal-project
```

Edit *composer.json*. In the `extra` array, change the value of `webroot` from `web` to your preferred directory name. Save the file. Then execute:

```
composer install
```

Which will download Drupal and all its dependencies.

For more information, see [Using Composer to Install Drupal and Manage Dependencies](https://www.drupal.org/docs/develop/using-composer/using-composer-to-install-drupal-and-manage-dependencies).

## Composerize an existing Drupal application

Taking an existing Drupal application that is NOT managed with Composer and beginning to manage it with Composer can be a little tricky. The exact method of implementation depends on the directory structure of your Drupal application, and it may require additional steps to handle edge cases that are not addressed in this tutorial.

There are multiple tools that automate the "composerization" process for you:

1. The [Composerize Drupal](https://github.com/grasmash/composerize-drupal) Composer plugin (recommended).
2. The [Composerize](https://drupal.org/project/composerize) module.

If none of these tools work for you, the following manual steps should get you started.

Enter your repository's root directory, where *.git* lives.

**Note:** It is **extremely important** that you **execute commands from the correct directory**.

For some projects, the root directory may directly contain the Drupal *core* directory. In other projects, the root directory may be an additional level up such that *core* lives in *docroot/core*, *web/core*, etc.

Remove any vestigial *composer.json* files or *vendor* dirs

Your entire application should have exactly one *composer.json* file and exactly one *vendor* directory. If there is already a vestigial *composer.json* file or *vendor* directory that are unused, remove them.

```
cd path/above/core/dir
find . -name "composer.json" -exec rm -rf {} \;
find . -name "composer.lock" -exec rm -rf {} \;
find . -name "vendor" -exec rm -rf {} \;
```

It's ok if these commands emit warnings like `No such file or directory`.

Create a new *composer.json* file using the following as a template:

```
{
    "name": "me/my-project",
    "description": "My custom Drupal project",
    "type": "project",
    "license": "proprietary",
    "homepage": "https://www.example.com",
    "repositories": [
        {
            "type": "composer",
            "url": "https://packages.drupal.org/8"
        }
    ],
    "require": {
        "composer/installers": "^1.2",
        "cweagans/composer-patches": "^1.7",
        "drupal/core-composer-scaffold": "^8.8",
        "drupal/core-project-message": "^8.8",
        "drupal/core-recommended": "^8.8"
    },
    "require-dev": {
        "drupal/core-dev": "^8.8"
    },
    "conflict": {
        "drupal/drupal": "*"
    },
    "minimum-stability": "stable",
    "prefer-stable": true,
    "config": {
        "sort-packages": true,
         "allow-plugins": {
            "composer/installers": true,
            "cweagans/composer-patches": true,
            "drupal/core-composer-scaffold": true,
            "drupal/core-project-message": true
        }
    },
    "extra": {
        "drupal-scaffold": {
            "locations": {
                "web-root": "web/"
            }
        },
        "enable-patching": true,
        "installer-paths": {
            "web/core": ["type:drupal-core"],
            "web/libraries/{$name}": ["type:drupal-library"],
            "web/modules/contrib/{$name}": ["type:drupal-module"],
            "web/profiles/contrib/{$name}": ["type:drupal-profile"],
            "web/themes/contrib/{$name}": ["type:drupal-theme"],
            "drush/Commands/contrib/{$name}": ["type:drupal-drush"],
            "web/modules/custom/{$name}": ["type:drupal-custom-module"],
            "web/themes/custom/{$name}": ["type:drupal-custom-theme"],
            "web/libraries/{$name}": ["type:drupal-library"]
        },
        "drupal-core-project-message": {
            "include-keys": ["homepage", "support"],
            "post-create-project-cmd-message": [
                "<bg=blue;fg=white>                                                         </>",
                "<bg=blue;fg=white>  Congratulations, you’ve installed the Drupal codebase  </>",
                "<bg=blue;fg=white>  from the drupal/recommended-project template!          </>",
                "<bg=blue;fg=white>                                                         </>",
                "",
                "<bg=yellow;fg=black>Next steps</>:",

                "  * Install the site: https://www.drupal.org/docs/8/install",
                "  * Read the user guide: https://www.drupal.org/docs/user_guide/en/index.html",
                "  * Get support: https://www.drupal.org/support",
                "  * Get involved with the Drupal community:",
                "      https://www.drupal.org/getting-involved",
                "  * Remove the plugin that prints this message:",
                "      composer remove drupal/core-project-message"
            ]
        }
    }
}
```

1. The sample above assumes that Drupal is contained in a *web* subdirectory. Modify all strings containing `web` to match your directory structure correctly.
2. Replace the value of `name` with the name of your project.
3. `composer require drupal/core:[your-version-of-core]`. E.g., `composer require drupal/core 8.9.0`.

You now have a functional *composer.json* file that appropriately requires Drupal core and the various plugins required to manage a Drupal site with Composer.

Now, you must use Composer to manage all of your required contributed projects (modules, themes, profiles, etc.). This is a manual process that requires your review.

To require an individual project, use the command `composer require drupal/[project-name]`, e.g. `composer require drupal/token`. This will download the latest stable version that is compatible with the version of Drupal core that you're using, which may actually be an upgrade.

If you'd prefer to download an exact version, run `composer require drupal/[project-name]:[exact-version]`.

Examples:

```
composer require 'drupal/token:^1.5'
composer require 'drupal/simple_fb_connect:~3.0'
composer require 'drupal/ctools:3.0.0-alpha26'
composer require 'drupal/token:1.x-dev'
```

Repeat the `composer require` command for every contributed Drupal project required by your application.

You should also repeat `composer require` for any third-party libraries that may live in *docroot/libraries*. See the heading, *Handling front end dependencies*, in [Composer Configuration for Drupal](https://drupalize.me/tutorial/composer-configuration-drupal) for more information.

To speed up this process, you may use Drush to generate a list of all installed Drupal projects. To do this, you must have Drupal installed on the local machine.

To install Drush, use:

```
composer require drush/drush
```

Drush can query Drupal's database to determine which projects are available:

```
./vendor/bin/drush pml --no-core --status=enabled

 ------------------ ---------------------- --------- ---------
  Package            Name                   Status    Version
 ------------------ ---------------------- --------- ---------
  Chaos tool suite   Chaos tools (ctools)   Enabled   8.x-3.0
 ------------------ ---------------------- --------- ---------
```

Next, we will follow best practices and remove your contributed modules from version control.

Create a new *.gitignore* or modify an existing one by adding the following lines:

```
web/core
web/modules/contrib
web/themes/contrib
web/profiles/contrib
web/libraries
```

Next, remove these from version control:

```
git rm --cached web/core
git rm --cached web/modules/contrib
git rm --cached web/themes/contrib
git rm --cached web/profiles/contrib
git rm --cached web/libraries
git rm --cached vendor
```

It's ok if these commands emit an error like `fatal: pathspec 'vendor' did not match any files`. That just means there was nothing to remove.

When using Composer to manage your Drupal project there’s no need to commit anything in the */vendor* , Drupal core (*/web/core*), or contributed modules and themes (*/web/modules/contrib* or */web/themes/contrib*) directories. In fact, [it’s recommended not to](https://getcomposer.org/doc/faqs/should-i-commit-the-dependencies-in-my-vendor-directory.md). This is the default configuration (in Drupal's *.gitignore*) when starting a new Drupal project, as that ensures the same code is used on all environments, and reduces the size of diffs. If you really want to (because of how your code gets deployed to production, for example), it's possible through changing the *.gitignore* file. In this case, make sure the committed versions match the versions in your *composer.lock* file.

That's it! You are now managing all of your site dependencies with Composer. Be sure to continue reading and learn how to correctly deploy this application to a production environment.

## Install a new Drupal package via Composer

To install a new Drupal package, first ensure that application's *composer.json* is correctly configured as per [Composer Configuration for Drupal](https://drupalize.me/tutorial/composer-configuration-drupal). It should, at minimum, include the "drupal" `repositories` entry and `installer-paths` configuration.

To install a new Drupal project (module, theme, profile, etc.), execute:

```
composer require drupal/[project]
```

For instance, to require `ctools`, execute:

```
composer require drupal/ctools
```

By default this will download the latest stable version. You may also specify the version constraint:

```
composer require drupal/ctools 1.0.0
```

(See also [Specify the Version of a Composer Package](https://drupalize.me/tutorial/specify-version-composer-package).)

This command may return an error if `drupal/ctools` 1.0.0 or one of its dependencies is not compatible with one of your root dependencies (those explicitly defined in your *composer.json* file). If that occurs, you will need to change the version constraint for one or more of your requirements until you have defined a set of intercompatible version constraints.

Note that in Composer parlance, "installing" simply means downloading the code, updating *composer.lock*, and making that code available via the autoloader. You still need to "install" the Drupal project (core, module, theme, profile, etc.) to the Drupal database via the UI or Drush.

## Updating a dependency

To update any package, execute:

```
composer update [vendor]/[package]
```

For instance, to update `drupal/ctools`, execute:

```
composer update drupal/ctools
```

Note that this will update **only** `drupal/ctools` and will not update `drupal/ctools`'s dependencies, even if `drupal/ctools` requires new dependencies.

To update `drupal/ctools` and also all of the packages that `drupal/ctools` depends on, execute:

```
composer update drupal/ctools --with-all-dependencies
```

To update `drupal/ctools` and require a new minimum version (such as 1.1.0), execute:

```
composer require drupal/ctools:^1.1.0 --update-with-all-dependencies
```

This command may return an error if `drupal/ctools` 1.1.0 or one of its dependencies is not compatible with one of your root dependencies (those explicitly defined in your *composer.json* file). If that occurs, you will need to change the version constraint for one or more of your requirements until you have defined a set of intercompatible version constraints.

To quickly update all packages (within the bounds of your version constraints), execute:

```
composer update
```

As with updating any Drupal project, you should execute database updates after downloading the new package. If you are using Drupal Configuration Management, you should also re-export configuration after the database updates are complete.

## Update Drupal core via Composer

Drupal core is a package like any other. So, you can follow the instructions for "updating a dependency" and simply specify `drupal/core` as the package name. It's a good idea to specify a new minimum version for `drupal/core` so that a downgrade is never accidentally performed.

As with updating any Drupal project, you should execute database updates after downloading the new package. If you are using Drupal Configuration Management, you should also re-export configuration after the database updates are complete.

## Installing a module's dependencies with Composer

Let's say there's a module we did not install with Composer. How do we install the dependencies listed in that module's *composer.json* file? If you're asking this question, you're actually on the wrong track. You first must use Composer to manage your entire Drupal application and install the module with Composer. Then, its dependencies will be installed for you automatically. See "Start using Composer to manage an existing Drupal Application" earlier in this tutorial.

As an alternative to using Composer, you *might* be able to use [Ludwig](https://www.drupal.org/project/ludwig) to install the module's dependencies *if* that module supports Ludwig.

## Recap

In this tutorial, we learned how to perform common Composer tasks for Drupal applications.

## Further your understanding

- What does the `composer create-project` command do?
- How do you update Drupal core with Composer?
- How do you install a specific version of a Drupal module?
- Why might the `composer update drupal/ctools:^1.1.0` command fail?

## Additional resources

- [Composer template for Drupal projects](https://github.com/drupal-composer/drupal-project) (github.com)
- The [Composerize Drupal](https://github.com/grasmash/composerize-drupal) Composer plugin (github.com)
- The [Composerize](https://drupal.org/project/composerize) module (Drupal.org)
- [Drupal 8 Composer Best Practices](https://www.lullabot.com/articles/drupal-8-composer-best-practices) (lullabot.com)
- [composer require documentation](https://getcomposer.org/doc/03-cli.md#require) (getcomposer.org)
- [composer update documentation](https://getcomposer.org/doc/03-cli.md#update) (getcomposer.org)
- [Using Composer to manage Drupal site dependencies](https://www.drupal.org/docs/develop/using-composer/using-composer-to-manage-drupal-site-dependencies#creating-new) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Composer Configuration for Drupal](/tutorial/composer-configuration-drupal?p=2467)

Next
[Deploy to a Hosting Environment](/tutorial/deploy-hosting-environment?p=2467)

Clear History

Ask Drupalize.Me AI

close