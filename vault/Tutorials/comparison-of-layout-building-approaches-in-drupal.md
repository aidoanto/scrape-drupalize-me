---
title: "Comparison of Layout-Building Approaches in Drupal"
url: "https://drupalize.me/tutorial/comparison-layout-building-approaches-drupal?p=2653"
guide: "[[layout-builder]]"
---

# Comparison of Layout-Building Approaches in Drupal

## Content

Layout Builder is one of many different approaches to handling editorial layouts in Drupal. Now that it's stable, and part of Drupal core, we expect to see it become the dominant approach over time. However, as with most things in Drupal, there are multiple ways to solve the problem of creating component based flexible layouts that can be administered via the user interface.

It's a good idea to understand the different approaches and know what's available.

When it comes to component based design and ability to construct flexible layouts, it is important to understand the benefits and risks of the most popular techniques: Paragraphs, Bricks, entities and view modes, and Layout Builder. Understanding which approach fits the needs of your project best can be critical for its success in the future.

In this tutorial we'll look at some common approaches to administering layouts in a way that gives content editors controls including:

- Drupal core's Layout Builder
- Using core's entity reference fields and view modes
- The contributed Paragraphs module
- The contributed Bricks module

By the end of this tutorial you should have a broad overview of the different popular approaches to creating editor-controlled layouts.

## Goal

Provide an overview of different approaches to building component-based flexible layouts in Drupal.

## Prerequisites

- None

## Entities and view modes

### When to use this approach

- Your project is built with an effort to minimize contributed modules and custom code.
- Stable well-tested solution is required.
- The goal of the project is to have component-based design without previewing the output prior to saving.
- Revision history for the components is not important and can be discarded.
- Your site needs to be fully translatable.

### Overview

The use of entities and view modes is arguably the least recognized technique that we will cover. However, it is available out of the box and can be improved with minimal contributed modules.

The approach is based on dividing content types on your site into 2 different categories: *main* content types and *helper* content types. Into the *main* category we place all of the content types that have *page* displays and are supposed to be accessed via a URL, not as part of another page. Into the helper category we will place content types that are meant to be used within other pages and not have their individual page displays.

Examples of main content types could be *Landing page* or *Article*. Examples of helper content types could be *Slider*, *Free Form HTML*, or *CTA*.

The idea is that main content types have a multivalue entity reference field that will link to helper content types. For example, *Landing page* can have an entity reference to the *Grid* helper content type. In turn, the Grid content type would have a multivalue entity reference to *CTA*. This allows editors to create grids of CTAs.

The second referenced item might be a *Slider*, and the third can be a *Full HTML Free Form*. Later on you can reorder the items with drag and drop and change the layout using just core functionality. A content creation form might look something like this:

Image

![Screenshot of multivalued entity reference approach](/sites/default/files/styles/max_800w/public/tutorials/images/multivalue_er.png?itok=VIgtPfZc)

