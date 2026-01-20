---
title: "Overview: Views Pluginsfree"
url: "https://drupalize.me/tutorial/overview-views-plugins?p=2939"
guide: "[[views-drupal]]"
order: 25
---

# Overview: Views Pluginsfree

## Content

The Drupal core Views module architecture is built on top of the [Drupal Plugin API](https://drupalize.me/tutorial/what-are-plugins). This allows site administrators to pick and choose from a list of options (plugins) to handle all the different parts of a view -- including what to display, what style to display it in, how to order the results, who has access, and more. In the Views UI, any time you're presented with the option to choose something from a list of options you're likely dealing with some type of plugin.

The advantage of a plugin-based design is that all functional parts of the Views module are provided in an extensible object-oriented way. The Views module defines the basic framework, and provides interfaces for other modules to implement, extend, and customize via plugins. Customizations to filters, fields, area handlers, sorts, and relationship handlers start with plugins.

In this tutorial we'll:

- Learn about Views plugins and the role they play
- Explore the different plugin types and their underlying classes
- Get a high level overview of the steps for creating a custom Views plugin

By the end of this tutorial you'll have a solid understanding of the different Views plugin types, what they are used for, and where to start if you'd like to define your own.

## Goal

Introduce Views plugins in Drupal, their types, and underlying classes.

## Prerequisites

- [Overview: Build and Render Cycles in Views](https://drupalize.me/tutorial/overview-build-and-render-cycles-views)

## Views plugin types

All Views plugins can be divided into 2 major categories: *plugins* and *handlers*.

- Handlers are plugins that participate in the build process of the Views query object. They are responsible for filtering, contextual filtering, sorting, and relationships.
- Other plugins are responsible for the wizard build process, row styles, display styles, pagers, caching, access control, and more.

## Handlers

The following is a list of the different types of handlers, and information about how each handler type is used. The Views module provides handler plugins for common scenarios. It's worth taking the time to learn what handlers already exist before writing your own. if you are defining a custom handler, you can often extend an existing one rather than starting from scratch.

### Area handlers

Area handlers are plugins that are responsible for handling *areas* of the view like header, footer, and empty text. You can explore the full list of [area handlers](https://api.drupal.org/api/drupal/core%21modules%21views%21src%21Plugin%21views%21area%21AreaPluginBase.php/group/views_area_handlers/) in the official documentation. A real life example of a custom area handler would be a reusable back link that can be displayed at the top of the view. The user can specify the link and its title via configuration rather than having to code an HTML `a` tag.

### Argument handlers

Argument handlers are plugins that help to handle arguments passed to the view in the form of *contextual filters*. You can explore the full list of [argument handlers](https://api.drupal.org/api/drupal/core%21modules%21views%21src%21Plugin%21views%21argument%21ArgumentPluginBase.php/group/views_argument_handlers/) in the official documentation. In real life these are mostly used to map pretty URLs like `/view-path/today` for some machine or system values like a relative timestamp, taxonomy term ids, or other contextual values.

### Field handlers

Field handlers are plugins that handle the retrieving and displaying of data in the *Fields* section of the view. You can explore the full list of [field handlers](https://api.drupal.org/api/drupal/core%21modules%21views%21src%21Plugin%21views%21field%21FieldPluginBase.php/group/views_field_handlers/) in the official documentation. Custom field handlers are used to override or extend default field handler behaviors, or to handle computed fields in the view. For example, providing Views with the ability to display a set of points on a map. These are similar to field formatters for the Field API.

### Filter handlers

Filter handlers are plugins that are responsible for limiting the items in a view by adding conditions to the query object. You can explore the full list of [filter handlers](https://api.drupal.org/api/drupal/core%21modules%21views%21src%21Plugin%21views%21filter%21FilterPluginBase.php/group/views_filter_handlers/) in the official documentation. The most common use case for extending this handler type would be to define a custom date filter, or an entity reference exposed filter that has more knowledge about your specific data model.

### Join handlers

Join handlers are plugins that perform joins in the query object. Standard join is the most popular one; its behavior can be customized by the configuration object passed into it. You can explore the full list of [join handlers](https://api.drupal.org/api/drupal/core%21modules%21views%21src%21Plugin%21views%21join%21JoinPluginBase.php/group/views_join_handlers/) in the official documentation.

### Relationship handlers

Relationship handlers are plugins that manage the relationships between different entities in a view. You can explore the full list of [relationship handlers](https://api.drupal.org/api/drupal/core%21modules%21views%21src%21Plugin%21views%21relationship%21RelationshipPluginBase.php/group/views_relationship_handlers/) in the official documentation. Custom relationship handlers are typically used to expose complex connections between entities that are more than one level deep.

### Sort handlers

Sort handlers are plugins that affect the `ORDER BY` clause of the query object and appear in the *Sort* section of the View's UI. You can explore the full list of [sort handlers](https://api.drupal.org/api/drupal/core%21modules%21views%21src%21Plugin%21views%21sort%21SortPluginBase.php/group/views_sort_handlers/) in the official documentation. Custom sort plugins are common and mostly used to provide sorting functionality based on complicated calculations. One real life example would be sorting by Title alphabetically with the exclusion of articles. For example, excluding the word *the* in *The Empire State Building* so that it would appear under "E" in an alphabetical list.

## Plugins

Non-handler plugins are responsible for the various parts of the Views object itself instead of the query object that Views uses to retrieve results.

### Access plugins

Access plugins check, and control, access to the Views object. You can explore the full list of [access plugins](https://api.drupal.org/api/drupal/core%21modules%21views%21src%21Plugin%21views%21access%21AccessPluginBase.php/group/views_access_plugins/) in the official documentation. A real life example is a custom access check that cannot be described by a user's permissions or roles. For example: only grant access if today is the current user's birthday.

### Argument default plugins

Argument default plugins work closely with *Argument handlers*, but their only responsibility is providing default values for contextual filters. This is specifically useful for Views displays that don't retain the context of their current position on the site. You can explore the full list of [argument default plugins](https://api.drupal.org/api/drupal/core%21modules%21views%21src%21Plugin%21views%21argument_default%21ArgumentDefaultPluginBase.php/group/views_argument_default_plugins/) in the official documentation. An example of a custom argument default plugin would be setting a default value based on a contextual condition. For example, if the node where the block is rendered on has a certain regional taxonomy, pass a default geolocation value to the maps view display.

### Argument validate plugins

Argument validate plugins also work in conjunction with *Argument handlers*. They are responsible for validation of the values that are passed to the contextual filters. They are also often responsible for additional transformation of the values passed through contextual filters. You can explore the full list of [argument validate plugins](https://api.drupal.org/api/drupal/core%21modules%21views%21src%21Plugin%21views%21argument_validator%21ArgumentValidatorPluginBase.php/group/views_argument_validate_plugins/) in the official documentation.

### Cache plugins

Cache plugins are responsible for determining whether Views objects can be cached. You can explore the full list of [cache plugins](https://api.drupal.org/api/drupal/core%21modules%21views%21src%21Plugin%21views%21cache%21CachePluginBase.php/group/views_cache_plugins/) in the official documentation.

### Display plugins and display extender plugins

These handle the overall display of the view and provide additional display options across all display types. You can explore the full list of [display plugins](https://api.drupal.org/api/drupal/core%21modules%21views%21src%21Plugin%21views%21display%21DisplayPluginInterface.php/group/views_display_plugins/) and [display extender plugins](https://api.drupal.org/api/drupal/core%21modules%21views%21src%21Plugin%21views%21display_extender%21DisplayExtenderPluginBase.php/group/views_display_extender_plugins/) in the official documentation. In the Views UI these are the options available when you choose to add a new display (e.g. block) to a view.

### Pager plugins

Pager plugins are responsible for the pagination of the results of the view, starting from the query stage of the build process up to the rendering of the pager. You can explore the full list of [pager plugins](https://api.drupal.org/api/drupal/core%21modules%21views%21src%21Plugin%21views%21pager%21PagerPluginBase.php/group/views_pager_plugins/) in the official documentation. A real life example would be the contributed module [Views Infinite Scroll](https://www.drupal.org/project/views_infinite_scroll) that defines a custom pager plugin and attaches a JavaScript library to provide an *infinite* pager.

### Query plugins

Query plugins transform a Views query object into a query object of the particular database backend. In most cases, it's SQL, but it doesn’t have to be. You can explore the full list of [query plugins](https://api.drupal.org/api/drupal/core%21modules%21views%21src%21Plugin%21views%21query%21QueryPluginBase.php/group/views_query_plugins/) in the official documentation. This could be useful if your database backend is different from the ones supported by Drupal core, and you are writing a custom handling functionality for it. Or you could allow Views to query data from a third party API.

### Row plugins

Row plugins are responsible for the rendering of an individual result row. You can explore the full list of [row plugins](https://api.drupal.org/api/drupal/core%21modules%21views%21src%21Plugin%21views%21row%21RowPluginBase.php/group/views_row_plugins/) in the official documentation. Creating a custom row plugin might be useful if you want to display information in a format not currently supported by Views. For example, an object with custom serialization rules.

### Style plugins

Style plugins are responsible for rendering the full collection of results. For example, render rows in a format of a table, grid, or HTML list. For the most part they provide an object wrapper around the theme template file. You can explore the full list of [style plugins](https://api.drupal.org/api/drupal/core!modules!views!src!Plugin!views!style!StylePluginBase.php/group/views_style_plugins/) in the official documentation. It might be useful to define your own if template overrides of one of the provided ones don't fit the requirements. You might also use one to add a new list style like CSV or TSV.

### Wizard plugins

Wizard plugins are used for the screen and set of options that you see when you first start building a new view. You can explore the full list of [wizard plugins](https://api.drupal.org/api/drupal/core%21modules%21views%21src%21Plugin%21views%21wizard%21WizardPluginBase.php/group/views_wizard_plugins/) in the official documentation. You might create a new wizard plugin if your site's administrators are creating a lot of views with a very similar configuration, and you want to provide a simpler UI to get them started.

## Defining a plugin

Views plugins work like any other Drupal plugin. So it's a good idea to make sure you're familiar with [the Plugin API](https://drupalize.me/tutorial/what-are-plugins) first.

Each type of plugin slightly differs in implementation, but there are certain common steps that need to be taken in order for the plugin to be recognized by the Drupal Plugin API and Views.

The plugin typically needs to extend the base class for its type. For instance, custom *Style* plugins will need to extend the `\Drupal\views\Plugin\views\style\StylePluginBase` class provided by the Views module -- unless you'd like to write everything from scratch and not take advantage of what has already been defined in the Views framework.

Next, your plugin class needs to be in a certain PSR-4 namespace. The namespace typically follows the pattern `Plugin\views\[machine_name_of_base_class]`. For example, for the *Style* plugin it will be `Plugin\views\style`.

Lastly, every plugin class needs associated [PHP attributes](https://drupalize.me/tutorial/php-attributes) with the corresponding metadata.

You can learn more about the basics of implementing plugins in [Implement a Plugin Using PHP Attributes](https://drupalize.me/tutorial/implement-plugin-using-php-attributes).

## Recap

In this tutorial we explored the different plugin types provided by the Views module. We learned about the difference between handler and non-handler plugins. We defined the responsibilities of each plugin type to help determine which type(s) you'll need to implement for your specific requirements.

## Further your understanding

- Wizard plugins are rarely extended in real life. Why do you think this is the case? What use case could you think of that would require you to extend the wizard plugin?
- What's the difference between the 3 argument plugin types described above? Why is one of them considered a handler and the 2 others are not?

## Additional resources

- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins) (Drupalize.me)
- [Views plugins](https://api.drupal.org/api/drupal/core!modules!views!views.api.php/group/views_plugins) (api.drupal.org)
- [Plugin API](https://api.drupal.org/api/drupal/core%21core.api.php/group/plugin_api/) (api.drupal.org)
- [Plugins (Plugin API)](https://drupalize.me/topic/plugins) (Drupalize.me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Expose Custom Entities to Views](/tutorial/expose-custom-entities-views?p=2939)

Next
[Define a Views Field Handler Plugin](/tutorial/define-views-field-handler-plugin?p=2939)

Clear History

Ask Drupalize.Me AI

close