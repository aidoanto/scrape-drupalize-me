---
title: "Expose Filter Criteria to Users in Views"
url: "https://drupalize.me/tutorial/expose-filter-criteria-users-views?p=2670"
guide: "[[views-drupal]]"
---

# Expose Filter Criteria to Users in Views

## Content

Instead of providing multiple views with different filter criteria, consider empowering your users by exposing filter criteria as an interactive form. You can even configure the forms to use AJAX to refresh results. In this tutorial, we'll walk through the process of adding and configuring exposed filter or sort criteria in a view.

## Goal

Add, expose, and configure the *Debut Date* filter in the *Baseball Players* view.

## Prerequisites

- [Overview: Filter Criteria in Views](https://drupalize.me/tutorial/overview-filter-criteria-views)
- [Add Filters in Views](https://drupalize.me/tutorial/add-filter-criteria-view)
- [Overview: Expose Filter Criteria in Views](https://drupalize.me/tutorial/overview-exposed-filter-criteria-views)

Examples and screenshots in this tutorial are from the demo site we set up in:

- [Set up Demo Site with Views and Content](https://drupalize.me/tutorial/set-demo-site-views-and-content)

If you are new to Views, check out these Drupal User Guide tutorials:

- [Concept: Uses of Views](https://drupalize.me/tutorial/user-guide/views-concept)
- [Concept: The Parts of a View](https://drupalize.me/tutorial/user-guide/views-parts)

## Watch: Expose Filter Criteria to Users in Views

Sprout Video

## Add and expose filter criteria to existing view

Let's start by adding filters to our *Baseball Player* view. We want to allow site visitors to filter the list of baseball players by the player's debut dates.

### Open Baseball Players view for editing

From our site administration page, visit Structure > Views (*admin/structure/views*).

Locate the Baseball Player view and select *Edit* in the *Operations* column.

Image

![Screenshot of list of views with Baseball Players view shown](/sites/default/files/styles/max_800w/public/tutorials/images/exposed-filters--edit-baseball-players.png?itok=ZqGD2mCp)

### Add new filter criteria: debut

Next to the **Filter Criteria** heading, select the *Add* button. This will open a modal window where we can select the field we want to filter our list on.

Select the checkbox next to *Debut (field\_player\_debut)*. Then select the *Add and configure filter criteria* button.

Image

![Screenshot of add new filters modal window open with Debut field selected](/sites/default/files/styles/max_800w/public/tutorials/images/exposed-filters--add-debut-filter.png?itok=q-cUSuZd)

### Explore exposed filter settings

After selecting the field we want to configure as a filter criteria, a new modal window will appear that allows us to configure our new filter. At the top of this new modal window is a checkbox labeled *Expose this filter to visitors, to allow them to change it*.

Image

![Screenshot of filter configuration modal window](/sites/default/files/styles/max_800w/public/tutorials/images/exposed-filters--debut-filter-configuration.png?itok=ofQm5jBo)

Select the checkbox *Expose this filter to visitors, to allow them to change it*. The modal window will refresh its content and display the exposed filter configuration options.

Image

![Screenshot of exposed filter configuration modal window](/sites/default/files/styles/max_800w/public/tutorials/images/exposed-filters--exposed-debut-filter-configuration.png?itok=7Fa_21bX)

#### Exposed filter options

| Setting | Description |
| --- | --- |
| **Label** | A label for the exposed filter field |
| **Description** | Help text for the field |
| **Required** | When checked, visitors must provide a value for this exposed filter before they are able to filter the list of content. |
| **Expose operator** | To give visitors even more control of this view, we can expose the operator for filters. This allows visitors to choose between various methods to compare the filter's value against items in the database. |
| **Placeholder** | This provides a placeholder within the exposed filter's field. Useful for giving the visitor a hint for how they should use the field. |
| **Filter identifier** | This is the name the filter uses to identify the values passed into the filter through the URL. |

### Update Debut exposed filter settings

Let's update the settings of this exposed filter. First, let's change the *Label* to the value of **`Player Debut Date`**.

Next, let's provide a description that tells people how to use this filter. Change the value of the *Description* field to be **`Find players who debuted on or after the entered date.`**

Since many date formats exist, let's use the *Placeholder* field to provide visitors an example of the format we need. Change the value of the *Placeholder* field to be **`YYYY-MM-DD`**. That should help them enter the appropriate format: *year-month-day*.

Change the *Operator* value to be **`Is greater than or equal to`**.

Then select the *Apply* button at the bottom of the modal window.

Image

![Screenshot of Debut exposed filter configuration modal window with values filled in](/sites/default/files/styles/max_800w/public/tutorials/images/exposed-filters--exposed-debut-filter-configured.png?itok=eH5tEeBh)

### Preview and test exposed filter form

Now that we've added and exposed a filter, let's scroll down and preview our view to see how it looks.

Image

![Screenshot of preview section of the view page showing new exposed filter](/sites/default/files/styles/max_800w/public/tutorials/images/exposed-filters--exposed-filter-preview.png?itok=BbqTrKtU)

Here in the preview we can also test the exposed filter.

Change the value of the Player Debut Date field to `2010-06-01` and select the *Apply* button located directly beneath the field. You should see the preview update to show baseball players where the value of their **Debut** field is greater than or equal to `2010-06-01`.

Image

![Screenshot of preview of our new view with exposed filter in use](/sites/default/files/styles/max_800w/public/tutorials/images/exposed-filters--exposed-filter-preview-changed.png?itok=BBu0r0oV)

### Save the view

Select the *Save* button.

Now anyone who visits this view will be able to use our exposed filter to find the list of data they want. You can see the exposed filter in action on the Baseball Players page by visiting the */baseball-players* path.

Image

![Screenshot of Baseball Players page with exposed filter shown](/sites/default/files/styles/max_800w/public/tutorials/images/exposed-filters--exposed-filter-on-page.png?itok=W_fXXcBt)

## Recap

In this tutorial, we learned how to expose filter criteria to our website visitors. Exposed filters allow visitors to filter list of content themselves. With this feature of the Views module, we can build useful lists for our users. We can allow visitors to find a piece of content within a larger list or make complex and powerful dashboards that allow administrators to manage large amounts of data with ease.

## Further your understanding

- Add a new filter criteria to the *Baseball Players* view for the field *Final game*. Expose this new filter and set its *Operator* to **`Is less than or equal to`**. Along with the *Debut* exposed filter we setup in this tutorial, this new filter will allow visitors to search for Baseball Players within a range of dates.
- Update the *Content administration* view that comes with Drupal out of the box (found at */admin/content*). Add exposed filter criteria that will help content administrators find the content they need to access.

## Additional resources

- [Drupal User Guide: Chapter 9. Creating Listings with Views](https://drupalize.me/series/user-guide/views-chapter) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview: Exposed Filter Criteria in Views](/tutorial/overview-exposed-filter-criteria-views?p=2670)

Next
[Overview: Sort Criteria in Views](/tutorial/overview-sort-criteria-views?p=2670)

Clear History

Ask Drupalize.Me AI

close