---
title: "Overview: Views API in Drupalfree"
url: "https://drupalize.me/tutorial/overview-views-api-drupal?p=2939"
guide: "[[views-drupal]]"
---

# Overview: Views API in Drupalfree

## Content

The Views module is a query generator and render engine in Drupal core. It's typically used to create and output collections of items such as Drupal content entities. But it can also aggregate users, blocks, log records, and more. The output can be rendered many ways, including as a list, a grid, or an RSS feed. Views is commonly used in Drupal to create pages, blocks and other types of displays.

Through the Views API developers can expose new data to Views, add new configuration options, create new output plugins, field formatters, sort handlers, filter handlers, and more. By creating these customizations as extensions of Views instead of as stand alone queries, or hard-coded lists, you can empower site administrators to mix and match your customizations with the existing feature set in any way they might need.

In this tutorial we'll:

- Get a high level overview of the Views API.
- Discuss the functional parts of the Views API such as hooks, plugins, and data types.
- Learn how to use the Views API in your project.

By the end of this tutorial you'll have a solid understanding of the parts of the Views API and some guidance on which to use for your goals.

## Goal

Introduce the Views API and related concepts to Drupal developers who have site building experience with the Views module in Drupal.

## Prerequisites

- [Creating Listings with Views](https://drupalize.me/series/user-guide/views-chapter) (Drupal User Guide)
- [Views: Create Lists with Drupal](https://drupalize.me/series/views-create-lists-drupal)
- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins)
- [What Are Hooks?](https://drupalize.me/tutorial/what-are-hooks)

## Views API defined

The Views module is developed with maximum flexibility and ease of use in mind. Most of the typical use cases for websites such as generating a list of events, grid of news cards, or page of search results can be accomplished using just Views.

In situations when the options provided by Drupal core and existing contributed modules are not enough, developers can utilize the *Views API* to add their own features. The API consists of a collection of [plugin types](https://drupalize.me/tutorial/what-are-plugins) and [hooks](https://drupalize.me/tutorial/what-are-hooks) exposed by the Views module and described within *views.api.php* file of the Views module in Drupal core. The Views API also covers a views render layer and describes a template naming convention and hierarchy that can be used to create template overrides within a theme.

## Interact with the Views module

Views API allows developers to interact with the Views module in several different ways. One of the easiest ways is by using *hooks*. Some operations in Views can be influenced by hooks. Hooks also are invoked during every step of Views build and render process providing the opportunity for developers to influence the outcome of each step, alter output, or add conditions.

Hooks are also used to expose information to the view and extend or add new data types. In this case developers can use data hooks to provide data to the view.

Views plugins provide a more complex level of interaction with Views code compared to hooks. Plugins govern almost every aspect of Views, including querying, sorting, and filtering, as well as displaying and rendering of different components and a view as a whole. Views API allows for alteration and extension of default plugins, and outlines mechanisms to define custom plugins.

## Views hooks

Views hooks are functions defined in a custom module or theme and typically are used to influence the outcome of a certain stage of a view building, rendering or configuration process.

You implement a Views hook just like any other Drupal hook. We'll cover some specific common use cases in the tutorials in this series.

All Views hooks are defined and outlined in the [*/core/modules/views/views.api.php file*](https://api.drupal.org/api/drupal/core!modules!views!views.api.php/group/views_overview) and are grouped together in the following categories:

### Data hooks

Used to describe (expose), analyze, and alter the data that Views can interact with. These hooks are typically used to make Views aware of custom database tables, fields, and pseudo field properties, or to alter the default data definition for entities, fields and tables provided by another module. One of the most frequently used hooks in this category is `hook_views_data()` which returns an array that describes the structure of database tables and other data fields so that Views knows how to work with them. If you have custom data you want Views to know about you'll use these hooks.

Learn more in:

- [Expose a Custom Database Table to Views](https://drupalize.me/tutorial/expose-custom-database-table-views)
- [Add Relationships Between 2 Tables in Views](https://drupalize.me/tutorial/add-relationships-between-2-tables-views)
- [Expose Custom Entities to Views](https://drupalize.me/tutorial/expose-custom-entities-views)

### Plugin alter hooks

These hooks are used to alter the lists of plugins used by different parts of the Views build and render process. Hooks in this category provide a way for developers to modify plugin properties after they have been declared by other modules.

You'll use these hooks when you want to change something about the way an existing plugin works, or when a specific plugin gets used.

More about Views plugins below.

### Build and render hooks

These hooks influence each step of the build and render process. These hooks allow you to alter the view results, access conditions, arguments, or render output of different elements of the view programmatically. Learn more about the build and render cycle and how these hooks influence it in [Overview: Build and Render Cycles in Views](https://drupalize.me/tutorial/overview-build-and-render-cycles-views).

### Query related hooks

These hooks allow you to manipulate the query that Views will use to retrieve data prior to its execution. The most frequently used hook in this category is `hook_views_query_alter()`. It can be used to add or change conditions, add joins, modify a query's sort and range, and add grouping to the query. Learn more in [Alter the Query Used for a View](https://drupalize.me/tutorial/alter-query-used-view).

See the full list of [Views hooks](https://api.drupal.org/api/drupal/core%21modules%21views%21views.api.php/11.x) on Drupal.org.

## Views plugins

Views plugins are objects that are used to build and render a view. They are based on the Drupal [Plugin API](https://drupalize.me/tutorial/what-are-plugins). They're used primarily in situations where the Views UI needs to allow a site builder to be able to choose from one of many options. For example: What field(s) do I want to display? How should this data get sorted? What format should the output be?

Views plugins fall under different categories. The largest category is *handlers*. Handlers are special plugins that are used to handle different parts of the query process -- filters, sorts, joins, arguments -- and Views render elements such as fields and areas.

Plugins that fall outside the handler category are responsible for access checks, caching, displays (page vs. block vs. REST), wizard options, query objects and styles (table vs. RSS vs. rendered entities).

Frequently, developers declare their custom plugins or extend default ones to handle filtering, sorting and rendering, and to add custom validation rules for arguments and access callbacks.

If your goal is to add a new option to the list of fields, sorts, filters, or other lists of things that a site builder can choose from when constructing a view, chances are you want to create a new plugin. This is also true if you want to modify how one of the existing options works; the plugin system makes it possible to extend an existing plugin and add new features to it.

The full list of possible [Views plugins sub-categories](https://api.drupal.org/api/drupal/core!modules!views!views.api.php/group/views_plugins/) can be found on Drupal.org.

Views plugins tutorials

- [Overview Views Plugins](https://drupalize.me/tutorial/overview-views-plugins)
- [Define a Views Field Handler Plugin](https://drupalize.me/tutorial/define-views-field-handler-plugin)
- [Define a Custom Views Pseudo Field Plugin](https://drupalize.me/tutorial/define-custom-views-pseudo-field-plugin)
- [Define a Custom Views Filter Plugin](https://drupalize.me/tutorial/define-custom-views-filter-plugin)
- [Define a Custom Views Sort Plugin](https://drupalize.me/tutorial/define-custom-views-filter-plugin)
- [Define a Custom Views Area Handler Plugin](https://drupalize.me/tutorial/define-custom-views-area-handler-plugin)
- [Define a Custom Views Access Plugin](https://drupalize.me/tutorial/define-custom-views-access-plugin)
- [Define a Custom Views Style Plugin](https://drupalize.me/tutorial/define-custom-views-style-plugin)

## Views templates

The Views module provides a collection of default templates that are used to handle different options of the output in various levels of granularity of rendered elements. The module defines [theme hook suggestions](https://drupalize.me/tutorial/what-are-template-files) for the template overrides that can be used for naming and [overriding the default template](https://drupalize.me/tutorial/override-template-file) in the custom theme.

The downside of the Views template system is that it doesn't currently show the possible theme hook suggestions when you're using [Twig's debugging output](https://drupalize.me/tutorial/configure-your-environment-theme-development). Instead, you'll only see a single base template listed. This happens because Views template overrides are related to your particular view and display configuration and can't be presented as a generic override suggestion. But with a little work you can figure out the available theme hook suggestions for Views provided templates.

For each view there will be at least 2 template files used: the main wrapper *views-view.html.twig* and the nested one determined by the style used for the output.

Examples include:

- *views-view-unformatted.html.twig* - For the *unformatted rows* style
- *views-view-table.html.twig* - For the *table* style
- *views-view-grid.html.twig* - For the *grid* style
- *views-view-list.html.twig* - For the HTML *ordered list* and *unordered list* styles

This can be made more granular if you chain the name of the view and name of the display to the original template name:

Example: *views-view-unformatted--my-view--my-display.html.twig*

Where `my-view` is the machine name of the view with all `_` characters replaced with a `-`, and `my-display` is the machine name of the particular display with all the `_` characters replaced with a `-`.

Once a custom template suggestion pattern is identified the corresponding file can be placed inside the *templates/* directory of your theme. After [clearing the cache](https://drupalize.me/tutorial/clear-drupals-cache) you should be able to see your new template in use.

Learn more:

- [Overview: Theming Views](https://drupalize.me/tutorial/overview-theming-views)
- [Override a View's Wrapper Template](https://drupalize.me/tutorial/override-views-wrapper-template)

## Recap

The Views API provides ways for developers to interact with the Views module and expand its features. Developers can write code that influences the build and render pipeline of an existing view in order to change things like the query used to select data or the build processes, or to alter the final rendered output via hooks. Developers can also create plugins which provide new options for selecting, filtering, sorting, access control, caching, and all the various elements a site builder might use when constructing a view. Theme developers can override templates to further modify the output generated by Views.

## Further your understanding

- When would you use hooks? When would you define a custom plugin?
- Can you think of examples of features that the core Views module doesn't provide that you might need? How do those features map to the different methods for extending Views listed above?

## Additional resources

- [Views API overview](https://api.drupal.org/api/drupal/core!modules!views!views.api.php/group/views_overview/) (api.drupal.org)
- [List of views hooks](https://api.drupal.org/api/drupal/core%21modules%21views%21views.api.php/11.x) (api.drupal.org)
- [Drupal plugin system overview](https://api.drupal.org/api/drupal/core%21core.api.php/group/plugin_api/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Overview: Build and Render Cycles in Views](/tutorial/overview-build-and-render-cycles-views?p=2939)

Clear History

Ask Drupalize.Me AI

close