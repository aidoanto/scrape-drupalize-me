---
title: "Write a Custom Process Plugin"
url: "https://drupalize.me/tutorial/write-custom-process-plugin?p=3115"
guide: "[[learn-migrate-drupal]]"
---

# Write a Custom Process Plugin

## Content

This tutorial covers writing a custom process plugin that you can use to manipulate the value of any field during the process (or transform) phase of a migration. Process plugins take an individual field value provided by a source plugin, and perform transformations on that data before passing it along to the load phase.

In this tutorial we'll write a process plugin that can either uppercase an entire string or the first letter of each word in the string depending on configuration.

By the end of this tutorial you should know how to start writing your own process plugins.

## Goal

Write a migration process plugin that can convert an entire string, or the first letter of a string, to uppercase.

## Prerequisites

- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins)
- [Process Plugins](https://drupalize.me/tutorial/process-plugins)

Before you write your own process plugin make sure that it doesn't exist already. The [Understanding Process Plugins](https://drupalize.me/tutorial/process-plugins) tutorial provides a good list.

## The basics

Process plugins are managed by the [MigratePluginManager](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21MigratePluginManager.php/class/MigratePluginManager/).

Process plugins live in the `Drupal/{MY_MODULE}/src/Plugin/migrate/process` namespace. In our case this becomes `namespace Drupal\baseball_migration\Plugin\migrate\process`, and the code lives in the file *baseball\_migration/src/Plugin/migrate/process/StrToUpper.php*.

Process plugins use `\Drupal\migrate\Attribute\MigrateProcess` attributes. Generally all you'll need to specify is the `id`. View the [attribute class' documentation](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Attribute%21MigrateProcess.php/function/MigrateProcess%3A%3A__construct/) for details about the `handle_multiple` key, if you want to handle iteration of arrays yourself. The `id` specified here is the name you will use to refer to your source plugin when writing a migration.

Example attribute:

```
use Drupal\migrate\Attribute\MigrateProcess;

/**
 * This plugin converts a string to uppercase.
 */
#[MigrateProcess("strtoupper")]
```

Migrate process plugins implement `\Drupal\migrate\Plugin\MigrateProcessInterface`, though it's generally easiest to start by extending `\Drupal\migrate\ProcessPluginBase`. Then implement the transform method which does the actual processing.

```
use Drupal\migrate\Attribute\MigrateProcess;
use Drupal\migrate\ProcessPluginBase;
use Drupal\migrate\MigrateException;
use Drupal\migrate\MigrateExecutableInterface;
use Drupal\migrate\Row;

/**
 * This plugin converts a string to uppercase.
 */
#[MigrateProcess("strtoupper")]
class StrToUpper extends ProcessPluginBase {
  /**
   * {@inheritdoc}
   */
  public function transform($value, MigrateExecutableInterface $migrate_executable, Row $row, $destination_property) {
    // Do value transformation here ...
  }
}
```

The `$value` argument contains the field value that the plugin is currently manipulating. Perform any transformations on this value and then return the result.

The additional arguments are the migration in which the process is being executed, the row from the source currently being processed, and the destination property currently being worked on. These can provide additional context for processing, such as evaluating the value of another field in the row to determine how processing for this field should proceed.

## Example process plugin

Complete process plugin example:

```
<?php
/**
 * @file
 * Example of how to write a Migrate API process plugin.
 */

// Process plugins live in the Drupal\{MODULE}\Plugin\migrate\process
// namespace.
namespace Drupal\baseball_migration\Plugin\migrate\process;

use Drupal\migrate\Attribute\MigrateProcess;
use Drupal\migrate\ProcessPluginBase;
use Drupal\migrate\MigrateException;
use Drupal\migrate\MigrateExecutableInterface;
use Drupal\migrate\Row;

/**
 * This plugin converts a string to uppercase.
 */
#[MigrateProcess("strtoupper")]
class StrToUpper extends ProcessPluginBase {

  /**
   * {@inheritdoc}
   */
  public function transform($value, MigrateExecutableInterface $migrate_executable, Row $row, $destination_property) {
    // In the transform() method we perform whatever operations our process
    // plugin is going to do in order to transform the $value provided into its
    // desired form, and then return that value.
    if (is_string($value)) {
      // Check the plugin configuration to see if we should be using the ucfirst
      // or strtoupper function to perform our transformation. Configuration is
      // read from the migration YAML file where we've specified that we want
      // this process plugin to be used for a specific field.
      if (isset($this->configuration['ucfirst']) && $this->configuration['ucfirst'] == TRUE) {
        return ucfirst($value);
      }
      else {
        return strtoupper($value);
      }
    }
    else {
      // Throw an exception indicating our process plugin failed to transform
      // this value.
      throw new MigrateException(sprintf('%s is not a string', var_export($value, TRUE)));
    }
  }
}
```

## Use your custom process plugin

To use the StrToUpper process plugin we just created, refer to it by the ID from the attribute in your migration YAML file.

Example:

```
process:
  uid: uid
  name:
    plugin: strtoupper
    source: name
  field_first_name:
    plugin: strtoupper
    source: name
    # This example shows using the optional 'ucfirst' configuration
    # for the strtoupper plugin. If set to 'true' the plugin will
    # use the PHP ucfirst function instead of strtoupper and capitalize
    # just the first letter instead of the entire string.
    ucfirst: 'true'
  pass: pass
  mail: mail
```

## Using services

For more complex processing of data you may want to use a service instead of just calling a native PHP function like we've done above. [This article](http://www.drupalwatchdog.net/blog/2015/6/write-migrate-process-plugin-learn-drupal-8) demonstrates how you can use dependency injection to inject any service into your process plugin.

## Recap

In this tutorial we walked through writing a custom process plugin: a PHP class that lives in the `Drupal\{module_name}\Plugin\migrate\process` namespace and extends `Drupal\migrate\ProcessPluginBase`. Our process plugin can convert either an entire string, or just the first character of a string, to uppercase. We then looked at an example of how you can make use of custom process plugins in a migration by changing the migration YAML file.

## Further your understanding

- Give an example of a data manipulation you could perform in a custom process plugin that isn't provided by one of the existing plugins
- Can you figure out what the `handle_multiple` option for a process plugin attribute does?
- The StrToUpper process plugin could alternatively be written with no `transform()` method, and implement `StrToupper:ucfirst()` and `StrToUpper::strtoupper()` instead, can you figure out how? Hint, look at `ProcessPluginBase`.

## Additional resources

- [Understanding Process Plugins](https://drupalize.me/tutorial/process-plugins)
- [Migrate Process documentation](https://www.drupal.org/node/2129651) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Process Plugins](/tutorial/process-plugins?p=3115)

Next
[Destination Plugins](/tutorial/destination-plugins?p=3115)

Clear History

Ask Drupalize.Me AI

close