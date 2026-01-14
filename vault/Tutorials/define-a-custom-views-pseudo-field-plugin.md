---
title: "Define a Custom Views Pseudo Field Plugin"
url: "https://drupalize.me/tutorial/define-custom-views-pseudo-field-plugin?p=2939"
guide: "[[views-drupal]]"
---

# Define a Custom Views Pseudo Field Plugin

## Content

By default, the Views module can display data contained in any field attached to an entity that is exposed in Views, and the content of any database column exposed to Views via an implementation of `hook_views_data()`. It's also possible to create *pseudo* fields. These appear in the Views UI like any other field, but don't map directly to the data stored in a database column and instead allow the data to be preprocessed. This could be performing a calculation, combining multiple fields into one, and much more.

A common example in core is the fields that allow you to perform edit or delete operations on a node. These don't correspond to a specific database column. And they can't be hard-coded because they require dynamic content specific to the node in question. Instead, they are the result of taking the entity ID and combining it with knowledge about the appropriate route for someone to edit the entity and outputting that as a link.

Another example: Imagine a cooking website where you collect *cook time* and *preparation time* (*prep time*) for recipes and want to also display the *full time* to prepare. In this case *cook time* and *prep time* could be fields on the recipe content type and *total time* could be handled as a calculated output of both fields, added together and converted into hours and minutes. To achieve this, you can create a custom Views pseudo field and specify the calculation and processing logic in the render function.

In this tutorial we'll:

- Learn how to define a custom Views field plugin for a pseudo field
- Attach the created field to node entities, and expose it to display in a view

By the end of this tutorial you should know how to define a Views pseudo field plugin, attach it to the node entity type via `hook_views_data_alter()`, and display it in a view.

## Goal

Define a Views field plugin that displays the total time required to prepare a recipe by adding the *cook time* and *prep time* fields together.

## Prerequisites

