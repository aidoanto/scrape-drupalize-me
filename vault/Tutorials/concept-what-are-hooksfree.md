---
title: "Concept: What Are Hooks?free"
url: "https://drupalize.me/tutorial/concept-what-are-hooks?p=3240"
guide: "[[drupal-module-developer-guide]]"
order: 38
---

# Concept: What Are Hooks?free

## Content

Hooks in Drupal enable modules to alter or extend the behavior of Drupal core or other modules. By annotating class methods with `#[Hook]` attributes, or implementing functions with specific names, modules can intervene at various points in Drupal's execution flow. This tutorial introduces hooks, their implementation, and their significance in module interaction.

In this tutorial, we'll:

- Define what hooks are.
- Explore how hooks are implemented in modules.
- Understand when modules should define and invoke new hooks.

By the end of this tutorial, you'll understand the concept of hooks as a means to alter Drupal's behavior.

## Goal

Learn how hooks enable modules to customize and extend Drupal functionality.

## Prerequisites

- [Concept: What Are Modules?](https://drupalize.me/tutorial/concept-what-are-modules)
- [Concept: Anatomy of a Module](https://drupalize.me/tutorial/concept-anatomy-module)

## Understanding hooks

Hooks are one of the ways that module's can write PHP code that ties into Drupal's runtime and alter, extend, or enhance, existing functionality.

From an implementation perspective, hooks are code that is called at specific times to alter or add to the base behavior. Each hook has a unique name (like `hook_entity_load()`), a defined set of parameters, and a defined return value.

As a module developer you'll implement hooks that fall into 3 categories:

- **Informational hooks**: Gather data from modules, such as permissions or menu items.
- **Alter hooks**: Modify data provided by other modules.
- **Action hooks**: Respond to events within Drupal, like entity creation.

## Implementing hooks

There are two different ways that modules can implement a hook. Using class methods annotated with `#[Hook]` attributes, or by implementing a global function that follows a specific naming convention. In most cases you should use the `#[Hook]` attribute approach.

The `#[Hook]` attribute method was introduced in Drupal 11.1.x and is the recommended way to implement hooks if you're writing code for Drupal core greater than or equal to 11.1.x. They can be written to be backward compatible ([see the change record](https://www.drupal.org/node/3442349)). Function-based hooks have been used by Drupal since the early days and will likely continue to work for a while. In this guide, we'll demonstrate both methods since you're very likely to encounter both in documentation and code examples in the wild for the foreseeable future.

Implement hooks by following these steps:

1. **Find the hook**: Determine which hook you need to implement.
2. **Naming**: Attribute your method, or name your function using the appropriate pattern.
3. **Coding**: Write the PHP logic for your hook.

### Example OOP implementation

Here's an example of implementing `hook_form_alter()` in the *anytown* module using the Object-Oriented Programming (OOP) approach. This code would live in the PHP file, *src/Hook/AllHooks.php*:

```
<?php

declare(strict_types=1);

namespace Drupal\anytown\Hook;

use Drupal\Core\Form\FormStateInterface;
use Drupal\Core\Hook\Attribute\Hook;

class AllHooks {

  /**
   * Implements hook_form_alter().
   */
  #[Hook('form_alter')]
  public function formAlter(&$form, FormStateInterface $form_state, $form_id) : void {
    // Code goes here ...
  }

}
```

In this example, we used the hook's short name, which is the hook name (`hook_form_alter`) with the `hook_` prefix removed, as the value to pass to the `#[Hook]` attribute.

The class name, `AllHooks`, and file name, *AllHooks.php*, can be anything, as long as:

- The class name and file location follow the PSR-4 standard
- The file (code) lives in the `Drupal\{MODULE_NAME}\Hook` namespace

It is common to **group related hook implementations** into one class. For example, you could group all form-related hooks into a class, `FormHooks`, in the file *src/Hook/FormHooks.php*.

### Example functional programming implementation

Here's an example of implementing `hook_form_alter()` in the *anytown* module using the global function (procedural) approach, in use prior to Drupal 11.1.x. This code would live in the *anytown.module* PHP file:

The naming convention for functions is `MODULE_NAME_hookname()`, replacing `MODULE_NAME` with your module's name.

```
/**
 * Implements hook_form_alter(). 
 */
function anytown_form_alter(&$form, \Drupal\Core\Form\FormStateInterface $form_state, $form_id) {
  // Custom logic to alter forms.
}
```

It's best practice to document hook implementations with an "Implements HOOK." comment, replacing `HOOK` with the name of the hook you're implementing. This allows your future self and others reading your code to be able to readily understand that this is a specific Drupal hook implementation.

## Defining and invoking hooks

You can define and invoke hooks in your module to let other modules interact with its functionality. This helps create modular, extensible code that others can easily extend. Defining custom hooks involves:

- Choosing a unique name.
- Documenting the hook's purpose, parameters, and expected return values in a *MODULE\_NAME.api.php* file.
- Invoking the hook at appropriate times in your module's code using the `module_handler` service.

You should define a new hook when:

- Your code performs a critical action like saving a record to the database, or processing a response from a third-party API.
- Any time you're gathering a list of "things" that someone might want to add to.
- Any time you want to let other code alter a list or definition before you use it.

Learn more in [Define and Invoke a New Hook](https://drupalize.me/tutorial/define-and-invoke-new-hook).

## Recap

Hooks are essential for Drupal module development, offering a way to alter core functionality or integrate with other modules. Understanding how to implement and invoke hooks is key to building flexible code that can use and provide integration points with other modules in the system.

## Further your understanding

- What are the steps required to implement a hook?
- What scenarios in your module's custom logic could benefit from invoking hooks?

## Additional resources

- [What Are Hooks?](https://drupalize.me/tutorial/what-are-hooks) (Drupalize.Me)
- [Hooks](https://api.drupal.org/api/drupal/core%21core.api.php/group/hooks/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Concept: What Are Events?](/tutorial/concept-what-are-events?p=3240)

Clear History

Ask Drupalize.Me AI

close