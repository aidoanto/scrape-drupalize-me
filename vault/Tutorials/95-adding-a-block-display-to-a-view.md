---
title: "9.5. Adding a Block Display to a View"
url: "https://drupalize.me/tutorial/user-guide/views-block?p=2449"
guide: "[[acquia-certified-drupal-developer-exam]]"
---

# 9.5. Adding a Block Display to a View

## Content

### Goal

Add a block display to the Recipes view to display the most recent recipes in a sidebar, and change its configuration without changing the existing Recipes page view.

### Prerequisite knowledge

- [Section 9.1, “Concept: Uses of Views”](https://drupalize.me/tutorial/user-guide/views-concept "9.1. Concept: Uses of Views")
- [Section 9.2, “Concept: The Parts of a View”](https://drupalize.me/tutorial/user-guide/views-parts "9.2. Concept: The Parts of a View")
- [Section 9.3, “Creating a Content List View”](https://drupalize.me/tutorial/user-guide/views-create "9.3. Creating a Content List View")

### Site prerequisites

- The Recipe content type must exist, it must have a Main image field, and your site must have a couple of Recipe content items. See [Section 6.1, “Adding a Content Type”](https://drupalize.me/tutorial/user-guide/structure-content-type "6.1. Adding a Content Type"), [Section 6.3, “Adding Basic Fields to a Content Type”](https://drupalize.me/tutorial/user-guide/structure-fields "6.3. Adding Basic Fields to a Content Type"), [Section 6.9, “Changing Content Entry Forms”](https://drupalize.me/tutorial/user-guide/structure-form-editing "6.9. Changing Content Entry Forms"), and [Section 5.2, “Creating a Content Item”](https://drupalize.me/tutorial/user-guide/content-create "5.2. Creating a Content Item").
- The *Thumbnail (100x100)* image style must be defined. This is created on your site when you install the core Image module (installed with the core Standard installation profile) but can be recreated if deleted. See [Section 6.13, “Setting Up an Image Style”](https://drupalize.me/tutorial/user-guide/structure-image-style-create "6.13. Setting Up an Image Style").
- The Recipes view must exist. See [Section 9.3, “Creating a Content List View”](https://drupalize.me/tutorial/user-guide/views-create "9.3. Creating a Content List View") and [Section 9.4, “Duplicating a View”](https://drupalize.me/tutorial/user-guide/views-duplicate "9.4. Duplicating a View").

### Steps

Sprout Video

1. In the *Manage* administrative menu, navigate to *Structure* > *Views* (*admin/structure/views*). Find the view "Recipes" and click *Edit* from its dropdown button. Alternatively, navigate to the Recipes page in the main site navigation, and click the *Edit view* contextual link in the main area of the page. See [Section 4.1, “Concept: Administrative Overview”](https://drupalize.me/tutorial/user-guide/config-overview "4.1. Concept: Administrative Overview") for information about contextual links.
2. Create a new block display by clicking *Add* under *Displays*. Click *Block* from the list of links that appears. The new display is created, and the focus is automatically switched to its configuration.

   Image

   ![Add block display](/sites/default/files/styles/max_800w/public/user_guide/images/views-block_add-block.png?itok=es5OEfeI)
3. To change the title of this display, click *Block* in the *Display name* field. The *Block: The name and the description of this display* pop-up appears. Change the *Administrative name* to "Recent recipes". Click *Apply*.
4. To change the title of the block, click Recipes in the *Title* field under *Title*. In the pop-up that appears, select *This block (override)* from the *For* select list. Change the *Title* field to "New recipes" and click *Apply (this display)*.

   Image

   ![Title only for this block](/sites/default/files/styles/max_800w/public/user_guide/images/views-block_title.png?itok=5yumD-1b)
5. To change the block’s style, click *Grid* in the *Format* field under *Format*. In the pop-up that appears, select *This block (override)* from the *For* select list. Select *Unformatted list* and Click *Apply (this display)*. You can further configure the style options in the next pop-up that appears. Then click *Apply*.
6. To configure the image field, click *Content: Main image* under *Fields*. In the pop-up that appears, select *This block (override)* from the *For* select list. Select *Image style Thumbnail (100x100)*. Click *Apply (this display)*.

   Image

   ![Image to thumbnail](/sites/default/files/styles/max_800w/public/user_guide/images/views-block_image.png?itok=cCFUBdUL)
7. To remove ingredients as a filter, click *Content: Ingredients (exposed)* under *Filter criteria*. In the pop-up that appears, select *This block (override)* from the *For* select list. Click *Remove* at the bottom.
8. To configure how you want the content to be sorted in the view, click *Add* from the dropdown button under *Sort criteria*. In the pop-up that appears, select *This block (override)* from the *For* select list. Check *Authored on* (in the *Content* category), and then click *Add and configure sort criteria*.
9. In the appearing configuration pop-up, select *Sort descending* to have the most recent recipes appear first. Click *Apply*.
10. To specify the number of items to be displayed, click *Mini* in the *Use pager* field under *Pager*. In the pop-up that appears, select *This block (override)* from the *For* select list. Under *Pager*, select *Display a specified number of items*. Click *Apply (this display)*. In the *Block: Pager options* pop-up, provide "5" as the value for *Items to display*. Click *Apply*.
11. Click *Save*. You will either see the view editing page again, or the Recipes page, depending on what you did in step 1. You should also see a message saying that the view has been saved.

    Image

    ![Summary page after configuration](/sites/default/files/styles/max_800w/public/user_guide/images/views-block_recipes.png?itok=6Vgf_Goo)
12. Place the "Recipes: Recent Recipes" block in the *Sidebar second* region. See [Section 8.3, “Placing a Block in a Region”](https://drupalize.me/tutorial/user-guide/block-place "8.3. Placing a Block in a Region"). Navigate to the site’s home page to see the block.

    Image

    ![New Recipes block on homepage](/sites/default/files/styles/max_800w/public/user_guide/images/views-block_sidebar.png?itok=GVnAtYYF)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[9.4. Duplicating a View](/tutorial/user-guide/views-duplicate?p=2449)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close