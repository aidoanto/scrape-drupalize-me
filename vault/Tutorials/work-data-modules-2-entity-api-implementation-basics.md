---
title: "Entity API Implementation Basics"
url: "https://drupalize.me/tutorial/entity-api-implementation-basics?p=2607"
guide: "[[work-data-modules]]"
order: 2
---

# Entity API Implementation Basics

## Content

Entities are the core data structures that provide the building blocks for nearly everything on a Drupal site. Whether an entity provides configuration or content, it plays a key role in how Drupal stores and manages data. Entities provide a consistent, developer-friendly, and Drupal-aware abstraction to data stored in the database.

In this tutorial, we will:

- Explore how different entity types relate.
- Compare configuration and content entities to understand the purpose and implementation of both.
- Review how (at a high level) an entity type is defined.

By the end of this tutorial, you'll understand the relationship between configuration and content entities and be able to identify the parts of code that define a custom entity type.

## Goal

Understand the structure and terminology behind the Drupal Entity API.

## Prerequisites

- [Entity API Overview](https://drupalize.me/tutorial/entity-api-overview)
- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins)
- [PHP Attributes](https://drupalize.me/tutorial/php-attributes)

## Why create a custom entity type?

You might want to create a custom entity type when your module needs to store or manage structured data that doesn't fit neatly into Drupal's existing entities. Custom entities provide flexibility and reusability while taking advantage of Drupal's robust APIs for storage, access control, form generation, and rendering.

Common reasons to create a custom entity type include:

- You need to define a custom data structure with its own CRUD operations and permissions.
- You want to create reusable content or configuration types that integrate with [Views](https://drupalize.me/topic/views-module-drupal), [fields](https://drupalize.me/topic/fields-and-field-api), and other Drupal APIs.
- You need a lightweight alternative to nodes for data that doesn't require a full editorial workflow.
- You need users to be able to create one or more *configuration entities* for your module, such as image styles or vocabularies.

As a case in point, if you're building a module that manages external API credentials or stores location data for multiple content types, creating a custom configuration or content entity type allows you to model that data cleanly and extend Drupal's core capabilities.

**Tip**: See also the [Drupal Module Developer Guide](https://drupalize.me/guide/drupal-module-developer-guide) chapter on working with data. It includes an introduction to data types in Drupal and project-based tutorials to give you practice working with entities in the UI and in code.

## Configuration entities vs. content entities

You can usually tell which type of entity you're working with by its purpose and class hierarchy.

If the information is primarily edited by *authors* or *editors* and displayed for the site's audience, it's likely a **content entity**. If only *site builders* or *developers* configure it, and its content influences how the site works, it's probably a **configuration entity**.

Here are some examples from Drupal core:

### Configuration entities

- Custom block types
- Views
- Menus
- Roles
- Taxonomy vocabularies

### Content entities

- Custom blocks
- Nodes
- Users
- Taxonomy terms

Configuration entities manage information about how a site is set up, while content entities represent user-facing data.

For more details, see [Configuration Data Types](https://drupalize.me/tutorial/configuration-data-types) and [Create a Configuration Entity Type](https://drupalize.me/tutorial/create-configuration-entity-type).

## Entity types in Drupal core

You can see how entities relate to each other in [Drupal’s entity class hierarchy diagram](../assets/images/entity-api-implementation-basics-0.png).

![](../assets/images/entity-api-implementation-basics-0.png)

From this hierarchy, we can see that:

- Configuration entities extend `\Drupal\Core\Config\Entity\ConfigEntityBase`.
- Content entities extend `\Drupal\Core\Entity\ContentEntityBase`.

Both inherit from `\Drupal\Core\Entity\Entity`, which implements `\Drupal\Core\Entity\EntityInterface`. Comparing their interfaces reveals the key differences.

### `ConfigEntityInterface` methods

Configuration entities focus on storage and synchronization.

- `enable()`, `disable()`, `setStatus()`
- `calculateDependencies()`
- `getDependencies()`, `onDependencyRemoval()`
- `isInstallable()`, `trustData()`

### `ContentEntityInterface` methods

Content entities focus on fields, revisions, and translations.

- `baseFieldDefinitions()`, `bundleFieldDefinitions()`
- `hasField()`, `getFieldDefinition()`
- `validate()`, `isRevisionTranslationAffected()`
- `setRevisionTranslationAffected()`

In short, configuration entities store and sync setup data, while content entities manage fieldable, revisable, and translatable data.

## Content entity basics

Content entities can be *fieldable*, meaning they can have fields attached to them. These fields fall into two categories:

- **Base fields:** Defined by the entity type itself, shared across all bundles.
- **Bundle fields:** Defined at the bundle (subtype) level, specific to one bundle, and usually [configured via the Field UI](https://drupalize.me/tutorial/user-guide/structure-fields).

For example, the node entity type (defined in *core/modules/node/src/Entity/Node.php*) declares its base fields in the `Node::baseFieldDefinitions()` method:

```
public static function baseFieldDefinitions(EntityTypeInterface $entity_type) {
  $fields = parent::baseFieldDefinitions($entity_type);

  $fields['title'] = BaseFieldDefinition::create('string')
    ->setLabel(t('Title'))
    ->setRequired(TRUE)
    ->setTranslatable(TRUE)
    ->setRevisionable(TRUE);

  $fields['uid'] = BaseFieldDefinition::create('entity_reference')
    ->setLabel(t('Authored by'))
    ->setDescription(t('The username of the content author.'))
    ->setSetting('target_type', 'user');

  return $fields;
}
```

Every node, regardless of type, has these **base fields**: title, author, status, created, changed, and others defined in the Node class, or one of the classes it extends.

To see which **bundle fields** exist for a specific content type, use the UI. For example, to see the bundle field for the *Page* node type, go to *Structure* > *Content types* > *Page* > *Manage fields* (*/admin/structure/types/manage/page/fields*).

For example:

- The **Basic Page** content type includes the *body* field.
- The **Article** type adds *body*, *image*, *tags*, and *comments*.

In this context, "shared" fields refer to **base fields**, defined by the entity type and common to all bundles. If you create a custom base class that defines fields used by several bundles, those fields are still considered **base fields**, not bundle fields.

The distinction between *base* and *bundle* fields is important when you're writing code that accesses an entity's field data. With *base* fields, your code can assume that all entities of the same type will have the field. But with bundle fields, because they are user configurable, you'll need to first check for the field's existence before using it.

If you want to identify which base fields an entity type provides:

- Open the entity class and inspect the `baseFieldDefinitions()` method.
- Or use the *Devel Entity Info* tab if you have the [Devel module](https://drupalize.me/topic/devel) installed.

## Entity bundle classes

In Drupal 10 and later, you can define *bundle classes* to represent individual bundles of a content entity type. A bundle class encapsulates logic and behavior specific to one bundle without modifying the parent entity type.

For example, the Article and Page content types are bundles of the Node entity type. A bundle class could define methods, constants, or dependencies specific to one of these bundles.

Bundle classes are useful when:

- You want to encapsulate logic unique to one bundle (for example, default field values or computed properties).
- You need to override behavior for one bundle without affecting others.
- You want a clear separation between shared (entity type) logic and bundle-specific logic.

The Drupalize.Me site uses bundle classes extensively. For example, this site has a *Tutorial* node type, with *bundle* fields added via the UI. In a custom module, we define a `\Drupal\dme\Entity\Tutorial` bundle class that is used for all *Tutorial* nodes. This class defines methods like `Tutorial::isFree()` and `Tutorial::isRead()`. These methods can be used in our theme and elsewhere in our custom code to check if a tutorial "is free" and react accordingly. And, we can change the logic in the `isFree()` method at any point. In the past, this was handled by doing things like `if $node->get('tutorial_is_free')->value == TRUE` all over our custom code. The bundle class approach allows us to avoid hard-coding implementation details.

Each bundle class should extend the entity's base class and can be linked through the `bundle_class` property in the entity type's attribute definition.

Learn more in [Using Entity Bundle Classes for Site-Specific Features](https://drupalize.me/tutorial/using-entity-bundle-classes-site-specific-features).

## EntityType attributes

Every entity type (content or configuration) must include an attribute—`#[ContentEntityType]` or `#[ConfigEntityType]`—so that Drupal can discover it.

**Note:** Prior to Drupal 11, entity types were defined using [annotations](https://drupalize.me/tutorial/annotations). [Attributes](https://drupalize.me/tutorial/php-attributes) are now the preferred method. (But you'll likely encounter both.)

The following example shows the `#[ContentEntityType]` attribute from the Node entity:

```
use Drupal\Core\Entity\Attribute\ContentEntityType;
use Drupal\Core\StringTranslation\TranslatableMarkup;

/**
 * Defines the node entity class.
 */
#[ContentEntityType(
  id: 'node',
  label: new TranslatableMarkup('Content'),
  label_collection: new TranslatableMarkup('Content'),
  label_singular: new TranslatableMarkup('content item'),
  label_plural: new TranslatableMarkup('content items'),
  entity_keys: [
    'id' => 'nid',
    'revision' => 'vid',
    'bundle' => 'type',
    'label' => 'title',
    'langcode' => 'langcode',
    'uuid' => 'uuid',
    'status' => 'status',
    'published' => 'status',
    'uid' => 'uid',
    'owner' => 'uid',
  ],
  handlers: [
    'storage' => NodeStorage::class,
    'storage_schema' => NodeStorageSchema::class,
    'view_builder' => NodeViewBuilder::class,
    'access' => NodeAccessControlHandler::class,
    'views_data' => NodeViewsData::class,
    'form' => [
      'default' => NodeForm::class,
      'delete' => NodeDeleteForm::class,
      'edit' => NodeForm::class,
      'delete-multiple-confirm' => DeleteMultiple::class,
    ],
    'route_provider' => [
      'html' => NodeRouteProvider::class,
    ],
    'list_builder' => NodeListBuilder::class,
    'translation' => NodeTranslationHandler::class,
  ],
  links: [
    'canonical' => '/node/{node}',
    'delete-form' => '/node/{node}/delete',
    'delete-multiple-form' => '/admin/content/node/delete',
    'edit-form' => '/node/{node}/edit',
    'version-history' => '/node/{node}/revisions',
    'revision' => '/node/{node}/revisions/{node_revision}/view',
    'create' => '/node',
  ],
  collection_permission: 'access content overview',
  permission_granularity: 'bundle',
  bundle_entity_type: 'node_type',
  bundle_label: new TranslatableMarkup('Content type'),
  base_table: 'node',
  data_table: 'node_field_data',
  revision_table: 'node_revision',
  revision_data_table: 'node_field_revision',
  translatable: TRUE,
  show_revision_ui: TRUE,
  label_count: [
    'singular' => '@count content item',
    'plural' => '@count content items',
  ],
  field_ui_base_route: 'entity.node_type.edit_form',
  common_reference_target: TRUE,
  list_cache_contexts: ['user.node_grants:view'],
  revision_metadata_keys: [
    'revision_user' => 'revision_uid',
    'revision_created' => 'revision_timestamp',
    'revision_log_message' => 'revision_log',
  ],
)]
class Node extends EditorialContentEntityBase implements NodeInterface {
  // Class implementation...
}
```

This attribute defines metadata such as:

- The entity's ID and labels.
- Storage and access handler classes.
- Table names and translation settings.

The Entity API provides extensive helper classes to facilitate easy creation of custom entity types. This includes handling the UI, access control, translation, revisions, integration with Views, and more. The attribute configuration is used to configure, or completely override, the default behaviors.

You can learn more about using attributes to define a custom entity type in [Create a Custom Content Entity](https://drupalize.me/tutorial/create-custom-content-entity).

## Recap

In this tutorial, we learned how Drupal distinguishes between configuration and content entities, how these relate through inheritance, and how entity metadata is declared using attributes. We also explored the difference between base and bundle fields within content entities.

## Further your understanding

- Create your own `#[ContentEntityType]` attribute for a custom entity type.
- Review how base fields are defined in other core entities like *User* or *Taxonomy term*.

## Additional resources

- [Create a Configuration Entity Type](https://drupalize.me/tutorial/create-configuration-entity-type) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Entity API Overview](/tutorial/entity-api-overview?p=2607)

Next
[Create a Custom Content Entity](/tutorial/create-custom-content-entity?p=2607)

Clear History

Ask Drupalize.Me AI

close