---
title: "Find Data with EntityQuery"
url: "https://drupalize.me/tutorial/find-data-entityquery?p=2607"
guide: "[[work-data-modules]]"
order: 7
---

# Find Data with EntityQuery

## Content

Often when building a site in Drupal you'll find yourself wanting to display a list of nodes, or find entities created by a particular author, or locate some content based on a particular set of criteria. Rather than querying the database directly, Drupal provides a helper class, `EntityQuery`, to make things a bit easier. The `EntityQuery` class will probably look very familiar to you if you're familiar with the Database API, or the `EntityFieldQuery` class in Drupal 7.

In this tutorial we'll:

- Go through several examples of using `EntityQuery` to find subsets of content.
- Demonstrate how to iterate over the results of an `EntityQuery` query.

By the end of this tutorial, you should understand how to use entity queries to create custom sets of data from entities.

## Goal

Use the `EntityQuery` service to obtain a subset of entities of a specific type.

## Prerequisites

- [Entity API Overview](https://drupalize.me/tutorial/entity-api-overview)

## Find entity IDs then load entity objects

There are two parts to finding and using entities:

1. Use the `EntityQuery` service to construct and execute a query. This will return an array of entity IDs that match the conditions of the query.
2. Load the corresponding entity objects that match the IDs returned from the query

## The `EntityQuery` service

The `EntityQuery` service should be obtained via the `getQuery()` method of the entity storage handler for the given entity type. This can be done via the `Drupal` global object. Or you can load it from the service container.

## For OOP code

Inject the `entity_type.manager` service.

**Tip:** This is a commonly used service, and most base classes already include it.

Example:

```
use Drupal\Component\DependencyInjection\ContainerInterface;
use Drupal\Core\DependencyInjection\ContainerInjectionInterface;
use Drupal\Core\Entity\EntityTypeManagerInterface;

class ExampleController implements ContainerInjectionInterface {

  /**
   * The entity type manager.
   *
   * @var \Drupal\Core\Entity\EntityTypeManagerInterface
   */
  protected $entityTypeManager;

  /**
   * Constructor.
   *
   * @param \Drupal\Core\Entity\EntityTypeManagerInterface $entity_type_manager
   *   Entity type manager.
   */
  public function __construct(EntityTypeManagerInterface $entity_type_manager) {
    $this->entityTypeManager = $entity_type_manager;
  }

  /**
   * {@inheritDoc}
   */
  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('entity_type.manager'),
    );
  }

  public function myMethod() {
    $entity_type = 'node';
    $query = $this->entityTypeManager->getStorage($entity_type)->getQuery();
  }

}
```

### For non-OOP code use the Drupal global

The `EntityQuery` class can be loaded via `\Drupal::entityQuery()`.

Example:

```
$entity_type = 'node';
$query = \Drupal::entityQuery($entity_type);

// The above is shorthand for the following.
$entity_type = 'node';
$conjunction = 'AND';
$query = \Drupal::entityTypeManager()->getStorage($entity_type)->getQuery($conjunction);
```

## Access control

As of Drupal 10, `EntityQuery` [requires that access checking is explicitly defined](https://www.drupal.org/node/3201242). Prior to Drupal 10, you could leave this off, and it would default to only returning entities that the currently logged-in user has access to.

You should always be explicit about access control. Either:

Only return entities that the current user has access to (default behavior before Drupal 10):

```
$query->accessCheck(TRUE);
```

Or, disable access checking, and return all entities. This has **security implications** in that users may see entities that they are not permitted to access.

```
$query->accessCheck(FALSE);
```

## `EntityQuery` Conditions

The most important method in the `EntityQuery` class is the `condition()` method. Conditions allow us to limit our query in specific ways so that we can get back exactly what we want. Let's walk through a few examples in code to get a sense of how this can work in practice.

```
$query = \Drupal::entityQuery('node');

// Use conditions to get a list of published articles.
$node_ids = $query
    ->accessCheck(TRUE)
    ->condition('type', 'article')
    ->condition('status', 1)
    // Once we have our conditions specified we use the execute() method to run the query
    ->execute();

// Find all users with the Administrator role.
$admin_user_ids = \Drupal::entityQuery('user')
  ->accessCheck(TRUE)
  ->condition('roles', 'Administrator', 'CONTAINS')
  ->execute();
```

The condition method takes up to four arguments: field, value, operator, and language code. The field should be the field name (and optional column) of the field being queried. Column names can be useful when dealing with reference fields, since additional field names can then be chained together. An example of this chaining would be if you want to query for articles created by a particular user name (rather than by ID) you could use:

```
$query = \Drupal::entityQuery('node');

$articles_by_name = $query
  ->accessCheck(TRUE)
  ->condition('type', 'article')
  ->condition('uid.entity.name', 'admin')
  ->execute();
```

Traversing references like this will work for any entity reference field. The references can be chained together. Assuming you have a content type named *course* with an entity reference field to another content type named *tutorial* with an entity reference field for user entities, and you wanted to find all *course* nodes that reference a *tutorial* node that was authored by the *user* with name "amber", you could use the following condition:

```
$query = \Drupal::entityQuery('node');
$courses_with_tutorials_by_amber = $query
  ->accessCheck(TRUE)
  ->condition('type', 'course')
  ->condition('field_tutorials.entity:node.field_tutorial_author.entity:user.name', 'amber')
  ->execute();
```

Once you have the field name and the desired value identified, the next parameter passed to the condition method is the operator. The operator can take one of several options: `=`, `<>`, `>`, `>=`, `<`, `<=`, `STARTS_WITH`, `CONTAINS`, `ENDS_WITH`, `IN`, `NOT IN`, or `BETWEEN`. For most operators, the value and the type of the column need to be the same literal. For example, it makes little sense to use the `BETWEEN` operator on an integer field, or the `<>` operator on a string. The `IN` and `NOT IN` operators expect array values. The final parameter is language code and allows you to limit the results of a query based on the translation status in a particular language.

```
// Find particular nodes published in the last year.
$query = \Drupal::entityQuery('node');

$now = time();
$last_year = $now - 60*60*24*365;

$last_years_articles = $query
    ->accessCheck(TRUE)
    ->condition('type', 'article')
    ->condition('created', $last_year, '>=')
    ->execute();
```

Two other methods that come in handy when building up the conditions of a query, `orConditionGroup()` and `andConditionGroup()`. Either allows you to define a group of conditions which will subsequently be either OR'ed or AND'ed together. By default, conditions are AND'ed together when you chain calls on the query object like `$query->condition()->condition()`.

The following example finds all nodes of the type *article* authored by *user 22* OR *user 14* OR the *user with name "admin"*.

```
$query = \Drupal::entityQuery('node');

$group = $query->orConditionGroup()
  ->condition('uid', 22)
  ->condition('uid', 14)
  ->condition('uid.entity.name', 'admin')

$entity_ids = $query
  ->accessCheck(TRUE)
  ->condition('type', 'article')
  ->condition($group)
  ->execute();
```

## Other query helper methods

### exists() or notExists()

If you need a simple check whether or not a particular field exists you can use the `exists()` or `notExists()` methods.

```
$query = \Drupal::entityQuery('node');

$untagged_articles = $query
  ->accessCheck(TRUE)
  ->condition('type', 'article')
  ->notExists('field_tags')
  ->execute();
```

### sort()

The `sort()` method can be useful to order the results returned from `EntityQuery` in a particular way.

```
$query = \Drupal::entityQuery('user');

$time = time();
$yesterday = $time - 60*60*24;

$new_users = $query
  ->accessCheck(TRUE)
  ->condition('created', $yesterday, '>=')
  ->sort('created', 'DESC')
  ->execute();
```

### count()

If you're less interested in the actual entity ids, and more interested in how many entities match a particular query the `count` method returns the number of entities found matching your conditions.

```
$query = \Drupal::entityQuery('user');

$time = time();
$yesterday = $time - 60*60*24;

$new_user_count = $query
  ->accessCheck(TRUE)
  ->condition('created', $yesterday, '>=')
  ->count()
  ->execute();
```

### range() and pager()

When working with a site that has a large amount of content it's important to think about limiting the number of results your query might return. Imagine the amount of memory required to load all of the published issue queue nodes from *drupal.org* with an entity query. That wouldn't be a very smart idea. This is where the `pager()` and `range()` methods come in handy. Pager allows us to specify a particular number of results, while the range method allows us to specify an index (or starting) number and the length (or page size) or results to return. Together these can be used to return a subset of any size from a result set.

```
$query = \Drupal::entityQuery('node');

$newest_articles = $query
  ->accessCheck(TRUE)
  ->condition('type', 'article')
  ->condition('status', 1)
  // Only return the newest 10 articles
  ->sort('created', 'DESC')
  ->pager(10)
  ->execute();

$not_quite_as_new_articles = $query
  ->accessCheck(TRUE)
  ->condition('type', 'article')
  ->condition('status', 1)
  // Only return the next newest 10 articles
  ->sort('created', 'DESC')
  ->range(10, 10)
  ->execute();
```

## Debugging queries

Sometimes it can be helpful to see the SQL statement that's being used. `EntityQuery` objects can be converted to their SQL equivalent using the `__toString()` method like so:

```
print $query->__toString();
```

If you use the [Devel module](https://www.drupal.org/project/devel) you can add the `debug` tag to any query and its SQL string will be printed as a message on the page:

```
$query = \Drupal::entityQuery('node');
$nids = $query
  ->condition('type', 'tutorial')
  ->accessCheck(TRUE)
  ->addTag('debug')
  ->execute();
```

## Loading entity objects

Once you're retrieved one or more entity IDs using `EntityQuery` you can load the corresponding entity objects.

### Get the ID of all article nodes

```
$query = \Drupal::entityQuery('node');
$node_ids = $query
    ->accessCheck(TRUE)
    ->condition('type', 'article')
    ->condition('status', 1)
    ->execute();
```

If you know the entity type you can load it using the static `loadMultiple()` method of the entity class:

```
$nodes = \Drupal\node\Entity\Node::loadMultiple($node_ids);
```

### The `EntityTypeManager` service

If you don't know the entity type, use `EntityTypeManager` service manually:

```
$nodes = \Drupal::entityTypeManager()->getStorage('node')->loadMultiple($node_ids);
```

Or, via the service container:

```
$entityTypeManager = \Drupal::service('entity_type.manager')->getStorage('node');
$nodes = $entityTypeManager->loadMultiple($node_ids);
```

### Iterate through results

All of the above methods return an array of entity objects, which you can loop through:

```
foreach ($nodes as $article) {
  print $article->label();
}
```

### Use `EntityStorageInterface::loadByProperties()` method

If you don't need complex conditions, another option is to use the [`EntityStorageInterface::loadByProperties()` method](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21EntityStorageInterface.php/function/EntityStorageInterface%3A%3AloadByProperties) which will return fully loaded entity objects.

```
$node_storage = \Drupal::service('entity_type.manager')->getStorage('node');
$nodes = $node_storage->loadByProperties([
  'type' =>'recipe',
  // Works with regular fields.
  'field_example_int' => 14,
  // Or with reference fields.
  'field_tags.entity:taxonomy_term.name' => 'carrots',
]);
```

The `loadByProperties()` method takes a single argument, an associative array where the keys are the property names and the values are the values those properties must have. If a property takes multiple values, passing an array of values will produce an `IN` condition.

## Recap

In this tutorial we took a look at the `EntityQuery` class. We learned how to use the `conditions` method to construct queries to identify particular sets of entity IDs matching our conditions. We also saw some of the other helper methods provided by `EntityQuery`. You can find additional documentation for these methods, along with several others in the [`QueryInterface` class](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21Query%21QueryInterface.php/interface/QueryInterface/).

## Further your understanding

- Construct an entity query to find a list of all users in a particular role that have not published content.
- See if you can identify and use a helper method from the `QueryInterface` class to search across all node revisions.

## Additional resources

- [`QueryInterface` documentation](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21Query%21QueryInterface.php/interface/QueryInterface/) (api.drupal.org)
- [entityQuery examples for everybody](https://www.drupaleasy.com/blogs/ultimike/2020/07/entityquery-examples-everybody) (drupaleasy.com)
- [Entity Storage, the Drupal 8 Way](http://www.drupalwatchdog.net/blog/2015/3/entity-storage-drupal-8-way) (drupalwatchdog.net)
- [Get a Service from the Container](https://drupalize.me/videos/get-service-container) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Working with Entity CRUD](/tutorial/working-entity-crud?p=2607)

Next
[Entity API Hooks](/tutorial/entity-api-hooks?p=2607)

Clear History

Ask Drupalize.Me AI

close