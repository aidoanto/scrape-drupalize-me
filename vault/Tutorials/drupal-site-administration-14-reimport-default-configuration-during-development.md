---
title: "Reimport Default Configuration during Development"
url: "https://drupalize.me/tutorial/reimport-default-configuration-during-development?p=2478"
guide: "[[drupal-site-administration]]"
order: 14
---

# Reimport Default Configuration during Development

## Content

When working on configuration in a module, whether as part of a migration that uses Migrate Plus configuration entities, or while developing custom configuration entities, you'll often need to re-import the configuration stored in the *.yml* files of the modules *config/install/* or *config/optional/* directories. This is tricky though, because Drupal only reads in those default configuration settings when the module is first enabled. So any changes you make to those files after the module has been installed will not be reflected without these workarounds.

Knowing how to do this can improve the developer experience of [adding (or debugging) the default configuration](https://drupalize.me/tutorial/default-configuration-module) that's provided with a module. Or for anyone using Migrate Plus configuration entities as part of a migration.

In this tutorial we'll:

- Learn about the Configuration Development module
- Look at how you can use Drush to perform a partial configuration import
- Write an implementation of `hook_uninstall()` to remove a module's configuration when it's uninstalled

By the end of this tutorial you should be able to re-import the configuration provided by a module without having to uninstall and then reinstall the module.

## Goal

Efficiently import the contents of a module's *config/install/* directory during development without having to uninstall and then reinstall the module.

## Prerequisites

- [Overview: Configuration Management in Drupal](https://drupalize.me/tutorial/overview-configuration-management-drupal)

**Note:** The content of this tutorial was initially part of our [Learn to Migrate to Drupal guide](https://drupalize.me/guide/learn-migrate-drupal) which is why it references migration configuration. However, the techniques used will work for any configuration located in a module's *config/install/* directory.

## Re-import with Configuration Development module

You can use the [Configuration Development module](https://www.drupal.org/project/config_devel) to easily re-import the configuration continuously, or on-demand. The latter option is recommended, and is also the most efficient when dealing with more than just a single migration's configuration.

With *config\_devel* enabled, add the names of the files that contain your migrations to the module's auto-import configuration and save it. After doing so, Drupal will automatically import the listed YAML files on each page load so you no longer need to do it manually.

## Partial configuration imports with Drush

The Drush `config-import` command has a `--partial` flag which will allow you to specify a directory of configuration files to import.

Example:

```
drush config-import --partial --source=modules/custom/my_migration/config/install
```

This can be combined with file watching utilities like [fswatch](https://emcrisostomo.github.io/fswatch/) or [inotifywait](https://linux.die.net/man/1/inotifywait) which will watch a directory of files and execute a command whenever one is changed.

Example *migrate-reload.sh*:

```
#!/bin/bash

WATCH_DIR="/var/www/html/modules/custom/my_migration/config/install"
echo "Watching $WATCH_DIR ...";

fswatch -o -0 --event=Updated $WATCH_DIR | xargs -0 -I{} drush config-import --partial --yes --source="$WATCH_DIR"
```

## Implement hook\_uninstall() then reinstall the module

You could implement `hook_uninstall()` in your migration module's *mymodule.install* file, and then uninstall and install your module again each time. With Drush: `drush pmu MODULENAME && drush en MODULENAME --y`, replacing *MODULENAME* with the name of the custom module containing your migration.

```
<?php
use \Drupal\Core\Database\Database;
 
/** 
 * Implements hook_uninstall(). 
 */ 
function mymodule_uninstall() { 
  $connection = Database::getConnection();
  $connection->query("DELETE FROM {config} WHERE name LIKE 'mymodule.migration.my_migration%'"); 
  drupal_flush_all_caches();
} 
?>
```

Alternatively, you can declare that the migration has a dependency on the module that contains it. So that when the module is uninstalled the configuration is also removed. This does essentially the same thing as the `hook_uninstall()` above.

```
dependencies:
  enforced:
    module:
    # By adding the module that provided this migration/configuration here, it
    # will be removed when the module is uninstalled.
    - mymodule
```

## Recap

In this tutorial we looked at 3 different ways you can re-import the contents of a module's *config/install/* and *config/optional/* directories during development.

## Further your understanding

- How are you re-importing your module's configuration while the configuration is under development? How does using one of the other method's described in this tutorial change your workflow? What could be improved?

## Additional resources

- [Configuration Development module](https://www.drupal.org/project/config_devel) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Automate Deployment of Configuration](/tutorial/automate-deployment-configuration?p=2478)

Clear History

Ask Drupalize.Me AI

close