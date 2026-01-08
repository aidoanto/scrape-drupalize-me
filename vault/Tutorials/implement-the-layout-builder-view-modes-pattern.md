---
title: "Implement the Layout Builder View Modes Pattern"
url: "https://drupalize.me/tutorial/implement-layout-builder-view-modes-pattern?p=2653"
guide: "[[layout-builder]]"
---

# Implement the Layout Builder View Modes Pattern

## Content

We recommend planning ahead when using Layout Builder, documenting how you intend to use Layout Builder for your specific use-case, and then doing your best to stick to it. One approach that we've found works well for sites that need a maximum amount of flexibility (and have the resources to do the upfront planning and theming required) is using entity view modes.

This approach is similar in concept to component based design systems, where you do the initial work of creating a set of components that all work well together up-front, and then allow them to be mixed and matched in whatever way is necessary.

In this tutorial we'll:

- Create new view modes for the *Basic Page* content type representing the different components.
- Use the *ctools blocks* module to allow displaying an entity as a block and choosing which view mode to use when rendering the entity.
- Provide custom HTML and CSS styling for the new components.

By the end of this tutorial you'll know how to use Layout Builder in combination with entity view modes.

## Goal

Create 2 new view modes for the *Basic Page* content type, *Hero* and *CTA*, and use them in a layout.

## Prerequisites

