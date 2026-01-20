---
title: "get an overview"
url: "https://drupalize.me/tutorial/introduction-migrations-drupal"
guide: "[[learn-migrate-drupal]]"
order: 31
---

# get an overview

## Content

Whether you're updating from Drupal 6 or Drupal 7, or importing data from some other source, you need to know about the migrate system in the latest version of Drupal. This tutorial provides an overview and links to additional tutorials where you can learn more about how all the individual parts work.

By the end of this tutorial you should have a better understanding of what the migration system is capable of and know where to find more information about how to use it.

## Goal

Know where to get started with your Drupal upgrade or migration project.

## Prerequisites

- None.

## What is a migration?

We use the word "migration" as a generic term for any process that seeks to take data from some source external to the current Drupal site (Drupal 8 or higher) and use it to automatically create nodes, users, configuration, and any other component of your site. In short, automating what might otherwise be a tedious job of copying and pasting.

The core Drupal software includes a migration system whose purpose is to make it easier to import data from a variety of sources. This migration system was introduced and stabilized in Drupal 8 and continues to be improved. The migrate system is both a framework designed to facilitate writing custom migrations, and an implementation of that framework aimed at Drupal-to-Drupal migrations.

The system consists of three core modules: Migrate, Migrate Drupal, and Migrate Drupal UI. Learn more about the role that each fulfills in the [Core Migration Modules](https://drupalize.me/tutorial/core-migration-modules) tutorial, as well as plugins contained by other core modules that make use of the migration framework to ensure the content or configuration they handle has a migration path.

*Note:* resources labeled with Drupal 8 should work in the latest version of Drupal unless specifically noted.

## Upgrade, update, or migrate?

Previous versions of Drupal provided an upgrade mechanism that allowed for in-place version updates, which worked for both major version *upgrades*, and minor version *updates*. While convenient, this method also had some significant downsides. Especially tricky was moving between major versions of Drupal. Users often wanted to preserve their existing content, while making changes to take advantage of new systems -- a process that begins to resemble a migration much more than an in-place upgrade.

So now in Drupal there is no direct upgrade from Drupal 6 or 7 to the latest version of Drupal. Instead *upgrading* to the latest version of Drupal will require you to migrate your site and files from a previous Drupal version (version 7 or lower) to the latest version of Drupal (Drupal 8 or higher). The migrate system in core aims to make this process as easy as possible.

As of right now, the Migrate Drupal and Migrate Drupal UI modules provide a way to:

- Connect your destination Drupal site to your Drupal 6 or 7 source
- Extract both the content and configuration
- Transform it into the new format
- Save it into your destination Drupal site using the latest version of Drupal

For example, the Migrate Drupal module is smart enough to understand both Drupal 6 and latest-Drupal nodes, and can extract a Drupal 6 node and all its field data and then save it as a current version of Drupal node. In fact, it's so smart that it'll even take care of migrating the content type definition for you.

You can read [more about this change](https://www.drupal.org/upgrade/migrate) on Drupal.org.

For many people, this is likely what you're looking for: a way to upgrade your older Drupal 6 or Drupal 7 site to the shiny latest version of Drupal. The first part of this guide covers the process of preparing for and executing a Drupal-to-Drupal migration. If this sounds like what you're trying to do, check out the [Preparing for a Drupal-to-Drupal Migration](https://drupalize.me/tutorial/prepare-drupal-drupal-migration) tutorial.

## Migrate from anywhere

The migration system makes it possible to pull content into Drupal from just about anywhere. The core API supports extraction from any SQL data source, including previous versions of Drupal. [Contributed modules](https://drupalize.me/tutorial/migration-related-contributed-modules) extend this system to support other data types like CSV or JSON, as well as other platforms like WordPress.

Some of the existing data sources include:

- MySQL, MariaDB
- Previous versions of Drupal
- CSV
- JSON, you could even use a REST endpoint
- XML
- Etc.

If there isn't already a way to extract the data from your current data store you can [write a custom source plugin](https://drupalize.me/tutorial/write-custom-source-plugin). Source plugins are the mechanism that allows the Drupal migration framework to understand the ins and outs of extracting data from different data-stores. Source plugins can also be smart about the data-store, for example a WordPress source plugin, written by someone who understands how WordPress works, could be smart enough to dynamically update the fields available for extraction based on the WordPress site in question.

## Migrate understands Drupal

When you import data into Drupal you're dealing with entities, fields, and configuration. The migrate framework understands how all of these Drupalisms work, making it possible to save an array of content as a new Drupal user account without having to understand the intricacies of Drupal's database schema, field system, or password hashing algorithms.

The migrate system is smart about things like content type configuration. It will automatically import content into whatever fields you've defined for your application's unique information architecture. And it even knows how to validate the content for each field type prior to saving new data.

Some of the things you can create with a migration include:

- Content (nodes, taxonomy, any generic entity) including any attached files and images
- Content types
- User accounts
- Roles and permissions
- Simple configuration like the site name
- Complex configuration like image styles
- Etc.

The majority of the work that you'll do when writing a migration path is creating migration plugins. Migration plugins are responsible for mapping the data extracted from a source to the Drupal definition of that data. For example, mapping the title and sub-title of an article in your previous CMS to the article node type's title and custom sub-title fields in Drupal. And perhaps opting to transform the data during the import using process plugins.

## Execute, rollback, and debug with ease

In addition to making it possible to write a migration, the system also facilitates executing those migrations. Using either the UI or Drush, you can do things like:

- Execute a complete migration plan
- Run an individual migration, and its dependencies, without running the complete plan
- Run a partial migration in order to facilitate testing and debugging
- Rollback a migration that was previously run to allow for re-running it after making adjustments

At the moment, Drupal core provides a relatively simple [UI for handling Drupal-to-Drupal migrations](https://drupalize.me/tutorial/drupal-drupal-migration-ui), and contributed modules doing the bulk of the work in this space. This space is currently the most volatile and subject to change. The tools for running a migration are all rapidly evolving and adding new features. The more people use them, the better they will get. In the future we will likely see more of this functionality moved into Drupal core as it stabilizes.

Being able to execute migrations with Drush commands is extremely useful as it allows for better automation of processes that can be time consuming and cumbersome to practice, test, and debug.

## Where should you start?

There is rarely a single way, or even necessarily a right way of performing a migration, a fact that makes learning how to perform one especially challenging. Every site is different, and every site grows organically over time. All user-generated content is dirty and needs massaging. Everyone performs migrations under different circumstances and for different reasons.

So, rather than attempt to define a gold standard for how a migration should be performed, with this guide we've set out to help provide you with the information you need to make the best decision for your unique migration, and the know how to be able to address and overcome the hurdles you encounter along the way.

We suggest you start by reviewing our [Prepare for a Drupal-to-Drupal Migration](https://drupalize.me/tutorial/prepare-drupal-drupal-migration) tutorial. Next, make a migration plan before writing any custom code, or running any Drush commands.

## Recap

In this tutorial:

- we defined what migrations are (importing data from outside of your site),
- the difference between upgrades and updates, and
- a really high-level look at what Drupal's migrate system can do.

We discussed how the Migrate API can read from many disparate sources and how it understands Drupal's internals in a way that makes it easier to do things the "Drupal way". Finally, we laid out some background information about how and where to get started with your own migration project.

## Further your understanding

- What is the difference between an upgrade and a migration?
- What are the benefits of using the migration framework in core vs writing custom scripts to perform the task?

## Additional resources

- [Migrate documentation from the Drupal.org handbook](https://www.drupal.org/upgrade/migrate) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Clear History

Ask Drupalize.Me AI

close