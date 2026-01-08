---
title: "Create Migrations from Core Templates"
url: "https://drupalize.me/tutorial/create-migrations-core-templates?p=3116"
guide: "[[learn-migrate-drupal]]"
---

# Create Migrations from Core Templates

## Content

One method of [creating a custom Drupal-to-Drupal migration](https://drupalize.me/tutorial/custom-drupal-drupal-migrations) involves using the Migrate Upgrade module to generate a set of migration configuration entities that you can use as a starting point. Even if you're not going to use the generated output in the end, this is still an informative exercise as it allows you to see examples of various migration paths.

In this tutorial we'll:

- Use the Migrate Upgrade module's Drush commands to import Drupal core's migration templates
- Examine the generated configuration entities
- Use the Migrate Tools module's Drush commands to view a list of the individual migrations that make up our Drupal-to-Drupal migration

By the end of this tutorial, you should be able to use the Migrate Upgrade module to generate the migrations that Drupal core would use to migrate content, list those migrations, and inspect them individually.

## Goal

Use Migrate Upgrade to create migration configuration entities for a Drupal-to-Drupal migration path.

## Prerequisites

- [Prepare for a Drupal-to-Drupal Migration](https://drupalize.me/tutorial/prepare-drupal-drupal-migration)
- [Custom Drupal-to-Drupal Migrations](https://drupalize.me/tutorial/custom-drupal-drupal-migrations)
- [Migration-Related Contributed Modules](https://drupalize.me/tutorial/migration-related-contributed-modules)
- [Drush](https://drupalize.me/topic/drush)

## Generate migration configuration entities

Instead of starting our [custom Drupal-to-Drupal migration](https://drupalize.me/tutorial/custom-drupal-drupal-migrations) from scratch, we're going to use the [Migrate Upgrade module](https://www.drupal.org/project/migrate_upgrade) to copy all of the migrations for handling Drupal-to-Drupal migrations provided by Drupal core and use those as a starting point.

For more on the distinction between migration plugins and migration configuration entities, check out our [Write a Custom Migration](https://drupalize.me/tutorial/write-custom-migration) tutorial.

Normally when you run the `migrate-upgrade` Drush command provided by the Migrate Upgrade module it loads all the migration plugins provided by Drupal core, inspects your source site in order to determine which migrations to use, and then starts executing them. However, if you pass the `--configure-only` option to the command instead of executing the migrations it loads them into the active configuration store as Migrate Plus style migration configuration entities. Let's do that now.

Sprout Video

Note about this video: Some Drush commands have changed in Drush 9. See [Inspect Configuration with Drush](https://drupalize.me/tutorial/inspect-configuration-drush) for more information.

### Run drush migrate-upgrade --configure-only

```
drush migrate-upgrade --configure-only --legacy-db-key=migrate --legacy-root=/path/to/sites/default/files
```

`--configure-only`: Tells the command to create the migration configuration entities from the core migration templates, but skip executing them.

`--legacy-db-prefix`: Tells the command which `$databases` configuration in settings.php it should use to connect to the source site. In this example we added the 'migrate' configuration in an earlier step.

`--legacy-root`: Full path to directory that contains all user generated files from the old Drupal site, usually *\*/sites/default/files*.

Here's the code that does this, just to help further illustrate what is going on when you run this command.

```
// From the provided source information, instantiate the appropriate migrations
// in the active configuration in memory.
$runner->configure();
if (drush_get_option('configure-only')) {
  // If the --configure-only flag was passed export the migrations as
  // configuration entities. Essentially, save them from memory into the
  // configuration storage.
  $runner->export();
}
else {
  // Execute the migrations that are stored in memory.
  $runner->import();
  \Drupal::state()->set('migrate_drupal_ui.performed', REQUEST_TIME);
}
```

When this command runs, the migrate system performs an evaluation of your source Drupal site and determines which migration plugins are going to be necessary. For example, my source site has a content type named "blog\_post" with a handful of custom fields. The system determines that I need the d7\_node\_type, d7\_node, and d7\_field\_\* migrate templates amongst others to perform a migration. Only the migration templates that are needed for your specific source site will be imported as configuration entities.

### Inspect the configuration entities

Once the import has been completed you can take a look at the results in a few different ways. Exploring the generated configuration entities is a great way to learn more about how the migrations work.

Use Drush (`drush config:status`) to list all known configuration items, and look for any with the prefix *migrate\_plus.migration.\*.* Then inspect the individual entries. (See also [Inspect Configuration with Drush](https://drupalize.me/tutorial/inspect-configuration-drush).)

Example:

```
drush cget migrate_plus.migration.upgrade_d7_node_blog_post
```

(Note: `drush cget` is shorthand alias for both the Drush 8 command `drush config-get` and the Drush 9 command `drush config:get`.)

This represents the migration that will be used to import *blog\_post* content from our source Drupal 7 site into our destination Drupal site.

Here's an example of what you'll see, with some additional comments added:

```
# Every configuration entity has UUID associated with it.
uuid: **********************************
langcode: en
status: true
dependencies: {  }
# The ID, or name, of this specific migration, this is also part of the name
# of the configuration entity. Migration configuration entity names follow the
# pattern `migrate_plus.migration.{ID}`.
id: upgrade_d7_node_blog_post
migration_tags:
  - Drupal 7
  - Configuration
# The migration group was automatically created and bundles together all of the
# migrations that were created by running drush migrate-upgrade --configure-only
migration_group: migrate_drupal_7
label: 'Nodes (Blog post)'
# Source plugin configuration. Using \Drupal\node\Plugin\migrate\source\d7\Node
source:
  plugin: d7_node
  node_type: blog_post
# The process section maps fields/properties in Drupal 7 to fields in 
# the latest Drupal version.
# Fields, and their configuration, will also be migrated from Drupal 7 to 
# the latest Drupal version.
# Essentially mirroring the content type. This is done by the d7_node_type
# migration. The automatically generated migration here also includes the custom
# field definitions from the Drupal 7 site. 
process:
  nid: nid
  vid: vid
  langcode:
    plugin: default_value
    source: language
    default_value: und
  title: title
  uid: node_uid
  status: status
  created: created
  changed: changed
  promote: promote
  sticky: sticky
  revision_uid: revision_uid
  revision_log: log
  revision_timestamp: timestamp
  body: body
  # The blog_post content type in our Drupal 7 site has some custom fields added
  # which are automatically included in the migration configuration.
  field_blog_post_files:
    plugin: iterator
    source: field_blog_post_files
    process:
      target_id: fid
      display: display
      description: description
  field_blog_post_images:
    plugin: iterator
    source: field_blog_post_images
    process:
      target_id: fid
      alt: alt
      title: title
      width: width
      height: height
  field_blog_post_promote: field_blog_post_promote
  field_planet: field_planet
  taxonomy_blog_tags:
    plugin: iterator
    source: taxonomy_blog_tags
    process:
      target_id: tid
# Imported records will be saved as nodes, using the entity:node destination
# plugin.
destination:
  plugin: 'entity:node'
  default_bundle: blog_post
# List of other migrations that are required in order for this migration to be
# successful. For example, we need to migrate the blog_post content type itself
# before we can migrate the content of blog_post nodes.
migration_dependencies:
  required:
    - upgrade_d7_user
    - upgrade_d7_node_type
  optional:
    - upgrade_d7_field_instance
```

These configuration entities follow the same format as a custom migration. Learn more about how all of this works in our [Write a Custom Migration tutorial](https://drupalize.me/tutorial/write-custom-migration).

Note that contributed modules that provide migrations should categorize all migrations to either `Content` or `Configuration` using `migrate_tags`. The `Configuration` migrate tag has been added to the above example. See the change record for Drupal 8.6: [Core migrations are now categorized to Configuration or Content](https://www.drupal.org/node/2944527).

### List the migrations

Use Migrate Tools either via Drush, or the UI, to list the available custom migrations.

Before you do this though, you might need to make some changes to your settings. When the configuration entities were created via `drush migrate-upgrade` they where all exported as part of a migration group -- in my case, "migrate\_drupal\_7". Its configuration is stored in the configuration entity named *migrate\_plus.migration\_group.migrate\_drupal\_7*, and looks like this:

```
drush cget migrate_plus.migration_group.migrate_drupal_7
```

(Note: `drush cget` is shorthand alias for both the Drush 8 command `drush config-get` and the Drush 9 command `drush config:get`.)

```
uuid: 0f7def86-105b-4971-a448-202796146abd
langcode: en
status: true
dependencies: {  }
id: migrate_drupal_7
label: 'Import from Drupal 7'
description: 'Migrations originally generated from drush migrate-upgrade --configure-only'
source_type: 'Drupal 7'
module: null
shared_configuration:
  source:
    key: drupal_7
```

Note the `shared_configuration:source:key: drupal_7` value. This tells all of the migrations in this group to add the `key: drupal_7` value to their source plugin configuration. That indicates that anytime the migration needs to access the source database it should look for the database connections array in your *settings.php* file with the key `$databases['drupal_7']['default']`. If this doesn't exist, and you point at your source Drupal 7 site's database, you're likely to see some errors. You can either define `$databases['drupal_7']['default']` in your *settings.php*, or edit the configuration entity and change the `key` value to match what's already defined in your *settings.php*.

You can view a list of the migrations that were created by:

- Using the `drush migrate-status` command. This will list all migration configuration entities the system can locate. See our tutorial [Run Custom Migrations](https://drupalize.me/tutorial/run-custom-migrations) to learn more about the Migrate Tools Drush commands
- Navigate to *Structure* > *Migrate* (*admin/structure/migrate*) in the Manage menu, and choose the option to "List migrations" for your migration group

Both methods will display the current status of each migration, information about how many records exist to migrate, how many have already been migrated, and more.

Example:

```
drush migrate-status
 Group: Import from Drupal 7 (migrate_drupal_7)  Status  Total  Imported  Unprocessed  Last imported
 upgrade_block_content_type                      Idle    1      0         1
 upgrade_d7_dblog_settings                       Idle    1      0         1
 upgrade_d7_image_settings                       Idle    0      0         0
 upgrade_d7_image_styles                         Idle    0      0         0
 upgrade_d7_node_settings                        Idle    1      0         1
 upgrade_d7_search_settings                      Idle    1      0         1
 upgrade_d7_taxonomy_vocabulary                  Idle    5      0         5
 upgrade_d7_url_alias                            Idle    27954  0         27954
 upgrade_d7_user_flood                           Idle    0      0         0
 ...
```

If you're following along with the process of [creating a custom Drupal-to-Drupal migration](https://drupalize.me/tutorial/custom-drupal-drupal-migrations), the next step is to [create a module to house your migration code](https://drupalize.me/tutorial/export-migration-configuration-entities-module).

## Recap

In this tutorial, we used the Migrate Upgrade module's `drush migrate-upgrade --configure-only` command to run a Drupal-to-Drupal migration in configuration-only mode. This has the effect of preparing all the necessary migrations by inspecting both the Drupal 7 source and Drupal destination sites and then instead of running them right away, importing them into the Drupal destination site as configuration. After which we can view a list of the generated migrations and inspect individual migrations.

## Further your understanding

- Learn how to [execute individual migrations](https://drupalize.me/tutorial/run-custom-migrations). (Drupalize.Me)
- Use Drush to explore the configuration entities that make up your migration.

## Additional resources

- [Learn more about Configuration Management](https://drupalize.me/series/configuration-management) (Drupalize.Me)
- [See the 8.6 change record: Core migrations are now categorized to Configuration or Content](https://www.drupal.org/node/2944527) (Drupal.org)
- [Inspect Configuration with Drush](https://drupalize.me/tutorial/inspect-configuration-drush) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Why Use Migrate Upgrade and Migrate Plus?](/tutorial/why-use-migrate-upgrade-and-migrate-plus?p=3116)

Next
[Export Migration Configuration Entities into a Module](/tutorial/export-migration-configuration-entities-module?p=3116)

Clear History

Ask Drupalize.Me AI

close