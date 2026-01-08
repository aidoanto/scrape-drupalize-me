---
title: "Create a Page with a Contextual Filter"
url: "https://drupalize.me/tutorial/create-page-contextual-filter?p=2670"
guide: "[[views-drupal]]"
---

# Create a Page with a Contextual Filter

## Content

In this tutorial, we'll add and configure a contextual filter for a view. Our *Baseball Awards* **content type** has a field *Year*. We'll make it possible for a page to be dynamically created on our site that contains the year and lists the awards for that specific year. To do this, we'll add a contextual filter to the *Baseball Awards* **view** that will allow visitors to filter the list of awards by the award year. We'll also add a block using the summary view contextual filter configuration, which visitors can use to view results for specific years.

## Goal

Add a "year" contextual filter to the *Baseball Awards* view and a block populated with links to allow users to quickly filter the view by year.

## Prerequisites

- [Overview: Contextual Filters in Views](https://drupalize.me/tutorial/overview-contextual-filters-views)

Examples and screenshots in this tutorial are from the demo site we set up in:

- [Set up Demo Site with Views and Content](https://drupalize.me/tutorial/set-demo-site-views-and-content)

If you are new to Views, check out these Drupal User Guide tutorials:

- [Concept: Uses of Views](https://drupalize.me/tutorial/user-guide/views-concept)
- [Concept: The Parts of a View](https://drupalize.me/tutorial/user-guide/views-parts)

## Watch: Create a Page with a Contextual Filter

Sprout Video

## Add a contextual filter

In the following steps, we'll add a contextual filter to the *Baseball Awards* view for the field *Year*.

### Go to Views

From the administrative menu, navigate to *Structure* > *Views* (*admin/structure/views*).

Tip: The **Advanced** section in the Views UI (where the contextual filters live) will collapse again each time you apply settings. To keep it expanded, access the *Settings* tab on the main Views page, then check **Always show advanced display settings** and select *Save configuration*.

### Edit the *Baseball Awards* view

Locate the *Baseball Awards* view and select the *Edit* button in the *Operations* column.

Image

![Screenshot of list of views with Baseball Awards view shown](/sites/default/files/styles/max_800w/public/tutorials/images/contextual-filters--edit-baseball-awards-view.png?itok=m0gaFtPm)

### Expand the Advanced section

Expand the **Advanced** section by clicking on the column label.

Image

![Screenshot of view edit page with Advanced column open](/sites/default/files/styles/max_800w/public/tutorials/images/contextual-filters--advanced-column.png?itok=HktPVvr8)

### Add a new contextual filter

Next to the **Contextual Filters** heading, select the *Add* button. This will open a modal window that contains a list of available contextual filter criteria.

In the list of filters, locate the filter labeled *Year* for the field *field\_player\_award\_year*. Select the checkbox beside the filter then select the *Add and configure contextual filters* button.

Image

![Screenshot of modal window containing list of available contextual filters with Year field selected](/sites/default/files/styles/max_800w/public/tutorials/images/contextual-filters--year-add-filter.png?itok=H1HBF7Fx)

### Configure the *Year* contextual filter for the page display

1. For *When the filter value is NOT in the URL*, select **`Display all results for the specified field`**.
2. For *When the filter value IS in the URL or a default is provided*, select the checkbox *Override title*.

This will display a new field where we can provide a pattern that represents the new title for our view. Furthermore, a list of available replacement tokens labeled **Replacement patterns** will appear.

### Configure value for *Override title*

In the new text field that appears beneath *Override title*, provide the value **`{{ arguments.field_player_award_year_value }} Baseball Awards`**.

Tip: Expand the **Replacement patterns** section and copy/paste the appropriate token.

### Configure validation criteria

Select the checkbox labeled *Specify validation criteria*.

For the *Validator* field, select the value **`Numeric`**. Since we're dealing with years, we can reliably expect the contextual filter's values to be numerals.

For the *Action to take if filter value does not validate* field, select the value **`Display contents of "No results found"`**. (We'll configure what displays for "No results" next.)

Our contextual filter criterion configuration should now look like this:

Image

![Screenshot of modal window with contextual filter configuration values chosen](/sites/default/files/styles/max_800w/public/tutorials/images/contextual-filters--year-configuration-modal-final.png?itok=ygjLpXQq)

### Configure no results behavior

In the center column, next to **No results behavior**, select the **Add** button. Search for "text area" and select the checkbox next to **Text area**. Select **Add and configure no results behavior**.

In the **Content** text area, enter the text, **`No results found.`**, then select **Apply**.

### Preview and test

We should now have a working contextual filter in our *Page* display. We can see it in action by using the **Preview** section on the view's edit page. Let's scroll to the **Preview** section and take a look.

At the moment, we are previewing the view without a value provided to our new contextual filter. If we examine the list of content, we can see all baseball awards in this data set.

Image

![Screenshot of preview of the view without contextual filter value](/sites/default/files/styles/max_800w/public/tutorials/images/contextual-filters--preview-no-filter.png?itok=E65KC1gW)

Let's use our new contextual filter to limit the list to baseball awards awarded in the year 1901.

At the top of the **Preview** section there is a text field with the label *Preview with contextual filters*. Type the value **`1901`** into that field, then select the *Update preview* button. The preview changes in two important ways:

1. The list of content is now limited (filtered) by the field "Year" and the value `1901`.
2. The title for the view should change to `1901 Baseball Awards`.

Image

![Screenshot of preview of the view with list of content filtered by the year 1901](/sites/default/files/styles/max_800w/public/tutorials/images/contextual-filters--preview-filtered.png?itok=GBuWxP4Q)

### Save the view

We have a few more things to configure, but let's save our working view at this point. Select the *Save* button.

## Display a summary of valid contextual filters for users

At the moment, in order to view the results for any given year, our users would need to enter the year into the correct place in the URL. Remember that the view is using the part of the path after the last slash (`/`) in the URL as a value for the filter. The most straightforward way of ensuring users arrive at the correct URL is to provide a link.

Let's create a block that shows a list of valid links to years that a user can click on to filter the view. The number of results for each year will be in parentheses next to it. This type of block is also known as a *summary view*; because, when we configure the contextual filter, we'll select *Display a summary*.

To create a *summary view* we'll create a new block display with a new contextual filter, configured to "display a summary". After we're done configuring the block, we'll display it on the page for the *Baseball Awards* view.

Image

![Screenshot of a block showing a summary of the results by year](/sites/default/files/styles/max_800w/public/tutorials/images/contextual-filters--summary-block.png?itok=NCjTB25h)

### Add a new block display

Below *Displays*, select the *+Add* button, then *Block* from the dropdown list.

### Edit the contextual filter for the block display

Expand the *Advanced* section in the third column. Select the existing *Year* contextual filter which was inherited from the Page display.

At the top of the modal, under *For*, select **This block (override)**.

#### When the filter is *not* available

- Select *Display a summary*.
- Format: *Unformatted*

For *Base path*, leave blank, since we'll be placing this block on the same page as the page display.

- Select (check): *Display record count with link*
- Select (check): *Display items inline*
- Separator: `|`

Image

![Screenshot of a contextual filter configuration](/sites/default/files/styles/max_800w/public/tutorials/images/contextual-filters--summary-block-config-1.png?itok=kNi9_fi9)

#### When the filter value *is* available or a default is provided

- Select (check): *Specify validation criteria*
- Validator: *Numeric*
- Action to take if filter value does not validate: *Display contents of "No results found"*

All other items, leave with the default values.

Select button *Apply (this display)*.

Image

![Screenshot of a contextual filter configuration](/sites/default/files/styles/max_800w/public/tutorials/images/contextual-filters--summary-block-config-2.png?itok=TTktQVEB)

### Configure the pager in the block display

The *Pager* configuration inherited its values from the *Page* display. We want to override this setting so that all award years will display in the block (without a pager).

In the second column, under **Pager**, next to *Use pager*, select the linked value.

In the modal window at the top, select *For* **`This block (override)`**.

In the list of options, select *Display all items*.

Select the button *Apply (this display)* and in the next modal, leave the default value (0) and select *Apply*.

### Save the view

We'll need to to save the view before configuring the view header on the page display in the next step.

### Add the summary view to the page of results

We can do this either by adding the block display as a header to the page display or by placing the block in a region on the page created by our view.

To keep the configuration all in one place, let's use the first method, adding the block as a header to the page display.

Switch to the *Page* display and in the second column, next to *Header*, select the *Add* button.

Select *For* **`This page (override)`** from the dropdown at the top of the modal window. Use the search or scroll down to find *View area* and select the checkbox next to it. Then, select *Apply (this display)*.

For *View to insert*, choose **View: baseball\_awards - Display: block\_1**. Select *Apply (this display)*.

Image

![Screenshot of header configuration for the page display](/sites/default/files/styles/max_800w/public/tutorials/images/contextual-filters--page-display-header-view.png?itok=uH0VmZwm)

### Save the view and test it out

Before previewing the results, save the view because the links in the summary view will navigate you to the view's page instead of keeping you in the preview area.Select the *Save* button to save the view. In the preview area, select one of the years from the summary view to navigate to the page. Or, using the administrative menu, navigate *Back to site*, then select the *Baseball Awards* menu item.

Image

![Animated gif shows user clicking on the links in the summary view and the results changing by year.](/sites/default/files/styles/max_800w/public/tutorials/images/contextual-filters--end-result-summary-view.gif?itok=9rktOgVX)

## Recap

In this exercise we created a new contextual filter for the Baseball Awards view that allows visitors to filter our list of content by visiting various URLs on our website.

## Further your understanding

- Instead of using a view header to place the summary block, how would you go about placing the summary view block on the Baseball Awards page? (See also [Placing a Block in a Region](https://drupalize.me/tutorial/user-guide/block-place?p=3068).)

## Additional resources

- [Drupal User Guide: Chapter 9. Creating Listings with Views](https://drupalize.me/series/user-guide/views-chapter) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview: Contextual Filters in Views](/tutorial/overview-contextual-filters-views?p=2670)

Next
[Overview: Theming Views](/tutorial/overview-theming-views?p=2670)

Clear History

Ask Drupalize.Me AI

close