---
title: "Introduction to Layout Builderfree"
url: "https://drupalize.me/tutorial/introduction-layout-builder?p=2653"
guide: "[[layout-builder]]"
---

# Introduction to Layout Builderfree

## Content

The Layout Builder module for Drupal provides a layout user interface (UI), a set of flexible visual design tools that allows content creators and site administrators to customize the layout of a page via a powerful drag-and-drop UI. You can use Layout Builder to customize the layout of a single page, create a custom layout for all content of a certain type, or build landing pages.

At a high level it allows users to generate a layout -- two columns with a header, for example -- and then place a content type's fields and any blocks into that layout.

Layout Builder provides an API, and layout discovery feature, that themes and other modules can use to provide new templates. It allows more consistent tooling across the entire page-building ecosystem.

In this tutorial we'll:

- Give an overview of what Drupal Layout Builder is, and its common uses
- Introduce terminology and concepts related to Layout Builder

By the end of this tutorial you'll have a better understanding of what the Drupal core Layout Builder module does and how it might help with your specific use-case.

## Goal

Introduce the core Layout Builder module and related ecosystem.

## Prerequisites

- [Chapter 5. Basic Page Management](https://drupalize.me/series/user-guide/content-chapter)
- [Chapter 6. Setting Up Content Structure](https://drupalize.me/series/user-guide/content-structure-chapter)

## What is Layout Builder?

Image

![Screenshot of Layout Builder graphic UI](../assets/images/section.png)

One of the most commonly requested features over the years has been for Drupal to provide some kind of easy-to-use page builder with a WYSIWYG sort of experience. These tools are present in other platforms, and can allow for far more flexibility without the need to write code. Such a tool can empower a whole new category of Drupal users to customize the look and feel of their Drupal applications.

To address this demand, contributed modules such as Panels and Display Suite filled the gap. But solutions using these modules were often incompatible with one another. Layout Builder (in Drupal core), provides a consistent API for modules to register a layout, and define what layouts are and can do. Moving this responsibility to core helps to unify the contributed module ecosystem rather than having lots of different silos.

Layout Builder in Drupal core consists of two modules:

- **Layout Discovery**: An API module that defines what a layout is and handles layout registration and rendering. It also includes utilities such as automatically generating icons for the UI and more.
- **Layout Builder**: A drag-and-drop UI for creating flexible layouts for content types built on top of the Layout Discovery API. The Layout Builder UI allows site administrators to configure a layout to use when displaying a content type, and then arrange the content types fields within the layout. Layout Builder can also place any block into a layout, which opens up all kinds of possibilities.

## Layout Builder capabilities

Layout Builder module works with the fields of a specific content type, blocks, and block types.

In the simplest setup, a site builder creates a layout for a content type and applies the layout to all nodes of that content type. If they make changes to the layout, the changes apply to all existing and newly-created nodes of that type. Configuration options allow the site builder to specify a default layout for a content type, while allowing per-node customization of that layout.

Layout Builder defines two main concepts used when creating a layout:

- **Section**: Sections are the containers into which we place *blocks*. A example of such a container is a column in a 2-column layout. Each layout can have as many sections as required, but must have at least one. Sections create the skeleton of the layout. Once we define the sections, we cannot move them around.
- **Block**: A block is a content element that we can place into a layout. We place blocks in *sections*. Blocks represent the content that will appear there.

It's important to understand that a *block* inside Layout Builder is not the same thing as a standard Drupal block entity. It has a more abstract definition and acts more like a placeholder indicating that *something goes here*.

One example is a *block* that creates a wrapper for the fields of a content type. When we associate a layout with a content type, these blocks can placed into the sections for that "layout + content type" combination. Since they're specific to the content type these blocks wouldn't be available for the same layout on a different content type.

Image

![Screenshot of Layout Builder body field options](../assets/images/field_settings.png)

Depending on the field type, the *block* exposes the appropriate field formatter configuration. It's much like the *Manage display* settings for a content type not using the Layout Builder.

The second type of *block* available within the Layout Builder are block entities. All custom blocks configured for your site, and all module-provided blocks, are available to use within the Layout Builder.

This opens up a variety of options. For example, the *ctools* module exposes views and view modes for the content type. The *facets* module allows you to place facets blocks inside the layout builder, and the *system* module allows you to place the "Powered by Drupal" block, breadcrumbs, content and messages. You can also author your own custom block plugins to provide any content you need. Any custom block plugins you create will be available in Layout Builder.

Layout Builder creates flat layouts. That is, it doesn't allow for the nesting of sections, or blocks.

The Layout Builder UI allows editors to preview their layouts using real content. You can toggle between a generic layout screen and one with preview content entered.

## Extending Layout Builder

The Layout Builder module is still in active development. The Drupal community is working on features and enhancements to its functionality. If you find yourself in a situation where the module doesn't do certain things that might be useful, chances are high that other people in the Drupal community also thought the same thing. There may already be a contributed module that extends the current Layout Builder functionality and solves the problem you're facing.

Find the complete list of [modules that work with Layout Builder on Drupal.org](https://www.drupal.org/docs/8/core/modules/layout-builder/additional-modules).

The most popular contributed modules that are actively maintained and promoted by the community are solving problems of enhancing the editorial experience by simplifying and decluttering the UI. They allow things like hiding blocks that should not be available for placement within the layouts, and making certain layouts accessible to specific content types.

Some modules provide different options for the layout and appearance of the right control panel of the Layout Builder UI. All these options improve usability of the Layout Builder interface and editorial workflow.

## An evolving toolset

Layout Discovery module, layout API and Layout Builder are products of [the Drupal layout initiative](https://www.drupal.org/about/strategic-initiatives/layout). The initiative's goal is, "to provide site builders and content authors with intuitive tools to build pages, change layouts, and add and rearrange blocks with live preview." It's one of the main strategic initiatives active in the Drupal community.

The current challenge is working with multilingual websites; translation of specific layouts is not yet supported.

You can get an overview of the current state of things by [browsing the issue queue](https://www.drupal.org/project/issues/search/drupal?component%5B%5D=layout_builder.module) for related issues. Often, you will find existing solutions to issues you encounter.

We think the existing tools are production-ready, but you might find some rough edges as you go.

## Recap

The Layout Builder ecosystem is the newest addition of layout construction tools available in Drupal core. It consists of 2 primary modules in Drupal core: *Layout Discovery*, which allows modules and themes to declare their custom layouts, and *Layout Builder*, which provides a visual design tool that allows the construction of layouts without writing custom code. In addition, there are a growing number of contributed modules that seek to improve the UX of the existing core modules.

Layout Builder is stable, but is still a work in progress. The Drupal community has resolved some of the immediate problems through contributed projects, while patches available in specific issues mitigate other problems.

## Further your understanding

- How could you make use of Layout Builder in your projects?
- Enable Layout Builder module in core. Go to Basic Page content type. In the "manage display" tab, enable use of Layout Builder. Select *Manage Layout* and try to create your first layout with Layout Builder.

## Additional resources

- [Layout Builder documentation](https://www.drupal.org/docs/8/core/modules/layout-builder) (Drupal.org)
- [Layout API](https://www.drupal.org/docs/drupal-apis/layout-api) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Create a Flexible Layout for a Content Type](/tutorial/create-flexible-layout-content-type?p=2653)

Clear History

Ask Drupalize.Me AI

close