This can be expanded with a few improvements. Using the [Inline Entity Form](https://www.drupal.org/project/inline_entity_form) module will allow for the creation of the helper child nodes from within the parent node's form.

The [Rabbit Hole](https://www.drupal.org/project/rabbit_hole) module allows you to hide the full page displays for the helper content types, preventing them from being indexed by bots and discovered by end users.

Parent content types may be expanded with options that apply to their children. For example, a Grid content type may have a setting for the number of columns. This setting could then be passed to the template using a preprocess function and used for theming.

### Advantages

The advantages of this approach are ease of setup and close to core functionality. It allows for settings to be created and exposed to editors by making additional content type fields on the parent content types. The resulting content is fully translatable through Drupal core's translation mechanism.

### Disadvantages

The experience of creating new content can be cumbersome and require multiple individual forms. Using Inline Entity Form can help with this. However, when using Inline Entity Form, content types are not revisionable.

There is ongoing work to fix this and to use *entity\_reference\_revisions* fields instead of *entity\_reference* core fields. But it may lead to unpredictable results because helper content types can be reused across the site, thus creating additional revisions that may cause problems on previously-created content types that are linking to the older revision.

This approach may require some custom code: preprocess functions and template overrides.

All of the other approaches are essentially opinionated implementations of the above approach.

## Paragraphs

### When to use this approach

- Allow multiple fields to be grouped together and then repeated multiple times in the node.
- If you are looking for a replacement for the *Field Collection* module.
- Looking for component-based revisionable design with a clean editorial UX.

### Technique

Originally the [Paragraphs module](https://www.drupal.org/project/paragraphs) wasn't designed for building layouts. Its primary feature is the ability to provide child fieldable entities that would improve the editorial experience of authoring structured content. It started as a way to move content entry from blobs of HTML in a WYSIWYG interface into fieldable editorial forms.

Later on, the community started using Paragraphs for layouts. It's particularly well suited for landing pages. The idea behind this technique is similar to the entity view modes technique. The Paragraphs module provides its own entity type. These entities can have different bundles, and in turn bundles can have different fields and form and display settings.

Different components equate to different bundles of paragraphs. Returning back to the example discussed above, in the case with Paragraphs all helper content types will become Paragraphs bundles: *Slider*, *Grid*, *CTA*, *Free form*. These bundles will be attached to the *Landing page* using the *Paragraphs* field that comes with the module, which is an enhanced entity reference field.

The content authoring form using this setup looks something like the following:

Image

![Screenshot of paragraphs setup](/sites/default/files/styles/max_800w/public/tutorials/images/paragraphs.png?itok=uux1oQAI)

### Advantages

Paragraphs are easy to set up and doesn't require any additional contributed modules to get started. It also allows for tracking revisions of the components as well as the main content type.

There's a predictable display since the majority of information is entered into individual fields instead of a WYSIWYG.

### Disadvantages

Paragraphs has a couple of known issues. One is the deletion of paragraphs and revisions when the main entity is deleted. This is a long-standing issue and the community is testing patches to fix it.

Paragraphs requires special setup for multilingual sites. More details about this can be found in the Drupal Wiki page, [Multilingual Paragraphs configuration](https://www.drupal.org/docs/contributed-modules/paragraphs/multilingual-paragraphs-configuration).

Paragraphs doesn't allow editors to visualize the outcome prior to hitting save on the editorial form.

## Bricks

### When to use this approach

- Bricks is designed to control field layouts, compared to Layout Builder which controls an entity's layout.
- Fully multilingual
- Can be revisionable (with additional module)
- Allows nesting of different components, and a drag & drop interface for content creation, as well as surfacing display related settings to content editors
- Works well with other layout solutions like Layout Builder or Paragraphs

### Technique

Each component is a Bricks bundle. There is a special layout brick type specifically for layouts. Bricks are attached to the *main* content type using a special Bricks entity reference field that renders components as a tree and allows for nesting.

Bricks is perfect for having a parent brick with special configuration options, like speed of the slider or its mode (e.g. slide, fade), and child bricks representing slides nested within it.

Bricks allows editors to go a few levels deep into the structure of the page and better visualize hierarchy of components on the page.

An example setup of Bricks can look something like the following:

Image

![Screenshot of Bricks setup](/sites/default/files/styles/max_800w/public/tutorials/images/bricks.png?itok=wTfBhnUC)

You notice that in *Bricks* setup there is an ability to switch view modes for each brick as well as add additional CSS classes right from the UI. This is useful when a front-end framework like Bootstrap is being used; application of different classes allows for different style results without the need for extra code.

### Advantages

- Built for layouts
- Fully translatable
- Allows for nesting of components
- Can be used in combination with Paragraphs
- Flexible, fully customizable solution
- Uses core Layout Discovery API

### Disadvantages

- Fully-contributed solution
- Overly-complex for simple use-cases

## Layout Builder

### When to use this approach

- You need a flexible visual interface for building layouts.
- Advanced use of Layout Discovery API is required for the project.
- Minimize contributed modules; everything needed is in core.
- Your site is not multilingual (multilingual support is possible but with additional contributed modules and some limitations).
- You want to merge together different types of entities including blocks, custom entities, content entities, and Views.

### Technique

Layout Builder and its ecosystem can be used to provide layouts for entities. It works with any entity, and can work per bundle (e.g. content type) or per entity. The basic setup can be achieved with only core modules. Advanced use supports creation of custom layouts in a module or theme as well as utilization of some contributed modules to allow for additional refinements of the functionality.

Layouts are up in the *Manage Display* section for the content type (or entity bundle) either for the entire content type or on a node by node basis. After sections are placed inside the layout container, editors place blocks and fields of the content type inside the sections.

Layout Builder is a visual interface and provides real-time preview for editors.

Learn more about using [Layout Builder](https://drupalize.me/tutorial/introduction-layout-builder).

### Advantages

- Does not require any contributed modules, though can be enhanced by using them.
- Full support for revisions.
- Allows editors to preview the final result.
- Allows for various degrees of complexity in its setup from simple layout by content type to dynamic custom layouts defined in a custom module.

### Disadvantages

- Relatively new; some rough edges may require the use of patches.
- Does not support nesting, two-dimensional layouts only.
- Requires more robust editorial skills; fewer pre-configured options and more different choices that can yield endless amounts of combinations.

## Recap

In this tutorial we compared different common approaches to building component-based flexible layouts in Drupal. Each of these options: content types, Paragraphs, Bricks, and Layout Builder, come with their advantages, disadvantages, and different difficulty level for the initial setup. Choosing the option that is the best choice for your project requirements is key to the entire project success and its maintainability. We recommend taking the time to explore modules like Paragraphs and Bricks, and familiarize yourself with their capabilities to help make better informed decisions about what to use and when.

Finally, if you're not sure, or if Layout Builder satisfies your needs, we recommend using it. Solutions provided by Drupal core tend to have better documentation and long-term community support.

## Further your understanding

- What approach is best for your project? Why?
- What other approaches can be used to build flexible layouts now in Drupal?
- Use [simplytest.me](https://simplytest.me) to install and try Paragraphs and Bricks.

## Additional resources

- [Layout Builder documentation](https://www.drupal.org/docs/8/core/modules/layout-builder) (Drupal.org)
- [Bricks](https://www.drupal.org/project/bricks) (Drupal.org)
- [Paragraphs documentation](https://www.drupal.org/docs/contributed-modules/paragraphs) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Define Custom Layouts in a Module or Theme](/tutorial/define-custom-layouts-module-or-theme?p=2653)

Next
[Tips for Theming with Layout Builder](/tutorial/tips-theming-layout-builder?p=2653)

Clear History

Ask Drupalize.Me AI

close