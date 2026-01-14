---
title: "Theme Settings Overview"
url: "https://drupalize.me/tutorial/theme-settings-overview?p=3266"
guide: "[[frontend-theming]]"
---

# Theme Settings Overview

## Content

One important aspect of theme administration is the configuration of global and theme-specific settings. In this tutorial, you will learn where theme settings are configured in Drupal's administrative interface, the difference between global and theme-specific settings, and what each global setting refers to on a base installation of Drupal with a custom theme installed.

## Goal

Get a high-level overview of theme settings in Drupal.

## Prerequisites

[What Is a Theme?](https://drupalize.me/tutorial/what-theme)

## Global settings for themes

Global settings apply to certain common theming elements such as a theme's logo, shortcut icon, and how user pictures are displayed in posts or comments.

As you might have already guessed, global settings will apply to all themes installed now or in the future, until they are overridden in a specific theme's settings.

Global settings for themes will only affect themes that implement them.

## Permissions

To administer settings for themes and follow along with this tutorial and the related tutorial [Change Theme Settings](https://drupalize.me/tutorial/change-theme-settings), we assume you have the following permissions:

- System > Administer themes
- Toolbar > Use the administration toolbar
- System > View the administrative theme

Strictly speaking, you only *need* to have "Administer themes" to update the settings for a theme. However, without the Toolbar, you may have a harder time navigating to the appropriate page, because no menu will be present (by default). Similarly, you don't *need* permission to "View the administrative theme" but it's a good idea for all site administrators to have a similar interface so that training and documentation can be consistent, thereby avoiding: "But that's not what I see on my screen!"

Optional:

- System > Use the administration pages and help

This is appropriate if the role has permission to do other site configuration or administrative tasks. This is a common permission for site administrators to have. If you have this permission on, but you don't actually have permission to configure anything else on the site, you will see a top-level menu item for Help, Structure and Configuration, but there might only be a message on those pages saying "You don't have any administrative items."

## Theme settings in Drupal

### Toggle display

Image

![Toggle display theme settings](../assets/images/global-theme-settings-toggle-display.png)

This group of settings enables you to show or hide certain elements that many themes account for and display through their template files, including the core theme, Bartik.

### User pictures in posts

Image

![User pictures in posts](../assets/images/global-theme-settings-user-pic-posts.png)

User pictures typically display alongside the author of an article.

### User pictures in comments

Image

![User pictures in comments](../assets/images/global-theme-settings-user-pic-comments.png)

Sometimes a theme will display a user picture next to the comment poster's name.

### User verification status in comments

Image

![User verification status in comments](../assets/images/global-theme-settings-verification-status.png)

User verification status in comments commonly displays next to the name provided by an unauthenticated commenter.

### Shortcut icon

Image

![Drupal's default shortcut icon or favicon](../assets/images/global-theme-settings-default-favicon.png)

The shortcut icon, or "favicon," is a special type of image that some web browsers display next to the title of a website, in a tab or window.

If you have a file called *favicon.ico* in the root of your theme's directory and this setting is checked to use the default favicon, then your theme's *favicon.ico* will display. (There would be no need to specify a path.)

### Logo image settings

Image

![Bartik's logo.svg](../assets/images/theme-settings-bartik-logo-svg.png)

Themes may display a logo image, and this setting will toggle its display. For example, in the Bartik theme, the "Druplicon" is displayed next to the title in the header region.

### Using the default logo supplied by the theme

Image

![Location of logo.svg in the Bartik theme](../assets/images/bartik-file-list-default-logo-svg.png)

If you don't want to change the default logo supplied by the theme, leave this checked. Drupal will either look for a file called *logo.svg* in a theme's root directory or for the logo indicated in the theme's info file (see next section).

See *core/lib/Drupal/Core/Theme/ThemeInitialization.php*: [public function getActiveTheme()](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Theme%21ThemeInitialization.php/11.x) and search for string, "logo.svg" to peek under the hood and see how this works.

### Providing a custom logo image

Image

![Custom logo for demo Ice Cream theme](../assets/images/theme-settings-custom-icecream-logo.png)

This setting is available if you want to specify a file name or path other than the default path of *PATH/TO/THEME/logo.svg*.

As of Drupal 8.6, you can specify a path to a custom default logo in your [theme's info file](https://drupalize.me/tutorial/describe-your-theme-info-file). Add a `logo` key and provide a path relative to your theme directory as the value.

```
logo: 'images/logo.png'
```

## Theme-specific settings

When selecting a theme on the Appearance page or selecting the *Settings* link, you will find the global settings that you can override as well as custom settings added by the theme that apply only to this particular theme. For example, if you select Bartik, a core theme, you'll notice a color wheel and a group of settings that allow an administrator to change the color scheme of Bartik's header.

Image

![Theme-specific settings for Bartik using the Color module](../assets/images/bartik-theme-settings-color.png)

All of the global settings can be overridden in a specific theme's settings. In addition, a theme may provide additional settings that only apply to that particular theme.

When you start to configure a theme's settings, you will start with whatever global settings had already been applied. Once you change a setting in a theme that also appears in global settings, the theme's settings will be honored. Any future changes in global settings will no longer apply to a theme where settings have been changed.

## Resetting a theme's settings

If you want to reset your theme settings to match the global settings and have any changes you make in global settings affect that theme, you'll need to uninstall and reinstall the theme whose settings you want to reset.

On the Appearance administration page, make sure the theme you need to reset is not the default (set another theme as the default), then click Uninstall. That theme will now appear in the list of uninstalled themes. Click Install and the theme will be re-installed and its theme settings reset. Now any changes you make in global settings will affect that theme. Once you start making changes to a theme's settings, though, changes to global settings will no longer apply to that theme. (This process is only recommended on a local development environment and not on a live/production site.)

## Altering installed theme settings

Altering the display of a theme using theme settings is one way to customize an installed theme or core theme, without "hacking" the template files. However, if you do intend to alter a core or other installed theme on your site, it is best practice to create a new theme and specify the core theme that you want to emulate as the base theme. Learn more about using base themes in this tutorial: [Use a Base Theme](https://drupalize.me/tutorial/use-base-theme).

## Recap

In this tutorial we learned about the various settings you can configure within a theme.

## Further your understanding

In the next tutorial, [learn how to change global and theme-specific settings](https://drupalize.me/tutorial/change-theme-settings).

## Additional resources

- [function theme\_get\_setting](https://api.drupal.org/api/drupal/core!includes!theme.inc/function/theme_get_setting/) (api.drupal.org)
- [Change record: Theme developers can add the default logo filename to the theme's .info.yml](https://www.drupal.org/node/2939152) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Download, Install, and Uninstall Themes](/tutorial/download-install-and-uninstall-themes?p=3266)

Next
[Change Theme Settings](/tutorial/change-theme-settings?p=3266)

Clear History

Ask Drupalize.Me AI

close