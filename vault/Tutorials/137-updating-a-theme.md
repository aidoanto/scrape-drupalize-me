---
title: "13.7. Updating a Theme"
url: "https://drupalize.me/tutorial/user-guide/security-update-theme?p=2404"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
---

# 13.7. Updating a Theme

## Content

### Goal

Update a contributed theme on your site and run the *Database Updates* script.

### Prerequisite knowledge

- [Section 13.3, “Concept: Security and Regular Updates”](https://drupalize.me/tutorial/user-guide/security-concept "13.3. Concept: Security and Regular Updates")
- [Section 13.1, “Concept: Cron”](https://drupalize.me/tutorial/user-guide/security-cron-concept "13.1. Concept: Cron")

### Site prerequisites

- A contributed theme has been installed and there is an update available for it. See [Section 11.5, “Downloading and Installing a Theme from *Drupal.org*”](https://drupalize.me/tutorial/user-guide/extend-theme-install "11.5. Downloading and Installing a Theme from Drupal.org") and [Section 13.4, “Keeping Track of Updates”](https://drupalize.me/tutorial/user-guide/security-announce "13.4. Keeping Track of Updates").
- If your site is live, you should test this process in a development environment before running it on your production site. See [Section 11.8, “Making a Development Site”](https://drupalize.me/tutorial/user-guide/install-dev-making "11.8. Making a Development Site").
- You have created a full site backup. See [Section 12.3, “Concept: Data Backups”](https://drupalize.me/tutorial/user-guide/prevent-backups "12.3. Concept: Data Backups").
- If you want to use the user interface to check for updates, the core Update Manager module must be installed. See [Section 4.3, “Installing a Module”](https://drupalize.me/tutorial/user-guide/config-install "4.3. Installing a Module") for instructions on installing core modules.

### Steps

Sprout Video

Updating a contributed theme requires first putting your site into maintenance mode, then obtaining the new code files and applying any required database updates, then finally taking the site out of maintenance mode.

You can update the code for a contributed theme using Composer. If you are updating a custom theme rather than a contributed theme, obtain the new theme files, then continue with instructions for running the database updates via the administrative interface below.

This assumes that you are using Composer to manage the files in your site; see [Section 3.6, “Using Composer to Download and Update Files”](https://drupalize.me/tutorial/user-guide/install-composer "3.6. Using Composer to Download and Update Files").

#### Update a contributed theme with Composer

1. Put your site in maintenance mode. See [Section 11.2, “Enabling and Disabling Maintenance Mode”](https://drupalize.me/tutorial/user-guide/extend-maintenance "11.2. Enabling and Disabling Maintenance Mode").
2. In the *Manage* administrative menu, navigate to *Reports* > *Available updates* > *Update* (*admin/reports/updates*).
3. Find any themes in the list that need updating.

Image

![Available updates](/sites/default/files/styles/max_800w/public/user_guide/images/security-update-theme-updates.png?itok=VUcuuYqX)

1. Determine the short name of the project you want to update. For contributed modules and themes, it is the last part of the URL of the project page; for example, the Honey theme, at <https://www.drupal.org/project/honey>, has short name `honey`.
2. If you want to update to the latest stable release, use the following command, substituting the short name of the project to be updated for `honey`:

   ```screen
   composer update drupal/honey --with-dependencies
   ```

+ To learn how to download specific versions see [Section 3.6, “Using Composer to Download and Update Files”](https://drupalize.me/tutorial/user-guide/install-composer "3.6. Using Composer to Download and Update Files").

1. After obtaining the new theme files run any database updates page by typing the URL *example.com/update.php* in your browser.
2. Click *Continue* to run the updates. The database update scripts will be executed.
3. Click *Administration pages* to return to the administration section of your site.
4. Take your site out of maintenance mode. See [Section 11.2, “Enabling and Disabling Maintenance Mode”](https://drupalize.me/tutorial/user-guide/extend-maintenance "11.2. Enabling and Disabling Maintenance Mode").
5. Clear the Drupal cache (refer to [Section 12.2, “Clearing the Cache”](https://drupalize.me/tutorial/user-guide/prevent-cache-clear "12.2. Clearing the Cache")).

### Expand your understanding

- Review the site log, see [Section 12.4, “Concept: Log”](https://drupalize.me/tutorial/user-guide/prevent-log "12.4. Concept: Log"), once the updates are complete to check for errors.
- [Section 13.6, “Updating a Module”](https://drupalize.me/tutorial/user-guide/security-update-module "13.6. Updating a Module")

Was this helpful?

Yes

No

Any additional feedback?

Previous
[13.6. Updating a Module](/tutorial/user-guide/security-update-module?p=2404)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close