---
title: "Overview: Media Management in Drupalfree"
url: "https://drupalize.me/tutorial/overview-media-management-drupal?p=2672"
guide: "[[media-and-responsive-images]]"
order: 1
---

# Overview: Media Management in Drupalfree

## Content

Drupal's media management tools, the Media and Media Library modules, provide content authors with drag-and-drop media and asset handling, full WYSIWYG editor integration, and a library of reusable media assets. There's minimal configuration required to get started, but full control via Drupal's standard Entity and Field systems for those who need it.

In this tutorial we'll:

- Provide an introduction to the media system in Drupal and its use-cases
- Explain the Drupal core features that the Media system is built on
- Link to other tutorials that will go into much more depth on these topics

By the end of this tutorial you should know what role the Media and Media Library core modules fill and know whether or not you'll want to make use of them on your project.

## Goal

Provide an introduction to the suite of media management related modules, concepts, and best practices.

## Prerequisites

- [2.3. Concept: Content Entities and Fields](https://drupalize.me/tutorial/user-guide/planning-data-types?p=3076)
- [Chapter 6. Setting Up Content Structure](https://drupalize.me/series/user-guide/content-structure-chapter)

## What is media management?

Image

![Example of the Media Library UI](../assets/images/media-library-widget-ui.png)

The brief answer is: media management makes it possible for content authors to upload and reuse media assets via a common interface.

The Drupal core *Media* and *Media Library* modules provide a drop-in replacement for the Drupal core Image/File field types with a unified interface for editors to upload, manage, and reuse files and other multimedia assets.

Did we mention reusable? For years, one of the more painful aspects of managing content in Drupal has been figuring out how to re-use the image you uploaded to an article last week, but no longer have a copy of on your computer. Over the years there have been numerous approaches to solving this using contributed modules. All of those have helped inform the creation of the new Media and Media Library modules in Drupal core.

In Drupal we define "media" as any resource, probably with a visual element, and its associated metadata. Images are probably the most common type of media on the web. They consist of a file (such as JPG, GIF, or PNG format), which is the part you see. They also hold information like alt text, photographer, and metadata (such as capture date and tags for organizing).

All Media entities have a single canonical source, but your application might display them in different permutations depending on context. Using the example of an image again, a single JPG file could be displayed as a thumbnail on the home page, a large responsive version as the hero image for an article, or in a slideshow with a caption and the photographer displayed.

You can apply this pattern to all kinds of things, not just images. Videos could be an uploaded .mp4 file plus an encoding workflow, the URL of a remote video on YouTube, or on your own internal video platform. Tweets, posts on Instagram, or products on Amazon -- anything you might embed into your site's pages and want to ensure a consistent styling for could be Media entities.

## Built with Drupal core's fundamental building blocks

Much like a traditional [digital asset management system (DAM)](https://en.wikipedia.org/wiki/Digital_asset_management), the Media system in Drupal encompasses creation, indexing, workflow management, version control, and access control -- things that Drupal core provides building blocks for already.

The Drupal media ecosystem is built on the core [Entity](https://drupalize.me/topic/entities) and [Field](https://drupalize.me/topic/fields) APIs which means it works with existing tools like Views and Layout Builder. It shares a similar administrative UI, and mental model, with the creation of content and content types.

For site administrators, this means you can tailor the tools to meet your specific use-case. Perhaps your organization has specific requirements around the collection of author credits for media. You can use fields to collect this data. Or maybe as your library grows you need to give authors new ways to filter and search for assets. Because under-the-hood the system uses Views, you can customize it as needed.

## Media module overview

The core Media module provides unified management of the creation, configuration, and display of media entities. Media entities are content entities, and can be administered like most other Drupal content entities. The thinking is that if Drupal core provides a single authoritative way to describe media it becomes easier for contributed solutions to make assumptions about that media.

Media entities get divided up into Media types, generically referred to as bundles. In the context of Media entities, we call them Media types. You can add custom fields to Media types, and their display can be controlled from the standard [view modes and field formatters tools](https://drupalize.me/tutorial/user-guide/structure-view-modes?p=3071). That's similar to the concept of content types as it applies to Nodes, where Basic Page, Article, and Blog post are all examples of different content types.

The Media module introduces the concept of Media sources, and provides some common ones in core, including filesytem files, images, and remote videos via oEmbed. This can be expanded to include almost any media source via a plugin architecture.

Learn more in [Overview: Media Types, Fields, and Entities](https://drupalize.me/tutorial/overview-media-types-media-entities-and-media-fields-drupal)

## Media Library module overview

The core Media Library module provides an improved interface for content authors to use when selecting existing media entities and creating new ones. Its primary feature is a field widget that is a drop-in replacement for the Media module's entity reference UI.

The goal is to provide a UI that works for most use-cases with minimal configuration required. In some cases, you may find that the module's limited configuration prevents you from achieving your requirements. In that case, the contributed [Entity Browser module](https://www.drupal.org/project/entity_browser) is a good alternative that also works with core Media entities (though it's far more complicated to set up).

The main listing is powered by Views, and can be customized as needed. For example; A common customization is to add a tags field to media entities to help with organization, and to then expose that tags field as a filter in the Media Library.

## Contributed modules in the media ecosystem

With a baseline for collecting, listing, and displaying media assets in core, the contributed module ecosystem can focus on providing enhanced tools and integration with additional media sources.

[Here's a pretty good list of contributed Media sources](https://www.drupal.org/node/2860796). That should give you an idea of the types of things that can be integrated into your media management system.

Modules like [Entity Browser](https://www.drupal.org/project/entity_browser) and [Inline entity form](https://www.drupal.org/project/inline_entity_form) can be used to replace the core Media Library for more advanced use-cases or when advanced customization is needed.

## An evolving ecosystem

The Drupal media management ecosystem is evolving. Prior to the addition of Media in core, much of the work on this system happened in the the contributed [Media Entity module](https://www.drupal.org/project/media_entity). Because of slight variations in their approach when working with Media-related contributed modules, it's important to verify your versions and their compatibility with Drupal core Media entities.

In our experience most Media ecosystem modules make clear on the project page which version(s) of the module with work with core Media entities vs. which work with the deprecated Media Entity module.

For a long time now, most sites have used the core Image and File fields to handle the upload and display of media assets like images or a library of PDF files. The goal is for the use of those fields in conjunction with content (nodes) to be replaced with Media fields.

Going forward, we recommend that you use Media fields in the place of Image and File fields in most cases when dealing with content. Read more about [Media Types, Fields, and Entities](https://drupalize.me/tutorial/overview-media-types-media-entities-and-media-fields-drupal) to help get a better understanding of what the differences are. If you're still unsure what approach to take, let us know.

## Recap

Media management refers to the user interface provided for content authors to create, use, and reuse media assets. It also includes the tools available to site administrators, module developers, and themers to customize how the interface works or how assets are displayed to end users. The objective is for Drupal core to provide a baseline for collecting and displaying media assets, and a UI for using them that requires minimal configuration, while still allowing for advanced application-specific customization when needed.

## Further your understanding

- What content in your application should logically be part of a media asset library? What requirements do you have around the collection and display of media that might require application-specific customizations?
- Learn more about [the Media in core initiative](https://www.drupal.org/about/strategic-initiatives/media), and [the community's current roadmap](https://www.drupal.org/project/ideas/issues/2825215)

## Additional resources

- [Media module](https://www.drupal.org/docs/8/core/modules/media) (Drupal.org)
- [Media Library module](https://www.drupal.org/docs/core-modules-and-themes/core-modules/media-library-module) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Overview: Media Types, Media Entities, and Media Fields in Drupal](/tutorial/overview-media-types-media-entities-and-media-fields-drupal?p=2672)

Clear History

Ask Drupalize.Me AI

close