---
title: "Why Use Migrate Upgrade and Migrate Plus?"
url: "https://drupalize.me/tutorial/why-use-migrate-upgrade-and-migrate-plus?p=3116"
guide: "[[learn-migrate-drupal]]"
---

# Why Use Migrate Upgrade and Migrate Plus?

## Content

Why use Migrate Upgrade and Migrate Plus? The short answer is: because it'll save you from having to type out a bunch of YAML by scaffolding a migration for you.

The contributed [Migrate Plus](https://www.drupal.org/project/migrate_plus) and [Migrate Upgrade](https://www.drupal.org/project/migrate_upgrade) modules are commonly used to aid in the process of performing a Drupal-to-Drupal migration. The combination of the two makes it easier to customize the configuration of individual migrations on a per-project basis by allowing you to edit each individual migrations configuration using the same mechanics that you would to [write a custom migration](https://drupalize.me/tutorial/write-custom-migration).

It's not the only approach to making these changes, but for many people (including us), it's the most efficient way.

In this tutorial we'll:

- Get a more in-depth look at the role of the Migrate Plus and Migrate Upgrade modules
- Discuss the use cases for using them as part of a Drupal-to-Drupal migration

By the end of this tutorial you should be able to explain what both the Migrate Plus and Migrate Upgrade modules are used for.

## Goal

Explain the role of the contributed Migrate Plus and Migrate Upgrade modules.

## Prerequisites

- [Custom Drupal-to-Drupal Migrations](https://drupalize.me/tutorial/custom-drupal-drupal-migrations)

## How Migrate Drupal assembles a monolithic migration

First, a little background. When you perform a Drupal-to-Drupal migration the core Migrate Drupal module connects to and inspects the source site, and then uses the information it finds to generate all the individual migrations required. Or, at least it tries to. Understanding a bit about how that process works can help make debugging migrations a bit less of a "black box".

Most core modules, and many contributed modules, have a *migrations/* directory of *.yml* migration plugins. These are responsible for knowing how to extract data from the Drupal 7 version of the module, transform it, and load it into the Drupal 8+ version of the module. In order for these plugins to have any effect the module has to be enabled in the Drupal destination site **before** the migration is executed.

Think of these *.yml* migration files as templates. In some cases the data to migrate is relatively simple and the template will work as-is. In others, though, the source data can vary depending on configuration and other factors. So the module responsible for the data needs to analyze the source site before it can know exactly what it needs to do for the migration.

Sometimes there's no Drupal 8+ version of the module. For example [Address Field](https://www.drupal.org/project/addressfield) was popular in the Drupal 7, but has no Drupal 8 version. The [Address](https://www.drupal.org/project/address) module is the Drupal 8+ equivalent. And the Address module contains migration plugins for extracting Drupal 7 Address Field data and importing it into the new Address module.

Sometimes there are modules like [Media Migration](https://www.drupal.org/project/media_migration) which attempt to deal with a whole class of common Drupal-to-Drupal migration needs. Usually this relates to scenarios where best practices for how to do something have changed between versions of Drupal. In this case converting Drupal 7 image fields to Drupal 9 Media entities and updating all the various places those fields are used.

Some of the *.yml* migration files are templates for a [deriver](https://drupalize.me/tutorial/plugin-derivatives). Take a look at the *core/node/migrations/d7\_complete.yml* file which contains this line `deriver: Drupal\node\Plugin\migrate\D7NodeDeriver`. That tells the migration system that instead of treating this file as an individual migration plugin it should instead use the `D7NodeDeriver` class to dynamically create one migration for each node type. In this case the contents of the *.yml* file are a template. The deriver can alter, and extend, the template. In the case of nodes, it'll do some introspection of the Drupal 7 site to figure out what different fields are attached to each node type and then effectively generate the `process:` section of the YAML file necessary to migrate those fields.

This happens for configuration, too. There is code, for example, that will look at your Drupal 7 source sites content types and fields and then generate the individual migrations necessary to recreate those same content types and fields in the destination site.

This is all done in memory, and it's done **every time you run a migration command** like `drush migrate:status` or `drush migrate:import`. This means that instead of editing a migration's YAML configuration like you would if you were writing a custom migration, you'll need to [implement hooks](https://drupalize.me/tutorial/what-are-hooks) that alter the logic used to generate the migration definition. This is ultimately more reusable (good for contributed modules or if you're migrating a lot of sites), but is also a less-friendly developer experience when working on the migration for an individual site.

When customizing the migration for a single site it's often easier to edit the YAML that defines the migration directly than it is to edit the PHP that generates the YAML file that runs the migration. And that's where the contributed Migrate Plus and Migrate Upgrade modules come into the picture. They allow you to work with the generated YAML rather then recreating it every time.

## Migrate Upgrade and Migrate Plus

All of the above migration discovery features, and the UI for using them, are provided by the Drupal core Migrate Drupal module. The contributed [Migrate Upgrade](https://www.drupal.org/project/migrate_upgrade) makes it possible to trigger the execution of these monolithic migrations via Drush.

Example:

```
drush migrate:upgrade
```

Though in practice we rarely use it that way, and instead use the `--configure-only` option which calculates the configuration for the monolithic migration, but then instead of running each individual migration it saves their configuration as [configuration entities](https://drupalize.me/tutorial/configuration-data-types).

The contributed [Migrate Plus](https://www.drupal.org/project/migrate_plus) has code that reads configuration entities like those created above, and uses a [plugin deriver](https://drupalize.me/tutorial/plugin-derivatives) to create migration plugins for the Migrate API. Effectively it makes it so that you can then run the individual migrations from Migrate Drupal one at a time. This makes debugging easier. And, you can edit them, which makes is possible to customize them without writing hooks.

Because the configuration management system data stores can export/import configuration entities as YAML files, it's possible to export the configuration into a module and put it in version control. Even better, because the configuration entities from Migrate Plus have the same schema as a migration YAML file (with a few additions for the configuration management system), it's easy to convert them to standard migrations instead of configuration entities and improve the overall developer experience of working on them.

## Customizing individual migrations via hooks

The alternative approach to customizing the configuration of an individual migration is to implement one or more hooks. Think of this as writing PHP code that influences what YAML configuration Migrate Upgrade would end up creating. And instead of exporting the YAML, editing it, and running that migration. You run the monolithic-style migration, but your PHP code changes what's happening during that migration.

The benefit of this approach is that you're writing PHP, and your configuration can be dynamically calculated. This is especially true for the following scenarios:

- Contributed modules that need to provide a migration path for the data their module manages, and that path can vary depending on how the module was used on the source site.
- Generic solutions to common problems. For example converting image fields to media entities is a common task for a migration, and if it's done in PHP, it's possible to provide a generic solution that'll work for many different sites; because, it can calculate the migration logic based on the source site's specific configuration.
- Custom migrations where your team needs to migrate a lot of similar sites and you find yourself needing to make the same customizations to the YAML migration files for every site. Encapsulating that logic in PHP can be more efficient, since you'll only need to do it once and can reuse the module on every site.

## Recap

Using a combination of Migrate Plus and Migrate Upgrade modules you can ask Migrate Drupal to generate, but not execute, a monolithic Drupal-to-Drupal migration. Then convert the resulting configuration into migration YAML files in a custom module. At which point you have a pretty good start on a Drupal-to-Drupal migration that you can customize as if it were a migration from any other source. From a developer experience perspective, this simplifies the work of customizing the migration.

## Further your understanding

- If you don't use Migrate Plus and Migrate upgrade how would you customize an individual migration that moves blog posts from Drupal 7 to Drupal 9?
- What's a better approach for your project editing migration YAML files or PHP hooks?

## Additional resources

- [Migrate Plus](https://www.drupal.org/project/migrate_plus) (Drupal.org)
- [Migrate Upgrade](https://www.drupal.org/project/migrate_plus) (Drupal.org)
- [What Are Hooks?](https://drupalize.me/tutorial/what-are-hooks) (Drupalize.Me)
- [Plugin Derivatives](https://drupalize.me/tutorial/plugin-derivatives) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Custom Drupal-to-Drupal Migrations](/tutorial/custom-drupal-drupal-migrations?p=3116)

Next
[Create Migrations from Core Templates](/tutorial/create-migrations-core-templates?p=3116)

Clear History

Ask Drupalize.Me AI

close