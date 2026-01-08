---
title: "Use Layout Builder Restrictions to Configure Available Layouts and Blocks"
url: "https://drupalize.me/tutorial/use-layout-builder-restrictions-configure-available-layouts-and-blocks?p=2653"
guide: "[[layout-builder]]"
---

# Use Layout Builder Restrictions to Configure Available Layouts and Blocks

## Content

The [Layout Builder Restrictions](https://www.drupal.org/project/layout_builder_restrictions) module allows you to configure which layouts, and which blocks, should be available in the Layout Builder UI. This helps improve the user experience by removing blocks that you don't want someone to place into a layout. It also restricts which layouts are available for a content type. For example, you may allow an editor to change the layout for a blog page but restrict them to choosing between 1- or 2-column layouts. Yet, you can still provide a 3-column layout option for use in other scenarios.

In this tutorial we'll:

- Install the Layout Builder Restrictions module
- Learn how to curate the list of layouts for use on a per-content type basis
- Restrict the list of blocks available for placement via Layout Builder's UI

By the end of this tutorial you'll know how to use the Layout Builder Restrictions module to curate the list of layout and block options available to editors in the Layout Builder UI.

## Goal

Remove the "Two column" layout option from the Article content type, and allow the "Who's online" block to be placed in Article layouts but not Basic page layouts.

## Prerequisites

- [Introduction to Layout Builder](https://drupalize.me/tutorial/introduction-layout-builder)
- [Create a Flexible Layout for a Content Type](https://drupalize.me/tutorial/create-flexible-layout-content-type)
- [Change the Layout on a Per-Page Basis](https://drupalize.me/tutorial/change-layout-page-basis)
- [Limit Blocks Available in Layout Builder with Block List Override](https://drupalize.me/tutorial/limit-blocks-available-layout-builder-block-list-override)
- [4.3. Installing a Module](https://drupalize.me/tutorial/user-guide/config-install?p=3069)

## Drupal video tutorial: Layout Builder Restrictions module demo

Sprout Video

## Removing blocks from the list

The Layout Builder Restrictions module's functionality overlaps with the Block List Override module which we cover in [Limit Blocks Available in Layout Builder with Block List Override](https://drupalize.me/tutorial/limit-blocks-available-layout-builder-block-list-override). Both modules allow you to restrict the list of blocks available for an administrator to place via the Layout Builder UI.

Layout Builder Restrictions includes the addition to create a safelist, in addition to a blocklist. In addition to saying, "block these specific blocks", it lets you curate a specific selection of usable blocks. This can be helpful when new modules add new blocks and you don't want to have to review and change the configuration every time. However, these lists are per content type, not global (like Block List Override). So you would have to configure the list for each content type.

Layout Builder Restrictions also allows you to configure a safe list of layouts to use with a content type, a feature that Block List Override does not provide.

## Configure Layout Builder Restrictions

### Install and enable the Layout Builder Restrictions module

If your site is based on Composer, navigate to your terminal in the root of your site where the *composer.json* file is located and run the following command:

```
composer require  drupal/layout_builder_restrictions
```

Once the module is installed, enable it either with Drush or the UI.

Image

![Screenshot of extend section with Layout Builder Restrictions module](/sites/default/files/styles/max_800w/public/tutorials/images/enable_layout_builder_restrictions.png?itok=aYmlC93d)

Learn more about [installing modules with Composer](https://drupalize.me/tutorial/user-guide/install-composer?p=3074), and [downloading and installing modules from Drupal.org](https://drupalize.me/tutorial/user-guide/extend-module-install?p=3072).

### Explore configuration of the Layout Builder Restrictions module

Primary configuration of the Layout Builder Restrictions module is available through the content type management interface.

In the *Manage* administration menu, navigate to *Structure* > *Content types*, then choose the *Manage display* operation for the *Article* content type (*admin/structure/types/manage/article/display*).

If you don't have it already enabled, select the *Use Layout Builder* checkbox and select *Save*. Once this is enabled you should see that now we have two new sections available for us to explore under *Layout options*: *Blocks available for placement (all layouts & regions)* and *Layouts available for sections*.

Image

![Screenshot of Manage display section for article content type](/sites/default/files/styles/max_800w/public/tutorials/images/manage_display_article.png?itok=smMTxIlR)

Note that this configuration is for the Article content type and won't affect any other content types using Layout Builder.

### Remove *Two column* layout option from the Article content type.

Expand the *Layouts available for sections* fieldset, and select the *Allow only specific layouts* radio button. Then choose all layouts except *Two column*, and select *Save*.

Image

![Screenshot of Allow only specific layouts section](/sites/default/files/styles/max_800w/public/tutorials/images/exclude_two_column.png?itok=LD8eWMJ_)

### Check that *Two column* layout is not available for Articles

Once the configuration is saved, select the *Manage layout* button to open the Layout Builder UI. Then select the *+ Add section* link and notice that the *Two column* layout is excluded from the section's list of options.

Image

![Screenshot of excluded Two column section in Article add section interface section](/sites/default/files/styles/max_800w/public/tutorials/images/two_column_excluded.png?itok=loqkLiEr)

If you open the Layout Builder UI for the Basic page content type (or any other) you'll see that the *Two column* option is still available there:

Image

![Screenshot of Two column layout section in Basic page content type](/sites/default/files/styles/max_800w/public/tutorials/images/two_column_exists_on_basic_page.png?itok=1Dq9YPr8)

## Disable blocks using Layout Builder Restrictions

The Layout Builder Restrictions module can also be used to allow, or deny, blocks in the Layout Builder UI on a per content type basis. As an example, we'll deny the *Who's online* block from the Basic page content type.

### Exclude the *Who's online* block from Basic page content type

In the *Manage* administration menu navigate to *Structure* > *Content types*, then choose the *Manage display* operation for the *Basic page* content type (*admin/structure/types/manage/page/display*). Ensure that *Use Layout Builder* is enabled.

Expand the *Blocks available for placement (All layouts & regions)* fieldset provided by Layout Builder Restrictions. Scroll down to the *Lists (Views)* section and select *Restrict specific Lists (Views) blocks* option. You should see a list of views blocks available to be restricted. Select *Who's online*. Scroll to the bottom and select *Save*.

Image

![Screenshot of restricted Who's online block in Basic pages](/sites/default/files/styles/max_800w/public/tutorials/images/blacklist_whos_online.png?itok=v_JKd0B2)

### Check that this block is not available for placement on Basic pages

Select the *Manage layout* button. Then select the *+ Add block button*. Search for the word "Who" in the blocks list and notice that this block is not available for placement anymore.

Image

![Screenshot of search for Who's online block](/sites/default/files/styles/max_800w/public/tutorials/images/not_available_whos_online.png?itok=UKifpe3_)

The Layout Builder Restrictions module provides 2 options for blocks: *allow* and *restrict*. In different situations it's best to follow one or another approach. Typically, if your website uses Layout Builder on the majority of content types, and most pages on the site use it, then it's best to use *restrict* since the number of blocks that need to be unavailable typically will be less than the number of blocks that can be used within the Layout Builder UI.

On the other hand, if your site is using Layout Builder for one specific content type, like Landing page for example, and it is a very specific, restricted use case then you may go with the approach of *whitelist* controlling precisely what blocks might be used for landing pages of your site.

We encourage you to experiment with both approaches in order to figure out which is more useful, and maintainable, for your specific use-case.

## Recap

In this tutorial we installed and configured the Layout Builder Restrictions module. We learned how to limit the layout options available for the Article content type. We practiced how to restrict the blocks that can be used for layouts of Basic pages by removing the *Who's online* block from the available options.

## Further your understanding

- What is the difference between Layout Builder Restrictions and Block List Override module? When would you use one or another? Why?
- Enable Layout Builder Restrictions By Region module that comes with Layout Builder Restrictions and explore the features it adds.

## Additional resources

- [Layout Builder Restrictions documentation](https://www.drupal.org/project/layout_builder_restrictions) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Limit Blocks Available in Layout Builder with Block List Override](/tutorial/limit-blocks-available-layout-builder-block-list-override?p=2653)

Next
[Layout Builder Design Patterns](/tutorial/layout-builder-design-patterns?p=2653)

Clear History

Ask Drupalize.Me AI

close