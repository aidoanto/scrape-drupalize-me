---
title: "Entity API Hooks"
url: "https://drupalize.me/tutorial/entity-api-hooks?p=2607"
guide: "[[work-data-modules]]"
order: 8
---

# Entity API Hooks

## Content

Drupal's Entity system provides several hooks that allow custom code to interact with various parts of the entity life cycle.

In this tutorial we'll:

- Examine the available hooks
- Learn how to make use of them to act on several different types of operations on individual entities

By the end if this tutorial you should have a better understanding of the hooks available to developers who want to respond to entity lifecycle operations and how to use them to customize the way specific entity types work.

## Goal

Learn about the various hooks we can use to interact with entities.

## Prerequisites

- [Entity API Overview](https://drupalize.me/tutorial/entity-api-overview)
- [Working with Entity CRUD](https://drupalize.me/tutorial/working-entity-crud)
- [Logging](https://drupalize.me/blog/201510/how-log-messages-drupal-8)
- [What Are Hooks?](https://drupalize.me/tutorial/what-are-hooks)
- [Implement Any Hook](https://drupalize.me/tutorial/implement-any-hook)

All of the entity hooks we're going to cover in this tutorial are also documented in the *core/lib/Drupal/Core/Entity/entity.api.php* file. One pattern that will emerge is that most of the hooks have multiple versions. The first, such as `hook_entity_create` will be triggered for every the creation of *every* entity. The second `hook_ENTITY_TYPE_create` allows us to target a particular entity type. In order to use this second type of hook not only do you replace the `hook` portion of the function name with the machine name of your module, but you also replace `ENTITY_TYPE` with the type of entity (node, user, term, file, etc). Not only is the second approach a bit more performant, but it also makes our code easier to read since the function name gives us more contextual information about what it is doing.

## Load entities

The first hooks we'll look at are [`hook_entity_load`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_load/) (`hook_ENTITY_TYPE_load`) and [`hook_entity_storage_load`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_storage_load/). These hooks allow us to interact with entity types as they're loaded by the API. As such, it's extremely important that these implementation take performance considerations into account since this code could be executed hundreds or thousands of times per page load. If you're adding additional data onto content entities you should use `hook_entity_storage_load`, because the results of that hook are cached.

### hook\_entity\_load

```
function hook_entity_load(array $entities, $entity_type_id) {
  foreach ($entities as $entity) {
    $entity->foo = mymodule_add_something($entity);
  }
}
```

### hook\_ENTITY\_TYPE\_load

```
function hook_ENTITY_TYPE_load($entities) {
  foreach ($entities as $entity) {
    $entity->foo = mymodule_add_something($entity);
  }
}
```

### hook\_entity\_storage\_load

```
function hook_entity_storage_load(array $entities, $entity_type) {
  if ($entity_type == ' user') {
    foreach ($entities as $entity) {
      $entity->foo = mymodule_add_something_uncached($entity);
    }
  }
}
```

The best example of an implementation of these hooks in core can be found in [`comment_entity_storage_load`](https://api.drupal.org/api/drupal/core%21modules%21comment%21comment.module/function/comment_entity_storage_load/) where comment statistics are added.

## Interact with an entity before it is loaded

### hook\_entity\_preload

A new hook (as of 8.7) has been introduced that allows you to interact with an entity before it is loaded.

```
function hook_entity_preload(array $ids, $entity_type_id) {
  $entities = [];
  foreach ($ids as $id) {
    $entities[] = mymodule_swap_revision($id);
  }
  return $entities;
}
```

According to the [change record](https://www.drupal.org/node/3015367):

> Some modules need to act before an entity is loaded, and swap out the default revision with a different one. For example, the Workspaces module swaps the default revision with a workspace-specific revision, if one exists.

Here is an example of Workspaces module implementing `hook_entity_preload`:

```
function workspaces_entity_preload(array $ids, $entity_type_id) {
  return \Drupal::service('class_resolver')
    ->getInstanceFromDefinition(EntityOperations::class)
    ->entityPreload($ids, $entity_type_id);
}
```

## Interact with entities prior to display

You may also find yourself with a need to interact with entities just prior to their display. Especially in the instance where the additional data you need to append to your entity is itself an entity, you may need to implement [`hook_entity_prepare_view`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_prepare_view/).

### hook\_entity\_prepare\_view

```
function hook_entity_prepare_view($entity_type_id, array $entities, array $displays, $view_mode) {
  // Load a specific node into the user object for later theming.
  if (!empty($entities) && $entity_type_id == 'user') {
    // Only do the extra work if the component is configured to be
    // displayed. This assumes a 'mymodule_addition' extra field has been
    // defined for the entity bundle in hook_entity_extra_field_info().
    $ids = array();
    foreach ($entities as $id => $entity) {
      if ($displays[$entity->bundle()]->getComponent('mymodule_addition')) {
        $ids[] = $id;
      }
    }
    if ($ids) {
      $nodes = mymodule_get_user_nodes($ids);
      foreach ($ids as $id) {
        $entities[$id]->user_node = $nodes[$id];
      }
    }
  }
}
```

## Interact with entities before rendering

There are several hooks we can use to interact with our entities as they are assembled but before they're handed off to the rendering system: [`hook_entity_view`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_view/),
[`hook_ENTITY_TYPE_view`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_ENTITY_TYPE_view/), and
[`hook_entity_view_alter`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_view_alter/).

In the case of `hook_entity_view` our hook receives the renderable array of content for our entity that is about to be rendered, the entity object itself, the entity display object containing information about the display options, and the view mode the entity is rendered in as parameters. We can use this hook to either add additional markup, alter the existing render array, or add a theme function to the render process for our entities.

### hook\_entity\_view

```
function hook_entity_view(array &$build, \Drupal\Core\Entity\EntityInterface $entity, \Drupal\Core\Entity\Display\EntityViewDisplayInterface $display, $view_mode) {
  // Only do the extra work if the component is configured to be displayed.
  // This assumes a 'mymodule_addition' extra field has been defined for the
  // entity bundle in hook_entity_extra_field_info().
  if ($display->getComponent('mymodule_addition')) {
    $build['mymodule_addition'] = array(
      '#markup' => mymodule_addition($entity),
      '#theme' => 'mymodule_my_additional_field',
    );
  }
}
```

### hook\_ENTITY\_TYPE\_view

```
function hook_ENTITY_TYPE_view(array &$build, \Drupal\Core\Entity\EntityInterface $entity, \Drupal\Core\Entity\Display\EntityViewDisplayInterface $display, $view_mode) {
  // Only do the extra work if the component is configured to be displayed.
  // This assumes a 'mymodule_addition' extra field has been defined for the
  // entity bundle in hook_entity_extra_field_info().
  if ($display->getComponent('mymodule_addition')) {
    $build['mymodule_addition'] = array(
      '#markup' => mymodule_addition($entity),
      '#theme' => 'mymodule_my_additional_field',
    );
  }
}
```

If your code needs to operate on the fully rendered HTML of an entity rather than just on the structured data of the render array, you will want to use `hook_entity_view_alter` instead. This hook is typically used to adjust the weight of elements that haven't been rendered yet, and add additional `#post_render` callback functions that allow interacting with the rendered HTML of an entity.

### hook\_entity\_view\_alter

```
function hook_entity_view_alter(array &$build, Drupal\Core\Entity\EntityInterface $entity, \Drupal\Core\Entity\Display\EntityViewDisplayInterface $display) {
  if ($build['#view_mode'] == 'full' && isset($build['an_additional_field'])) {
    // Change its weight.
    $build['an_additional_field']['#weight'] = -10;

    // Add a #post_render callback to act on the rendered HTML of the entity.
    $build['#post_render'][] = 'my_module_node_post_render';
  }
}
```

This hook is called when an entity is being viewed, after the [render array](https://drupalize.me/tutorial/what-are-render-arrays) has been created, after all implementations of `hook_entity_view()` have been invoked, but before it is rendered to HTML. Modules should implement this hook if they need to alter the structured data of the renderable array.

## Create or update entities

Perhaps we need to perform an action every time an entity, or an entity of a certain type, is created. In that case we need to implement [`hook_entity_create`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_create/) or [`hook_ENTITY_TYPE_create`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_ENTITY_TYPE_create/). In this example implementation we're using Drupal's logger to add information about the newly created entity to our watchdog log.

### hook\_entity\_create

```
function hook_entity_create(\Drupal\Core\Entity\EntityInterface $entity) {
  \Drupal::logger('example')->info('Entity created: @label', ['@label' => $entity->label()]);
}
```

### hook\_ENTITY\_TYPE\_create

```
function hook_ENTITY_TYPE_create(\Drupal\Core\Entity\EntityInterface $entity) {
  \Drupal::logger('example')->info('ENTITY_TYPE created: @label', ['@label' => $entity->label()]);
}
```

Similar, but slightly different from the "create" hook is [`hook_entity_insert`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_insert/). The insert hook responds to the creation of a new entity once the actual data has been stored. This hook can respond to, but can not change the data stored along with a new entity.

### hook\_entity\_insert

```
function hook_entity_insert(Drupal\Core\Entity\EntityInterface $entity) {
  // Insert the new entity into a fictional table of all entities.
  db_insert('example_entity')
    ->fields(array(
      'type' => $entity->getEntityTypeId(),
      'id' => $entity->id(),
      'created' => REQUEST_TIME,
      'updated' => REQUEST_TIME,
    ))
    ->execute();
}
```

### hook\_ENTITY\_TYPE\_insert

```
function hook_ENTITY_TYPE_insert(Drupal\Core\Entity\EntityInterface $entity) {
  // Insert the new entity into a fictional table of this type of entity.
  db_insert('example_entity')
    ->fields(array(
      'id' => $entity->id(),
      'created' => REQUEST_TIME,
      'updated' => REQUEST_TIME,
    ))
    ->execute();
}
```

### hook\_entity\_revision\_create

In Drupal, hooks are available to help you control a new revision created with `\Drupal\Core\Entity\ContentEntityStorageBase::createRevision()`. Implement `hook_entity_revision_create` if you need to change the new revision generated by the above mentioned method. This can be especially useful if you need to carry over the values of untranslatable fields or are dealing with complex use cases involving multilingual sites. (See [Fields and widgets have more control about affecting changes and pending revision translations](https://www.drupal.org/node/2975280) for further links and discussion.)

```
function hook_entity_revision_create(Drupal\Core\Entity\EntityInterface $new_revision, Drupal\Core\Entity\EntityInterface $entity, $keep_untranslatable_fields) {
  // Retain the value from an untranslatable field, which are by default
  // synchronized from the default revision.
  $new_revision->set('untranslatable_field', $entity->get('untranslatable_field'));
}
```

### hook\_ENTITY\_TYPE\_revision\_create

This hook is the same as `hook_entity_revision_create` except that you replace `ENTITY_TYPE` in the function name with the machine name of the entity type you want to target.

```
function hook_ENTITY_TYPE_revision_create(Drupal\Core\Entity\EntityInterface $new_revision, Drupal\Core\Entity\EntityInterface $entity, $keep_untranslatable_fields) {

  // Retain the value from an untranslatable field, which are by default
  // synchronized from the default revision.
  $new_revision
    ->set('untranslatable_field', $entity
    ->get('untranslatable_field'));
}
```

If you're interested in interacting with entity updates rather than their creation, there is [`hook_entity_update`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_update/).

### hook\_entity\_update

```
function hook_entity_update(Drupal\Core\Entity\EntityInterface $entity) {
  // Update the entity's entry in a fictional table of all entities.
  db_update('example_entity')
    ->fields(array(
      'updated' => REQUEST_TIME,
    ))
    ->condition('type', $entity->getEntityTypeId())
    ->condition('id', $entity->id())
    ->execute();
}
```

### hook\_ENTITY\_TYPE\_update

```
function hook_ENTITY_TYPE_update(Drupal\Core\Entity\EntityInterface $entity) {
  // Update the entity's entry in a fictional table of this type of entity.
  db_update('example_entity')
    ->fields(array(
      'updated' => REQUEST_TIME,
    ))
    ->condition('id', $entity->id())
    ->execute();
}
```

Sometimes you may not especially care if you're working with a create or update operation, but you need to add information in either situation. In that case you can make use of [`hook_entity_presave`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_presave/) to avoid code duplication. In these hooks, `$entity->original` will be populated with the original entity if this is an update operation.

### hook\_entity\_presave

```
function hook_entity_presave(Drupal\Core\Entity\EntityInterface $entity) {
  if ($entity instanceof ContentEntityInterface && $entity->isTranslatable()) {
    $route_match = \Drupal::routeMatch();
    \Drupal::service('content_translation.synchronizer')->synchronizeFields($entity, $entity->language()->getId(), $route_match->getParameter('source_langcode'));
  }
}
```

### hook\_ENTITY\_TYPE\_presave

```
function hook_ENTITY_TYPE_presave(Drupal\Core\Entity\EntityInterface $entity) {
  if ($entity->isTranslatable()) {
    $route_match = \Drupal::routeMatch();
    \Drupal::service('content_translation.synchronizer')->synchronizeFields($entity, $entity->language()->getId(), $route_match->getParameter('source_langcode'));
  }
}
```

## Delete entities

The entity deletion process also offers several hooks to give us the ability to interact:

- [`hook_entity_predelete`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_predelete/)
- [`hook_ENTITY_TYPE_predelete`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_ENTITY_TYPE_predelete/)
- [`hook_entity_delete`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_delete/)
- [`hook_ENTITY_TYPE_delete`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_ENTITY_TYPE_delete/)
- [`hook_entity_revision_delete`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_revision_delete/)
- [`hook_ENTITY_TYPE_revision_delete`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_ENTITY_TYPE_revision_delete/)

### hook\_entity\_predelete

```
function hook_entity_predelete(Drupal\Core\Entity\EntityInterface $entity) {
  // Count references to this entity in a custom table before they are removed
  // upon entity deletion.
  $id = $entity->id();
  $type = $entity->getEntityTypeId();
  $count = db_select('example_entity_data')
    ->condition('type', $type)
    ->condition('id', $id)
    ->countQuery()
    ->execute()
    ->fetchField();

  // Log the count in a table that records this statistic for deleted entities.
  db_merge('example_deleted_entity_statistics')
    ->key(array('type' => $type, 'id' => $id))
    ->fields(array('count' => $count))
    ->execute();
}
```

### hook\_ENTITY\_TYPE\_predelete

```
function hook_ENTITY_TYPE_predelete(Drupal\Core\Entity\EntityInterface $entity) {
  // Count references to this entity in a custom table before they are removed
  // upon entity deletion.
  $id = $entity->id();
  $type = $entity->getEntityTypeId();
  $count = db_select('example_entity_data')
    ->condition('type', $type)
    ->condition('id', $id)
    ->countQuery()
    ->execute()
    ->fetchField();

  // Log the count in a table that records this statistic for deleted entities.
  db_merge('example_deleted_entity_statistics')
    ->key(array('type' => $type, 'id' => $id))
    ->fields(array('count' => $count))
    ->execute();
}
```

While the predelete hook runs just before the entity is deleted, `hook_entity_delete` fires immediately after the actual entity storage is removed.

### hook\_entity\_delete

```
function hook_entity_delete(Drupal\Core\Entity\EntityInterface $entity) {
  // Delete the entity's entry from a fictional table of all entities.
  db_delete('example_entity')
    ->condition('type', $entity->getEntityTypeId())
    ->condition('id', $entity->id())
    ->execute();
}
```

### hook\_ENTITY\_TYPE\_delete

```
function hook_ENTITY_TYPE_delete(Drupal\Core\Entity\EntityInterface $entity) {
  // Delete the entity's entry from a fictional table of all entities.
  db_delete('example_entity')
    ->condition('type', $entity->getEntityTypeId())
    ->condition('id', $entity->id())
    ->execute();
}
```

Sometimes we may need to act on the deletion of a revision. Thankfully Drupal core provides for that scenario as well.

### hook\_entity\_revision\_delete

```
function hook_entity_revision_delete(Drupal\Core\Entity\EntityInterface $entity) {
  $referenced_files_by_field = _editor_get_file_uuids_by_field($entity);
  foreach ($referenced_files_by_field as $field => $uuids) {
    _editor_delete_file_usage($uuids, $entity, 1);
  }
}
```

### hook\_ENTITY\_TYPE\_revision\_delete

```
function hook_ENTITY_TYPE_revision_delete(Drupal\Core\Entity\EntityInterface $entity) {
  $referenced_files_by_field = _editor_get_file_uuids_by_field($entity);
  foreach ($referenced_files_by_field as $field => $uuids) {
    _editor_delete_file_usage($uuids, $entity, 1);
  }
}
```

## Edit entities

There is also a hook that allows us to interact with the form for our entities before it is rendered, [`hook_entity_prepare_form`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_prepare_form/) and [`hook_ENTITY_TYPE_prepare_form`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_ENTITY_TYPE_prepare_form/).

### hook\_entity\_prepare\_form

```
function hook_entity_prepare_form(\Drupal\Core\Entity\EntityInterface $entity, $operation, \Drupal\Core\Form\FormStateInterface $form_state) {
  if ($operation == 'edit') {
    $entity->label->value = 'Altered label';
    $form_state->set('label_altered', TRUE);
  }
}
```

### hook\_ENTITY\_TYPE\_prepare\_form

```
function hook_ENTITY_TYPE_prepare_form(\Drupal\Core\Entity\EntityInterface $entity, $operation, \Drupal\Core\Form\FormStateInterface $form_state) {
  if ($operation == 'edit') {
    $entity->label->value = 'Altered label';
    $form_state->set('label_altered', TRUE);
  }
}
```

## Interact with entity translations

The translation system also provides a similar set of hooks for interacting with the CRUD operations of individual translations of entities.

Creation via [`hook_entity_translation_create`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_translation_create/), [`hook_ENTITY_TYPE_translation_create`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_ENTITY_TYPE_translation_create/).

### hook\_entity\_translation\_create

```
function hook_entity_translation_create(\Drupal\Core\Entity\EntityInterface $translation) {
  \Drupal::logger('example')->info('Entity translation created: @label', ['@label' => $translation->label()]);
}
```

### hook\_ENTITY\_TYPE\_translation\_create

```
function hook_ENTITY_TYPE_translation_create(\Drupal\Core\Entity\EntityInterface $translation) {
  \Drupal::logger('example')->info('ENTITY_TYPE translation created: @label', ['@label' => $translation->label()]);
}
```

Insert via [`hook_entity_translation_insert`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_translation_insert/), [`hook_ENTITY_TYPE_translation_insert`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_ENTITY_TYPE_translation_insert/).

### hook\_entity\_translation\_insert

```
function hook_entity_translation_insert(\Drupal\Core\Entity\EntityInterface $translation) {
  $variables = array(
    '@language' => $translation->language()->getName(),
    '@label' => $translation->getUntranslated()->label(),
  );
  \Drupal::logger('example')->notice('The @language translation of @label has just been stored.', $variables);
}
```

### hook\_ENTITY\_TYPE\_translation\_insert

```
function hook_ENTITY_TYPE_translation_insert(\Drupal\Core\Entity\EntityInterface $translation) {
  $variables = array(
    '@language' => $translation->language()->getName(),
    '@label' => $translation->getUntranslated()->label(),
  );
  \Drupal::logger('example')->notice('The @language translation of @label has just been stored.', $variables);
}
```

Delete via [`hook_entity_translation_delete`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_translation_delete/), and [`hook_ENTITY_TYPE_translation_delete`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_ENTITY_TYPE_translation_delete/).

### hook\_entity\_translation\_delete

```
function hook_entity_translation_delete(\Drupal\Core\Entity\EntityInterface $translation) {
  $variables = array(
    '@language' => $translation->language()->getName(),
    '@label' => $translation->label(),
  );
  \Drupal::logger('example')->notice('The @language translation of @label has just been deleted.', $variables);
}
```

### hook\_ENTITY\_TYPE\_translation\_delete

```
function hook_ENTITY_TYPE_translation_delete(\Drupal\Core\Entity\EntityInterface $translation) {
  $variables = array(
    '@language' => $translation->language()->getName(),
    '@label' => $translation->label(),
  );
  \Drupal::logger('example')->notice('The @language translation of @label has just been deleted.', $variables);
}
```

## Control access to entities

The Entity API also provides several hooks for interacting with the access control system.

First, basic access to entities can be affected with [`hook_entity_access`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_access/) and [`hook_ENTITY_TYPE_access`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_ENTITY_TYPE_access/).

### hook\_entity\_access

```
function hook_entity_access(\Drupal\Core\Entity\EntityInterface $entity, $operation, \Drupal\Core\Session\AccountInterface $account) {
  // No opinion.
  return AccessResult::neutral();
}
```

### hook\_ENTITY\_TYPE\_access

```
function hook_ENTITY_TYPE_access(\Drupal\Core\Entity\EntityInterface $entity, $operation, \Drupal\Core\Session\AccountInterface $account) {
  // No opinion.
  return AccessResult::neutral();
}
```

We can also control access to entity creation via ['hook\_entity\_create\_access'](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_create_access/) and [`hook_ENTITY_TYPE_create_access`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_ENTITY_TYPE_create_access/).

### hook\_entity\_create\_access

```
function hook_entity_create_access(\Drupal\Core\Session\AccountInterface $account, array $context, $entity_bundle) {
  // No opinion.
  return AccessResult::neutral();
}
```

### hook\_ENTITY\_TYPE\_create\_access

```
function hook_ENTITY_TYPE_create_access(\Drupal\Core\Session\AccountInterface $account, array $context, $entity_bundle) {
  // No opinion.
  return AccessResult::neutral();
}
```

## Recap

The Entity API provides hooks for interacting with the entire Create, Read, Update and Delete (CRUD) life cycle of entities. It also provides nearly identical hooks that allow us to target a particular type rather than all entities. There are similar hooks for working with entity revisions and translations, too. We're also able to use hooks defined by the Entity API to work with the entity forms before they're displayed, add information to our entities just before they're handed off to the rendering system, and affect access control.

## Further your understanding

- The only non-test harness implementation of `hook_ENTITY_TYPE_create` in core is used by the Field UI. What is it used for?
- How does the comment system make use of `hook_entity_view`?
- How does the comment system make use of `hook_entity_predelete`?

## Additional resources

- [Entity API Documentation](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/group/entity_api/) (Drupal.org)
- [New hook\_entity\_revision\_create() and hook\_ENTITY\_TYPE\_revision\_create() hooks](https://www.drupal.org/node/2985957) (Drupal.org)
- [Fields and widgets have more control about affecting changes and pending revision translations](https://www.drupal.org/node/2975280) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Find Data with EntityQuery](/tutorial/find-data-entityquery?p=2607)

Next
[Modify Existing Entities with Alter Hooks](/tutorial/modify-existing-entities-alter-hooks?p=2607)

Clear History

Ask Drupalize.Me AI

close