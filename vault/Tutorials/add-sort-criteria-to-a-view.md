---
title: "Add Sort Criteria to a View"
url: "https://drupalize.me/tutorial/add-sort-criteria-view?p=2670"
guide: "[[views-drupal]]"
---

# Add Sort Criteria to a View

## Content

In this tutorial, we'll walk through the process of adding and configuring sort criteria to a view.

## Goal

- Add *Year* (*field\_player\_award\_year*) as a sort criterion to the *Baseball Awards - Outfielders* view and configure its settings.

## Prerequisites

- [Set up Demo Site with Views and Content](https://drupalize.me/tutorial/set-demo-site-views-and-content)
- [Overview: Sort Criteria in Views](https://drupalize.me/tutorial/overview-sort-criteria-views)

We'll pick up where we left off in [Add Filter Criteria to a View](https://drupalize.me/tutorial/add-filter-criteria-view).

## Watch: Add Sort Criteria to a View

Sprout Video

## Add sort criteria to a view

In [Add Filter Criteria to a View](https://drupalize.me/tutorial/add-filter-criteria-view), we duplicated the Baseball Awards view (see [Set up Demo Site with Views and Content](https://drupalize.me/tutorial/set-demo-site-views-and-content)), and added filter criteria. Now, we'll take the view, *Baseball Awards - Outfielders*, and add sort criteria to it.

### Add a new sort criterion

Next to the **Sort Criteria** section, select *Add*. This will open a modal window containing a list of fields we can use to sort our content list.

Image

![Screenshot of modal window with list of fields available as sort criteria](/sites/default/files/styles/max_800w/public/tutorials/images/filters-sorts-add-items--sort-fields-overview.png?itok=W6cpVY58)

### Add *Year* (*field\_player\_award\_year*) as a sort criterion

In the search field at the top type the word **`Year`** to limit results to fields labeled as *Year*. Select the checkbox next to the field *Year* (*field\_player\_award\_year*), then select the *Add and configure sort criteria* button at the bottom of the modal.

Image

![Screenshot of sort criteria modal window with Year field selected](/sites/default/files/styles/max_800w/public/tutorials/images/filters-sorts-add-items--sort-select-year-field.png?itok=8JCpmzRn)

### Configure sort criterion to "sort descending"

After selecting adding a sort criterion, we can configure its *order* settings.

The sort's *Order* field has two options, `Sort ascending` and `Sort descending`. These options will apply for both numeric and text values.

Select the radio button next to the option for *Sort descending*, then select *Apply*.

Image

![Screenshot of sort criteria configuration modal with descending option selected](/sites/default/files/styles/max_800w/public/tutorials/images/filters-sorts-add-items--sort-year-descending.png?itok=M-3azyFq)

### Preview results

We have now modified our list of content so that the most recent award listed first. When we preview our list, we can see this new sort criteria in action. If you need to change the sort criteria, select the sort label in the **Sort Criteria** section and reconfigure as needed.

Image

![Screenshot of view configuration with new sort criteria added and preview of sorted list](/sites/default/files/styles/max_800w/public/tutorials/images/filters-sorts-add-items--sort-preview.png?itok=cOk4uiEe)

### Save the view

Select the *Save* button.

## Recap

In this tutorial, we added a sort to our view of *Baseball Awards - Outfielders*, to sort the results by year, descending, so that the most recent awards would appear at the top of the list.

## Further your understanding

- Try adding another sort criteria. How are the results affected?

## Additional resources

- [Drupal User Guide: Chapter 9. Creating Listings with Views](https://drupalize.me/series/user-guide/views-chapter) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview: Sort Criteria in Views](/tutorial/overview-sort-criteria-views?p=2670)

Next
[Overview: Exposed Sort Criteria in Views](/tutorial/overview-exposed-sort-criteria-views?p=2670)

Clear History

Ask Drupalize.Me AI

close