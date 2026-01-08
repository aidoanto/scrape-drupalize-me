---
title: "What Are Hooks?free"
url: "https://drupalize.me/tutorial/what-are-hooks?p=2751"
guide: "[[alter-drupal-modules]]"
---

# What Are Hooks?free

## Content

Hooks allow modules to alter and extend the behavior of Drupal core, or another module. They are one of the various ways that code components in Drupal can communicate with one another. Using hooks a module developer can change how core or another module works -- without changing the existing code. As a Drupal developer, understanding how to implement and invoke hooks is essential.

In this tutorial we'll:

- Define what hooks are and the types of hooks that exist
- Understand the use case for hooks

By the end of this tutorial you should be familiar with the concept of hooks and understand when you might want to implement a hook.

## Goal

Understand what hooks are and how they are used in Drupal. Be able to know where to find information about implementing and invoking hooks from your custom code.

## Prerequisites

- [Overview: Info Files for Drupal Modules](https://drupalize.me/tutorial/overview-info-files-drupal-modules)

Sprout Video

## Hooks

From an implementation perspective, hooks are snippets of code called at specific times to alter or add to the base behavior. Each hook has a unique name (e.g., `hook_entity_load()`), a defined set of parameters, and a defined return value.

Every hook has three parts: a **name**, an **implementation**, and a **definition**. The implementation consists of the custom code in your module that you want to execute. Another module or subsystem provides the definition, which specifies the hook's name and which arguments are passed to the implementation, as well as when the implementation will be called.

Any number of modules can implement the same hook. This allows multiple modules to contribute to the final outcome. For example, you might have installed two or three different modules that implement `hook_toolbar()` that add links to the administration toolbar. Each implementation will be called in order based on the module's weight stored in the `core.extension` configuration object (which can be viewed using Drush with `drush config:get core.extension`). If multiple modules have the same weight, they will be called in alphabetical order based on the module's machine name.

## A naming convention

At their most basic, hooks are a naming convention. Define a PHP function whose name follows a known pattern, and Drupal will call that function at critical points during the life cycle of a request. Replace the word `HOOK` in the hook definition with the machine name of your module, and tada 🎉, you've implemented a hook!

This:

```
HOOK_entity_load()
```

Becomes:

```
mymodule_entity_load()
```

### Class-based hooks (new in Drupal 11.1)

As of Drupal 11.1.x you can (and should) implement hooks as class methods using attributes. Here's an example of a class-based hook:

```
<?php

namespace Drupal\mymodule;

use Drupal\Core\Attribute\Hook;
use Drupal\Core\Entity\EntityInterface;

/**
 * Example of a class-based hook using an attribute.
 */
class MyModuleHooks {

  #[Hook('entity_load')]
  public function entityLoad(EntityInterface $entity) {
    // Replace `HOOK_entity_load()` with your own logic here.
    // This method will be invoked just like the older hook_entity_load()
    // but using the new attribute-based approach.
  }

}
```

This new approach co-exists with the traditional way of implementing hooks as functions. Both are valid, and both will continue to work. Here's what we anticipate in the future:

- You should be familiar with both approaches, as you'll see both approaches used in documentation and code.
- We'll teach both in [Implement Any Hook](https://drupalize.me/tutorial/implement-any-hook).
- Support for procedural hooks will be removed, but not until Drupal 12 at the earliest (and we would guess even later).
- Attributes for every hook. Instead of `#[Hook('cron')]` we think there's good chance future implementations will use attribute classes specific to the hook like `#[\Drupal\core\Hooks\Cron]` or something similar.

## What can I do with hooks?

Things you can do with hooks:

- [Discover existing hooks](https://drupalize.me/tutorial/discover-existing-hooks): Get a list of all the hooks that could be implemented and find the one you want.
- [Implement a hook](https://drupalize.me/tutorial/implement-any-hook): Lookup the documentation for any hook and implement it in your module.
- [Define (invoke) a new hook](https://drupalize.me/tutorial/define-and-invoke-new-hook): Define, and invoke, a new hook so that other developers can extend your code without modifying it.

## Types of hooks

Generally you can place hooks into one of three categories:

- Hooks that answer a question
- Hooks that alter existing data
- Hooks that react to an action

### Info hooks

**Hooks that answer questions**, often referred to as "info hooks", are invoked when some component in Drupal is gathering a list of information about a particular topic. For example, a list of all the items that should be displayed in the toolbar, or a list of requirements to verify prior to installation. These hooks primarily return arrays whose structure and values are determined by the hook definition. The user module is a good example of this: see [`user_toolbar()`](https://api.drupal.org/api/drupal/core%21modules%21user%21user.module/function/user_toolbar) which adds links to common user account pages to the Toolbar.

Note: Drupal now has fewer info hooks than Drupal 7. Info hooks used to be the primary way of gathering new lists of functionality. Now, the [plugin system](https://drupalize.me/tutorial/what-are-plugins) generally handles this.

### Alter hooks

**Hooks that alter existing data**, often referred to as "alter hooks", and identifiable by the fact that their names are suffixed with *\_alter*, are invoked in order to allow modules to alter a list of previously gathered information. These are often paired with info hooks. A component may first invoke an info hook to gather a list of information, then immediately invoke an alter hook to allow anyone to alter the list that was just created before it's used. You might, for example, change the order that items are listed in the Toolbar, or even change the name used for an item added by another module. The taxonomy module has an example of this: [`taxonomy_views_data_alter()`](https://api.drupal.org/api/drupal/core%21modules%21taxonomy%21taxonomy.views.inc/function/taxonomy_views_data_alter), which adds taxonomy term fields to the information about nodes provided to the Views module.

Of special note is `hook_form_alter()`, one of the most powerful, and likely most commonly implemented hooks. `hook_form_alter()` allows modules to alter the Form API arrays generated by other modules, thereby modifying, and participating in, every aspect of the form generation, validation, and submission workflow. Taking some time to explore examples of `hook_form_alter()` in use is a great way to get ideas for how your module might affect the way Drupal works.

### Action hooks

**Hooks that react to an action**, similar to [events](https://drupalize.me/tutorial/what-are-events), are invoked when specific actions are taken in code somewhere in the system in order to allow other code to do something based on that action. For example, `hook_user_cancel()` is invoked every time a user account is canceled. Modules that store data about users that need to perform cleanup tasks can implement this hook to be notified about the account that is being canceled and take the necessary actions on their own data. The comment module is a good example of this, see [`comment_user_cancel()`](https://api.drupal.org/api/drupal/core%21modules%21comment%21comment.module/function/comment_user_cancel) which removes comments created by a user when their account is canceled.

## Recap

In this tutorial, we learned that hooks are composed of three parts: a name, an implementation, and a definition. We learned about the naming convention for hooks as well as three kinds of tasks you can perform with a hook: discover existing hooks, implement a hook, and define (invoke) a new hook. Finally, we learned about the types of hooks: hooks that answer a question, alter existing data, or react to an action.

## Further your understanding

- How do hooks relate to [plugins](https://drupalize.me/tutorial/what-are-plugins) and [events](https://drupalize.me/tutorial/what-are-events)?
- Can you find an example of an implementation of a hook in Drupal core? Which one did you find? What do you think this particular implementation is doing?

## Additional resources

- [Hooks API documentation](https://api.drupal.org/api/drupal/core%21core.api.php/group/hooks) (api.drupal.org)
- [Change record: Support for object oriented hook implementations using autowired services](https://www.drupal.org/node/3442349) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Implement Any Hook](/tutorial/implement-any-hook?p=2751)

Clear History

Ask Drupalize.Me AI

close