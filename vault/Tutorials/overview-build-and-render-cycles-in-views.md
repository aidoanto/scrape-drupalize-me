---
title: "Overview: Build and Render Cycles in Views"
url: "https://drupalize.me/tutorial/overview-build-and-render-cycles-views?p=2939"
guide: "[[views-drupal]]"
---

# Overview: Build and Render Cycles in Views

## Content

In the process of displaying the content of a view to an end user, every view goes through a common build cycle. As a developer it helps to understand the build and render cycle that a view goes through and how you can use it to alter the final result. It helps to know where things are in the cycle when your code is executed, and how that impacts what your code can and can't do. The Views module exposes hooks -- documented in *[views.api.php](https://api.drupal.org/api/drupal/core%21modules%21views%21views.api.php/11.x)* -- that allow developers to influence every step of the cycle. This includes altering the database query that gets executed, changing the configuration of filters, computing things based on raw results, and changing the rendered output of any field.

In this tutorial we'll:

- Learn the steps of the Views build and render cycle.
- Identify the hooks invoked during each step and provide examples of what types of things you might do with each hook.

By the end of this tutorial you should be able to list the hooks invoked by Views, when they get called during the build and render cycle, and explain the impact this has.

## Goal

Learn about Views hooks, when they are called, and how they can help to meet custom requirements for views in your projects.

## Prerequisites

