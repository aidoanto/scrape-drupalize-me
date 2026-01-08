---
title: "Clear Drupal's Cachefree"
url: "https://drupalize.me/tutorial/clear-drupals-cache?p=3285"
guide: "[[drupal-site-administration]]"
---

# Clear Drupal's Cachefree

## Content

Knowing how to clear Drupal's cache is an important skill for any developer. You'll likely find yourself doing it frequently in order to get Drupal to register the changes you make to your code, or other updates you make via the UI. It is also a good first step to trouble shooting problems with your Drupal site: Clear the cache before you do any other debugging to ensure it's not just a bad cache entry.

## Goal

Learn three methods of clearing Drupal's cache: via the administrative UI, with Drush, and by truncating tables in the database.

## Prerequisites

- (Optional) [Concept: Cache](https://drupalize.me/tutorial/user-guide/prevent-cache?p=2398) (Drupal User Guide)

## Overview

There are two common ways to clear Drupal's cache: via the UI, or with Drush.

## Clearing the cache via the UI

### Go to the Performance administrative page

In the *Manage* administrative menu, navigate to *Configuration* > *Performance* (*admin/config/development/performance*).

### Select the "clear all caches" button

Image

![Clear all caches](/sites/default/files/styles/max_800w/public/tutorials/images/drupal_clear_cache_ui.png?itok=PJgKdjhP)

After successfully clearing the cache Drupal should display the message "Caches cleared."

### Add Performance page to Shortcuts

Depending on your role, you may be clearing the cache a lot! Add the Performance page to your Shortcuts so that you can access the page more quickly. Click on the star icon next to the title, "Performance". The star icon will change from an outline of a star to a filled-in yellow star. Access Shortcuts via the Admin Toolbar.

Image

![Add Performance to Shortcuts](/sites/default/files/styles/max_800w/public/tutorials/images/performance-add-to-shortcut.png?itok=z_hvwR0k)

## Clearing the cache with Drush

To clear all caches, use the `cache-rebuild` command: `drush cache-rebuild`. This will empty all caches and rebuild the data required for Drupal to execute a page request. Alternatively, use the aliased commands `drush cr` or `drush rebuild`.

### Open a Terminal window and `cd` to your Drupal site root

If you're using [Drush aliases](https://drupalize.me/tutorial/drush-site-aliases), you can skip this step.

### Run the command `drush cache-rebuild` (`drush cr`)

Wait for the command to successfully execute and return to your site.

Image

![drush cr demo](/sites/default/files/styles/max_800w/public/tutorials/images/drush_cr_terminal.png?itok=HP8mqWm_)

### Reload the page you were working on in your browser

It might take a bit longer than usual since the cache has been rebuilt.

## What's the difference between cache-clear and cache-rebuild?

You may have been used to using "drush cc all" aka `drush clear-cache`. Now it's `drush cache-rebuild` or `drush cr`, for short. What's the difference and why the change?

Caching is widespread in Drupal and creates many interdependencies. Improperly or incomplete cache flushing operations can cause the site to fatally error. In order to guarantee that old data is properly flushed and the site stays up and running, `drush cache-rebuild` both rebuilds or re-bootstraps the Drupal site in addition to clearing the cache. Additionally, the Drush command cache is cleared with `drush cache-rebuild`, since that was one of the caches included in the old `drush cache-clear` command.

Drush's `cache-rebuild` command does the following:

- Clears the APC cache
- Bootstraps Drupal
- Calls `drupal_rebuild()`
- Clears the Drush cache (to maintain consistency with Drupal 7's drush cache-clear command)

If you'd like to take a peek under the hood of Drush's rebuild method, check out [drush/src/Commands/core/CacheCommands.php](https://github.com/drush-ops/drush/blob/9.5.x/src/Commands/core/CacheCommands.php#L179) (line 179).

## Truncate cache-related database tables

Another method of clearing the cache is to truncate—or clear all the data from—the cache-related database tables. These are all the tables that begin with "cache\_" (after the site-specific table prefix, if there is one).

In a SQL GUI application like Sequel Pro, which is what I like to use, this is easily accomplished by connecting to the server, selecting your site's database, highlighting all of the tables beginning with `cache_`, ctrl-clicking and selecting **Truncate tables**. Confirm that you do when the alert pops up. Other database administrative programs will also have the ability to truncate tables.

Image

![Truncate tables with Sequel Pro](/sites/default/files/styles/max_800w/public/tutorials/images/truncate_cache_tables.png?itok=R8po7hZo)

Or, from the mysql CLI or a SQL command field in a database administrative tool (like PhpMyAdmin or others), you would run the following:

```
TRUNCATE cache_config;
TRUNCATE cache_container;
TRUNCATE cache_data;
TRUNCATE cache_default;
TRUNCATE cache_discovery;
TRUNCATE cache_dynamic_page_cache;
TRUNCATE cache_entity;
TRUNCATE cache_menu;
TRUNCATE cache_render;
TRUNCATE cache_toolbar;
```

## Recap

In this tutorial, you learned three methods for clearing Drupal's cache: via the administrative performance page at *admin/config/development/performance*, with `drush cache-rebuild` or `drush cr`, and by truncating *cache\_* tables in the database.

## Further your understanding

- Now that you know how to rebuild Drupal's cache, learn how to turn off certain caches to work on theming and front-end development in [Configure Your Environment for Theme Development](https://drupalize.me/tutorial/configure-your-environment-theme-development).

## Additional resources

- [Clearing or rebuilding Drupal's cache](https://www.drupal.org/documentation/clearing-rebuilding-cache) (Drupal.org)
- [Drush cache-rebuild](https://drushcommands.com/drush-9x/cache/cache:rebuild/) (drushcommands.com)
- [drupal\_rebuild()](https://api.drupal.org/api/drupal/core!includes!utility.inc/function/drupal_rebuild/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Clear History

Ask Drupalize.Me AI

close