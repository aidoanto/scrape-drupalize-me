---
title: "6.9. Changing Content Entry Forms"
url: "https://drupalize.me/tutorial/user-guide/structure-form-editing?p=2412"
guide: "[[acquia-certified-drupal-developer-exam]]"
---

# 6.9. Changing Content Entry Forms

## Content

### Goal

Change the Recipe form to use a different widget to enter terms in the Ingredients field.

### Prerequisite knowledge

- [Section 6.1, “Adding a Content Type”](https://drupalize.me/tutorial/user-guide/structure-content-type "6.1. Adding a Content Type")
- [Section 6.3, “Adding Basic Fields to a Content Type”](https://drupalize.me/tutorial/user-guide/structure-fields "6.3. Adding Basic Fields to a Content Type")
- [Section 6.5, “Concept: Taxonomy”](https://drupalize.me/tutorial/user-guide/structure-taxonomy "6.5. Concept: Taxonomy")
- [Section 6.8, “Concept: Forms and Widgets”](https://drupalize.me/tutorial/user-guide/structure-widgets "6.8. Concept: Forms and Widgets")

### Site prerequisites

The Recipe content type must exist, and it must have an Ingredients taxonomy term reference field. At least one Vendor content item must exist. See [Section 6.1, “Adding a Content Type”](https://drupalize.me/tutorial/user-guide/structure-content-type "6.1. Adding a Content Type") and [Section 6.6, “Setting Up a Taxonomy”](https://drupalize.me/tutorial/user-guide/structure-taxonomy-setup "6.6. Setting Up a Taxonomy").

### Steps

Sprout Video

1. In the *Manage* administrative menu, navigate to *Content* > *Add content* > *Recipe* (*node/add/recipe*) to look at the content entry form that is set up by default. Notice how you have to enter ingredients one by one, instead of having a more compact format.
2. In the *Manage* administrative menu, navigate to *Structure* > *Content types* (*admin/structure/types*). Then click *Manage form display* on the dropdown button for the Recipe content type. The *Manage form display* page appears.
3. For the Ingredients field, select *Autocomplete (Tags style)* in the *Widget* column.

   Image

   ![Manage the Recipe form](/sites/default/files/styles/max_800w/public/user_guide/images/structure-form-editing-manage-form.png?itok=2wJ3tGbm)
4. Click *Save*.
5. In the *Manage* administrative menu, navigate to *Content* > *Add content* > Recipe (*node/add/recipe*) to verify the changed behavior of the content form. The Ingredients field is now a single text field that accepts multiple values.

   Image

   ![Add a recipe](/sites/default/files/styles/max_800w/public/user_guide/images/structure-form-editing-add-recipe.png?itok=rjDYaSAZ)
6. Create two Recipe content items (see [Section 5.2, “Creating a Content Item”](https://drupalize.me/tutorial/user-guide/content-create "5.2. Creating a Content Item")), such as recipes for "Green Salad" and "Fresh Carrots". Make sure all the fields have values, including images, ingredients, and submitted by (set this to one of the Vendor content items you created in [Section 6.3, “Adding Basic Fields to a Content Type”](https://drupalize.me/tutorial/user-guide/structure-fields "6.3. Adding Basic Fields to a Content Type")).

### Expand your understanding

Change the main site Contact form by navigating in the *Manage* administrative menu to *Structure* > *Contact forms*. For instance, you may want to hide the *Send yourself a copy* or *Language* fields.

Was this helpful?

Yes

No

Any additional feedback?

Previous
[6.8. Concept: Forms and Widgets](/tutorial/user-guide/structure-widgets?p=2412)

Next
[6.10. Concept: View Modes and Formatters](/tutorial/user-guide/structure-view-modes?p=2412)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close