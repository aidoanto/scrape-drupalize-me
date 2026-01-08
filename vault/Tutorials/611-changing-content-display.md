---
title: "6.11. Changing Content Display"
url: "https://drupalize.me/tutorial/user-guide/structure-content-display?p=2412"
guide: "[[acquia-certified-drupal-developer-exam]]"
---

# 6.11. Changing Content Display

## Content

### Goal

Make the content items more readable, accessible, and visibly attractive by reordering the fields, hiding labels, and tuning the output of the fields.

### Prerequisite knowledge

- [Section 2.3, “Concept: Content Entities and Fields”](https://drupalize.me/tutorial/user-guide/planning-data-types "2.3. Concept: Content Entities and Fields")
- [Section 6.10, “Concept: View Modes and Formatters”](https://drupalize.me/tutorial/user-guide/structure-view-modes "6.10. Concept: View Modes and Formatters")

### Site prerequisites

The Vendor content type must exist, it must have Main Image and Vendor URL fields, and your site must have at least one Vendor content item. See [Section 6.1, “Adding a Content Type”](https://drupalize.me/tutorial/user-guide/structure-content-type "6.1. Adding a Content Type"), [Section 6.3, “Adding Basic Fields to a Content Type”](https://drupalize.me/tutorial/user-guide/structure-fields "6.3. Adding Basic Fields to a Content Type"), and [Section 5.2, “Creating a Content Item”](https://drupalize.me/tutorial/user-guide/content-create "5.2. Creating a Content Item").

### Steps

Sprout Video

1. Find and view a Vendor content item you created in [Section 6.3, “Adding Basic Fields to a Content Type”](https://drupalize.me/tutorial/user-guide/structure-fields "6.3. Adding Basic Fields to a Content Type"). Notice that there are several things that could be done to improve how the page looks:

   - The Main Image and Vendor URL fields should not have labels.
   - The order of the fields should be changed so that the image comes first.
   - The image should be smaller.
2. To fix the first two problems, and update some additional settings, in the *Manage* administrative menu, navigate to *Structure* > *Content types* (*admin/structure/types*). Then click *Manage display* in the dropdown button for the Vendor content type.

   Image

   ![Manage display](/sites/default/files/styles/max_800w/public/user_guide/images/structure-content-display_manage_display.png?itok=z62iUh-L)
3. Under the *Label* column, select *Hidden* for Main image. Do the same for Vendor URL.

   Image

   ![Selecting main image title as hidden](/sites/default/files/styles/max_800w/public/user_guide/images/structure-content-display_main_image_hidden.png?itok=lenqdlHc)
4. Click the gear wheel for the Vendor URL field, to open the configuration options.
5. Fill in the fields as shown below.

   | Field name | Explanation | Example value |
   | --- | --- | --- |
   | Trim link text length | Maximum displayed length for link text | Blank (no trimming) |
   | Open link in new window | Whether links should open in a new window or the same window | Checked |

   Image

   ![Link trim length](/sites/default/files/styles/max_800w/public/user_guide/images/structure-content-display_trim_length.png?itok=kQ1zI2RC)
6. Click *Update*.
7. Drag the cross bar handles of the fields to reorder as Main image, *Body*, Vendor URL, and *Links*. As an alternative to dragging, you can click the *Show row weights* link at the top of the table and enter numerical weights (fields with lower or more negative weights will be shown first).

   Image

   ![Changing order of fields](/sites/default/files/styles/max_800w/public/user_guide/images/structure-content-display_change_order.png?itok=eED6wdtW)
8. Click *Save*.
9. Find the Vendor content item from step 1 again, and verify that the updates have been made.
10. Repeat similar steps to manage the display of the Recipe content type fields.

### Expand your understanding

- Make the main image smaller. See [Section 6.13, “Setting Up an Image Style”](https://drupalize.me/tutorial/user-guide/structure-image-style-create "6.13. Setting Up an Image Style").
- If you do not see the effect of these changes in your site, you might need to clear the cache. See [Section 12.2, “Clearing the Cache”](https://drupalize.me/tutorial/user-guide/prevent-cache-clear "12.2. Clearing the Cache").

### Related concepts

[Section 6.12, “Concept: Image Styles”](https://drupalize.me/tutorial/user-guide/structure-image-styles "6.12. Concept: Image Styles")

### Additional resources

- [*Drupal.org* community documentation page "Specify how fields are displayed"](https://www.drupal.org/docs/7/nodes-content-types-and-fields/specify-how-fields-are-displayed)
- [*Drupal.org* community documentation page "Rearrange the order of fields"](https://www.drupal.org/docs/7/nodes-content-types-and-fields/rearrange-the-order-of-fields)
- [*Drupal.org* community documentation page "View modes"](https://www.drupal.org/node/1577752)

**Attributions**

Written by [Ann Greazel](https://www.drupal.org/u/AnnGreazel) and [Boris Doesborg](https://www.drupal.org/u/batigolix).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[6.10. Concept: View Modes and Formatters](/tutorial/user-guide/structure-view-modes?p=2412)

Next
[6.12. Concept: Image Styles](/tutorial/user-guide/structure-image-styles?p=2412)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close