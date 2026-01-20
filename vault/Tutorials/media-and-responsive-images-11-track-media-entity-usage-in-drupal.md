---
title: "Track Media Entity Usage in Drupal"
url: "https://drupalize.me/tutorial/track-media-entity-usage-drupal?p=2672"
guide: "[[media-and-responsive-images]]"
order: 11
---

# Track Media Entity Usage in Drupal

## Content

One of the most powerful features of Drupal's Media Library is that it enables content authors to re-use media entities. Have a favorite image that you like to use with all blog posts about a specific topic? Or a default icon you want to use for a tutorial unless an alternative is provided? The Media Library can accommodate this without requiring you to keep a copy of the image locally and then attach it to every node where it's needed.

This can lead to a potential issue when an editor deletes an image, thinking they've also deleted all the content that used it. If they missed a post referencing the now deleted image, what happens when there is no image to show?

The contributed [Entity Usage module](https://www.drupal.org/project/entity_usage) provides a mechanism for tracking relationships between entities. This is essential functionality when working with a library of reusable media entities because it helps ensure that media entities attached to content are not deleted.

In this tutorial we'll:

- Discuss the use case for the Entity Usage module
- Learn how to configure Entity Usage to keep track of relationships between media entities and nodes that reference them
- Prevent media items from being deleted if they are in use somewhere on the site

By the end of this tutorial you should be able to explain what the Entity Usage module does, and how to use it to solve common problems related to deleting items from a large Media library.

## Goal

Install and configure the contributed Entity Usage module to keep track of relationships between media entities and the content entities that use them.

## Prerequisites

- [Overview: Media Types, Media Entities, and Media Fields in Drupal](https://drupalize.me/tutorial/overview-media-types-media-entities-and-media-fields-drupal)

## Watch: Track Media Entity Usage in Drupal

Sprout Video

## How media entity tracking works

The module works by keeping track of the relationships between a source entity and a target entity. Consider the following example: a site with an *Article* content type and an *Image* media type. The *Article* content type uses a *Media* field to allow content authors to select one or more *Media* images to display with an article. In this scenario the *Article* is the source, the image is the target, and the Media (entity reference) field is what creates the relationship.

Image

![Diagram illustrating relationship between source and target entities via entity reference fields](../assets/images/media-source-target.png)

Whenever a source entity gets created, updated, or deleted, the Entity Usage module inspects the relationship for any target entities and when it finds one creates a *usage* record.

An Article could target an image in different ways: Entity reference fields, embedded in a text field via CKEditor, as the target of a link field, and more.

The Entity Usage module supports plugins that scan for different types of relationships. From the module's README these tracking methods are supported:

- Entities related through *entity\_reference* fields
- Entities related through link fields
- Standard HTML links inside text fields.
- Media entities embedded into WYSIWYG text fields using core's Media Library
- Entities embedded into text fields using the Entity Embed module
- Entities embedded into text fields using the LinkIt module
- Entities related through *block\_field* fields
- Entities related through *entity\_reference\_revisions* fields (i.e. paragraphs)
- Entities related through *dynamic\_entity\_reference* fields
- Entities related through Layout Builder. Supported methods: a) Core's inline (non-reusable) content blocks, and b) entities selected through the contributed Entity Browser Block module

You can also [write an `@EntityUsageTrack` plugin](https://drupalize.me/tutorial/implement-plugin-any-type) with your own custom logic as needed.

## Install and configure Entity Usage

### Install Entity Usage module

Use Composer, or your method of choice, to download the Entity Usage module.

```
composer require 'drupal/entity_usage:^2.0@beta'
```

(Tip: Go to the Entity Usage project page, scroll down to **Downloads** and click on the latest release to get a copy-pasteable Composer command of that release.)

Learn more about installing modules in [Downloading and Installing a Module from Drupal.org](https://drupalize.me/tutorial/user-guide/extend-module-install)

And then [install the module](https://drupalize.me/tutorial/user-guide/config-install).

### Configure usage tracking

In the *Manage* administration menu, navigate to *Configuration* > *Entity Usage Settings* (*admin/config/entity-usage/settings*). This page contains all the settings for the module; we'll discuss what each one does.

#### Enabled local tasks

Lists all the content entity types on your site. Choose which ones you would like to have a *Usage* tab added to the list of Local actions alongside the normal *View* and *Edit* tabs. The tab will contain a report showing each usage of the entity. Typically you'll want to do this for all your target entity types.

In this case, select the *Media* entity type from the list and leave the others off.

Example:

<drupal-media data-entity-type="media" data-entity-uuid="7bb90938-647c-4189-bfa3-0a74bfa7ceb1" alt="Example of the entity usage tab and its content. Shows the image being used by one Content entity named "Test Article"">

#### Enabled source entity types

Choose which entity types to use as a possible source for a relationship. These are the entities that will be scanned to see if they contain a relationship to any of the target entity types. The question to ask yourself is, "If an image is used when creating one of these, should that count as a trackable usage of the image?"

In this case, select *Content*, since we want to keep track of whenever an image is used as part of a node.

#### Enabled target entity types

Choose which entity types to use as a possible target for a relationship. These are the entities whose usage you want to track. The question to ask yourself is, "If one of these is used, do I want to keep track of that?"

In this case, select *Media*, since we want to keep track of whenever an image (a Media entity) is used as part of a node.

#### Enabled tracking plugins

This dictates which tracking plugins you want triggered whenever a source entity that's enabled above gets created, updated, or deleted. The question to ask here is, "Where should the module look at source entities to try and find target entities?"

Only enable the ones that are relevant for your use-case. There's no reason to scan "Entity Embed" tokens if you're not using the Entity Embed module.

In our case we'll enable *Media WYSIWYG Embed (Core)* and *Entity Reference* since Media fields are entity reference fields. This will find any time we add an image to a node via either a media field or by embedding it into any WYSIWYG enabled textarea.

#### Warning message on edit/delete form

In the next 2 sections you can configure whether or not you want to display a message on the target entities' edit or delete forms letting a user know that they are about to modify an entity that's referenced elsewhere. You'll only be able to turn this feature on for entity types that are enabled in the target entity types configuration above.

Example warning message:

<drupal-media data-entity-type="media" data-entity-uuid="604ebef6-ae3b-484a-9f74-f72af1549379" alt="Form for editing a Media entity of type Image with a warning message that says "Modifications on this form will affect all existing usages of this entity."">

This is probably why you're using this module, and you'll want to enable one or both of these warnings.

#### Generic

Finally, there are some global configuration options, including allowing for tracking of references created by base fields. That is, fields defined in code for the entity type rather than configuration.

If you're using the *HTML links* tracking plugin it parses all text fields and looks for links to internal entities. By default it will only scan relative URLs. If you would like to also scan for absolute URLs you can add a list of valid domains.

Once you've made your changes, press the *Save configuration* button at the bottom of the form to save them.

Your site will now start tracking entity usage based on your configuration.

## Update usage statistics

Sometimes you need to bulk update usage statics across the whole site. This is usually after you change the module's configuration or when you first enable the module and want to backfill usage data for all existing content. You can do this 2 ways.

Via the administrative UI: In the *Manage* administration menu, navigate to *Configuration* > *Entity Usage Settings* and then select the *Batch Update* tab (*admin/config/entity-usage/batch-update*). Then press the *Recreate all entity usage statistics* button.

Or via Drush: The module provides a Drush command for updating usage statistics. This will be more efficient and reliable for sites with large amounts of content that needs scanning.

```
drush entity-usage-recreate
```

Both of these approaches will scan **all** of the configured source entity types on your site using **all** of the configured plugins. This could take a while.

## A warning about performance

This module can have performance implications when creating or updating content items when used in scenarios where saving one entity can trigger updating (and thus scanning of) a whole chain of nested entities. For example, if you're using the Paragraphs module.

The usage report page can also be slow if an entity has a large number of tracked uses.

Neither of these should have any impact on users viewing content on your site. But it could make the content editing experience feel unresponsive.

## Recap

The contributed Entity Usage module allows you to keep track of any time 1 entity on your site references another, whether that's through an entity reference field, embedding an image in the WYSIWYG, or via a direct link. Using the module, we were able to configure our site to keep track of each time an image (Media entity) is used when authoring a piece of content. Then we displayed a warning message to content editors about where an image is used when they try to update or delete that image. This provides an important UX improvement for sites that have large libraries of Media assets that are re-used throughout the content.

## Further your understanding

- What different ways does your site allow 1 entity to reference another?
- What are some other use cases for keeping track of entity usage other then ensuring authors don't delete an image that's in use elsewhere?
- What should you be aware of regarding the performance of this module, and how does that impact your specific site?

## Additional resources

- [Entity Usage documentation](https://www.drupal.org/docs/contributed-modules/entity-usage) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Customize the Drupal Media Library Browser Widget](/tutorial/customize-drupal-media-library-browser-widget?p=2672)

Next
[Use View Modes with Media Entities in Drupal](/tutorial/use-view-modes-media-entities-drupal?p=2672)

Clear History

Ask Drupalize.Me AI

close