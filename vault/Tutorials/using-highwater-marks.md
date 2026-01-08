---
title: "using highwater marks"
url: "https://drupalize.me/tutorial/use-highwater-marks-limit-what-gets-imported"
guide: "[[learn-migrate-drupal]]"
---

# using highwater marks

## Content

When running migrations you can use the `highwater_mark` [source plugin](https://drupalize.me/tutorial/source-plugins) configuration option to influence which rows are considered for import on subsequent migration runs. This allows you to do things like only look at new rows added to a large dataset. Or to reimport records that have changed since the last time the migration was run. The term, highwater mark, comes from water line marks found on structures in areas where water level changes are common. In running migrations, you can think of a *highwater mark* as a line that denotes how far the migration has progressed, and saying, "from now one, we only care about data created after this line".

Another common use case for highwater marks is when you're importing a large dataset and the system runs out of resources. Usually this will look like a migration failing because it timed out, or the process ran out of memory. A highwater mark *should* allow you to pickup from where you left off.

In this tutorial we'll:

- Define what a highwater mark is, and how you can use them to limit the rows considered for importing each time a migration is executed.
- Demonstrate how highwater marks can be used to reimport source records that have been modified since the previous time the migration was executed.
- Introduce the `track_changes` option.

By the end of this tutorial you should be able to define what a `highwater_mark` is and how to use them to speed up the import of large datasets or force the migration to reimport records when the source data is changed.

You should also be aware of [the `track_changes` feature](https://drupalize.me/tutorial/track-changes-source-data-during-migration) which is a slower, but more dynamic, method of checking for changes in source data and reimporting records when a change is found.

## Goal

Define what highwater marks are, and how and when to use them in your migrations.

## Prerequisites

- [Write a Custom Migration](https://drupalize.me/tutorial/write-custom-migration)
- The functionality of *highwater marks* and *track changes* is defined by `\Drupal\migrate\Plugin\migrate\source\SourcePluginBase`. It only works if the source plugin you're using extends that class. Most do.
- [Source Plugins](https://drupalize.me/tutorial/source-plugins)

## Use a `highwater_mark`

The Migrate API can use [highwater marks](https://www.drupal.org/docs/drupal-apis/migrate-api/migrate-api-overview#s-highwater-marks) to limit the list of rows to import to only those that are above the mark. Anything below the mark is considered already processed and can be ignored. The 2 most common use cases are:

- Only import records that have been **added** to the source data since the last time the migration ran.
- Only migrate records that have been **updated** since the last time the migration ran.

Consider Drupal 7 nodes as an example. You could use either the `node.nid` field or the `node.changed` field as a highwater mark. Every time the migration is run, it'll keep track of the last `nid` value or the latest `changed` timestamp it sees. The next time the migration runs, it'll filter out rows that are below that value. In the case where you're using a timestamp as the highwater mark, if a record was previously imported but the timestamp changed to something that is now higher than the mark, it'll still be in the list of records to import.

The logic for highwater marks happens in the `\Drupal\migrate\Plugin\migrate\source\SqlBase::initializeIterator` method. Which is responsible for discerning the list of rows that will be considered for migration.

Highwater marks are configured per-migration, in the source plugin configuration of the migration's YAML (*.yml*) file.

Example:

```
source:
  plugin: d7_users
  # This will record the LAST uid it sees as the mark.
  highwater_mark:
    # The value of the name key should be the name of a field in the source
    # data for the migration.
    name: uid
```

Another example using a timestamp field:

```
source:
  plugin: d7_users
  # This will record the LAST timestamp it sees as the mark.
  highwater_mark:
    name: changed
    alias: u
```

The `highwater_mark` property has a `name` key which contains the name of the field in the source data that contains the highwater value, and the optional table `alias`.

It's a good idea to ensure that the source data is sorted by the same field that you're using as the highwater mark. If you don't, it's possible you could end up with rows slipping through the cracks. In the example above that uses the `uid` field if the records were in a random order and `uid=21` came before `uid=2` but the migration failed at `uid=21` then the next time it runs it'll look for anything *higher* than 21 and thus miss `uid=2`.

If you're using something that inherits from `SqlBase` as the source the highwater field is automatically added to the `ORDER BY` clause of the query.

**Note:** If you get errors about an ambiguous field in the `ORDER BY` clause when using an SQL source, this is because you're joining tables, and there is more than one field with the same alias. You'll need to be more specific and use the `{table_alias}.{field_name}` syntax that you would use in SQL query. For example, use `u.changed` instead of just `changed`. Find where the tables are joined in the source plugin to figure out which table alias is being used. Then use that to populate the `alias` option.

## Recap

The `highwater_mark` configuration option for the `source` section of a migration allows you to determine which source records should be considered for (re)import. Highwater marks limit the list of source rows to consider by telling the migration to only look at rows where the highwater field's value is above the previous mark and ignore all other rows. This can be used to limit the migration to only import new records by using something like an auto-incrementing numeric ID field as the highwater mark. Or to import both new and changed records by using a timestamp field.

## Further your understanding

- Read more about how we used highwater marks to speed up a slow migration in [Speed up Your Drupal Migrations with Highwater Marks](https://drupalize.me/blog/speed-your-drupal-migrations-high-water-marks).
- How can using highwater marks speed up the migration of a large dataset?
- Can you give an example of how you could use a highwater mark to import source records that have been modified since the previous run of the same migration?

## Additional resources

- [Track Changes to Source Data During a Migration](https://drupalize.me/tutorial/track-changes-source-data-during-migration) (Drupalize.Me)
- [Speed up Your Drupal Migrations with Highwater Marks](https://drupalize.me/blog/speed-your-drupal-migrations-high-water-marks) (Drupalize.Me)
- [Tracking changes in Migrate with dynamic row hashes](https://mglaman.dev/blog/tracking-changes-migrate-dynamic-row-hashes) (mglaman.dev)

Was this helpful?

Yes

No

Any additional feedback?

Clear History

Ask Drupalize.Me AI

close