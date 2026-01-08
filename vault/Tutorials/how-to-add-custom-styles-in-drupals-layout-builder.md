---
title: "How to Add Custom Styles in Drupal's Layout Builder"
url: "https://drupalize.me/tutorial/how-add-custom-styles-drupals-layout-builder?p=2653"
guide: "[[layout-builder]]"
---

# How to Add Custom Styles in Drupal's Layout Builder

## Content

The [Layout Builder Styles module](https://www.drupal.org/project/layout_builder_styles) extends the Drupal core Layout Builder UI to add the ability for editors to apply custom CSS classes to the blocks and sections that make up a layout. This gives layout editors more control over the look and feel of elements within a layout. It's especially useful when using Drupal's Layout Builder in conjunction with a design system like Bootstrap, Material UI, or your own predefined utility classes.

The module allows site builders to define new styles. Then, when placing a block into a layout, if there are any styles available for the block type, the user is presented with a select list where they can choose one or more to apply. When a style is applied, any CSS classes associated with the style are added to the markup. Also, a new style-specific [theme hook suggestion](https://drupalize.me/tutorial/discover-existing-theme-hook-suggestions) is added to the block to allow for further customization.

In this tutorial we'll:

- Install and configure the Drupal Layout Builder Styles module
- Learn how to define new styles
- Learn how anyone editing a layout can apply the styles we defined to a block or section in the layout to change the UX

By the end of this tutorial, you should be able to use the Layout Builder Styles module to allow editors to add predefined styles to existing layouts and blocks without writing any code.

## Goal

Use Layout Builder Styles module. Apply an error message style to blocks in the Basic page layout.

## Prerequisites

- [Introduction to Layout Builder](https://drupalize.me/tutorial/introduction-layout-builder)
- [Create a Flexible Layout for a Content Type](https://drupalize.me/tutorial/create-flexible-layout-content-type)
- [4.3. Installing a Module](https://drupalize.me/tutorial/user-guide/config-install?p=3069)

## Follow these steps

### Install and enable the module

Download the code for the contributed [Layout Builder Styles module](https://www.drupal.org/project/layout_builder_styles) using Composer, then enable the module using Drush or the Extend page.

If your site is based on Composer, run the following command from the root of your project:

```
composer require  drupal/layout_builder_styles
```

Once the module is installed, enable it either with Drush (`drush en layout_builder_styles`) or through the UI (in the Administration menu, navigate to *Extend* (*admin/modules*), select the module, then press the *Install* button).

Image

![Screenshot of extend section with Layout Builder Styles module](/sites/default/files/styles/max_800w/public/tutorials/images/enable_layout_builder_styles.png?itok=nAlXv3s6)

Learn more about [installing modules with Composer](https://drupalize.me/tutorial/user-guide/install-composer?p=3074), and [downloading and installing modules from Drupal.org](https://drupalize.me/tutorial/user-guide/extend-module-install?p=3072).

### Configure the module

The module requires someone with the *administer site configuration* permission to create new *styles*. Each style maps to one or more CSS classes that will be added to the DOM when the style is used. These styles can then be applied to the blocks and sections of a layout by anyone who can edit the layout.

In the *Manage* administration menu, navigate to *Configuration* > *Layout Builder Styles* (*admin/config/content/layout\_builder\_style*). This is the configuration page for the Layout Builder Styles module.

Image

![Screenshot of Layout Builder Styles configuration page](/sites/default/files/styles/max_800w/public/tutorials/images/layout_builder_styles_config.png?itok=OaOn3K4p)

The configuration is divided into two tabs:

- The default tab (*Styles*) is for creating, updating, and deleting styles.
- On the *Groups* tab, styles are grouped together, allowing site builders to select one or more styles from each group.

In an example configuration, you could create a *group* called "Padding" with a few *styles* that affect the amount of padding around a block. Or a *group* named "Background" to allow site builders to choose between multiple background styling options.

When creating a group, administrators can choose whether to restrict editors to choosing just one style from a group to apply to a block, or allowing multiple styles from the same group.

Limiting to one style per group is useful for sites which have styles attached to the corresponding markup of the layout plugin.

The multiple styles option is useful for sites whose style declarations rely strictly on CSS modifications. In this case, styles may be designed to be used in combinations, similar to Bootstrap, or Tailwind chained utility classes.

### Add a new style

On the *Styles* tab, select the *+ Add layout builder style* button. On the next screen enter a name for your new style. We will create a *Warning* style, reusing CSS classes from Drupal core's error messages. Add the CSS classes `messages` and `messages--error` in the *CSS classes* block.

Image

![Screenshot of Layout Builder Add Style interface](/sites/default/files/styles/max_800w/public/tutorials/images/layout_builder_add_style.png?itok=zTf6vq8C)

The Layout Builder Styles module provides the ability to apply styles to the entire Layout Builder layout plugin section or to the blocks placed in this section.

For this example, we want to apply the style to blocks, and restricted to the *Basic block* type inside the *Custom Block Types* dropdown.

Image

![Screenshot of Layout Builder Block Restriction Interface](/sites/default/files/styles/max_800w/public/tutorials/images/layout_builder_style_restrict_block.png?itok=gqFvR9uy)

Press the *Save* button to save your new style configuration.

### Test the style

Navigate to the *Manage Layout* section of the content type that has Layout Builder set up on your site. For this tutorial, we have it set up for the *Basic page* content type. In the *Administration menu*, navigate to *Structure* > *Content types* > *Basic page* > *Manage display* > *Manage layout* (*admin/structure/types/manage/page/display/default/layout*).

Add a section (or use an existing one) and then select *+ Add block*. In the right-side toolbar choose *+ Create custom block*.

Now in the block configuration form you should see a *Style* dropdown. Fill in the form, select the *Warning* style we created, and press *Save*.

Image

![Screenshot of adding style to basic block](/sites/default/files/styles/max_800w/public/tutorials/images/layout_builder_style_warning_block.png?itok=eiITZv16)

**Note**: The *Layout Builder Modal* module is used in our example site so the block form is displayed in a modal. To learn how to set it up yourself refer to [Use Layout Builder Modal When Creating Custom Blocks](https://drupalize.me/tutorial/use-layout-builder-modal-when-creating-custom-blocks).

After you save the configuration you should see your new block rendered in the style of Drupal error messages.

Image

![Screenshot of warning block](/sites/default/files/styles/max_800w/public/tutorials/images/layout_builder_style_warning_block_render.png?itok=_aA3Wnis)

**Note**: these styles only work since we are using the *Bartik* theme for this example. If you are using a different theme, make sure to define required classes in your theme's CSS. The Layout Builder Styles module does not define any CSS classes on its own, and instead expects those styles will be defined and loaded by the active theme.

## Recap

In this tutorial, we learned how to work with the Layout Builder Styles contributed module. The module allows editors to create styles and then apply them within the Layout Builder UI without writing code. Styles may be applied to either the sections or blocks in a layout. The module provides the option to apply multiple styles at once or restrict to one style per section or block. This is especially useful for sites that are based on a design system with utility classes that can be reused across the site.

## Further your understanding

- Change the setting of the *Warning* style so it is applied to the section instead of the block. What is the difference between the two looks?
- Explore theme hooks that are now available using Twig debug. Think about how Layout Builder Styles hooks can be used to modify the markup.

## Additional resources

- [Layout API](https://www.drupal.org/docs/drupal-apis/layout-api) (Drupal.org)
- [How to register layouts documentation](https://www.drupal.org/docs/drupal-apis/layout-api/how-to-register-layouts) (Drupal.org)
- [Layout Builder Styles module page](https://www.drupal.org/project/layout_builder_styles) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add Views to a Layout](/tutorial/add-views-layout?p=2653)

Next
[Adding Asset Libraries to Custom Layouts](/tutorial/adding-asset-libraries-custom-layouts?p=2653)

Clear History

Ask Drupalize.Me AI

close