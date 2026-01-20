---
title: "Discover Hooks and Their Documentation"
url: "https://drupalize.me/tutorial/discover-hooks-and-their-documentation?p=3240"
guide: "[[drupal-module-developer-guide]]"
order: 40
---

# Discover Hooks and Their Documentation

## Content

To use a hook in a module, you'll need to know how to find the API documentation for the hook. The API documentation for a hook describes the hook's purpose, provides the function signature, and defines each of its parameters.

In this tutorial, we'll:

- Explore methods for listing available hooks.
- Guide you to the documentation for specific hooks.

By the end of this tutorial, you'll be able at find possible hooks for your task, and understand the documentation for a hook.

## Goal

Learn how to identify possible hooks to implement in your custom Drupal module and access their documentation.

## Prerequisites

- [Concept: What Are Hooks?](https://drupalize.me/tutorial/concept-what-are-hooks)

## Video tutorial

Sprout Video

## Discovering available hooks

The hooks you can implement in your Drupal module vary based on the enabled modules, site configuration, current request, and the actions Drupal performs in response. Identifying available hooks and choosing the right one for your needs can sometimes be challenging due to this variability.

In the *anytown* module that we've been working on throughout this guide, we want to add some user-facing **help text** that Drupal can display when the *Help* module is enabled. We need to figure out what hook(s) we need to implement in order to add help text to Drupal.

### Look at the source

*Hook* definitions are primarily found in *MODULE\_NAME.api.php* files within Drupal core and contributed modules. For instance, the Node module's hook definitions are in *core/modules/node/node.api.php*. Use your IDE to search for functions beginning with `hook_`. The names of these functions often hint at the hook's purpose, but you'll find more detailed information in the documentation.

For hooks from contributed modules, search for a *MODULE\_NAME.api.php* file in the module's root directory.

As we learned in [Concept: What Are Hooks?](https://drupalize.me/tutorial/concept-what-are-hooks), hooks are invoked by the `module_handler` service. To observe hooks in action, consider setting a debugger breakpoint or adding a `var_dump()` in methods like `\Drupal\Core\Extension\ModuleHandler::invoke`, `\Drupal\Core\Extension\ModuleHandler::invokeAllWith`, and `\Drupal\Core\Extension\ModuleHandler::alter`.

**Hint:** We know that we want to add text for the *Help* module, so it's probably a good bet that the hook we want to implement is provided by that module.

### Example hook definition

Inside the *MODULE\_NAME.api.php* file, you'll encounter hook definitions complete with PHP comments and code.

Example from *node.api.php*:

```
/**
 * Act on a node being indexed for searching.
 *
 * This hook is invoked during search indexing, after loading, and after the
 * result of rendering is added as $node->rendered to the node object.
 *
 * @param \Drupal\node\NodeInterface $node
 *   The node being indexed.
 *
 * @return string
 *   Additional node information to be indexed.
 *
 * @ingroup entity_crud
 */
function hook_node_update_index(\Drupal\node\NodeInterface $node) {
  // Example implementation.
}
```

This documentation details the hook's name (`hook_node_update_index`), purpose, and parameters.

**Note:** The hook documentation demonstrates the older-style functional hooks, not the new OOP style we use in this guide. But it's still relevant. Use the function signature to determine the method signature, and any example code will work identically in either a function or a method implementation.

### Drupal core hooks

For Drupal core hooks, [api.drupal.org](https://api.drupal.org/api/drupal/) offers comprehensive documentation. Simply search for `hook_` to find a full list of hooks. This is particularly useful when you're ready to implement a hook and need to verify function signatures or parameter details.

**Note:** Ensure you refer to the documentation for the correct version of Drupal, as details may vary.

### Examples for Developers project

The [Examples for Developers project](https://www.drupal.org/project/examples) provides practical hook implementations for example modules with supplemental inline documentation.

### Finding implementations of a specific hook

To see how a hook is used across the system, use the [Devel module's](https://www.drupal.org/project/devel) Drush command `drush fn-hook` (or `drush devel:hook`) to list every implementation of a specified hook in the codebase.

For example, use `drush devel:hook cron` to search for implementations of `hook_cron()` in the current codebase.

## Recap

Discovering hooks and their documentation requires a blend of source code exploration, using resources like *api.drupal.org*, and leveraging tools such as Devel's Drush commands. These strategies enable you to find hooks that will work for your task.

## Further your understanding

- How would you find the documentation for `hook_file_download()` and its applications?
- Which hook allows for the modification of JavaScript files attached to a page?
- If multiple modules implement the same hook how does Drupal determine which one to call first?

## Additional resources

- [Discover Existing Hooks](https://drupalize.me/tutorial/discover-existing-hooks?p=2766) (Drupalize.Me)
- [Hooks](https://api.drupal.org/api/drupal/core%21core.api.php/group/hooks) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: What Are Events?](/tutorial/concept-what-are-events?p=3240)

Next
[Implement hook\_help()](/tutorial/implement-hookhelp?p=3240)

Clear History

Ask Drupalize.Me AI

close