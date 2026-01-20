---
title: "Provide Initial Settings with Simple Configuration"
url: "https://drupalize.me/tutorial/provide-initial-settings-simple-configuration?p=2476"
guide: "[[work-data-modules]]"
order: 23
---

# Provide Initial Settings with Simple Configuration

## Content

As we learned in [Configuration Data Types](https://drupalize.me/tutorial/configuration-data-types), simple configuration is suitable for storing module settings as boolean values, integers, or text strings in one or more key/value pairs. In this tutorial, we'll walk through creating a schema and providing default configuration to store initial settings that a module needs to function.

## Goal

Provide some simple configuration in a settings YAML file.

## Prerequisites

- [Introduction to YAML](https://drupalize.me/videos/introduction-yaml)
- [Overview: Info Files for Drupal Modules](https://drupalize.me/tutorial/overview-info-files-drupal-modules)
- [Inspect Configuration with Drush](https://drupalize.me/tutorial/inspect-configuration-drush)

## Use simple configuration for initial settings

Simple configuration is a type of configuration data in Drupal useful for storing key/value pairs. Default simple configuration can be stored in *MODULENAME.settings.yml* or *MODULENAME.CONFIG.PREFIX.yml* files.

To provide initial settings that our module needs to function, we will provide a schema to describe the structure of our configuration and then use simple configuration to store our default values.

While a module can provide as many configuration files as needed, in this tutorial, we'll focus on creating a settings YAML file to store initial default values for a module.

In these instructions, we'll use a module name of `demo`. **Substitute your module name for `demo`**.

### Create the schema directory

Create *config/schema* inside your module's root directory.

### Create the schema YAML file

Inside *demo/config/schema* create *demo.schema.yml*.

If your module already has a schema file, you can add to it; don't create a separate file for each kind of configuration your module provides. You can store schemas for all types of configuration including configuration stored in settings YAML files, other simple configuration objects, and configuration entities.

This is what we should have so far:

```
modules
-- demo
---- config
---- schema
------ demo.schema.yml
```

### Describe the structure using YAML

Now we need to describe the structure for our configuration, using the format and properties described in [Configuration schema/metadata](https://www.drupal.org/docs/drupal-apis/configuration-api/configuration-schemametadata).

```
demo.settings:
  type: config_object
  label: 'Demo module settings.'
  mapping:
    demo_label:
      type: string // Can be any valid data type, such as boolean, string, float, email, uri
      label: 'A demo label'
  demo_checkbox:
    type: boolean
    label: 'A demo checkbox'
```

- `demo.settings`: We use this key because we're storing our configuration in *demo.settings.yml*.
- `type`: The first key inside *demo.settings* is `type`, which will be `config_object` since we're using the simple configuration data subtype (and not a `config_entity`).
- `label`: Provide a label for the configuration object as a whole, for example "Demo module settings".
- `mapping`: The mapping array contains one or more arrays of configuration keys describing the structure of the keys inside your configuration object. At minimum, each property should have a data type and usually also a label. Visualize a settings form. The property name will be the name of the field.

### Create the settings configuration YAML file

Now that we've defined our schema, we can create our settings configuration file containing default values.

To ensure that these settings are applied when a user installs the module, we'll place this file in our module's *config/install* directory. The file name should match the settings array key in our schema with a *.yml* extension. The file's keys should contain the elements defined in the schema's `mapping` array with values of the schema-defined data type.

For example, the configuration file corresponding to `demo.settings` inside *modules/custom/demo/config/schema/demo.schema.yml* would be:

*modules/custom/demo/config/install/demo.settings.yml*:

```
demo_label: "A Demo Label"
demo_checkbox: 1
```

### Install or re-install the module

Now that we have placed configuration in our module's *config/install* directory, if we have already enabled the module, we will need to uninstall and re-enable the module. We can do this with Drush:

```
drush pmu demo && drush en demo --y
```

If you haven't enabled the module yet, do so now:

```
drush pm:enable demo
```

Alternatively, in a Drupal site, navigate to Extend from the administrative menu, uncheck the module and submit to uninstall it, and then check it again (and submit) to enable it again.

### Test by retrieving the configuration with Drush

We can test that Drupal recognizes our new configuration by retrieving it with Drush. Open a command-line utility, navigate to your Drupal site and enter:

```
drush cget demo.settings
```

(Note: `drush cget` is shorthand alias for both the Drush 8 command `drush config-get` and the Drush 9 command `drush config:get`.)

The output (at this point) should be identical to the contents of your default settings in *modules/custom/demo/config/install/demo.settings.yml*:

```
demo_label: "A Demo Label"
demo_checkbox: 1
```

## Recap

In this tutorial, we learned how to recognize simple configuration in Drupal and how to create the appropriate files to store and describe simple configuration in a module.

## Further your understanding

- Look through *core/modules* inside module's *config/schema* and *config/install* directories. Can you recognize simple configuration in use?

## Additional resources

- [Configuration API](https://api.drupal.org/api/drupal/core%21core.api.php/group/config_api) (Drupal.org)
- [Create a Settings Form in a Module](https://drupalize.me/tutorial/create-settings-form-module) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Default Configuration in a Module](/tutorial/default-configuration-module?p=2476)

Next
[Create a Settings Form in a Module](/tutorial/create-settings-form-module?p=2476)

Clear History

Ask Drupalize.Me AI

close