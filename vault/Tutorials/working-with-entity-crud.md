---
title: "Working with Entity CRUD"
url: "https://drupalize.me/tutorial/working-entity-crud"
guide: "[[acquia-certified-drupal-front-end-specialist-exam]]"
---

# Working with Entity CRUD

## Content

Entity CRUD (Create, Read, Update, and Delete) operations are handled via the `EntityTypeManager` service.

In this tutorial we'll:

- Learn how to use the `EntityTypeManager` service to perform basic CRUD operations with examples you can copy/paste
- Access both property and field values of an entity
- Update entities by setting new field values and then saving the object

By the end of this tutorial, you'll be able to understand Entity CRUD operations and be well on your way to becoming comfortable with accessing and manipulating entity values in code.

## Goal

Provide examples of using Entity API to perform CRUD operations.

## Prerequisites

- [Entity API Overview](https://drupalize.me/tutorial/entity-api-overview)

## Background for Drupal 7 developers

In Drupal 7, the [contributed Entity module](https://www.drupal.org/project/entity) was essentially a requirement if you were looking for basic CRUD operations for your custom entities without writing lots of code yourself. Arguably one of the most useful pieces of this contributed module was the `EntityMetadataWrapper` class. This allowed developers to access properties and field values relatively easily. Entity API now uses the `EntityTypeManager` class to help make working with entities a little easier.

## Load an Entity with EntityTypeManager

Entities are loaded using the Entity Storage Manager, which is easiest to access via the Entity Type Manager service.

Examples:

```
// Load via the container with service ID, 'entity_type.manager'.
$node_storage = \Drupal::service('entity_type.manager')->getStorage('node');

// Or, load using the Drupal global object.
$node_storage = \Drupal::entityTypeManager()->getStorage('node');
```

Once you have the appropriate storage manager loaded, you can load complete entity objects:

```
$entity_type = 'node';
$storage = \Drupal::entityTypeManager()->getStorage($entity_type);

// Load a single entity by its ID.
$entity = $storage->load(1);

// Load multiple entities by their IDs. Will return an array of entity objects.
$entities = $storage->loadMultiple([1, 2, 3]);

// Load entities by property values. Returns an array of entity objects.
$entities = $storage->loadByProperties(['type' => 'vendor']);
```

To load entities using complex queries, see [Find Data with EntityQuery](https://drupalize.me/tutorial/find-data-entityquery).

### Note about old examples

Some older documentation and code might use the static `load()` method of the entity object like this:

```
$node = \Drupal\node\Entity\Node::load(22);
```

While still functional, this method is **not recommended** for new code due to lower testability and potential coupling issues.

## Entity CRUD

`EntityTypeManager` is entity type agnostic. One of the big advantages to this is that once you learn how the basic CRUD operations work the same methods work regardless of what type of entity you're working with (blocks, nodes, terms, users, etc). Let's take a look at each of the CRUD operations one by one.

The `EntityTypeManager` implementation of `getStorage` offers some insight into how the service works.

The `EntityTypeManager` is responsible for loading the [plugins](https://drupalize.me/tutorial/what-are-plugins) used for a particular function with a particular entity type (the `getHandler()` method). Most of the methods in `EntityTypeManager` do some type of [plugin discovery](https://drupalize.me/tutorial/plugin-discovery) (when necessary) and then return the relevant handler.

### Create

If you know the class of the entity you're working with, you can use the static `create()` method on the entity class (assuming it has one). For example, for nodes, use the `create()` method in the `\Drupal\node\Entity\Node` class:

```
$node = \Drupal\node\Entity\Node::create(['title' => 'First!']);
$node->save();
```

This approach can potentially vary, in detail, depending on the type of entity you're working with.

Here's what creating a node looks like using the `EntityTypeManager`:

```
$node = \Drupal::entityTypeManager()->getStorage('node')->create(['type' => 'page', 'title' => 'About Us']);
$node->save();
```

### Read

We already covered loading entities when looking at `EntityTypeManager` above. Thankfully the Entity API gives us a straightforward way of reading properties and field values as well.

Let's assume we have our node loaded. We can access the value of the node body in a few ways:

```
$node = \Drupal::entityTypeManager()->getStorage("node")->load(22);

$body_text = $node->body->value;
$body_text = $node->get('body')->value;
$body_array = $node->body->getValue();
```

You might try something similar to see the tags associated with our node. It might be a surprise to learn that `$node->field_tags->value` returns `NULL`. Since the tags field supports multiple values, we have to go about getting multivalue fields using one of the latter two methods.

For example, we can return an array of values for `field_tags` using:

```
$field_tags = $node->field_tags->getValue();
```

This method returns:

```
// Output of $field_tags = $node->field_tags->getValue();

array(3) {
  [0]=>
  array(1) {
    ["target_id"]=>
    string(2) "14"
  }
  [1]=>
  array(1) {
    ["target_id"]=>
    string(1) "7"
  }
  [2]=>
  array(1) {
    ["target_id"]=>
    string(1) "2"
  }
}
```

Let's say we're not interested in displaying the term IDs for those tags, but would prefer to see the actual tag. The Entity API is chainable, so you can get values from other referenced entities like so:

```
// The value of field_tags[1]->entity in this case is a \Drupal\taxonomy\Entity\Term entity.
$second_tag = $node->field_tags[1]->entity->name->value;

// The value of uid->entity is a \Drupal\user\Entity\User entity.
$author_name = $node->uid->entity->name->value;
```

Another handy helper method can also retrieve all of the referenced entities already loaded for you:

```
$tags = $node->field_tags->referencedEntities();

foreach ($tags as $tag) {
  print $tag->label();
}
```

You can see these helper methods defined in the class hierarchy for the entity type. (The [ContentEntityBase documentation](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21ContentEntityBase.php/class/ContentEntityBase/) is a good place to start.)

### Rendering fields using field formatters

Modules can get the render array representation of a field, formatted using the field formatter, and configuration defined for a specific view mode. This allows the code to take into account any user-defined configuration related to how the field's content should be displayed. When retrieving a field's value with the intent of displaying it as HTML, this is preferred approach.

```
$body_field = $node->get('body');

// Replace with the desired view mode.
$view_mode = 'full';

// Returns a render array representing the field's value.
$build = $body_field->view($view_mode);
```

### Translated fields

The Entity API makes handling translations relatively straightforward, too. The `getTranslation()` method can be used to retrieve a particular translation (if one exists). This simplifies our code when working with entities in multiple languages. For example:

```
$translation = $node->getTranslation('es');

// English title
print $node->title->value;

// Spanish title.
// $translation in this case is an instance of \Drupal\node\Entity\Node. The
// getTranslation() method returns an object of the same type as the one from
// which it's called.
print $translation->title->value;
```

### Update

Just like reading and accessing values from properties and fields, we can update them in a similar fashion.

If we want to change the title of our node, we set it the same way we'd read it, followed by a call to the `save()` method to make sure our change persists.

```
$entity = \Drupal::entityTypeManager()->getStorage('node')->load(22);
$entity->title->value = 'Yes we can!';
// Update the multivalue tags field term id
// Use $entity->field_tags->getValue() to see the field's data structure.
$entity->field_tags[0]->target_id = 3;
$entity->save();
```

### Delete

The only piece of information required to delete an entity is its ID. Once the entity is loaded (using that ID) you can call the `delete()` method.

```
// Delete a single entity.

$entity = \Drupal::entityTypeManager()->getStorage('node')->load(22);
$entity->delete();

// Delete multiple entities at once.
$entity_ids = [22, 42];
$entity_type = 'node';
$storage_handler = \Drupal::entityTypeManager()->getStorage($entity_type));
$entities = $storage_handler->loadMultiple($entity_ids);
$storage_handler->delete($entities);
```

## Recap

In this tutorial we looked at the `EntityTypeManager` and how it can be used to load any type of entity (provided we have the ID). Then we learned how we can read and access the properties and values of our entity as well as methods for updating and deleting. You may find yourself wondering how we find the IDs needed by the `EntityTypeManager`. If so, continue on to [our tutorial on Using Entity queries](https://drupalize.me/tutorial/find-data-entityquery).

## Further your understanding

- What other entity related services are provided by Drupal core?
- Try to update the title of a block displaying on your site using only PHP and `drush eval`.
- What helper method could you use to see what languages a node has been translated into? (Hint: look for helper methods in `ContentEntityBase`)

## Additional resources

- [Working with the Entity API](https://www.drupal.org/docs/drupal-apis/entity-api/working-with-the-entity-api) (Drupal.org)
- [Entity API cheatsheet](https://www.metaltoad.com/blog/drupal-8-entity-api-cheat-sheet) (metaltoad.com)

Was this helpful?

Yes

No

Any additional feedback?

Clear History

Ask Drupalize.Me AI

close