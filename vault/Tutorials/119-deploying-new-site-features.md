---
title: "11.9. Deploying New Site Features"
url: "https://drupalize.me/tutorial/user-guide/extend-deploy?p=2357"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
order: 93
---

# 11.9. Deploying New Site Features

## Content

### Goal

Copy a view that you have created in a local development site to the production site.

### Prerequisite knowledge

- [Section 11.8, “Making a Development Site”](https://drupalize.me/tutorial/user-guide/install-dev-making "11.8. Making a Development Site")
- [Section 11.10, “Synchronizing Configuration Versions”](https://drupalize.me/tutorial/user-guide/extend-config-versions "11.10. Synchronizing Configuration Versions")
- [Section 11.7, “Concept: Development Sites”](https://drupalize.me/tutorial/user-guide/install-dev-sites "11.7. Concept: Development Sites")

### Site prerequisites

- The core Configuration Manager module must be installed in both the development and production sites. See [Section 4.3, “Installing a Module”](https://drupalize.me/tutorial/user-guide/config-install "4.3. Installing a Module") for instructions on installing core modules.
- The Vendor content type must exist in both the development and production sites, with the same fields. See [Section 6.1, “Adding a Content Type”](https://drupalize.me/tutorial/user-guide/structure-content-type "6.1. Adding a Content Type").
- The Vendors view must exist in the development site but not the production site. See [Section 9.3, “Creating a Content List View”](https://drupalize.me/tutorial/user-guide/views-create "9.3. Creating a Content List View").

### Steps

Sprout Video

1. Open the local development site.
2. In the *Manage* administrative menu, navigate to *Configuration* > *Development* > *Configuration synchronization* > *Export* > *Single item* (*admin/config/development/configuration/single/export*). The *Single export* page appears.
3. Select *View* from the *Configuration type* list.
4. Select Vendors from the *Configuration name* list. The configuration appears in the textarea.
5. Copy the configuration from the textarea.

   Image

   ![Export a single item](../assets/images/extend-deploy-export-single.png)
6. Open the production site.
7. In the *Manage* administrative menu, navigate to *Configuration* > *Development* > *Configuration synchronization* > *Import* > *Single item* (*admin/config/development/configuration*). The *Import* page appears.
8. Select *View* from the *Configuration type* list.
9. Paste the configuration in the textarea.
10. Click *Import*. The confirmation page appears.
11. Click *Confirm*.
12. Verify that the view was imported by navigating in the *Manage* administrative menu to *Structure* > *Views*.

### Expand your understanding

The steps in this topic show how to export and import a single configuration item. However, often if you develop functionality on a development website and want to transfer it to your production site, you will need to transfer multiple configuration items. For instance, if you developed a new content type with fields, you would need to transfer several configuration items for each field, one for the content type itself, and possibly multiple view mode and form mode items, and they would have to be transferred in the right order. Getting this right can be both tedious and difficult.

As an alternative, you can export and import the complete configuration of the site. For this, you would need a local development site that is a clone of the production site (see [Section 11.8, “Making a Development Site”](https://drupalize.me/tutorial/user-guide/install-dev-making "11.8. Making a Development Site")), and then you can follow the steps in [Section 11.10, “Synchronizing Configuration Versions”](https://drupalize.me/tutorial/user-guide/extend-config-versions "11.10. Synchronizing Configuration Versions") to synchronize configuration between development and production sites.

Another alternative is to use the [contributed Features module](https://www.drupal.org/project/features), which allows exporting and importing bundled functionality (for example, all the configuration for a photo gallery).

Finally, if you do not see the effect of these changes in your site, you might need to clear the cache. See [Section 12.2, “Clearing the Cache”](https://drupalize.me/tutorial/user-guide/prevent-cache-clear "12.2. Clearing the Cache").

### Related concepts

- [Section 11.7, “Concept: Development Sites”](https://drupalize.me/tutorial/user-guide/install-dev-sites "11.7. Concept: Development Sites")
- [Section 2.6, “Concept: Editorial Workflow”](https://drupalize.me/tutorial/user-guide/planning-workflow "2.6. Concept: Editorial Workflow")

Was this helpful?

Yes

No

Any additional feedback?

Previous
[11.8. Making a Development Site](/tutorial/user-guide/install-dev-making?p=2357)

Next
[11.10. Synchronizing Configuration Versions](/tutorial/user-guide/extend-config-versions?p=2357)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close