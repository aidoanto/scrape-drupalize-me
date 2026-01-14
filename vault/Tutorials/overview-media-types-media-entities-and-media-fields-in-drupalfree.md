---
title: "Overview: Media Types, Media Entities, and Media Fields in Drupalfree"
url: "https://drupalize.me/tutorial/overview-media-types-media-entities-and-media-fields-drupal?p=2672"
guide: "[[media-and-responsive-images]]"
---

# Overview: Media Types, Media Entities, and Media Fields in Drupalfree

## Content

Media entities are standard Drupal fieldable content entities. For the most part, they function, and are managed, in the same way as Nodes. So if you've previously created content in Drupal, much of working with Media entities should be familiar -- with some notable exceptions related to the connections between Media types and the media resources they represent.

In this tutorial we'll:

- Get an overview of Media entities, Media types, and Media fields in Drupal
- Point to other tutorials that go into more depth on individual topics
- Learn some basic terminology and concepts related to the Media system in Drupal

By the end of this tutorial you'll have an overview of the pieces that make up the Media system in Drupal core.

## Goal

Explain how Media Types and Media Fields fit into the broader Entity/Fields-based information architecture of Drupal.

## Prerequisites

Media entities are standard Drupal fieldable content entities with a couple of notable additions that we'll explain. Media entities can be referenced anywhere that Drupal knows how to work with content entities. They can take advantage of the full suite of tools that Drupal provides for managing content entities like Views, Workflows, Content Moderation, JSON:API, access control, and more.

To take full advantage of the Media system it helps to have a solid understanding of the following concepts:

### For everyone

If you're not familiar with *content entities* and *fields* as Drupal concepts, start with [2.3. Concept: Content Entities and Fields](https://drupalize.me/tutorial/user-guide/planning-data-types?p=3076).

