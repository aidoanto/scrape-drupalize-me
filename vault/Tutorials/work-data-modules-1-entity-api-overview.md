---
title: "Entity API Overviewfree"
url: "https://drupalize.me/tutorial/entity-api-overview?p=2607"
guide: "[[work-data-modules]]"
order: 1
---

# Entity API Overviewfree

## Content

When learning Drupal development, it won't be long before you encounter the word "entity" and the Entity API. But what are entities in Drupal? How can you use them to build your site? When should you use the Entity API?

This tutorial will explain Drupal's Entity system from a high level. We'll look at:

- The main problems the Entity system solves
- Key terms you should know
- Key concepts we'll explore as we dive into Drupal's Entity API

By the end of this tutorial, you should be able to explain the problems that the Entity API solves, and when you should use it in your own code.

## Goal

Provide an introduction to the Drupal Entity API.

## Prerequisites

- [1.5. Concept: Types of Data](https://drupalize.me/tutorial/user-guide/understanding-data?p=3081)
- [Chapter 6. Setting Up Content Structure](https://drupalize.me/course/user-guide/content-structure-chapter)

## What are entities?

Entities are the basic building blocks of Drupal's data model. They make up, in one way or another, all of the visible content a user interacts with on a Drupal-powered site. There are several types of entities included in Drupal core that make up both the configuration and content of a default installation. It's important to understand the basic differences between these two types of entities before we really dig in further.

**[Configuration entities](https://drupalize.me/tutorial/configuration-data-types)** are objects that allow us to store information (and default values) for configurable settings on our site. Examples of configuration entities in core include image styles, user roles and displays in views. Configuration entities can be exported via core's configuration management system. They can also be used to provide default configuration used during the installation process or when a new module is enabled. Configuration entities support translation, but they cannot have user-configured fields attached to them. The data structure of a configuration entity is limited to what is provided by module code.

**Content entities** are configurable, support translation and revisions, and allow additional fields to be attached for more complex data modeling. Content entities included in core include nodes, taxonomy terms, blocks, and users.

Often, you will find entity variants that come in pairs. The Block module, for example, provides configuration entities to define custom block types and content entities to provide the actual content of custom blocks.

## Key terms in Drupal's Entity API

Now that we have a little better idea of what Drupal means by the word entity, let's look at some other key terms that we'll need to know in order to understand Drupal's Entity API.

### Bundles

Bundles are another generic noun, used to describe containers for a sub-type of a particular entity. For example, nodes are a type of entity. The node entity has a bundle for each content type (i.e., article, page, blog post, etc.). Taxonomy is another entity type, and each individual vocabulary is its own bundle. Bundles provide an organizational abstraction layer that allows for differences in field definitions and configurations between entity sub-types. For a particular entity type (i.e., node), all bundles (article, page, etc.) will have the same base fields (title, author) but will have different bundle fields (articles have tags).

### Fields

Fields consist of individual (or compound) data elements that make up the details of the data model. If you're trying to build a photo gallery, your node type will need some method of collecting images. An image field would be handy in this case. Drupal core provides [several different types of fields](https://www.drupal.org/docs/drupal-apis/entity-api/fieldtypes-fieldwidgets-and-fieldformatters), including boolean, decimal, float, integer, entity reference, link, image, email, telephone, and several text fields. Fields, in turn, are built on top of the actual data primitives in Drupal, [Typed Data](https://www.drupal.org/node/1795854). Fields can be added to content entities, and field configuration will vary between bundles of the same entity type.

### Plugins

In short, plugins provide developers with an API to encapsulate reusable behavior. Plugins are used throughout Drupal core, and you'll be exposed to several of them while working with the Entity API. We have several tutorials that cover plugins in more depth, starting with [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins) in our [Drupal Module Development Guide](https://drupalize.me/guide/drupal-module-developer-guide).

### PHP Attributes

[PHP Attributes](https://drupalize.me/tutorial/php-attributes) provide metadata and shared configuration when defining a new entity type. The Entity API uses attributes to discover which classes to load for a particular entity type (among other things).

### Annotations

Prior to Drupal 11, the Entity API used [annotations](https://drupalize.me/tutorial/annotations) to define the metadata and common configuration for an entity type. Current best practice uses [PHP attributes](https://drupalize.me/tutorial/php-attributes) instead. However, given that annotations were used for many years (and are still supported via a backwards compatibility layer), you'll likely encounter them in code you work with, so it's wise to understand how they operate.

### Handlers

If you've worked with the Entity API in previous versions of Drupal, you're probably already familiar with controllers. Handlers are Drupal's latest equivalent of Drupal 7's controllers.

[Handlers](https://www.drupal.org/docs/drupal-apis/entity-api/handlers) are responsible for acting on and with entities. They help manage things like storage, access control, building lists and views of entities, and the forms required for creating, viewing, updating, and deleting entities.

## Differences from Drupal 7's Entity API

If you already have experience with the Entity API in previous versions of Drupal and you're familiar with the [Entity contrib module](https://www.drupal.org/project/entity), much of this probably seems quite familiar. The Entity API was introduced late in the development cycle for Drupal 7. As such, it wasn't completely functional on its own. In practice, most implementations either required this contributed module or were left recreating much of its functionality. Drupal 7's version of the Entity API had to account for differences in accessing and working with entity properties (things like the node title and published status) and fields (things like images, reference fields, etc). This interface is now unified in Drupal because everything is a field. Developers interact with fields using the same techniques regardless of whether they are base fields or bundle fields. Also, the method used for querying entity information, the `EntityFieldQuery` class, had limited functionality in core in Drupal 7. The method for querying entities has now been simplified in Drupal, yet it is simultaneously more powerful through chaining.

Here are a few illustrative examples of these differences:

### Printing a field value

#### ...in Drupal 7

```
print $node->field_name[LANGUAGE_NONE][0]['value'];
```

#### ...now in Drupal

```
print $node->field_name->value;

// Or chaining to a referenced entity.
$author_name = $node->uid->entity->name->value;
```

### Getting a field definition

#### ...in Drupal 7

```
$field = field_info_field($field_name);
$instance = field_info_instance($entity_type, $field_name, $bundle);
```

#### ...now in Drupal

```
$field_definition = $entity->field_name->getFieldDefinition();
```

### Saving a field value

#### ...in Drupal 7

```
$node->field_name[LANGUAGE_NONE][0]['value'] = 'Hello world';
$node->save();
```

#### ...now in Drupal

```
$node->field_name->value = 'Hello world';
$node->save();
```

## Recap

The Entity API in Drupal provides the basic organizational mechanisms for creating the site's content model. Since everything in Drupal is an entity, it's important to understand the distinction between configuration and content entities. Likewise, since an entity's properties and values are all fields (base or bundle) we have a unified method of working with them. It's important to understand the relationship between entity types, bundles and fields and how each layer can be used in content modeling.

## Further your understanding

- What criteria could you use to decide if you need to implement a configuration or a content entity?
- Can you identify the entity types included in a standard installation of Drupal?
- Can you identify the bundles of the node entity type? How about categorizing all of a node's data as either a base field or a bundle field?

## Additional resources

- [Overview of Configuration (vs. other types of information)](https://www.drupal.org/node/2120523) (Drupal.org)
- [Create a Configuration Entity Type](https://drupalize.me/tutorial/create-configuration-entity-type) (Drupalize.Me)
- [Entity API implements Typed Data API](https://www.drupal.org/node/1795854) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Entity API Implementation Basics](/tutorial/entity-api-implementation-basics?p=2607)

Clear History

Ask Drupalize.Me AI

close