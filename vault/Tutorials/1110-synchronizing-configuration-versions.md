---
title: "11.10. Synchronizing Configuration Versions"
url: "https://drupalize.me/tutorial/user-guide/extend-config-versions?p=2357"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
order: 56
---

# 11.10. Synchronizing Configuration Versions

## Content

### Goal

Synchronize the configuration between a development and live site.

### Prerequisite knowledge

- [Section 1.5, “Concept: Types of Data”](https://drupalize.me/tutorial/user-guide/understanding-data "1.5. Concept: Types of Data")
- [Section 3.1, “Preparing to Install”](https://drupalize.me/tutorial/user-guide/install-prepare "3.1. Preparing to Install")
- [Section 11.7, “Concept: Development Sites”](https://drupalize.me/tutorial/user-guide/install-dev-sites "11.7. Concept: Development Sites")
- [Section 11.8, “Making a Development Site”](https://drupalize.me/tutorial/user-guide/install-dev-making "11.8. Making a Development Site")

### Site prerequisites

- You must have a development copy of your production site. See [Section 11.8, “Making a Development Site”](https://drupalize.me/tutorial/user-guide/install-dev-making "11.8. Making a Development Site").
- The core Configuration Manager module must be installed on both the development and production sites. See [Section 4.3, “Installing a Module”](https://drupalize.me/tutorial/user-guide/config-install "4.3. Installing a Module") for instructions on how to install core modules.
- You must have changed configuration on either the production or development site (the *source site*), and want to synchronize the changes to the other site (the *destination site*). As an example, you can develop a new content type, fields, and views on your development site, and when it is all working correctly, deploy the changes to the live site.
- All configuration that should not be synchronized between the source and destination sites must be stored in configuration overrides in the *settings.php* file rather than in the database. See [Section 11.8, “Making a Development Site”](https://drupalize.me/tutorial/user-guide/install-dev-making "11.8. Making a Development Site").

### Steps

Sprout Video

1. In the source site, in the *Manage* administrative menu, navigate to *Configuration* > *Development* > *Configuration synchronization* > *Export* (*admin/config/development/configuration/full/export*).
2. Click *Export*. Your site will generate an archive of the full site configuration. Save the file on your local computer.
3. In the destination site, in the *Manage* administrative menu, navigate to *Configuration* > *Development* > *Configuration synchronization* > *Import* (*admin/config/development/configuration/full/import*).
4. Browse to find the downloaded configuration archive, and click *Upload*. Your configuration archive will be uploaded to the destination site, and you will be redirected to the configuration *Synchronize* page (*admin/config/development/configuration*) with a message saying your files were uploaded.
5. Verify that the differences shown on the page are what you expect. You may see configuration items that have been added, deleted, or changed; for changed items, you can click *View differences* to see what the changes are.
6. When you are satisfied, click *Import all* to import the configuration changes.

### Expand your understanding

- If the changes you have made involve only one configuration item (such as one view), you can use the single configuration export/import feature to deploy the change between sites. See [Section 11.9, “Deploying New Site Features”](https://drupalize.me/tutorial/user-guide/extend-deploy "11.9. Deploying New Site Features").
- After the step where you export the full configuration from the source site, you might also want to unpack the archive and commit it to a version control system, such as Git, to track changes in your site configuration. See [Section 11.11, “Managing File and Configuration Revisions with Git”](https://drupalize.me/tutorial/user-guide/extend-git "11.11. Managing File and Configuration Revisions with Git").

Was this helpful?

Yes

No

Any additional feedback?

Previous
[11.9. Deploying New Site Features](/tutorial/user-guide/extend-deploy?p=2357)

Next
[11.11. Managing File and Configuration Revisions with Git](/tutorial/user-guide/extend-git?p=2357)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close