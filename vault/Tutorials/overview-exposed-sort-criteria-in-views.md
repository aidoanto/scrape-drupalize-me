---
title: "Overview: Exposed Sort Criteria in Views"
url: "https://drupalize.me/tutorial/overview-exposed-sort-criteria-views?p=2670"
guide: "[[views-drupal]]"
order: 9
---

# Overview: Exposed Sort Criteria in Views

## Content

Exposing sort criteria allows the users of your site to sort a view using an interactive form.

By the end of this tutorial you will:

- Understand what it means to expose sort criteria and when it might be useful.
- Be able to identify a view's exposed sort criteria.

## Goal

- Understand what exposed sort criteria are, when they are useful, and what they look like in a view.

## Prerequisites

- [Overview: Sort Criteria in Views](https://drupalize.me/tutorial/overview-sort-criteria-views)
- [Add Sort Criteria to a View](https://drupalize.me/tutorial/add-sort-criteria-view)

Examples and screenshots in this tutorial are from the demo site we set up in:

- [Set up Demo Site with Views and Content](https://drupalize.me/tutorial/set-demo-site-views-and-content)

If you are new to Views, check out these Drupal User Guide tutorials:

- [Concept: Uses of Views](https://drupalize.me/tutorial/user-guide/views-concept)
- [Concept: The Parts of a View](https://drupalize.me/tutorial/user-guide/views-parts)

## Configuration options for exposed sort criteria

Similar to filter criteria, sort criteria can be configured to allow visitors to choose the field to use for sorting (*Sort by*), as well as the sort direction (*Order*).

When configuring exposed sort criteria, we have the following options:

- **Label**: The label is the value the visitor sees when using the exposed sort criteria field.
- **Order**: The order value is the default or starting direction in which the list is sorted. For example, A-Z (ascending) or Z-A (descending).

Image

![Screenshot of simple text sort criteria exposed configuration form](../assets/images/exposed-filters-sorts--sort-text-example.png)

Some sort criteria will have additional options, for example, date fields. Date fields have an extra option, granularity.

- **Granularity**: The smallest unit of time to use when comparing dates.

Image

![Screenshot of a date field sort criteria exposed configuration form](../assets/images/exposed-filters-sorts--sort-date-example.png)

## Preview and test the exposed sort form

Like exposed filter criteria, we can preview and test our exposed sort criteria while working on our view. Here is the same example view that we saw before, now with exposed sort criteria. Take notice of two things in particular with exposed sort criteria:

1. Exposed sort criteria appear as individual values within a single field.
2. The *Order* field is exposed alongside the exposed sort criteria by default.

Image

![Screenshot of preview showing our exposed sort criteria as a field in the exposed form above the list of content](../assets/images/exposed-filters-sorts--sort-preview.png)

## Exposed form options

When working with either exposed filter or sort criteria, also consider the configuration of the exposed form itself. The view edit interface provides some options for configuring the form, located in the **Advanced** column in the **Exposed form** section.

Image

![Screenshot of view edit form with the exposed form section highlighted](../assets/images/exposed-filters-sorts--highlight-form-options.png)

| Setting | Description |
| --- | --- |
| **Exposed form in block** | Whether or not we want the exposed form to be created as a block. Doing so requires that we place the block ourselves via Structure > Block layout (*admin/structure/block*). |
| **Exposed form style** | Whether or not we want our exposed form to require the visitor enter filter values before the view shows a list of content. |

### Exposed form settings

You can configure the form used for the exposed filter or sort criteria, like the submit button text and whether or not to include a reset button (a best practice).

| Setting | Description |
| --- | --- |
| **Submit button text** | Text the visitor will see for the exposed form submit button. |
| **Include reset button** | Whether or not to add a button to the form that will reset all the exposed filter and sort values when it's selected. |
| **Reset button label** | Text the visitor will see for the exposed reset button. |
| **Exposed sorts label** | Label text that will appear above the exposed sort criteria field. |
| **Allow people to choose the sort order** | Whether or not the *Order* field is exposed for sort criteria. |
| **Label for ascending sort** | Text for the *Sort ascending* option when the *Order* field is shown. |
| **Label for descending sort** | Text for the *Sort descending* option when the *Order* field is shown. |

Image

![Screenshot of exposed form settings configuration form](../assets/images/exposed-filters-sorts--exposed-form-settings.png)

## Recap

When we expose sort criteria, we are creating a form that allows visitors to interact with and change our list of content.

Exposing sort criteria means that visitors to our site can change the value and operator that the sort criteria use when building a list of content.

You can use these options to change simple lists of content into powerful tools our site, enabling visitors and administrators to customize content lists and find what they need.

## Further your understanding

- If your view uses the **Table** format, you can configure each column to be "sortable". Experiment with the table format settings by selecting Table *Settings* (in the **Format** section of Views UI). This will pop up a modal window with *Page: Style options* that include configuring which columns should be sortable. Which do you prefer? Exposing sort criteria in a form or having selectable table headings that will sort a column?

Image

![Screenshot of exposed form settings configration form](../assets/images/exposed-filters-sorts--table-sort.png)

## Additional resources

- [Drupal User Guide: Chapter 9. Creating Listings with Views](https://drupalize.me/series/user-guide/views-chapter) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add Sort Criteria to a View](/tutorial/add-sort-criteria-view?p=2670)

Next
[Expose Sort Criteria to Users in Views](/tutorial/expose-sort-criteria-users-views?p=2670)

Clear History

Ask Drupalize.Me AI

close