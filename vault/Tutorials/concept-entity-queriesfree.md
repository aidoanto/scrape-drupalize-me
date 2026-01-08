---
title: "Concept: Entity Queriesfree"
url: "https://drupalize.me/tutorial/concept-entity-queries?p=3243"
guide: "[[drupal-module-developer-guide]]"
---

# Concept: Entity Queriesfree

## Content

Entity queries are the standard method for retrieving, filtering, and sorting lists of entities programmatically in Drupal. Unlike direct database queries, entity queries work seamlessly with Drupal's entity system, including support for access control and abstraction from storage details.

In this tutorial, we'll:

- Introduce entity queries and their operation within Drupal.
- Explain the advantages of using entity queries over direct database queries.
- Provide examples of entity query usage.

By the end of this tutorial, you'll understand how to efficiently and securely fetch lists of entities using entity queries.

## Goal

Understand how to use entity queries to retrieve lists of entities instead of using direct database queries.

## Prerequisites

- [Concept: Entity API and Data Storage](https://drupalize.me/tutorial/concept-entity-api-and-data-storage)
- [Concept: Dependency Injection](https://drupalize.me/tutorial/concept-dependency-injection)

## What are entity queries?

Entity queries provide a high-level abstraction for querying Drupal entities. They abstract database schema complexities, enforce access control, and offer a unified method for entity access.

Direct SQL queries can be problematic due to Drupal's dynamic database schema and the potential for bypassing access controls. Entity queries avoid these issues, ensuring data security and integrity.

## Entity query basics

Entity queries consist of specifying criteria to filter and sort entities. To create an entity query:

1. Get a query object using `EntityTypeManager` or the Drupal global service.
2. Define criteria using methods like `condition()`, `sort()`, and `range()`.
3. Execute the query to retrieve entity IDs, then load entities as needed.

Entity queries are built with the `QueryInterface`, which offers methods for adding conditions, sorting, and setting limits.

Example of obtaining a query object:

```
// Using EntityTypeManager service with dependency injection.
$query = $this->entityTypeManager->getStorage($entity_type)->getQuery();

// Using the Drupal global service.
$query = \Drupal::entityQuery($entity_type);
```

An example query:

```
$newest_articles = $query
  ->accessCheck(TRUE)
  ->condition('type', 'recipe')
  ->condition('status', 1)
  ->condition('field_drupal_version', '9', '>=')
  ->sort('created', 'DESC')
  ->execute();
```

Queries return an array of entity IDs. Example:

```
$newest_articles = [
  8 => '5',
  9 => '6',
];
```

Load the complete entity objects using the entity type manager service. Example:

```
$nodes = $this->entityTypeManager->getStorage($entity_type)->loadMultiple($newest_articles);

foreach ($nodes as $node) {
  print $node->label();
}
```

## Performance considerations

When using entity queries in Drupal, it's important to consider performance, particularly for large datasets. These queries, while convenient, can add overhead due to the abstraction from direct database interactions.

To optimize performance:

- Use pagination with the `range()` method to limit entities loaded into memory
- Consider loading only necessary fields, if the full entity objects aren't required.
- Cache query results where possible.

## Recap

Entity queries provide a programmatic, secure, and efficient way to query entity data. They allow custom code to remain agnostic about Drupal's underlying data structure. And offer a consistent approach for retrieving any entity data.

## Further your understanding

- How does the automatic application of access control in entity queries affect module development?
- In a scenario requiring a list of entities, what entity query would you use?

## Additional resources

- [Find Data with Entity Queries](https://drupalize.me/tutorial/find-data-entityquery) (Drupalize.Me)
- [`QueryInterface` documentation](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21Query%21QueryInterface.php/interface/QueryInterface/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add Custom Validation to User Entities](/tutorial/add-custom-validation-user-entities?p=3243)

Next
[Reset Vendor Status with Cron](/tutorial/reset-vendor-status-cron?p=3243)

Clear History

Ask Drupalize.Me AI

close