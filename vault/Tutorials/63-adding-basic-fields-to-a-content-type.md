---
title: "6.3. Adding Basic Fields to a Content Type"
url: "https://drupalize.me/tutorial/user-guide/structure-fields?p=2412"
guide: "[[acquia-certified-drupal-developer-exam]]"
order: 4
---

# 6.3. Adding Basic Fields to a Content Type

## Content

### Goal

Add a link field and an image field to the Vendor content type.

### Prerequisite knowledge

[Section 2.3, “Concept: Content Entities and Fields”](https://drupalize.me/tutorial/user-guide/planning-data-types "2.3. Concept: Content Entities and Fields")

### Site prerequisites

The Vendor content type must exist. See [Section 6.1, “Adding a Content Type”](https://drupalize.me/tutorial/user-guide/structure-content-type "6.1. Adding a Content Type").

### Steps

Sprout Video

Add the fields Vendor URL and Main image to the Vendor content type.

1. In the *Manage* administrative menu, navigate to *Structure* > *Content types* (*admin/structure/types*). Then click *Manage fields* in the dropdown button for the Vendor content type. The *Manage fields* page appears. From here you can either create a new field for the content type or re-use an existing field. Note that the names and descriptions of the content types and fields that were provided by your installation profile are shown in English on these pages; see [Section 2.7, “Concept: User Interface, Configuration, and Content translation”](https://drupalize.me/tutorial/user-guide/language-concept "2.7. Concept: User Interface, Configuration, and Content translation") for an explanation.
2. Click *Create a new field*. The *Add field* page appears.

   Image

   ![Add field page to choose field type](../assets/images/structure-fields-add-field.png)
3. Choose the *Link* field type from the *Choose a field type* options. Click *Continue*. The *Add field* page appears with a form to configure the field label.
4. Fill in the fields as shown below.

   | Field name | Explanation | Value |
   | --- | --- | --- |
   | Label | Label that is visible in administration pages | Vendor URL |
   | Choose a type of field | Field type | Link |

   A machine name is automatically generated, based on the *Label* value. Click *Edit* if you want to override the default name.

   Image

   ![Add field page to set field label](../assets/images/structure-fields-add-field-label.png)
5. Click *Continue. The page \_Vendor URL settings for Vendor* appears which allows you to configure the field. Fill in the fields as shown below.

   | Field name | Explanation | Value |
   | --- | --- | --- |
   | Label | Label that is visible in the content form | Vendor URL |
   | Allowed number of values | The number of values that can be entered | Limited, 1 |
   | Help text | The instruction that is shown below the field | (leave blank) |
   | Required field | Whether the field is required or not | Unchecked |
   | Allowed link type | The kind of links that can be entered | External links only |
   | Allow link text | Whether a link text can be entered | Disabled |

   Image

   ![Field settings page for Vendor URL](../assets/images/structure-fields-vendor-url.png)
6. Click *Save settings*. The Vendor URL has been added to the content type. Continue creating the Main image field.
7. Click *Create a new field*. The *Add field* page appears.
8. Choose the *File upload* field type from the *Choose a field type* options. Click *Continue*. The *Add field* page appears with a form to configure the field label.
9. Some field types require the selection of a sub-type. Fill in the fields as shown below.

   | Field name | Explanation | Value |
   | --- | --- | --- |
   | Label | Label that is visible in administration pages | Main image |
   | Choose an option below | Field sub-type | Image |
10. Click *Continue*. The page Main image settings for Vendor appears. Fill in the fields as shown below.

    | Field name | Explanation | Value |
    | --- | --- | --- |
    | Label | Label that is visible in the content form | Main image |
    | Allowed number of values | The number of values that can be entered | Limited, 1 |
    | Default image | You can set a default image here. This will be used when you do not provide an image when creating a Vendor content item. | (leave blank) |
    | Help text | The instruction that is shown below the field | (leave blank) |
    | Required field | Whether the field is required or not | Checked |
    | Allowed file extensions | The type of images that can be uploaded | png, gif, jpg, jpeg |
    | File directory | The directory where the files will be stored. By providing a file directory value, you ensure that all images uploaded via the Main image field will be located in the same directory. | vendors |
    | Minimum image dimensions | The minimum dimensions of the uploaded image | 600 x 600 |
    | Maximum upload size | The maximum file size of the uploaded image | 5 MB |
    | Enable Alt field | Whether an alternative text can be entered | Checked |
    | Alt field required | Whether an alternative text is required | Checked |

    Image

    ![Field settings page for Main Image](../assets/images/structure-fields-main-img.png)
11. Click *Save settings*. Main image has been added to the content type.

    Image

    ![Manage fields page](../assets/images/structure-fields-result.png)
12. Add a Main image field to the Recipe content type, using similar steps. Start by navigating to the Recipe content type’s *Manage Fields* page. Then use the *Re-use an existing field* button to open the modal dialog and press the *Re-use* button that corresponds with the Main image field in the table. Then skip to step 7 and follow the remaining steps.

    Image

    ![Select a field to re-use](../assets/images/structure-fields-main-img-reuse.png)
13. Create two Vendor content items (see [Section 5.2, “Creating a Content Item”](https://drupalize.me/tutorial/user-guide/content-create "5.2. Creating a Content Item")) called "Happy Farm" and "Sweet Honey". Make sure that they include images and URLs.

### Expand your understanding

- [Section 6.12, “Concept: Image Styles”](https://drupalize.me/tutorial/user-guide/structure-image-styles "6.12. Concept: Image Styles")
- [Section 6.11, “Changing Content Display”](https://drupalize.me/tutorial/user-guide/structure-content-display "6.11. Changing Content Display")
- [Section 6.9, “Changing Content Entry Forms”](https://drupalize.me/tutorial/user-guide/structure-form-editing "6.9. Changing Content Entry Forms")

### Additional resources

[*Drupal.org* community documentation page "Add a field to a content type"](https://www.drupal.org/docs/7/nodes-content-types-and-fields/add-a-field-to-a-content-type)

**Attributions**

Written by [Sree Veturi](https://www.drupal.org/u/sree) and [Boris Doesborg](https://www.drupal.org/u/batigolix), and [Joe Shindelar](https://www.drupal.org/u/eojthebrave) at [Drupalize.Me](https://drupalize.me).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[6.2. Deleting a Content Type](/tutorial/user-guide/structure-content-type-delete?p=2412)

Next
[6.4. Concept: Reference Fields](/tutorial/user-guide/structure-reference-fields?p=2412)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close