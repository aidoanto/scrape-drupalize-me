---
title: "ContentEntityType Attribute: Properties Reference"
url: "https://drupalize.me/tutorial/contententitytype-attribute-properties-reference?p=2607"
guide: "[[work-data-modules]]"
order: 4
---

# ContentEntityType Attribute: Properties Reference

## Content

This reference document contains a detailed list of available properties for the `#[ContentEntityType]` attribute in Drupal 11. The current documentation in the Drupal 11 code base lists, but doesn't always describe, each of these properties. Or, in many cases, the property is an associative array where the nested key/value pairs are important, but what they should be isn't well documented. So we've created this helpful reference. Most of the properties listed here will also apply to `#[ConfigEntityType]` attributes. These properties define the metadata and behavior of custom entity types.

In this tutorial, we'll:

- Look at an example of how to use `#[ContentEntityType]` attributes.
- Provide a comprehensive list of available properties and a description of each.
- Show detailed examples of using nested array properties like `handlers[]`.

By the end of this tutorial, you should be able to understand how and when to use any of the properties of a `#[ContentEntityType]` attribute in order to modify the behavior of a custom entity type.

## Goal

Provide a list of the properties available on the `#[ContentEntityType]` attribute, all in one place.

## Prerequisites

- [Entity API Implementation Basics](https://drupalize.me/tutorial/entity-api-implementation-basics)
- [PHP Attributes](https://drupalize.me/tutorial/php-attributes)

## Usage example

The `#[ContentEntityType]` attribute is a required part of defining a custom entity type. See [Entity API Implementation Basics](https://drupalize.me/tutorial/entity-api-implementation-basics) for more information about defining custom entity types.

```
use Drupal\Core\Entity\ContentEntityBase;
use Drupal\Core\Entity\Attribute\ContentEntityType;
use Drupal\Core\StringTranslation\TranslatableMarkup;

/**
 * My custom entity type.
 */
#[ContentEntityType(
  id: 'my_entity',
  label: new TranslatableMarkup('My Entity'),
  // ... additional properties
)]
class MyEntity extends ContentEntityBase {
  // Entity implementation
}
```

## Complete `ContentEntityType` property reference

The `ContentEntityType` attribute extends the base `EntityType` attribute, inheriting all its properties and adding content-specific functionality.

### Core identification properties

| Property | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `id` | `string` | **Yes** | None | Machine name of the entity type. Must be unique, lowercase, and max 32 characters. Tip: Start with your module name. |
| `label` | `TranslatableMarkup` | **Yes** | None | Human-readable name for the entity type (singular form). |
| `label_collection` | `TranslatableMarkup` | No | Value of `label` | Collective name for a group of entities. Example: "Users" for user entities. |
| `label_singular` | `TranslatableMarkup` | No | Value of `label` | Explicit singular form. Example: "user". |
| `label_plural` | `TranslatableMarkup` | No | Value of `label_collection` | Explicit plural form. Example: "users". |
| `label_count` | `array` or `PluralTranslatableMarkup` | No | None | Provides countable labels. Example: `'singular' => '@count user', 'plural' => '@count users'`. |

### Grouping and organization

| Property | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `group` | `string` | No | `'content'` | Machine name of the entity type group. Content entities default to `'content'`; config entities default to `'configuration'`. |
| `group_label` | `TranslatableMarkup` | No | `new TranslatableMarkup('Content')` | Human-readable label for the entity type group in admin interfaces. |

### Handler classes

| Property | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `handlers` | `array` | No | `[]` | Array of handler types mapped to their implementation classes. |

While an entity represents a specific piece of data, handlers are responsible for acting on and with that data. The `handlers` array maps *handler types* to their implementation classes. We generally recommend extending the existing handlers and implementing your custom logic on top of that.

Example using common core-provided handlers:

```
handlers: [
  'storage' => 'Drupal\Core\Entity\Sql\SqlContentEntityStorage',
  'view_builder' => 'Drupal\Core\Entity\EntityViewBuilder',
  'list_builder' => 'Drupal\Core\Entity\EntityListBuilder',
  'access' => 'Drupal\Core\Entity\EntityAccessControlHandler',
  'form' => [
    'default' => 'Drupal\Core\Entity\ContentEntityForm',
    'delete' => 'Drupal\Core\Entity\ContentEntityDeleteForm',
  ],
],
```

#### Sub-keys of `handlers` array

| Handler type | Required | Description | Used by | Interface/Base class | Default (Content) | Default (Config) |
| --- | --- | --- | --- | --- | --- | --- |
| `storage` | Auto-defaults | Handles loading, saving, and deleting entities. | All entities | `EntityStorageInterface` | `SqlContentEntityStorage` | `ConfigEntityStorage` |
| `storage_schema` | Auto-defaults | Manages database schema for the entity type. | Content entities | `EntityStorageSchemaInterface` | `SqlContentEntityStorageSchema` | N/A |
| `view_builder` | Optional | Builds render arrays for entity display. | Displayable entities | `EntityViewBuilderInterface` | `EntityViewBuilder` | `EntityViewBuilder` |
| `list_builder` | Optional | Builds admin listing pages for entities. | Admin UI | `EntityListBuilderInterface` | `EntityListBuilder` | `ConfigEntityListBuilder` |
| `access` | Optional | Controls access to entity operations. | All entities | `EntityAccessControlHandlerInterface` | `EntityAccessControlHandler` | `EntityAccessControlHandler` |
| `form` | Recommended | Handles entity forms (Value can be an array with `add`, `edit`, and `delete` keys to specify different handlers for each operation). | Editable entities | `FormInterface` | `ContentEntityForm` | `EntityForm` |
| `route_provider` | Optional | Automatically generates entity routes. | All entities | `EntityRouteProviderInterface` | None | None |
| `translation` | Conditional | Handles content translation. | Translatable content | `ContentTranslationHandlerInterface` | `ContentTranslationHandler` | N/A |
| `views_data` | Optional | Provides Views integration data. | Views-enabled | `EntityViewsDataInterface` | `EntityViewsData` | N/A |

For additional details, see [EntityTypeInterface::getHandlerClasses](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21EntityTypeInterface.php/function/EntityTypeInterface%3A%3AgetHandlerClasses/) (api.drupal.org).

### Database configuration

| Property | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `base_table` | `string` | **Yes**\* | None | Primary database table name. Required for SQL-stored entities. |
| `data_table` | `string` | No | None | Table for translatable/revisionable field data. Required if the entity is translatable. |
| `revision_table` | `string` | No | None | Table storing revision data. Required if the entity is revisionable. |
| `revision_data_table` | `string` | No | None | Table for translatable revision field data. Required if the entity is **both** translatable and revisionable. |
| `revision_metadata_keys` | `array` | No | `[]` | Maps metadata keys for revisions (revision\_user, revision\_created, revision\_log\_message). |

### Entity keys

| Property | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `entity_keys` | `array` | **Yes** | `[]` | Maps entity property names to field machine names. |

The `entity_keys` array maps standard entity properties to field names. These should map to fields defined in the `baseFields()` method.

```
entity_keys: [
  'id' => 'id',             // Primary identifier (required)
  'uuid' => 'uuid',         // Universal identifier (required)
  'revision' => 'vid',      // Revision ID (for revisionable entities)
  'bundle' => 'type',       // Bundle field (for bundleable entities)
  'label' => 'title',       // Field used as entity label
  'langcode' => 'langcode', // Language code field (for translatable)
  'status' => 'status',     // Published/unpublished status
  'published' => 'status',  // Alias for status
  'uid' => 'uid',           // Owner/author user ID
  'owner' => 'uid',         // Alias for uid
  'default_langcode' => 'default_langcode', // Whether this is default translation
  'revision_translation_affected' => 'revision_translation_affected',
],
```

#### Sub-keys of `entity_keys` array

| Key | Required | Description |
| --- | --- | --- |
| `id` | **Yes** | Primary identifier for the entity. Must be an integer or serial field. |
| `uuid` | **Yes** | Universally unique identifier. Must be a UUID field. |
| `revision` | Conditional | Revision ID. Required if the entity is revisionable. |
| `bundle` | Conditional | Bundle/sub-type field. Required if the entity has bundles. |
| `label` | Recommended | Field to use as the entity's display label. |
| `langcode` | Conditional | Language code field. Required if the entity is translatable. |
| `status` or `published` | Optional | Boolean indicating published status. |
| `uid` or `owner` | Optional | References the user who owns/created the entity. |
| `default_langcode` | Conditional | Boolean indicating if this is the default language. Required for translatable entities. |
| `revision_translation_affected` | Conditional | Boolean indicating if revision affects translation. Required for translatable revisionable entities. |

### Translation support

| Property | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `translatable` | `bool` | No | `FALSE` | Whether the entity type supports translation. |

### Bundle configuration

| Property | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `bundle_label` | `TranslatableMarkup` | No | None | Human-readable name for bundles of this entity type. Example: "Content type" for nodes. |
| `bundle_entity_type` | `string` | No | None | Entity type ID of the bundle configuration entity. Example: `'node_type'` for nodes. |

**Note:** When you're defining the configuration entity that represents bundles (via `#[ConfigEntityType]`), use the `bundle_of` property on that attribute to point back to the parent content entity type.

### Routing and links

| Property | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `links` | `array` | No | `[]` | Maps link types to URL templates. |
| `link_templates` | `array` | No | `[]` | *Deprecated*. Use `links` instead. |
| `field_ui_base_route` | `string` | No | None | Route name where Field UI tabs should appear. Required for fieldable entities with Field UI support. |

The `links` array maps link template types to URL patterns:

```
links: [
  'canonical' => '/myentity/{myentity}',
  'add-page' => '/myentity/add',
  'add-form' => '/myentity/add/{myentity_type}',
  'edit-form' => '/myentity/{myentity}/edit',
  'delete-form' => '/myentity/{myentity}/delete',
  'collection' => '/admin/content/myentity',
  'version-history' => '/myentity/{myentity}/revisions',
  'revision' => '/myentity/{myentity}/revisions/{myentity_revision}/view',
  'revision-revert-form' => '/myentity/{myentity}/revisions/{myentity_revision}/revert',
  'revision-delete-form' => '/myentity/{myentity}/revisions/{myentity_revision}/delete',
],
```

#### Sub-keys of `links` array

| Link Type | Required | Description |
| --- | --- | --- |
| `canonical` | Recommended | Default/main page for viewing the entity. |
| `add-page` | Optional | Page listing available bundles when creating a new entity (for entity types with bundles). |
| `add-form` | Optional | Form for creating a new entity (or entity of a specific bundle). |
| `edit-form` | Recommended | Form for editing an existing entity. |
| `delete-form` | Recommended | Confirmation form for deleting an entity. |
| `collection` | Optional | Administrative listing page for all entities of this type. |
| `version-history` | Conditional | List of revisions (for revisionable entities). |
| `revision` | Conditional | View a specific revision (for revisionable entities). |
| `revision-revert-form` | Conditional | Revert to a specific revision (for revisionable entities). |
| `revision-delete-form` | Conditional | Delete a specific revision (for revisionable entities). |

### Permissions and access

| Property | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `admin_permission` | `string` | No | None | Permission that grants full administrative access to this entity type. |
| `collection_permission` | `string` | No | None | Permission required to view the collection/list of entities. |
| `permission_granularity` | `string` | No | `'entity_type'` | Granularity level for permissions: `'entity_type'` or `'bundle'`. |

### Caching configuration

| Property | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `static_cache` | `bool` | No | `TRUE` | Whether to cache loaded entities in memory during a request. |
| `render_cache` | `bool` | No | `TRUE` | Whether to cache rendered output of entities. |
| `persistent_cache` | `bool` | No | `TRUE` | Whether to cache field values in persistent cache. |
| `list_cache_contexts` | `array` | No | `[]` | Cache contexts for entity lists. Example: `['user']`, `['user.permissions']`. |
| `list_cache_tags` | `array` | No | `[]` | Cache tags for entity lists. Cleared when the list may have changed. |

### UI and display

| Property | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `show_revision_ui` | `bool` | No | `FALSE` | Whether to show revision UI for revisionable entities. |
| `common_reference_target` | `bool` | No | `FALSE` | Promotes entity in Field UI's entity reference field type selector. |

### Internal flags

| Property | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `internal` | `bool` | No | `FALSE` | Whether entity type is internal (not meant for use by other modules). |

### Entity class configuration

| Property | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `entity_type_class` | `string` | No | `'Drupal\Core\Entity\ContentEntityType'` | Class name for the entity type definition object. Usually, this should not be changed. |

### Constraints

| Property | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `constraints` | `array` | No | `[]` | Array of validation constraint plugin IDs to apply to entities of this type. |

## Complete example

Here's a comprehensive example showing many properties in use:

```
<?php

namespace Drupal\mymodule\Entity;

use Drupal\Core\Entity\Attribute\ContentEntityType;
use Drupal\Core\Entity\ContentEntityBase;
use Drupal\Core\Entity\EntityChangedTrait;
use Drupal\Core\Entity\EntityPublishedTrait;
use Drupal\Core\Entity\EntityTypeInterface;
use Drupal\Core\Entity\RevisionLogEntityTrait;
use Drupal\Core\Field\BaseFieldDefinition;
use Drupal\Core\StringTranslation\TranslatableMarkup;

/**
 * Defines the product entity.
 */
#[ContentEntityType(
  id: 'product',
  label: new TranslatableMarkup('Product'),
  label_collection: new TranslatableMarkup('Products'),
  label_singular: new TranslatableMarkup('product'),
  label_plural: new TranslatableMarkup('products'),
  label_count: [
    'singular' => '@count product',
    'plural' => '@count products',
  ],
  bundle_label: new TranslatableMarkup('Product type'),
  handlers: [
    'storage' => 'Drupal\Core\Entity\Sql\SqlContentEntityStorage',
    'storage_schema' => 'Drupal\mymodule\ProductStorageSchema',
    'view_builder' => 'Drupal\Core\Entity\EntityViewBuilder',
    'list_builder' => 'Drupal\mymodule\ProductListBuilder',
    'access' => 'Drupal\mymodule\ProductAccessControlHandler',
    'views_data' => 'Drupal\views\EntityViewsData',
    'translation' => 'Drupal\content_translation\ContentTranslationHandler',
    'form' => [
      'default' => 'Drupal\Core\Entity\ContentEntityForm',
      'add' => 'Drupal\Core\Entity\ContentEntityForm',
      'edit' => 'Drupal\Core\Entity\ContentEntityForm',
      'delete' => 'Drupal\Core\Entity\ContentEntityDeleteForm',
    ],
    'route_provider' => [
      'html' => 'Drupal\Core\Entity\Routing\AdminHtmlRouteProvider',
    ],
  ],
  base_table: 'product',
  data_table: 'product_field_data',
  revision_table: 'product_revision',
  revision_data_table: 'product_field_revision',
  translatable: TRUE,
  show_revision_ui: TRUE,
  entity_keys: [
    'id' => 'id',
    'revision' => 'vid',
    'bundle' => 'type',
    'label' => 'name',
    'uuid' => 'uuid',
    'langcode' => 'langcode',
    'status' => 'status',
    'published' => 'status',
    'uid' => 'user_id',
    'owner' => 'user_id',
    'default_langcode' => 'default_langcode',
    'revision_translation_affected' => 'revision_translation_affected',
  ],
  revision_metadata_keys: [
    'revision_user' => 'revision_user',
    'revision_created' => 'revision_created',
    'revision_log_message' => 'revision_log_message',
  ],
  links: [
    'canonical' => '/product/{product}',
    'add-page' => '/product/add',
    'add-form' => '/product/add/{product_type}',
    'edit-form' => '/product/{product}/edit',
    'delete-form' => '/product/{product}/delete',
    'collection' => '/admin/content/products',
    'version-history' => '/product/{product}/revisions',
    'revision' => '/product/{product}/revisions/{product_revision}/view',
  ],
  bundle_entity_type: 'product_type',
  field_ui_base_route: 'entity.product_type.edit_form',
  admin_permission: 'administer products',
  permission_granularity: 'bundle',
  common_reference_target: TRUE,
  list_cache_contexts: ['user.permissions'],
  list_cache_tags: ['product_list'],
)]
class Product extends ContentEntityBase implements ProductInterface {
  
  use EntityChangedTrait;
  use EntityPublishedTrait;
  use RevisionLogEntityTrait;

  /**
   * {@inheritdoc}
   */
  public static function baseFieldDefinitions(EntityTypeInterface $entity_type) {
    // id, vid, uid, and many common base fields referenced in entity_keys are
    // defined here.
    $fields = parent::baseFieldDefinitions($entity_type);
    
    $fields['name'] = BaseFieldDefinition::create('string')
      ->setLabel(new TranslatableMarkup('Name'))
      ->setRevisionable(TRUE)
      ->setTranslatable(TRUE)
      ->setRequired(TRUE)
      ->setSetting('max_length', 255)
      ->setDisplayConfigurable('view', TRUE)
      ->setDisplayConfigurable('form', TRUE);
      
    $fields['user_id'] = BaseFieldDefinition::create('entity_reference')
      ->setLabel(new TranslatableMarkup('Authored by'))
      ->setRevisionable(TRUE)
      ->setSetting('target_type', 'user')
      ->setDefaultValueCallback(static::class . '::getDefaultEntityOwner')
      ->setDisplayConfigurable('view', TRUE)
      ->setDisplayConfigurable('form', TRUE);
      
    $fields['created'] = BaseFieldDefinition::create('created')
      ->setLabel(new TranslatableMarkup('Created'))
      ->setRevisionable(TRUE);
      
    $fields['changed'] = BaseFieldDefinition::create('changed')
      ->setLabel(new TranslatableMarkup('Changed'))
      ->setRevisionable(TRUE);
    
    return $fields;
  }
}
```

## Usage details

### Required minimums

For a **basic content entity**, you'll need to provide the following at a minimum:

1. `id`: Unique machine name of the entity type.
2. `label`: Human-readable name of the entity type, used in the UI.
3. `base_table`: Database table name. Drupal will create this automatically.
4. `entity_keys`: At minimum `id` and `uuid`.
5. `handlers`: At least form handlers if you want a UI. Start with the core provided handlers, then extend and override if they don't do what you need.

### Commonly modified properties

1. `handlers`: Complete set (storage, view\_builder, list\_builder, access, forms), using core-provided handler classes is fine.
2. `links`: At least canonical, edit-form, delete-form, collection.
3. `admin_permission` or a custom access handler.
4. `bundle_label` and `bundle_entity_type` (if using bundles).
5. `field_ui_base_route` (if entity is fieldable).
6. `translatable: TRUE` and appropriate table structure for multilingual sites.
7. Cache configuration (`list_cache_contexts`, `list_cache_tags`).

### Revisionable entities

If your entity needs revisions:

1. Set `revision_table` and `revision_data_table` (if translatable).
2. Add `revision` to `entity_keys`.
3. Add `revision_metadata_keys` (`revision_user`, `revision_created`, `revision_log_message`).
4. Consider setting `show_revision_ui: TRUE`.
5. Add revision-related links (version-history, revision, etc.).
6. Use `RevisionLogEntityTrait` in your entity class.

### Translatable entities

If your entity supports translation:

1. Set `translatable: TRUE`.
2. Define `data_table` (and `revision_data_table` if revisionable).
3. Add `langcode` and `default_langcode` to `entity_keys`.
4. Add translation handler to `handlers`.
5. Consider `revision_translation_affected` in `entity_keys`.

## Property validation

Drupal will validate your attribute properties when the entity type is discovered. Common errors include:

- **Missing required properties**: `id`, `label`, `base_table`, `entity_keys`.
- **Invalid entity\_keys**: Referencing non-existent fields.
- **Table mismatch**: Translatable without `data_table`, revisionable without `revision_table`.
- **Handler class not found**: Handler references a non-existent class.
- **ID too long**: Entity type ID exceeds 32 characters.

## Recap

In this tutorial, we provided a complete list and a short description of all the different properties used by `#[ContentEntityType]` attributes. Use this as a guide when figuring out your specific use case.

## Further your understanding

- Explore the list of available properties for `#[ConfigEntityType]` attributes. How are they the same/different from those listed above?

## Additional resources

- [Entity API Documentation](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/group/entity_api/) (api.drupal.org)
- [EntityType class](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21EntityType.php/class/EntityType/) (api.drupal.org)
- [ContentEntityType attribute](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21Attribute%21ContentEntityType.php/class/ContentEntityType/) (api.drupal.org)
- [EntityTypeInterface](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21EntityTypeInterface.php/interface/EntityTypeInterface/) (api.drupal.org)
- [Change record: PHP attributes for entity type classes](https://www.drupal.org/node/3330769) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Create a Custom Content Entity](/tutorial/create-custom-content-entity?p=2607)

Next
[Scaffold a Custom Content Entity Type with Drush Generators](/tutorial/scaffold-custom-content-entity-type-drush-generators?p=2607)

Clear History

Ask Drupalize.Me AI

close