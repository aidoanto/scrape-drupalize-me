---
title: "Custom Drupal-to-Drupal Migrations"
url: "https://drupalize.me/tutorial/custom-drupal-drupal-migrations?p=3116"
guide: "[[learn-migrate-drupal]]"
---

# Custom Drupal-to-Drupal Migrations

## Content

Drupal core provides support for migrating data from Drupal 6 or 7. The templates provided in core migrate your data in a very specific way. They attempt to copy things verbatim whenever possible. However, you may wish to alter this for your migrations. In this tutorial we are going to explore the various ways that you can alter the existing Drupal-to-Drupal migrations to meet your needs.

## Goal

Understand the process of using Migrate Plus and migration configuration entities to create a custom Drupal-to-Drupal migration.

## Prerequisites

- [Migration-Related Contributed Modules](https://drupalize.me/tutorial/migration-related-contributed-modules)
- [Migrate System Terms and Concepts](https://drupalize.me/tutorial/migrate-system-terms-and-concepts)
- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)
- [Install Drush with Composer](https://drupalize.me/tutorial/install-drush-using-composer)

When you [perform a Drupal-to-Drupal migration](https://drupalize.me/tutorial/drupal-drupal-migration-ui) using the [migration plugins provided by Drupal core](https://drupalize.me/tutorial/core-migration-modules) one of the biggest gotchas right now is that you can't configure the migration at all. Your only option is to run it. If your goal is to upgrade from Drupal 6 or 7 to the latest version of Drupal and leave everything as-is, this works great. However, here are many reasons you may need to customize a migration, such as:

- You wish to ignore certain items in a generated migration
- You may wish to alter your data structure (concat fields, change data formats, etc.)
- You may wish to consolidate certain content types, or user roles

As an example we're going to look at how we can migrate just the blog content from the Drupalize.Me site to the latest version of Drupal. In this case we want to start using the latest version of Drupal to manage our blog, but aren't ready to upgrade the rest of the site yet. The default Drupal-to-Drupal migration doesn't allow for this; it tries to move everything all at once. Our Drupal 7 site contains thousands of nodes, users, and configuration options that are not related to the blog. Instead, we're going to move only:

- The configuration that makes up the blog content type and associated fields
- The content of all nodes of the type *blog\_post* and associated images
- User accounts for anyone who has written a blog post
- Vocabularies and taxonomy terms related to blog posts

## Warning: migrations can be tricky

We want to acknowledge that while everything might work great in the pristine conditions of our laboratory they tend to get a bit finicky in the real world. It would be impossible for us to try and cover every possible scenario you might encounter, so instead we'll do our best to try and help prepare you for understanding where to look, and what you're looking at. Any migration is likely to be 20% coding, and 80% planning and debugging. It's just the nature of these things.

## Steps involved

At a very high level, the process is as follows:

- Install the required modules
- Tell the Migrate API where to find your source Drupal site
- Generate some migration configuration entities
- Create a new module to house your custom migration
- Export the migration configuration entities to YAML in your custom module
- Customize the migration YAML files to meet your needs
- Execute your custom migration

We'll spread this out across a couple of tutorials. This tutorial will serve to tie it all together.

## Install the required modules

Make sure you've got the following modules installed:

- Migrate (Drupal core)
- Migrate Drupal (Drupal core)
- Migrate Drupal UI (Drupal core)
- [Migrate Upgrade (drupal.org/project/migrate\_upgrade)](https://www.drupal.org/project/migrate_upgrade)
- Drush version 10.4+ or [Migrate Tools (drupal.org/project/migrate\_tools)](https://www.drupal.org/project/migrate_tools)
- [Migrate Plus (drupal.org/project/migrate\_plus)](https://www.drupal.org/project/migrate_plus)

*Note*: Installing the correct version of these contributed modules is important and depends on the version of Drupal you're using. Use the most recent version of each module.

If you're not already familiar with what Migrate Plus and Migrate Upgrade are used for when doing a Drupal-to-Drupal migration check out [Why Use Migrate Upgrade and Migrate Plus?](https://drupalize.me/tutorial/why-use-migrate-upgrade-and-migrate-plus).

## Tell the Migrate API where to find your source Drupal site

Update the *settings.php* file for your destination Drupal site to include an array that defines how the Migrate API can access the database from your old Drupal site. Pay attention to the array keys here, `['migrate']['default']`; by default the Migrate API will use the `$databases` connection named `'migrate'`. You can change this via configuration, but unless you have a reason then it's easier to just conform to the defaults.

```
$databases['migrate']['default'] = array (
  'database' => 'd7_db',
  'username' => 'd7_dbuser',
  'password' => 'd7_dbpass',
  'prefix' => '',
  'host' => 'localhost',
  'port' => '3306',
  'namespace' => 'Drupal\\Core\\Database\\Driver\\mysql',
  'driver' => 'mysql',
);
```

If you're curious, there's a little more about how this works in the [Write a Custom Source Plugin](https://drupalize.me/tutorial/write-custom-source-plugin) tutorial.

## Generate some migration configuration entities

When you migrate from a previous version of Drupal the Migrate API uses a set of migration templates provided by Drupal core and contributed modules in order to dynamically generate the migrations that end up being run. For example, in our case, our Drupal 7 site has a handful of custom content types including one named *blog\_post*. It would be impossible for Drupal to know about every possible configuration of every site, so instead it contains templates for what the migration of a content type's content might look like. These templates are used for the basis of dynamic migrations.

A dynamic migration is created when the Migrate API performs an inspection of your Drupal source site. Using its knowledge of how previous versions of Drupal work, it's able to figure out that our site has a *blog\_post* content type, and that that content type has some custom fields. Using that information it can generate a migration that looks a lot like the [custom YAML migrations you might write](https://drupalize.me/tutorial/write-custom-migration) yourself.

When you [run a standard upgrade using the migration tools](https://drupalize.me/tutorial/drupal-drupal-migration-ui), these dynamic migrations are stored in memory, executed immediately, and then removed at the end of the request. However, in this case, we want to make some changes to the dynamically-generated migrations before they are executed.

You can do so by following [this tutorial on generating migration configuration entities](https://drupalize.me/tutorial/create-migrations-core-templates).

After that you can use `drush migrate-status` to list all the generated but not-yet-executed migrations. These migrations can now be run, rolled-back, and otherwise manipulated just like custom migrations. Learn about [running custom migrations via the CLI](https://drupalize.me/tutorial/run-custom-migrations).

## Create a custom module

After generating the migration configuration entities you can go ahead and start modifying them. [Edit the configuration using Drush](https://drupalize.me/tutorial/inspect-configuration-drush) to make your changes. In some cases this might be adequate. However, we recommend getting these configuration entities out of the database and into files. This allows for version control, deployment to testing environments, and better collaboration with team members.

You can also be selective here and choose to include some but not all the generated migrations. This is helpful in our use case where we only want to move the *blog\_post* content type and some users. We'll copy only those migrations, and leave out all the other migrations that we don't need.

Learn how to [create a module for custom Drupal-to-Drupal migrations](https://drupalize.me/tutorial/export-migration-configuration-entities-module)

## Customizing things further

This is where it gets really fun. Now, you can start editing the YAML files that represent the migrations in your custom module. You can do things like:

- Alter the data model so that what was 2 fields in your old Drupal site becomes 1 field on the new site
- Change field names on the destination Drupal site and update the mapping in the migration
- Change the source plugin used
- Add mappings for a new field that doesn't exist on the old site and give it a default value on the new site
- Change the process plugin used to map a field from the default `get` to any other process plugin

With our custom module started, we've now also got a home for writing additional plugins that allow us to further customize our migration. [This tutorial walks through creating a custom source plugin](https://drupalize.me/tutorial/write-custom-source-plugin) that limits the list of users migrated to only those that have written 1 or more blog posts, and then updates the related migration to use the new source plugin.

Ideas about other things you could do with a custom source plugin:

- Limit the values for other data sets that are being migrated
- Use `::prepareRow()` to generate new computed fields and then update your mapping in the YAML file

You can also implement `hook_migrate_prepare_row()` to further customize the migration. In [this tutorial](https://drupalize.me/tutorial/use-hookmigratepreparerow) we demonstrate how to use `hook_migrate_prepare_row()` to limit the content types that are migrated to just the *blog\_post* content type, and only the relevant fields.

If you want dive further into the process of merging your content types before migrating, we recommend reading this article, [Merging Entities During a Migration to Drupal 8](https://www.lullabot.com/articles/merging-entities-during-a-migration-to-drupal-8), which will walk you through an example of migrating part of a Drupal 7 site to the latest version of Drupal, with an eye toward cleaning up the content model. You'll learn:

- To write a custom migrate source plugin in your destination Drupal codebase that inherits from another source plugin. See also these related tutorials: [Source Plugins](https://drupalize.me/tutorial/source-plugins) and [Write a Custom Source Plugin](https://drupalize.me/tutorial/write-custom-source-plugin).
- To take advantage of object-oriented inheritance to pull field values from other entities with minimal code.
- To use the Drupal migrate row object to make more values available in your migration YAML configuration. See [Export Migration Configuration Entities into a Module](https://drupalize.me/tutorial/export-migration-configuration-entities-module).

## Recap

Hopefully by now you're getting some ideas about why you might want to create a custom Drupal-to-Drupal migration and now posses a framework for how to get started, which includes:

- Using Migrate Upgrade to generate migration configuration entities that can be individually inspected, changed, and executed
- Exporting generated migrations into a custom module for better tracking and collaboration
- Further customizing the Drupal-to-Drupal migration by using custom source plugins and `hook_migrate_prepare_row()`

## Further your understanding

- Can you explain the effect of the `--configure-only` flag when used with the `drush migrate-upgrade` command?
- You could also [write a custom migration](https://drupalize.me/tutorial/write-custom-migration) from scratch using the source plugins from core instead of following this process. Which makes the most sense for your use case?
- Check out the tutorial, [Configuration Data Storage](https://drupalize.me/tutorial/configuration-data-types), to learn more about the configuration system in Drupal. In our experience, the better you understand how configuration storage works the easier it will be to troubleshoot custom migrations
- Read about creating custom [source](https://drupalize.me/tutorial/source-plugins) and [process](https://drupalize.me/tutorial/process-plugins) plugins which you'll be able to use in your custom migration

## Additional resources

- Read about [preparing for a migration](https://drupalize.me/tutorial/prepare-drupal-drupal-migration) before you get started
- [Migration-Related Contributed Modules](https://drupalize.me/tutorial/migration-related-contributed-modules)
- [Why Use Migrate Upgrade and Migrate Plus?](https://drupalize.me/tutorial/why-use-migrate-upgrade-and-migrate-plus)
- [Merging Entities During a Migration to Drupal 8](https://www.lullabot.com/articles/merging-entities-during-a-migration-to-drupal-8) (lullabot.com)
- [Write a Custom Source Plugin](https://drupalize.me/tutorial/write-custom-source-plugin) (Drupalize.Me)
- [Inspect Configuration with Drush](https://drupalize.me/tutorial/inspect-configuration-drush) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Drupal-to-Drupal Migration with Drush](/tutorial/drupal-drupal-migration-drush?p=3116)

Next
[Why Use Migrate Upgrade and Migrate Plus?](/tutorial/why-use-migrate-upgrade-and-migrate-plus?p=3116)

Clear History

Ask Drupalize.Me AI

close