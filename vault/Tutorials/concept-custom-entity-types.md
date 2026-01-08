---
title: "Concept: Custom Entity Types"
url: "https://drupalize.me/tutorial/concept-custom-entity-types?p=3243"
guide: "[[drupal-module-developer-guide]]"
---

# Concept: Custom Entity Types

## Content

Drupal's Entity API enables us to define custom content entity types. It provides a structured approach to store custom data. Creating a custom entity makes sense when built-in entity types like nodes or taxonomy terms don't meet the specific requirements of a project. Custom entities allow for custom data structures, and use Drupal's core features such as access control, Views integration, and JSON:API support. Using the Entity API to create custom content entities ensures your custom data will be compatible with other Drupal modules.

In this tutorial, we'll:

- Discuss use cases for custom content entities.
- Get a high-level overview of defining a custom entity type.
- Provide additional resources where you can learn more about defining custom entity types.

By the end of this tutorial, you'll understand the use case for custom content entities and how to begin defining one.

## Goal

Understand when to use custom content entities and the overall process of creating one.

## Prerequisites

- [Concept: Entity API and Data Storage](https://drupalize.me/tutorial/concept-entity-api-and-data-storage)
- [Implement a Block Plugin](https://drupalize.me/tutorial/implement-block-plugin)

## When to use custom entity types

While adding fields to an existing entity type is a common way of creating custom data models in Drupal, sometimes that isn't the right approach. Here are some example use cases for when it makes sense to create a custom entity type for your Drupal application.

### Example use cases

- Managing data with intricate relationships or custom behaviors.
- Handling application-specific data that requires specific storage, validation, or display logic.
- Retrieving and storing data from external APIs as entities so the data can be integrated with Drupal's other systems like Views.

The creation of custom entity types is common enough that you should be aware of it, but it's not something you'll do frequently.

## How a custom entity type is defined

**Tip**: The quickest way to get started with a new custom entity type is to use the `drush generate entity:content` command.

Entity types in Drupal are defined as [annotated class plugins](https://drupalize.me/tutorial/concept-what-are-plugins). Below is an example that defines a custom *Contact* entity type. This example uses custom handlers and access control:

```
<?php

namespace Drupal\content_entity_example\Entity;

use Drupal\Core\Entity\EntityStorageInterface;
use Drupal\Core\Field\BaseFieldDefinition;
use Drupal\Core\Entity\ContentEntityBase;
use Drupal\Core\Entity\EntityTypeInterface;
use Drupal\content_entity_example\ContactInterface;
use Drupal\Core\Entity\EntityChangedTrait;
use Drupal\user\EntityOwnerTrait;

/**
 * Defines the ContentEntityExample entity.
 *
 * @ingroup content_entity_example
 *
 *  The following annotation is the actual definition of the entity type which
 *  is read and cached. Don't forget to clear cache after changes.
 *
 * @ContentEntityType(
 *   id = "content_entity_example_contact",
 *   label = @Translation("Contact entity"),
 *   handlers = {
 *     "list_builder" = "Drupal\content_entity_example\Entity\Controller\ContactListBuilder",
 *		 "views_data" = "Drupal\views\EntityViewsData",
 *     "access" = "Drupal\content_entity_example\ContactAccessControlHandler",
 *     "form" = {
 *       "add" = "Drupal\content_entity_example\Form\ContactForm",
 *       "edit" = "Drupal\content_entity_example\Form\ContactForm",
 *       "delete" = "Drupal\Core\Entity\ContentEntityDeleteForm",
 *     },
 *     "route_provider" = {
 *       "html" = "Drupal\Core\Entity\Routing\AdminHtmlRouteProvider",
 *     }
 *   },
 *   list_cache_contexts = { "user" },
 *   base_table = "contact",
 *   admin_permission = "administer contact entity",
 *   entity_keys = {
 *     "id" = "id",
 *     "label" = "name",
 *     "uuid" = "uuid",
 *     "owner" = "user_id",
 *   },
 *   links = {
 *     "canonical" = "/content_entity_example_contact/{content_entity_example_contact}",
 *     "add-form" = "/content_entity_example_contact/add",
 *     "edit-form" = "/content_entity_example_contact/{content_entity_example_contact}/edit",
 *     "delete-form" = "/contact/{content_entity_example_contact}/delete",
 *     "collection" = "/content_entity_example_contact/list"
 *   },
 *   field_ui_base_route = "content_entity_example.contact_settings",
 * )
 */

class Contact extends ContentEntityBase implements ContactInterface {
  
  /**
   * {@inheritDoc}
   */
  public static function baseFieldDefinitions(EntityTypeInterface $entity_type) {
    $fields = parent::baseFieldDefinitions($entity_type);

    $fields['name'] = BaseFieldDefinition::create('string')
      ->setLabel($this->t('Name'))
      ->setDescription($this->t('The name of the contact'))
      ->setRequired(TRUE);

    // Additional base fields defined here.

    return $fields;
  }

}
```

## Contributed module alternatives

There are numerous contributed modules like [Paragraphs](https://www.drupal.org/project/paragraphs), and [Entity Construction Kit (ECK)](https://www.drupal.org/project/eck) that can often remove the need to write a module that defines a custom entity type.

## Learn more

- As mentioned above, the `drush generate content:entity` command is a good starting point.
- The tutorial [Create a Custom Content Entity](https://drupalize.me/tutorial/create-custom-content-entity) goes into more details.
- The [Examples for Developers](https://www.drupal.org/project/examples) project contains a complete working example of defining a custom entity type and integrating it with Views and other Drupal core subsystems.

## Recap

Custom entity types provide a powerful way to customize data models in Drupal because they integrate seamlessly with core functionalities. This tutorial introduced the concept of custom entity types, and provided guidance on learning more about how they are created.

## Further your understanding

- Explore Drupal's Entity API and core entities to grasp the potential of custom entities.
- Evaluate how custom entities could enhance data management and functionality in your Drupal projects.

## Additional resources

- [Create a Custom Content Entity](https://drupalize.me/tutorial/create-custom-content-entity) (Drupalize.Me)
- [Creating a custom content entity](https://www.drupal.org/docs/drupal-apis/entity-api/creating-a-custom-content-entity) (Drupal.org)
- [Entity API](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/group/entity_api/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Display a List of Vendors](/tutorial/display-list-vendors?p=3243)

Clear History

Ask Drupalize.Me AI

close