---
title: "Common Issues with Migrations"
url: "https://drupalize.me/tutorial/common-issues-migrations?p=3116"
guide: "[[learn-migrate-drupal]]"
order: 12
---

# Common Issues with Migrations

## Content

The Drupal-to-Drupal migration system is still a work in progress. As such, there are a few things that simply don't work, and a few others that still have kinks to be ironed out. In this tutorial, we'll look at some of the common hang-ups that we've encountered, the status of resolving those issues, and what your options are in the meantime.

## Goal

Know where to find more information about common issues you might encounter while performing a Drupal-to-Drupal migration.

## Prerequisites

- [Introduction to Migrations with Drupal](https://drupalize.me/tutorial/introduction-migrations-drupal)

## Overview

- As of Drupal 8.5.x the core Migrate API is considered stable and no major backwards compatibility breaking changes are expected. If you're writing custom migrations, you're good to go.
- If you're doing a Drupal-to-Drupal migration, there are still a few known issues. Though none of them will block you from proceeding. This issue, now marked as "fixed", [[META] Drupal 7 to Drupal 8 Migration path](https://www.drupal.org/node/2456259), is a central tracking point for the status of all Drupal 7 core module migration paths.

Below are a few additional things to keep in mind when preparing for a migration.

## Features module

The [Drupal 7 Features module](https://www.drupal.org/project/features) is often used in Drupal 7 sites to allow for the storage of configuration information in files instead of the database. This can cause problems when performing a Drupal-to-Drupal migration since any information that is stored exclusively in Features and not in the database will not be accessible to the Drupal Upgrade source plugins. One example might be Views that have been exported into features.

If you have configuration data stored in Features that you want migrated to a version of Drupal that uses [configuration management](https://drupalize.me/series/configuration-management), the recommended best practice is to move it into the database first, so that the migration system can access it.

This issue, [Provide way to Import views/true exportables back to the database](https://www.drupal.org/project/features/issues/663136), contains comments and patches on how to go about doing this.

## Views module

Unlike most other configuration, Views are not automatically migrated from Drupal 6/7 to the latest version of Drupal. There was some initial work done towards automatic migration of Drupal 7 views in this issue, [Upgrade path for Views from Drupal 6 and 7](https://www.drupal.org/node/2500547). However, the current consensus is that it's far too complex and time consuming to account for every possible edge case. Since core will only accept a complete solution, this isn't likely to happen anytime soon.

This can be worked around by manually recreating the views you need in your destination Drupal site.

There is also ongoing work in a couple of different contributed modules that may be worth at least exploring. **Update:** Neither of these modules has been updated in quite some time and at this point we recommended them purely as reference code for exploring your own automated solutions for migrating Views.

- [View Migration](https://www.drupal.org/project/view_migration) (Drupal.org)
- [Migrate Views](https://www.drupal.org/project/migrate_views) (Drupal.org)

## References and Entity References

In Drupal 7, there are a variety of different contributed modules that make it possible to create relationships between entities. Some of these are Entity Reference, References, Node Reference, and User Reference. **Entity Reference** is now part of the core software and is the standard for creating these relationships going forward. This consolidation can be tricky during migrations.

Automatic migration for the Drupal 7 Entity Reference module was completed in [Upgrade path to entity reference field from 7.x](https://www.drupal.org/node/2611066). In our tests, this upgrade path works well.

Migrating from Drupal 7 References module fields isn't currently supported. Instead, you should use the [Reference to EntityReference Field Migration](https://www.drupal.org/project/entityreference_migration) to convert your Drupal 7 reference fields to entity reference fields before attempting a migration.

## Don't panic!

Don't let this hold you back from starting your migration. Many of the issues have patches included with them that work, or mostly work. If you're trying to perform a migration and are dependent on the repair of one of these issues, give the patches a test and see if they work. Then let the community know how it went, so we can continue to improve the tools.

## Recap

In this tutorial, we looked at some of the known issues with Drupal's migration system, and where you can find more information about the current state of each issue. If you know of any others you think we should include in this list please let us know.

## Further your understanding

- Read through the community documentation, [Known issues when upgrading from Drupal 6 or 7 to Drupal 9 or higher](https://www.drupal.org/docs/upgrading-drupal/known-issues-when-upgrading-from-drupal-6-or-7-to-drupal-8-or-9) as there may be known issues listed there that apply to your site.

## Additional resources

- [Known issues when upgrading from Drupal 6 or 7 to Drupal 9 or higher](https://www.drupal.org/docs/upgrading-drupal/known-issues-when-upgrading-from-drupal-6-or-7-to-drupal-8-or-9) (Drupal.org)
- Learn how to [apply and test patches](https://drupalize.me/videos/test-patches?p=1176) in Drupal (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Drupal-to-Drupal Migration Planning: Content Inventory](/tutorial/drupal-drupal-migration-planning-content-inventory?p=3116)

Next
[Drupal-to-Drupal Migration with the UI](/tutorial/drupal-drupal-migration-ui?p=3116)

Clear History

Ask Drupalize.Me AI

close