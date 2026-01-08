---
title: "Implement Any Hook"
url: "https://drupalize.me/tutorial/implement-any-hook?p=2751"
guide: "[[alter-drupal-modules]]"
---

# Implement Any Hook

## Content

Hooks allow module developers to execute custom code at key moments during Drupal's request processing life cycle. They can be used to react to actions or conditions, alter forms and existing configuration, and extend Drupal in various ways. Knowing how to implement a hook is an essential skill for any Drupal developer. All hooks are implemented in the same way, so once you know how to implement one, you'll be able to implement any.

In this tutorial we'll:

- Define a recipe for implementing hooks
- Locate a hook's documentation
- Provide examples of both function-based and class-based hook implementations

By the end of this tutorial, you should be able to start implementing any hook in your custom code.

## Goal

Locate the documentation for a known hook and then implement it in your custom Drupal module.

## Prerequisites

- [What Are Hooks?](https://drupalize.me/tutorial/what-are-hooks)

Sprout Video

## How to implement a hook

### Procedural hooks

- Locate the documentation for the hook.
- Copy the function definition into your module's *.module* file.
- Rename the function.
- Add your custom code.

[Learn how to implement a hook as a function](#implement-a-hook-as-a-function)

### OOP hooks, Drupal 11.1+

**Note:** This technique was introduced in **Drupal 11.1** and should be used for any code that is targeting this version or later.

- Locate the documentation for the hook.
- Create a class (or add to an existing one) in *src/Hook/\*\*.php*.
- Copy the function definition into your class as a method.
- Rename the method, and add a `#[Hook]` attribute.
- Add your custom code.

[Learn how to implement a hook as a class](#implement-a-hook-as-a-class)

## Locate the documentation

Regardless of the approach you take to implementing the hook, start by locating the documentation.

Hooks are documented by the module or subsystem that invokes them within *\*.api.php* files. Once you [know the name of the hook you want to implement](https://drupalize.me/tutorial/discover-existing-hooks) you can locate its documentation either directly in the *\*.api.php* file where it's defined, or by searching on <https://api.drupal.org>.

Using an IDE with a robust function navigation/lookup tool is a great way to do this. You can generally jump right to the function definition, read the support documentation `@docblock` and copy/paste the function signature from there.

**Tip:** All of the `hook_` functions in *\*.api.php* files are for documentation purposes only. The code they contain is never loaded or executed by Drupal. Additionally, the example code in the function bodies is almost always both functional and useful, making them a great source for learning.

## Implement a hook as a function

Example:

```
/**
 * Implements hook_form_alter().
 */
function mymodule_form_alter(&$form, \Drupal\Core\Form\FormStateInterface $form_state, $form_id) {
  // Custom code and comments go here ...
}
```

### Copy the function

Once you've located the function in the *\*.api.php* file or on <https://api.drupal.org>, copy and paste the function into your module's *MODULENAME.module* file. Procedural hook implementations need to live in a module's *MODULENAME.module* file so that the code is loaded and available when needed. (See [notes](#notes) for exceptions to this rule.)

Example:

```
modules
|--contrib
|--custom
|----mymodule
|------mymodule.info.yml
|------mymodule.module *
```

### Rename the function

Replace the word `hook` in the name of the function you just pasted with the machine name of your module. That is, the name of your module's *MODULENAME.info.yml* file without the extension.

Some hooks have additional tokens in their name that need replacing for them to work. These are designated by all caps in the hook's name. For example, `hook_form_FORM_ID_alter()` or `hook_ENTITY_TYPE_load()`. These hooks are generally available to provide a more targeted version of a generic counterpart which is called frequently. You should replace the all-caps token with an appropriate value.

When a form is built, both `hook_form_alter()` and `hook_form_FORM_ID_alter()` are invoked. The generic version is called for every single form, while the targeted version is only invoked for the specific form indicated by replacing the `FORM_ID` with the actual ID of the form.

For example, let's rename `hook_form_FORM_ID_alter()` in the module, `mymodule`, and the form ID, `user_login_alter`:

`mymodule_form_user_login_alter()`

### Add your custom code

Replace the code in the new function's body with your own custom code that implements whatever it is you need your module to do.

### Document your hook

The convention is to replace the `@docblock` comment for a function that is an implementation of a hook with the standard `Implements hook_*()`. Then provide in-line comments for your custom code.

## Remember the `use` statements

Many hook implementations contain [type hinting](https://drupalize.me/videos/php-type-hinting?p=2099) in the function definition. When referring to a class in a *MODULENAME.module* file you'll need to remember to either add a `use` statement, or use the full name of the class.

Example with `use` statement:

```
use \Drupal\Core\Form\FormStateInterface;

function mymodule_form_alter(&$form, FormStateInterface $form_state, $form_id) {}
```

Example with full class name:

```
function mymodule_form_alter(&$form, \Drupal\Core\Form\FormStateInterface $form_state, $form_id) {}
```

## Implement a hook as a class

Example (*src/Hook/MyModuleFormHooks.php*):

```
<?php
declare(strict_types=1);

namespace Drupal\mymodule\Hook;

use Drupal\Core\Form\FormStateInterface;
use Drupal\Core\Hook\Attribute\Hook;

class MyModuleFormHooks {

  /**
   * Implements hook_form_alter().
   */
  #[Hook('form_alter')]
  public function formAlter(&$form, FormStateInterface $form_state, $form_id) : void {
    // Custom code and comments go here ...
  }

}
```

### Create the class file

Classes that implement hooks are located in the *src/Hook/* subdirectory of a module in the `Drupal\{MODULE_NAME}\Hook` namespace using the [PSR-4 standard](https://drupalize.me/tutorial/concept-php-namespaces-and-psr-4). The name of the class itself doesn't matter, and a class can have one or more methods that implement hooks. We recommend one class per hook, or grouping hook implementations for like functionality together. For example, a single class to implement `hook_cron()`, a class with methods that implement both `hook_token_info()` and `hook_tokens()` which function as a pair.

For example:

```
modules
|--contrib
|--custom
|----mymodule
|------mymodule.info.yml
|------src
|--------Hook
|----------MyModuleCronHooks.php
|----------MyModuleFormHooks.php
|----------MyModuleTokenHooks.php
```

### Copy the example function

Once you've located the function in the *\*.api.php* file or on <https://api.drupal.org>, copy and paste the function into your new class as a method. In our experience this is the easiest way to ensure you get the method signature correct. Make sure you add any relevant `use` statements.

You'll need to add `public` to the function signature, and we suggest renaming it to something using `camelCase`.

### Add a `#[Hook]` attribute

Remove the prefix `hook_` from the name of the function you just pasted to get the short name of the hook.

Some hooks have additional tokens in their name that need replacing for them to work. These are designated by all caps in the hook's name. For example, `hook_form_FORM_ID_alter()` or `hook_ENTITY_TYPE_load()`. These hooks are generally available to provide a more targeted version of a generic counterpart which is called frequently. You should replace the all-caps token with an appropriate value (indicated in the API documentation).

When a form is built, both `hook_form_alter()` and `hook_form_FORM_ID_alter()` are invoked. The generic version is called for every single form, while the targeted version is only invoked for the specific form indicated by replacing the `FORM_ID` with the actual ID of the form. Example: `hook_form_user_login_alter()`.

This short name is the value you pass to the `#[Hook] attribute. You should end up with something like:

- `hook_cron()` => `cron` => `#[Hook('cron')]`
- `hook_entity_load()` => `entity_load` => `#[Hook('entity_load')]`
- `hook_form_FORM_ID_alter()` => `hook_form_user_login_alter()` => `form_user_login_alter` => `#[Hook('form_user_login_alter')]`

### Add your custom code

Replace the code in the new method's body with your own custom code that implements whatever it is you need your module to do.

### Document your hook

The convention is to replace the `@docblock` comment for a method that is an implementation of a hook with the standard `Implements hook_*()`. Then provide in-line comments for your custom code.

## Examples

Here are a couple of example procedural hook implementations with verbose comments. The name of the module implementing the hooks is `hooks_example`.

Example implementation of `hook_help()`:

```
/**
 * Implements hook_help().
 *
 * When implementing a hook you can use the standard "Implements HOOK_NAME."
 * format as the docblock for the function. This is an indicator that further
 * documentation for the function parameters can be found in the docblock for
 * the hook being implemented and reduces duplication.
 *
 * This function is an implementation of hook_help(). Following the naming
 * convention for hooks, the "hook_" in hook_help() has been replaced with the
 * short name of our module, "hooks_example_" resulting in a final function name
 * of hooks_example_help().
 */
function hooks_example_help($route_name, RouteMatchInterface $route_match) {
  switch ($route_name) {
    // The name of the route, from hooks_example.routing.yml that you want to
    // display the help text on.
    case 'help.page.block':
      return '<p>' . t('This text is provided by the function hooks_example_help(), which is an implementation of the hook hook_help().') . '</p>';
  }
}
```

Example implementation of `hook_ENTITY_TYPE_view()`:

```
/**
 * Implements hook_ENTITY_TYPE_view().
 *
 * Some hook names include additional tokens that need to be replaced when
 * implementing the hook. These hooks are dynamic in that when they are being
 * invoked a portion of their name is replaced with a dynamic value. This is
 * indicated by placing the token words in all caps. This pattern is often used
 * in situations where you want to allow modules to generically act on all
 * instances of a thing, or to act on only a specific subset.
 *
 * There are lots of different entity types in Drupal: Node, user, file, etc.
 * Using hook_entity_view() a module can act on a any entity that is being
 * viewed, regardless of type. If we wanted to count views of all entities,
 * regardless of type this would be a good choice. This variant is also useful
 * if you want to provide administrators with a form where they can choose from
 * a list of entity types which ones they want to count views for. The logic in
 * the generic hook implementation could then take that into account and act on
 * only a select set of entity types.
 *
 * If however, you know you only ever want to act on viewing of a node entity
 * you can instead implement hook_ENTITY_TYPE_view(). Where ENTITY_TYPE is a
 * token that can be replaced with any valid entity type name.
 */
function hooks_example_node_view(array &$build, EntityInterface $entity, EntityViewDisplayInterface $display, $view_mode) {
  // This example hook implementation keeps track of the number of times a user
  // has viewed a specific node during their current session, then displays that
  // information for them when they view a node.
  //
  // In addition, a hook is invoked that allows other modules to react when the
  // page view count is updated.

  // Retrieve the active session from the current request object.
  $session = \Drupal::request()->getSession();
  $current_counts = $session->get('hooks_example.view_counts', array());
  if (!isset($current_counts[$entity->id()])) {
    // If this is the first time they've viewed the page we need to start the
    // counter.
    $current_counts[$entity->id()] = 1;
  }
  else {
    // If they have already viewed this page just increment the existing
    // counter.
    $current_counts[$entity->id()]++;
  }

  // Save the updated values.
  $session->set('hooks_example.view_counts', $current_counts);
}
```

## A note on *.module* files and procedural hooks

Earlier we said that a procedural hook implementation needs to live in a module's *MODULENAME.module* file. That is really only partially true. Hooks need to be defined in a PHP file that is guaranteed to be loaded by Drupal prior to the hook being invoked. If the function doesn't exist in memory at the time the hook is invoked it won't be executed. This makes *.module* files an easy choice since they are included on every request.

However, some hooks related to modules being enabled, disabled, and updated live in an *MODULENAME.install* file, since they are only ever needed during these rare events. This is indicated in the documentation for these hooks.

Some hooks like `hook\_form\_alter()`, `hook\_js\_alter()`, and `hook\_css\_alter()` can be implemented by a theme. These are defined in the theme's [*THEMENAME.theme* file](https://drupalize.me/tutorial/add-logic-themenametheme).

Additionally, it's not uncommon to see *.inc* (include) files which are then included via the *MODULENAME.module* file. This allows a module implementing lots of hooks to organize them into smaller, more manageable files. Going forward, you can organize hooks into class-based hooks to keep things organized.

## Recap

Implementing a hook involves defining a new function or a class in your module and following a specific naming convention. Hook names, and thereby function names as well as parameters can be figured out by reading the API documentation available for the specific hook. Once you've defined a new function with the appropriate signature, you can implement your custom logic within the body of the function or method, and alter, extend, and enhance Drupal to meet your site's needs.

## Further your understanding

- What is the naming convention used for implementing hooks?
- Only Drupal core hooks are indexed on <https://api.drupal.org>. Where would you find the documentation for hooks provided by a contributed module like [Flag](https://www.drupal.org/project/flag)?
- [Learn about how hooks are invoked](https://drupalize.me/tutorial/define-and-invoke-new-hook).

## Additional resources

- [Drupal core hook documentation](https://api.drupal.org/api/drupal/core%21core.api.php/group/hooks/) has information about implementing hooks and a complete list of hooks provided by Drupal core (api.drupal.org)
- [Drupal.org documentation on hooks](https://www.drupal.org/docs/creating-custom-modules/understanding-hooks) (Drupal.org)
- [This article](http://alanstorm.com/drupal_module_hooks/) examines in depth how Drupal hooks work using some regular PHP concepts. The article was written for Drupal 7 but the content is still relevant for later versions of Drupal. (alanstorm.com)
- If there isn't a hook you can implement to accomplish your needs there might be [a Plugin](https://drupalize.me/tutorial/what-are-plugins) or [an Event](https://drupalize.me/tutorial/what-are-events) that will work

Was this helpful?

Yes

No

Any additional feedback?

Previous
[What Are Hooks?](/tutorial/what-are-hooks?p=2751)

Next
[Discover Existing Hooks](/tutorial/discover-existing-hooks?p=2751)

Clear History

Ask Drupalize.Me AI

close