---
title: "Overview: Sort Criteria in Views"
url: "https://drupalize.me/tutorial/overview-sort-criteria-views?p=2670"
guide: "[[views-drupal]]"
---

# Overview: Sort Criteria in Views

## Content

With sort criteria, we can specify how to order our list. We can specify sort criteria using any field on or related to our view's base entity, and then specify in which order to sort, e.g. ascending or descending. If you are familiar with MySQL, it may be helpful to know that sort criteria are the `ORDER BY` clause of the query that Views builds. In this tutorial, you'll learn:

- How to add and configure sort criteria to a view to sort the list in various ways
- What configuration options are available

By the end of this lesson, you should understand how to use and configure sort criteria in Views. (Note: We'll cover *exposed sort criteria* in [Overview: Exposed Sort Criteria in Views](https://drupalize.me/tutorial/overview-exposed-sort-criteria-views))

## Goal

- Understand how you can refine the results of your view by adding and configuring filter criteria and filter groups through the Views UI.

## Prerequisites

Examples and screenshots in this tutorial are from the demo site we set up in:

- [Set up Demo Site with Views and Content](https://drupalize.me/tutorial/set-demo-site-views-and-content)

If you are new to Views, check out these Drupal User Guide tutorials:

- [Concept: Uses of Views](https://drupalize.me/tutorial/user-guide/views-concept)
- [Concept: The Parts of a View](https://drupalize.me/tutorial/user-guide/views-parts)

## What are sort criteria?

*Sort criteria* are settings for a view that determine what order the content appears in the list. If you are familiar with MySQL, it may be helpful to know that sort criteria are the `ORDER BY` clause of the query that Views builds.

On the edit screen for a view, find the **Sort Criteria** section beneath the **Filter Criteria** section.

Image

![Screenshot of view edit page with sort criteria section highlighted](/sites/default/files/styles/max_800w/public/tutorials/images/filters-sorts--highlight-sorts-section.png?itok=crG5X_Ma)

Every field added to our content types, users, and other Drupal entities is available in Views as a sort criteria (most of the time). To illustrate that statement, here is a side-by-side comparison of the fields that are a part of our *Baseball Player* content type next to a list of available sort criteria.

Image

![Screenshot of list of fields on Baseball Player content type shown beside a list of sorts available with some of the Baseball Player fields shown](/sites/default/files/styles/max_800w/public/tutorials/images/filters-sorts--fields-sorts-compare.png?itok=0qMMbyXq)

## Sort criteria configuration options

When we add sort criteria to our view, we need to configure one important option.

- **Order**: The direction of the sort.

The *Order* option has two values to choose from, `Sort ascending` and `Sort descending`. These options will apply for both numeric and text values.

Image

![Screenshot of sort criteria configuration form](/sites/default/files/styles/max_800w/public/tutorials/images/filters-sorts--sort-options.png?itok=KMNlIWMZ)

In the case that our sort criteria is a numeric value, "ascending" means it will sort the list starting from the lowest number and going to the highest number, and "descending" means it will sort the list starting from the highest number and going to the lowest number.

In the case that our sort criteria is text (such as a word or sentence), "ascending" means it will sort the list starting at the letter `A` and going to the letter `Z`, and "descending" means it will sort the list starting at the letter `Z` and going to the letter `A`.

## Exposed sort criteria

Another option for configuring a sort criterion is to *expose* it. This means that the user can use a form to change the sort order for themselves. See the related tutorial [Overview: Exposed Sort Criteria in Views](https://drupalize.me/tutorial/overview-exposed-sort-criteria-views).

## Recap

In this lesson, we covered how to use and configure sort criteria in Views to change the sort order of the list.

## Further your understanding

- Get some hands-on practice adding filters with [Add Sort Criteria to a View](https://drupalize.me/tutorial/add-sort-criteria-view).
- Learn about exposing sort criteria to users in [Overview: Exposed Sort Criteria in Views](https://drupalize.me/tutorial/overview-exposed-filter-criteria-views).

## Additional resources

- [Drupal User Guide: Chapter 9. Creating Listings with Views](https://drupalize.me/series/user-guide/views-chapter) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Expose Filter Criteria to Users in Views](/tutorial/expose-filter-criteria-users-views?p=2670)

Next
[Add Sort Criteria to a View](/tutorial/add-sort-criteria-view?p=2670)

Clear History

Ask Drupalize.Me AI

close