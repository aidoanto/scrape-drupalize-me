---
title: "Run Custom Migrations"
url: "https://drupalize.me/tutorial/run-custom-migrations?p=3115"
guide: "[[learn-migrate-drupal]]"
order: 28
---

# Run Custom Migrations

## Content

As of right now, the most reliable way to run custom migrations is using Drush. Depending on the version of Drush you're using you may also need the [Migrate Tools module](https://www.drupal.org/project/migrate_tools). In this tutorial we'll walk through using Drush to run a custom migration, as well as the other commands that can be used to manage the execution of migrations.

By the end of this tutorial you should know how to run your custom migrations.

## Goal

Use Drush commands to import a list of baseball players using a custom migration.

## Prerequisites

- [Write a Custom Migration](https://drupalize.me/tutorial/write-custom-migration)
- [Migration-Related Contributed Modules](https://drupalize.me/tutorial/migration-related-contributed-modules)
- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)
- [Install Drush with Composer](https://drupalize.me/tutorial/install-drush-using-composer)

*Note*: This tutorial is specific to running [custom migrations](https://drupalize.me/tutorial/write-custom-migration). If you're trying to execute a Drupal-to-Drupal migration using Drush see [Drupal-to-Drupal Migration with Drush](https://drupalize.me/tutorial/drupal-drupal-migration-drush).

Sprout Video

## The quick version

With Drush >= 10.4.x installed you can do the following.

Run an individual custom migration:

```
drush migrate:import {MIGRATION_ID}
```

Or run all custom migrations:

```
drush migrate:import --all
```

## Optionally install Migrate Tools

If you're using Drush version 10.4+ the commands from the [Migrate Tools module](https://www.drupal.org/project/migrate_tools) module are built into Drush core, and you likely do not need to install the Migrate Tools module unless something else depends on it. Prior to Drush 10.4+ the commands for interacting with migrations via Drush live in the Migrate Tools module.

There are a couple of minor differences between the commands in Drush core, and those in Migrate Tools. The most notable is that the `drush migrate:import` command in Migrate Tools currently supports a `--group` option and Drush core does not. More on this below.

Install Migrate Tools:

```
composer install drush/migrate_tools
```

If you're upgrading from an older version of Drush + Migrate Tools to Drush 10.4+ you should be able to disable and remove the Migrate Tools module, and then upgrade Drush, and have things continue to work. And note that if you are using Migrate Tools 5.x it will prevent you from upgrading to Drush 10.4+ because of conflicts. You can, and in most cases should, remove Migrate Tools and upgrade Drush.

```
drush pm:uninstall migrate_tools
composer remove drupal/migrate_tools
composer update drush/drush --with-dependencies
```

We expect that in the future there will be a 6.x release of the Migrate Tools module that is compatible with Drush 10.4+ and adds additional features (like `--group`) to the Drush core migrate commands. Keep on eye on development in these two issues:

- <https://gitlab.com/drupalspoons/migrate_tools/-/issues/118>
- <https://www.drupal.org/project/migrate_tools/issues/3213947>

## List migration-related Drush commands

Run `drush --filter=migrate` to get a list of the migration-related commands:

Example:

```
drush --filter=migrate
Drush Commandline Tool 10.5.0

Run `drush help [command]` to view command-specific help.  Run `drush topic` to read even more documentation.

 Available commands:
 migrate:
   migrate:fields-source (mfs)     List the fields available for mapping in a source.
   migrate:import (mim)            Perform one or more migration processes.
   migrate:messages (mmsg)         View any messages associated with a migration.
   migrate:reset-status (mrs)      Reset an active migration's status to idle.
   migrate:rollback (mr)           Rollback one or more migrations.
   migrate:status (ms)             List all migrations with current status.
   migrate:stop (mst)              Stop an active migration operation.
   migrate:upgrade (mup)           Perform one or more upgrade processes.
   migrate:upgrade-rollback (mupr) Rolls back and removes upgrade migrations.
```

## List migrations and check their status

Custom migrations are defined by modules, a site can have one or more custom migrations defined, each individual migration can be identified by its unique ID.

Use the `drush migrate:status` command to verify that Drupal can see your custom migration(s), and to get additional information about their current state. You should see a list of migrations along with details about whether the migration is currently running, the total number of records the migration deals with, the number of records that have been previously imported, the number remaining to be imported, and a time stamp indicating the last time the migration was run.

Example:

```
drush migrate:status

> Group: dmeblog_migrate     Status  Total  Imported  Unprocessed  Last imported
>  baseball_player            Idle    17725  17725     0            2016-06-01 16:38:51
>  upgrade_d7_user_role       Idle    14     0         14
>  upgrade_d7_user            Idle    15     0         15
>  upgrade_d7_node_type       Idle    7      0         7
>  upgrade_d7_node_blog_post  Idle    540    0         540
```

## Find a migration's ID

Almost all of the `migrate:*` commands can accept a migration ID as an argument. The ID is located in the YAML file that defines the migration.

Example from *modules/custom/baseball\_migration/migrations/baseball\_player.yml*:

```
# The machine name for a migration. Also used by various CLI tools when
# referencing the migration as an argument for a command.
id: baseball_player
```

The ID can also be found in the output from the `migrate:status` command as shown above.

## Run a migration

Run all migrations:

```
drush migrate:import --all
```

Limit a migration to configration only. Imports only migrations with a `migration_tags` value of `Configuration`.

```
drush migrate:import --tag=Configuration
```

Limit a migration to content only. Imports only migrations with a `migrations_tags` value of `Content`.

```
drush migrate:import --tag=Content
```

Run an individual migration by specifying its unique ID. Run multiple by providing a comma separated list of migration IDs

```
drush migrate:import {MIGRATION_ID}
```

Use the migration group name, as defined by the `migration_group` key in your migrations YAML file, to run multiple related migrations at the same time. **Note**: This option is currently only available if you're using the Migrate Tools module. If not, we recommend using `--tag` to group migrations together as needed.

```
drush migrate:import --group=baseball
```

After completing the command will output a status message:

```
drush migrate:import baseball_player
> Processed 1725 items (1725 created, 0 updated, 0 failed, 0 ignored) - done with 'baseball_player'
```

Check for any failed migrations. Additionally the command may have output additional messages during execution if any exceptions were raised.

One of my favorite tricks it to use a combination of the `--limit` and `--idlist` flags to debug migrations. Using `--limit` allows you to limit the number of rows that are imported, which can be really useful when testing your migration code. Often times running a complete migration involves importing hundreds, or even thousands of nodes, and takes a long time. Limit it to a more reasonable number like 25 if you just want to confirm that things are working as expected.

You can use the `--idlist` flag to specify one or more specific records to import. The ID here refers the the unique ID of the source record as defined by the source plugin. If you've got records that are giving you trouble you can use this technique to import just those records, validate the result, revert, update your code, and do it again. Like above, this helps avoid the long wait involved when running a complete migration.

## Stop a running migration

You can stop a running migration using the `migrate-stop` command.

```
drush migrate:stop {MIGRATION_ID}
```

## Migrate messages

When running a migration all messages are logged in addition to being output via the CLI. You can review logged messages for any migration `migrate-messages` command.

```
drush migrate:messages {MIGRATION_ID}
```

## Rolling back a migration

When you run a migration the Migrate API tracks each imported record. During testing, or in the case of a failed migration you may want to reverse the migration and try again. This can be accomplished using the `migrate-rollback` command.

```
drush migrate:rollback {MIGRATION_ID}
```

Like `migrate:import`, `migrate:rollback` can be used to rollback all migrations, all migrations in a group, and migrations by their ID either single or comma separated.

## Recap

In this tutorial, we walked through the process of using Drush. We also looked at the commands provided by the Migrate Tools module to execute, stop, review messages for, and rollback a custom migration.

## Further your understanding

- Use `drush help {COMMAND}` to get more information about the options available for any of the `migrate:*` commands. Example: `drush help migrate:import`

## Additional resources

- [Migrate Tools](https://www.drupal.org/project/migrate_tools) (Drupal.org)
- [Migrate commands are now part of Drush core](https://gitlab.com/drupalspoons/migrate_tools/-/issues/118) (gitlab.com)
- [Change record: Core migrations are now categorized to Configuration or Content](https://www.drupal.org/node/2944527) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Write a Custom Migration](/tutorial/write-custom-migration?p=3115)

Next
[Use Highwater Marks to Limit What Gets Imported](/tutorial/use-highwater-marks-limit-what-gets-imported?p=3115)

Clear History

Ask Drupalize.Me AI

close