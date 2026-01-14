---
title: "How to Create a Layout with Configurable Settings in Drupal's Layout Builder"
url: "https://drupalize.me/tutorial/how-create-layout-configurable-settings-drupals-layout-builder?p=3271"
guide: "[[layout-builder]]"
---

# How to Create a Layout with Configurable Settings in Drupal's Layout Builder

## Content

When building a site using Drupal's Layout Builder, it's a good idea to keep the number of layout plugins manageable. In many cases it's better to create a single layout plugin that can be re-used rather than duplicate a layout multiple times to accommodate minor variations. One way to do this is to provide editors with configuration options that will change the output when a layout is used.

For example, imagine you need to provide variations of a 3-column layout where the columns are different widths. You could define a new layout for each variation. Or you could define a single layout with a configuration option that allows a user to choose the column widths. The latter approach reduces code duplication, and makes the codebase easier to maintain.

In this tutorial we'll:

- Learn how to declare advance layout plugins with configurable settings in the Drupal Layout Builder
- Extend the `LayoutDefault` class and create a custom settings form that editors will see when using a layout
- Use the provided configuration values in the layout's Twig template file to modify the layout when it is rendered

By the end of this tutorial you should be able to expose layout-related settings to editors, allowing for more flexibility in custom layout plugins.

## Goal

Create a new 3-column flexible layout with a settings form for column width.

## Prerequisites

