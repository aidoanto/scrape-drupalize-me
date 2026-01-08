---
title: "Create a View of Moderated Content"
url: "https://drupalize.me/tutorial/create-view-moderated-content?p=2501"
guide: "[[drupal-site-administration]]"
---

# Create a View of Moderated Content

## Content

The Content Moderation module exposes data about a content item's moderation state to Views. That allows us to use that information when building custom views. The data includes a moderation state field, filter, and a relationship to the moderation state entity.

In this tutorial we'll:

- Build a new view that uses the moderation state field and lists all revisions for a content item
- Display that view as a block which can be shown on any content page

By the end of this tutorial you'll know how to use the moderation state field in a view.

## Goal

Create a new View with a block display that lists all the revisions of the node currently being displayed.

## Prerequisites

- [Create a Custom Workflow](https://drupalize.me/tutorial/create-custom-workflow)
- [Moderated Content and Views](https://drupalize.me/tutorial/moderated-content-and-views)
- [Overview: Filter Criteria in Views](https://drupalize.me/tutorial/overview-filter-criteria-views)
- [Overview: Sort Criteria in Views](https://drupalize.me/tutorial/overview-sort-criteria-views)

## Video walk-through

Sprout Video

## Create a block that lists revisions of a node

We'll use a contextual filter to limit the content that is displayed to only records associated with a specific Node ID. We'll provide a default value for that filter from the URL. This way when the block is displayed while the user is viewing a content page, the ID of that content item will be pulled out of the URL and provided to the view so that we only display revisions for that content item.

### Create a new View

In the Manage administration menu navigate to *Structure* > *Views* (*admin/structure/views*). Then click the button labeled *Add view*.

Fill in the form on the resulting page with the following values. Leave all other fields as their default value.

| Field | Value |
| --- | --- |
| View name | Revisions Block |
| Show | Content revisions |
| Create a block | checked |
| Display format | Table |

Image

![Views add form filled in with values indicated above.](/sites/default/files/styles/max_800w/public/tutorials/images/views-add.png?itok=p1P3z7FJ)

Then click the button labeled *Save and edit* to continue.

### Add fields to the view

By default, the view will list a *Changed* field, and a *Title* field. Remove the *Title* field (since it would be repetitive), and add the *Link to revision* and *Moderation state* fields, as well as any others you might want to display.

### Update the filter criteria

By default, the view uses the **Published (= Yes)** filter criteria. Since we want to display all revisions for a piece of content, not only the published ones, remove this filter from the view.

### Sort by revision changed date

Sort the list of revisions in reverse chronological order by adding the *Changed* field as sort criteria. Click the button labeled *Add* for the *Sort criteria* section. Then choose *Changed* from the list of fields and click the button labeled *Add and configure sort criteria*.

Image

![Form for choosing the sort criteria with Changed selected.](/sites/default/files/styles/max_800w/public/tutorials/images/view-sort-changed.png?itok=FNjB4u5D)

On the resulting configuration form change the *Order* to *Sort descending* and click the button labeled *Apply*.

### Add a contextual filter

Expand the Advanced section and select the button labeled *Add* for the *Contextual filters* section to add a new contextual filter. Then choose ID from the field options and click the button labeled *Add and configure contextual filters*.

Image

![Form for choosing the ID field with ID field selected.](/sites/default/files/styles/max_800w/public/tutorials/images/view-context-id.png?itok=bza8QUle)

In the configuration options set the value of the *When the filter is not available* field to *Provide default value*, and *Type* option to *Content ID from URL*.

In the *When the filter value is available* section choose *Specify validation criteria*, set *Validator* to *Content*, and leave the remaining options as the default values.

Image

![Form for changing contextual filter options with above values set.](/sites/default/files/styles/max_800w/public/tutorials/images/view-context-options.png?itok=9H36mYJb)

Click the button labeled *Apply* to save the contextual filter.

### Configure access permissions

Under the *Block settings* section click the link labeled *Permissions* to change any access control rules. By default, this block will display for anyone with the *View all revisions* permission.

### Save the view

Finally, click the button labeled *Save* at the bottom of the view configuration form to save your new view.

Finally, you can add the newly created Block to the node content page using whatever block layout method you want. See [Placing a Block in a Region](https://drupalize.me/tutorial/user-guide/block-place?p=3068) for example.

Example:

Image

![Node view page with lorem ipsum node and new revisions block showing in the right column listing a couple of revisions.](/sites/default/files/styles/max_800w/public/tutorials/images/views-block-example.png?itok=R10TwTWD)

## Recap

In this tutorial we created a new view that integrates with information provided by Content Moderation and Workflows. The view provides a block that displays a list of all the revisions for a page along with the moderation state for each revision.

## Further your understanding

- Update the view created above to include log messages, and a revert button, for each revision
- What are some example use cases that you can think of for when you might want to create a new view that makes use of the moderation state for a content item?

## Additional resources

- [Views filters for content moderation state added](https://www.drupal.org/node/2936380) (Drupal.org)
- [Placing a Block in a Region](https://drupalize.me/tutorial/user-guide/block-place?p=3068) (Drupal User Guide)
- [Creating Listings with Views](https://drupalize.me/series/user-guide/views-chapter) (Drupal User Guide)
- [Views: Create Lists with Drupal](https://drupalize.me/series/views-create-lists-drupal) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Moderated Content and Views](/tutorial/moderated-content-and-views?p=2501)

Clear History

Ask Drupalize.Me AI

close