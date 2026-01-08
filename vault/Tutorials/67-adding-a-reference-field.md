---
title: "6.7. Adding a Reference Field"
url: "https://drupalize.me/tutorial/user-guide/structure-adding-reference?p=2412"
guide: "[[acquia-certified-drupal-developer-exam]]"
---

# 6.7. Adding a Reference Field

## Content

### Goal

Add a reference field so that recipes can be linked to the vendor that has submitted it.

### Prerequisite knowledge

- [Section 6.3, “Adding Basic Fields to a Content Type”](https://drupalize.me/tutorial/user-guide/structure-fields "6.3. Adding Basic Fields to a Content Type")
- [Section 6.4, “Concept: Reference Fields”](https://drupalize.me/tutorial/user-guide/structure-reference-fields "6.4. Concept: Reference Fields")
- [Section 6.1, “Adding a Content Type”](https://drupalize.me/tutorial/user-guide/structure-content-type "6.1. Adding a Content Type")

### Site prerequisites

The Recipe and Vendor content types must exist. See [Section 6.1, “Adding a Content Type”](https://drupalize.me/tutorial/user-guide/structure-content-type "6.1. Adding a Content Type").

### Steps

Sprout Video

1. In the *Manage* administrative menu, navigate to *Structure* > *Content types* (*admin/structure/types*). Then click *Manage fields* in the dropdown button for the Recipe content type. The *Manage fields* page appears.
2. Click *Create a new field*. The *Add field* page appears. Choose the *Reference* field type from the *Choose a field type* options. Click *Continue*. The *Add field* page appears with a form to configure the field label.

   Image

   ![Adding a reference field to a content type](/sites/default/files/styles/max_800w/public/user_guide/images/structure-adding-reference-add-field.png?itok=oXTIY1Js)
3. Fill in the fields as shown below. Click *Save and continue*.

   | Field name | Explanation | Value |
   | --- | --- | --- |
   | Label | The title you want to give the field | Submitted by |
   | Choose an option below: | Type of content to reference | Content |

   Image

   ![Adding a reference field to a content type](/sites/default/files/styles/max_800w/public/user_guide/images/structure-adding-reference-add-field-label.png?itok=UqU3dlEC)
4. The page Submitted by appears which lets you set the allowed number of values. Fill in the fields as shown below. Click *Save settings*.

   | Field name | Explanation | Value |
   | --- | --- | --- |
   | Type of item to reference | Option to select the type of referenced entity | Content |
   | Allowed number of values | Specify the count of values associated with the field | Limited, 1 |

   Image

   ![Storage configuration of a reference field](/sites/default/files/styles/max_800w/public/user_guide/images/structure-adding-reference-set-field-basic.png?itok=o6Xg0Uol)
5. The page *Submitted by settings for Recipe* appears which allows you to configure the field. Fill in the fields as shown below. Click *Save settings*.

   | Field name | Explanation | Value |
   | --- | --- | --- |
   | Label | Title shown for this field on the page | Submitted by |
   | Help text | Brief text aiding the person creating content | Choose the vendor that submitted this recipe |
   | Required field | Whether a value has to be provided or not | Checked |
   | Reference type > Reference method | Option to select reference method | Default |
   | Reference type > Content type | Specify the content type | Vendor |
   | Reference type > Sort by | Sorting field | Vendor name |
   | Reference type > Sort direction | Sorting order | Ascending |

   Image

   ![Settings for a reference field](/sites/default/files/styles/max_800w/public/user_guide/images/structure-adding-reference-field-settings.png?itok=1Ts1jCOl)
6. The Submitted by field has been added to the content type.

   Image

   ![Manage fields page for the Recipe content type](/sites/default/files/styles/max_800w/public/user_guide/images/structure-adding-reference-manage-fields.png?itok=JY4Qm3Ed)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[6.6. Setting Up a Taxonomy](/tutorial/user-guide/structure-taxonomy-setup?p=2412)

Next
[6.8. Concept: Forms and Widgets](/tutorial/user-guide/structure-widgets?p=2412)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close