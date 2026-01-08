---
title: "Default Configuration in a Module"
url: "https://drupalize.me/tutorial/default-configuration-module?p=2476"
guide: "[[work-data-modules]]"
---

# Default Configuration in a Module

## Content

When you create a module for Drupal, it can be useful to provide default configuration. This can be settings for a form, the placement of a block, or something more complex like the default image styles provided by the Image module in core. A module can provide default configuration for simple configuration or configuration entities.

In this tutorial, we will cover:

- Possible locations for default configuration
- What happens with configuration when a module is installed or uninstalled
- Managing dependencies in configuration
- Where to find examples of default configuration

## Goal

Provide default configuration in a module in either *config/install* or *config/optional* and understand the implications of each location.

## Prerequisites

- [Overview: Configuration Management in Drupal](https://drupalize.me/tutorial/overview-configuration-management-drupal)

## Watch: Default Configuration in a Module

Sprout Video

## Default configuration locations

For Drupal modules, there are two places that you can put default configuration:

- *config/install*
- *config/optional*

## Providing default configuration in *config/install*

Configuration placed in *config/install* is only read at install time. This is a good place to put configuration that should be active when a module is first installed.

## Providing default configuration in *config/optional*

If your module's configuration has dependencies on other modules which may not be installed when your module is installed, this configuration should be placed in *config/optional*. This directory is scanned by Drupal every time a module is enabled and any configuration object that can be created will be, if its dependencies are met.

For example, Node module doesn't require Views to function; however, Node module provides (among others) a "frontpage" view which depends on the Views module, because it provides the schemas for views configuration entities. Once Views is installed, all modules' *config/optional* directories are searched for views configuration entities. It's at this time that Node module's *config/optional/views.view.frontpage.yml* configuration (as well as the others) will be found and created.

The *config/optional* directory may be a better and potentially more reliable place to put configuration with dependencies on modules that are not otherwise needed by the module, because only configuration that can be installed will be installed. In addition, when a module is enabled, *config/optional* directories are scanned for new configuration entities dependent on the newly enabled module that can now be activated.

## Configuration installation is recursive

Starting with Drupal 8.6, [configuration installation is recursive](https://www.drupal.org/node/2997504). This is best illustrated with an example:

- Module "1" provides configuration object "A", with a dependency on module "2".
- Module "1" provides configuration object "B", which depends on configuration object "A".

Prior to Drupal 8.6, when installing module "2", only object "A" would be installed.

Starting with Drupal 8.6, when installing module "2", both object "A" and "B" will be installed.

## Considerations

Which directory you should place default configuration for your module depends on several factors that you will want to consider to ensure a smooth and predictable installation and uninstallation process for the user. As module developer, ask yourself:

- Does my module's configuration depend on a module that is not otherwise required in order for my module to function? If the answer is yes, place your configuration in *config/optional*.
- For each configuration object that my module provides, how critical is it to the core functionality of my module? Is it *must-have* configuration, like an essential taxonomy vocabulary or field widget? Place it in *config/install* and possibly use the `enforced` key (see below for details). Or, is it *nice-to-have* default configuration, possibly providing an example that integrates or depends on another module (i.e. a view or image style)? Place it in *config/optional* instead.

## Handling configuration dependencies

In your configuration's YAML file, you can declare dependencies on modules, other configuration entities, or other kinds of extensions (like a theme). Use the `dependencies` key and nested inside of that, use the `module`, `config`, or `theme` keys.

For example, see lines 3-15 of the configuration for the Article node type in *core/profiles/standard/config/install/core.entity\_view\_display.node.article.default.yml*:

```
dependencies:
  config:
    - field.field.node.article.body
    - field.field.node.article.comment
    - field.field.node.article.field_image
    - field.field.node.article.field_tags
    - image.style.large
    - node.type.article
  module:
    - comment
    - image
    - text
    - user
```

## Enforcing a dependency that is not auto-calculated

In Drupal, you can declare enforced dependencies in YAML files describing configuration entities. These dependencies are in addition to those auto-calculated. This prevents modules from being uninstalled while their configuration objects remain.

If you need to declare a module dependency that might otherwise be missed by Drupal's auto-calculation of dependencies, add a level of nesting and use the `enforced` key inside an array of `dependencies`.

For example, in the Forum module, the configuration for the taxonomy vocabulary, `forums` has a dependency on its own module, Forum, in order to prevent the Forum module from being uninstalled while data or configuration objects dependent on the `forums` vocabulary still remain in the system.

See also the change record, [Config dependencies can optionally be enforced](https://www.drupal.org/node/2404447).

Example: *core/modules/forum/config/install/taxonomy.vocabulary.forums.yml*

```
langcode: en
status: true
dependencies:
  enforced:
    module:
      - forum
name: Forums
vid: forums
description: 'Forum navigation vocabulary'
hierarchy: 1
weight: -10
```

## Possible structures of `dependencies` array

The `dependencies` key can list `module`, `config`, or `theme` dependencies. You can also use the `enforced` key to ensure that a module is not uninstalled before configuration entities that depend on it are deleted.

### Declaring dependencies on modules or other configuration

List dependencies grouped by type by their ID or machine name:

```
dependencies:
  module:
    - module_id
  config:
    - config_id
  theme:
    - theme_id
```

Examples:

- *core/modules/forum/config/install/core.entity\_form\_display.comment.comment\_forum.default.yml*
- *core/profiles/standard/config/optional/responsive\_image.styles.narrow.yml*
- *core/profiles/standard/config/install/block.block.bartik\_account\_menu.yml*

### Enforcing dependencies

This is usually done within the module that provides the configuration.

```
dependencies:
  enforced:
    module:
      - module_id
```

Examples:

- *core/modules/forum/config/install/taxonomy.vocabulary.forums.yml*
- *core/modules/forum/config/install/node.type.forum.yml*
- *core/modules/book/config/install/core.entity\_view\_mode.node.print.yml*

### Declaring both enforced and "regular" dependencies

```
dependencies:
  module:
    - module_id
  enforced:
    - module:
      - module_id
```

Example:

- *core/profiles/standard/config/optional/image.style.max\_2600x2600.yml*

## Use `hook_update` to alter the structure of your configuration

If you want to update the default configuration for your module, you will need to update the YAML files in either *config/install* or *config/optional* for new users of your module as well as implement `hook_update_N` for existing users.

To learn more about updating default configuration in a module, see:

- [Updating Configuration in Drupal 8](https://www.drupal.org/node/2535454) (Drupal.org)

## Find more examples of default configuration

There are many examples of default configuration in Drupal's core modules. Browse for yourself in *core/modules* and when a module has a *config* directory, see if it also has an *install* directory inside of it. That's where the module's default configuration is stored, which will be created when the module is installed.

### Example: default image styles

The core Image module provides three image styles "out-of-the-box." In *core/modules/image/config/install* you'll find several configuration YAML files: simple configuration key-value pairs in *image.settings.yml* and configuration entities that describe 3 image styles in *image.style.large.yml*, *image.style.medium.yml*, and *image.style.thumbnail.yml*.

The file, *image.style.large.yml*, describes the *Large (480x480)* image style listed at *Configuration > Media > Image styles* (*admin/config/media/image-styles*).

*core/modules/image/config/install/image.style.large.yml*:

```
langcode: en
status: true
dependencies: {  }
name: large
label: 'Large (480×480)'
effects:
  ddd73aa7-4bd6-4c85-b600-bdf2b1628d1d:
    uuid: ddd73aa7-4bd6-4c85-b600-bdf2b1628d1d
    id: image_scale
    weight: 0
    data:
      width: 480
      height: 480
      upscale: false
```

This file contains an array ([including nested arrays denoted by indentation](https://drupalize.me/videos/introduction-yaml)) of keys and values that describe the properties of the default "Large" image style. The keys are determined by the image style (`image.style.*`) configuration provided by the Image module in *core/modules/image/config/schema/image.schema.yml*.

## Exercise: provide a new node type with your module

### Create a YAML file with the new node type configuration

Create a file called *node.type.example\_node\_type.yml* and save it to *DRUPALROOT/modules/MODULENAME/config/install*.

### Add default configuration to the YAML file

```
langcode: en
status: true
dependencies: {  }
name: 'Example Node Type'
type: example_node_type
description: 'A new Node Type.'
help: ''
new_revision: false
preview_mode: 1
display_submitted: false
```

The key/value pairs defined in this file are the properties of the configuration entity, and their values.

**Note:** The filename matters here. The naming convention is `node.type.{ID}.yml`, where `{ID}` is the value returned by `$entity->id()`. In most cases this will be a key in the YAML file with the name `id:`. However, in the case of node types the canonical ID of the entity is the value of the `type` property, e.g., `type: example_node_type`. The final filename in this case needs to be *node.type.example\_node\_type.yml*.

### Install the module

Navigate to *node/add*, and you will see your new "Example Node Type" listed.

Experiment with adding different types of default configuration to a custom module through YAML files.

## Recap

In this tutorial, you learned where default configuration can be stored (in either *config/install* or *config/optional*) and how to structure a YAML file that describes default configuration. We also talked about how dependencies work when it comes to configuration as well as how and when Drupal will load default configuration into active configuration when those dependencies are met.

## Further your understanding

- Provide default configuration in a module and save it to your module's *config/install* directory. If your module is already enabled, what would you need to do to get Drupal to recognize and load the default configuration you just added?
- In the tutorial, [Load and Save Configuration Entity Data](https://drupalize.me/tutorial/use-configuration-entities-modules-settings-form), one of the steps is to provide default configuration. Walk through that tutorial to get practice and see the concept in action.

## Additional resources

- [Introduction to YAML](https://drupalize.me/videos/introduction-yaml) (Drupalize.Me)
- Change record: [Optional configuration provided by modules and themes is now stored in config/optional](https://www.drupal.org/node/2453919) (Drupal.org)
- Change record: [Config dependencies can optionally be enforced](https://www.drupal.org/node/2404447) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Configuration Data Types](/tutorial/configuration-data-types?p=2476)

Next
[Provide Initial Settings with Simple Configuration](/tutorial/provide-initial-settings-simple-configuration?p=2476)

Clear History

Ask Drupalize.Me AI

close