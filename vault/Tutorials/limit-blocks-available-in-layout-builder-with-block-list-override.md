---
title: "Limit Blocks Available in Layout Builder with Block List Override"
url: "https://drupalize.me/tutorial/limit-blocks-available-layout-builder-block-list-override?p=2653"
guide: "[[layout-builder]]"
---

# Limit Blocks Available in Layout Builder with Block List Override

## Content

When building with Layout Builder, the list of blocks available for a site administrator to place in a layout can grow and become overwhelming to navigate. This is especially true when you've got a lot of different modules enabled, as each can add new blocks. As well, complex configurations may require site admins to create more and more custom blocks. Some blocks, like certain Views, or default core blocks like "Who's online", are not meant to be used within the Layout Builder. These blocks can clutter the UI and also impact the performance of Layout Builder UI. The contributed module [Block List Override](https://www.drupal.org/project/block_list_override) is designed to help solve this problem.

In this tutorial we'll:

- Learn what the Block List Override module does
- Install and configure the module to improve the user experience when creating layouts

By the end of this tutorial you should know how to use the Block List Override module to improve the UX of the Layout Builder interface.

## Goal

Install and configure the Block List Override module, and learn how to prevent certain blocks from appearing in the Layout Builder UI.

## Prerequisites

- [Layout Builder overview](https://drupalize.me/tutorial/introduction-layout-builder)
- [Create a Flexible Layout for a Content Type](https://drupalize.me/tutorial/create-flexible-layout-content-type)
- [Change the Layout on a Per-Page Basis](https://drupalize.me/tutorial/change-layout-page-basis)
- [4.3. Installing a Module](https://drupalize.me/tutorial/user-guide/config-install?p=3069)

## Drupal video tutorial: Block List Override module demo

Sprout Video

## Follow these steps

Follow these steps to remove one or more blocks from the Layout Builder UI and restrict what a site administrator will see.

### Install and enable Block List Override module

If your site is based on Composer, navigate to your terminal in the root of your site where the *composer.json* file is located. Then run the following command to download the Block List Override module:

```
composer require drupal/block_list_override
```

If you don't manage your Drupal installation with Composer you can install the module by [downloading it from drupal.org](https://www.drupal.org/project/block_list_override).

Once the module is installed, enable it either with Drush:

```
drush en block_list_override -y
```

Image

![Screenshot of extend section with Block List Override module](/sites/default/files/styles/max_800w/public/tutorials/images/install_block_list_override.png?itok=KBXGdJNd)

...or through the UI. In the *Manage* administration menu, navigate to *Extend* (*admin/modules*), select the *Block List Override* module's checkbox and press the *Install* button.

[Learn more about downloading and installing modules](https://drupalize.me/tutorial/user-guide/extend-module-install).

### Configure the Block List Override module

In the *Manage* administration menu, navigate to *Configuration* and then choose *Block List Override Settings* (*/admin/config/block\_list\_override/settings*) from the list.

**Note:** This requires the "Access Block List Override" permission (*/admin/people/permissions#module-block\_list\_override*).

On the configuration page for the module there is a detailed description explaining the purpose of the module and how to use it.

The configuration of the module is split into two main sections:

- *System-wide list*: To hide blocks from the *Block layout* page and anywhere else on your Drupal website, including the Layout Builder UI.
- *Layout Builder list*: To hide blocks only from the Layout Builder UI.

System-wide list section:

Image

![Screenshot of the System-wide list section](/sites/default/files/styles/max_800w/public/tutorials/images/block_list_override_system_wide_list.png?itok=Tjb0_giV)

Layout Builder list section:

Image

![Screenshot of the Layout Builder list section](/sites/default/files/styles/max_800w/public/tutorials/images/block_list_override_layout_builder_list.png?itok=OemaHkvM)

### Hide the *Powered by Drupal* block from Layout Builder

To add a block to the list, you need to know its ID.

Navigate to the *System Block List* (*admin/config/block\_list\_override/system-list*) using the local menu tab.

Image

![System Block list menu tab](/sites/default/files/styles/max_800w/public/tutorials/images/block_list_override_system_block_list_tab.png?itok=xgmBOx9Q)

Find the *Powered by Drupal* block, and copy its block ID.

Image

![Screenshot of the Powered by Drupal block](/sites/default/files/styles/max_800w/public/tutorials/images/powered_by_drupal.png?itok=PH6At8xo)

Then navigate back to *Settings* using the local menu tab (*admin/config/block\_list\_override/settings*).

Paste the block ID into the *Layout Builder List Match* field and press the *Save configuration* button.

Image

![Screenshot of the Powered by Drupal block](/sites/default/files/styles/max_800w/public/tutorials/images/block_list_override_list_match.png?itok=bJeFgw81)

### Check that the block is excluded from Layout Builder UI

Navigate to the *Manage layout* section of a content type for which you have Layout Builder available. If you don't have any content types set up, learn more about how to get started in our tutorials outlined in the prerequisites section.

For this tutorial we have Layout Builder enabled for the *Basic page* (*admin/structure/types/manage/page/display/default/layout*) content type.

Press the *+ Add block* button and filter block list by the word "Powered". Notice that it returned no results. This is because we've hidden the block.

Image

![Screenshot of no results for Powered by Drupal block](/sites/default/files/styles/max_800w/public/tutorials/images/no_results_layout_builder.png?itok=wlgz0JLn)

### Check that the block is still available

In the Block layout section, check that the block is still available.

Navigate to the *Structure* > *Block layout* (*admin/structure/block*) and select the *Place* button on one of the regions. Filter by the word "Powered" and see that the block is still there.

Image

![Screenshot of Powered by Drupal block showing up in the Block layout list](/sites/default/files/styles/max_800w/public/tutorials/images/powered_by_drupal_block_layout.png?itok=TnDJJeOY)

### (Or) Hide *Powered by Drupal* block

Alternatively, hide the *Powered by Drupal* block from the entire website

Navigate to *Configuration* > *System* > *Block List Override Settings* (*admin/config/block\_list\_override/settings*). Copy the ID of *Powered by Drupal* block and paste it into the *System-wide List Match* field and select *Save configuration*.

Image

![Screenshot of system-wide list match configuration section](/sites/default/files/styles/max_800w/public/tutorials/images/block_list_override_system_list_match.png?itok=YEpg3OKq)

Navigate to *Structure* > *Block layout* (*admin/structure/block*) and try placing the "Powered by Drupal" block. Notice that the block doesn't show up in the search results anymore.

Image

![Screenshot of system-wide list match configuration section](/sites/default/files/styles/max_800w/public/tutorials/images/no_results_block_layout.png?itok=4dUC3Ykl)

Knowing which blocks to remove from the Layout Builder UI depends on your specific use-case, and we'll leave it up to you to figure out which blocks to add to the list.

## Recap

In this tutorial we covered step-by-step instructions of how to install and configure the Block List Override contributed module to hide blocks from the Layout Builder UI, and/or the sytem-wide Block layout list.

## Further your understanding

- What blocks do you think should be hidden on your project? Why?
- You can use prefixes, e.g.: *system\_*, to remove all blocks provided by the System module.

## Additional resources

- [Block List Override documentation](https://www.drupal.org/docs/contributed-modules/block-list-override) (Drupal.org)
- [Layout Builder documentation](https://www.drupal.org/docs/8/core/modules/layout-builder) (Drupal.org)
- [Layout API](https://www.drupal.org/docs/drupal-apis/layout-api) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Change the Layout on a Per-Page Basis](/tutorial/change-layout-page-basis?p=2653)

Next
[Use Layout Builder Restrictions to Configure Available Layouts and Blocks](/tutorial/use-layout-builder-restrictions-configure-available-layouts-and-blocks?p=2653)

Clear History

Ask Drupalize.Me AI

close