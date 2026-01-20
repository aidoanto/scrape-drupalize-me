---
title: "Define and Invoke a New Hook"
url: "https://drupalize.me/tutorial/define-and-invoke-new-hook?p=2751"
guide: "[[alter-drupal-modules]]"
order: 4
---

# Define and Invoke a New Hook

## Content

As a module developer you should define and invoke new hooks in your module in order to allow other developers -- or even future you -- to extend your module's functionality without hacking your module's code. This requires:

- Creating a new, unique, name for your hook
- Providing documentation for your hook
- Invoking the hook at critical points in your code

By the end of this tutorial you should have a better idea of when to define a new hook and know how to invoke a hook from your code.

## Goal

Our example module keeps track of the number of times a user has viewed the current node. We're going to define and document a new hook that gets triggered each time view count is incremented.

## Prerequisites

- [What Are Hooks?](https://drupalize.me/tutorial/what-are-hooks)
- Not required, but it is helpful to know [how to implement a hook](https://drupalize.me/tutorial/implement-any-hook)

There are three different things you can do when invoking a hook. We introduced these as the three types of hooks in the [What Are Hooks?](https://drupalize.me/tutorial/what-are-hooks) tutorial. They are: provide notice about an action, gather information, and alter gathered information.

Sprout Video

## Quick reference: Invoke a hook

Hooks are **invoked** using the `module_handler` service implemented by `\Drupal\Core\Extension\ModuleHandler`. This can be accessed from the service container via the name `module_handler` or by the `\Drupal::moduleHandler()` shortcut. Hooks can be invoked in several ways (see also the methods on [interface ModuleHandlerInterface](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Extension%21ModuleHandlerInterface.php/interface/ModuleHandlerInterface/)).

- Execute the hook in every module that implements it: `ModuleHandler::invokeAll()`
- Execute the hook per-module, usually by looping over a list of enabled modules: `ModuleHandler::invoke()`
- Call an alter allowing for alteration of existing data structures using `ModuleHandler::alter()`

## Should I define a hook?

As a module developer you want to define and invoke new hooks at key points in your code in order to allow others to modify functionality without having to modify the code of your module.

- You should invoke a hook, or alternatively [dispatch an event](https://drupalize.me/tutorial/what-are-events), any time your code performs a critical action. Saving records to the database, sending or receiving data from an API, or responding to user input are all actions that others might want to react to.
- Any time you're gathering a list of "things". That could be calculating a list of options for a form field, aggregating user permissions, or building an entity types definition. The objective is to ensure that other modules can add that list or definition. One common technique would be to invoke a hook wherever you need to use the list, and then implement the hook itself within the same module to provide a set of default options.
- Any time you want to let other code alter a list or definition before you use it. In the example above, after gathering all the information for the list from hook implementations you should also give others the opportunity to alter the complete set of data to make changes to items in the list added by any module.

## Define a new hook

Defining a new hook consists of:

- Choosing a unique name for your hook
- Documenting your new hook
- Invoking the hook in your module's code

As an example, we've got a module that implements `hook_ENTITY_TYPE_view()` in order to log the number of times a user has viewed a page as a session variable, and then display the total count. Now, we want to add the option for other modules to react when the view count is incremented. So we're going to define, and invoke, a new hook.

### Choose a unique name

Every hook needs a unique name. A hook's name will always start with `hook_`. In order to ensure uniqueness we recommend following this with your module's short name, and finally a word or two that hints at what the hook does.

Let's call our hook, `hook_hooks_example_increment_count()`. That is, `hook_{MODULE_NAME}_increment_count()`.

Hook names must be valid PHP function names, and follow the Drupal coding standard. That means lowercase alphanumeric characters and underscores only.

### Document your hook

Hooks are documented in a *{MODULE\_NAME}.api.php* file within the module that defines them. So in our case we can add a new file *hooks\_example/hooks\_example.api.php*. When documenting a hook you write it as if defining a new function, using the unique hook name as the function name. Then add a `@docblock` comment documenting what the hook does and any parameters. The standard is to have the first line contain a short summary starting with an imperative verb, followed by more detailed documentation in additional paragraphs, then documentation for all parameters. Finally, the function body should contain an example of how someone might use the hook.

Example: *hooks\_example/hooks\_example.api.php*:

```
/**
 * Respond to node view count being incremented.
 *
 * This hooks allows modules to respond whenever the total number of times the
 * current user has viewed a specific node during their current session is
 * increased.
 *
 * @param int $current_count
 *   The number of times that the current user has viewed the node during this
 *   session.
 * @param \Drupal\node\NodeInterface $node
 *   The node being viewed.
 */
function hook_hooks_example_count_incremented($current_count, \Drupal\node\NodeInterface $node) {
  // If this is the first time the user has viewed this node we display a
  // message letting them know.
  if ($current_count === 1) {
    $messenger = \Drupal::messenger();
    $messenger->addStatus(t('This is the first time you have viewed the node %title.', array('%title' => $node->label())));
  }
}
```

### Invoke your hook

Hooks are invoked using the `module_handler` service implemented by `\Drupal\Core\Extension\ModuleHandler`. Hooks can be invoked in a few different ways:

- All at once using `ModuleHandlerInterface::invokeAll()` to call all implementations of the specified hook provided by any enabled module. Hook implementations can optionally return a value, depending on the hook definition. If they do, the `invokeAll()` method aggregates the responses from all hooks in an array and returns the array.
- One at a time using `ModuleHandlerInterface::invoke()` to call only the the specified module's implementation of a hook.
- Using `ModuleHandlerInterface::alter()` to pass alterable variables to `hook_TYPE_alter()` implementations for all enabled modules. This method should be used for instances where the calling module has assembled data and would like to give other modules an opportunity to alter that data before it's used. A common pattern is to use `invokeAll()` to first gather input from other modules, the immediately afterwards call `alter()` to give modules the opportunity to alter the aggregate data.

Hooks can be invoked from anywhere in your Drupal code. The only requirement is access to the `module_handler` service.

The following example code demonstrates invoking a new hook named `hook_hooks_example_count_incremented()` from within an implementation of `hook_ENTITY_TYPE_view()`:

```
/**
 * Implements hook_ENTITY_TYPE_view().
 */
function hooks_example_node_view(array &$build, EntityInterface $entity, EntityViewDisplayInterface $display, $view_mode) {
  // Count the number of times the current node has been viewed this session.
  $session = \Drupal::request()->getSession();
  $current_counts = $session->get('hooks_example.view_counts', array());
  if (!isset($current_counts[$entity->id()])) {
    $current_counts[$entity->id()] = 1;
  }
  else {
    $current_counts[$entity->id()]++;
  }
  $session->set('hooks_example.view_counts', $current_counts);

  // Invoke a hook to alert other modules that the count was updated.
  $module_handler = \Drupal::moduleHandler();

  // In this example we're invoking hook_hooks_example_count_incremented() and
  // passing all implementations the current view count for the node, and the
  // node object itself. Note that you should not include the "hook_" prefix in
  // the argument.
  $module_handler->invokeAll('hooks_example_count_incremented', array($current_counts[$entity->id()], $entity));

  // Display the current number of pages the user has viewed along with the
  // node's content.
  $build['view_count'] = array(
    '#markup' => '<p>' . t('You have viewed this node @total times this session.', array('@total' => $current_counts[$entity->id()])) . '</p>',
    '#cache' => array(
      'max-age' => 0,
    ),
  );
}
```

### Example implementation

An example implementation of the hook invoked in the previous step from a module named *persistentcount* would look like the following:

```
/**
 * Implements hook_hooks_example_count_incremented().
 */
function persistentcount_hooks_example_count_incremented($count, $node) {
  // Save the current count for the node being viewed to the database for later
  // use.
  $connection = \Drupal::database();
  $connection->merge('persistcount_count')
  ->key('entity_id', $node->id())
  ->fields([
      'count' => $count,
  ])
  ->execute();
}
```

## Alter hooks

Alter hooks are a special kind of hook that can be used whenever you want to give other code the chance to modify an existing data structure. When calling an implementation of an alter hook arguments are passed by reference, therefore any changes that the hook implementation makes to the provided variable will be reflected upstream in the calling code.

The most common example of this is `hook_form_alter()`. When forms are created in Drupal they are generated as an associative array by the module that provides the form. Before rendering that array to HTML the Form API invokes `hook_form_alter()` and gives any enabled module a chance to make changes to the form array. They can add new elements, alter existing ones, and provide new validation handlers amongst other things.

Another common use case is when a module needs to build a list of things, but doesn't want to that list to be hard coded. By invoking an alter hook the main module can give any other module the chance to add to the list, or remove things, before it's used. You'll frequently see a pattern that looks like:

1. Create an array of items based on internal business logic.
2. Invoke an alter hook with that array as an argument allowing any module to modify it.
3. Loop through the array and perform whatever business logic is required on each item in the list.

You should use alter hooks in your own code any time you want to allow other developers the opportunity to change a variable before it's used.

Alter hook names are always automatically given the suffix `_alter`. So the complete hook name would be `hook_{NAME}_alter()`. However, you do not need to specify the suffix when invoking the hooks, the `alter()` method of ModuleHandlerInterface will take care of that automatically.

```
// Generate your custom data set.
$valid_animals = ['cats', 'dogs', 'horses'];
// Pass the data set to the alter() method of the module_handler service.
\Drupal::moduleHandler()->alter('mymodule_valid_animals', $valid_animals);

// The argument is passed by reference, so any changes made to $valid_animals by
// any module implementing `hook_mymodule_valid_animals(&$valid_animals)` are
// now available within $valid_animals. For example if another module named
// `bugs` could implement the following code, and the resulting $valid_animals
// array would contain ['cats', 'dogs' 'horses', 'ants', 'spiders'].
function bugs_mymodule_valid_animals_alter(&$valid_animals) {
  $valid_animals[] = 'ants';
  $valid_animals[] = 'spiders';
}
```

[Learn more about invoking alter hooks](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Extension%21ModuleHandler.php/function/ModuleHandler%3A%3Aalter/).

## Recap

Invoking a new hook is a 3-step process that requires:

- Coming up with a new unique name for your hook
- Documenting your new hook in a *{MODULE\_NAME}.api.php* file
- And finally, invoking your new hook using the `module_handler` service

## Further your understanding

- Can you find examples of the `invokeAll()` and `invoke()` methods of the module handler service being used in Drupal core? Why is `invoke()` used instead of the simpler `invokeAll()`?
- Can you find an example of an alter hook being invoked in Drupal core that is not `hook_form_alter()`?
- (New in 9.4.x) Do you have custom module code that has been building a function name and then calling it immediately after with some arguments? Learn how to execute a hook in a particular module and passing in a closure ([anonymous function](https://www.php.net/manual/en/functions.anonymous.php)) with `ModuleHandler::invokeAllWith(string $hook, callable $callback): void`. See this 9.4.x change record for more information and examples for how to update your `getImplementations()` and `ModuleHandler::invoke` code to use the `module_handler` service's `invokeAllWith()`: [All hook invocation delegated to Module Handler service](https://www.drupal.org/node/3000490).

## Additional resources

- [\Drupal\Core\Extension\ModuleHandler documentation](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Extension%21ModuleHandler.php/class/ModuleHandler/) (api.drupal.org)
- Learn about [discovering and using existing services](https://drupalize.me/tutorial/discover-and-use-existing-services) like the `module_handler` service
- Change record: [All hook invocation delegated to Module Handler service](https://www.drupal.org/node/3000490) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Discover Existing Hooks](/tutorial/discover-existing-hooks?p=2751)

Clear History

Ask Drupalize.Me AI

close