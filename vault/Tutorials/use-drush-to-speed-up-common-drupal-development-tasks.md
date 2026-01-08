---
title: "Use Drush to Speed up Common Drupal Development Tasks"
url: "https://drupalize.me/tutorial/use-drush-speed-common-drupal-development-tasks?p=2593"
guide: "[[command-line-tools-drupal]]"
---

# Use Drush to Speed up Common Drupal Development Tasks

## Content

Back-end developers, and Drupal site builders, often find themselves having to perform the same UI steps over and over again, like exporting configuration, importing configuration changes, running cron, processing a large queue of jobs, indexing items for Search API, and more. Performing these tasks with Drush saves time and reduces the number of clicks required.

Drush core contains commands to execute all the most common tasks. Many contributed modules provide their own Drush commands to make interaction with the module's features, easier, faster, and scriptable.

In this tutorial we'll:

- Learn about the Drush core commands for common tasks like interacting with queues, performing database backups, and importing/exporting configuration
- Demonstrate how to find the Drush commands provided by contributed modules in your project

By the end of this tutorial you'll learn some popular commands for common tasks that'll speed up your daily work.

## Goal

Introduce some of our favorite Drush commands and teach you how to discover more while providing examples of the ways Drush can assist backend developers and site builders with their most common tasks.

## Prerequisites

- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)
- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)

## Quick reference

Throughout this tutorial we'll look at the following Drush commands and examples of what they're used for. This is a subset of the complete list of Drush commands and is intended to illustrate what's possible. We encourage you to explore the available commands on your own and familiarize yourself with what Drush can do. Even if you're not using it today, you might find yourself in the future saying, "Hey, I think I can do this faster with Drush!"

- `queue:list` - List of all the queues on the site
- `queue:run [queue_name]` - Run a specific queue
- `queue:delete [queue_name]` - Delete all items in the queue
- `search-api:status` - Get the status of all Search API indexes on the site
- `search-api:index [index_id]` - Tell Search API to index all un-indexed items
- `search-api:reindex [index_id]` - Mark items for reindexing without deleting data
- `search-api:clear [index_id]` - Clear all index data and mark items for reindexing
- `views:list` - Get a list of all the Views on the site
- `views:execute [views_name] [views_display]` - Execute a specific View
- `config:status` - Get the current status of configuration items
- `config:import` - Import configuration into the site
- `config:export` - Export configuration from the site
- `sql:dump --result-file=[my_file]` - Dump the database into a file
- `sql:drop`- Drop the current database
- `sql:cli < [my_file]` - Import a database from a file

At any time you can run the `drush` command with no arguments to get a list of all the commands available for a specific site. Then use `drush help {command}` for more information and examples.

## Drush commands for queue management

The Drupal Queue operations API allows to modules to queue *work* for later processing. Queues are most often used for batches (like sending an email to everyone with an account), migrations, and any other tasks that might normally cause the PHP web server to timeout. Some contributed modules also use queues as part of their processing mechanisms. For example, indexing content for searching.

The most efficient way to interact with queues is through Drush commands. To see the list of all registered queues on your website run `drush queue:list`. This command -- similar to other Drush *list* commands -- takes options for `--format`, `--field`, and `--filter`. This command is often used to debug the queue and figure out what queues are present.

Example:

```
drush queue:list
```

Output:

```
------------------------ ------- --------------------------------- 
Queue                    Items   Class
------------------------ ------- --------------------------------- 
media_entity_thumbnail   0       Drupal\Core\Queue\DatabaseQueue
------------------------ ------- ---------------------------------
```

