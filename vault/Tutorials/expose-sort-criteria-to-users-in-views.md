---
title: "Expose Sort Criteria to Users in Views"
url: "https://drupalize.me/tutorial/expose-sort-criteria-users-views?p=2670"
guide: "[[views-drupal]]"
---

# Expose Sort Criteria to Users in Views

## Content

Like exposed filters, we can expose sort criteria to the site visitor. Exposing sort criteria gives the visitor more control over the list of content they are viewing. In this tutorial, we'll configure our view of baseball players to allow visitors to sort the list in different ways by adding several exposed sort criteria.

## Goal

Add exposed sort criteria to the *Baseball Players* view.

## Prerequisites

- [Overview: Sort Criteria in Views](https://drupalize.me/tutorial/overview-sort-criteria-views)
- [Add Sort Criteria in Views](https://drupalize.me/tutorial/add-sort-criteria-view)
- [Overview: Expose Sort Criteria in Views](https://drupalize.me/tutorial/overview-exposed-sort-criteria-views)

Examples and screenshots in this tutorial are from the demo site we set up in:

- [Set up Demo Site with Views and Content](https://drupalize.me/tutorial/set-demo-site-views-and-content)

If you are new to Views, check out these Drupal User Guide tutorials:

- [Concept: Uses of Views](https://drupalize.me/tutorial/user-guide/views-concept)
- [Concept: The Parts of a View](https://drupalize.me/tutorial/user-guide/views-parts)

## Watch: Expose Sort Criteria to Users in Views

Sprout Video

## Add sort criteria to the view

Let's customize the *Baseball Players* view to allow visitors to sort the list of baseball players by any of the following fields:

- Debut
- Final game
- Height
- Weight

### Open the view for editing

From our site administration page, visit Structure > Views (*admin/structure/views*).

Locate the *Baseball Players* view and select *Edit* in the *Operations* column.

Image

![Screenshot of list of views with Baseball Players view shown](/sites/default/files/styles/max_800w/public/tutorials/images/exposed-filters--edit-baseball-players.png?itok=ZqGD2mCp)

### Add *Debut (field\_player\_debut)* as a sort criterion

Next to the **Sort Criteria** heading, select the *Add* button. This will open a modal window where we can select the field we want to use to sort our list.

Select the checkbox labeled "Debut" (`field_player_debut`), then select the *Add and configure sort criteria* button.

Image

![Screenshot of list of possible sort criteria with Debut selected](/sites/default/files/styles/max_800w/public/tutorials/images/exposed-sorts--debut-sort-add.png?itok=-RilHV-f)

### Expose *Debut* sort criterion to visitors

After selecting the field we want to configure as a sort criterion, a new modal window will appear that allows us to configure our new filter. At the top of this new modal window is a checkbox labeled *Expose this sort to visitors, to allow them to change it*.

Image

![Screenshot of exposed sort criteria modal window with values changed](/sites/default/files/styles/max_800w/public/tutorials/images/exposed-sorts--debut-sort-exposed.png?itok=Gg-QIa8o)

Select the checkbox *Expose this sort to visitors, to allow them to change it*. The modal window will refresh and show exposed sort configuration options.

### Configure exposed sort criterion

The new form for the exposed sort has one option, *Label*. Use the *Label* field to provide a user-friendly label for this field. Change the value of the *Label* option to be `Player Debut Date`, then select the *Apply* button.

Image

![Screenshot of sort criteria modal window](/sites/default/files/styles/max_800w/public/tutorials/images/exposed-sorts--debut-sort-options.png?itok=mU2JyMJi)

Note: You can customize the label above the field, `Sort by` in the **Advanced** column under **Exposed Form**. Select the *Settings* link next to *Exposed form style* and change the value of *Exposed sorts label* (default value is `Sort by`).

Image

![Screenshot of exposed sort form modal window with exposed sorts label highlighted](/sites/default/files/styles/max_800w/public/tutorials/images/exposed-sorts--exposed-sort-form-label.png?itok=yhNFbWYK)

### Preview and test exposed sort form

If we scroll down to preview the view we'll see our new exposed sort form in action.

Image

![Screenshot of preview of the view with new exposed sort criteria shown](/sites/default/files/styles/max_800w/public/tutorials/images/exposed-sorts--debut-sort-preview.png?itok=KzmLrjLL)

When we expose any sort criteria, we can decide whether or not to expose the sort operator as well. The operator is exposed by default and here it has the label Order. Site visitors can sort by this criteria in ascending or descending order.

Repeat the process to add sort criteria for:

- Final Game
- Height
- Weight

As you expose each one, give it a descriptive label to help visitors understand how the sort criteria will sort the list of content.

Here is a screenshot of our final results:

Image

![Screenshot of our list of exposed sort criteria and the preview for the view with all the new exposed sort criteria](/sites/default/files/styles/max_800w/public/tutorials/images/exposed-sorts--final-sorts-preview.png?itok=sDxsgYHA)

Be sure to preview and test each sort criterion. You can rearrange the order by selecting the dropdown menu *Add* in the **Sort Criteria** section of Views and selecting *Rearrange*. Drag the sort criteria in the order you want them.

### Save the view

Select the *Save* button.

Now anyone visiting the *Baseball Players* view can sort the results by any of the exposed sort criteria.

Image

![Screenshot of Baseball Players page with new exposed sort criteria shown](/sites/default/files/styles/max_800w/public/tutorials/images/exposed-sorts--final-sorts-page.png?itok=J_H6sD7N)

## Recap

In this tutorial, we added sort criteria and then exposed each one. This added an interactive form for our site visitors to use to sort the results displayed on the page.

## Further your understanding

- As we learned in the **Further your understanding** section of [Overview: Expose Sort Criteria in Views](https://drupalize.me/tutorial/overview-exposed-sort-criteria-views), you can add sorting functionality to Views using the Table format by configuring the table format settings. Experiment with adding sort to specific columns in the table along with adding exposed sort criteria. Which do you prefer? One or the other, or both? Which configuration provides the best usability to your end users?

## Additional resources

- [Drupal User Guide: Chapter 9. Creating Listings with Views](https://drupalize.me/series/user-guide/views-chapter) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview: Exposed Sort Criteria in Views](/tutorial/overview-exposed-sort-criteria-views?p=2670)

Next
[Overview: Relationships in Views](/tutorial/overview-relationships-views?p=2670)

Clear History

Ask Drupalize.Me AI

close