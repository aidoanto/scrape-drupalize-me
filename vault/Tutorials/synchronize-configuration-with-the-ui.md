---
title: "Synchronize Configuration with the UI"
url: "https://drupalize.me/tutorial/synchronize-configuration-ui?p=2478"
guide: "[[drupal-site-administration]]"
order: 6
---

# Synchronize Configuration with the UI

## Content

The Configuration Manager module gives you as an administrator the ability to import and export configuration items on different instances of a Drupal site using a graphical user interface. In this tutorial, we'll take a tour of the Configuration Manager and the administrative interface it provides.

By the end of this lesson you will be able to:

- Access administrative pages for Import, Export, and Synchronize
- Find and configure permissions for Configuration Manager
- Identify the 3 primary actions of configuration management and how to perform them using the UI

## Goal

- Import and export configuration using the administrative interface.

## Prerequisites

- [Overview: Configuration Management in Drupal](https://drupalize.me/tutorial/overview-configuration-management-drupal)

## Overview

The configuration system gives you the ability to move configuration from one instance (or clone) of a Drupal site to another, such as from local development to production. One of Drupal's core modules is the Configuration Manager, which provides an administrative interface to import, export, and synchronize configuration items between Drupal site instances.

Sprout Video

The core Configuration Manager module is enabled by default when you select the standard installation profile. You can access help, permissions, and configure pages via its listing on the *Extend* administrative page in the *Core* section.

Image

![Configuration Manager module as listed on the Extend page](../assets/images/extend_config_manager.png)

*Configuration Manager module as listed on the Extend page.*

## Permissions

The Configuration Manager module provides 3 permissions that cover the 3 primary actions of configuration management:

- Export configuration
- Import configuration
- Synchronize configuration

Using the *Manage* menu, navigate to *People* > *Permissions* (*admin/people/permissions*) and look under the *Configuration Manager* heading to view these permissions.

Image

![Permissions for the Configuration Manager module](../assets/images/permissions_config_manager.png)

*Permissions for the Configuration Manager module.*

All of these permissions should only be enabled for site administrators, as they provide the ability to change the configuration of one site instance based on another site instance. Anyone with the "synchronize configuration" permissions can introduce changes to the configuration of the site.

## Synchronize configuration

The process of configuration sync involves 3 steps:

1. Export: export the full configuration as YAML files from one instance of a site.
2. Import: stage the configuration on a second instance of the site and compare the differences.
3. Synchronize: move the staged configuration from the first site into the active configuration of the second site.

Using the Configuration Manager, we can perform these actions using the administrative UI provided by the module, which can be accessed through any of the following pathways:

- Configuration > Development > Configuration synchronization
- Extend > Configuration Manager > Configure
- *admin/config/development/configuration*

These 3 steps are broken out into 3 pages which you can access via the menu tabs: Synchronize, Import, and Export. Note that the order of these tabs might not be the order that you perform the operations. "It depends." Read through this tutorial first before you decide which step you need to perform first.

## Synchronize

Image

![Synchronize UI for the Configuration Manager](../assets/images/synchronize_config_manager.png)

If you have made changes to the configuration of your site (changes in *active configuration*) or have imported configuration items from another instance to your configuration sync directory (using the Import tab for example), the Synchronize page is where you will examine which configuration items are affected and what the differences are.

For example, let's say you've made a change to the site title and slogan on the local instance of your site. This change exists in your site instance's active configuration, but only in your instance because it hasn't been exported. The Synchronize tab shows you exactly this. Specifically, the `system.site` configuration item is affected. (However, if this is a new install, there is nothing in the sync directory and the Synchronize tab is comparing to the snapshot storage.)

Image

![Synchronize tab shows changes in configuration](../assets/images/synchronize_changes_config_manager.png)

Since there are differences, you can click on the View differences button. The plus and minus signs tells you what will be removed and what will be added if you clicked the Import all button on the Synchronize page.

Image

![View differences](../assets/images/view_diff_config_manager.png)

However, if you want to keep the changes you made in active configuration, you will need to export your active configuration to a compressed site archive (saving it to your computer) using the Export tab...

Image

![Export UI for the Configuration Manager](../assets/images/export_config_manager.png)

...and then import that compressed file archive right back in, using the Import tab.

It is only after completing those steps will the active configuration be in sync with the files in the configuration sync directory, and the changes you made to the site title and slogan be ready for import into another instance of the site.

## Import configuration to a different instance

[On a different instance of the site](https://drupalize.me/tutorial/clone-drupal-site-using-web-based-tools), to update the site title and slogan to match your local configuration, use the import tab to import the site archive you just exported from your local instance and saved to your computer.

Image

![Import UI for the Configuration Manager](../assets/images/import_config_manager.png)

Once the archive is uploaded and "staged", you will be redirected to the Synchronize tab where you can view the differences and verify the changes that will be made when you complete the import and synchronization process by clicking the "Import all" button.

Image

![Uploaded configuration ready for import](../assets/images/sync_ready_import_config_manager.png)

After you click "Import all", a batch operation will begin and a progress bar will display. After it is complete (if all went well) a message displays, confirming the successful import.

Image

![Successful import of configuration](../assets/images/config_imported_successfully_ui_msg.png)

You can now see the new site title and slogan on this instance of your site.

Note: if you're importing configuration on a live production site, you may first want to put your site in maintenance mode.

## Full archive vs. single-item

On both the Import and Export tab, you have a choice of full archive or single-item import or export. The full archive method is preferred and recommended, even if you are confident about which configuration types are affected. In Drupal 7, the Views module provided the ability to export and import single views. As Views is now in core, the single-item import/export option merely exists to prevent a regression in functionality in Views as a contributed module for Drupal 7.

You can (and should) use the full archive option even if only one configuration item is affected. This is the default option when you click on the Import or Export menu items.

Image

![Export: full archive option](../assets/images/export_full_archive.png)

Image

![Import: full archive option](../assets/images/import_full_archive.png)

## Alternatives to the Configuration Manager UI

You don't have to use the UI to manage configuration. In fact, you may prefer to only use command line tools to export and import configuration. Learn how to manage configuration through Drush and Git instead of the UI in this tutorial:

- [Inspect Configuration with Drush](https://drupalize.me/tutorial/inspect-configuration-drush)

You might decide that allowing access to the Configuration Manager UI on your production site could very easily backfire. To learn how you can disallow configuration changes through the UI on your production site, see the project page for the contributed module, [Configuration Read-Only Mode](https://www.drupal.org/project/config_readonly).

## Recap

In this tutorial, we reviewed what you can do using the Configuration Manager UI to import, export, and synchronize your site's configuration. You can use this UI to import and export a single item or a full set of configuration. In this way, you can move configuration from one instance of your site, like your local development site to your live production site using the administrative UI.

## Further your understanding

- Experiment with making changes to configuration on a local Drupal site, checking in with the Synchronize page after each change that you make. What happens when you click the "Import all" button on the synchronize tab? How can you save your changes in active configuration to YAML files in your site's configuration sync directory using the Configuration Manager UI? What is an alternative toolchain for managing configuration?
- On which instance of the site might it be prudent to disallow changes to configuration using the UI?
- Who on your team should have permissions to use the Configuration Manager? Do they understand the implications of this? Discuss with your site's stakeholders what the policy and procedures should be for managing configuration on your Drupal site.

## Additional resources

- [Inspect Configuration with Drush](https://drupalize.me/tutorial/inspect-configuration-drush) (Drupalize.Me)
- [Configuration Read-Only Mode](https://www.drupal.org/project/config_readonly) (Drupal.org)
- [Rebuilding POP in D8: Configuration Management](https://www.lullabot.com/articles/rebuilding-pop-in-d8-configuration-management) (Lullabot.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Clone a Drupal Site using Web-Based Tools](/tutorial/clone-drupal-site-using-web-based-tools?p=2478)

Next
[Synchronize Configuration with Drush](/tutorial/synchronize-configuration-drush?p=2478)

Clear History

Ask Drupalize.Me AI

close