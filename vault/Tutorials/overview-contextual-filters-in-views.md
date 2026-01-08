---
title: "Overview: Contextual Filters in Views"
url: "https://drupalize.me/tutorial/overview-contextual-filters-views?p=2670"
guide: "[[views-drupal]]"
---

# Overview: Contextual Filters in Views

## Content

Contextual filters are a Views mechanism for dynamically refining the contents of a view. It might be helpful to think of them as "dynamic filters". In this tutorial, we'll discuss the concept of *context*, look at how to add contextual filters in the Views UI, and review the *Taxonomy term* view that comes with Drupal and how it uses a contextual filter.

## Goal

- Understand what a contextual filter is all about and how and when to use one in Views.

## Prerequisites

Examples and screenshots in this tutorial are from the demo site we set up in:

- [Set up Demo Site with Views and Content](https://drupalize.me/tutorial/set-demo-site-views-and-content)

If you are new to Views, check out these Drupal User Guide tutorials:

- [Concept: Uses of Views](https://drupalize.me/tutorial/user-guide/views-concept)
- [Concept: The Parts of a View](https://drupalize.me/tutorial/user-guide/views-parts)

## What is context (in this context)?

The first thing we want to understand before going forward is the concept of *context*. For the sake of this tutorial, *context* is certain information that the view can access based on the page containing the view or the visitor interacting with the view.

For example, if a view has a block display which appears all Drupal nodes, then the view can make use of the *current node* context. In that case, almost any information about the current node we can use to dynamically change the results of our view. Similarly, a view could make use of the *current user*, and any information about the current user, as contextual input.

## What are contextual filters?

Like exposed filters, contextual filters are a mechanism in Views that we can use to create dynamic lists. The main difference between an exposed filter and a contextual filter is the source of the filter's value.

With exposed filters, the visitor interacting with the view provides the values for the filters by using form fields. With contextual filters, the filter determines its own value dynamically based on some *context* in which the view appears. Most often this context is a node, user, taxonomy term, or other contextual information -- even a date.

## How to use contextual filters in Views

We can add contextual filter criteria to a view the same way we configure other settings in a view. Locate the **Contextual Filter** section the **Advanced** column, and click *Add*.

Image

![Screenshot of contextual filters section within advance column](/sites/default/files/styles/max_800w/public/tutorials/images/contextual-filters--locate-section.png?itok=SNmW0x0Z)

Like other mechanisms, clicking on the button labeled *Add* will open a modal window that contains a list of available contextual filters we can add to our view.

Image

![Screenshot of list of available contextual filters](/sites/default/files/styles/max_800w/public/tutorials/images/contextual-filters--add-modal.png?itok=LKPVdXOE)

After selecting a contextual filter to add to our view, we need to configure it. Due to the dynamic nature of contextual filters, this modal window contains a lot of options.

Image

![Screenshot of contextual filter configuration options](/sites/default/files/styles/max_800w/public/tutorials/images/contextual-filters--configuration-options.png?itok=_s8KKt76)

Let's go over these options and discuss how they might affect our view.

## Contextual filter configuration options

The contextual filter configuration contains 2 main sections:

- When the filter value **is NOT** in the URL
- When the filter value **IS** in the URL or a default is provided

### When the filter value is NOT in the URL

This section allows us to configure how the view should act when a value for our Contextual Filter is not provided to the view. Another way of thinking about this is, "How do we want the view to act by default?"

Image

![Screenshot of filter not available options](/sites/default/files/styles/max_800w/public/tutorials/images/contextual-filters--options-filter-not-provided.png?itok=uty4iQfl)

| Setting | Description |
| --- | --- |
| **Display all results for the specified field** | When selected, this option makes it so that the list of content is not filtered at all by this contextual filter. |
| **Provide default value** | This option allows us to provide a default value to the contextual filter when no other value is provided. |
| **Type** | Options for how to set the default contextual filter value. Often when configuring the default value for a contextual filter we're going to provide a specific fixed value, or we'll configure this option to look at the page URL for a default value. |
| **Show "Page not found"** | This option essentially makes the contextual filter value required. It makes sense to use this when the view has a path (like in a page display) and needs a value in the path in order to show specific results. A 404 "Page not found" error will display if there's no value provided. |
| **Display a summary** | Rather than showing our list of content, the view will appear as a summary of possible values for the chosen contextual filter. There are configuration options available for the summary that allow us to chose the order of summary items shown, along with some simple formatting options. |
| **Display contents of "No results found"** | When selected, this option will cause the contents of the *No Results Behavior* section to appear when no contextual filter value is provided to the view. |
| **Display "Access Denied"** | Displays a 403 "Access Denied" error for the view when no contextual filter value is provided. |

### When the filter value IS in the URL or a default is provided

This section allows us to configure how the contextual filter works when a value is provided. For example, we can validate the contextual filter value, or alter the title for the view.

Image

![Screenshot of filter provided options](/sites/default/files/styles/max_800w/public/tutorials/images/contextual-filters--options-filter-provided.png?itok=5BNHSODy)

| Setting | Description |
| --- | --- |
| **Override title** | This option allows us to dynamically change the *Title* for the view using the tokens available from the *Replacement Patterns* section. |
| **Specify validation criteria** | With validation criteria we can configure the contextual filter to verify that the value provided meets certain expectations. Validating our filter values is a very useful and powerful option. We should use this option when possible. |
| **Validator** | The mechanism by which we should validate our contextual filter value. |
| **Action to take if filter value does not validate** | Configure how the view should act when a provided contextual filter value does not pass validation. |

## Contextual filter values in the page path

When we configure contextual filters on our view that has a page display, we can configure the *Path* setting to expect the contextual filter value. We do this by adding the percentage symbol `%` as a dynamic placeholder in the page path where we want the contextual filter value to appear.

Let's look at the path and contextual filters for the *Taxonomy term* view that comes with Drupal (*admin/structure/views/view/taxonomy\_term*). There are two parts of this worth noting:

1. The view has one contextual filter configured: *Content: Has taxonomy term ID*
2. The path has one percentage symbol in it at the end: *taxonomy/term/%*

Image

![Screenshot of page path option](/sites/default/files/styles/max_800w/public/tutorials/images/contextual-filters--path-argument.png?itok=wmeATnFt)

Configured this way, the contextual filter will attempt to find its value by looking at the third part of the path where the view is shown. For example, if we visit the path *taxonomy/term/123* on our site, the view will be filtered to show content that has the taxonomy term ID `123`.

We can configure a page display to expect more than one contextual filter value in its path settings by providing multiple percentage symbols separated by `/`.

## Preview contextual filter values

When working on a view with contextual filters we can use the preview area to test that our filters are working as expected. At the top of the **Preview** section of the view edit form, there is a field labeled *Preview with contextual filters*. We can provide values to our contextual filters using this field.

Image

![Screenshot of preview form](/sites/default/files/styles/max_800w/public/tutorials/images/contextual-filters--preview-form.png?itok=Knj7jeS5)

## Recap

Like exposed filters, contextual filters are a mechanism in Views that we can use to create dynamic lists. The main difference between an exposed filter and a contextual filter is the source of the filter's value.

## Further your understanding

- Examine the *Taxonomy term* view that comes with Drupal out of the box (*admin/structure/views/view/taxonomy\_term*). Look at how its contextual filter is configured. Look at how the *Path* is configured.
- Attempt to duplicate the *Taxonomy term* view from scratch.

## Additional resources

- [Drupal User Guide: Chapter 9. Creating Listings with Views](https://drupalize.me/series/user-guide/views-chapter) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add a Relationship to a View](/tutorial/add-relationship-view?p=2670)

Next
[Create a Page with a Contextual Filter](/tutorial/create-page-contextual-filter?p=2670)

Clear History

Ask Drupalize.Me AI

close