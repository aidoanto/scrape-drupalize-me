---
title: "Use a Base Theme"
url: "https://drupalize.me/tutorial/use-base-theme?p=3267"
guide: "[[frontend-theming]]"
order: 11
---

# Use a Base Theme

## Content

Make your theme a subtheme of a *base* theme, allowing it to inherit all the base theme's templates and other properties. When creating Drupal themes it is common to use the Classy theme provided with Drupal core as a base theme to jumpstart your development.

In this tutorial we'll learn how to:

- Use the `base theme` key in our theme's *THEMENAME.info.yml* file
- Make our Ice Cream theme inherit from the Classy theme, or any other theme

By the end of this tutorial you should be able to tell Drupal that your theme is a child of another theme and should inherit all of the parent theme's features.

## Goal

Make our theme a subtheme of the Classy base theme.

## Prerequisites

- [Describe Your Theme with an Info File](https://drupalize.me/tutorial/describe-your-theme-info-file)
- [Theme Inheritance with Base Themes](https://drupalize.me/tutorial/theme-inheritance-base-themes)
- For a comparison between Classy and Stable, read [Drupal Base Themes: Stable and Classy](https://drupalize.me/tutorial/drupal-base-themes-stable-and-classy)

## Base theme or Starterkit?

**Note:** If you're starting a new theme, and your goal is to start from scratch, check out [Start a New Theme with Starterkit](https://drupalize.me/tutorial/start-new-theme-starterkit). Starterkit was added in Drupal 10, and is now the preferred way to start a new theme rather than by extending Classy or Stable.

## All themes must declare a `base theme`

As of Drupal 9 the `base theme` key is required. If you're unsure what to put use `base theme: false` (Drupal 10 and later) or `base theme: stable9` (Drupal 9).

## Use another theme as the base theme

Sprout Video

Configure your theme to use another theme as the *base theme*.

### Determine the theme's name

Find the machine name of the theme you would like to use as a base theme.

This can be found by locating the *THEMENAME.info.yml* file for the theme. Whatever comes before *.info.yml* is the machine name of that theme.

Example: *cores/themes/classy/**classy**.info.yml* has a machine name "classy".

### Edit your .info.yml file

Edit your theme's *THEMENAME.info.yml* file, add a `base theme` key to the existing YAML metadata.

Example:

```
# THEMENAME.info.yml file for Ice Cream example theme.
name: Ice Cream
type: theme
description: 'A great theme for warm summer days.'
base theme: stable9
package: Custom
core_version_requirement: ^8 || ^9 || ^10
```

### Clear the cache

Clear Drupal's internal cache using either the Drupal UI, or a tool like drush, so that the changes to your *.info.yml* file are read by Drupal.

Your theme will now inherit templates and all other properties from the specified base theme.

## Recap

In this tutorial we learned how to change the base theme used for our custom theme from Stable to Classy, or any other theme. We also learned how to determine the machine name of a theme so we could know what value to use with the `base theme` key in our theme's *THEMENAME.info.yml* file.

## Further your understanding

- How do you know what value to use for the 'base theme' key when making your theme a subtheme of another theme?
- If you make your theme a subtheme of Bartik, can you still make changes to the theme's colors via the UI?

## Additional resources

- [Learn about subthemes and base themes](https://drupalize.me/tutorial/theme-inheritance-base-themes) (Drupalize.Me)
- [Learn more about *.info.yml* files](https://drupalize.me/tutorial/describe-your-theme-info-file) (Drupalize.Me)
- [An Introduction to YAML](https://drupalize.me/videos/introduction-yaml) (Drupalize.Me)
- [Creating a Drupal Subtheme](https://www.drupal.org/node/2165673) (Drupal.org)
- [Stable theme has been removed from core](https://www.drupal.org/node/3309392) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Drupal Base Themes: Stable and Classy](/tutorial/drupal-base-themes-stable-and-classy?p=3267)

Next
[Regions](/tutorial/regions?p=3267)

Clear History

Ask Drupalize.Me AI

close