---
title: "Drupal Plugin Types"
url: "https://drupalize.me/tutorial/drupal-plugin-types?p=2765"
guide: "[[alter-drupal-modules]]"
---

# Drupal Plugin Types

## Content

The term *plugin type* is used as a way to provide a generic name for all plugins managed by the same plugin manager. Example plugin types include *block*, *field widget*, and *image effect*. A plugin type doesn't consist of any code that provides specific functionality. Instead, it provides a way to refer to the system and it describes the central purpose of all plugins of that type.

In this tutorial, we'll cover what the term *plugin type* means and how it is used when talking about Drupal's plugin system. By the end of this tutorial, you'll understand what a plugin type is and be ready to learn how to define a plugin type in a module.

## Goal

Understand what a plugin type is in a Drupal system.

## Prerequisites

- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins)

## What is a plugin type?

Plugins that perform similar functionality are of the same plugin type.

A plugin type consists of code in the form of a [plugin manager](https://drupalize.me/tutorial/plugin-managers), [individual plugin instances](https://drupalize.me/tutorial/implement-plugin-any-type), and a use case for the functionality provided by plugins of the given type.

As an example, the *image effect* plugin type is defined by the class `\Drupal\image\ImageEffectManager`. It serves to solve the use case wherein a single image can be transformed by multiple configurable effects into a new derivative that can be displayed for the end user.

Plugin types are defined by modules and each plugin type belongs to a specific module. However, plugin instances are not module specific; any module can provide plugins of any type.

## Common plugin types

Some of the more commonly implemented plugin types are:

- **Block**: Add a new block that an administrator can place via the block layout UI
- **Field formatter**: Add a new option for display data contained in fields of a specific type(s)
- **Field widget**: Add a new form widget for collecting data for fields of a specific type(s)
- **Menu link**: Define a menu link
- **Menu local task**: Define a local task. For example, edit tabs on content pages
- **Views field**: Add a new field option to Views
- **Views filter**: Add a new filter option to Views

Because the plugin types available for any Drupal instance depend on the installed modules it's impossible to create a complete list of plugin types. However, there are some techniques you can use to get a complete list for any site. Learn about [discovering existing plugin types](https://drupalize.me/tutorial/discover-existing-plugin-types).

## Define a new plugin type

As a Drupal module developer knowing how, and when, to define a new plugin type will help you to write modules that are easier to maintain and extend. Next, learn how to [Define a New Plugin Type](https://drupalize.me/tutorial/define-new-plugin-type).

## Recap

In this tutorial, we defined a plugin type as a generic term used to describe all plugins managed by the same plugin manager, and their central purpose. We also learned that plugin types are generally defined by modules, and looked at some common plugin types that module developers are likely to encounter.

## Further your understanding

- Learn about [discovering existing plugin types](https://drupalize.me/tutorial/discover-existing-plugin-types).

## Additional resources

- [Drupal 8 Plugins Explained](https://drupalize.me/blog/201407/drupal-8-plugins) (Drupalize.Me blog)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[What Are Plugins?](/tutorial/what-are-plugins?p=2765)

Next
[Define a New Plugin Type](/tutorial/define-new-plugin-type?p=2765)

Clear History

Ask Drupalize.Me AI

close