[Chapter 6. Setting Up Content Structure](https://drupalize.me/series/user-guide/content-structure-chapter) covers the basics of administering and configuring content entities. While it focuses on Nodes, the same concepts apply to Media entities.

### For developers

To better understand how the Media system works from a code perspective you'll want to be familiar with the following:

- [Entity API Overview](https://drupalize.me/tutorial/entity-api-overview)
- [Field API Overview](https://drupalize.me/tutorial/field-api-overview)
- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins)

## Media entities

An entity is an item of content data, which can consist of text, HTML markup, images, and any other data. At least a subset of this data is intended to be consumed by site visitors. "Media entities" specifically refers to data which represents media resources. Examples include images, documents, audio files, remote videos, and even things like an Instagram or Twitter URL which doesn't necessarily fit into the traditional definition of media.

For example, think of an image file (a resource), plus some associated tags for organizing purposes, and a photo credit naming the photographer and date. Include metadata like width/height of the image, who created the record in Drupal, and whether the record is published or not.

Next, consider an Instagram URL (a resource) that represents an image, comments, likes, and metadata, as well as resource-specific logic for creating an HTML representation of the thing to display.

Every individual media resource, whether it's an image, a remote video on YouTube, or a PDF file, is a Media entity.

Providing an abstraction like this around different types of media resources allows code in Drupal to be able to do things like find, load, and display a resource without having to know the specific details of that resource. That makes the system flexible while still being predictable.

[Learn to administer Media entities](https://drupalize.me/tutorial/find-add-edit-and-delete-media-entities-drupal).

### A note about media entity publication status

Every media entity, like any Drupal content entity, has a Published/Unpublished status. Anyone with either the permission to edit the specific entity, or who has the generic *Administer media* permission, can view unpublished media entities.

Items that are unpublished will **not** be available to select in the Media Library when selecting items to attach via a media field. However, if you unpublish a media entity that was previously attached to another content entity it'll remain attached, and anyone with permission to view the unpublished media entity will still see it.

<drupal-media data-entity-type="media" data-entity-uuid="7562c8fc-0a70-455e-a2a8-8804a9138258" alt="Media field with unpublished image attached showing "unpublished" marker on the image">

### Media entity revisions

Media entities are revisionable, like content entities. Whether or not new revisions are created depends on the specific Media types configuration.

Learn more about revisions in [What Are Revisions?](https://drupalize.me/tutorial/what-are-revisions)

### Paths, aliases, and urls

Like most other content entities in Drupal, Media entities have a URL associated with them. By default this is `/media/{ID}`, but just like when you create a node, you can edit the URL alias for a Media entity.

However, unlike nodes, the canonical URL for a Media entity, `/media/{ID}`, will result in a "404 page not found" error, rather than a page that displays the Media entity in question. In most cases, this is the desired behavior. Media entities are most likely being attached to a page that someone would navigate to, like an Article, and displayed there. But you don't want someone to just navigate to a Media entity out of context.

This display can be configured via the Media module's settings. If you have a use-case that *does* involve allowing people to view a Media entity at the `/media/{ID}` or other configured URL you can enable that feature.

## Media types

Media entities, just like any other content entity in Drupal, can be broken up into subtypes, commonly referred to as bundles. In the context of Media entities we call them Media types. You might be familiar with the concept of content types as it applies to Nodes. Basic Page, Article, and Blog post are all examples of different content types.

Media types are groupings of Media entities that all share the same fields. When you install the Media module (assuming you're using the Standard profile) the following types are automatically created:

- Document
- Image
- Audio file (local)
- Video file (local)
- Remote video

Media types have an important distinction compared to Nodes: not all Media types are equal, and every Media type inherits from a specific **Media source plugin**. The source plugin provides domain-specific knowledge about the kind of resource being represented. For example, Media types dealing with images know how to validate file extensions and render `<img>` tags. Media types dealing with remotely hosted videos might know how to retrieve thumbnails from a remote API, and display an HTML video player and transcript.

All Media types are also required to have a **source field**. This gets created by default, and can not be modified. This field stores a value that uniquely identifies the resource to display. For an *Image* media type this is likely a pointer to the image file. For a YouTube-hosted remote video this would be the canonical URL of the video which can be used to identify the video when making requests to the YouTube API.

[Learn to administer add fields to Media types](https://drupalize.me/tutorial/how-add-fields-media-type-drupal).

### Media type view modes

Media entities are rendered using view modes. A Media type can define different configurations of fields and field formatters for different view modes, and this will impact what the final output looks like. Most places that list Media entities (Media reference fields, Views, etc.) will let you choose which of the available view modes you want to use for displaying media in that specific context.

## Media fields

In most cases you'll want to associate Media entities with Content entities for end user consumption. For example: adding a cover image to a blog post, a video resource to a tutorial, or a list of PDFs to the bottom of a knowledge base page. This is accomplished using entity references. The Media module provides a specific Media reference field that provides a couple of features on top of the standard entity reference field.

The Media entity field widget (the bit someone fills out when creating a blog post) provides a link to the Media administration page so you can browse the list of available Media entities, and a link to the form to add new Media entities.

Media reference fields can also (optionally) reference different Media types from the same field. However, File or Image reference fields are limited to one specific resource type.

If you enable the Media Library module, the Media reference field will automatically be replaced with the much more useful Media Library UI.

[Learn to use Media fields to attach Media entities to content](https://drupalize.me/tutorial/add-media-field-content-type-drupal).

## Should I use an Image field or a Media field?

Image fields have been the go-to mechanism for including images in content for years, and a common question now that Media is stabilized and part of Drupal core is, "Should I use an Image field or a Media field?"

We think that when your goal is to add an Image (or any other media) to content you should use a Media field, if for no other reason than it makes it easier to re-use images without uploading a duplicate.

Drupal core will recommend you use a Media field whenever you go to add an Image or File field to a content type:

Image

![Example of help message displayed, content reads: Use Media reference fields for most files, images, audio, videos, and remote media. Use File or Image reference fields when creating your own media types, or for legacy files and images created before enabling the Media module.](../assets/images/image-field-warning.png)

A good example of an exception to this rule is user profile images. These are images that are NOT reusable (two users are not going to share the same profile image).

## Recap

In this tutorial we learned that Media entities are standard Drupal content entities with a few notable exceptions. They are grouped into bundles, commonly referred to as Media types. They can be associated with, and displayed as part of, other content entities using a Media reference field.

## Further your understanding

- What are the main differences between standard content entities and Media entities?
- Can you give some examples of when it would be useful to add custom fields to a Media type?
- Thinking about your project, where might you use Media reference fields?

## Additional resources

- [Media module overview](https://www.drupal.org/docs/8/core/modules/media/overview) (Drupal.org)
- [Creating and configuring Media Types](https://www.drupal.org/docs/8/core/modules/media/creating-and-configuring-media-types) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview: Media Management in Drupal](/tutorial/overview-media-management-drupal?p=2672)

Next
[Add a Media Field to a Content Type in Drupal](/tutorial/add-media-field-content-type-drupal?p=2672)

Clear History

Ask Drupalize.Me AI

close