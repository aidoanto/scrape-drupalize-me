---
title: "Moderated Content and Views"
url: "https://drupalize.me/tutorial/moderated-content-and-views?p=2501"
guide: "[[drupal-site-administration]]"
---

# Moderated Content and Views

## Content

When building views of moderated content there are some important things to be aware of. One is the difference between choosing Content or Content revisions as the base for your view. You should also know about some fields and filters added by the Content Moderation module.

In this tutorial we'll:

- Understand when, and why, to choose Content revisions as the base for your view instead of Content
- Learn about the fields, and filters, added by the Content Moderation module
- Learn how to update the view at *admin/content/moderate* that comes with the Content Moderation module to make it work with any workflow.

By the end of this tutorial you should understand the important concepts necessary to create views of moderated content.

## Goal

List the additional options the Content Moderation module provides for Views and understand some important considerations for using Views with moderated content.

## Prerequisites

- [Overview of Workflows and Content Moderation](https://drupalize.me/tutorial/overview-workflows-and-content-moderation)

## Content vs Content revisions

When you first start a new view in the *View settings* you choose the type of items you want the view to show. When working with moderated content in Views it's important to keep in mind the difference between creating a view of "Content", and a view of "Content revisions".

Image

![Form for creating a new view with select list showing different base tables opened to demonstrate that both content and content revisions are in the list.](/sites/default/files/styles/max_800w/public/tutorials/images/views-show-content-type.png?itok=hXi33E22)

- **Content:** Always shows the latest default revision of an entity. When creating views for website visitors you'll likely use this to ensure you're showing them only the content they are intended to see. Think of this as building a view using whatever version of the content would be displayed on the page.
- **Content revisions:** This contains all revisions of a piece of content, including the current default revision. Use this if you're creating views where you want someone to be able to see versions of a piece of content: past, present, and future.

## The moderation state field

Content items that are being moderated by a Content Moderation workflow will have an additional *Moderation state* field accessible in Views. This can be used to display the state that a revision had assigned to it when it was saved.

## Filter by moderation state

Content items that are being moderated by a Content Moderation workflow can be filtered based on their *Moderation state*. This also works well as an exposed filter: it provides a select list so a user can choose one or more moderation states they would like to filter by.

Additionally, the filter, *Is latest revision*, while not provided by Content Moderation, can be useful when dealing with moderated content.

## Sorting

There are no Content Moderation specific sorting options. Usually when working with revisions you'll probably want to order things based on their created/changed date in order to indicate the order in which the revisions exist.

## Modify the provided Content Moderation view

When you install the Content Moderation module it also installs a new view. To see this view, in the Manage administration menu navigate to *Content* > *Moderated content* (*admin/content/moderated*). This view is a variation of the default *admin/content* view with an exposed filter provided to allow you to filter based on the moderation state of a piece of content.

A note about using this view: it's been configured to work with the default Editorial workflow, and the states that that workflow contains. If you're using a different workflow configuration, or if you've added or removed states, you'll need to edit this view and update the 2 *Content revision: Moderation state* filter criteria. The *Content revision: Moderation state* exposed filter uses the *Is one of* operator, and you need to tell it which of the available state options it can use. You can choose "Select all" or hold down the shift key and select multiple states. If you added or changed Moderation states, the other *Content revision: Moderation state* filter may say "Unknown" next to it and return a validation error in the Preview area. Either remove this filter, or select the value "Published" for "Is not on of" to return a list of only moderated, unpublished content.

## Recap

In this tutorial we took a quick look at the new options provided to views by the Content Moderation module, reviewed the difference between views of Content and Content revisions, and learned about how to modify the default content moderation view to make it work with any workflow.

## Further your understanding

- Can you update the view at *admin/content/moderated* to work with your custom workflow?
- What's the difference between a view of Content and Content revisions, and when should you choose to use each?

## Additional resources

- [Views filters for content moderation state added](https://www.drupal.org/node/2936380) (Drupal.org)
- [Overview: Filter Criteria in Views](https://drupalize.me/tutorial/overview-filter-criteria-views)
- [Overview: Exposed Filter Criteria in Views](https://drupalize.me/tutorial/overview-exposed-filter-criteria-views)
- [Overview: Sort Criteria in Views](https://drupalize.me/tutorial/overview-sort-criteria-views)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Manage Moderated Content](/tutorial/manage-moderated-content?p=2501)

Next
[Create a View of Moderated Content](/tutorial/create-view-moderated-content?p=2501)

Clear History

Ask Drupalize.Me AI

close