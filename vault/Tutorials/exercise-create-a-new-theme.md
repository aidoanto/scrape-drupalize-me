---
title: "Exercise: Create a New Theme"
url: "https://drupalize.me/tutorial/exercise-create-new-theme?p=3269"
guide: "[[frontend-theming]]"
order: 12
---

# Exercise: Create a New Theme

## Content

It's time to create the bare-bones structure for a new theme on your site. You should try to complete this exercise based what you've learned from the tutorial prerequisites listed below. In this exercise, we'll:

- Create an info file that describes a custom theme to Drupal with the regions listed below (we're going to name ours "reboot").
- Enable, and view, a bare-bones custom theme.

By the end of this exercise, you should feel comfortable starting a theme using several methods.

## Goal

Create scaffolding for a new valid theme and install it.

## Prerequisites

- [Set Up Demo Site for Theming Practice](https://drupalize.me/tutorial/set-demo-site-theming-practice)

In this tutorial you'll be applying your knowledge of creating a new theme. We assume that you're already familiar with the information in these tutorials:

- [An Introduction to YAML](https://drupalize.me/tutorial/introduction-yaml)
- [Install and Uninstall Themes](https://drupalize.me/tutorial/download-install-and-uninstall-themes)
- [Describe Your Theme with an Info File](https://drupalize.me/tutorial/describe-your-theme-info-file)
- [Regions](https://drupalize.me/tutorial/regions)
- [Add Regions to a Theme](https://drupalize.me/tutorial/add-regions-theme)

And now that Classy and Stable have been removed as base themes, and Starterkit is now part of Drupal, read up on [how to start a new theme with Starterkit](https://drupalize.me/tutorial/start-new-theme-starterkit).

## Exercise

Create a new theme called **reboot** with the following information. Since this is a new theme, you have a few options for how to set it up:

1. Use [Starterkit](https://drupalize.me/tutorial/start-new-theme-starterkit) to start your theme, with template files from core's *starterkit* copied into your theme's *templates* directory.
2. Use `drush generate theme` to scaffold a theme.
3. Manually create a theme directory and info file, using a *core* theme for help.
4. Experiment with each method using different theme names and compare the results. Decide which workflow works best for you.

- Use the name, `reboot` or another unique name.
- Add the following regions:
  - 'Header' (header)
  - 'Primary menu' (primary\_menu)
  - 'Secondary menu' (secondary\_menu)
  - 'Page top' (page\_top)
  - 'Page bottom' (page\_bottom)
  - 'Highlighted' (highlighted)
  - 'Featured top' (featured\_top)
  - 'Breadcrumb' (breadcrumb)
  - 'Content' (content)
  - ‘Sidebar first' (sidebar\_first)
  - ‘Sidebar second' (sidebar\_second)
  - 'Footer first' (footer\_first)
  - 'Footer second' (footer\_second)

After you have created your new theme, install and set it as default using the *Appearance* page in the administrative UI.

## Recap

After completing this exercise you should be able to view all public-facing pages of your site using your newly-created theme. It'll be pretty plain, but it's enough to confirm that things are working and Drupal can find and use your theme.

## Further your understanding

- Did you know that [Classy](https://www.drupal.org/node/3305674) and [Stable](https://www.drupal.org/node/3309392) were removed as base themes from Drupal? Instead of relying on a base theme as dependency, a new theme creation workflow was created using Starterkit which scaffolds a theme and copies template files into your theme. Learn more in [Start a New Theme with Starterkit](https://drupalize.me/tutorial/start-new-theme-starterkit).

## Additional resources

- [An Introduction to YAML](https://drupalize.me/tutorial/introduction-yaml) (Drupalize.Me)
- [Install and Uninstall Themes](https://drupalize.me/tutorial/download-install-and-uninstall-themes) (Drupalize.Me)
- [Describe Your Theme with an Info File](https://drupalize.me/tutorial/describe-your-theme-info-file) (Drupalize.Me)
- [Regions](https://drupalize.me/tutorial/regions) (Drupalize.Me)
- [Add Regions to a Theme](https://drupalize.me/tutorial/add-regions-theme) (Drupalize.Me)
- [Change record: Classy removed and replaced with Starterkit theme generator](https://www.drupal.org/node/3305674) (Drupal.org)
- [Change record: Stable theme has been removed from core](https://www.drupal.org/node/3309392) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Set Up Demo Site for Theming Practice](/tutorial/set-demo-site-theming-practice?p=3269)

Next
[Exercise: Add an Asset Library](/tutorial/exercise-add-asset-library?p=3269)

Clear History

Ask Drupalize.Me AI

close