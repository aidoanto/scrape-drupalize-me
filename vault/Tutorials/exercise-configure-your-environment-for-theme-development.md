---
title: "Exercise: Configure Your Environment for Theme Development"
url: "https://drupalize.me/tutorial/exercise-configure-your-environment-theme-development?p=3269"
guide: "[[frontend-theming]]"
order: 14
---

# Exercise: Configure Your Environment for Theme Development

## Content

Drupal has a few handy settings you can tweak to make developing themes a little more intuitive and a lot more awesome. In this tutorial, we'll practice manually setting up our environment for theme development by:

- Disabling some caches
- Turning off CSS and JS aggregation
- Turning on the Twig debug service

By the end of this tutorial, you'll have practiced setting up your environment for theme development.

## Goal

Get practice configuring your local environment to make it easier to work on theme development tasks.

## Prerequisites

- [Set Up Demo Site for Theming Practice](https://drupalize.me/tutorial/set-demo-site-theming-practice)

This tutorial is a hands-on exercise based on what we learned in:

- [Configure Your Environment for Theme Development](https://drupalize.me/tutorial/configure-your-environment-theme-development) (Drupalize.Me)

## Practice tips

If you want to try and complete this on your own you'll need to:

- Make changes to your site's *settings.php* file. Hint: check out the *example.settings.local.php* file included with core.
- Modify configuration via a *services.yml* file. Hint: check out the *default.services.yml* file included with core.

Once this is done, if you view the source of any page on your Drupal site you should see extra HTML comments with helpful information about which template file was used to generate a section of markup.

Example:

```
<!-- THEME DEBUG -->
<!-- THEME HOOK: 'node' -->
<!-- FILE NAME SUGGESTIONS:
   * node--view--frontpage--page-1.html.twig
   * node--view--frontpage.html.twig
   * node--2--teaser.html.twig
   * node--2.html.twig
   * node--page--teaser.html.twig
   * node--page.html.twig
   * node--teaser.html.twig
   x node.html.twig
-->
<!-- BEGIN OUTPUT from 'themes/icecream/templates/node.html.twig' -->
```

At the end of this exercise, you'll find a video walk-through of the solution.

## Exercise: Enable Twig debug mode via the UI

**New as of Drupal 10.1**: Enable Twig's debug mode and disable Drupal's caching via the administrative UI. This is much easier than the process outlined below, but there are 2 important caveats:

1. The **settings are stored as application state in the database**. Because it's *state* you don't have to worry about accidentally deploying them as configuration. But, it means anytime you down-sync a copy of the database to your production environment you'll lose those changes.
2. **Render cache debugging needs to be enabled separately** via *development.services.yml*. (See instructions in the prerequisite tutorial or below.)

To enable Twig debugging, in the *Manage* administration menu navigate to *Configuration* > *Development* (*admin/config/development/settings*), check the *Twig development mode* box, and then press the *Save settings* button.

Image

![Settings form with checkbox for enabling Twig debugging mode and disabling markup caching](../assets/images/twig-debug-ui-settings.png)

## Exercise: Enable Twig debug mode in files

If you aren't a version of Drupal that enables you to use the UI to enable Twig debug mode, or if you don't want to use the UI, you can use the following method.

### Create a *settings.local.php* file

Copy the file *sites/example.settings.local.php* to *sites/default/settings.local.php*. As long as you don't commit this to version control this file will serve as a location for settings you want to only be applied on your development environment.

### Include the new settings file

Edit the file *sites/default/settings.php*, find the commented out code shown below and uncomment it. It should be near the bottom. This will ensure that the *settings.local.php* file you created above will be included in future requests if it exists.

```
if (file_exists(__DIR__ . '/settings.local.php')) {
  include __DIR__ . '/settings.local.php';
}
```

### Edit the settings

Open the *settings.local.php* file and review the contents. Locate the sections for disabling the render cache, and the dynamic page cache. Uncomment the code to disable both.

### Create a *services.yml* file

Copy *sites/default/default.services.yml* to *sites/default/services.yml*.

### Enable Twig debug mode

Edit *sites/default/services.yml* and set the `twig -> config -> debug` property to `true`.

### Test it out

Clear the cache. Navigate to the home page and refresh.

View source to confirm that it worked, look for additional HTML comments that indicate which template was used to print each section of the page.

**Tip:** We recommend increasing PHP's memory limit to at least 256M and enabling the option to display errors. Twig's debug functions can consume a lot of memory and cause errors.

In *settings.local.php* add the following at the top of the file:

```
error_reporting(E_ALL);
ini_set('display_errors','On');
ini_set('memory_limit', '256M');
```

## Recap

After completing this exercise when you view the source for any page using your theme you should see HTML comments like the following throughout the code. This indicates that Twig debug mode was successfully enabled.

```
<!-- THEME DEBUG -->
<!-- THEME HOOK: 'node' -->
<!-- FILE NAME SUGGESTIONS:
   * node--view--frontpage--page-1.html.twig
   * node--view--frontpage.html.twig
   * node--1--teaser.html.twig
   * node--1.html.twig
   * node--article--teaser.html.twig
   * node--article.html.twig
   * node--teaser.html.twig
   x node.html.twig
-->
<!-- BEGIN OUTPUT from 'core/themes/classy/templates/content/node.html.twig' -->
```

Sprout Video

## Further your understanding

- Try out different var-dumping tools to see which one you like working with the best. Explore the configuration options for Devel on the *Configuration* page of the admin UI.

## Additional resources

- [Configure Your Environment for Theme Development](https://drupalize.me/tutorial/configure-your-environment-theme-development) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Exercise: Add an Asset Library](/tutorial/exercise-add-asset-library?p=3269)

Next
[Exercise: Override the Main Page Template](/tutorial/exercise-override-main-page-template?p=3269)

Clear History

Ask Drupalize.Me AI

close