- [Layout Builder Design Patterns](https://drupalize.me/tutorial/layout-builder-design-patterns)
- [Create a Flexible Layout for a Content Type](https://drupalize.me/tutorial/create-flexible-layout-content-type)
- [Change the Layout on a Per-Page Basis](https://drupalize.me/tutorial/change-layout-page-basis)

## Drupal video tutorial: Layout Builder View Modes demo

Sprout Video

## Getting started

In comparison to the other approaches outlined in [Layout Builder Design Patterns](https://drupalize.me/tutorial/layout-builder-design-patterns), this one requires the most work up-front to set up. Once set up, it provides a large amount of flexibility to editors while still ensuring consistent theming throughout the site.

For the purpose of this tutorial we have configured the *Basic page* content type to use Layout Builder. The content type has *Hero Image*, *Hero Text*, *CTA Text*, *CTA Link*, and *Body* fields added to it.

Example:

Image

![Screenshot of Manage display section of Basic page content type](/sites/default/files/styles/max_800w/public/tutorials/images/basic_page_fields.png?itok=_JilcsCQ)

### Create the *Hero* and *CTA* view modes

Go to *Structure* > *Display modes* > *View modes* > *Add view mode* (*admin/structure/display-modes/view/add*). Choose *Content*. Fill in the name *Hero* and select *Save*.

Image

![Screenshot of adding Hero view mode](/sites/default/files/styles/max_800w/public/tutorials/images/add_hero_view_mode.png?itok=8TMdwcGg)

Repeat the same actions to create a *CTA* view mode.

When you are done, you should see something like below in the view modes section for content:

Image

![Screenshot of view modes for content](/sites/default/files/styles/max_800w/public/tutorials/images/view_modes.png?itok=0iM5lpeC)

### Set up *Hero* view mode fields for Basic page content type

Navigate to the *Manage display* tab for the *Basic page* content type (*admin/structure/types/manage/page/display*). Open the *Custom display settings* fieldset. Enable *Hero* and *CTA* view modes. Then select *Save*.

Image

![Screenshot of view modes in manage display section of content types](/sites/default/files/styles/max_800w/public/tutorials/images/manage_display_view_modes.png?itok=RIdtsQgE)

Once the configuration is saved, switch to the *Hero* tab and configure it to have *Hero Image* and *Hero Text* present. Hide the rest of the fields.

Image

![Screenshot of Hero view mode on Basic page content type](/sites/default/files/styles/max_800w/public/tutorials/images/hero_view_mode.png?itok=lVU_Nt48)

### Set up *CTA* view mode fields for Basic page

Switch to the *CTA* tab and set it up so it has *CTA Link* and *CTA Text* displayed. Hide the rest of the fields.

Image

![Screenshot of CTA view mode on Basic page content type](/sites/default/files/styles/max_800w/public/tutorials/images/cta_view_mode.png?itok=NQLtX2ug)

### Clean up *Default* view mode

Switch to the *Default* tab and select the *Manage layout* button. In the Layout Builder UI, remove all of the extra blocks and sections.

The final result should look something like this:

Image

![Screenshot of clean default layout on Basic page content type](/sites/default/files/styles/max_800w/public/tutorials/images/clean_default_layout.png?itok=2WUXj74I)

### Install *ctools* and *ctools blocks* module

If you don't have it already installed on your project, install the *ctools* module. We'll use the included *ctools blocks* module's ability to create custom blocks that display an entity using a specified view mode.

If you manage your site with *Composer*, navigate to the root of your project and run the following command:

```
composer require drupal/ctools
```

Once installed, enable the *ctools* and *ctools blocks* modules.

### Build default layout sections for Basic page

Navigate to the *Manage display* tab for the *Basic page* content type (*admin/structure/types/manage/page/display/default*). Then select the *Manage layout* button. In the Layout Builder UI select the *+ Add section* link and add a *One column* section named *Hero*.

Image

![Screenshot of add section area of Layout Builder UI](/sites/default/files/styles/max_800w/public/tutorials/images/add_hero_section.png?itok=-SIflO0Y)

Repeat these steps and add a *Two column* section named *Content* with *25%/75%* width for columns.

Image

![Screenshot of add section area of Layout Builder UI - for content](/sites/default/files/styles/max_800w/public/tutorials/images/add_content_section.png?itok=4i1It89s)

### Place blocks inside the sections

In the Layout Builder UI select the *+ Add block* button inside the *Hero* section. In the right configuration pane at the top, select *Chaos Tools* > *Entity view (Content)*. Uncheck *Display title* and select *Hero* view mode. Rename block into *Hero*. Then select *Add block*. This creates a new block in the Layout that displays an entity using the *Hero* view mode.

Image

![Screenshot of placing Hero block into the Hero section](/sites/default/files/styles/max_800w/public/tutorials/images/place_hero_block.png?itok=qRwvSkjF)

Repeat the steps to create a *CTA* view mode block in the *25%* left column section.

Place the *Body* field inside the right *75%* section. Your final layout should look something like the following:

Image

![Screenshot of final default Basic page layout](/sites/default/files/styles/max_800w/public/tutorials/images/final_basic_page_layout.png?itok=huR68Iga)

### Add a node and test the new layout

In the *Manage* administration menu navigate to *Content* > *Add content* > *Basic page* (*node/add/page*). Then fill in the form with some testing data and select *Save*. You should see something similar to the result below:

Image

![Screenshot of final default Basic page layout with content](/sites/default/files/styles/max_800w/public/tutorials/images/test_layout_bp.png?itok=NXqkPPgW)

One thing you may have noticed is that the *Title* field, in our case "Test", rendered twice: once at the top, and once above the *CTA* area. This is happening because we are rendering in the view mode. By default, the template files for the view modes that are not *Default* or *Full text* (in other words, not page view modes) are rendered with titles.

This can be fixed within your theme by [overriding the relevant templates](https://drupalize.me/tutorial/override-template-file) and removing the title.

## Theme the component

In order to see the effects of this approach, and how it can help with keeping your code organized, let's apply some basic theming to one of the components. This assumes you're familiar with [overriding template files](https://drupalize.me/tutorial/override-template-file), and [adding CSS via asset libraries](https://drupalize.me/tutorial/attach-asset-library).

We'll focus on the CTA component, theming it in such a way that makes it reusable in different layouts, and in other situations, like Views.

## Customize the markup for the component

Using this approach allows theme developers to style individual components, like a CTA, or a hero image, independent of the layout in which they are used. This allows the components to be more reusable. Here's an example of what that styling could look like:

Image

![Screen shot of page with hero and CTA component themed with custom styles.](/sites/default/files/styles/max_800w/public/tutorials/images/themed-components-example.png?itok=vw1jiBVL)

Imagine that you can move the blue-and-white CTA component to another section in this layout, or use it in a different layout, and you can see how this approach is useful.

We'll start by creating a template file specific to this component. Remember, the component is an "entity + view mode" combination. In this case a **node entity using the *CTA* view mode**. Nodes are always rendered using the *node.html.twig* template, so that's the one we'll override.

One of the [theme hook suggestions](https://drupalize.me/tutorial/discover-existing-theme-hook-suggestions) for *node.html.twig* is `node--{VIEW MODE}.html.twig`. In this case *node--cta.html.twig*. This will be used when any node is rendered using the CTA view mode.

### Create a new template for the node CTA component

Create the file *templates/components/cta/node--cta.html.twig* in your theme with the following code:

```
{#
/**
 * @file
 * Display a node in the CTA view mode.
 */
#}
{%
  set classes = [
    'node',
    'node--type-' ~ node.bundle|clean_class,
    node.isPromoted() ? 'node--promoted',
    node.isSticky() ? 'node--sticky',
    not node.isPublished() ? 'node--unpublished',
    view_mode ? 'node--view-mode-' ~ view_mode|clean_class,
    'clearfix',
    'cta',
  ]
%}

{{ attach_library('kitrab/node.cta') }}

<div{{ attributes.addClass(classes) }}>
  <div{{ content_attributes.addClass('node__content', 'clearfix') }}>
    {{ content }}
  </div>
</div>
```

This outputs just the content of the fields configured for the CTA view mode and some contextual classes. It also attaches a component specific CSS library which we'll create next. You'll need to make sure the library name matches the one you create by changing `kitrab/` to the name of your theme.

### Add a node.cta asset library

[Create a *THEMENAME.libraries.yml* file](https://drupalize.me/tutorial/define-asset-library), or add to an existing one with the following code:

```
node.cta:
  css:
    component:
      templates/components/cta/cta.css: {}
```

### Add styling in a new CSS file

Then, in your theme, create the CSS file this new library references, *templates/components/cta/cta.css*, with the following styles:

```
.cta .node__content {
  align-items: center;
  border: 4px solid #0a6eb4;
  border-top-width: 1px;
  border-left-width: 1px;
  display: flex;
  flex-direction: column;
  margin: 0 10px;
  padding: 8px;
  text-align: center;
}

.cta .node__content .field--name-field-cta-link a {
  background: #0a6eb4;
  color: white;
  display: block;
  margin: 10px 0;
  padding: 4px 8px;
}
```

### Clear caches

Now [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache). And refresh the page to see your new component theming applied.

The result is a styled component that editors can place into any part of a layout, and developers can quickly find the related code.

Can you repeat the same steps for the hero component? In the end you should have a directory structure like the following:

```
.
├── kitrab.info.yml
├── kitrab.libraries.yml
└── templates
    └── components
        ├── cta
        │   ├── cta.css
        │   └── node--cta.html.twig
        └── hero
            ├── hero.css
            └── node--hero.html.twig
```

## Recap

In this tutorial we learned how to use entity view modes within a layout. To do so we defined a layout with 3 sections. Then we created new view modes that correspond to those sections. Next we rendered the page content into the layout via custom blocks that displayed portions of the entity using the previously-created view modes. And finally we demonstrated how theme developers can design and implement the different view modes.

## Further your understanding

- Is this technique a good fit for your project? Why? Why not?
- What would be some good use cases for this approach?

## Additional resources

- [Layout Builder documentation](https://www.drupal.org/docs/8/core/modules/layout-builder) (Drupal.org)
- [Layout API](https://www.drupal.org/docs/drupal-apis/layout-api) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Layout Builder Design Patterns](/tutorial/layout-builder-design-patterns?p=2653)

Next
[Use Layout Builder Modal When Creating Custom Blocks](/tutorial/use-layout-builder-modal-when-creating-custom-blocks?p=2653)

Clear History

Ask Drupalize.Me AI

close