- [Overview: Views Plugins](https://drupalize.me/tutorial/overview-views-plugins)
- [Define a Views Field Handler Plugin](https://drupalize.me/tutorial/define-views-field-handler-plugin)
- [Implement a Plugin Using PHP Attributes](https://drupalize.me/tutorial/implement-plugin-using-php-attributes)
- [Adding a Content Type](https://drupalize.me/tutorial/user-guide/structure-content-type?p=3071)
- [Adding Basic Fields to a Content Type](https://drupalize.me/tutorial/user-guide/structure-fields?p=3071)

## Initial setup

If you'd like to follow along with this tutorial, follow the steps below to set up the Recipe content type and fields we'll use. Feel free to skip the setup and move to the field plugin definition part of this tutorial if you are using it as a guide to fulfill your own set of requirements.

### Create a *Recipe* content type

Create a *Recipe* content type and add 2 integer numeric fields: *Cook time* and *Prep time*. Your content type setup may look something like the following:

Image

![Screenshot of Recipe content type](../assets/images/recipe_content_type.png)

Your time field setup can look something like below:

Image

![Screenshot of cook time field settings](../assets/images/cook_time_field.png)

Fields:

| Field label | Machine name | Type |
| --- | --- | --- |
| Cook time | field\_cook\_time | Number (integer) |
| Prep time | field\_prep\_time | Number (integer) |

Create 3 or 4 recipes so that you have something to show in the view later.

### Create a custom *Recipe* module

To define a custom field plugin we'll create a new *recipe* module, and add our field handler plugin to that module.

Create the *recipe* folder in the */modules/custom* folder of your Drupal site. Add a *recipe.info.yml* file. The contents of the file may look something like the following.

```
name: Recipe
type: module
description: 'Custom functionality for Recipes.'
core_version_requirement: ^8 || ^9 || ^10
package: 'Custom'
dependencies:
  - drupal:views
```

## Define a pseudo field

Now that we've got our *Recipe* content type configured we can create a new field handler plugin that will house the code with the logic we'll use to calculate the data for the field. Then in either `hook_views_data()` or `hook_views_data_alter()` we'll define a new field that uses our custom plugin.

### Define a plugin

In the `recipe` module directory, add the file *src/Plugin/views/field/FullTime.php* (and necessary directories). Field plugins are defined in the `Plugin\views\field` sub-namespace. Your folder structure may look like the following:

```
recipe
├── recipe.info.yml
└── src
    └── Plugin
        └── views
            └── field
                └── FullTime.php
```

This is the base of a custom field plugin. Custom field plugins use `\Drupal\views\Attribute\ViewsField` attributes. Since it's a custom field plugin, it'll extend the generic `\Drupal\views\Plugin\views\field\FieldPluginBase` class. The skeleton of the class should look something like the below.

```
<?php

namespace Drupal\recipe\Plugin\views\field;

use Drupal\views\Attribute\ViewsField;
use Drupal\views\Plugin\views\field\FieldPluginBase;
use Drupal\views\ResultRow;

/**
 * Field handler to flag the node type.
 *
 * @ingroup views_field_handlers
 */
#[ViewsField("full_time")]
class FullTime extends FieldPluginBase {

}
```

### Add some logic

In our custom plugin we'll need to define and override 2 methods: `query()` and `render()`. Your *FullTime.php* file should look like this:

```
<?php

namespace Drupal\recipe\Plugin\views\field;

use Drupal\views\Attribute\ViewsField;
use Drupal\views\Plugin\views\field\FieldPluginBase;
use Drupal\views\ResultRow;

/**
 * Field handler to flag the node type.
 *
 * @ingroup views_field_handlers
 */
#[ViewsField("full_time")]
class FullTime extends FieldPluginBase {

  /**
   * @{inheritdoc}
   */
  public function query() {
    // Leave empty to avoid the field being used in the query.
  }

  /**
   * @{inheritdoc}
   */
  public function render(ResultRow $values) {
    $node = $values->_entity;
    if ($node->bundle() !== 'recipe') {
      return '';
    }
    $cook_time = $node->field_cook_time->value;
    $prep_time = $node->field_prep_time->value;

    $full_time = $cook_time + $prep_time;
    $full_time_h = floor($full_time / 60);
    $full_time_m = $full_time - $full_time_h * 60;

    return $this->t('Full cooking and preparation time @h h, @m min', ['@h' => $full_time_h, '@m' => $full_time_m]);
  }
}
```

We override the `query()` method and leave it empty. This is done so the Views module isn't trying to query this field, since there is no corresponding database column. This is what makes it a *pseudo field*.

Then in the `render()` method we can compute the data we want to display for the field. In this case we get the values of *cook\_time* and *prep\_time*, calculate the total value, and convert it to an hours and minutes format.

This example is specific to our site setup. It relies on the field names from the content type we created in the preparation steps above, and the field is limited to be available for nodes with bundle called *recipe*.

However, this same approach could be used for any entity type. Make sure to adjust conditions in the `render()` method code to fit your needs.

### Add a field in `hook_views_data_alter()`

We need to tell Views about the existence of our new field. In our case we want to add to the list of fields Views knows about for Node entities. This list is defined by the Node module. We can alter that list by implementing `hook_views_data_alter()` and adding to the `$data` array there.

In the *recipe* module's root, add a *recipe.module* PHP file (with an opening `<?php` tag at the top), and define `recipe_views_data_alter()` inside it. The code for the hook may look something like the below:

```
/**
 * Implements hook_views_data_alter().
 */
function recipe_views_data_alter(array &$data) {
  // This 'full_time' field is a pseudo field and doesn't correspond with any
  // specific database table. Instead, its data is computed by adding together
  // the values of the `field_cook_time` and `field_prep_time` fields on the
  // 'recipe' content type.
  // @see \Drupal\recipe\Plugin\views\field\FullTime.
  $data['node']['full_time'] = [
    'title' => t('Full cook and prep time'),
    'field' => [
      'title' => t('Full cook and prep time'),
      'help' => t('Total value of cook and prep time. <em>Appears on Recipe nodes only.</em>'),
      'id' => 'full_time',
    ],
  ];
}
```

### Enable the module

Enable the *Recipe* module either through drush (`drush en recipe`) or through the UI and [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache).

### Configure a view

Navigate to *Structure* > *Views* > *Add view*. Add a *Recipes* view with a page. The basic configuration may look something like the screenshot below:

Image

![Screenshot of recipes view](../assets/images/recipes_view.png)

Here we create a view with a page display that lists content of the type *Recipe* displayed as an unformatted list of fields. If necessary, change the format to use fields (*Format* > *Show*, select *Fields*). For now, we only add *Title* as a field, and order by *Authoring date* descending. Leave other settings as defaults or modify them to match your needs.

In the *Fields* section, select *Add* button and search for *Full cook and prep time*. Add the field, scroll down to view the results in the *Preview* section. Your preview area now should show the new computed value for the full cooking time.

Image

![Screenshot of recipes view preview](../assets/images/recipes_view_preview.png)

## Computed fields

In the steps above we added a pseudo field directly to the view using a custom field handler plugin. Our node doesn't know anything about this field, and it is only available in Views. If you'd like to be able to use the pseudo field outside the Views context you may want to create a *computed field* instead and then expose that to Views. The steps to expose computed fields to Views are the same as using Views pseudo fields. You can read more about [Dynamic/Virtual field values using computed field property classes](https://www.drupal.org/docs/drupal-apis/entity-api/dynamicvirtual-field-values-using-computed-field-property-classes) in the Drupal.org documentation.

## Recap

In this tutorial, we learned how to define a custom Views pseudo field plugin, add it to a specific entity type, and use it in a view. For this to work, we had to define a custom field plugin that has an empty `query()` method to ensure the Views module isn't trying to build a query against it. We also defined a `render()` method where the calculation happens and computes the data we want to display. Then we exposed this new field to Views through an implementation of `hook_views_data_alter()` and attached it to the `node` entity type.

## Further your understanding

- What hook should be used to expose computed fields to Views? What code needs to be written for it to work?
- When would it be better to use a computed field instead of the custom Views pseudo field?

## Additional resources

- [List of Views hooks](https://api.drupal.org/api/drupal/core%21modules%21views%21views.api.php/11.x) (api.drupal.org)
- [Hook\_views\_data documentation](https://api.drupal.org/api/drupal/core%21modules%21views%21views.api.php/function/hook_views_data/) (api.drupal.org)
- [Views field handlers](https://api.drupal.org/api/drupal/core!modules!views!src!Plugin!views!field!FieldPluginBase.php/group/views_field_handlers/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Define a Views Field Handler Plugin](/tutorial/define-views-field-handler-plugin?p=2939)

Next
[Define a Custom Views Filter Plugin](/tutorial/define-custom-views-filter-plugin?p=2939)

Clear History

Ask Drupalize.Me AI

close