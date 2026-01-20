---
title: "Composer Configuration for Drupalfree"
url: "https://drupalize.me/tutorial/composer-configuration-drupal?p=2467"
guide: "[[command-line-tools-drupal]]"
order: 5
---

# Composer Configuration for Drupalfree

## Content

Managing a Drupal application with Composer requires a few modifications to Composer's default behavior. For instance, Drupal expects that specialized packages called "modules" be downloaded to *modules/contrib* rather than Composer's default *vendor* directory.

Additionally, it is common practice in the Drupal community to modify contributed projects with patches from Drupal.org. How do we incorporate Drupal-specific practices like these into a Composer workflow?

In this tutorial we will:

- Address all of the Drupal-specific configuration necessary to manage a Drupal application using Composer

By the end of this tutorial you should know how to configure Composer to work with Drupal, and drupal.org.

## Goal

- Learn about the special Composer packages and configuration needed to build a Drupal application with Composer.

## Prerequisites

- [Anatomy of a Composer Project](https://drupalize.me/tutorial/anatomy-composer-project)

## Issues with Drupal's standard directory structure

The standard directory structure for a Drupal application is unusual. Drupal-specific quirks, sometimes called Drupalisms, pose a number of obstacles when using a standard Composer workflow.

Let's look at a few common examples. A typical Drupal application looks something like this (abbreviated) directory structure:

```
.git
.gitignore
docroot
├── core
│   └── libraries
│       └── jquery.cycle
├── modules
│   └── contrib
│       └── ctools
│   └── custom
│       └── my-module
├── themes
│   └── contrib
│   └── custom
│       └── my-theme
├── profiles
│   └── contrib
│   └── custom
├── sites
│   └── default
│       └── default.settings.php
│       └── default.services.yml
│   └── development.services.yml
│   └── example.settings.local.php
│   └── example.sites.php
├── .htaccess
├── index.php
├── robots.txt
├── ...
vendor
composer.json
...
```

Yikes! There are a few strange things going on:

- There are contributed packages not listed on packagist.org
- There are contributed packages placed outside of the *vendor* directory
- Custom files sit side-by-side with contributed files in multiple directories.
- There are some files provided by Drupal core, like *index.php*, that aren't actually in the *core* directory.
- There are some files, like *.htaccess*, which are initially provided by Drupal core but are intended to be modified.
- There are contributed packages written in both PHP and JavaScript

## Questions to consider when updating

These Drupalisms pose a few problems when we attempt to update Drupal core and/or contributed modules. For instance:

- How do we use Composer to download Drupal projects (modules, themes, etc.) if they aren't listed on Packagist?
- How do we tell Drupal to put modules into *modules/contrib* but put themes in *themes/contrib*?
- How can we use Composer to update core files like *index.php*, when those files aren't neatly separated into a dedicated *core* directory?
- What if we've modified our *.htaccess* file, but we need to pull in an upstream update to *.htaccess* provided by a new version of Drupal core? How do we avoid wiping out our customizations?
- What if we've modified our *robots.txt* and we don't want it to be updated by Composer at all?
- What if we've patched a contributed module? How can we update in without wiping out the patch's changes?
- How can we download a JavaScript library?
- How can we define Composer dependencies for a custom module?

We're going to tackle these problems one at a time. At the end, we will also provide solutions that address all of these issues in one fell swoop.

## How Drupal is organized via Composer

As of Drupal's 8.8.0 release (and continuing with Drupal 9), while there are a number of ways you could install Drupal using Composer, the recommended approach is to use the Composer template [drupal/recommmended-project](https://github.com/drupal/recommended-project). This relocates the document root to *web/* and installs *index.php*, *core*, *libraries*, *modules*, *profiles*, *themes*, and so on inside the *web* directory. The *vendor* directory is in the **project** root, enabling you to configure your web server to only provide access to files inside the *web* directory. (Keeping the *vendor* directory outside of the web server's document root is better for security.) You can see in the [drupal/recommended-project's *composer.json*](https://github.com/drupal/recommended-project/) how, in the `extra` key, the `drupal-scaffold` plugin defines the web root location of *web/* and the installer paths for each component type of the Drupal package.

### Abbreviated structure: drupal/recommended-project

```
├── composer.json
├── composer.lock
├── vendor
└── web
    ├── core
    ├── index.php
    ├── modules
    ├── profiles
    ├── sites
    │   ├── default
    ├── themes
```

If you cannot use the `drupal/recommended-project` layout, then there is a legacy project template that uses the same layout as Drupal 8.7.x and earlier. The *index.php*, *core* directory and so on, are placed directly in the project root, next to *composer.json* and the *vendor* directory. The "Vendor Hardening" plugin is uses to ensure the security of the configuration for Apache and Microsoft IIS web servers.

Note that the compressed *.zip* and *.tar.gz* downloads for Drupal is Composer-ready and uses the `drupal/legacy-project` template.

## Pre-8.8.0: How Drupal organized with Composer

Before Drupal 8.8.x, the Drupal core maintainers took the whole [Drupal core project on Drupal.org](https://drupal.org/project/drupal) and separated it into two Composer packages: `drupal/drupal` and `drupal/core`. Essentially, `drupal/core` was everything in the [*core*](https://github.com/drupal/drupal/tree/8.7.x/core) directory, and `drupal/drupal` was a wrapper one directory above *core* and included *core*, too.

## Scaffold files

What are scaffold files? Files such as *index.php*, *update.php*, *robots.txt*, and *.htaccess* that serve as assets in Drupal but aren't neatly separated into a dedicated *core* directory. These assets may also need to exist in specific locations depending on the server configuration or hosting situation.

Starting with 8.8.0 (and continuing with Drupal 9), there is an improved scaffold process. Scaffold files are declared and stored in *drupal/core* then copied into place. The purpose of declaring certain files as *scaffold files* is to allow Drupal sites to be fully managed by Composer while allowing individual asset files to be placed in arbitrary locations.

Dependencies of a Drupal site (e.g. modules and profiles) are only able to scaffold files if explicitely granted that right in the top-level *composer.json* file. Allowed packages are listed there under `extra > drupal-scaffold > allowed-packages`. Note: the `drupal/core` and `drupal/legacy-scaffold-assets` packages are implicitely allowed to scaffold files. You don't need to explicitly list them in your project's top-level *composer.json*.

The scaffold process occurs automatically after the `composer install` operation. The scaffold operation comprises copying or symlinking these individual asset files, called scaffold files into their declared locations.

## Migrating Composer Scaffold

The configuration for Composer scaffolding previous to 8.8.0 is considered "legacay configuration". To update from a legacy configuration to the Drupal Core Composer Scaffold, see the Drupal.org documentation section [Migrating Composer Scaffold](https://www.drupal.org/docs/develop/using-composer/using-drupals-composer-scaffold#s-migrating-composer-scaffold).

## Downloading packages from Drupal.org

How do we use Composer to download Drupal projects (modules, themes, etc.) if they aren't listed on Packagist?

By default, Composer will search the Packagist repository for the packages defined in your *composer.json* file. Packagist does have a listing for [Drupal Core](https://packagist.org/packages/drupal/core). However, most Drupal projects (modules, themes, etc.) are listed on [Drupal.org](https://drupal.org/) and *not* on Packagist.

In order for Composer to discover projects listed on Drupal.org, Composer needs a list of all packages that are available on Drupal.org. Drupal.org provides this information via a specialized Composer repository endpoint, available at `https://packages.drupal.org/8`.

Note that the "8" in the URL denotes that all packages returned by this endpoint will be for Drupal 8 and later (including Drupal 9 and 10). This enables us to drop the major version digit from our Composer version constraints for Drupal packages. E.g., we may use "1.0.0" to download "8.x-1.0" of a Drupal package because the "8" is implied by our use of the `https://packages.drupal.org/8` endpoint.

To make Composer aware of this endpoint, execute:

```
composer config repositories.drupal composer https://packages.drupal.org/8
```

That will add the following information to your *composer.json* file:

```
{ 
  "repositories": { 
    "drupal": {
      "type": "composer",
      "url": "https://packages.drupal.org/8" 
    }
  }
}
```

To require a Drupal package, simply use the prefix `drupal/` followed by the machine name of the Drupal project. For example, `composer require drupal/ctools`.

Note: You can use Composer to manage Drupal 7 sites as well, but this tutorial provides examples for the latest major version of Drupal, which is 8.

## Placing Drupal packages correctly

How do we tell Drupal to put modules into *modules/contrib* but put themes in *themes/contrib*?

By default, Composer downloads packages to the *vendor* directory. But Drupal requires that some packages be downloaded to a different location. For instance, contributed modules must be downloaded to *modules/* in order for Drupal to find them. (And you may also want to place contributed modules in *modules/contrib*.)

This is a common issue amongst PHP frameworks that rely on Composer. To solve this problem, the [Composer team](https://github.com/composer/installers) has created the [Composer Installers](https://github.com/composer/installers) plugin. The plugin defines new types of Composer packages. Each package type has a corresponding default installation location. [Composer Installers includes](https://github.com/composer/installers/blob/master/src/Composer/Installers/DrupalInstaller.php#L6) the following Drupal package types:

| Package type | Installation path |
| --- | --- |
| drupal-core | web/core/ |
| drupal-module | web/modules/`{$name}`/ |
| drupal-theme | web/themes/`{$name}`/ |
| drupal-library | web/libraries/`{$name}`/ |
| drupal-profile | web/profiles/`{$name}`/ |
| drupal-drush | drush/`{$name}`/ |
| drupal-custom-theme | web/themes/custom/`{$name}`/ |
| drupal-custom-module | web/modules/custom/`{$name}`/ |
| drupal-custom-profile | web/profiles/custom/`{$name}`/ |

You can install the `composer/installers` plugin for your Drupal application via:

```
composer require composer/installers
```

Note: If you use the `drupal/recommended-project` Composer template to install Drupal, the `composer/installers` plugin was already installed. Take a look at the `require` key of the [`drupal/recommended-project` *composer.json*](https://github.com/drupal/recommended-project) to see.

Each Drupal project on Drupal.org should have a *composer.json* file that correctly defines the package type. When Composer downloads the package, the Composer Installers plugin (if installed) will inspect the `type` and place the package in the correct corresponding directory.

The directory mappings are configurable. For instance, if you keep your Drupal docroot in a subdirectory named *docroot* (below your *composer.json* file) you may define the following configuration in your *composer.json* file to correctly download modules:

```
{
  "extra": {
    "installer-paths": {
      "web/core": ["type:drupal-core"],
      "web/modules/contrib/{$name}": ["type:drupal-module"],
      "web/modules/custom/{$name}": ["type:drupal-custom-module"],
      "web/profiles/contrib/{$name}": ["type:drupal-profile"],
      "web/profiles/custom/{$name}": ["type:drupal-custom-profile"],
      "web/themes/contrib/{$name}": ["type:drupal-theme"],
      "web/themes/custom/{$name}": ["type:drupal-custom-theme"],
      "web/libraries/{$name}": ["type:drupal-library"]
    }
  }
}
```

### One-off packages

This covers common Drupal packages well, but what if you have a "one-off" package that needs to be downloaded to a non-standard location?

The [Composer Installers Extender](https://github.com/oomphinc/composer-installers-extender) plugin will allow you to arbitrarily place specific packages wherever you would like. For instance, it would allow you to download `my/package` to `special/package/dir` using the following configuration:

```
{
  "extra": {
    "installer-paths": {
      "special/package/dir/": ["my/package"]
    }
  }
}
```

See the The [Composer Installers Extender documentation](https://github.com/oomphinc/composer-installers-extender##how-to-use) for more information.

### Don't commit contributed packages

In [Anatomy of a Composer Project](https://drupalize.me/tutorial/anatomy-composer-project), we learned that we should not commit *vendor* to our git repository. Drupal places core, modules, themes, and other contributed packages outside of the *vendor* directory. These packages should still be excluded from our Git repository, for the same reasons! You should use a *.gitignore* file in your project root that looks something like this:

```
web/core
web/modules/contrib
web/themes/contrib
web/profiles/contrib
web/libraries
vendor
```

## Patching core and contributed packages

What if we've patched a contributed module? How can we update it without wiping out the patch's changes?

"Don't hack core" has long been the mantra of the Drupal community. But the fact is that sometimes a bug in core or a contributed module does require "hacking" code that doesn't belong to you. Perhaps a better mantra would be "don't hack core, but when you do, use a patch."

Patches are the accepted method for tracking and applying changes to Drupal core and contributed projects. Luckily, the [Composer Patches](https://github.com/cweagans/composer-patches) plugin makes Composer an ideal tool for tracking, downloading, and applying these patches.

Since we **do not commit contributed modules**, patches will need to be applied by Composer each time that a package is installed or updated. This is the magic that makes hacking core with patches maintainable. Since contributed modules are not committed, we know that no developer working on our application can make a change to core code without documenting that change via a patch. Once the change is in a patch, it is applied in a consistent and reproducible manner.

To define a patch for a module, you must specify the patch information in your *composer.json*:

```
{
  "extra": {
    "patches": {
      "drupal/core": {
        "Clear Twig caches on deploys": "https://www.drupal.org/files/issues/2752961-90.patch"
      }
    }
  }
}
```

You may also use the Composer Patches plugin (`composer require cweagans/composer-patches:1.x-dev`) to apply locally stored patches, or to ignore patches defined by your dependencies. See [Composer Patches documentation (github.com)](https://github.com/cweagans/composer-patches) or [Patching projects using Composer (Drupal.org)](https://www.drupal.org/docs/develop/using-composer/using-composer-to-install-drupal-and-manage-dependencies#patches) for more information. Note that the 2.x branch of `cweagans/composer-patches` is not yet compatible with `drupal/recommended-project`.

## Handling front-end dependencies

How can we download a JavaScript library?

Many themes and modules require the installation of front-end dependencies like JavaScript libraries. Composer is designed to exclusively install PHP dependencies, but there are a variety of ways to make Composer download non-PHP dependencies.

The preferred approach is to manage those dependencies separately from your PHP dependencies. Use the existing tools that are designed for this such as [NPM](https://www.npmjs.com/) and [Bower](https://bower.io/).

Alternatively you can include non-PHP code as custom packages by following the instructions below.

## Custom packages

How can we define Composer dependencies for a custom module or install non-PHP dependencies? The answer is [custom packages](https://getcomposer.org/doc/05-repositories.md#package-2).

Most Drupal applications include at least one custom module or theme. You can define Drupal dependencies in a *\*.info.yml* file, but what about non-Drupal dependencies? You can define non-Drupal dependencies in your custom module's *composer.json*. But, if your custom module is not hosted on Packagist or Drupal.org, you will need to declare a *Composer path repository*, so that your Drupal project root's *composer.json* can read your module's *composer.json* file.

Let's say you have the following files:

```
web/modules/custom/my-module/composer.json
composer.json
```

If you execute `composer install` in your project's root directory, Composer will (rightly) only care about the *composer.json* file in that root directory. It will completely ignore *web/modules/custom/my-module/composer.json*.

To include the dependencies of a nested *composer.json* file you can use a [Composer path repository](https://getcomposer.org/doc/05-repositories.md#path). To use a Composer path repository, locate the `repositories` key in the *composer.json* in the root of your project (not your module's *composer.json*) and add a new repository object using the `path` type and in the `url`, put the path (relative to your project's root *composer.json*) to your module's *composer.json*. For example:

```
"repositories": [
  {
    "type": "composer",
    "url": "https://packages.drupal.org/8"
  },
  {
    "type": "path",
    "url": "web/modules/custom/my-module"
  }
]
```

Note: In versions prior to 8.8.0, the Wikimedia Composer Merge plugin was utilized to merge in additional *composer.json* files. This method is now deprecated. See [Use the Wikimedia Composer Merge Plugin](https://www.drupal.org/node/314178) for examples and instructions if you still need to use that method.

### Installing non-PHP dependencies

**Note:** Previously we recommended using asset-packagist.org for this. But due to the fact the domain lapsed and the service was temporarily unavailable we decided to recommend the other options below going forward. Though it is still a viable alternative.

To include non-PHP dependencies in your *composer.json* file you can define a custom package, and then require it. This will work for virtually anything you can download from the Internet.

As an example, let's add the [catdad/canvas-confetti](https://github.com/catdad/canvas-confetti) JavaScript library. We'll download a specific *.zip* archive hosted by GitHub. Define a new package in the `repositories` section of your *composer.json* file.

Example:

```
{
    "type": "package",
    "package": {
        "name": "catdad/canvas-confetti",
        "version": "1.5.1",
        "type": "drupal-library",
        "dist": {
            "type": "zip",
            "url": "https://github.com/catdad/canvas-confetti/archive/refs/tags/1.5.1.zip"
        }
    }
}
```

Then, in the `require` or `require-dev` section of your *composer.json* file, add `"catdad/canvas-confetti": "1.5.1."`. This instructs Composer to download the package using the name you specified in the `repositories` array above.

Normal Composer version constraints will not work when doing this. You'll need to take responsibility for tracking new releases for any libraries you install this way.

#### Put the library files into the correct location

By default Composer will install packages into the *vendor/* directory for your project. Drupal projects use the `composer/installers` plugin which allows us to instruct Composer to put files into different locations. For example, putting contributed modules into *web/modules/contrib/* so that Drupal can find them. We can also use this feature to place our custom packages wherever we want them to go.

The `composer/installers` plugin uses the configuration in the `installer-paths` section of our *composer.json* file to determine where to place packages based on their *type*. And because we defined our `catadad/canvas-confetti` package as `"type": "drupal-library"` the resulting files will end up in `"web/libraries/{$name}"`.

Here's the relevant part of the *composer.json* file:

```
"installer-paths": {
    "web/libraries/{$name}": ["type:drupal-library"],
}
```

You can change this configuration as needed. If you need the files in a different location specify your own `"type"` and location for files of that type.

Often times these 3rd-party libraries contain dozens of files. But we only need one or two (e.g. *confetti.min.js*) for our project. For this we can use the [Drupal composer scaffold](https://github.com/drupal/core-composer-scaffold) plugin to copy only specific files into pre-determined locations.

## Recap

In this tutorial, we examined the structure of a typical Drupal application and considered the challenges that Drupalisms pose for Composer-managed applications. For each challenge, we looked at one or more possible solutions.

Below is a sample *composer.json* file that incorporates all of the suggested solutions. It uses the `drupal/recommended-project` template plus some additional configuration.

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
        },
        {
            "type": "path",
            "url": "web/modules/custom/my-module"
        },
        {
            "type": "package",
            "package": {
                "name": "catdad/canvas-confetti",
                "version": "1.5.1",
                "type": "drupal-library",
                "dist": {
                    "type": "zip",
                    "url": "https://github.com/catdad/canvas-confetti/archive/refs/tags/1.5.1.zip"
                }
            }
        }
    ],
    "require": {
        "catdad/canvas-confetti": "1.5.1.",
        "composer/installers": "^1.2",
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
    "minimum-stability": "dev",
    "prefer-stable": true,
    "config": {
        "sort-packages": true
    },
    "extra": {
        "drupal-scaffold": {
            "locations": {
                "web-root": "web/"
            }
        },
        "enable-patching": true,
        "patches": {
          "drupal/core": {
            "Clear Twig caches on deploys": "https://www.drupal.org/files/issues/2752961-90.patch"
          }
        },
        "installer-paths": {
            "web/core": ["type:drupal-core"],
            "web/libraries/{$name}": ["type:drupal-library"],
            "web/modules/contrib/{$name}": ["type:drupal-module"],
            "web/profiles/contrib/{$name}": ["type:drupal-profile"],
            "web/themes/contrib/{$name}": ["type:drupal-theme"],
            "drush/Commands/contrib/{$name}": ["type:drupal-drush"],
            "web/modules/custom/{$name}": ["type:drupal-custom-module"],
            "web/themes/custom/{$name}": ["type:drupal-custom-theme"],
            "web/libraries/{$name}": ["type:drupal-library"],
            "special/package/dir/": ["my/package"]
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

In the next section, we will look at ways to quickly and easily create a new Drupal application that contains much of this configuration out of the box.

## Further your understanding

- How can you use Composer to download modules to *web/modules/contrib*?
- How can you use Composer to update *.htaccess*?
- When shouldn't you use Composer to manage frontend dependencies?

## Additional resources

- [Using Composer to Install Drupal and Manage Dependencies](https://www.drupal.org/docs/develop/using-composer/using-composer-to-install-drupal-and-manage-dependencies#patches) (Drupal.org)
- [Drupal Recommend Project Composer Template](https://github.com/drupal/recommended-project) (github.com)
- [Drupal Scaffold plugin](https://packagist.org/packages/drupal-composer/drupal-scaffold) (packagist.org)
- [Composer Installers plugin](https://github.com/composer/installers) (github.com)
- [Composer Installers Extender plugin](https://github.com/oomphinc/composer-installers-extender) (github.com)
- [Composer Patches plugin](https://github.com/cweagans/composer-patches) (github.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Specify the Version of a Composer Package](/tutorial/specify-version-composer-package?p=2467)

Next
[Use Composer with Your Drupal Project](/tutorial/use-composer-your-drupal-project?p=2467)

Clear History

Ask Drupalize.Me AI

close