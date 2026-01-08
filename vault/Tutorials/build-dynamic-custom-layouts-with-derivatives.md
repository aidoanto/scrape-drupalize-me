---
title: "Build Dynamic Custom Layouts with Derivatives"
url: "https://drupalize.me/tutorial/build-dynamic-custom-layouts-derivatives?p=3271"
guide: "[[layout-builder]]"
---

# Build Dynamic Custom Layouts with Derivatives

## Content

Layout plugins can be dynamically generated based on configuration using plugin derivatives. This allows developers to provide Drupal site administrators with a UI for creating new layout plugins, or to automatically register layout plugins based on the environment.

This is useful in situations where it's not enough to define a set of pre-configured layouts to use in the Layout Builder. Instead, you need to empower editors to declare their own new layout plugins without writing any code. Derivatives could also be used in scenarios where the layouts that should be made available depend on configuration set elsewhere in the module. Or, you might have a scenario where you want to have multiple different 2-column layouts, and for those layouts to have different names, so that they can be themed differently depending on which one is used.

In this tutorial we'll:

- Create a user interface that allows editors to dynamically define layouts via configuration.
- Learn how to set up a plugin deriver that creates layout plugins based on configuration.
- Create custom dynamic layout plugins with variable numbers of columns.

By the end of this tutorial you'll know how to declare dynamic custom layout plugins using derivatives.

## Goal

Create an interface for editors that allows them to define new dynamic layouts and specify the number of columns available.

## Prerequisites

