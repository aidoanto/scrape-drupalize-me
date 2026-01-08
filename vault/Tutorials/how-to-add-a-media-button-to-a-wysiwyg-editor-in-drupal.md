---
title: "How to Add a Media Button to a WYSIWYG Editor in Drupal"
url: "https://drupalize.me/tutorial/how-add-media-button-wysiwyg-editor-drupal?p=2672"
guide: "[[media-and-responsive-images]]"
---

# How to Add a Media Button to a WYSIWYG Editor in Drupal

## Content

A commonly asked question is, "How do you add images to the body of a content item in Drupal?" You can allow users to embed images, videos, or any other media into a field configured with a WYSIWYG editor, such as CKEditor. In this tutorial, we’ll show you how to enable Drupal’s *Insert Media* button for CKEditor, and configure the corresponding text format so that it can render embedded Media entities.

Content authors can then use the Media Library to select images (or other media) to embed into the page.

In this tutorial we'll:

- Learn how to enable the *Insert Media* button for CKEditor
- Demonstrate how to insert media into the body of a content item (or any other field configured to use CKEditor)

By the end of this tutorial you should know how to configure Drupal to allow content authors to embed images in content items.

## Goal

Add a Media Library button to the CKEditor (WYSIWYG Editor) configuration. Allow embedding Media entities directly into the body of an article.

## Prerequisites

- [Use Media Library to Browse Media Entities](https://drupalize.me/tutorial/use-drupal-media-library-browse-media-entities)
- [6.15. Concept: Text Formats and Editors](https://drupalize.me/tutorial/user-guide/structure-text-formats?p=3071)
- [6.16. Configuring Text Formats and Editors](https://drupalize.me/tutorial/user-guide/structure-text-format-config?p=3071)

## Watch: How to Add a Media Button to a WYSIWYG Editor in Drupal

Sprout Video

## Configure CKEditor with a Media Library button

The 2 things you need to do to enable users to embed Media entities via CKEditor are:

1. Configure CKEditor to display the Media Library button
2. Enable and configure the *Embed media* filter

### Add the Media Library button to CKEditor

In the *Manage* administration menu, navigate to *Configuration* > *Text formats and editors* (*admin/config/content/formats*), then select the *Configure* button in the row for the text format you would like to configure.

In the *Toolbar configuration* section, drag the *Insert item from Media Library* button -- the one with the icon of an overlapping image and musical note -- into the *Active toolbar*.

Image

![CKEditor configuration widget showing the media button added to the active toolbar configuration.](/sites/default/files/styles/max_800w/public/tutorials/images/ckeditor-configure.png?itok=LiqSrxQt)

### Remove the "insert image" button

While not required, we recommend that you remove the *Image* button from the *Active toolbar* if it's enabled. Having both the media button and the image button enabled can lead to confusion for end users who have to choose between the two.

And it's unlikely you want to mix embed types.

### Enable the *Media embed* filter

Under the *Enabled filters* section, check the box for *Embed media*. This filter processes the `<drupal-media>` tags that the button you just configured inserts into the editor and renders the relevant Media entity.

Image

![Configuration form for the Media embed filter with default values selected for all fields.](/sites/default/files/styles/max_800w/public/tutorials/images/ckeditor-configure-filter.png?itok=-vM5BLAp)

Under *Filter processing order*, make sure the *Embed media* filter is last.

You'll want this filter to run last -- with the exception of any filters like Pathologic that handle re-writing of file paths into absolute URLs, or custom filters that need to process the rendered media tags.

Under *Filter settings*, the *Embed media* tab allows you to configure how the filter works. It also impacts how the button you enabled above works.

- **Default view mode**: Lets you choose which view mode to use when displaying Media entities.
- **Media types selectable in the Media Library**: You can choose to allow content authors to only insert specific types of media into the text editor.
- **View modes selectable in the 'Edit media' dialog**: Optionally allow content authors to choose which view mode to use when rendering an embedded Media entity. For example, you can allow them to choose between inserting a thumbnail that links to a full image, or the full image.

### Change the way embedded media looks

When media items are embedded into a textarea Drupal will use the specified view mode to determine what the output looks like. If for example you're embedding an Image media entity and you want to display it as a full-width responsive image you would need to do the following:

- Define a new [*responsive* image style](https://drupalize.me/tutorial/user-guide/structure-image-responsive?p=3071).
- Define a new [view mode](https://drupalize.me/tutorial/user-guide/structure-view-modes?p=3071) and configure it to output the image field of the Image media type using the image style you defined previously.
- Enable the new view mode as the *Default view mode* or one of the selectable view modes in the configuration for the *Embed media* button.

You can learn more about Media entity view modes in [Use View Modes with Media Entities](https://drupalize.me/tutorial/use-view-modes-media-entities-drupal)

### Save your changes

Press the *Save configuration* button at the bottom of the page to save your changes.

After doing so you should be taken back to the page listing all text formats, and a message saying "The text format has been updated" will be displayed.

## Insert a Media entity and verify it works

Add a new content item, or edit an existing one, and insert a Media entity.

### Insert a Media entity

On the form for editing a content item, with CKEditor present, press the *Insert Media* button added above.

Image

![Body field on article editing form showing CKEditor with the Insert Media button present.](/sites/default/files/styles/max_800w/public/tutorials/images/ckeditor-insert.png?itok=qeFyAV2V)

### Select an item to insert

This will open the Media Library and you can choose the Media entity to embed. Note that in this scenario you're limited to selecting a single item. If you want to add another you'll need to repeat the process for each one.

Image

![Media library widget with a single image item selected](/sites/default/files/styles/max_800w/public/tutorials/images/ckeditor-insert-selected.png?itok=tSM6ZZpw)

Select an item and press *Insert selected*.

The selected Media entity will be embedded into the field, and a preview rendered, along with an *Edit media* button.

Image

![Body field with image inserted.](/sites/default/files/styles/max_800w/public/tutorials/images/ckeditor-inserted-image.png?itok=Jv8BxvA9)

### Edit the embedded item

If you press the *Edit media* button a modal window will open that allows you to further configure the embedded entity. The options available will vary depending on the Media type. This will allow you to change the element's alignment. If you allowed content authors to select a view mode to use for displaying Media when you configured the filter above they'll be able to do so in this modal.

Image

![Modal window with configuration options for an embedded image media entity.](/sites/default/files/styles/max_800w/public/tutorials/images/ckeditor-inserted-image-edit.png?itok=omc0kxdJ)

## Recap

In this tutorial we learned how to enable the *Insert Media* button for CKEditor to allow content authors to add Media entities into a text field. We then looked at how a content author could use the new button to add an image to the body of a content item.

## Further your understanding

- What do you expect will happen if you disable the *Align images* or *Caption images* filters for the text format that you configured to use the *Insert Media* button?
- Press the *View source* button on the body field with a Media entity embedded. What do you see? What did you expect to see? How does this differ if you view the source of the published page in your browser?

## Additional resources

- [6.10. Concept: View Modes and Formatters](https://drupalize.me/tutorial/user-guide/structure-view-modes?p=3071) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Use Drupal Media Library to Browse Media Entities](/tutorial/use-drupal-media-library-browse-media-entities?p=2672)

Next
[How to Add Fields to a Media Type in Drupal](/tutorial/how-add-fields-media-type-drupal?p=2672)

Clear History

Ask Drupalize.Me AI

close