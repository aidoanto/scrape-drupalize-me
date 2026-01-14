---
title: "Overview: Filter Criteria in Viewsfree"
url: "https://drupalize.me/tutorial/overview-filter-criteria-views?p=2670"
guide: "[[views-drupal]]"
---

# Overview: Filter Criteria in Viewsfree

## Content

With filters, we can define query conditions and refine the results of a view. But what is a filter and how do filters work in Views? In this tutorial, you'll learn:

- How to add and configure filter criteria to a view to refine results
- What configuration options are available for filter criteria operators
- How filter groups allow you to group and order filter criteria to achieve desired results

By the end of this lesson, you should understand how to use and configure filter criteria in Views to refine the results of your view. (Note: We'll cover *exposed filters* in [Overview: Exposed Filter Criteria in Views](https://drupalize.me/tutorial/overview-exposed-filter-criteria-views))

## Goal

- Understand how you can refine the results of your view by adding and configuring filter criteria and filter groups through the Views UI.

## Prerequisites

Examples and screenshots in this tutorial are from the demo site we set up in:

- [Set up Demo Site with Views and Content](https://drupalize.me/tutorial/set-demo-site-views-and-content)

If you are new to Views, check out these Drupal User Guide tutorials:

- [Concept: Uses of Views](https://drupalize.me/tutorial/user-guide/views-concept)
- [Concept: The Parts of a View](https://drupalize.me/tutorial/user-guide/views-parts)

## Explore filter criteria in Views UI

The **Filter Criteria** section of the Views UI contains all filter criteria that added to your view. Filters allow you to refine the results of your view by adding *conditions* to the query that you're building using Views UI.

To add a condition to your query, add a filter and configure an operator and value. Each time you add a filter, you refine the results of your view. Your list will contain data that matches the conditions defined through filter criteria.

If you are familiar with MySQL, it may be helpful to know that filter criteria are the `WHERE` clause of the query that Views builds.

On the edit screen for a view, the **Filter Criteria** section appears beneath the **Fields** section and above the **Sort Criteria** section.

Image

![Screenshot of view edit page with filter criteria section highlighted](../assets/images/filters-sorts--highlight-filters-section.png)

Every field added to our content types, users, or other entities is available to add as a filter criteria to a view (most of the time). To illustrate, here is a side-by-side comparison of the fields added to our demo site's *Baseball Player* content type next to a list of available filter criteria in this content view.

Image

![Screenshot of list of fields on Baseball Player content type shown beside a list of filters available with some of the Baseball Player fields shown](../assets/images/filters-sorts--fields-filters-compare.png)

## Configuration options for filters

Filter criteria have two main configurable options:

- **Value**: The value to use in the field table lookup
- **Operator**: The method of comparison used in the field table lookup

Here is an example of a filter criteria configuration. The filter criteria shown below would limit our list of content to show content where the value of the *field\_player\_height* field is less than or equal to 50 (inches).

Image

![Screenshot of simple text filter configuration form](../assets/images/filters-sorts--height-filter-configuration.png)

Here is another example of a filter criteria configuration. In this example, the filter criteria would limit our list to show content that belongs to the content type, *Player*.

Image

![Screenshot of a list filter configuration form](../assets/images/filters-sorts--content-type-filter-configuration.png)

### Expose this filter?

Another option for configuring a filter criterion is to *expose* the filter. This means that the user can use a form to change the filter values and refine the list for themselves. See the related tutorial [Expose Filter Criteria to Users in Views](https://drupalize.me/tutorial/overview-exposed-filter-criteria-views).

## Filter groups

By default all filter criteria connect with a logical `AND` keyword. This means that every item in our list must pass through every added filter criterion.

For example, if we add the following filter criteria to our view then our list would show content that is *both* "Promoted to the front page" `AND` "Sticky at top of lists":

- Content: Promoted to front page (`= Yes`)
- Content: Sticky at top of lists (`= Yes`)

But what if we wanted our list to show content that was **either** "Promoted to the front page" **or** "Sticky at top of lists"? To do this, we can use filter groups to configure how our filter criteria relate to each other. We can choose group our filter criteria by rearranging them. This screenshot illustrates the interface for arranging our filter criteria into groups, and choosing how to relate the filter criteria to each other.

Image

![Screenshot of filter criteria arrangement options with some filters grouped together as an or group](../assets/images/filters-sorts--filter-groups.png)

## Recap

In this tutorial, we explored the **Filter Criteria** section of the Views UI. With filter criteria, we can refine the results of a view. When we add a filter, we configure an operator and value, which builds the `WHERE` clause of the database query used to return a set of results. When dealing with filter criteria, we can use filter groups to further refine or expand our query and determine how filter criteria relate to each other.

## Further your understanding

- Get some hands-on practice adding filters with [Add Filters in Views](https://drupalize.me/tutorial/add-filter-criteria-view).
- Learn about exposing filters to users in [Overview: Exposed Filter Criteria in Views](https://drupalize.me/tutorial/overview-exposed-filter-criteria-views).

## Additional resources

- [Drupal User Guide: Chapter 9. Creating Listings with Views](https://drupalize.me/series/user-guide/views-chapter) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add a REST Endpoint with Views](/tutorial/add-rest-endpoint-views?p=2670)

Next
[Add Filter Criteria to a View](/tutorial/add-filter-criteria-view?p=2670)

Clear History

Ask Drupalize.Me AI

close