- [Plugin Derivatives](https://drupalize.me/tutorial/plugin-derivatives)
- [Define Custom Layouts in a Module or Theme](https://drupalize.me/tutorial/define-custom-layouts-module-or-theme)
- [Flexible and dynamic custom layouts](https://drupalize.me/tutorial/dynamic-layout-plugins-drupals-layout-builder)

## Define layouts using plugin derivatives

In this tutorial we assume that you have a custom module named *custom\_layouts* that will contain the code you write.

### Set up a configuration form

Start by creating a configuration form. This form should have elements that are included in layout plugin's YAML annotation: `label` and `category`. Add any additional parameters, like the number of columns in this case, that the deriver class will pass along as configuration to plugin instances.

For this tutorial we will include a select list with the options: *Two columns*, *Three columns*, *Four columns*.

In the module we need to create a configuration form that will extend core's *ConfigFormBase*. This form class needs to follow PSR-4 format and be located at the */src/Form* path of your custom module. Create this folder structure and add a class *LayoutConfigurationForm* there.

Your folder structure should look something like the following:

```
└── custom_layouts
    ├── custom_layouts.info.yml
    ├── custom_layouts.layouts.yml
    ├── src
    │      └── Form
    │              └── LayoutConfigurationForm.php
    └── templates
            └── layouts
                    └── custom-layouts--threecol-25-50-25.html.twig
```

And your configuration form class should look something like below:

```
<?php

namespace Drupal\custom_layouts\Form;

use Drupal\Core\Form\ConfigFormBase;
use Drupal\Core\Form\FormStateInterface;

/**
 * Configuration form for dynamic custom layouts.
 */
class LayoutConfigurationForm extends ConfigFormBase {

  /**
   * {@inheritdoc}
   */
  protected function getEditableConfigNames() {
    return ['custom_layouts.settings'];
  }

  /**
   * {@inheritdoc}.
   */
  public function getFormId() {
    return 'custom_layouts_form';
  }

  /**
   * {@inheritdoc}.
   */
  public function buildForm(array $form, FormStateInterface $form_state) {
    $form['layout_label'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Layout label'),
      '#size' => 60,
      '#maxlength' => 512,
      '#required' => TRUE,
    ];
    $form['layout_category'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Layout category'),
      '#size' => 60,
      '#maxlength' => 512,
      '#required' => TRUE,
    ];
    $form['number_of_columns'] = [
      '#type' => 'select',
      '#title' => $this->t('Number of columns'),
      '#options' => [
        'two_cols' => $this->t('Two columns'),
        'three_cols' => $this->t('Three columns'),
        'four_cols' => $this->t('Four columns'),
      ],
      '#required' => TRUE,
    ];
    return parent::buildForm($form, $form_state);
  }

  /**
   * {@inheritdoc}
   */
  public function submitForm(array &$form, FormStateInterface $form_state) {
    // Populating config array.
    $config = $this->config('custom_layouts.settings')->get('layouts');
    if (!isset($config)) {
      $config = [];
    }
    $layout['label'] = $form_state->getValue('layout_label');
    $layout['category'] = $form_state->getValue('layout_category');
    $layout['columns'] = $form_state->getValue('number_of_columns');
    // Convert label into future array key.
    // We use helper method for this to keep code readable.
    $label = $this->toMachineName($form_state->getValue('layout_label'));
    // Making sure we are saving unique layouts even if editors enter the same label.
    $count = count($config);
    $config[$label . '_' . $count] = $layout;
    // Saving config.
    $this->config('custom_layouts.settings')
      ->set('layouts', $config)
      ->save();
    parent::submitForm($form, $form_state);
  }

  /**
   * Helper function to convert label into machine name.
   *
   * @param string $label
   *    Label that needs to be converted.
   *
   * @return string $label
   *    converted label string.
   */
  protected function toMachineName(string $label) {
    $label = strtolower($label);
    $label = preg_replace('/[^a-z0-9]+/i', '_', $label);
    return $label;
  }

}
```

Our configuration form class defines the following mandatory methods:

- `getEditableConfigNames()`: Defines the variable that will store configuration options. `custom_layouts.settings` in this case.
- `getFormId()`: Form id for this configuration form.
- `buildForm()`: Build method of the form where its structure is defined. This should return a [Form API array](https://drupalize.me/tutorial/add-input-elements-form).
- `submitForm()`: Submit handler for the configuration form which saves the user-entered configuration into the `custom_layouts.settings` variable. Optionally you may define a validation handler.

### Add a route and menu item for the form

Now that we have a form, we need to define a path and menu item for editors to access it. Declare a new route in the modules *custom\_layouts.routing.yml* file, and a menu item in the *custom\_layouts.links.menu.yml*.

The *custom\_layouts.routing.yml* file should look like the following:

```
custom_layouts.form:
  path: '/admin/structure/custom-layouts'
  defaults:
    _form: '\Drupal\custom_layouts\Form\LayoutConfigurationForm'
    _title: 'Custom layouts configuration form'
  requirements:
    _permission: 'administer site configuration'
```

The *custom\_layouts.links.menu.yml* file contains the following:

```
custom_layouts.form:
  title: 'Custom layouts configuration'
  parent: system.admin_structure
  route_name: custom_layouts.form
  weight: 100
  menu_name: system
```

Clear the cache, and you should see the menu item in the *Administration menu* under the *Structure* section. In *Administration menu*, navigate to the path (admin/structure/custom-layouts) and you should see the form.

Test it by filling in the form and pressing the *Save configuration* button.

Image

![Screenshot of custom configuration form for layout plugins](/sites/default/files/styles/max_800w/public/tutorials/images/layout_config_form.png?itok=8W5E5yhd)

You should see a message that the configuration has been saved.

Learn more about [creating custom forms](https://drupalize.me/tutorial/define-new-form-controller-and-route), and [menu links](https://drupalize.me/tutorial/add-menu-link-module).

### Declare a *dynamic* layout plugin

Since we are going to be using [deriver](https://drupalize.me/tutorial/plugin-derivatives), we need to declare the layout plugin in PHP class, and not via YAML. Create the file *src/Plugin/Layout/DynamicLayout.php* with the following content:

```
<?php
namespace Drupal\custom_layouts\Plugin\Layout;

use Drupal\Core\Layout\Attribute\Layout;
use Drupal\Core\Layout\LayoutDefault;
use Drupal\Core\StringTranslation\TranslatableMarkup;
use Drupal\custom_layouts\Plugin\Deriver\DynamicLayoutDeriver;

/**
 * A layout from layout configuration.
 *
 * @Layout(
 *   id = "dynamic_layout",
 *   deriver = "Drupal\custom_layouts\Plugin\Deriver\DynamicLayoutDeriver"
 * )
 */
#[Layout(
  id: "dynamic_layout",
  deriver: DynamicLayoutDeriver::class
)]
class DynamicLayout extends LayoutDefault {}
```

Notice that the attribute at the top of the class doesn't have the standard layout plugin properties? Instead, we use the *deriver* key to point to a class that is responsible for mapping the configuration provided by our settings form onto instances of this `DynamicLayout` plugin.

*Note:* To keep this tutorial focused on learning how to implement dynamic layouts, we don't customize our layout plugin class and will be mapping templates in the deriver class. This is enough to accomplish the goal of this tutorial. In more complicated real-world cases you may want to implement a custom *build()* method in the layout plugin class to override the parent method and provide a render array that meets requirements for your custom dynamic layout plugin.

### Declare deriver class

The deriver class acts as a bridge between saved configuration and the missing layout plugin properties. Create the file *src/Plugin/Deriver/DynamicLayoutDeriver.php* with the following content:

```
<?php

namespace Drupal\custom_layouts\Plugin\Deriver;

use Drupal\Component\Plugin\Derivative\DeriverBase;
use Drupal\custom_layouts\Plugin\Layout\DynamicLayout;
use Drupal\Core\Layout\LayoutDefinition;

/**
 * Makes a dynamic layout for each layout config entity.
 */
class DynamicLayoutDeriver extends DeriverBase {

  /**
   * {@inheritdoc}
   */
  public function getDerivativeDefinitions($base_plugin_definition) {
    $config = \Drupal::config('custom_layouts.settings');
    $config = $config->get('layouts');
    if (!is_array($config)) {
      return;
    }
    foreach ($config as $key => $layout) {
      // Here we fill in any missing keys on the layout attribute.
      $this->derivatives[$key] = new LayoutDefinition([
        'class' => DynamicLayout::class,
        'label' => $layout['label'],
        'category' => $layout['category'],
        'regions' => $this->getRegions($layout['columns']),
        'template' => $this->getTemplate($layout['columns']),
        'icon_map' => $this->getIcon($layout['columns']),
      ]);
    }

    return $this->derivatives;
  }

  /**
   * Helper function to get icon of the layout based on the passed columns value.
   *
   * @param string $columns
   *    value of columns passed through the configuration.
   *
   * @return array
   *    array of icon definition.
   */
  protected function getIcon($columns) {
    switch ($columns) {
      case 'two_cols':
        return [['first', 'second']];
      case 'three_cols':
        return [['first', 'second', 'third']];
      case 'four_cols':
        return [['first', 'second', 'third', 'fourth']];
    }
  }

  /**
   * Helper function to get regions by columns value.
   *
   * @param string $columns
   *    value of columns passed through the configuration.
   *
   * @return array
   *    array of regions.
   */
  protected function getRegions($columns) {
    switch ($columns) {
      case 'two_cols':
        return ['first' => ['label' => 'First'],
                'second' => ['label' => 'Second'],];
      case 'three_cols':
        return ['first' => ['label' => 'First'], 
                'second' => ['label' => 'Second'],
                'third' => ['label' => 'Third'],];
      case 'four_cols':
        return ['first' => ['label' => 'First'],
                'second' => ['label' => 'Second'],
                'third' => ['label' => 'Third'],
                'fourth' => ['label' => 'Fourth'],];
    }
  }

  /**
   * Helper function to get template based on the columns value.
   *
   * @param string $columns
   *    value of columns passed through the configuration.
   *
   * @return string
   *    path to the template file.
   */
  protected function getTemplate($columns) {
    $module_handler = \Drupal::service('module_handler');
    $module_path = $module_handler->getModule('custom_layouts')->getPath();
    switch ($columns) {
      case 'two_cols':
        return $module_path . '/templates/layouts/custom-two-col';
      case 'three_cols':
        return $module_path . '/templates/layouts/custom-three-col';
      case 'four_cols':
        return $module_path . '/templates/layouts/custom-four-col';
    }
  }

}
```

In this code the most important part is the `getDerivativeDefinitions()` method that is responsible for generating a properties map, and dynamically defining layout plugins from that map. It loads the configuration from our configuration form, and then loops through each set of values and adds a new layout plugin to the list.

The rest of the code is helper methods we've added that map configuration options to icons, templates, and regions for each layout.

To keep focus on derivers and how they work, we simplified the example and use a simple configuration object instead of configuration entities. Using configuration entities would be better as it allows for update and delete operations, and enhanced management options for custom layout plugins. If you'd like to learn more about configuration entities, please refer to [Configuration Data Types](https://drupalize.me/tutorial/configuration-data-types) tutorial.

### Set up Twig templates

In our deriver class we identified the path to 3 template files. Since this is not a tutorial on Twig templating we will only provide content of the 2-columns template. Make sure you create the other 2: for 3 columns and 4 columns.

The 2-columns template should be located in the *templates/layouts/custom-two-col.html.twig* file per the `getTemplate()` method on our deriver, and may look something like the following:

```
{#
/**
 * @file
 *
 * Theme implementation for a two column layout.
 */
#}

{% if content|render|trim %}
  <div{{ attributes.addClass(classes) }}>
    <div {{ region_attributes.first.addClass('layout__region', 'layout__region--first') }} {% if not region_attributes.first %} class="layout__region layout__region--first" {% endif %}>
      {% if content.first %}
          {{ content.first }}
      {% endif %}
    </div>

    <div {{ region_attributes.second.addClass('layout__region', 'layout__region--second') }} {% if not region_attributes.second %} class="layout__region layout__region--second" {% endif %}>
      {% if content.second %}
          {{ content.second }}
      {% endif %}
    </div>
  </div>

{% endif %}
```

And the final folder structure of the module should be similar to this:

```
└── custom_layouts
    ├── custom_layouts.info.yml
    ├── custom_layouts.routing.yml
    ├── src
    │     ├── Form
    │     │      └── LayoutConfigurationForm.php
    │     └── Plugin
    │          ├── Deriver
    │          │       └── DynamicLayoutDeriver.php
    │          └── Layout
    │               └── DynamicLayout.php
    ├── custom_layouts.menu.links.yml
    └── templates
                └── layouts
                    ├── custom-four-col.html.twig
                    ├── custom-three-col.html.twig
                    └── custom-two-col.html.twig
```

## Use a dynamic layout inside Basic page content type

Now we can test that it's working. First clear the cache.

If you haven't already done so, use the new configuration form you just created to define one or more new layouts.

Then in the *Manage* administration menu, navigate to *Structure* > *Content types* > and choose the *Manage display* option for the *Basic page* content type. (Or any other content type with Layout Builder enabled.)

Press *Manage layout*. Then press *Add section*; at the bottom of the sidebar you should see your new custom section available for selection. Select it and populate its admin label. Then press *Add section*. Your section is now ready to be used within the Layout Builder.

Image

![Screenshot of custom layout section](/sites/default/files/styles/max_800w/public/tutorials/images/custom_layout_section.png?itok=Q0W28-Nv)

*Note*: Regions may not display side by side for you on the first placement, depending on your theme. To fix it you probably would want to add some CSS to your section -- either to its Twig template or within your theme.

## Recap

In this tutorial, we learned how to dynamically define layouts based on configuration using plugin derivatives. To do so we first created a UI that allows a site administrator to provide configuration for one or more new layouts. Then we defined a deriver class that can take that configuration and map it to instances of a custom layout plugin. Essentially programmatically doing what we might otherwise do via a static *{MODULE\_NAME}.layouts.yml* file.

## Further your understanding

- We used a simple configuration form for storing settings. Can you improve the code and store configuration as configuration entities? What are the benefits of doing so?
- Override the `build()` method of the custom layout plugin instead of providing template paths in the deriver class.

## Additional resources

- [Layout API](https://www.drupal.org/docs/drupal-apis/layout-api) (Drupal.org)
- [How to register layouts documentation](https://www.drupal.org/docs/drupal-apis/layout-api/how-to-register-layouts) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[How to Create a Layout with Configurable Settings in Drupal's Layout Builder](/tutorial/how-create-layout-configurable-settings-drupals-layout-builder?p=3271)

Clear History

Ask Drupalize.Me AI

close