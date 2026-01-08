---
title: "Overview: Access Control for Media Entities in Drupal"
url: "https://drupalize.me/tutorial/overview-access-control-media-entities-drupal?p=2672"
guide: "[[media-and-responsive-images]]"
---

# Overview: Access Control for Media Entities in Drupal

## Content

Access control for the Media entities in Drupal works in much the same way as any other content entity. The module provides fine-grained control over create, update, and delete operations, while providing only basic control over who can view Media assets. The thinking is that there are too many possible permutations of how an application may want to restrict read access to content. Therefore, rather than try and pick one setting and add it to core, it's left entirely up to the site administrator and contributed modules.

In this tutorial we'll:

- Look at the different permissions provided by the Media module for controlling access to Media entity operations
- Discuss some common misconceptions about file permissions that can lead to potentially exposing private data

By the end of this tutorial you should know how to configure access control for Media entities, and explain how access control relates to files attached to a Media entity attached to a Node.

## Goal

Get a brief overview of how access control works for Media entities in Drupal and explain some common misconceptions that can lead to insecure configurations.

## Prerequisites

- [Overview: Media Types, Media Entities, and Media Fields in Drupal](https://drupalize.me/tutorial/overview-media-types-media-entities-and-media-fields-drupal)

## Permissions related to viewing media

There is a single generic *view* permission that applies to all Media entities. This can be extended by contributed modules to be more granular. For example, modules like [Permissions by Term](https://www.drupal.org/project/permissions_by_term) or [Group](https://www.drupal.org/project/group) can be used to restrict view access for Media entities. You can also write your own custom logic. Learn more in [Entity Access Control](https://drupalize.me/tutorial/entity-access-control).

By default the stand alone URL for Media entities (*/media/{ID}*) is disabled. Thus, users can not navigate directly to a Media entity page. This can be changed via the *Standalone media URL* setting found at *Configuration* > *Media settings* (admin/config/media/media-settings).

Some common misconceptions to be aware of:

- Media items do not inherit access control from their parents. When a Media entity is attached to a Node (e.g. a photo associated with a Blog Post), if the user has permission to view the Media entity they'll be able to do so whether they have permission to view the Node or not. This is because Media entities can be re-used and might appear on another Node.
- This also applies when dealing with Drupal's private file system. The private file access handling will grant access to the file to whoever has access to the entity where the file is attached. This means that a Media entity with a file field will keep access to the entity and the file in sync. Users may have the expectation that access is also inherited from the entity referencing the media items, which doesn't happen.

Both of these can lead to misconfigured sites where you think your assets are protected but they end up exposed publicly. Specifically, users who know the direct link to a file on disk may be able to access that file even if it's associated with an unpublished Node.

## Permissions related to managing media

Permission can be granted to create, update, delete, manage and view revisions for *all* Media entities, or on a per [Media type](https://drupalize.me/tutorial/overview-media-types-media-entities-and-media-fields-drupal) basis. This can be further restricted by allowing a user to create, update, or delete only Media entities that they are the owner of. This gives you granular control over who can manage Media assets.

The *Administer media* permission allows anyone with that permission to bypass all other Media-related access control, and should be given to trusted users only.

Learn more about managing permissions in [Chapter 7. Managing User Accounts](https://drupalize.me/series/user-guide/user-chapter).

## Recap

Access control for Media entities works in much the same way as any other content entity. There's fine-grained control over create, update, and delete operations, and basic on/off control for viewing -- while leaving it open to customization via contributed modules.

## Further your understanding

- Can you outline a method for restricting access to articles and all the associated media assets only to people with an account on your site?
- How about allowing people with an account to view articles, but requiring an additional role to view the videos associated with an article? For example, a payment gateway.

## Additional resources

- [Chapter 7. Managing User Accounts](https://drupalize.me/series/user-guide/user-chapter) (Drupalize.Me)
- [Entity Access Control](https://drupalize.me/tutorial/entity-access-control) (Drupalize.Me)
- [Inform users that media items don't inherit access control from parents](https://www.drupal.org/project/drupal/issues/2984093) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Map Media Source Data to Custom Fields](/tutorial/map-media-source-data-custom-fields?p=2672)

Next
[Customize the Drupal Media Library Browser Widget](/tutorial/customize-drupal-media-library-browser-widget?p=2672)

Clear History

Ask Drupalize.Me AI

close