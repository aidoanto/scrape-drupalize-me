---
title: "11.5. Downloading and Installing a Theme from Drupal.org"
url: "https://drupalize.me/tutorial/user-guide/extend-theme-install?p=2357"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
---

# 11.5. Downloading and Installing a Theme from Drupal.org

## Content

### Goal

Download and install a theme from *Drupal.org*.

### Prerequisite knowledge

- [Section 11.4, “Finding Themes”](https://drupalize.me/tutorial/user-guide/extend-theme-find "11.4. Finding Themes")
- [Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools")

### Site prerequisites

Composer must be installed to download themes. If you want to use Drush, Drush must be installed. See [Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools").

### Steps

Sprout Video

To install a contributed theme, first download the theme with Composer. Then install it using either the administrative interface or Drush. If you are installing a custom theme rather than a contributed theme that is not available via Composer, skip the steps for downloading the theme, and refer to [Section 11.6, “Manually Installing Module or Theme Files”](https://drupalize.me/tutorial/user-guide/extend-manual-install "11.6. Manually Installing Module or Theme Files"). Then return here and follow the steps for installing the theme using either the administrative interface or Drush.

#### Download the contributed theme with Composer

1. On the theme’s project page on drupal.org (for example, *<https://www.drupal.org/project/honey>*), scroll to the *Releases* section at the bottom of the page.
2. Copy the provided Composer command for the version of the theme you want to install.

   Image

   ![Finding the composer command for a theme](/sites/default/files/styles/max_800w/public/user_guide/images/extend-theme-install-download.png?itok=hByf_syT)
3. Alternatively, type the following command (substituting the short name of the theme and desired version for `honey:^1.0`):

   ```screen
   composer require 'drupal/honey:^1.0'
   ```
4. At the command line, change to the root directory or your project. Paste the Composer command and execute it.
5. You should see a message about the theme being successfully downloaded.

#### Install the theme using the administrative interface

1. In the *Manage* administrative menu, navigate to *Appearance* (*admin/appearance*). The *Appearance* page appears.
2. Locate the new theme under *Uninstalled themes* and click *Install and set as default* to use it. All non-administrative pages on the site will now use this new theme.

   Image

   ![Uninstalled themes on Appearance page](/sites/default/files/styles/max_800w/public/user_guide/images/extend-theme-install-appearance-page.png?itok=f3ceJIoJ)

#### Install the theme using Drush

1. To install the theme, and set it as the default, run the following Drush\ commands, giving the project name (for example, *honey*) as a parameter:

   ```screen
   drush theme:enable honey
   drush config:set system.theme default honey
   ```
2. Follow the instructions on the screen.

### Expand your understanding

- In the *Manage* administrative menu, navigate to *Appearance* (*admin/appearance*) and uninstall any themes that you are not using.
- [Section 11.1, “Finding Modules”](https://drupalize.me/tutorial/user-guide/extend-module-find "11.1. Finding Modules")
- [Section 11.3, “Downloading and Installing a Module from *Drupal.org*”](https://drupalize.me/tutorial/user-guide/extend-module-install "11.3. Downloading and Installing a Module from Drupal.org")
- If you do not see the effect of these changes in your site, you might need to clear the cache. See [Section 12.2, “Clearing the Cache”](https://drupalize.me/tutorial/user-guide/prevent-cache-clear "12.2. Clearing the Cache").

Was this helpful?

Yes

No

Any additional feedback?

Previous
[11.4. Finding Themes](/tutorial/user-guide/extend-theme-find?p=2357)

Next
[11.6. Manually Installing Module or Theme Files](/tutorial/user-guide/extend-manual-install?p=2357)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close