---
title: "Customize the Drupal Media Library Browser Widget"
url: "https://drupalize.me/tutorial/customize-drupal-media-library-browser-widget?p=2672"
guide: "[[media-and-responsive-images]]"
---

# Customize the Drupal Media Library Browser Widget

## Content

When using the Drupal Media Library to browse for available Media entities to attach to your content, the interface that you see inside the modal window is created using Views. This means you can change it for your specific use-case. This is most useful when you want to expose filters for custom fields to allow users to more easily locate content in your library. As your library of media grows, you can create powerful application-specific ways for content authors to segment the list and find their assets.

In this tutorial we'll:

- Learn how to edit the Views used by the Drupal Media Library browser
- Add a new exposed filter for the custom tags field on some media entities
- Demonstrate how this change affects the user interface for locating and selecting media

By the end of this tutorial you should be able to customize the View used by the Media Library to add new filters and make other use-case specific changes.

## Goal

Override the default Media Library view and add an exposed filter for the tags field.

## Prerequisites

- [Add a Media Field to a Content Type in Drupal](https://drupalize.me/tutorial/add-media-field-content-type-drupal)
- [How to Add Fields to a Media Type in Drupal](https://drupalize.me/tutorial/how-add-fields-media-type-drupal)
- [Add Filter Criteria to a View](https://drupalize.me/tutorial/add-filter-criteria-view)

This tutorial assumes that you have the Media Library module enabled, that you have at least one content type with a Media field, and that you've [added a *tags* field to one or more media types](https://drupalize.me/tutorial/how-add-fields-media-type-drupal) for your site. The same technique for exposing custom filters for the Media Library view will work for any fields associated with media types.

## Watch: Customize the Drupal Media Library Browser Widget

Sprout Video

### Locate the Media Library view

In the *Manage* administration menu, navigate to *Structure* > *Views* (admin/content/views), then choose the *Edit* operation for the *Media library* view (admin/structure/views/view/media\_library).

This View is provided by the Media Library module and is required by the module in order for it to work. Whenever you open the Media Library browser you're seeing the output from this View.

The View contains three displays:

- *Page*: This display provides the page view at */admin/content/media*
- *Widget*: This display provides the output for the Grid view inside the Media Library's browser.
- *Widget (table)*: This display provides the output for the Table view inside the Media Library's browser.

While 2 widget displays have associated paths, you can't navigate to those paths outside of the Media Library browser. There's code in the module that forces those 2 specific paths to result in "403: Access denied".

### Add an exposed filter

Switch to the *Widget* display and press the *Add* button found next to *Filter Criteria*. Then choose the tags field (or any other field) from the list. Configure it as an exposed filter, and press apply. Learn more about exposed filters in [Overview: Exposed Filter Criteria in Views](https://drupalize.me/tutorial/overview-exposed-filter-criteria-views).

**Note**: For a consistent UI, add the exposed filter to the *Widget (table)* display, and the *Page* display, as well.

### Verify it works

Navigate to the add/edit form for any content type with a Media field. Press the *Add media* button to open the Media Library browser. Then confirm that your new filter appears in the UI.

Example:

Image

![Screenshot of Media Library browser with a textfield for filtering on tags shown in the UI.](../assets/images/add-exposed-filter-to-media-library-view.png)

## Change the way it looks

If you want to change the way that individual items shown in **the grid view of Media Library** are displayed, we recommend you make changes to the *Media library* view mode for the relevant media types. [6.10. Concept: View Modes and Formatters](https://drupalize.me/tutorial/user-guide/structure-view-modes?p=3071)

If you want to change the information available in **the table view of the Media Library** you can do so by adding or removing fields in the *Widget (table)* display of the *Media Library* View.

Make sure the *Media: Select media* field remains in the fields configuration for both widget displays. Without it, the Media Library browser will not allow users to select Media entities to insert.

For advanced use cases, the contributed [Entity Browser module](https://www.drupal.org/project/entity_browser) (a replacement for the Media Library UI) provides far more flexibility -- but is also much more complicated to set up initially.

## Recap

In this tutorial, we learned how to add a new exposed filter to the *Media library* View used when content authors are browsing for media assets. Because the Media browser is powered by a View behind the scenes, any changes we make to that View will be reflected in the UI.

## Further your understanding

- What additional fields might content authors like to use when filtering the media assets for your application?
- What are the limitations of trying to customize the Media Library browser by editing the Media Library view?

## Additional resources

- [Entity Browser module](https://www.drupal.org/project/entity_browser) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview: Access Control for Media Entities in Drupal](/tutorial/overview-access-control-media-entities-drupal?p=2672)

Next
[Track Media Entity Usage in Drupal](/tutorial/track-media-entity-usage-drupal?p=2672)

Clear History

Ask Drupalize.Me AI

close