To see the list of all available options, refer to the [official Drush documentation for this command](https://www.drush.org/latest/commands/queue_list/).

To run a specific queue, use the `drush queue:run` command. It takes the name of the queue as an argument.

Example:

```
drush queue:run media_entity_thumbnail
```

This command, when used for debugging, is the most efficient with its options:

- `--time-limit` - allows you to specify the maximum processing time (in seconds) for the queue. For instance, if your queue is timing out, you can specify a shorter processing period, so you don't have to wait for the server timeout which, depending on your settings, can be quite long.
- `--items-limit` option allows you to specify the maximum amount of items that can be processed during this queue run. Also, very useful for debugging, if, for example, you get errors during the process function; and for limiting the load on the server especially if the queue is being executed during the heavy cron job.
- `--lease-time` option (in seconds) specifies the maximum time for processing any single queue item. After the time has elapsed, the queue item will be released.

The last command in the `queue` group is `drush queue:delete`. It takes an argument of the queue name and deletes all items in the given queue.

Example:

```
drush queue:delete media_entity_queue
```

## Drush commands for Views

The Views module, part of Drupal's core software, is a query generator and render engine in Drupal core. It's typically used to create and output collections of items such as Drupal content entities. Drush comes with a `views` specific group of commands.

To get a report of all Views built on the site, run `drush views:list`. It returns the machine name of the view, its name and description, and status: enabled or disabled.

Example:

```
drush views:list
+-------------------+--------------------+-----------------------------------------------------------------------------------------------+----------+
| Machine name      | Name               | Description                                                                                   | Status   |
+-------------------+--------------------+-----------------------------------------------------------------------------------------------+----------+
| comment           | Comments           | Find and manage comments.                                                                     | Enabled  |
| comments_recent   | Recent comments    | Recent comments.                                                                              | Enabled  |
... <snip> ...
+-------------------+--------------------+-----------------------------------------------------------------------------------------------+----------+
```

The other popular `views` Drush command is `drush views:execute`. It takes 3 arguments:

- `view_name`: The machine name of the view
- `display`: An optional machine name of the display. If none is specified, the *default* display is used.
- A comma-delimited array of view arguments corresponding to the contextual filters

By default, the result of the command is a rendered markup for the view output. The command takes the `--count` option in order to display a count of items instead of the markup. For example `drush views:execute watchdog --count` returns an amount of items in the watchdog table.

This command is very useful when debugging views as well as for theming when quick reference for markup is needed. To see the list of all available options refer to the [official Drush documentation for this command](https://www.drush.org/latest/commands/views_execute/).

## Drush commands for configuration management

The Drupal core configuration management system also has its corresponding group of Drush commands. These commands are grouped under the `config` prefix. `drush config:status` allows you to see the differences between staged and current configuration. One of the useful applications of the command is `drush config:status 2>&1 | grep "No differences"`. It allows you to check if there are any differences between database and exported config. This variation is typically used in CI scripts.

Two popular commands for configuration management with Drush are `drush config:import` and `drush config:export` -- for importing and exporting configuration. The commands are so popular that you may also see their aliases `drush cim` and `drush cex` in tutorials and documentation.
These commands optionally take the config directory as an argument. This is useful when multiple config directories are present on the site: `drush cim sync` imports configuration from the *sync* directory into the site.

The import command takes the `--partial` option. It allows for partial configuration import. With this option, only new config will be created. Existing config will be updated but no configuration will be deleted. This option is very useful for local environments that are used for testing configuration from multiple Git branches without the need of obtaining a fresh copy of the database. To see the list of all available options values, refer to the [official Drush documentation for this command](https://www.drush.org/latest/commands/config_import/).

Export command comes with options to speed up your Git workflow. For example, `--add` option runs the `git add -p` command after the export and allows you to choose which config to add to the commit. `--commit` runs `git add -A` and `git commit` after the export, to add all exported files and invoke Git commit operation.

Since this is such a common and important ask we've got a whole series on [Configuration Management](https://drupalize.me/series/configuration-management). See also our Drush-specific tutorials: [Synchronize Configuration with Drush](https://drupalize.me/tutorial/synchronize-configuration-drush) and [Inspect Configuration with Drush](https://drupalize.me/tutorial/inspect-configuration-drush).

## Drush commands for database backups

Database commands in Drush are grouped under the `sql` prefix. We encourage you to explore this group's [official Drush documentation](https://www.drush.org/latest/commands/sql_cli/) to learn more of them.

One of the most popular commands in the group is `drush sql:dump`. This command allows you to export databases from the server. A common use case is with the `--result-file` option that saves the dump into a file. For example, `drush sql:dump --result-file=../my_dump.sql` will save the database in file, *my\_dump.sql*.

Another popular option is `--structure-tables-list`. It can be used to skip things like the `cache_*` tables and the session table. It speeds up imports, and the data those tables contain doesn't need to be backed up.

Example:

```
drush sql:dump --gzip --result-file=../my_dump.sql.gz --structure-tables-list=cache,cache_*
```

One of the challenges the community is facing since the advent of the [GDPR](https://en.wikipedia.org/wiki/General_Data_Protection_Regulation) and [CCPA](https://en.wikipedia.org/wiki/California_Consumer_Privacy_Act) regulations is sanitization of database dumps. Drush comes with the `drush sql:sanitize` command that allows it to sanitize the database by removing or obfuscating user data. However, this command acts on the active database used by the site therefore it is not usable for production servers, since it's altering the active production database.

A couple contrib solutions can be used instead of the Drush core `sql:dump` command. To learn more about this topic explore this [community project](https://github.com/machbarmacher/gdpr-dump).

Drush can also be used to import a database from backup. It takes 2 steps. First, you need to drop the existing database by running `drush sql:drop -y`. Then you need to run an import `drush sql:cli < ~/path/to/my_dump.sql`.

Example:

```
drush sql:drop --yes
drush sql:cli < ~/path/to/my_dump.sql
# Or
gunzip < ~/path/to/my_dump.sql.gz | drush sql:cli
```

## See if a contributed module provides any commands

Contributed modules can provide their own set of commands. To see if a contributed module provides any Drush commands, check if it has a *drush.services.yml* file in the root directory of the module, and the commands service class located in the */src/Commands* folder of the module.

You can also use `grep` like so: `drush | grep watchdog` -- This will return all commands for the Database Log module. Alternatively, you may run `drush list --filter=devel_generate` -- this will return all commands that start with `devel_generate`. In both of these examples you can replace `watchdog` and `devel_generate` with the machine name of contributed modules whose commands you would like to see.

## Drush commands for Search API

As an example, let's explore the Drush commands in the Search API module.

[Search API](https://drupalize.me/series/search-api-and-solr-drupal) is the community's most popular Drupal search system. It provides an API and a foundation for the big ecosystem of modules that includes various search back-ends such as Database, SOLR, and Elastic Search.

The main Search API module comes with its own Drush commands that help users interact with the different parts of search architecture from the command line.

In this tutorial we'll focus on the most popular ones. If you are interested in exploring all commands provided by Search API, we encourage you to explore the module's *SearchApiCommands.php* file.

To see the status of existing Search API indexes, run `drush search-api:status`. It shows the number of items in the index, number of indexed items, and percentage of index items. This command optionally takes the `indexId` argument that allows it to limit status reports to a particular index. If `indexId` isn't specified then statuses of all indexes are returned.

To index any new items, run `drush search-api:index`. This command takes an optional argument `indexId`. If no id is provided, it'll try to index items for all enabled indexes. The command also supports options:

- `--limit`: The max number of items to index; set to 0 to index all items
- `--batch-size`: The max number of items to be processed per batch run; set to 0 to index all items at once

To mark an index for reindexing without deleting existing data, run `drush search-api:reindex`. It also takes an optional `indexId` argument and array of options.

To clear all indexed data and mark it for reindexing, run `drush search-api:clear`. Similarly, it takes the optional `indexId` argument.

These commands are often used as part of a deployment workflow, or scheduled via cron to keep the index up-to-date.

## Recap

In this tutorial we covered some of the Drush commands that help speed up routine tasks for developers and site builders. We gave you some ideas of what's possible and the types of tasks Drush can assist with. We also learned that contributed modules can declare their own Drush commands, and looked at some of the commands provided by the Search API module. This tutorial only covers a small number of common use cases, so we recommend you spend some time going through the official Drush documentation to learn more about all the available Drush commands and their options.

## Further your understanding

- After reviewing the complete list of commands with `drush list` what are some others you think would help solve common problems?
- How do you get additional help for a command?
- Can you use Drush to view watchdog log records?

## Additional resources

- [Drush official documentation](https://www.drush.org) (drush.org)
- [Drush Git repository](https://github.com/drush-ops/drush) (github.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Use Drush for Common Site and Environment Management Tasks](/tutorial/use-drush-common-site-and-environment-management-tasks?p=2593)

Next
[Use Drush to Deploy Drupal Updates](/tutorial/use-drush-deploy-drupal-updates?p=2593)

Clear History

Ask Drupalize.Me AI

close