- [What Are Hooks?](https://drupalize.me/tutorial/what-are-hooks)
- [Discover Existing Hooks](https://drupalize.me/tutorial/discover-existing-hooks)

## The stages of a view

Each View transitions through the following stages during the process of generating the HTML output that a user sees on the page.

1. Pre-view
2. Build
3. Execution
4. Rendering

We'll explain each of these in more depth below.

For the purpose of this tutorial, we'll use the content administration view at *admin/content* as an example. The process is the same for any view.

## Pre-view stage

Views processing starts with the *pre-view* stage. At this stage, the Views object is just about to be processed, so it's a good time to add new arguments to the arguments array or switch the active display.

Each Views instance (or Views display) represents a `ViewsExecutable` object (`\Drupal\views\ViewExecutable`). This object contains all the data for the view, plus the member functions to build and execute the query and to output the result.

During the *pre-view* state:

- Views invokes [`hook_views_pre_view()`](https://api.drupal.org/api/drupal/core!modules!views!views.api.php/function/hook_views_pre_view/).
- `hook_views_pre_view()` receives the `ViewsExecutable` object being processed, the `$display_id` of the active display, and an array of arguments passed into the view.

In the content administration view, for example, this includes a `ViewsExecutable` object with the current display set to `page_1` (unless you renamed the default display for this view on your site).

The `hook_views_pre_view()` provides an opportunity to **modify values of contextual filters based on dynamic conditions defined in your custom module**. For example, your custom code may:

- Load values from temporary storage or application state
- Evaluate additional permissions based on the current user
- Pass a custom value based on the database query or other custom calculations

Setting these values early on ensures that they're taken into account during the remaining processing steps.

For example, the content administration view's access control configuration includes the permission *Access the Content overview page* which is open for all editors on your site. Maybe some junior editors should only have access to items they created, and you built a special trimmed-down version of the content view for them. Instead of creating a different role to hide the main content view, you can check if they have access to the main content administration view based on the job title field of their account.

## Build stage

During the build stage, the `ViewsExecutable` object is being used to define the query that will be used to retrieve records from the database (or whatever storage the view is associated with). At the beginning of this stage, the query isn't built yet but displays are already attached. By the end of this stage, the dynamic query object is complete and is ready to be executed.

During this stage, the configuration of our admin content view is being used to construct a dynamic query object. The specific display (`page_1`) has already been set. Different displays might have different fields or filters, and we need to know this to start building the query. In this specific example, the view is set to query the `node_field_data` table and add all the required MySQL `JOINS` and `WHERE` conditions based on the fields selected for the `page_1` display of the content view being assembled.

This stage invokes the following hooks, in this order:

1. [`hook_views_pre_build()`](https://api.drupal.org/api/drupal/core!modules!views!views.api.php/function/hook_views_pre_build/): Called when the view has displays attached, but prior to the query object being built. This hook is useful if we want to **alter the list of attached displays**.
2. [`hook_views_query_alter()`](https://api.drupal.org/api/drupal/core!modules!views!views.api.php/function/hook_views_query_alter/): Called after the dynamic query object is initially built. This is one of the most commonly used Views API hooks. It allows developers to **manipulate the dynamic query object prior to it being executed**. Use this to change query conditions, modify sorts, add grouping, and anything else that requires changing the query used to retrieve the list of items the view will display.
3. [`hook_views_query_substitutions()`](https://api.drupal.org/api/drupal/core!modules!views!views.api.php/function/hook_views_query_substitutions/): This hook allows you to **replace special strings in the query before it's executed**. Sometimes instead of hard coding a value into the query, dynamic tokens are used. These can be substituted at run-time while still allowing the work of building the query object to be cached. The most common example is to swap the language id placeholder for an actual value. In this hook, it's possible to load the language object, get its id and swap the value of the `***LANGUAGE_language_content***` key with the new language id. Another example is inserting the ID of the currently active user in a view that displays *all posts by the current user*.
4. [`hook_views_post_build()`](https://api.drupal.org/api/drupal/core!modules!views!views.api.php/function/hook_views_post_build/): This hook is executed **after the query object is built, but before the query has been executed**.

## Execution stage

The *execution* stage of the build cycle is responsible for serializing the query object into a query that can be run against the data store, executing the query, and then building an array from the results.

This stage invokes the following hooks, in this order:

1. [`hook_views_pre_execute()`](https://api.drupal.org/api/drupal/core!modules!views!views.api.php/function/hook_views_pre_execute/): This hook allows you to act on the view **after the query is built, but prior to the query being executed**. You should **not** modify the query here (use `hook_views_query_alter()`). You can assume that the query is in its final state and use this to do things like *inspect* the query that's going to be executed and output diagnostics information, such as, "This view contains N joins and might be slow to execute."
2. [`hook_views_post_execute()`](https://api.drupal.org/api/drupal/core!modules!views!views.api.php/function/hook_views_post_execute/): At this point, the query has been run against the data store and the results have been collected, but not yet processed by the various configured handlers. You might use this hook to do something like provide information about the number of results, or to perform logic that requires the raw data obtained from the database, prior to formatting.

## Render stage

After the query is executed, Views starts the render stage where the items returned by the query are processed by their respective handlers and the relevant HTML output is generated. This stage is divided into 2 stages: *pre-render* and *post-render*, with the following corresponding hooks:

1. [`hook_views_pre_render()`](https://api.drupal.org/api/drupal/core!modules!views!views.api.php/function/hook_views_pre_render/): Called **after results have been processed by handlers, and before being rendered**. At this point, the raw results for each individual field have been transformed into [Render API compatible arrays](https://drupalize.me/tutorial/what-are-render-arrays). This hook, unlike previously discussed ones, can be called by a custom module or a theme. It provides an opportunity to alter values of the result items prior to rendering, since it might be easier to manipulate them as arrays and objects versus manipulating rendered markup. In the case of *admin/content* view, which displays as a `<table>`, we don't have the Render array for the table itself, but we have created Render arrays for the values that will be inserted into the cells of the table.
2. [`hook_views_post_render()`](https://api.drupal.org/api/drupal/core!modules!views!views.api.php/function/hook_views_pre_render/): At this point, the **render arrays for each field are rendered and the results are converted into `#markup` objects**. This hook is typically used to perform alterations to the view's cache parameters, alter markup for the header and footer areas, or perform any other manipulations with the results that relied on the rendered markup.

Finally, the rendered results are wrapped into a `<table>` or markup for the selected display style, and returned to Drupal to be displayed.

## Recap

In this tutorial, we learned that when a view is being displayed it goes through a common build cycle, and that each step of the cycle invokes hooks that a developer can use to influence the end result. Different hooks are suited for different purposes. Depending on where in the cycle they are invoked, it may be either too early or too late to perform certain types of alterations. Knowing the order in which the hooks are invoked, as well as understanding the stages of the Views cycle, helps ensure we can achieve our output goals.

## Further your understanding

- What hook would be best to use if you'd like to alter the image style used when displaying an image field?
- What hook(s) can be implemented in a theme? And which can only be implemented in a module? Why?
- What is the difference between post-execute and pre-render hooks?

## Additional resources

- [Implement Any Hook](https://drupalize.me/tutorial/implement-any-hook) (Drupalize.Me)
- [List of views hooks](https://api.drupal.org/api/drupal/core%21modules%21views%21views.api.php/11.x) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview: Views API in Drupal](/tutorial/overview-views-api-drupal?p=2939)

Next
[Alter a View before It's Rendered](/tutorial/alter-view-its-rendered?p=2939)

Clear History

Ask Drupalize.Me AI

close