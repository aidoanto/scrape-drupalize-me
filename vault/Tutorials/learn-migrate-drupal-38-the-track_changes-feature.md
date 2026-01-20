---
title: "the track_changes feature"
url: "https://drupalize.me/tutorial/track-changes-source-data-during-migration"
guide: "[[learn-migrate-drupal]]"
order: 38
---

# the track_changes feature

## Content

If you need to write a migration that is capable of being executed multiple times and picking up changes to previously imported data, you can use the `track_changes` configuration option of most source plugins. This will tell the migration to keep a hash of each source row, and on subsequent runs of the same migration it will compare the previous hash to the current one. If they don't match this means the source data has changed, and Drupal will reimport that record and update the existing destination record with new data.

Using `track_changes` differs from calling `drush migrate:import --update` in that using `--update` will force every record to be re-imported regardless of whether the source data has changed or not.

In this tutorial we'll:

- Learn how change tracking works to detect changes in your source data
- Use the `track_changes` option in a migration

Note that progress of a migration can also be tracked [using highwater marks](https://drupalize.me/tutorial/use-highwater-marks-limit-what-gets-imported) if the source data has something like a `last_updated` timestamp column. Using highwater marks in this case is likely more efficient than using `track_changes`. It's a good idea to understand how both features work, and then choose the appropriate one for each migration.

## Goal

Explain how the `track_changes` feature works, and how to use it to keep destination records in sync with actively-changing source data.

## Prerequisites

- [Write a Custom Migration](https://drupalize.me/tutorial/write-custom-migration)
- [Use Highwater Marks to Limit What Gets Imported in a Migration](https://drupalize.me/tutorial/use-highwater-marks-limit-what-gets-imported)
- The functionality of both of these features is defined by `\Drupal\migrate\Plugin\migrate\source\SourcePluginBase`. And only works if the source plugin you're using extends that class. Most do.
- [Source Plugins](https://drupalize.me/tutorial/source-plugins)

## Use `track_changes` to import only new or changed records

The Migrate API has a [`track_changes`](https://www.drupal.org/docs/8/api/migrate-api/migrate-source-plugins/overview-of-migrate-source-plugins#s-migrate-api-track-changes-option) option that can be used to limit what is imported during a migration run. Setting the `track_changes` option to `TRUE` in a migration will cause each source row to be hashed and compared to the previous value to determine whether the item should be (re)imported.

Normally, when you run a migration the API keeps track of which source records have already been imported in a mapping table. On subsequent runs, the migration will compare the ID of each source row to what's in the mapping table. If the row has already been imported, it'll just skip it. (Unless you've specified something like the `--update` flag in a Drush migrate command.)

Change tracking is configured per-migration, in the source plugin configuration of the migration's YAML (.yml) file.

Example:

```
source:
  plugin: d7_users
  # Change tracking is a boolean value that defaults to FALSE.
  track_changes: TRUE
```

If you're curious, hashes for the records are kept in the `migrate_map_*` table, in the corresponding row for the migration.

If you want to alter what it means to be *changed* to something other than comparing hashes you can do so by overriding the `\Drupal\migrate\Plugin\migrate\source\SourcePluginBase::rowChanged` method in a [custom source plugin](https://drupalize.me/tutorial/write-custom-source-plugin).

## Should I use `highwater_mark` or `track_changes`?

Both the `highwater_mark` and `track_changes` features are used to accomplish roughly the same thing: limiting the rows that need importing to a subset of the total. Highwater marks are based on a static value like a timestamp, and `track_changes` compares row hashes and is more dynamic.

Note that you can only use one or the other. If you define both `highwater_mark` and `track_changes` the migration will throw an exception. You can see where this is determined in `\Drupal\migrate\Plugin\migrate\source\SourcePluginBase::__construct`.

If you set the `highwater_mark` to something like a timestamp that represents the date that a record was last updated, you can use either method to effectively say, "each time I run the migration only import records that are either new or have changed since the last time I ran the migration". This works assuming that the system where the data is being sourced from updates this timestamp whenever something is edited. For example, how Drupal updates the `changed` date every time a node is edited.

So what's the difference?

A **highwater mark** says: If the row isn't above the previous highwater mark than don't even consider it for (re)importing right now.

While `track_changes` **processes every row of source data**, including calling `prepareRow()` and associated hooks, and then checks to see if anything has changed since the last time it saw this row.

The primary difference is that the `track_changes` method evaluates **every row** whereas the `highwater_mark` method only looks at rows above the previous highwater mark.

The `track_changes` method is useful if the changes to the source data happen in a way that doesn't increment a timestamp or other infinitely-growing number that can be sensibly used as a highwater mark. But using `track_changes` is less efficient because it requires processing every row, every time the migration is run.

If you can reliably determine which records are new or changed via something like a timestamp, highwater marks are going to be more efficient -- and you should use them. If there's not a timestamp field and the only way to know if a record changed is to compare the record's data to the previous time it was migrated, you'll need to use `track_changes`.

## Recap

Using the `track_changes` configuration option in a migration allows you reimport a row when the source data has been modified. This is an effective way to create migrations that can continuously import from a source (opposed to migrations that are intended to be run once as part of a Drupal-to-Drupal upgrade) and keep the destination data in-sync with both changed and new records in the source data. Because it needs to calculate a hash to determine if the row has changed, it's much slower while considerably more dynamic, than using a highwater mark to accomplish the same thing.

## Further your understanding

- This blog post [Tracking changes in Migrate with dynamic row hashes](https://mglaman.dev/blog/tracking-changes-migrate-dynamic-row-hashes) goes into more depth about how track changes works, and potential use cases where highwater marks won't work.
- Can you think of an example of a change in your source data that could not be tracked with a highwater mark and would require using `track_changes` to catch?
- What are the advantages of using a highwater mark over tracking changes?

## Additional resources

- [Use Highwater Marks to Limit What Gets Imported in a Migration](https://drupalize.me/tutorial/use-highwater-marks-limit-what-gets-imported) (Drupalize.Me)
- [Speed up Your Drupal Migrations with Highwater Marks](https://drupalize.me/blog/speed-your-drupal-migrations-high-water-marks) (Drupalize.Me)
- [Tracking changes in Migrate with dynamic row hashes](https://mglaman.dev/blog/tracking-changes-migrate-dynamic-row-hashes) (mglaman.dev)

Was this helpful?

Yes

No

Any additional feedback?

Clear History

Ask Drupalize.Me AI

close