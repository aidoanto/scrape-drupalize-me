---
title: "Install a Contributed Module with No Drupal 9 Releasefree"
url: "https://drupalize.me/tutorial/install-contributed-module-no-drupal-9-release?p=3282"
guide: "[[keep-drupal-up-to-date]]"
order: 8
---

# Install a Contributed Module with No Drupal 9 Releasefree

## Content

As new major versions of Drupal are released, contributed modules need to be updated for compatibility. As of right now (October 2021) there are a lot of contributed modules with a Drupal 8 release and a patch in the queue to make them work with Drupal 9. However, there's no official Drupal 9 compatible release for the module, so the module can't be installed with Composer. This creates a circular problem where you can't `composer require` the module if you don't patch it, but you can't patch it until after it's been downloaded by Composer.

To help solve this common issue, Drupal.org provides a *lenient* Composer endpoint that publishes all modules as compatible with Drupal 9 regardless of whether that's true or not. By using it, you can `composer require` the module and then use `cweagans/composer-patches` to apply any necessary patches.

In this tutorial we'll:

- Add the lenient Composer endpoint to our project's *composer.json* file
- `composer require` a non-Drupal 9 compatible module
- Use Composer to download and apply a patch that makes the module Drupal 9 compatible

By the end of this tutorial you should be able to use contributed modules that require a patch to be compatible with Drupal 9.

## Goal

Use `composer require` to install a module that's not currently Drupal 9 compatible and then apply a patch so that it is.

## Prerequisites

- [Use Composer with Your Drupal Project](https://drupalize.me/tutorial/use-composer-your-drupal-project)
- The "Patching core and contributed packages" section of [Composer Configuration for Drupal](https://drupalize.me/tutorial/composer-configuration-drupal)
- This requires Composer >= version 2 to work

## What is the *lenient* Composer endpoint?

Drupal.org publishes a second composer repository endpoint at <https://packages.drupal.org/lenient>. This endpoint advertises any module that DOES NOT have a `core_version_requirement` entry in the module's *.info.yml* file as being compatible with **any** version of Drupal. If a module already has a `core_version_requirement` entry in its *.info.yml* file then the endpoint doesn't publish the package.

## Caveats

This requires Composer version 2 to work. Only Composer version 2 supports the priority repository feature that is being exploited to allow this to work. Composer 2 allows scanning through a list of repositories for a package starting with the first repository in the list and continuing through the list until it finds one with the requested package. Because the lenient endpoint only publishes modules that do not have a Drupal 9 release, as soon as the module is updated for Drupal 9 compatibility it'll be removed from the lenient endpoint and your project will use the official version.

Composer will output a warning message every time you use it while this lenient repository is present. Ideally, this is used as a stop-gap measure and all your projects have a full Drupal 9 release in the future.

## Why add a lenient endpoint?

As of this writing (October 2021) Drupal 9 has been released, and [Drupal 8 will reach end of life in November 2021](https://www.drupal.org/psa-2021-2021-06-29). At that point, Drupal 8 sites will no longer receive security updates. In order to remain secure, all Drupal 8 sites should update to Drupal 9.

For many sites, this is difficult because the contributed modules they rely on do not yet have a Drupal 9 compatible release -- making updating difficult or impossible. Furthermore, in **many** cases the fixes required to make the Drupal 8 module compatible with Drupal 9 can be automated (there's already a bot that will generate patches when possible), or there is an existing patch in the issue queue that just hasn't been applied by the project's maintainers yet. But, without the lenient facade developers can't use Composer to apply these patches, in effect leaving them stranded on Drupal 8.

## Use the lenient Composer facade

Ready to add the lenient Composer facade to your project and start making use of it?

### Edit your *composer.json* file

Edit the existing *composer.json* file in the root of your project and update it so the `"repositories"` section looks like the following:

```
"repositories": {
    "lenient": {
        "type": "composer",
        "url": "https://packages.drupal.org/lenient"
    },
    "0": {
        "type": "composer",
        "url": "https://packages.drupal.org/8"
    }
},
```

It's important that <https://packages.drupal.org/lenient> is listed before <https://packages.drupal.org/8> so that the repository priority feature works.

### Composer require the Drupal 8 module

Now, you should be able to use `composer` to download the Drupal 8 compatible version of the module.

Example:

```
composer require drupal/consumers
```

Note: The `drupal/consumers` module is only used as an example and may already have a Drupal 9 compatible release.

### Apply the Drupal 9 compatibility patch

The `cweagans/composer-patches` project can be used to apply patches automatically when running `composer install` or `composer update`.

First, make sure the package is present: `composer require cweagans/composer-patches`.

Then, edit the *composer.json* file in the root of the Drupal project (the same one you edited above) and add a `"patches"` section if it doesn't already exist.

Example:

```
{
  "extra": {
    "patches": {
      "drupal/consumers": {
        "[#3116338] Drupal 9 Compatibility": "https://www.drupal.org/files/issues/2020-03-10/3116338-composer-3.patch"
      }
    }
  }
}
```

Here, `"drupal/consumers"` is a list of patches to apply. Each one is a key/value pair. The key is a human-readable name and we recommend including the issue number so you can find it again later. The value is the path to the *.patch* file you want to apply.

Repeat for each module that needs patching.

At this point you should be able to use Composer to install modules for your Drupal 9 site, regardless of whether they advertise a Drupal 9 compatible release or not. However, **this does not mean the modules work** and you'll still need to test them out and perform your due diligence before deploying your updated site.

## Recap

In order to make it easier to update sites to Drupal 9 before the Drupal 8 end of life is reached and sites running Drupal 8 no longer receive critical security updates, you can use the *lenient* Composer endpoint now on Drupal.org. The endpoint advertises a module as being compatible with Drupal 9 regardless of whether that's true or not. This endpoint allows Composer to require the module, download it, and apply any existing patches that make it actually Drupal 9 compatible. This is a stop-gap to help with upgrades, and both module users and maintainers should continue to work towards creating Drupal 9 compatible releases for the modules used by their projects.

## Further your understanding

- How does Composer's priority repository feature work?
- What are some caveats of this approach to upgrading modules?
- What can you do to help ensure the modules you are using get a stable Drupal 9 release?

## Additional resources

- [Using Drupal's Lenient Composer Endpoint](https://www.drupal.org/docs/develop/using-composer/using-drupals-lenient-composer-endpoint) (Drupal.org)
- See the [Add a major-version-agnostic façade endpoint for stranded d8 projects](https://www.drupal.org/project/project_composer/issues/3227031) issue for more details about how/why this was done. (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Update Drupal from Versions Prior to 8.8.x using Composer](/tutorial/update-drupal-versions-prior-88x-using-composer?p=3282)

Clear History

Ask Drupalize.Me AI

close