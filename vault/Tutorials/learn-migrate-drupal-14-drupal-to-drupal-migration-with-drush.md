---
title: "Drupal-to-Drupal Migration with Drush"
url: "https://drupalize.me/tutorial/drupal-drupal-migration-drush?p=3116"
guide: "[[learn-migrate-drupal]]"
order: 14
---

# Drupal-to-Drupal Migration with Drush

## Content

In this tutorial we will run a site migration using Drush, and understand how to deal with any failures that occur.

## Goal

Run a Drupal-to-Drupal migration using Drush commands.

## Prerequisites

- [Prepare for a Drupal-to-Drupal Migration](https://drupalize.me/tutorial/prepare-drupal-drupal-migration)
- [Command Line Usage](https://drupalize.me/series/command-line-basics-series)
- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)
- [Install Drush with Composer](https://drupalize.me/tutorial/install-drush-using-composer)
- Basic bash scripting knowledge can be helpful in order to automate migration steps

## Drupal-to-Drupal migration with Drush

To execute a Drupal-to-Drupal migration using Drush, we will use the `migrate-upgrade` command, provided by the [Migrate Upgrade](https://www.drupal.org/project/migrate_upgrade) contributed module. Drush does not support prepping a migration, so if you want to see available and missing upgrade paths before executing your migration you need to [use the Migrate Drupal UI](https://drupalize.me/tutorial/drupal-drupal-migration-ui).

Before you begin your migration, you should first make a backup of your Drupal destination site.

After installing the latest version of Drupal, head to your Drupal root directory in your terminal.

To run a migration with Drush, you will need to have Drush installed. If you need to install Drush, see [Install Drush with Composer](https://drupalize.me/tutorial/install-drush-using-composer).

## Make a backup of your destination Drupal database

```
drush sql-dump > /path/to/save/migrate-backup.sql
```

You should consider writing a script to drop the database tables in your Drupal destination database, import a clean database backup, and re-enable any modules you may need for your migration.

Here's an example of what that might look like.

Create a file in the root of your destination Drupal site, called *cleanmigrate.sh*.

Add the following:

```
drush sql-drop -y
drush sqlq --file=/path/to/migrate-backup.sql
drush en migrate_drupal migrate_upgrade -y
```

Now make your script executable:

```
chmod +x cleanmigrate.sh
```

You can now import a clean database and enable modules like so:

```
./cleanmigrate.sh
```

## Execute a migration

Sprout Video

To run a migration with Drush, enable the following modules:

- Migrate
- Migrate Drupal
- Migrate Upgrade

```
drush en migrate_drupal migrate_upgrade -y
```

You can execute a migration using the `migrate-upgrade` command:

Type the following into your terminal:

```
drush help migrate-upgrade
```

Which results in the following:

```
Perform one or more upgrade processes.

Examples:
 migrate-upgrade                           Upgrade a Drupal 6 database to
 --legacy-db-url='mysql://root:[email protected]  latest Drupal version
 .0.1/d6'

Options:
 --legacy-db-prefix                        Prefix of the legacy Drupal
                                           installation.
 --legacy-db-url                           A Drupal 6 style database URL.
                                           Required.
 --legacy-root                             Site address or root of the legacy
                                           Drupal installation
```

To start a full migration, you can type the following:

```
drush migrate-upgrade --legacy-db-url='mysql://user:pass@host/dbname'
```

If you have **files** you want to migrate, pass the `--legacy-root` flag with the path to your site's files. For example:

```
drush migrate-upgrade --legacy-db-url='mysql://user:pass@host/dbname' --legacy-root=/var/www/drupal7
```

Drush will display status updates and any errors while running the migration, and notify you when complete.

Once the command completes, go and check out your migrated site and see how it looks. Chances are the first few times you'll need to do a bit of further configuration, and test again. But eventually you should be able to run your migration with no unexpected errors.

## The debug flag

You can pass `--debug` or `-d` with your Drush migrate command to get debug output from Drush. This will give you the most information possible about what is happening during a migration.

## Logging your debug output

You can pipe your Drush output to standard out (stdout) and log to file, using something like the following:

```
drush migrate-upgrade --debug 2>&1 | tee -a migration.log
```

This will write your migration output to `migration.log` in the current directory, as well as display it in your terminal.

The `tee` command allows us to write to stdout, and a logfile. The `-a` flag we pass with `tee` will append to the file. This can be useful if you need to run your migration multiple times, and wish to log everything in one place.

You can read about the `tee` command [here](https://en.wikipedia.org/wiki/Tee_(command)).

## Reruns

When running a migration, you may exhaust your system resources, and your migration may stop. Thanks to [highwater marks](https://drupalize.me/tutorial/migrate-system-terms-and-concepts), you can run the migration again and it should pick up where it left off.

## Find help with failures

Migrations are complex, and when running a migration, it is very likely you will run into failures of some kind.

Given the experimental nature of the modules in Drupal Core, it is also possible you will run into bugs.

There are a number of ways to report failures and get help with problems with your migrations:

- [Drupal Upgrade Issue Queue](https://www.drupal.org/project/issues/migrate_upgrade)
- Drupal Core Migration System Issues for reporting issues with core modules
- Module issue queue if you find a bug or exception with a contributed module
- The [#drupal-migrate](https://webchat.freenode.net/?channels=#drupal-migrate) IRC channel on Freenode
- The [#migration](https://drupal.slack.com/archives/C226VLXBP) channel on [Drupal Slack](https://www.drupal.org/slack)
- Hire a consultant

## Roll back a migration

Didn't go as planned? You can rollback the migration and try again in one of two ways:

- Revert to the database backup which you should have made prior to attempting an upgrade. This is generally more reliable.
- Use the `drush migrate-upgrade-rollback` command. This might be quicker, but in some use-cases can be error prone.

## Recap

In this tutorial we learned how to use Drush and the Migrate Upgrade module to execute a Drupal-to-Drupal migration from the command line. We said that, when possible, using Drush is the preferred method because it's more reliable and it's faster than the UI. We also covered a couple of tricks for debugging migrations when running them via Drush.

## Further your understanding

- Create a bash script to import a backup of your destination Drupal site and enable the Migrate modules.

## Additional resources

- [Learn more about the `tee` command](https://en.wikipedia.org/wiki/Tee) (wikipedia.org)
- [Drupal Upgrade Issue Queue](https://www.drupal.org/project/issues/migrate_upgrade) (Drupal.org)
- The [#drupal-migrate](https://webchat.freenode.net/?channels=#drupal-migrate) IRC channel on Freenode (freenode.net)
- The [#migration](https://drupal.slack.com/archives/C226VLXBP) channel on [Drupal Slack](https://www.drupal.org/slack) (drupal.slack.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Drupal-to-Drupal Migration with the UI](/tutorial/drupal-drupal-migration-ui?p=3116)

Next
[Custom Drupal-to-Drupal Migrations](/tutorial/custom-drupal-drupal-migrations?p=3116)

Clear History

Ask Drupalize.Me AI

close