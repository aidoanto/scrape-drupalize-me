---
title: "Add a Relationship to a View"
url: "https://drupalize.me/tutorial/add-relationship-view?p=2670"
guide: "[[views-drupal]]"
---

# Add a Relationship to a View

## Content

Now that you [understand the purpose of relationships in Views](https://drupalize.me/tutorial/overview-relationships-views), let's add a relationship to a view so that we can access and display a field value from a related entity.

In this tutorial, we'll modify the *Player Awards* view to add a relationship to the player that received the award. Then we will add a field that belongs to the player content that would normally not be available to the view without our new relationship.

## Goal

Add a player relationship to the *Baseball Awards* view. Add multiple player fields to the view that use the player relationship.

## Prerequisites

- [Overview: Relationships in Views](https://drupalize.me/tutorial/overview-relationships-views)

Examples and screenshots in this tutorial are from the demo site we set up in:

- [Set up Demo Site with Views and Content](https://drupalize.me/tutorial/set-demo-site-views-and-content)

If you are new to Views, check out these Drupal User Guide tutorials:

- [Concept: Uses of Views](https://drupalize.me/tutorial/user-guide/views-concept)
- [Concept: The Parts of a View](https://drupalize.me/tutorial/user-guide/views-parts)

## Watch: Add a Relationship to a View

Sprout Video

## Add player relationship to baseball awards view

In the following steps we'll open the *Baseball Awards* view (its page display) for editing and add a relationship.

From the administrative menu, go to Structure > Views (*admin/structure/views*).

Locate the view named *Baseball Awards* and select *Edit* in the *Operations* column.

Image

![Screenshot of list of views showing the Baseball Awards view](/sites/default/files/styles/max_800w/public/tutorials/images/relationships-add-item--edit-view.png?itok=k7_zPvT1)

In the right-most column, expand the **Advanced** section. This will allow you to view other configuration settings for views, including relationships.

Image

![Screenshot of view edit page showing advanced column open](/sites/default/files/styles/max_800w/public/tutorials/images/relationships-add-item--advanced-column.png?itok=qEvA2bSf)

Select the *Add* button located next to the **Relationships** section heading. This will open a new modal window that contains a list of all available relationships that can be added to our view.

Image

![Screenshot of view edit page with relationship list dialog open](/sites/default/files/styles/max_800w/public/tutorials/images/relationships-add-item--open-relationships.png?itok=fGXX4cGM)

Select the box next to the item named *Content referenced from field\_player\_award\_player*. Then select the button labeled *Add and configure relationships* at the bottom of the dialog.

Image

![Screenshot of relationship list dialog with a field selected](/sites/default/files/styles/max_800w/public/tutorials/images/relationships-add-item--select-relationship.png?itok=wXZG_f4i)

On the next dialog that appears, select the *Apply* button. We do not need to further configure the relationship.

Image

![Screenshot of relationship configuration page](/sites/default/files/styles/max_800w/public/tutorials/images/relationships-add-item--relationship-config.png?itok=Ia7BjQIG)

## Add fields that use the new relationship

Now that our view of Player Awards has access to the Player data that is associated with the Player Award, let's add some fields that display Player data.

Select the *Add* button located next to the **Fields** section header. Located the field named *Bats* that "Appears in: player". Check the box next to the item, then press the button labeled *Add and configure fields* at the bottom of the dialog.

Image

![Screenshot of view edit page with fields list dialog open](/sites/default/files/styles/max_800w/public/tutorials/images/relationships-add-item--field-bats-add.png?itok=8nzog9kV)

In the next dialog box that appears, locate the dropdown labeled *Relationship*. Change the value for the field to be **`field_player_award_player: Content`**.

Image

![Screenshot of field configuration dialog open](/sites/default/files/styles/max_800w/public/tutorials/images/relationships-add-item--field-bats-config.png?itok=FPncCGDy)

## Preview the view to see the newly related player data

We can now see our new relationship by selecting the *Update Preview* button located in the **Preview** section of the views' edit page.

Image

![Screenshot of view preview with new Bats column](/sites/default/files/styles/max_800w/public/tutorials/images/relationships-add-item--preview-results.png?itok=S8gGp5IY)

Don't forget to save the view!

## Recap

Relationships are a powerful mechanism within the Views module. They provide us a way to get field data from referenced content, creating more complex and complete lists of content.

## Further your understanding

- Add the following additional player fields to the view: Throws, Debut, and Final Game.
- Add a filter criterion that uses the new relationship.

## Additional resources

- [Drupal User Guide: Chapter 9. Creating Listings with Views](https://drupalize.me/series/user-guide/views-chapter) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview: Relationships in Views](/tutorial/overview-relationships-views?p=2670)

Next
[Overview: Contextual Filters in Views](/tutorial/overview-contextual-filters-views?p=2670)

Clear History

Ask Drupalize.Me AI

close