- [Define Custom Layouts in a Module or Theme](https://drupalize.me/tutorial/define-custom-layouts-module-or-theme)
- [Adding Asset Libraries to Custom Layouts](https://drupalize.me/tutorial/adding-asset-libraries-custom-layouts)
- [Dynamic Layout Plugins in Drupal's Layout Builder](https://drupalize.me/tutorial/dynamic-layout-plugins-drupals-layout-builder)

## Follow these steps

This assumes that you've followed the steps in [Define Custom Layouts in a Module or Theme](https://drupalize.me/tutorial/define-custom-layouts-module-or-theme), and have a static 3-column custom layout defined in a module. We'll expand that existing layout to have user-configurable column widths.

### Set up an alternate PHP class

By default, all custom layout plugins use the `\Drupal\Core\Layout\LayoutDefault` class provided by core. We can create a new class that extends this one to add a settings form for our custom layout plugin.

Use the `class` property in the *{MODULE\_NAME}.layouts.yml* file to specify the alternate class you want to use.

Example:

```
custom_layouts_threecol_25_50_25:
  label: 'Three column 25/50/25'
  path: templates/layouts
  class: '\Drupal\custom_layouts\Layout\ThreeColumnsLayoutClass'
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

The `class` properties value is the full PSR-4 name of the class you want to use.

### Add a new class

Next, define the new class. The `class` property uses the full class name, and implements the PSR-4 standard. Layout plugins should always be in the `Drupal\{MODULE_NAME}\Layout` namespace.

In this case the `\Drupal\custom\_layouts\Layout\ThreeColumnsLayoutClass` class is in the file *src/Layout/ThreeColumnsLayoutClass.php*.

Since we want to add a custom settings form and rely on the core functionality for the rest, we will extend core's `\Drupal\Core\Layout\LayoutDefault` class and implement `PluginFormInterface`.

The skeleton of your class should look like the following:

```
<?php
namespace Drupal\custom_layouts\Layout;

use Drupal\Core\Form\FormStateInterface;
use Drupal\Core\Layout\LayoutDefault;
use Drupal\Core\Plugin\PluginFormInterface;

/**
 * Alternate class for custom three columns layout.
 */
class ThreeColumnsLayoutClass extends LayoutDefault implements PluginFormInterface {
}
```

[`LayoutDefault`](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Layout!LayoutDefault.php/class/LayoutDefault/) is the class that layout plugins declared in a YAML file use by default when they're instantiated. By adding the `class` key in our plugin declaration we're saying, "Instead of using `LayoutDefault` use this custom class." If your custom class implements [`PluginFormInterface`](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Plugin!PluginFormInterface.php/interface/PluginFormInterface/), there is code in the Layout Builder module that will detect this and then display the provided form in the UI when you're adding a layout to a section through Layout Builder UI. This makes it possible for us to add a settings form.

The folder structure of your module should look like the one below:

```
└── custom_layouts
    ├── custom_layouts.info.yml
    ├── custom_layouts.layouts.yml
    ├── src
    │   └── Layout
    │       └── ThreeColumnsLayoutClass.php
    └── templates
        └── layouts
            └── custom-layouts--threecol-25-50-25.html.twig
```

To add a configuration settings form we need to implement the `buildConfigurationForm`, `validateConfigurationForm`, and `submitConfigurationForm` methods of the `PluginFormInterface` in our custom class. We'll also declare a `defaultConfiguration` method to supply some reasonable defaults for the form.

This assumes you're comfortable defining forms using the [Form API](https://drupalize.me/tutorial/form-api-overview).

### Add default configuration values

The goal of this tutorial is to expose options for the column widths of the custom 3-column layout. We'll define 3 options: *Equal columns*, *25%-50%-25%*, and *50%-25%-25%*. These options will be exposed to the users as a select list.

The first step is to set up default values to use when no configuration is set. For this we'll define a `defaultConfiguration` method and return a default value for the select element.

Add a `defaultConfiguration` method, like the one below, to the `ThreeColumnsLayoutClass` class:

```
/**
  * {@inheritdoc}
  */
public function defaultConfiguration() {
  return parent::defaultConfiguration() + [
    'column_width' => 'equal_columns',
  ];
}
```

### Build the configuration form

In the `ThreeColumnsLayoutClass` class add a `buildConfigurationForm` method that looks like the following:

```
/**
  * {@inheritdoc}
  */
public function buildConfigurationForm(array $form, FormStateInterface $form_state) {
  $form = parent::buildConfigurationForm($form, $form_state);
  $configuration = $this->getConfiguration();
  $form['column_width'] = [
    '#type' => 'select',
    '#title' => $this->t('Choose column width'),
    '#options' => [
      'equal_columns' => $this->t('Equal columns'),
      '25_50_25' => $this->t('25%-50%-25%'),
      '50_25_25' => $this->t('50%-25%-25%'),
    ],
    '#default_value' => $configuration['column_width'],
  ];
  return $form;
}
```

This calls `parent::buildConfigurationform()` to get the base configuration form and then extends it with a select element that contains our 3 options.

Notice that we get a configuration object at the top of the build method and then pass the value to the `#default_value` render array key. We don't need to check if the value is set since we defined it in the `defaultConfiguration()` method.

### Add submit handler

We need to add a submit handler that processes the submitted values and stores them in the plugin configuration.

Add a `submitConfigurationForm` method to the `ThreeColumnsLayoutClass` class:

```
/**
  * {@inheritdoc}
  */
public function submitConfigurationForm(array &$form, FormStateInterface $form_state) {
  $this->configuration['column_width'] = $form_state->getValue('column_width');
  parent::submitConfigurationForm($form, $form_state);
}
```

For our example we can omit the validation handler, since the form consists only of the select element with predefined options and the Form API will handle validation of these for us.

### Use provided configuration in the Twig template

Configuration values are available in the Twig template for the layout plugin as part of the `{{ settings }}` variable. We can update the template for the layout to include CSS classes based on the option selected in the configuration form.

Edit the *templates/layouts/custom-layouts--threecol-25-50-25.html.twig* file, so it looks like the following:

```
{#
/**
 * @file
 * Default theme implementation for a three column layout.
 */
#}

{#
/**
 * The settings variable is provided by the layout plugin, contains all
 * configuration options for the plugin including the ones added through our
 * custom code.
 *
 * The following code uses the column_width configuration to alter the set of
 * classes used in the template and thereby alters the display.
 */
#}
{% if settings.column_width == 'equal_columns' %}
  {%
  set classes = [
    'layout',
    'layout--equal',
  ]
%}
{% elseif settings.column_width == '25_50_25' %}
  {%
    set classes = [
      'layout',
      'layout--threecol-25-50-25',
    ]
  %}
{% else %}
  {%
    set classes = [
      'layout',
      'layout--threecol-50-25-25',
    ]
  %}
{% endif %}
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

    <div {{ region_attributes.third.addClass('layout__region', 'layout__region--third', 'layout__region-sidebar', 'region-small') }} {% if not region_attributes.third %} class="layout__region layout__region--third layout__region-sidebar" {% endif %}>
      {% if content.third %}
          {{ content.third }}
      {% endif %}
    </div>

  </div>

{% endif %}
```

### Test the configuration options

You'll need to [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) so Drupal picks up our updated layout plugin definition.

In the Administrative menu, navigate to the manage layout section of the Basic page content type (admin/structure/types/manage/page/display/default/layout) and press the *Add section* link. Choose our new 3-column layout, and you should see the new configuration form available in the right sidebar.

Image

![Screenshot of the configuration form for the section](../assets/images/three_column_config.png)

Fill in the form and place the section. If you inspect the element in your web browser you should see the layout class corresponding to the option you selected applied to the section container.

## Create preview-aware layout plugins and styles

To see the visual effects in the layout preview, you can create a "preview aware" layout plugin and add a class like `layout-preview` to it. You'll need to implement CSS in your theme that applies width and layout styles based on the class. Alternatively, you can define a CSS library and attach it to the layout template. Learn more about [Adding Libraries to Custom Layouts](https://drupalize.me/tutorial/adding-asset-libraries-custom-layouts).

For example, in a layout plugin that extends `LayoutDefault`:

```
use Drupal\Core\Layout\Attribute\Layout;
use Drupal\Core\Layout\LayoutDefault;
use Drupal\Core\StringTranslation\TranslatableMarkup;

/**
 * An example layout that uses preview mode detection.
 */
#[Layout(
  id: 'preview_aware_layout',
  label: new TranslatableMarkup('Preview-aware layout'),
  regions: [
    "main" => [
      "label" => new TranslatableMarkup("Main Region"),
    ],
  ],
)]
class PreviewAwareLayout extends LayoutDefault {

  /**
   * {@inheritdoc}
   */
  public function build(array $regions) {
    $build = parent::build($regions);

    if ($this->inPreview) {
      $build['main']['#attributes']['class'][] = 'layout-preview';
    }

    return $build;
  }

}
```

*Note:*: The above example was originally taken from this change record: [Block and layout plugins can now determine if they are being rendered in preview mode](https://www.drupal.org/node/3272267).

## Recap

In this tutorial we learned how to define advanced layout plugins that present editors with a settings form. Then we used the provided settings inside the layout's Twig template to modify the layout. This approach allows us to minimize the number of layout plugins we need to create by combining similar layouts together and exposing flexible settings to the editors.

## Further your understanding

- What other settings could you expose to editors?
- How can the core defined settings form be reused inside your custom layouts?

## Additional resources

- [Layout API](https://www.drupal.org/docs/drupal-apis/layout-api) (Drupal.org)
- [How to register layouts documentation](https://www.drupal.org/docs/drupal-apis/layout-api/how-to-register-layouts) (Drupal.org)
- Change record: [Block and layout plugins can now determine if they are being rendered in preview mode](https://www.drupal.org/node/3272267) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Dynamic Layout Plugins in Drupal's Layout Builder](/tutorial/dynamic-layout-plugins-drupals-layout-builder?p=3271)

Next
[Build Dynamic Custom Layouts with Derivatives](/tutorial/build-dynamic-custom-layouts-derivatives?p=3271)

Clear History

Ask Drupalize.Me AI

close