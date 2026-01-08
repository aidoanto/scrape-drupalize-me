---
title: "Concept: Update Hooks"
url: "https://drupalize.me/tutorial/concept-update-hooks?p=3246"
guide: "[[drupal-module-developer-guide]]"
---

# Concept: Update Hooks

## Content

Update hooks in Drupal are used for executing database updates or applying configuration changes during module updates. They ensure these changes occur once and in the correct order.

In this tutorial, we'll:

- Explore the purpose of update hooks.
- Learn how to implement update hooks for database updates or configuration changes.

By the end of this tutorial, you should be able to understand the use case for update hooks and know how to get started implementing one.

## Goal

Understand how and when to use update hooks in Drupal module development.

## Prerequisites

- [Implement hook\_help()](https://drupalize.me/tutorial/implement-hookhelp)
- [13.6. Updating a Module](https://drupalize.me/tutorial/user-guide/security-update-module)

## Why and when to use update hooks

When a Drupal module requires database schema modifications or configuration updates due to changes in the module's code, you'll implement update hooks. Update hooks are executed automatically by Drupal, and ensure all essential data migrations or configuration adjustments are correctly applied, in order, and without repeating.

Different types of update hooks serve distinct purposes. Some update hooks run at a reduced bootstrap level:

- `hook_update_N()`: The most common. For low-level changes like adding/altering database tables and configurations before other modules update. Place in a *MODULE\_NAME.install* file. Runs before configuration import.
- `hook_post_update_NAME()`: Use when a fully bootstrapped Drupal system is needed. Use to inject content or make changes relying on services. Runs before configuration import. Must be in a *MODULE\_NAME.post\_update.php* file.
- `hook_deploy_NAME()`: A hook provided by Drush. For changes needing a fully-loaded system/configuration. Runs **after configuration import** through the Drush command `drush deploy:hook`. Note that this hook is not part of Drupal core, but is commonly used.

## Common use cases for update hooks

- **Schema changes**: Adding, changing, or removing database columns or tables.
- **Data migration**: Migrating or transforming data for a new schema.
- **Configuration updates**: Updating or adding new configuration settings.

## Implementing an update hook

Place update hooks that implement `hook_update_N()` in a module's *MODULE\_NAME.install* file. Follow the naming pattern: `hook_update_N()`, where `hook` is the module's machine name, and `N` is a sequential number indicating the order of execution.

Here's an example of an update hook that updates a configuration setting:

```
/**
  * Implements hook_update_N().
  */
function mymodule_update_9101(&$sandbox) {
  \Drupal::configFactory()->getEditable('mymodule.settings')
    ->set('new_setting', 'new_value')
    ->save();
}
```

## Best practices for update hooks

- Increment the `N` part of the hook name to ensure proper execution order. Numbers are often suffixed with the major Drupal version, for example `8xxx` or `10xxx`.
- Do one action per update hook. Write multiple hooks for multiple unrelated changes.
- Always verify the current state before acting. For example, check the existence of a field before adding it.
- Document each update hook thoroughly.
- Test update hooks in a development environment and make a backup before deploying to a production environment.
- Use `$sandbox` for batch processing lengthy updates.

See the [documentation for details on numbering your hook\_update\_N implementations](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Extension!module.api.php/function/hook_update_N).

## Recap

Update hooks are a way to apply schema, database, or configuration changes to the system during module updates. Using update hooks are a way to ensure the module and a site where a module is installed remain functional after a module has been updated.

## Further your understanding

- How can you ensure an update hook runs only once?
- What steps would you take to revert changes if needed?

## Additional resources

- [Update API Guide](https://www.drupal.org/docs/drupal-apis/update-api) (Drupal.org)
- [Update API](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Extension%21module.api.php/group/update_api) (api.drupal.org)
- [Drupal 9: Different Update Hooks And When To Use Them](https://www.hashbangcode.com/article/drupal-9-different-update-hooks-and-when-use-them) (hashbangcode.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Lint Your Code with PHP\_CodeSniffer](/tutorial/lint-your-code-phpcodesniffer?p=3246)

Clear History

Ask Drupalize.Me AI

close