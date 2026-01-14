---
title: "Customize an Existing Source Plugin"
url: "https://drupalize.me/tutorial/customize-existing-source-plugin?p=3116"
guide: "[[learn-migrate-drupal]]"
order: 19
---

# Customize an Existing Source Plugin

## Content

As part of creating a custom Drupal-to-Drupal migration we want to limit the set of users that are migrated from our source site into our destination Drupal site. In this tutorial we'll:

- Extend the existing source plugin
- Alter the query that's used to select users from our source site
- Update our user migration to use the new source plugin

By the end of this tutorial you should be able to override the core source plugins used when migrating from prior versions of Drupal in order to gain more control over exactly what is migrated.

## Goal

Write and use a custom source plugin that limits the set of users migrated during a custom Drupal-to-Drupal migration.

## Prerequisites

- [Custom Drupal-to-Drupal Migrations](https://drupalize.me/tutorial/custom-drupal-drupal-migrations)
- [Export Migration Configuration Entities into a Module](https://drupalize.me/tutorial/export-migration-configuration-entities-module)

## Getting started

You could alternatively achieve this goal using [hook\_migrate\_prepare\_row()](https://drupalize.me/tutorial/use-hookmigratepreparerow) to filter out and skip users that you don't want to migrate. One benefit of creating a source plugin though is that the total number of items to migrate listed by commands like `drush migrate-status` will accurately reflect what's going to be migrated.

This tutorial assumes that you've been following along with the [Custom Drupal-to-Drupal Migrations](https://drupalize.me/tutorial/custom-drupal-drupal-migrations) and [Export Migration Configuration Entities into a Module](https://drupalize.me/tutorial/export-migration-configuration-entities-module) tutorials. We'll be building off what was started there. If you're writing your own custom migration though this should still serve as a useful example of how to get started further customizing your Drupal-to-Drupal migration.

Additionally, if you've never written a custom source plugin check out our [Write a Custom Source Plugin](https://drupalize.me/tutorial/write-custom-source-plugin) tutorial, which covers the concepts in more detail.

## Extending an existing source plugin

In our use case we want to customize the source plugin used to migrate users from Drupal 7 into our destination Drupal site. Instead of migrating the thousands of user accounts on Drupalize.Me, we only want to migrate those that have authored one or more blog posts.

Our existing migration looks like this:

### Excerpt from *migrate\_plus.migration.dmeblog\_d7\_user.yml*

```
id: dmeblog_d7_user
migration_group: dmeblog_migrate
label: 'User accounts'
source:
  plugin: d7_user
```

It's currently using the source plugin `d7_user`, which maps to the PHP class `Drupal\user\Plugin\migrate\source\d7\User`. We can extend the existing class and override just the relevant parts. Here's the code that makes up our custom source plugin.

### File: *dmeblog\_migrate/src/Plugin/migrate/source/d7/User.php*

```
<?php

namespace Drupal\dmeblog_migrate\Plugin\migrate\source\d7;

use Drupal\user\Plugin\migrate\source\d7\User as D7User;

/**
 * Fetch only users that have authored a blog post.
 *
 * Rather than start from scratch we extend the Drupal\user\Plugin\migrate\source\d7\User
 * class and override the query method. Then change the query that gets used to
 * select only users who have authored one or more blog posts.
 *
 * @MigrateSource(
 *   id = "custom_d7_user",
     source_module = "user"
 * )
 */
class User extends D7User {

  /**
   * Override the query() method, and provide a custom query that selects just
   * the users we're interested in.
   */
  public function query() {
    // Our custom query returns the set of fields as
    // Drupal\user\Plugin\migrate\source\d7\User::query(), but contains some
    // extra logic. Including a join to the node table, and a new condition that
    // effectively limits the rows returned to only those users who have
    // authored one-or-more blog posts.
    $query = $this->select('users', 'u');
    $query->join('node', 'n', 'n.uid = u.uid');
    $query->fields('u');
    $query->distinct()
      ->condition('n.type', 'blog_post', '=');
    return $query;
  }
}
```

And that's it. Since all we're doing is changing the list of users that are migrated we can rely on the existing `Drupal\user\Plugin\migrate\source\d7\User` class to do the rest of the work.

## Using the new source plugin

In order to make our custom migration use this new source plugin we need to alter the *migrate\_plus.migration.dmeblog\_d7\_user.yml* file. Change the `id:` line to use the ID of our new source plugin taken from its annotation.

### Example

```
id: dmeblog_d7_user
migration_group: dmeblog_migrate
label: 'User accounts'
source:
# Use our custom_d7_user plugin (Drupal\dmeblog_migrate\Plugin\migrate\source\d7\User)
# See the @MigrateSource annotation.
  plugin: custom_d7_user
```

After customizing the migration YAML file you'll need to reload the configuration before the migration system will see your changes. The [Configuration development module](https://www.drupal.org/project/config_devel) is helpful for this.

## Recap

In this tutorial we created a new custom source plugin that extends the existing `Drupal\user\Plugin\migrate\source\d7\User` plugin. Our custom plugin contains code to limit the set of users that are returned when querying the source, effectively limiting the users that will be migrated. We then updated our migration YAML file so that it uses the new `custom_d7_user` plugin we created.

## Further your understanding

- What advantages does this method have over using [hook\_migrate\_prepare\_row()](https://drupalize.me/tutorial/use-hookmigratepreparerow)?
- Can you rewrite this custom source plugin so that it only migrates users who are in a specific role?

## Additional resources

- [Understanding Source Plugins](https://drupalize.me/tutorial/source-plugins) (Drupalize.Me)
- [Write a Custom Source Plugin](https://drupalize.me/tutorial/write-custom-source-plugin) (Drupalize.Me)
- [Configuration development module](https://www.drupal.org/project/config_devel) (Drupal.org)
- [Change record: Use 'source\_module' and 'destination\_module' annotation to indicate module responsible for migration](https://www.drupal.org/node/2831566) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Export Migration Configuration Entities into a Module](/tutorial/export-migration-configuration-entities-module?p=3116)

Next
[Use hook\_migrate\_prepare\_row()](/tutorial/use-hookmigratepreparerow?p=3116)

Clear History

Ask Drupalize.Me AI

close