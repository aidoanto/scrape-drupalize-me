---
title: "Process Plugins"
url: "https://drupalize.me/tutorial/process-plugins?p=3115"
guide: "[[learn-migrate-drupal]]"
order: 24
---

# Process Plugins

## Content

Process plugins manipulate data during the transform phase of the ETL process while the data is being moved from the source to the destination. Drupal core provides a handful of common process plugins that can be used to perform the majority of data transformation tasks. If you need some functionality beyond what is already provided you can [write your own custom process plugins](https://drupalize.me/tutorial/write-custom-process-plugin).

In this tutorial we'll:

- Examine the role that process plugins fulfill
- Understand the processing pipeline
- List the existing process plugins in Drupal core and what each one does
- Better understand when you might need to write your own process plugin

By the end of this tutorial you should be able to explain what process plugins do, and understand how you'll make use of them in your own migration.

## Goal

Explain how process plugins work and the role they play.

## Prerequisites

- [Migrate System: Terms and Concepts](https://drupalize.me/tutorial/migrate-system-terms-and-concepts)
- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins)

Sprout Video

## What is a process plugin?

Process plugins manipulate data during the transform phase of the ETL process while the data is being moved from the source to the destination. Each row of data provided by a [source plugin](https://drupalize.me/tutorial/source-plugins) will be passed through one or more process plugins which operate on the source data to transform it into the desired format. This result is then passed to a [destination plugin](https://drupalize.me/tutorial/destination-plugins) during the load phase.

When writing a migration path the developer creates a map which tells the API which fields in the source data should be loaded into which fields in the destination object. Process plugins perform the task of moving the data from one field to another, optionally performing additional *processing* along the way. The developer is required to provide information about how to process each row of source data on a property-by-property basis.

## The process pipeline

The [migrate process documentation](https://www.drupal.org/node/2129651) on Drupal.org does a great job of explaining the use case for process plugins and how to chain multiple processors together. This is essential reading for anyone creating a migration.

## Example usage

In this example, *title* is the name of the destination field to which we'll save the processed data. We're processing using the *concat* plugin, and it's configured to combine the value of the *nameFirst* and *nameLast* fields from our source data together with a whitespace character space between them.

```
# We generate the node.title (which we treat as the name) by concatenating
# two source fields together and putting a space between them
title:
  plugin: concat
  source:
    - nameFirst
    - nameLast
  delimiter: " "
```

Each plugin, depending on the operation being performed, has different configuration options.

## Common process plugins

Here's a list of the process plugins provided by core. Each plugin links to the documentation where you can learn about configuration options and usage.

- [get](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21migrate%21process%21Get.php/class/Get/): Copy a value verbatim
- [default\_value](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21migrate%21process%21DefaultValue.php/class/DefaultValue/): Provide a default value to use when no source value is present
- [concat](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21migrate%21process%21Concat.php/class/Concat/): Combine two or more properties with a delimiter
- [callback](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21migrate%21process%21Callback.php/class/Callback/): Execute the specified PHP function and use the returned value.
- [download](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21migrate%21process%21Download.php/class/Download/): Download a remote file into the file system.
- [file\_copy](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21migrate%21process%21FileCopy.php/class/FileCopy/): Move (and optionally rename) a local file from one location to another.
- [urlencode](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21migrate%21process%21UrlEncode.php/class/UrlEncode/): URL-encode a string.
- [explode](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21migrate%21process%21Explode.php/class/Explode/): Create an array by splitting the source value at specified boundaries.
- [extract](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21migrate%21process%21Extract.php/class/Extract/): Extract data from a potentially multi-level array.
- [flatten](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21migrate%21process%21Flatten.php/class/Flatten/): Convert a nested array into a flattened array.
- [format\_date](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21migrate%21process%21FormatDate.php/class/FormatDate/): Convert a date/datetime from one format to another.
- [make\_unique\_entity\_field](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21migrate%21process%21MakeUniqueEntityField.php/class/MakeUniqueEntityField): Ensure the source value is made unique against an entity field.
- [MakeUniqueBase](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21migrate%21process%21MakeUniqueBase.php/class/MakeUniqueBase): Ensure the source value is unique. Abstract base class. See also `make_unique_entity_field`.
- [machine\_name](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21migrate%21process%21MachineName.php/class/MachineName/): Convert a string to a valid machine name.
- [migration\_lookup](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21migrate%21process%21MigrationLookup.php/class/MigrationLookup/): (Formerly called [migration](https://www.drupal.org/node/2861226).) Use another migration to determine the unique ID of another object created during migration. Allows for maintaining object relationships even when their unique IDs might change during the import process.
- [skip\_on\_empty](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21migrate%21process%21SkipOnEmpty.php/class/SkipOnEmpty/): Skip processing of a property or an entire row, if current property is empty. Uses PHP's `empty()` function for evaluation.
- [skip\_row\_if\_not\_set](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21migrate%21process%21SkipRowIfNotSet.php/class/SkipRowIfNotSet/): Skip processing of a property or an entire row, if current property is not set. Uses PHP's `isset()` function for evaluation.
- [static map](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21migrate%21process%21StaticMap.php/class/StaticMap/): Lookup a value based on a map specified in the configuration.
- [sub\_process](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21migrate%21process%21SubProcess.php/class/SubProcess/): (Formerly `iterator`.) Run a process pipeline on each value in an array.

See a [complete list of core process plugins](https://www.drupal.org/docs/8/api/migrate-api/migrate-process-plugins/list-of-core-migrate-process-plugins) in the Drupal.org community documentation.

Don't see what you need here? We've got a [tutorial on writing custom process plugins](https://drupalize.me/tutorial/write-custom-process-plugin).

## The details

Process plugins are managed by the [MigratePluginManager](https://api.drupal.org/api/drupal/core%21modules%21migrate%21src%21Plugin%21MigratePluginManager.php/class/MigratePluginManager/).

Migrate process plugins implement `\Drupal\migrate\Plugin\MigrateProcessInterface` and often extend `\Drupal\migrate\ProcessPluginBase`. They use `\Drupal\migrate\Attribute\MigrateProcess` attributes and must be in the *src/Plugin/migrate/process* directory of the module that defines them.

[View a full list of process plugins provided by Drupal core](https://www.drupal.org/docs/8/api/migrate-api/migrate-process-plugins/list-of-migrate-process-plugins).

Looking at plugins for migrating Drupal 6 files, there are two process plugins responsible for processing file information, at `Drupal/core/modules/file/src/Plugin/migrate/process/d6/`.

The 2 plugins, `CckFile` and `FileUri`, transform the data from the source plugin to create a `CckFile` instance, and process (or transform) Drupal 6 file URLs into URLs compatible with the latest version of Drupal.

## Recap

Process plugins perform the transform phase of the ETL process. They take incoming data from a source plugin, and manipulate it as needed before handing it off to a destination plugin. They also serve the purpose of mapping source values to destination fields. Module developers can write custom process plugins as needed, though Drupal core provides a bunch that will cover most use cases.

## Further your understanding

- What are process plugins used for?
- What process plugin would I use if I wanted to combine the value of two fields in my source data together into a single field for the destination?
- Can you come up with an example of a custom process plugin that you might write for your own migration purposes?

## Additional resources

- [Write a Custom Process Plugin](https://drupalize.me/tutorial/write-custom-process-plugin) (Drupalize.Me)
- [Migrate process](https://www.drupal.org/node/2129651) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Write a Custom Source Plugin](/tutorial/write-custom-source-plugin?p=3115)

Next
[Write a Custom Process Plugin](/tutorial/write-custom-process-plugin?p=3115)

Clear History

Ask Drupalize.Me AI

close