---
title: "Modify Existing Entities with Alter Hooks"
url: "https://drupalize.me/tutorial/modify-existing-entities-alter-hooks?p=2607"
guide: "[[work-data-modules]]"
---

# Modify Existing Entities with Alter Hooks

## Content

On occasion, you may need to modify the behavior of entity types defined by another module. Thankfully, Drupal includes several alter hooks that can be used to override the behavior of another entity.

In this tutorial, we will:

- Walk through the common Entity API hooks
- Look at example implementations of each
- And discuss the use cases for each

By the end of this tutorial, you will have a better understanding of how to override the default behavior of an entity type provided by Drupal core (or another contributed module) within your custom code.

## Goal

Demonstrate how to alter or enhance entities owned by another module.

## Prerequisites

- [Discover Existing Hooks](https://drupalize.me/tutorial/discover-existing-hooks)
- [Implement Any Hook](https://drupalize.me/tutorial/implement-any-hook)
- [Create a Custom Content Entity](https://drupalize.me/tutorial/create-custom-content-entity)
- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins)
- [PHP Attributes](https://drupalize.me/tutorial/php-attributes)

Drupal includes [hundreds of hooks](https://api.drupal.org/api/drupal/core%21core.api.php/group/hooks/) that allow our custom code to interact with various subsystems. The Entity API hooks we'll be covering in this tutorial are documented in the *core/lib/Drupal/Core/Entity/entity.api.php* file.

## Alter entity metadata

As we learned in [Create a Custom Content Entity](https://drupalize.me/tutorial/create-custom-content-entity), the `#[ContentEntityType]` attribute defines the metadata that drives a content entity type's behavior. Drupal provides hooks for altering this metadata.

### Override attributes with `hook_entity_type_alter`

If the behavior you want to override is defined in that attribute, [`hook_entity_type_alter`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_type_alter/) can help.

```
function hook_entity_type_alter(array &$entity_types) {
  /** @var $entity_types \Drupal\Core\Entity\EntityTypeInterface[] */
  // Set the controller class for nodes to an alternate implementation of the
  // Drupal\Core\Entity\EntityStorageInterface interface.
  $entity_types['node']->setStorageClass('Drupal\mymodule\MyCustomNodeStorage');
}
```

This hook receives the cached information from every entity type definition. Within your implementation, you can adjust any attribute value you need in order to accomplish your goal. In the example above, we're changing the storage class for nodes to an alternate implementation provided by a custom module.

### Modify bundle info with `hook_entity_bundle_info_alter`

Rather than overriding information for an entire entity type, there may be instances where you only need to make changes for one particular bundle. In that case, [`hook_entity_bundle_info_alter`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_bundle_info_alter/) may come in handy.

```
// Change the user interface label for user accounts to 'Full account'.
function hook_entity_bundle_info_alter(&$bundles) {
  $bundles['user']['user']['label'] = t('Full account');
}
```

### Change base fields with `hook_entity_base_field_info_alter`

Instead of changing the metadata of an entity type or bundle, perhaps you find yourself needing to change the base fields. In that case, [`hook_entity_base_field_info_alter`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_base_field_info_alter/) to the rescue. *Note*: this hook [will be changing](https://www.drupal.org/node/2346329) in an upcoming release of Drupal, but for now it's the best method available to alter base field information.

```
function hook_entity_base_field_info_alter(&$fields, \Drupal\Core\Entity\EntityTypeInterface $entity_type) {
  // Alter the mymodule_text field to use a custom class.
  if ($entity_type->id() == 'node' && !empty($fields['mymodule_text'])) {
    $fields['mymodule_text']->setClass('\Drupal\anothermodule\EntityComputedText');
  }
}
```

### Use alternative storage configuration

You can use `hook_entity_field_storage_info_alter` to update storage configuration.

If the configuration changes you need to make have to do with the storage definitions of an entity, you may be interested in [`hook_entity_field_storage_info_alter`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_field_storage_info_alter/).

```
function hook_entity_field_storage_info_alter(&$fields, \Drupal\Core\Entity\EntityTypeInterface $entity_type) {
  // Alter the max_length setting.
  if ($entity_type->id() == 'node' && !empty($fields['mymodule_text'])) {
    $fields['mymodule_text']->setSetting('max_length', 128);
  }
}
```

### Add info to an entity type with `hook_entity_type_build`

At times, rather than altering information provided by a particular entity type, you may wish to add additional information to an entity type definition. In this case, [`hook_entity_type_build`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_type_build/) can help.

```
function hook_entity_type_build(array &$entity_types) {
  /** @var $entity_types \Drupal\Core\Entity\EntityTypeInterface[] */
  // Add a form for a custom node form without overriding the default
  // node form. To override the default node form, use hook_entity_type_alter().
  $entity_types['node']->setFormClass('mymodule_foo', 'Drupal\mymodule\NodeFooForm');
}
```

The core Settings Tray module in its *settings\_tray.module* file uses `hook_entity_type_build()` to set a form class and a link template:

```
/**
 * Implements hook_entity_type_build().
 */
function settings_tray_entity_type_build(array &$entity_types) {
  /** @var \Drupal\Core\Entity\EntityTypeInterface[] $entity_types */
  $entity_types['block']
    ->setFormClass('settings_tray', BlockEntitySettingTrayForm::class)
    ->setLinkTemplate('settings_tray-form', '/admin/structure/block/manage/{block}/settings-tray');
}
```

## Alter the entity rendering process

Probably the most useful Entity API hooks allow us to intercept entities during the building and rendering process to change or add additional information prior to their final output.

### Change view mode configuration with 2 hooks

Each entity type can define its own unique collection of view modes. These view modes can be used to define a particular configuration of how the output for a particular entity should be generated. The configuration for a particular view mode can be altered using [`hook_entity_view_mode_info_alter`](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Entity!entity.api.php/function/hook_entity_view_mode_info_alter/). Perhaps more often you'll be interested in changing the view mode itself (rather than the view mode settings) with [`hook_entity_view_mode_alter`](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Entity!entity.api.php/function/hook_entity_view_mode_alter/). This technique can be used to change the view mode, based on particular conditions.

```
function hook_entity_view_mode_alter(&$view_mode, Drupal\Core\Entity\EntityInterface $entity) {
  // For nodes, change the view mode when it is 'teaser'.
  if ($entity->getEntityTypeId() == 'node' && $view_mode == 'teaser') {
    $view_mode = 'my_custom_view_mode';
  }
}
```

*Note:* See also this Drupal 10.0.0 change record: [$context removed from hook\_entity\_view\_mode\_alter()](https://www.drupal.org/node/3193299).

### Tweak display settings with `hook_entity_view_display_alter`

The display settings for an entity can be changed using [`hook_entity_view_display_alter`](https://api.drupal.org/hook_entity_view_display_alter). One particular implementation of this hook can be seen in the node module, where it is used to hide field labels when nodes are displayed using the search index view mode.

```
function node_entity_view_display_alter(EntityViewDisplayInterface $display, $context) {
  if ($context['entity_type'] == 'node') {
    // Hide field labels in search index.
    if ($context['view_mode'] == 'search_index') {
      foreach ($display->getComponents() as $name => $options) {
        if (isset($options['label'])) {
          $options['label'] = 'hidden';
          $display->setComponent($name, $options);
        }
      }
    }
  }
}
```

### Make changes before final rendering

Once the view mode and display settings are set, and the render pipeline is building the entity for display, we have a handful of opportunities to alter data before the final rendering process. We can alter the render array generated by the `EntityDisplay` class for a particular entity using [`hook_entity_display_build_alter`](https://api.drupal.org/hook_entity_display_build_alter). For example, we could append additional RDF information to taxonomy terms:

```
use Drupal\Core\Render\Element;

function hook_entity_display_build_alter(&$build, $context) {
  // Append RDF term mappings on displayed taxonomy links.
  foreach (Element::children($build) as $field_name) {
    $element = &$build[$field_name];
    if ($element['#field_type'] == 'entity_reference' && $element['#formatter'] == 'entity_reference_label') {
      foreach ($element['#items'] as $delta => $item) {
        $term = $item->entity;
        if (!empty($term->rdf_mapping['rdftype'])) {
          $element[$delta]['#options']['attributes']['typeof'] = $term->rdf_mapping['rdftype'];
        }
        if (!empty($term->rdf_mapping['name']['predicates'])) {
          $element[$delta]['#options']['attributes']['property'] = $term->rdf_mapping['name']['predicates'];
        }
      }
    }
  }
}
```

The final Entity API system hook we can use to alter the content before it is passed to the theme system in the render pipeline is [`hook_entity_view_alter`](https://api.drupal.org/hook_entity_view_alter). At this point, the complete structure of the render array for the entity has been built. After this hook fires, the content will begin processing from a render array into the final output format (usually HTML). If you find yourself needing to alter the final markup output of an entity, you should use this hook to add a `#post_render` callback for final processing.

```
function hook_entity_view_alter(&$build, $type) {
  if ($build['#view_mode'] == 'full' && isset($build['an_additional_field'])) {
    // Change its weight.
    $build['an_additional_field']['#weight'] = -10;

    // Add a #post_render callback to act on the rendered HTML of the entity.
    $build['#post_render'][] = 'my_module_node_post_render';
  }
}
```

## Recap

In this tutorial, we took a look at several of the hooks provided by the Entity API system. We saw how it's possible to implement a hook in our custom module to override the metadata associated with any entity type. We also saw how some of the hooks allow us to interact with the user-configurable display settings, and how to use these hooks to change how entities are rendered.

## Further your understanding

- How does the translation system make use of `hook_entity_type_alter` to add translation support to entities?
- Which [Entity API hook](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/) could you use to alter the access behavior for a particular field?
- If you found yourself needing to override the settings on an entity form, which Entity API hook could you use (without using `hook_form_alter`)?

## Additional resources

- [Entity API hooks](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/) (Drupal.org)
- [Entity CRUD, editing, and view hooks](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/group/entity_crud/) (Drupal.org)
- Change record: [$context removed from hook\_entity\_view\_mode\_alter()](https://www.drupal.org/node/3193299) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Entity API Hooks](/tutorial/entity-api-hooks?p=2607)

Next
[Using Entity Bundle Classes for Site-Specific Features](/tutorial/using-entity-bundle-classes-site-specific-features?p=2607)

Clear History

Ask Drupalize.Me AI

close