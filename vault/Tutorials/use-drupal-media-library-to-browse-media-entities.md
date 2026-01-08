---
title: "Use Drupal Media Library to Browse Media Entities"
url: "https://drupalize.me/tutorial/use-drupal-media-library-browse-media-entities?p=2672"
guide: "[[media-and-responsive-images]]"
---

# Use Drupal Media Library to Browse Media Entities

## Content

The Drupal core Media Library module provides an enhanced user interface for locating Media entities and attaching them to an article. It's a drop-in replacement for the default entity reference widget which uses a not very intuitive autocomplete field. Using the Drupal core Media Library module requires minimal configuration.

If you want to provide content creators with a gallery-like library of Media entities that they can browse through in order to find the ones they want to add to their content, the Media Library is the easiest way to do it. It can be configured to work with both Media fields and the CKEditor powered WYSIWYG editor commonly used for editing the body field of Drupal nodes. There's really no reason not to use it.

In addition to providing a better UI for locating existing Media entities, the Media Library provides a way to create new Media entities right from the content creation form. This prevents an otherwise confusing requirement where Media entities need to be created, via a different set of forms, before they can be used.

In this tutorial we'll:

- Install and configure the Media Library module to work with Media fields
- Use the user interface provided by the Media Library to improve the experience of finding and selecting Media entities to associate with a piece of content

By the end of this tutorial you'll know how to replace the default entity reference widget used for selecting Media entities with the much improved Media Library UI.

## Goal

Replace the default Entity Reference field used to associate Media entities to Articles with the richer Media Library UI.

## Prerequisites

- [Add a Media Field to a Content Type](https://drupalize.me/tutorial/add-media-field-content-type-drupal)
- [6.4. Concept: Reference Fields](https://drupalize.me/tutorial/user-guide/structure-reference-fields)
- [6.8. Concept: Forms and Widgets](https://drupalize.me/tutorial/user-guide/structure-widgets)

This tutorial assumes that you've already [added a Media field to one or more content types](https://drupalize.me/tutorial/add-media-field-content-type-drupal) (the Article content type in this case), and that you want to replace the default entity reference widget currently being used.

## Watch: Use Drupal Media Library to Browse Media Entities

Sprout Video

## Enable and configure the Media Library UI

The Media Library module replaces the standard Media entity selection UI, which is really just a fancy text field, with a robust interface for browsing existing Media entities and uploading new ones. In that interface, Media entities are represented visually so it's easier to understand what you're looking at. It includes a grid of thumbnails for images and videos, and a table listing file names for PDF documents, for example.

Image

![Pop-up window provided by Media Library module showing a gallery of image thumbnails you can choose from and a form to upload new images.](/sites/default/files/styles/max_800w/public/tutorials/images/media-library-widget-ui.png?itok=zmxf8esx)

### Enable the Media Library module

If you haven't already done so, make sure the Media Library module is enabled.

In the *Manage* administration menu navigate to *Extend* (admin/extend), locate and check the checkbox for *Media Library*, then scroll to the bottom of the page and press the *Install* button.

### Configure a Media field to use the Media Library UI

With the Media Library module enabled, in the *Manage* administration menu navigate to *Structure* > *Content types* (admin/structure/types) and choose the *Manage form display* option from the *Operations* dropdown in the *Article* row. (Or the row of the content type that has the Media field you want to modify.)

For each field that you want to use the Media Library UI, update the select list in the *Widget* row and choose the *Media Library* option.

<drupal-media data-entity-type="media" data-entity-uuid="9d341753-cc3c-4d80-96aa-13093ae40510" alt="Select list with "Media Library" option selected">

### Optionally configure the widget

The Media library widget has one configuration option which allows you to change the order that the Media Type tabs appear in the Media Library UI. To change this, press the gear icon to configure the widget. Then use the drag & drop UI to re-order the list and press *Update* to save your changes.

Note: When Media fields are added you can configure the different Media types that the field can reference. Those types are what shows up in this list.

<drupal-media data-entity-type="media" data-entity-uuid="1f3c045a-1ff5-460f-bb64-8403808a5eff" alt="Media library tab order configuration showing "Image" and "Remote Video" options in a list that can be reordered.">

### Verify it worked

In the *Manage* administration menu, navigate to *Content* (admin/content), then press the *Add content* button, and choose *Article* from the list.

The Media reference field should now have a simpler UI with an *Add media* button in the middle. Pressing this button should open the Media Library UI and allow content authors to select Media entities for the field.

<drupal-media data-entity-type="media" data-entity-uuid="c6887934-3fd4-4db6-aff3-6970fd1e56b7" alt="Screen shot of old entity reference autocomplete widget with "Before" label, and new Media Library widget's "Add media" button with "After" label.">

## Media Library advanced UI

The Media Library module has a single configuration option which allows for enabling the advanced UI. This can be turned on by navigating to *Configuration* > *Media Library* (admin/config/media/media-library), and toggling the *Enable advanced UI* checkbox.

When enabled, if you open the Media Library, then select a couple of items, and then use the embedded form to add a new item, you'll see the changes on the resulting form for adding details about the newly added media.

In *normal* mode, the form will show you the number of items currently selected in the bottom right, and a single *Save* button which when pressed will return you to the Media Library with your current selection still available and allow you to select the new item(s).

Example:

Image

![Example of form described above.](/sites/default/files/styles/max_800w/public/tutorials/images/media-library-basic-ui.png?itok=CT1hx8hn)

With the *advanced* UI enabled, this form will show a more detailed list of the currently selected items, and you'll have two buttons: *Save and Select* which will return you to the Media Library with the new item(s) selected (in addition to any existing selected items), and *Save and Insert* which will save the new item(s), close the Media Library, and insert both the new and previously selected items into the corresponding field or editor.

Example:

Image

![Example of form described above.](/sites/default/files/styles/max_800w/public/tutorials/images/media-library-advanced-ui.png?itok=FcltteBe)

## Recap

In this tutorial, we learned how to improve the experience for authors who need to select Media entities to add to a piece of content. To do so we enabled the Media Library module, and configured the Media reference fields attached to a content type to use the Media Library widget.

## Further your understanding

- Can you think of a use-case where using the autocomplete style entity reference field for choosing Media entities might be better?
- Try using the form within the Media Library UI to add new Media entities. What happens? How does this differ from adding them directly va the Media add form?

## Additional resources

- [Use Media Library with CKEditor](https://drupalize.me/tutorial/how-add-media-button-wysiwyg-editor-drupal) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Find, Add, Edit, and Delete Media Entities in Drupal](/tutorial/find-add-edit-and-delete-media-entities-drupal?p=2672)

Next
[How to Add a Media Button to a WYSIWYG Editor in Drupal](/tutorial/how-add-media-button-wysiwyg-editor-drupal?p=2672)

Clear History

Ask Drupalize.Me AI

close