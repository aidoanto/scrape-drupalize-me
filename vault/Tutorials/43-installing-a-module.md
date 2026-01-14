---
title: "4.3. Installing a Module"
url: "https://drupalize.me/tutorial/user-guide/config-install?p=2343"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
order: 20
---

# 4.3. Installing a Module

## Content

### Goal

Install a core module, or a contributed module whose files have already been uploaded to the site, through the administrative interface or using Drush.

### Prerequisite knowledge

[Section 1.2, “Concept: Modules”](https://drupalize.me/tutorial/user-guide/understanding-modules "1.2. Concept: Modules") [Section 3.6, “Using Composer to Download and Update Files”](https://drupalize.me/tutorial/user-guide/install-composer "3.6. Using Composer to Download and Update Files")

### Site prerequisites

If you want to use Drush to install modules, Drush must be installed. See [Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools").

### Steps

Sprout Video

You can use the administrative interface or Drush to install modules.

Contributed modules are not included with the core software must first be downloaded using Composer. See [Section 3.6, “Using Composer to Download and Update Files”](https://drupalize.me/tutorial/user-guide/install-composer "3.6. Using Composer to Download and Update Files") for more information.

#### Using the administrative interface

1. In the *Manage* administrative menu, navigate to *Extend* (*admin/modules*). The *Extend* page appears showing all the available modules in your site.
2. Check the boxes for the module or modules you want to install. For example, check the box for the core Ban module.

   Image

   ![Enabling the core Ban module](../assets/images/config-install-check-modules.png)
3. Click *Install*. The checked modules will be installed.

#### Using Drush

1. In the *Manage* administrative menu, navigate to *Extend* (*admin/modules*). The *Extend* page appears showing all the available modules in your site.
2. Find the machine name of the module you want to install, by expanding the information area for the module. For instance, the core Ban module’s machine name is *ban*.
3. Run the following Drush command to install the module:

   ```screen
   drush pm:enable ban
   ```

### Expand your understanding

If you do not see the effect of these changes in your site, you might need to clear the cache. See [Section 12.2, “Clearing the Cache”](https://drupalize.me/tutorial/user-guide/prevent-cache-clear "12.2. Clearing the Cache").

### Additional resources

[Drush](http://www.drush.org)

**Attributions**

Written and edited by [Boris Doesborg](https://www.drupal.org/u/batigolix) and [Jennifer Hodgdon](https://www.drupal.org/u/jhodgdon), and [Joe Shindelar](https://www.drupal.org/u/eojthebrave) at [Drupalize.Me](https://drupalize.me).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[4.2. Editing Basic Site Information](/tutorial/user-guide/config-basic?p=2343)

Next
[4.4. Uninstalling Unused Modules](/tutorial/user-guide/config-uninstall?p=2343)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close