---
title: "How to Add Fields to a Media Type in Drupal"
url: "https://drupalize.me/tutorial/how-add-fields-media-type-drupal?p=2672"
guide: "[[media-and-responsive-images]]"
---

# How to Add Fields to a Media Type in Drupal

## Content

Drupal media entities are fieldable entities, which means that you can add any custom fields you want to your Media types. These fields can be used for collecting additional metadata about a resource, categorizing and organizing resources so they're easier to find in a large media library, or for displaying information like a photo credit or transcript for a video. The possibilities are endless once you know how to add, and optionally display, fields in Drupal.

Some example use cases for adding fields to Media types:

- Collect, and display, a credit to go along with a photo. This could also be a date, a location, or any other metadata.
- Store resource width and height dimensions as custom fields so they can be referenced by display logic in the theme layer.
- Use Taxonomy reference fields to add tags or categories to help keep a large library organized.

In this tutorial we'll:

- Learn how to add fields to a Media type
- Verify our new custom field is working

By the end of this tutorial you'll know how to add custom fields to any Media type.

## Goal

Add a tags field to the Image media type to help keep a large image library organized.

## Prerequisites

- [Fields](https://drupalize.me/topic/fields)
- [Chapter 6: Setting Up Content Structure](https://drupalize.me/series/user-guide/content-structure-chapter)

## Watch: How to Add Fields to a Media Type in Drupal

Sprout Video

## Media entities are content entities

Media entities, like content entities, can have any number of additional fields attached to them. The process, and much of the information architecture considerations, are the same as when adding fields to content types. If you know how to add fields to a content type, you know how to add them to a Media type.

There's one major difference, which is that Media types can perform **field mapping**. A Media type's source plugin can be used to extract additional data from the linked resource. For example, you can draw EXIF data from an image, or additional metadata from the YouTube API for a remote video. Then you can map that data to custom fields.

We go into much more detail on custom field management in the content linked in the prerequisites section.

## Add a tags field to the Image Media type

### Add the tags field

In the *Manage* administration menu, navigate to *Structure* > *Media types*, and then choose the *Manage fields* option from operations menus in the the *Image* row. (Or, the row for whichever Media type you're adding fields to.)

Press the *Add field* button.

In the *Add a new field* select list, choose the *Taxonomy term* option. Set the *Label* to "Tags". Then click the *Save and continue* button.

<drupal-media data-entity-type="media" data-entity-uuid="a7da25eb-24be-4be4-99f1-7c970d1dfb3d" alt="Add field form with Taxonomy term option selected under add a new field, and the Label field populated with "Tags"">

On the Field settings form, set the *Allowed number of values* to "unlimited" to allow for any number of tags to be added.

Fill in the Tags settings for the Image form on the resulting page.

Check the *Create referenced entities if they don't already exist* checkbox. This will configure the field to create a new Taxonomy term when the user enters a value into the tags field that doesn't match an existing term.

Check the *Tags* checkbox under *Vocabulary* to indicate that only terms from the Tags vocabulary should be used.

Image

![Form for configuring tags fields options](/sites/default/files/styles/max_800w/public/tutorials/images/media-type-add-tags-field-config.png?itok=lWt7wKPo)

Then press the *Save settings* button.

### Configure the field widget

You can improve the UX of adding tags to an image by changing the default widget for the Taxonomy reference field. Navigate to the *Manage form display* tab, find the *Tags* field in the table, and change the value of the *Widget* select list to the *Autocomplete (Tags style)* option. This will result in a single text field with tags separated via commas instead of one text field for each tag.

Image

![Form showing widget option for Tags field changed to Autocomplete (Tags style) ](/sites/default/files/styles/max_800w/public/tutorials/images/media-type-add-tags-field-widget-config.png?itok=kqqrVH1W)

### Confirm that it worked

Confirm it worked by adding a new Image media entity or editing an existing one. The relevant form should contain the new tags field.

Image

![Form for editing an Image media entity with new Tags field displayed and two tags entered.](/sites/default/files/styles/max_800w/public/tutorials/images/media-type-add-tags-field-add-image.png?itok=3NLGPVa-)

By default the newly added fields **are displayed** when the Media entity is displayed. You can change this by modifying the configuration of the view mode being used to display the Media entity via the *Manage display* tab. In this case it makes sense to hide the new tags field as it's intended purely for organizing the library.

Learn more about customizing how entities are displayed in [6.10. Concept: View Modes and Formatters](https://drupalize.me/tutorial/user-guide/structure-view-modes?p=3071).

## Map source data to custom fields

Media entity types can be configured to automatically populate a field when a new entity is created based on data extracted from the Media provider by a source plugin. Learn more in [Map Media Source Data to Custom Fields](https://drupalize.me/tutorial/map-media-source-data-custom-fields).

## Show fields in the Media Library upload form

When using the Media Library UI to browse for available media to insert into a field, users are also given the option to create new Media entities from within the Media Library.

For example, note the *Add files* section here:

Image

![Media Library image tab showing form for uploading a new image.](/sites/default/files/styles/max_800w/public/tutorials/images/media-library-widget-ui.png?itok=zmxf8esx)

When new items are created you'll be presented with a form to provide details about the entity before it's saved. You'll probably want to include at least some of the custom fields you've configured on this form. To do so, you'll need to configure them in the *Media library* form display mode for the Media type in question.

Navigate to the *Manage form display* tab for the Media type, and then in the secondary tabs choose *Media library* and configure the fields.

Example:

<drupal-media data-entity-type="media" data-entity-uuid="291f3fb1-091d-451e-ab24-42728f189f16" alt="Screenshot of page above with "Media library" tab highlighted">

After configuring it the form in the Media library should reflect any changes:

Image

![Screenshot of Media library form with custom photo credit and tags fields added.](/sites/default/files/styles/max_800w/public/tutorials/images/media-type-add-field-form-display-mode-example.png?itok=5cxtKY15)

## Display custom field data

Custom field data for Media types can be displayed in a variety of different ways. Some approaches include:

- [View modes and field formatters](https://drupalize.me/tutorial/user-guide/structure-view-modes?p=3071)
- [Display Content with Views](https://drupalize.me/topic/display-content-views)
- [Override a Template File](https://drupalize.me/tutorial/override-template-file) in your theme

## Recap

In this tutorial we learned how to add custom fields to a Media entity type that can store any data we need for our specific use case. This process is identical to adding fields to any other fieldable entity.

## Further your understanding

- Add a photo credit text field that allows someone to optionally enter a photographer's name and have it displayed along with a photo.
- How could you use custom fields to help organize a large Media library?

## Additional resources

- [Fields](https://drupalize.me/topic/fields) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[How to Add a Media Button to a WYSIWYG Editor in Drupal](/tutorial/how-add-media-button-wysiwyg-editor-drupal?p=2672)

Next
[Map Media Source Data to Custom Fields](/tutorial/map-media-source-data-custom-fields?p=2672)

Clear History

Ask Drupalize.Me AI

close