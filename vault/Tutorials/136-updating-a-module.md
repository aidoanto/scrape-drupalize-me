---
title: "13.6. Updating a Module"
url: "https://drupalize.me/tutorial/user-guide/security-update-module?p=2404"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
order: 48
---

# 13.6. Updating a Module

## Content

### Goal

Update a contributed module and run the *Database updates* script.

### Prerequisite knowledge

- [Section 13.3, “Concept: Security and Regular Updates”](https://drupalize.me/tutorial/user-guide/security-concept "13.3. Concept: Security and Regular Updates")
- [Section 13.1, “Concept: Cron”](https://drupalize.me/tutorial/user-guide/security-cron-concept "13.1. Concept: Cron")

### Site prerequisites

- A contributed module has been installed and there is an update available for it. See [Section 11.3, “Downloading and Installing a Module from *Drupal.org*”](https://drupalize.me/tutorial/user-guide/extend-module-install "11.3. Downloading and Installing a Module from Drupal.org") and [Section 13.4, “Keeping Track of Updates”](https://drupalize.me/tutorial/user-guide/security-announce "13.4. Keeping Track of Updates").
- If your site is live, you should test this process in a development environment before running it on your production site. See [Section 11.8, “Making a Development Site”](https://drupalize.me/tutorial/user-guide/install-dev-making "11.8. Making a Development Site").
- You have created a full-site backup. See [Section 12.3, “Concept: Data Backups”](https://drupalize.me/tutorial/user-guide/prevent-backups "12.3. Concept: Data Backups").
- If you want to use the user interface to check for updates, the core Update Manager module must be installed. See [Section 4.3, “Installing a Module”](https://drupalize.me/tutorial/user-guide/config-install "4.3. Installing a Module") for instructions on installing core modules.

### Steps

Sprout Video

Before you start, check for module-specific update instructions. Read and understand all module-specific requirements before proceeding with the updates. To find instructions, check the module’s project page *Read Documentation* link.

To view further instructions, after downloading the updated files, look for *README.txt*, *INSTALL.txt*, and *UPGRADE.txt* that come with the module. Also, review the release notes on the project page by clicking the version number you’re downloading.

Image

![Release notes link](../assets/images/security-update-module-release-notes.png)

Updating a module requires first putting your site into maintenance mode, then obtaining the new code files and applying any required database updates, then finally taking the site out of maintenance mode.

You can update the code for a contributed module using Composer. If you are updating a custom module rather than a contributed module, obtain the new module files, then continue with instructions for running the database updates via the administrative interface below.

This assumes that you are using Composer to manage the files in your site; see [Section 3.6, “Using Composer to Download and Update Files”](https://drupalize.me/tutorial/user-guide/install-composer "3.6. Using Composer to Download and Update Files").

#### Update a contributed module with Composer

1. Put your site in maintenance mode. See [Section 11.2, “Enabling and Disabling Maintenance Mode”](https://drupalize.me/tutorial/user-guide/extend-maintenance "11.2. Enabling and Disabling Maintenance Mode").
2. In the *Manage* administrative menu, navigate to *Reports* > *Available updates* > *Update* (*admin/reports/updates*).
3. Find and check the module in the list. Click *Download these updates* for the module.

   Image

   ![Available updates](../assets/images/security-update-module-updates.png)
4. Determine the short name of the project you want to update. For contributed modules and themes, it is the last part of the URL of the project page; for example, the Geofield module, at <https://www.drupal.org/project/geofield>, has short name `geofield`.
5. If you want to update to the latest stable release, use the following command, substituting the short name of the project to be updated for `geofield`:

   ```screen
   composer update drupal/geofield --with-dependencies
   ```

+ To learn how to download specific versions see [Section 3.6, “Using Composer to Download and Update Files”](https://drupalize.me/tutorial/user-guide/install-composer "3.6. Using Composer to Download and Update Files").

1. After obtaining the new module files run any database updates page by typing the URL *example.com/update.php* in your browser.
2. Click *Continue* to run the updates. The database update scripts will be executed.
3. Click *Administration pages* to return to the administration section of your site.
4. Take your site out of maintenance mode. See [Section 11.2, “Enabling and Disabling Maintenance Mode”](https://drupalize.me/tutorial/user-guide/extend-maintenance "11.2. Enabling and Disabling Maintenance Mode").
5. Clear the Drupal cache (refer to [Section 12.2, “Clearing the Cache”](https://drupalize.me/tutorial/user-guide/prevent-cache-clear "12.2. Clearing the Cache")).

### Expand your understanding

- Review the site log (refer to [Section 12.4, “Concept: Log”](https://drupalize.me/tutorial/user-guide/prevent-log "12.4. Concept: Log")) once the updates are complete to check for errors.
- [Section 13.7, “Updating a Theme”](https://drupalize.me/tutorial/user-guide/security-update-theme "13.7. Updating a Theme")

Was this helpful?

Yes

No

Any additional feedback?

Previous
[13.5. Updating the Core Software](/tutorial/user-guide/security-update-core?p=2404)

Next
[13.7. Updating a Theme](/tutorial/user-guide/security-update-theme?p=2404)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close