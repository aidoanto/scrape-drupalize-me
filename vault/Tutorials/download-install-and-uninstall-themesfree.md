---
title: "Download, Install, and Uninstall Themesfree"
url: "https://drupalize.me/tutorial/download-install-and-uninstall-themes?p=3266"
guide: "[[frontend-theming]]"
order: 31
---

# Download, Install, and Uninstall Themesfree

## Content

Before visitors to your site will see the pages displayed using a theme the theme needs to be installed and set as the default. This is true whether it's a custom theme you wrote yourself, or a contributed theme you downloaded from Drupal.org. Installing themes can be done either via the user interface, or using Drush. Once a theme is installed, users of your site will see all public facing page rendered using that theme. Themes that are no longer being used can safely be uninstalled.

In this tutorial we'll:

- Demonstrate how to install a theme and make it the default using both the UI and Drush.
- Learn to differentiate between installed themes, default themes, and uninstalled themes.
- Configure our site to use an administration theme for the administrative pages.

By the end of this tutorial you should be able to install a theme and make it the one visitors to your site see by default.

## Goal

Understand how to download, install, and uninstall a theme.

## Prerequisites

- Downloading a theme from Drupal.org requires using Composer, learn more in [3.5. Using Composer to Download and Update Files](https://drupalize.me/tutorial/user-guide/install-composer?p=3074)

## Video walk-through

This video from the [Drupal User Guide: 11.5. Downloading and Installing a Theme from Drupal.org](https://drupalize.me/tutorial/user-guide/extend-theme-install?p=3072) demonstrates how to download and install a theme from Drupal.org.

Sprout Video

## Download a theme

New themes can be either custom themes that you create, or themes downloaded from Drupal.org. Before a theme can be installed, its files need to be placed into the */themes* directory in the root of your Drupal project in a place where Drupal can find them.

Themes can be [installed with Composer](https://drupalize.me/tutorial/user-guide/install-composer?p=3074):

```
composer require drupal/honey
```

Or downloaded manually. See the User Guide [11.6. Manually Downloading Module or Theme Files](https://drupalize.me/tutorial/user-guide/extend-manual-install?p=3072) for instructions.

## Install a theme via the UI

As long as theme you want to install is located in the */themes/* directory, or one of the other locations Drupal knows to look for theme code, it can be installed by following the steps below. For more information about the location of a theme and its files see [Structure of a Theme](https://drupalize.me/tutorial/structure-theme).

### Log in

Log in as an administrator, or another user who has permission to administer themes.

### Open the Appearance page

In the *Manage* administrative menu, navigate to *Appearance* (*admin/appearance*). This is the primary location for configuring themes and their settings.

### Locate the theme

Locate the theme that you would like to enable from the list of themes on the *Appearance* page.

### Set as default

If the theme is already installed, click the link labeled *Set as default*.

### Or install and set as default

If the theme is not currently installed, click the *Install and set as default* link for the theme that you want use.

### Verify it worked

Navigate to the homepage, or any other public-facing page on your site, and you should see that your new theme is active.

## Install a theme using Drush

**Note:** In the community Drupal User Guide video, `drush en THEME` is demonstrated, but it no longer works. The current command is:

```
drush theme:enable THEME
```

(Substitute `THEME` with the machine name of your theme; for example, `honey`.)

### Set the theme as the default using Drush

```
drush config:set system.theme default THEME --yes
```

(Substitute `THEME` with the name of your theme; for example, `honey`.)

## Uninstall a theme

Follow the steps below to uninstall an unused theme. Note that you must always have at least one theme installed and set as default.

### Log in

Log in as an administrator, or another user who has permission to administer themes.

### Open the Appearance page

In the *Manage* administrative menu, navigate to *Appearance* (*admin/appearance*).

### Locate the theme

Locate the theme that you would like to uninstall in the list of installed themes on the *Appearance* page.

### Uninstall the theme

Click on the link labeled *Uninstall* next to the theme to be disabled.

### Verify it worked

You should see a message at the top of the page that says, "The configuration options have been saved."

## Uninstall a theme using Drush

If you want to uninstall a theme using Drush, first you need to ensure that it is not set as the default theme. (Some other theme needs to be installed and set as the default theme.)

Once the theme you want uninstall is no longer the default, run the following Drush command:

```
drush theme:uninstall THEME
```

(Substitute `THEME` with the name of your theme; for example, `honey`.)

## Installed vs. uninstalled and default

When you navigate to *Appearance* (*admin/appearance*), you'll notice the page is divided into two sections: installed themes, and uninstalled themes.

It's possible to have more than one theme enabled at a time, but only one can be the default theme. For most sites, the default theme is the one that the general public will see when visiting the site.

In most cases you're likely to only have two themes installed: one used for the end-user facing portion of your website, and an administration theme.

## Administration themes

Generally, you don't need the same flashy interface for your administrators as you do for your users. Instead, administrators want an interface that allows them to quickly and easily accomplish administration tasks in a consistent and user-friendly way.

Drupal allows you to designate a separate theme as the "administration theme." This theme will be used when displaying any administration pages — for the most part, anything that starts with *admin/* in the path. It may also be used for adding content and editing pages.

By default, Drupal uses the Claro administration theme that comes with core. However, should you want to change it, you can do so by following these steps.

## Changing the administrative theme

### Install the theme

Install a theme as per the instructions above. Instead of setting it to the default theme, in this case, you only need to click the *Install* link.

**Tip:** Many [contributed themes](https://www.drupal.org/project/project_theme) are specifically designed as administrative themes. You might get the best results selecting a theme optimized for administrative pages.

### Choose an administration theme

In the *Manage* administrative menu, navigate to *Appearance* (*admin/appearance*). Scroll to the bottom of the page to find the section where you may choose an *Administration theme*. Use the dropdown list to choose any installed theme.

### Save configuration

Select *Save configuration* to save your changes and use the new administrative theme. You should see a message at the top of the page that says, *The configuration options have been saved.* And you should notice a that the *Appearance* page now uses the theme you selected as an administrative theme.

## Recap

In this tutorial, we walked through downloading, installing, and uninstalling a theme in Drupal. We also discussed how to change the administrative theme and what it means for a theme to be the *default*.

## Further your understanding

- What is the difference between a theme that's installed, and a theme that is installed and set as the default?
- When are non-default themes used?
- Where does Drupal look for themes that it can install? Learn about the [Structure of a Theme](https://drupalize.me/tutorial/structure-theme) to understand more about the use-case for putting your code into each of these various locations.

## Additional resources

- [3.5. Using Composer to Download and Update Files](https://drupalize.me/tutorial/user-guide/install-composer?p=3074) (Drupal User Guide)
- [4.6. Configuring the Theme](https://drupalize.me/tutorial/user-guide/config-theme?p=3069) (Drupal User Guide)
- [11.5. Downloading and Installing a Theme from Drupal.org](https://drupalize.me/tutorial/user-guide/extend-theme-install?p=3072) (Drupal User Guide)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[What Is a Theme?](/tutorial/what-theme?p=3266)

Next
[Theme Settings Overview](/tutorial/theme-settings-overview?p=3266)

Clear History

Ask Drupalize.Me AI

close