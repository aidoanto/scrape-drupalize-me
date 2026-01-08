---
title: "What Are Plugins?free"
url: "https://drupalize.me/tutorial/what-are-plugins?p=2765"
guide: "[[alter-drupal-modules]]"
---

# What Are Plugins?free

## Content

The Drupal plugin system allows a particular module or subsystem to provide functionality in an extensible, object-oriented way. The controlling module defines the basic framework (interface) for the functionality, and other modules can create plugins (implementing the interface) with particular behaviors. Plugins are grouped into plugin types. Each plugin type is managed by a plugin manager service, which uses a plugin discovery method to discover provided plugins of that type and instantiate them using a plugin factory.

The system aims to make it easy for developers to allow for management of these components via the user interface, giving more flexibility and control to site administrators.

In this tutorial we'll take a high-level look at the problem the Plugin API is solving and provide a starting point for diving deeper into the various components that make up the Plugin API.

## Goal

Understand at a high-level what Drupal's Plugin system is all about and be ready to dive into the particulars.

## Watch: What Are Plugins?

Sprout Video

## What are plugins?

Plugins are a general reusable solution to a recurring problem within a given context. The plugin system isn't a finished chunk of code that can just be transferred directly into your own code; rather, it's a description or template for solving a specific problem that can be used in many different situations. Plugins also include some generalized utility code that demonstrates a pattern. This is meant to assist the developer who can use this utility code as a starting point instead of having to rewrite the boilerplate pieces each time. In software engineering we call this a [design pattern](https://sourcemaking.com/design_patterns). This one just happens to be specific to Drupal.

Plugins are used to solve the problem where you need to allow one or more modules to provide additional "things" that implement the same interface but provide distinctly different functionality. And in most cases, then provide a site administrator with a list of those "things" so they can choose and configure the appropriate functionality for their use case.

Blocks are the classic example. In Drupal every block consists of essentially the same parts: a label, some content, and various settings related to visibility and cacheability. How that label and content is generated is likely very different from one module to the next, though. A custom block with static content vs. one provided by Views, for example.

Each plugin behaves the same way externally (to any code that's using it) but internally may vary wildly from one to the next, as long as it sticks to the requirements about what its external face should look like as set forth by the *plugin type* that's being implemented.

Examples of things in Drupal that employ the plugin pattern:

- Blocks
- Render API elements
- Actions which can be triggered on configurable events
- Image manipulation effects
- Field types, field widgets, and field formatters
- Items in a navigation menu

## The technical explanation

The [Drupal documentation](https://api.drupal.org/api/drupal/core%21core.api.php/group/plugin_api/) describes plugins as follows:

> The basic idea of plugins is to allow a particular module or subsystem of Drupal to provide functionality in an extensible, object-oriented way. The controlling module or subsystem defines the basic framework (interface) for the functionality, and other modules can create plugins (implementing the interface) with particular behaviors. The controlling module instantiates existing plugins as needed, and calls methods to invoke their functionality.

> Plugins are grouped into [plugin types](https://drupalize.me/tutorial/drupal-plugin-types), each generally defined by an interface. Each plugin type is managed by a [plugin manager service](https://drupalize.me/tutorial/plugin-managers), which uses a [plugin discovery method](https://drupalize.me/tutorial/plugin-discovery) to discover provided plugins of that type and instantiate them using a [plugin factory](https://drupalize.me/tutorial/plugin-factories-and-mappers).

## When should I employ the plugin pattern?

Anytime you want to provide new functionality for a system that already makes use of the plugin system you'll need to implement a new plugin instance of the given type. For example, if you wanted to add a new block, render element, field type, or image effect.

[Learn how to implement plugins of any type](https://drupalize.me/tutorial/implement-plugin-any-type).

If your module needs to provide users with the ability to choose between one or more units of functionality, and that choice is considered configuration, you'll want to implement the Plugin API and provide a new plugin type, as well as corresponding plugins that provide the units of functionality, and method for determining which of all the available plugins to use.

### Example: Voting API module

The [Voting API module](https://www.drupal.org/project/votingapi) provides a generic way to store, retrieve, and tabulate votes. The module itself provides 3 different ways that votes can be tallied. However, this is logic that is likely to be customized. Rather than be forced to include use case-specific logic and giant switch statements to try and determine which ones to use, the module maintainers choose to make the tallying functionality support plugins. Now, they can provide a few basic common examples, and you are free to write a new module with a tallying plugin specific to your application, without having to bother the module maintainers.

Learn how to create a new plugin manager, and [define your own plugin type](https://drupalize.me/tutorial/define-new-plugin-type).

## The Plugin API

The plugin system consists of 4 major components.

### Plugin Types

Plugins that perform similar functionality are of the same plugin type. All blocks, for example, are plugins of the block plugin type. When creating a plugin, information about which interface to implement, the mechanisms used for discovery and instantiation, and how the plugin is used by the application are provided by the plugin type. [Read more about plugin types](https://drupalize.me/tutorial/drupal-plugin-types).

### Plugin Discovery

The process of locating the definition of, and metadata for, all plugins of a given type. When creating a new plugin type you'll need to define the discovery mechanism. When implementing a plugin you'll need to know which discovery mechanism it's using so you know how to ensure your plugin can be discovered. [Learn more about plugin discovery](https://drupalize.me/tutorial/plugin-discovery).

### Plugin Factory

Responsible for instantiating a specific plugin(s) and returning a usable instance to the code making use of the provided functionality. You'll need to know about plugin factories when defining a new plugin type. When implementing a plugin, it's helpful--but not essential--to understand how a plugin factory works. [Learn more about plugin instantiation](https://drupalize.me/tutorial/plugin-factories-and-mappers).

### Plugins

Individual units of functionality that adhere to a specific plugin type definition. For example, each block available on your site is representative of an individual block plugin. If you want to add new functionality to an existing tool you probably want to implement a new plugin. [Learn more about implementing plugins of any type](https://drupalize.me/tutorial/implement-plugin-any-type).

There are several things a module developer may need to do with plugins:

- [Define a completely new plugin type](https://drupalize.me/tutorial/define-new-plugin-type)
- [Create a plugin of an existing plugin type](https://drupalize.me/tutorial/implement-plugin-any-type)
- [Use a plugin manager service](https://drupalize.me/tutorial/plugin-managers) to perform tasks that involve plugins, like instantiating an instance of a specific plugin.

## Recap

In this tutorial, we learned that plugins are a general reusable solution to a recurring problem within a given context, blocks being a common example. Drupal provides an API for defining and creating plugins that comprises 4 components: Plugin Types, Plugin Discovery, Plugin Factory, and Plugins. As a developer, you may need to define a new plugin type, create a plugin using an existing plugin type, or use a plugin manager service.

## Further your understanding

- Many different parts of Drupal core use plugins to allow module developers to add new functionality. Can you name a few of them?
- Describe an example in which you're developing a new module and it makes sense for you to define a new plugin type.
- [Learn about events](https://drupalize.me/tutorial/what-are-events), another method of extending Drupal.

## Additional resources

- [DrupalCon Los Angeles 2015: An Overview of the Drupal 8 Plugin System - by Joe Shindelar](https://www.youtube.com/watch?v=gd6s4wC_bP4)
- [DrupalCon Barcelona 2015: Altering, Extending, and Enhancing Drupal 8 - by Joe Shindelar](https://www.youtube.com/watch?v=EglfVllpYd4)
- [Plugins documentation](https://www.drupal.org/developing/api/8/plugins) (Drupal.org)
- [Plugin API documentation](https://api.drupal.org/api/drupal/core%21core.api.php/group/plugin_api/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Drupal Plugin Types](/tutorial/drupal-plugin-types?p=2765)

Clear History

Ask Drupalize.Me AI

close