---
title: "Describe Your Theme with an Info File"
url: "https://drupalize.me/tutorial/describe-your-theme-info-file?p=3267"
guide: "[[frontend-theming]]"
order: 37
---

# Describe Your Theme with an Info File

## Content

Info files, aka *THEMENAME.info.yml* files, provide Drupal with metadata about your theme, the features it supports, and the regions that it defines. All themes are required to have a *THEMENAME.info.yml* file, and creating one is generally the first step you'll take when creating a new theme.

In this tutorial we'll:

- Create a new *.info.yml* file and define a new theme
- Review the required key/value pairs of an *.info.yml* file
- Enable our new theme in the Drupal UI

By the end of this tutorial you'll be able start a new theme by creating the required *\*.info.yml* file and better understand its contents.

## Goal

Create a *THEMENAME.info.yml* for a new custom theme.

## Prerequisites

- [An Introduction to YAML](https://drupalize.me/videos/introduction-yaml)

## Watch: Describe Your Theme with an Info File

Sprout Video

## Generate an info file

The fastest way to create an info file for your theme is via the Drush command: `drush generate theme-info`, which will walk you through all the required values and generate some scaffolding files for your theme. This is optional. You can create the files manually.

## Create an info file

If you want to create an info file from scratch, or understand more deeply what the info file is doing, you can follow along with this tutorial.

### Choose a name

The first thing you'll need to do is decide on a name for your theme – both a human readable name that will be used to refer to your theme in the UI, and a machine readable name that will be used to reference your theme in code. This will inform the name you ultimately give to your info file. For this example, we'll name our theme *Ice Cream* with a machine name of *icecream*.

**Note:** The machine name must be all lowercase, start with a letter, use an underscore (`_`) instead of spaces, and contain no other symbols. Examples of a good machine name are *icecream*, and *ice\_cream*. Examples of a bad machine name are *ice cream* or *6icecream*.

The machine name we choose is what we'll use when creating our *info.yml* file, and is also typically the name given to the directory that contains our theme and all its code.

### Create an info file

Create the file *themes/icecream/icecream.info.yml*

### Edit the info file

Open the *themes/icecream/icecream.info.yml* in your editor of choice and add the following code to it:

```
# THEMENAME.info.yml file for Ice Cream example theme.
name: Ice Cream
type: theme
base theme: stable9
description: 'A great theme for warm summer days.'
package: Custom
core_version_requirement: ^9 || ^10
```

Here's what these key/value pairs do:

#### `name`

(required) The human readable name of your theme, displayed in Drupal's UI when administrators are browsing the list of available themes

#### `type`

(required) Tell Drupal what type of project this is. Required, and will always be set to 'theme' for a theme.

#### `description`

A short one-line description used in the UI when listing your theme.

#### `package`

The package your theme belongs in; used for grouping projects together.

#### `core`

Replaced by `core_version_requirement` as of Drupal 8.7.7.
(The `core` key was required in versions 8.7.6 and prior.) The version of Drupal core that your theme is compatible with. Required for Drupal 8 versions prior to and including 8.7.6; for Drupal 8 themes this will likely always just be `8.x`.

#### `core_version_requirement`

Using [Semantic Versioning](https://drupalize.me/videos/semantic-versioning), declare which versions of Drupal core the theme is compatible with. Introduced in Drupal 8.7.7. To learn more, see the examples and explanation in [Overview: Info Files for Drupal Modules](https://drupalize.me/tutorial/overview-info-files-drupal-modules) or in this [change record](https://www.drupal.org/node/3070687).

In most cases your theme should use `core_version_requirement: ^9 || ^10`.

#### `base theme`

(required) The machine name of an installed theme to be used as a base theme. If you're not sure what base theme to use choose Stable9. If no base theme should be used, enter `false` as a value for this key.

See a [complete list of keys](https://www.drupal.org/node/2349827).

### Clear the cache

With your *themes/icecream/icecream.info.yml* file in place, Drupal should be able to recognize your theme and display it as an option on the *Appearance* page. You'll need to [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache). This will cause Drupal to recreate the list of themes it knows about – and this time it will find your *.info.yml* file and recognize your new theme.

### Verify your theme is listed

Finally, navigate to the *Appearance* (*admin/appearance*) page. You should see your Ice Cream theme listed under *Uninstalled themes*.

## Use Starterkit to start a new theme

As an alternative to writing an info file from scratch, you can use the Drupal core Starterkit utility to setup the necessary structure and files for a new theme. Learn more in [Start a New Theme with Starterkit](https://drupalize.me/tutorial/start-new-theme-starterkit).

## Recap

In this tutorial we created a new *THEMENAME.info.yml* file for our custom theme. We then populated the file with values for all required, and some commonly used, keys. This is the only required file for a theme, and having it in place allows us to enable and start developing our theme.

## Further your understanding

- What does your theme look like if you enable it with nothing but an *.info.yml* file?
- What is significant about the portion of the filename before the *.info.yml* extension?
- Which of these is not a valid machine name? `my_theme`, `my-theme`, `mytheme`
- Read through the *.info.yml* files of the themes in */core/themes* to get a better idea of what you can expect to find in an info file

## Additional resources

- [Learn YAML](https://drupalize.me/videos/introduction-yaml) (Drupalize.Me)
- [Defining a theme with an .info.yml file](https://www.drupal.org/node/2349827) (Drupal.org)
- [Drupal 8 Theming Fundamentals, Part 1](https://www.lullabot.com/blog/article/drupal-8-theming-fundamentals-part-1) (Lullabot.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Start a New Theme with Starterkit](/tutorial/start-new-theme-starterkit?p=3267)

Next
[Theme Inheritance with Base Themes](/tutorial/theme-inheritance-base-themes?p=3267)

Clear History

Ask Drupalize.Me AI

close