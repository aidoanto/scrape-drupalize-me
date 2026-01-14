---
title: "11.2. Enabling and Disabling Maintenance Mode"
url: "https://drupalize.me/tutorial/user-guide/extend-maintenance?p=2357"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
order: 48
---

# 11.2. Enabling and Disabling Maintenance Mode

## Content

### Goal

Put your site in maintenance mode to allow users with the right permissions to use the site while users without this permission are presented with a message that the site is under maintenance.

### Prerequisite knowledge

[Section 13.3, “Concept: Security and Regular Updates”](https://drupalize.me/tutorial/user-guide/security-concept "13.3. Concept: Security and Regular Updates")

### Site prerequisites

If you want to use Drush to enable or disable maintenance mode, Drush must be installed. See [Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools").

### Steps

Sprout Video

You can use the administrative interface or Drush to enable or disable maintenance mode.

#### Enabling maintenance mode using the administrative interface

1. In the *Manage* administrative menu, navigate to *Configuration* > *Development* > *Maintenance mode* (*admin/config/development/maintenance*). The *Maintenance mode* page appears.
2. Fill in the fields as shown below.

   | Field name | Explanation | Value |
   | --- | --- | --- |
   | Put site into maintenance mode | Enable the maintenance mode | Checked |
   | Message to display when in maintenance mode | The information that is shown to website visitors when the mode is enabled. Variables such as @site can be used in the message | @site is currently under maintenance but should be back shortly. Thank you for your patience. |
3. Click *Save configuration*.
4. Verify that the site is in maintenance mode by accessing it from another browser where you aren’t logged in. If you are not able to verify, try clearing the cache. See [Section 12.2, “Clearing the Cache”](https://drupalize.me/tutorial/user-guide/prevent-cache-clear "12.2. Clearing the Cache").

   Image

   ![Maintenance mode enabled](../assets/images/extend-maintenance-mode-enabled.png)

#### Disabling maintenance mode using the administrative interface

1. In the *Manage* administrative menu, navigate to *Configuration* > *Development* > *Maintenance mode* (*admin/config/development/maintenance*). The *Maintenance mode* page appears.
2. Fill in the fields as shown below.

   | Field name | Explanation | Value |
   | --- | --- | --- |
   | Put site into maintenance mode | Disable the maintenance mode | Unchecked |
   | Message to display when in maintenance mode | No message required while disabling. You can leave the field blank. |  |
3. Click *Save configuration*.
4. Verify that the site is no longer in maintenance mode by accessing it from another browser where you aren’t logged in. If you are not able to verify, try clearing the cache. See [Section 12.2, “Clearing the Cache”](https://drupalize.me/tutorial/user-guide/prevent-cache-clear "12.2. Clearing the Cache").

   Image

   ![Maintenance mode disabled](../assets/images/extend-maintenance-mode-disabled.png)

#### Enabling or disabling maintenance mode using Drush

1. Follow the user interface steps above to edit the site maintenance message, if desired.
2. Run the following Drush commands to enable maintenance mode and clear the cache:

   ```screen
   drush config:set system.maintenance message "Optional message" -y
   drush state:set system.maintenance_mode 1 --input-format=integer
   drush cache:rebuild
   ```
3. Run the following Drush commands to disable maintenance mode and clear the cache:

   ```screen
   drush state:set system.maintenance_mode 0 --input-format=integer
   drush cache:rebuild
   ```
4. After running either set of commands, verify that your site is either in or out of maintenance mode by visiting the site in a browser where you are not logged in.

### Expand your understanding

- [Section 13.5, “Updating the Core Software”](https://drupalize.me/tutorial/user-guide/security-update-core "13.5. Updating the Core Software")
- [Section 13.7, “Updating a Theme”](https://drupalize.me/tutorial/user-guide/security-update-theme "13.7. Updating a Theme")
- [Section 13.6, “Updating a Module”](https://drupalize.me/tutorial/user-guide/security-update-module "13.6. Updating a Module")

Was this helpful?

Yes

No

Any additional feedback?

Previous
[11.1. Finding Modules](/tutorial/user-guide/extend-module-find?p=2357)

Next
[11.3. Downloading and Installing a Module from Drupal.org](/tutorial/user-guide/extend-module-install?p=2357)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close