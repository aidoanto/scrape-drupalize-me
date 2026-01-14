---
title: "Entity Access Control"
url: "https://drupalize.me/tutorial/entity-access-control?p=2607"
guide: "[[work-data-modules]]"
order: 12
---

# Entity Access Control

## Content

One of Drupal's strengths is its fine-grained permission and access system. The Entity API enables this by providing interfaces that let us define access control rules.

In this tutorial we'll:

- Look at how access control is handled, using Drupal core as an example.
- Demonstrate how to implement access control in a custom module.
- Learn about the hooks that allow developers to modify access control for entities provided by another module.

By the end of this tutorial you should have a better understanding of the entity access control system and how to work with it.

## Goal

Understand how to implement or alter access control for entities.

## Prerequisites

- [Entity API Implementation Basics](https://drupalize.me/tutorial/entity-api-implementation-basics)
- [What Are Hooks?](https://drupalize.me/tutorial/what-are-hooks)
- [Implement Any Hook](https://drupalize.me/tutorial/implement-any-hook)
- [Plugins](https://drupalize.me/tutorial/what-are-plugins)
- [PHP Attributes](https://drupalize.me/tutorial/php-attributes)
- [Create a Custom Content Entity](https://drupalize.me/tutorial/create-custom-content-entity)

## Entity access control

If you're already familiar with [Entity API implementation basics](https://drupalize.me/tutorial/entity-api-implementation-basics), you know that the behavior of each entity is defined by a `#[ContentEntityType]` attribute. These attributes also specify how access control works for that particular entity type. Let's take a look at an example from Drupal core for the entities created by the menu system.

Menu links are a content entity created by the *menu\_link\_content* module. We can find the entity type definition for menu links in the class within */core/modules/menu\_link\_content/src/Entity/MenuLinkContent.php*. In particular, let's look at the `#[ContentEntityType]` attribute from this file.

```
/**
 * Defines the menu link content entity class.
 *
 * @property \Drupal\Core\Field\FieldItemList $link
 * @property \Drupal\Core\Field\FieldItemList $rediscover
 */
#[ContentEntityType(
  id: 'menu_link_content',
  label: new TranslatableMarkup('Custom menu link'),
  label_collection: new TranslatableMarkup('Custom menu links'),
  label_singular: new TranslatableMarkup('custom menu link'),
  label_plural: new TranslatableMarkup('custom menu links'),
  entity_keys: [
    'id' => 'id',
    'revision' => 'revision_id',
    'label' => 'title',
    'langcode' => 'langcode',
    'uuid' => 'uuid',
    'bundle' => 'bundle',
    'published' => 'enabled',
  ],
  handlers: [
    'storage' => MenuLinkContentStorage::class,
    'storage_schema' => MenuLinkContentStorageSchema::class,
    'access' => MenuLinkContentAccessControlHandler::class,
    'form' => [
      'default' => MenuLinkContentForm::class,
      'delete' => MenuLinkContentDeleteForm::class,
    ],
    'list_builder' => MenuLinkListBuilder::class,
  ],
  links: [
    'canonical' => '/admin/structure/menu/item/{menu_link_content}/edit',
    'edit-form' => '/admin/structure/menu/item/{menu_link_content}/edit',
    'delete-form' => '/admin/structure/menu/item/{menu_link_content}/delete',
  ],
  admin_permission: 'administer menu',
  base_table: 'menu_link_content',
  data_table: 'menu_link_content_data',
  revision_table: 'menu_link_content_revision',
  revision_data_table: 'menu_link_content_field_revision',
  translatable: TRUE,
  label_count: [
    'singular' => '@count custom menu link',
    'plural' => '@count custom menu links',
  ],
  constraints: [
    'MenuTreeHierarchy' => [],
  ],
  revision_metadata_keys: [
    'revision_user' => 'revision_user',
    'revision_created' => 'revision_created',
    'revision_log_message' => 'revision_log_message',
  ],
  )]
class MenuLinkContent extends EditorialContentEntityBase implements MenuLinkContentInterface {}
```

Notice that the `access` key under `handlers` assigns a dedicated access-control class. That class is responsible for evaluating every access check for entities of this type.

Next, let's look at the file that provides this access control handler class in more detail: */core/modules/menu\_link\_content/src/MenuLinkContentAccessControlHandler.php*. This class extends `EntityAccessControlHandler`, which provides the default implementation for entity access control. The `EntityAccessControlHandler` class is also used if no access handler is specified in the `ContentEntityType` attribute.

The access control for menu links is a bit simpler than that of other content entities. Since they're not directly viewed, the access control we're concerned about in this class has to do with the create, update, and delete operations. The `checkAccess()` method does most of this work for us.

```
protected function checkAccess(EntityInterface $entity, $operation, AccountInterface $account) {
    switch ($operation) {
      case 'view':
        // There is no direct viewing of a menu link, but still for purposes of
        // content_translation we need a generic way to check access.
        return AccessResult::allowedIfHasPermission($account, 'administer menu');

      case 'update':
        if (!$account->hasPermission('administer menu')) {
          return AccessResult::neutral("The 'administer menu' permission is required.")->cachePerPermissions();
        }
        else {
          // Assume that access is allowed.
          $access = AccessResult::allowed()->cachePerPermissions()->addCacheableDependency($entity);
          /** @var \Drupal\menu_link_content\MenuLinkContentInterface $entity */
          // If the link is routed determine whether the user has access unless
          // they have the 'link to any page' permission.
          if (!$account->hasPermission('link to any page') && ($url_object = $entity->getUrlObject()) && $url_object->isRouted()) {
            $link_access = $this->accessManager->checkNamedRoute($url_object->getRouteName(), $url_object->getRouteParameters(), $account, TRUE);
            $access = $access->andIf($link_access);
          }
          return $access;
        }

      case 'delete':
        return AccessResult::allowedIfHasPermission($account, 'administer menu')
          ->andIf(AccessResult::allowedIf(!$entity->isNew())->addCacheableDependency($entity));

      default:
        return parent::checkAccess($entity, $operation, $account);
    }
  }
```

Here we can see the code responsible for performing access checks for the view, update, and delete operations. For updates, there is a check to see if the account has the `'administer menu'` permission. If it does not, `AccessResult::neutral` is returned with an additional message about the missing permission.

This may be a bit confusing, so let's step back and see what the possible return values are. There are three different possible return values for an access check:

- allowed (explicit final say)
- forbidden (explicit final say)
- neutral

Generally speaking, providing a return value of either **allowed** or **forbidden** gives your code the final say on the access permissions of this entity. Returning a result of **neutral** allows other modules to interact with this access query before a definitive answer is made. This is a common pattern in Drupal core, but as we'll see later is less common when working with a custom entity.

On the other hand, if the account does have the `'administer menu'` permission, we explicitly return an `AccessResult::allowed()` object. Notice that as this object is constructed, we're also calling a pair of helper methods to add cacheability metadata about the permissions and granularity of this access control. This helps speed up access control checking so we don't have to execute this code any more often than is required.

When it is time to actually render our menu link entities, access can be determined by calling the `access()` method directly on the entity `$entity->access($operation)`. In this case, the access method that is called is `EntityAccessControlHandler::access`, which is reproduced in part below: (from */core/lib/Drupal/Core/Entity/EntityAccessControlHandler.php*)

```
  public function access(EntityInterface $entity, $operation, AccountInterface $account = NULL, $return_as_object = FALSE) {
...
// We grant access to the entity if both of these conditions are met:
    // - No modules say to deny access.
    // - At least one module says to grant access.
    $access = array_merge(
      $this->moduleHandler()->invokeAll('entity_access', [$entity, $operation, $account]),
      $this->moduleHandler()->invokeAll($entity->getEntityTypeId() . '_access', [$entity, $operation, $account])
    );

    $return = $this->processAccessHookResults($access);

    // Also execute the default access check except when the access result is
    // already forbidden, as in that case, it can not be anything else.
    if (!$return->isForbidden()) {
      $return = $return->orIf($this->checkAccess($entity, $operation, $account));
    }
    $result = $this->setCache($return, $entity->uuid(), $operation, $langcode, $account);
    return $return_as_object ? $result : $result->isAllowed();
...
}
```

From the code documentation within this method, we can see that by returning `AccessResult::neutral`, we will be implicitly denying access since our access control depends on a module explicitly returning an allowed (or forbidden) result. This code also gives us a clue as to how we can modify the access control results for entities defined by other modules.

## Modifying access control

Looking at the code in `EntityAccessControlHandler::access`, there are two calls to `$this->moduleHandler()->invokeAll()`. This is how Drupal invokes particular hooks that allow modules to alter the behavior of each other. In this case, this access method is invoking two hooks back-to-back and merging the results they return. The first hook that is called is [`hook_entity_access`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_access/). This hook is passed an entity along with operation and account objects in order to allow custom modules to affect the access control of any entity.

The second hook that is invoked in this `access()` method provides a bit more granularity and allows you to target a particular entity type. This hook uses the dynamic entity type id to construct the access hook name [hook\_ENTITY\_TYPE\_access](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_ENTITY_TYPE_access/). Using this hook is preferred whenever possible, since it allows you to encapsulate the access control operations for a particular entity type within a single hook. These hooks both provide a (relatively) lightweight way of affecting the access control of entities defined by other modules without having to go to the trouble of fundamentally changing the way their access control works.

## Access control in custom entities

Let's look at how to go about implementing access control for a custom entity. For this example, we're going to use a hypothetical contact entity similar to the one in the [Examples](https://www.drupal.org/project/examples) project. The `#[ContentEntityType]` attribute for this contact entity (shown below) defines an `access` handler that maps to a custom class named `Drupal\content_entity_example\ContactAccessControlHandler`:

```
use Drupal\Core\Entity\Attribute\ContentEntityType;
use Drupal\Core\StringTranslation\TranslatableMarkup;

#[ContentEntityType(
  id: 'content_entity_example_contact',
  label: new TranslatableMarkup('Contact entity'),
  handlers: [
    'view_builder' => 'Drupal\Core\Entity\EntityViewBuilder',
    'list_builder' => 'Drupal\content_entity_example\Entity\Controller\ContactListBuilder',
    'form' => [
      'add' => 'Drupal\content_entity_example\Form\ContactForm',
      'edit' => 'Drupal\content_entity_example\Form\ContactForm',
      'delete' => 'Drupal\content_entity_example\Form\ContactDeleteForm',
    ],
    'access' => 'Drupal\content_entity_example\ContactAccessControlHandler',
  ],
  list_cache_contexts: ['user'],
  base_table: 'contact',
  admin_permission: 'administer content_entity_example entity',
  entity_keys: [
    'id' => 'id',
    'label' => 'name',
    'uuid' => 'uuid',
  ],
  links: [
    'canonical' => '/content_entity_example_contact/{content_entity_example_contact}',
    'edit-form' => '/content_entity_example_contact/{content_entity_example_contact}/edit',
    'delete-form' => '/contact/{content_entity_example_contact}/delete',
    'collection' => '/content_entity_example_contact/list',
  ],
  field_ui_base_route: 'content_entity_example.contact_settings',
)]
```

The `ContactAccessControlHandler` class would be located in *src/ContactAccessControlHandler.php*. Since this is the class that actually implements the access control for our Contact entities, let's look at it in a bit more detail.

```
<?php

namespace Drupal\content_entity_example;

use Drupal\Core\Access\AccessResult;
use Drupal\Core\Entity\EntityAccessControlHandler;
use Drupal\Core\Entity\EntityInterface;
use Drupal\Core\Session\AccountInterface;

/**
 * Access controller for the comment entity.
 *
 * @see \Drupal\comment\Entity\Comment.
 */
class ContactAccessControlHandler extends EntityAccessControlHandler {

  /**
   * {@inheritdoc}
   *
   * Link the activities to the permissions. checkAccess is called with the
   * $operation as defined in the routing.yml file.
   */
  protected function checkAccess(EntityInterface $entity, $operation, AccountInterface $account) {
    switch ($operation) {
      case 'view':
        return AccessResult::allowedIfHasPermission($account, 'view contact entity');

      case 'edit':
        return AccessResult::allowedIfHasPermission($account, 'edit contact entity');

      case 'delete':
        return AccessResult::allowedIfHasPermission($account, 'delete contact entity');
    }
    return AccessResult::allowed();
  }

  /**
   * {@inheritdoc}
   *
   * Separate from the checkAccess because the entity does not yet exist, it
   * will be created during the 'add' process.
   */
  protected function checkCreateAccess(AccountInterface $account, array $context, $entity_bundle = NULL) {
    return AccessResult::allowedIfHasPermission($account, 'add contact entity');
  }

}
```

Compared to the access control we looked at with menu links, this implementation is relatively straightforward. The `checkAccess()` method is looking for a particular permission for each type of operation (view, edit, delete) that can be performed on this entity. The `AccessResult` object that is returned uses the `allowedIfHasPermission()` method to do a comparison between the account object being passed in and a string that represents a particular permission. In this case, the permission is also defined by the *content\_entity\_example* module (in */modules/examples/content\_entity\_example/content\_entity\_example.permissions.yml*), but you could use any existing permission in your implementation.

As an aside, if you rely on an existing permission from another module, it would be a good idea to add this module as a dependency in the info file for your custom module. Since the create operation doesn't already have an existing entity, there is also a second method, `checkCreateAccess()`, to do a similar permission check for that operation.

## Recap

In this tutorial, we saw how the Entity API implements access control through a couple of examples. We looked at how Drupal core implements access control for the menu link entities, and how the 3 types of `AccessResult` values work. We then looked at a couple of hooks that could be used in custom code to alter the access control of other entity types. Finally, we took a look at how we could implement access control for our own custom entity type.

## Further your understanding

- There is one implementation of `hook_entity_access()` in Drupal core (not counting tests). Can you find it? What kind of access control is it setting up?
- There is one implementation of `hook_ENTITY_TYPE_access()` in Drupal core (not counting tests). Can you find it?
- While `AccessResult::allowedIfHasPermission` is a useful way to check for a particular permission, how might you go about checking for multiple permissions before deciding on a particular `AccessResult`?

## Additional resources

- [Examples module](https://www.drupal.org/project/examples) (Drupal.org)
- [Completed example code](https://git.drupalcode.org/project/examples/-/tree/3.x/modules/content_entity_example) (Drupal.org)
- [Entity API](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/group/entity_api/) (Drupal.org)
- [Change record: Allow contrib/custom modules to grant field-level access to User fields](https://www.drupal.org/node/2882674) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Entity Validation API](/tutorial/entity-validation-api?p=2607)

Next
[Typed Data API](/tutorial/typed-data-api?p=2607)

Clear History

Ask Drupalize.Me AI

close