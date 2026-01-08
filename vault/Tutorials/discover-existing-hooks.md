---
title: "Discover Existing Hooks"
url: "https://drupalize.me/tutorial/discover-existing-hooks?p=2751"
guide: "[[alter-drupal-modules]]"
---

# Discover Existing Hooks

## Content

How do you figure out what hooks are available to implement? How do you know which hook to implement to accomplish a task?

The list of hooks that are available to implement in your custom Drupal module varies depending on the modules enabled for a site. Each module can optionally invoke new hooks. There are also some hooks invoked by Drupal core subsystems like Form API that are always present. This can make it a little bit tricky sometimes to figure out what hooks are available, and which one to implement.

In this tutorial we'll look at:

- Different ways to get a list of available hooks
- Where to find the documentation for a hook so you can know if it's the one you want to implement

By the end of this tutorial you should be able to browse a list of hooks and their related documentation.

## Goal

Find the hook you need to implement in your custom Drupal module.

## Prerequisites

- [What Are Hooks?](https://drupalize.me/tutorial/what-are-hooks)

Sprout Video

## Look at the source

The canonical location for hook definitions is in *\*.api.php* files contained within Drupal core and contributed modules. You can browse through these files, like *core/modules/node/node.api.php* for example. Or use your IDE to search for functions whose name starts with `hook_`. The function names are generally indicative of what the hook does, but it can also help to read the documentation for more detail.

The documentation for a hook, what it does, and what parameters implementation functions receive is in the PHP `@docblock` comment for the `hook_` function in question.

This technique is the best way to find documentation for hooks provided contributed modules. Look for a *MODULENAME.api.php* file in the root directory of the module.

Example hook definition from *node.api.php*:

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
  $connection = Database::getConnection();
  $text = '';
  $ratings = $connection->query('SELECT title, description FROM {my_ratings} WHERE nid = :nid', [':nid' => $node->id()]);
  foreach ($ratings as $rating) {
    $text .= '<h2>' . Html::escape($rating->title) . '</h2>' . Xss::filter($rating->description);
  }
  return $text;
}
```

In this example we can get the name of the hook, which is just the name of the function, `hook_node_update_index()`, in this case. We see an idea of what it's used for by reading the first line of the documentation, and information about the parameters our implementation would have access to. This will usually provide enough information to decide if this is the hook you need to implement.

**Tip:** If you're unsure, [implement the hook in your module](https://drupalize.me/tutorial/implement-any-hook) and set a breakpoint, or just `var_dump()` the parameters to see if they have the information you need.

## Drupal core

Those `@docblock` comments from above are parsed and can be searched on [https://api.drupal.org](https://api.drupal.org/api/drupal). In most cases this should be your first stop when trying to figure out what hook to implement. You can [get a complete list of hooks here](https://api.drupal.org/api/drupal/core%21core.api.php/group/hooks), or type **`hook_`** into the search field.

This is also an extremely useful reference even when you already know what hook you want to implement. We use it frequently to do things like look up the function signature, or remind ourselves what values a specific parameter might contain.

## Find all modules that implement a specific hook

One good way to learn more about what a particular hook can be used to accomplish is to explore existing implementations. You can do so by seeking out the code in existing *.module* files.

The [Devel module](https://www.drupal.org/project/devel) contains a handy [Drush](https://drupalize.me/guide/use-drush-efficiently-manage-your-drupal-site) command that will give you a list of all implementations of a specific hook.

The following example lists all implementations of `hook_help()` in the current code base.

If you need to download and install Devel first:

```
composer require drupal/devel # Downloads Devel and adds it to composer.json
drush en devel # Enables Devel module
```

Now the various [Devel Drush commands](https://drushcommands.com/drush-9x/devel/) are available to you. Run this command and select a hook from the returned list to view it.

```
drush fn-hook help # Alias of drush devel:hook
```

## Recap

There are lots of different ways to learn about the hooks available to implement in Drupal. All of which are wrappers around the canonical documentation that exists in *\*.api.php* files in the code base. These wrappers often times make it easier to quickly find what you're looking for, but if they aren't working, or the hook you want information about isn't part of Drupal core, your best bet is to open up an editor and read the source.

## Further your understanding

- Can you find the documentation for `hook_file_download()`? What would you use it for?
- What hook allows you to alter the list of JavaScript files attached to a page?
- The Devel module contains a `drush fn-hook` command which allows you to view all implementations of a specific hook. Great for seeing examples of a hook in use.
- Did you know that the code which powers [api.drupal.org](https://api.drupal.org/api/drupal) is a Drupal module? You can set up your own copy of [api.drupal.org](https://api.drupal.org/api/drupal) and index not just core but contributed modules you use as well. Check out the [API module](https://www.drupal.org/project/api) to learn more.

## Additional resources

- [Complete list of Drupal core hooks](https://api.drupal.org/api/drupal/core%21core.api.php/group/hooks) (api.drupal.org)
- [API module](https://www.drupal.org/project/api) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Implement Any Hook](/tutorial/implement-any-hook?p=2751)

Next
[Define and Invoke a New Hook](/tutorial/define-and-invoke-new-hook?p=2751)

Clear History

Ask Drupalize.Me AI

close