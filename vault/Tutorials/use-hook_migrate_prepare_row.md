---
title: "Use hook_migrate_prepare_row()"
url: "https://drupalize.me/tutorial/use-hookmigratepreparerow?p=3116"
guide: "[[learn-migrate-drupal]]"
---

# Use hook_migrate_prepare_row()

## Content

Every row returned, from every source, during the execution of a migration is passed through [`hook_migrate_prepare_row()`](https://api.drupal.org/api/drupal/core!modules!migrate!migrate.api.php/function/hook_migrate_prepare_row/) and `hook_migrate_MIGRATION_ID_prepare_row()`. Using these two hooks we can augment our migration in a variety of different ways.

In this tutorial we'll:

- Discuss the use case for `hook_migrate_prepare_row()`
- Implement `hook_migrate_prepare_row()` and use it to skip all but a select list of fields during the field migration
- Implement `hook_migrate_MIGRATION_ID_prepare_row()` and use it to skip all but a select list of node types

By the end of this tutorial you should have a better understanding of when `hook_migrate_prepare_row()` might be useful when writing your own migration, as well as how to skip rows in a migration based on conditional logic.

## Goal

Use `hook_migrate_prepare_row()` and `hook_migrate_MIGRATION_ID_prepare_row()` to exclude some node types and fields from being migrated during a custom Drupal-to-Drupal migration.

## Prerequisites

- [Implement Any Hook](https://drupalize.me/tutorial/implement-any-hook)

Some common tasks that you can perform with `hook_migrate_prepare_row()` include:

- Skipping rows based on conditional logic
- Adding new or computed fields to a source row based on custom logic
- Inspecting failed migrations for debugging purposes
- Handle fields from previous Drupal versions that do not have a migration path

## Skipping rows with hook\_migrate\_prepare\_row()

For our example, we're going to implement `hook_migrate_prepare_row()` and use it to skip some records that we don't want to migrate. In our [Custom Drupal-to-Drupal Migration tutorial](https://drupalize.me/tutorial/custom-drupal-drupal-migrations) we're migrating all the blog posts from Drupalize.Me, but not the rest of the content. By default the dmeblog\_d7\_node\_type, and dmeblog\_d7\_field migrations migrate all content types and all field definitions regardless of whether we're also migrating the related content. We can skip the migration of all non blog\_post content types, and any fields that are not associated with the content type since we don't need it on our new site and it would only create a mess that we need to clean up later.

We'll add a couple of hook implementations to the *dmeblog\_migrate.module* file in [the module we created to contain our migration](https://drupalize.me/tutorial/export-migration-configuration-entities-module). If the file doesn't exist you can go ahead and create it.

Here's our implementation of `hook_migrate_prepare_row()`:

```
/**
 * Implements hook_migrate_prepare_row().
 *
 * This function will be called once for every row in every migration. Which
 * makes it quite powerful.
 *
 * It's also important to use some smart logic in this function to ensure you're
 * only performing your extra logic when it's really needed. Not doing so has
 * the potential to really slow things down.
 *
 * We recommend at a minimum always checking the $migration->id() value to see
 * which migration is currently being executed.
 */
function dmeblog_migrate_migrate_prepare_row(Row $row, MigrateSourceInterface $source, MigrationInterface $migration) {
  // This example performs some extra processing when running the
  // upgrade_d7_field migration. In this case we only want to migrate the fields
  // that are used by our Drupal 7 blog_post content type, and not all the
  // fields defined on our Drupal 7 site. So for each row in the Drupal 7 fields
  // list we compare it against a static list and tell the Migrate API to skip
  // any that are not in our list.
  if ($migration->id() == 'dmeblog_d7_field' || $migration->id() == 'dmeblog_d7_field_instance') {
    // Drupal 7 field names for all the fields we know we DO want to migrate.
    $blog_fields = [
      'field_blog_post_images',
      'field_blog_post_files',
      'field_planet',
      'taxonomy_blog_tags',
    ];

    // The `field_name` property here comes from the source plugin which defines
    // the list of source fields.
    // @see \Drupal\field\Plugin\migrate\source\d7\Field::fields()
    if (!in_array($row->getSourceProperty('field_name'), $blog_fields)) {
      // Skip this row by throwing a new MigrateSkipRowException exception.
      // Using FALSE here also instructs the Migrate API to forgo creating an
      // entry in the map table for this particular record instead of marking
      // it as ignored. Either would work in this case, this method works for us
      // since we don't really need to record that it was STATUS_IGNORED for any
      // reason.
      throw new MigrateSkipRowException('', TRUE);
    }
  }
}
```

This hook receives 3 arguments:

- `$row`: Contains the row currently being processed and is an instance of `Drupal\migrate\Row`. Take a look at [the documentation for this class](https://api.drupal.org/api/drupal/core!modules!migrate!src!Row.php/class/Row/) to get an idea of how you can access data contained in the row. The `Row::hasSourceProperty()`, and `Row::getSourceProperty()` methods are frequently useful. Find valid arguments for both by looking at the `fields()` method of the source plugin being used for the row.
- `$source`: The source that is currently being used to retrieve data, and that is responsible for construction of the current row. Useful for determining context in some cases.
- `$migration`: The migration currently being executed. Commonly used for determining context such as the migration's ID (`$migration->id()`). Can also be used to modify the migration process based on conditional logic. For example; adding a process pluging to the processing pipeline at runtime (`$migration->setProcess($process)`).

And here's an example that uses `hook_migrate_MIGRATION_ID_prepare_row()` to limit the fields that are migrated using the same technique.

```
/**
 * Implements hook_migrate_MIGRATION_ID_prepare_row().
 *
 * The migration we're processing in this place is "dmeblog_d7_node_type".
 */
function dmeblog_migrate_migrate_dmeblog_d7_node_type_prepare_row(Row $row, MigrateSourceInterface $source, MigrationInterface $migration) {
  // Skip all node types that are not in our list.
  $node_types = ['blog_post'];
  if (!in_array($row->getSourceProperty('type'), $node_types)) {
    throw new MigrateSkipRowException('', TRUE);
  }
}
```

It's worth noting that rejected rows in `hook_migrate_prepare_row()` are not removed from the total rows reported by `drush migrate-status` or the migrate dashboard. The counts reported there are the total rows available to the source, and rows which will be rejected by `hook_migrate_prepare_row()` on import cannot be predicted.

## Recap

In this tutorial, we implemented `hook_migrate_prepare_row()` and `hook_migrate_MIGRATION_ID_prepare_row()` in a custom module in order to limit the content types, and fields, that are migrated when doing a Drupal-to-Drupal migration. This demonstrates one possible way of customizing a migration. It ensures that only the configuration you're interested in is migrated. This same technique would work just as well for content migrations.

## Further your understanding

- Try changing `throw new MigrateSkipRowException('', FALSE);` to `TRUE` and running your migrations again. What changed?
- [This example module](https://github.com/Lullabot/d8_custom_migration) has some good examples of using `hook_migrate_prepare_row()` to skip rows, create computed fields, and handle missing migration paths for contributed modules

## Additional resources

- [Documentation for `hook_migrate_prepare_row()`](https://api.drupal.org/api/drupal/core!modules!migrate!migrate.api.php/function/hook_migrate_prepare_row/) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Customize an Existing Source Plugin](/tutorial/customize-existing-source-plugin?p=3116)

Clear History

Ask Drupalize.Me AI

close