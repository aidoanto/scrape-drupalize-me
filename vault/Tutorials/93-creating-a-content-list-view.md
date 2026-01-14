---
title: "9.3. Creating a Content List View"
url: "https://drupalize.me/tutorial/user-guide/views-create?p=2449"
guide: "[[acquia-certified-drupal-developer-exam]]"
---

# 9.3. Creating a Content List View

## Content

### Goal

Create a page listing vendors that will be automatically updated whenever a vendor is added, deleted, or updated on the site.

### Prerequisite knowledge

- [Section 9.1, “Concept: Uses of Views”](https://drupalize.me/tutorial/user-guide/views-concept "9.1. Concept: Uses of Views")
- [Section 9.2, “Concept: The Parts of a View”](https://drupalize.me/tutorial/user-guide/views-parts "9.2. Concept: The Parts of a View")

### Site prerequisites

- The core Views and Views UI modules must be installed. These are installed for you when you install with the core Standard installation profile.
- The Vendor content type must exist, with URL and Main image fields. Your site must have a couple of Vendor content items. See [Section 6.1, “Adding a Content Type”](https://drupalize.me/tutorial/user-guide/structure-content-type "6.1. Adding a Content Type"), [Section 6.3, “Adding Basic Fields to a Content Type”](https://drupalize.me/tutorial/user-guide/structure-fields "6.3. Adding Basic Fields to a Content Type"), and [Section 5.2, “Creating a Content Item”](https://drupalize.me/tutorial/user-guide/content-create "5.2. Creating a Content Item").
- The *Medium (220x220)* image style must be defined. This is created on your site when you install the core Image module (installed with the core Standard installation profile) but can be recreated if deleted. See [Section 6.13, “Setting Up an Image Style”](https://drupalize.me/tutorial/user-guide/structure-image-style-create "6.13. Setting Up an Image Style").

### Steps

Sprout Video

1. In the *Manage* administrative menu, navigate to *Structure* > *Views* > *Add view* (*admin/structure/views/add*). The *Add view* wizard appears.
2. Fill in the fields as shown below.

   | Field name | Explanation | Example value |
   | --- | --- | --- |
   | View basic information > View name | Name of the view that will be visible in the administration pages | Vendors |
   | View settings > Show | Type of information listed in the view | Content |
   | View settings > of type | Specify content type | Vendor |
   | View settings > sorted by | List order | Title |
   | Page settings > Create a page | Create a page that displays the view | Checked |
   | Page settings > Page title | Title show above the view | Vendors |
   | Page settings > Path | Address of the page | vendors |
   | Page settings > Page display settings > Display format | Type of list | Table |
   | Page settings > Items to display | Number of items visible on the page | 10 |
   | Page settings > Use a pager | Split up the list in several pages if there are more items | Checked |
   | Page settings > Create a menu link | Add the view page to the menu | Checked |
   | Page settings > Menu > Type | Type of menu item to create | Normal menu entry |
   | Page settings > Menu > Menu link title | Label of the link in the menu | Vendors |
   | Page settings > Menu > Parent | Menu in which to add the link | Main navigation |

   Image

   ![Add new view wizard](../assets/images/views-create-wizard.png)
3. Click *Save and edit*. The view configuration page appears.
4. Under *Fields*, click *Add* from the dropdown button. The *Add fields* pop-up appears.
5. Enter the word "image" in the search field.
6. Check Main image in the table.
7. Click *Apply*. The *Configure field: Content: Main Image* pop-up appears.
8. Fill in the fields as shown below.

   | Field name | Explanation | Example value |
   | --- | --- | --- |
   | Create a label | Add a label before the field value | Unchecked |
   | Image style | The format of the image | Medium (220x220) |
   | Link image to | Add a link to the content item | Content |
9. Click *Apply*. The view configuration page appears.
10. Under *Fields*, click *Add* from the dropdown button. The *Add fields* pop-up appears.
11. Enter the word "body" in the search field.
12. Select *Body* in the table.
13. Click *Apply*. The *Configure field: Content: Body* pop-up appears.
14. Fill in the fields as shown below.

    | Field name | Explanation | Example value |
    | --- | --- | --- |
    | Create a label | Add a label before the field value | Unchecked |
    | Formatter | The presentation of the field value | Summary or trimmed |
    | Trimmed limit: | The number of maximum characters shown | 120 |
15. Click *Apply*. The view configuration page appears.
16. Under *Fields*, click *Content: Title (Title)*. The *Configure field: Content: Title* pop-up appears.
17. Uncheck *Create a label*. This will remove the label that was created by the wizard.
18. Click *Apply*. The view configuration page appears.
19. Under *Fields*, click *Rearrange* in the dropdown button. The *Rearrange fields* pop-up appears.
20. Drag the cross bar handles of fields to put them into the right order: Image, Title, Body. As an alternative to dragging, you can click the *Show row weights* link at the top of the table and enter numerical weights (fields with lower or more negative weights will be shown first).
21. Click *Apply*. The view configuration page appears.
22. Optionally, click *Update preview* for a preview.
23. Click *Save*.

    Image

    ![Vendors view configuration page](../assets/images/views-create-view.png)
24. Navigate to the homepage and click Vendors from the main navigation to see the result.

    Image

    ![Vendors view output](../assets/images/views-create-view-output.png)

### Expand your understanding

The link to the view in the main navigation will probably not be in the right place. Change the order of the menu links in the main navigation. See [Section 5.7, “Changing the Order of Navigation”](https://drupalize.me/tutorial/user-guide/menu-reorder "5.7. Changing the Order of Navigation").

Was this helpful?

Yes

No

Any additional feedback?

Previous
[9.2. Concept: The Parts of a View](/tutorial/user-guide/views-parts?p=2449)

Next
[9.4. Duplicating a View](/tutorial/user-guide/views-duplicate?p=2449)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close