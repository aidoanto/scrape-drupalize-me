---
title: "Use Layout Builder Modal When Creating Custom Blocks"
url: "https://drupalize.me/tutorial/use-layout-builder-modal-when-creating-custom-blocks?p=2653"
guide: "[[layout-builder]]"
---

# Use Layout Builder Modal When Creating Custom Blocks

## Content

One of the biggest UX problems with the current Layout Builder UI in core is that the control panel is often too narrow. This is especially noticeable when creating inline blocks, and working with WYSIWYG fields. The contributed [Layout Builder Modal module](https://www.drupal.org/project/layout_builder_modal) is one solution to address this problem. It moves the UI for creating, and editing, custom blocks in a Layout into a wider modal window.

In this tutorial we'll:

- Install the Layout Builder Modal module
- Demonstrate how it can be used to improve the UX of managing custom blocks in Layout Builder

By the end of this tutorial you should know what the Layout Builder Modal module does, and determine if it's useful for your project.

## Goal

Install and configure the Layout Builder Modal module.

## Prerequisites

- [Introduction to Layout Builder](https://drupalize.me/tutorial/introduction-layout-builder)
- [Setup basic flexible layout per content type with Layout Builder](https://drupalize.me/tutorial/create-flexible-layout-content-type)
- [4.3. Installing a Module](https://drupalize.me/tutorial/user-guide/config-install?p=3069)

## Overview

After setting up this module you will have a better experience for editing layouts. The comparison screenshot below shows the default UI on the left, and using Layout Builder Modal on the right:

Image

![Screenshot of Layout Builder UI with and without the modal](/sites/default/files/styles/max_800w/public/tutorials/images/layout_builder_comparison.png?itok=CZ-zvPI8)

## Drupal video tutorial: Layout Builder Modal module demo

Sprout Video

## Install and configure the Layout Builder Modal module

### Install and enable the module

In this step, we'll download the code for the contributed [Layout Builder Modal module](https://www.drupal.org/project/layout_builder_modal) using Composer, then install/enable the module using Drush or the Extend page.

If your site is based on Composer, run the following command from the root of your project:

```
composer require  drupal/layout_builder_modal
```

Once the module is installed, enable it either with Drush (`drush en layout_builder_modal` or through the UI (navigate to *Extend* (*admin/modules*), select the module then select the Install button).

Image

![Screenshot of extend section with Layout Builder Modal module](/sites/default/files/styles/max_800w/public/tutorials/images/enable_layout_builder_modal.png?itok=I3WFMv8L)

Learn more about [installing modules with Composer](https://drupalize.me/tutorial/user-guide/install-composer?p=3074), and [downloading and installing modules from Drupal.org](https://drupalize.me/tutorial/user-guide/extend-module-install?p=3072).

### Explore configuration of the Layout Builder Modal module

In the *Manage* administration menu, navigate to *Configuration* > *Layout Builder Modal* (*admin/config/user-interface/layout-builder-modal*). This is the configuration page for the Layout Builder Modal module.

**Note:** This requires the *administer layout builder modal* permission.

Image

![Screenshot of Layout Builder Modal configuration page](/sites/default/files/styles/max_800w/public/tutorials/images/layout_builder_modal_config.png?itok=xBQlWPXY)

The 2 required parameters in the configuration are *Width* and *Height*; they define the size of your modal. We recommend setting the height of the modal to *auto* to avoid content overflow and vertical scrolling inside the modal window.

The *Auto resize* option makes the modal automatically fit the content. Using this option will prevent editors from needing to resize the modal manually. Depending on your editorial workflow, and devices and screen sizes used while editing, you may choose to leave this option *on* or *off*. By default it is *on* to ensure that the content fits the modal.

Layout Builder Modal module uses the jQuery Dialog plugin that is (at the time of writing) part of the Drupal core. The community is working on removing jQuery UI components from Drupal core. Once complete, the module will require an external library be installed with it. You can [read more about those plans in this issue](https://www.drupal.org/project/drupal/issues/3067261).

### Render Layout Builder Modal using the admin theme

By default, the Layout Builder UI utilizes the front-end theme. It is worth noting that the front-end theme isn't always well-fit to handle back-end UI like WYSIWYG and configuration controls.

Layout Builder Modal module allows you to choose which theme should be used within the modal window. We recommend changing it to the admin theme in most cases.

Let's select the *Administrative theme (Seven)* option and select *Save configuration*.

### Verify it works

To test that it's working, in the *Manage* administration menu navigate to *Structure* > *Content types*, then choose the *Manage display* operation for the *Basic page* content type (*admin/structure/types/manage/page/display*). Then select *Manage layout* to open the Layout Builder UI, and select the *+ Add block* for any section. In the right control panel choose *+ Create custom block*.

Image

![Screenshot of Layout Builder UI](/sites/default/files/styles/max_800w/public/tutorials/images/layout_builder_create_custom_block_btn.png?itok=dYyvPBub)

You should see that instead of opening block configuration inside the right off-canvas panel, a modal is opened up and it provides a wider window to allow for a better experience within WYSIWYG fields.

Image

![Screenshot of Layout Builder Modal](/sites/default/files/styles/max_800w/public/tutorials/images/layout_builder_modal_window.png?itok=5iQ3PMKv)

## Recap

In this tutorial we learned how to enhance the editorial experience of managing custom blocks in a layout by a using modal window rather than the default off-canvas panel. We accomplished this by installing and configuring the contributed Layout Builder Modal module.

## Further your understanding

- When would you want to use the front-end theme to render the modal vs. the administrative theme?
- Switch the theme to the front-end theme in the module settings, and test it out. What are the main differences, advantages, and disadvantages?

## Additional resources

- [Layout Builder Modal module](https://www.drupal.org/project/layout_builder_modal) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Implement the Layout Builder View Modes Pattern](/tutorial/implement-layout-builder-view-modes-pattern?p=2653)

Next
[Define Custom Layouts in a Module or Theme](/tutorial/define-custom-layouts-module-or-theme?p=2653)

Clear History

Ask Drupalize.Me AI

close