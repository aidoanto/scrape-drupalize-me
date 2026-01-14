---
title: "Add a Local Task Link in a Module"
url: "https://drupalize.me/tutorial/add-local-task-link-module?p=2758"
guide: "[[develop-custom-pages]]"
---

# Add a Local Task Link in a Module

## Content

Local task links are the tabs you see when logged in as an administrator viewing a node on a Drupal site. In this tutorial we'll take a look at how local tasks are added within a custom module. We'll also see how to alter local tasks provided by other modules via `hook_menu_local_tasks_alter()`.

## Goal

Understand what local tasks are and how to implement or alter them within a custom Drupal module.

## Prerequisites

- [Routes](https://drupalize.me/topic/routes)
- [Overview: Info Files for Drupal Modules](https://drupalize.me/tutorial/overview-info-files-drupal-modules)
- [Overview: Menu Links in a Module](https://drupalize.me/tutorial/overview-menu-links-module)
- [Implement Any Hook](https://drupalize.me/tutorial/implement-any-hook)

## Code examples

The example code in this tutorial is taken from the [Examples for Developers project](https://www.drupal.org/project/examples), in the [*menu\_example* module](https://git.drupalcode.org/project/examples/-/tree/3.x/modules/menu_example).

## Local task YAML files

Local task links make up the tabs you see when logged in as a site administrator. When viewing a node they may look like this:

Image

![Local task links](../assets/images/local-task-menu-links.png)

Like the other types of links, local tasks are added to a module by providing a YAML file. Typically we're looking for a file in the top level directory like *MODULE\_NAME.links.task.yml*. For example, the Node module provides several local tasks defined in */core/modules/node/node.links.task.yml*.

Here is an example local tasks YAML file. From [Examples for Developers](https://www.drupal.org/project/examples), [menu\_example/menu\_example.links.task.yml](https://git.drupalcode.org/project/examples/-/blob/3.x/modules/menu_example/menu_example.links.task.yml):

```
examples.menu_example.tabs:
  route_name: examples.menu_example.tabs
  title: Default primary tab
  base_route: examples.menu_example.tabs

examples.menu_example.tabs_second:
  route_name: examples.menu_example.tabs_second
  title: Second
  base_route: examples.menu_example.tabs
  weight: 2

examples.menu_example.tabs_third:
  route_name: examples.menu_example.tabs_third
  title: Third
  base_route: examples.menu_example.tabs
  weight: 3

examples.menu_example.tabs_fourth:
  route_name: examples.menu_example.tabs_fourth
  title: Fourth
  base_route: examples.menu_example.tabs
  weight: 4

examples.menu_example.tabs.secondary:
  route_name: examples.menu_example.tabs
  title: Default secondary tab
  parent_id: examples.menu_example.tabs

examples.menu_example.tabs_default_second:
  route_name: examples.menu_example.tabs_default_second
  title: Second
  parent_id: examples.menu_example.tabs

examples.menu_example.tabs_default_third:
  route_name: examples.menu_example.tabs_default_third
  title: Third
  parent_id: examples.menu_example.tabs
```

The keys in this file define the machine name of the local task. Often this is the same as the machine name for the route that the local task will link to. Each local task will often have three or four values:

- `title`: This is the text rendered in the tab for a local task.
- `route_name`: This is the route, or URL path that will be linked.
- `base_route`: The base\_route is used for tab grouping. This should be the same as the route\_name for the default route (`examples.menu_example.tabs` in the example above).
- `weight`: This provides the order for tabs within a particular group.
- `parent_id` is used to create multi level of tabs. To relate a tab to its parent use same name as `parent_id` as shown above in `examples.menu_example.tabs.secondary`.

## Define static local tasks (tabs)

Static local tasks will work for most use-cases.

### Create a *MODULENAME.links.task.yml* file

In our example, the module name is *menu\_example* and the local tasks YAML file is named *menu\_example.links.task.yml*, placed in the module's root directory.

### Choose a base route for the default page

This is the route for the default page and will be used to group the tabs on a particular page. In the example above, this is `examples.menu_example.tabs`.

### Define the default local task in *MODULENAME.links.task.yml*

Start out by defining the default local task.

```
examples.menu_example.tabs:
  route_name: examples.menu_example.tabs
  title: Default primary tab
  base_route: examples.menu_example.tabs
```

### Define additional local tasks ("tabs")

After defining the default local task, add any additional ones. Ensure that each local task definition includes the same `base_route` (copy it from the `base_route` value of your first, default local task). Also, include a weight for each item in addition to a `title` and `route_name`.

For example:

```
examples.menu_example.tabs_second:
  route_name: examples.menu_example.tabs_second
  title: Second
  base_route: examples.menu_example.tabs
  weight: 2

examples.menu_example.tabs_third:
  route_name: examples.menu_example.tabs_third
  title: Third
  base_route: examples.menu_example.tabs
  weight: 3

examples.menu_example.tabs_fourth:
  route_name: examples.menu_example.tabs_fourth
  title: Fourth
  base_route: examples.menu_example.tabs
  weight: 4
```

### Clear Drupal's cache

Since we've made a change to the menu registry, we'll need to [clear Drupal's cache](https://drupalize.me/tutorial/clear-drupals-cache). Use the Drush command `drush cache-rebuild` or Navigate to Configuration > Performance (*admin/config/development/performance*) and click the button **Clear all caches**.

### Login and navigate to the page and verify the local tasks

Login as administrator and navigate to the page and verify that all of your tabs are displaying as expected.

## Completed example

Your local tasks YAML file should look something like this (but with your particular definitions and names).

```
examples.menu_example.tabs:
  route_name: examples.menu_example.tabs
  title: Default primary tab
  base_route: examples.menu_example.tabs

examples.menu_example.tabs_second:
  route_name: examples.menu_example.tabs_second
  title: Second
  base_route: examples.menu_example.tabs
  weight: 2

examples.menu_example.tabs_third:
  route_name: examples.menu_example.tabs_third
  title: Third
  base_route: examples.menu_example.tabs
  weight: 3

examples.menu_example.tabs_fourth:
  route_name: examples.menu_example.tabs_fourth
  title: Fourth
  base_route: examples.menu_example.tabs
  weight: 4
```

## Altering local tasks

Drupal provides a mechanism for altering the local tasks of another module via [hook\_menu\_local\_tasks\_alter](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Menu%21menu.api.php/function/hook_menu_local_tasks_alter).

The parameters passed to this hook include an associative array with the tabs specified by other modules, as well as the route name of the current page. We can use this hook to either add tabs or alter existing tabs. In this example we're adding a tab called 'Add content' to all pages which links to the 'node/add' page.

```
function hook_menu_local_tasks_alter(&$data, $route_name) {

  // Add a tab linking to node/add to all pages.
  $data['tabs'][0]['node.add_page'] = array(
    '#theme' => 'menu_local_task',
    '#link' => array(
      'title' => t('Add content'),
      'url' => Url::fromRoute('node.add_page'),
      'localized_options' => array(
        'attributes' => array(
          'class' => array('example-tab'),
        ),
      ),
    ),
  );
}
```

The associative array `$data` in this function should look relatively familiar once you become accustomed to the syntax of the YAML files *MODULENAME.links.task.yml*. The only major difference is the additional specification of a `#theme` function used to render the tab link.

## Recap

Local task links present themselves as tabs on particular URLs and are often used to group similar operations or tasks with a particular entity. The Node module, for example, uses local tasks to make viewing, editing, revisions and translations accessible to site administrators in fewer clicks. New local tasks can be added by including a *MODULENAME.links.task.yml* file along with our custom module. They can also be altered by implementing the `hook_menu_local_tasks_alter` function.

## Further your understanding

- Look at the local tasks defined by the Block module. Based on reading the code, can you visualize how the local tasks will present themselves on the block administration pages?
- It is also possible to define dynamic local tasks by defining a deriver class in PHP. See the documentation at [Providing module-defined local tasks](https://www.drupal.org/docs/drupal-apis/menu-api/providing-module-defined-local-tasks) to learn more.

## Additional resources

- [Menu system documentation](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Menu%21menu.api.php/group/menu) (Drupal.org)
- [hook\_menu\_local\_tasks\_alter documentation](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Menu%21menu.api.php/function/hook_menu_local_tasks_alter) (Drupal.org)
- [Providing module-defined local tasks](https://www.drupal.org/docs/drupal-apis/menu-api/providing-module-defined-local-tasks) (Drupal.org)
- [Browse the code for Examples for Developers menu\_example](https://git.drupalcode.org/project/examples/-/tree/3.x/modules/menu_example) (git.drupalcode.org)
- [Dynamic Local Task generation](https://www.drupal.org/docs/drupal-apis/menu-api/providing-module-defined-local-tasks#dynamic-local-task-generation) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add a Contextual Link in a Module](/tutorial/add-contextual-link-module?p=2758)

Next
[Create Dynamic Menu Links](/tutorial/create-dynamic-menu-links?p=2758)

Clear History

Ask Drupalize.Me AI

close