---
title: "Define Custom Layouts in a Module or Theme"
url: "https://drupalize.me/tutorial/define-custom-layouts-module-or-theme?p=2653"
guide: "[[layout-builder]]"
order: 9
---

# Define Custom Layouts in a Module or Theme

## Content

Layout Builder module comes with some common layouts that can be used out of the box. The Drupal community has created modules that provide more layout options. However, perhaps your project requires special layouts that cannot be constructed with already existing options. Or you require more precise control over the CSS classes and HTML markup, especially if your website is based on a third-party front-end framework. In these cases you can define custom layouts in a module or theme and make them discoverable by the Layout Builder.

In this tutorial we'll:

- Define a new layout plugin
- Create a corresponding Twig template file for HTML markup
- Use our new layout in the Layout Builder UI

By the end of this tutorial you should know how to define a new layout in code, within a module or a theme.

## Goal

Define a custom 3-column layout in a module and use it within Layout Builder.

## Prerequisites

- [Introduction to Layout Builder](https://drupalize.me/tutorial/introduction-layout-builder)
- [Create a Flexible Layout for a Content Type](https://drupalize.me/tutorial/create-flexible-layout-content-type)

## Getting started

In this tutorial we will work within a custom module, but the process is the same for themes.

We assume you've already defined a custom module and will be adding to that. If not, learn how to [Create an Info File for a Module](https://drupalize.me/tutorial/create-info-file-module?p=2766) and define a new module.

Make sure your module is enabled.

### Define a layout plugin

Once a custom module is enabled, it is time to define our new custom layout. Layouts are defined in a special file named *{MODULE\_NAME}.layouts.yml* where `{MODULE_NAME}` is the machine name of your module or theme. This file lives in the root of your project, alongside the *.info.yml* file. This file is used by the *Layout Discovery* module and ensures Drupal can find your layouts.

Layouts are [plugins](https://drupalize.me/tutorial/what-are-plugins) of the type *layout*. Understanding how plugins are [defined](https://drupalize.me/tutorial/plugin-managers) and [discovered](https://drupalize.me/tutorial/plugin-discovery) will help when creating layouts.

In our example we've got a module named `custom_module`, and in the *custom\_layouts.layouts.yml* file we create our first layout definition. For this tutorial we will create a custom 3-column layout with 25% - 50% - 25% columns. The contents of the file should be something like the following:

```
custom_layouts_threecol_25_50_25:
  label: 'Three column 25/50/25'
  path: templates/layouts
  template: custom-layouts--threecol-25-50-25
  category: 'Columns: 3'
  default_region: second
  icon_map:
    - [first, second, third]
  regions:
    first:
      label: First
    second:
      label: Second
    third:
      label: Third
```

The outer key in the file is the unique machine name of the layout *custom\_layouts\_threecol\_25\_50\_25*. It contains the following properties:

- **label**: (required) The human-readable name that will be visible in the Layout Builder UI.
- **path**: The path to the templates folder where the template for this particular layout is stored, relative to the module's root directory.
- **template**: (required) The name of the template for the layout. Notice that it doesn't have an *.html.twig* extension.
- **category**: (required) The category of this layout section within the Layout Builder UI.
- **default\_region**: Identifies the default region for this layout and specifies its machine readable name. In our case it's the middle column.
- **icon\_map**: Used for generation of the icon inside the Layout Builder interface.
- **regions**: (required) Regions (subsections) of the layout. The keys are used as machine names for the regions, and each one contains an entry for a human readable label for the region that gets used in the Layout Builder UI.

For a complete list of properties see the [full annotation reference](https://www.drupal.org/docs/drupal-apis/layout-api/how-to-register-layouts#full-annotation-reference).

You can define any number of custom layouts in the same *.layouts.yml* file.

### Create a template for your layout's HTML markup

All layouts need to have a corresponding template (or theme hook) that provides the HTML markup.

Following the path that we declared in the annotation, let's create a *templates/layouts/* directory in the root of our module. Then create a new Twig template file using the name defined in the annotation, *custom-layouts--threecol-25-50-25.html.twig* in the directory. Your folder structure should be something like this:

```
modules
└── custom
    └── custom_layouts
        ├── custom_layouts.info.yml
        ├── custom_layouts.layouts.yml
        └── templates
            └── layouts
                └── custom-layouts--threecol-25-50-25.html.twig
```

Inside the template file define the markup layout, and render the provided variables.

Example:

```
{#
/**
 * @file
 *
 * This template provides a three column 25%-50%-25% display layout, with
 * additional areas for the top and the bottom.
 *
 * Available variables:
 * - content: The content for this layout.
 * - attributes: HTML attributes for the layout <div>.
 *
 * @ingroup themeable
 */
#}
{%
  set classes = [
    'layout',
    'layout--threecol-25-50-25',
  ]
%}
{% if content|render|trim %}
  <div{{ attributes.addClass(classes) }}>

    <div {{ region_attributes.first.addClass('layout__region', 'layout__region--first', 'layout__region-sidebar', 'region-small') }} {% if not region_attributes.first %} class="layout__region layout__region--first layout__region-sidebar region-small" {% endif %}>
      {% if content.first %}
        {{ content.first }}
      {% endif %}
    </div>

    <div {{ region_attributes.second.addClass('layout__region', 'layout__region--second', 'layout__region-main', 'region-medium') }} {% if not region_attributes.second %} class="layout__region layout__region--second layout__region-main region-medium" {% endif %}>
      {% if content.second %}
        {{ content.second }}
      {% endif %}
    </div>

    <div {{ region_attributes.third.addClass('layout__region', 'layout__region--third', 'layout__region-sidebar', 'region-small') }} {% if not region_attributes.third %} class="layout__region layout__region--third layout__region-sidebar region-small" {% endif %}>
      {% if content.third %}
        {{ content.third }}
      {% endif %}
    </div>

  </div>
{% endif %}
```

In the template you should render `{{ content.region_name }}`, where `region_name` is the machine name of each of the regions that we identified in the annotation.

Also important to note are `{{ attributes }}` and `{{ region_attributes }}` variables. Without these properties added to the region wrapper, regions inside your custom layout will not support drag and drop functionality. If you are new to Twig you may want to learn more about how to [work with attributes](https://drupalize.me/tutorial/classes-and-attributes-twig-templates) in Twig templates.

There are a couple other notable expressions used in the template above. `{% if content|render|trim %}` is used to pre-render the `content` variable. This allows us to check if the `content` variable has children and avoid printing empty wrappers.

Additionally, pre-rendering of the main `content` variable makes it possible to do checks on the individual regions later on like `{% if content.first %}`. Calling `{% if content.first %}` without pre-rendering will always pass, as it always has an array in it. This array resolves the condition to be true even if all that it renders to is an empty string.

**Note:** You'll likely want to add CSS for your layout. To do this, [define an asset library](https://drupalize.me/tutorial/define-asset-library). Then [attach the library](https://drupalize.me/tutorial/attach-asset-library) using the Twig `attach_library` function.

### Use the new layout

In order for the layout to appear in the Layout Builder UI we need to [clear Drupal's cache](https://drupalize.me/tutorial/clear-drupals-cache). Then navigate to the content type for which you have Layout Builder enabled. In our example it's *Basic page* (*admin/structure/types/manage/page/display/default/layout)*. If you don't have Layout Builder enabled for any of the content types and need a refresher you can learn how to do this in [Create a Flexible Layout for a Content Type](https://drupalize.me/tutorial/create-flexible-layout-content-type).

In the layout management section for the content type select the *+Add section* link. You should see our new layout in the sidebar.

Image

![Screenshot of the new layout section in the UI](../assets/images/new_three_column.png)

Choose the new section. Add a name *New section* and save. Now you should see your new section in the layout of the content type. One thing you'll notice is that all 3 columns are currently rendered one on top of another and don't have different widths applied to them. This is because you will need to add CSS to achieve the desired layout.

Image

![Screenshot of the new layout section placed](../assets/images/three_column_rendered.png)

## Recap

In this tutorial we learned how to define a custom layout in a module or theme. We created a new custom 3-column layout, defined the corresponding Twig template file, and used the new layout in the Layout Builder UI.

## Further your understanding

- Can you think of scenarios when your project would benefit from custom layouts?
- Where would you prefer to define layouts -- in a module or in the theme? Why?

## Additional resources

- [Layout API](https://www.drupal.org/docs/drupal-apis/layout-api) (Drupal.org)
- [How to register layouts documentation](https://www.drupal.org/docs/drupal-apis/layout-api/how-to-register-layouts) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Use Layout Builder Modal When Creating Custom Blocks](/tutorial/use-layout-builder-modal-when-creating-custom-blocks?p=2653)

Next
[Comparison of Layout-Building Approaches in Drupal](/tutorial/comparison-layout-building-approaches-drupal?p=2653)

Clear History

Ask Drupalize.Me AI

close