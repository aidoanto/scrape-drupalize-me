---
title: "4.4. Uninstalling Unused Modules"
url: "https://drupalize.me/tutorial/user-guide/config-uninstall?p=2343"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
---

# 4.4. Uninstalling Unused Modules

## Content

### Goal

Uninstall the core Search and History modules, as well as the core Ban module if you installed it in [Section 4.3, “Installing a Module”](https://drupalize.me/tutorial/user-guide/config-install "4.3. Installing a Module"), to reduce overhead.

### Prerequisite knowledge

[Section 1.2, “Concept: Modules”](https://drupalize.me/tutorial/user-guide/understanding-modules "1.2. Concept: Modules")

### Site prerequisites

- You must have at least one unused module on your site that you want to uninstall, such as the core Search module.
- If you want to use Drush to uninstall modules, Drush must be installed. See [Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools").

### Steps

Sprout Video

You can use the administrative interface or Drush to uninstall modules.

#### Using the administrative interface

1. In the *Manage* administrative menu, navigate to *Extend* > *Uninstall* (*admin/modules/uninstall*) where you will find the list of modules that are ready to be uninstalled.
2. Check the boxes for the modules you are uninstalling (*Ban*, *History*, and *Search*). Click *Uninstall* at the bottom of the page.

   Image

   ![Uninstalling module](/sites/default/files/styles/max_800w/public/user_guide/images/config-uninstall_check-modules.png?itok=U_DEUfC_)

   ### Note

   You cannot uninstall a module if it is required by some other module(s) and/or functionality. For example, the core File module is required by the core Text Editor, CKEditor, and Image modules. It can’t be uninstalled unless you uninstall its dependent module(s) and functionality first. A module that cannot be uninstalled yet will have a disabled checkbox, restricting you from uninstalling it.
3. Step 2 will prompt you to confirm the module uninstall request. Click *Uninstall*.

   Image

   ![Confirm uninstall - search module](/sites/default/files/styles/max_800w/public/user_guide/images/config-uninstall_confirmUninstall.png?itok=jTXq0zZe)

#### Using Drush

1. In the *Manage* administrative menu, navigate to *Extend* (*admin/modules*). The *Extend* page appears showing all the available modules in your site.
2. Find the machine name of the module you want to uninstall, by expanding the information area for the module. For instance, the core Ban module’s machine name is *ban*.
3. Run the following Drush command to uninstall the module:

   ```screen
   drush pm:uninstall ban
   ```

### Expand your understanding

- [Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools")
- [Section 12.2, “Clearing the Cache”](https://drupalize.me/tutorial/user-guide/prevent-cache-clear "12.2. Clearing the Cache")
- You can also uninstall the core Comment module by following these steps, but only after comment fields have been removed, which is a side effect of [Section 6.2, “Deleting a Content Type”](https://drupalize.me/tutorial/user-guide/structure-content-type-delete "6.2. Deleting a Content Type").

Was this helpful?

Yes

No

Any additional feedback?

Previous
[4.3. Installing a Module](/tutorial/user-guide/config-install?p=2343)

Next
[4.5. Configuring User Account Settings](/tutorial/user-guide/config-user?p=2343)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close