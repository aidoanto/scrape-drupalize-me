---
title: "Use Parameters in a Route"
url: "https://drupalize.me/tutorial/use-parameters-route?p=3134"
guide: "[[develop-custom-pages]]"
order: 5
---

# Use Parameters in a Route

## Content

Let's write some code that will allow us to see route parameters in action. We'll define a new route with a path like */journey/42/full* but where `42` can be any node ID, and `full` can be any view mode. When a user accesses the path we'll pass the dynamic parameters from the URL to the controller. The controller will then load the corresponding node and render it using the provided view mode, and return that to display on the page.

By the end of this tutorial you should be able to:

- Use dynamic slugs in a route to pass parameters to the route controller.
- See how Drupal will upcast a value like the node ID, 42, to a `Node` object automatically.
- Explain what happens when you visit a URL that matches a route but the parameters don't pass validation.

By the end of this tutorial, you should be able to pass dynamic values from the URL to a route's controller.

## Goal

Define a route and controller that allows for a URL like, */journey/42/card*, where `42` is the ID of a node entity, and `card` is the view mode to use to display it.

## Prerequisites

- [Create a Route and Controller](https://drupalize.me/tutorial/create-route-and-controller)
- [Overview: Parameters and Value Upcasting in Routes](https://drupalize.me/tutorial/overview-parameters-and-value-upcasting-routes)

## Watch: Use Parameters in a Route

Sprout Video

## Overview

Let's update the `journey` module that we started in [Create a Route and Controller](https://drupalize.me/tutorial/create-route-and-controller) with a new route that meets the following requirements:

- The path should allow for URLs like */journey/42/card*, but the parts `42`, and `card` are variable. For example, you can replace `42` with any node ID, and it'll work, and you can replace `card` with any valid view mode.
- The controller should load the node specified in the URL, and display it using the view mode specified or the view mode specified as the default.
- The route should require that the current user has access to view the node in question.

### Define a route with parameters in the path

First, edit the *journey.routing.yml* file to add a new route with slugs in the `path` to represent the dynamic parts of the URL.

Example:

```
journey.node_viewer:
  path: '/journey/{node}/{view_mode}'
  defaults:
    _controller: '\Drupal\journey\Controller\NodeViewer::view'
    _title: 'Node Viewer'
    view_mode: 'full'
  requirements:
    _entity_access: 'node.view'
    node: '\d+'
    view_mode: '\w+'
```

In this route definition, the `path` contains 2 *slugs*, `{node}` and `{view_mode}`. These represent wildcards in the path, and whatever value is in those places in the URL will be passed to the controller as arguments. The configuration also validates that whatever is in the place of the `{node}` slug in the URL will be a number, and that the `{view_mode}` slug will be a string containing alphanumeric characters and underscores. If not, the values will be considered invalid and the route will display a 404 page. If there is no value in the place of the `{view_mode}` slug (e.g. `/journey/42`) than the default value of `'full'` will be used.

### Define the `NodeViewer` controller

Create a new controller with a `view` method that will accept the parameters from the URL and make use of them.

Example *src/Controller/NodeViewer.php*:

```
namespace Drupal\journey\Controller;

use Drupal\Core\Controller\ControllerBase;
use Drupal\node\NodeInterface;

class NodeViewer extends ControllerBase {
  public function view(NodeInterface $node, string $view_mode) {
    // Get the render array of $node using the $view_mode view mode.
    $output = $this->entityTypeManager()
      ->getViewBuilder('node')
      ->view($node, $view_mode);

    return [
      'header' => [
        '#type' => 'markup',
        '#markup' => $this->t('<div class="messages messages--status">Displaying node using the @view_mode view mode</div>', ['@view_mode' => $view_mode]),
      ],
      'node' => $output,
    ];
  }
}
```

The `view` method takes 2 arguments `$node` and `$view_mode`. As long as the argument names are the same as the slugs (`{node}`, and `{view_mode}` without the curly braces) the routing system will figure out how to pair the values from the URL with the variables passed to the method. The order doesn't matter.

You might expect that when visiting the URL `/journey/42/teaser` that `$node` would be a string like `'42'`, but because of the `NodeInterface` type hint, the routing system will automatically *upcast* the parameter to a `Node` object. Learn more about upcasting in [Overview: Parameters and Value Upcasting in Routes](https://drupalize.me/tutorial/overview-parameters-and-value-upcasting-routes). The value of `$view_mode` will be whatever string is in that position of the URL because there is no parameter conversion defined.

### Test it out

Make sure you [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) after defining a new route and controller. Then, test it out by visiting different URL patterns like `/journey/42`, `/journey/42/teaser`, `/journey/asdf/teaser`, and `/journey/42/bad!value`.

You should see a page that either displays the node in the given view mode or a "page not found" message in the case of any invalid parameters.

Note that this code doesn't do any kind of validation checking that the `$view_mode` string is actually a valid view mode. Or that Drupal will render the node using the *default* view mode in the case where an invalid one is used.

## Recap

In this tutorial, we created a new route that allowed for dynamic parameters in the path, and then passed those values as arguments to the controller. In the controller method definition, we used type hinting to upcast the `$node` parameter from a node ID to a `Node` object. And then output the node using the specified view mode. We also demonstrated how to add parameter validation, and saw what happens when you view a URL where the path contains an invalid dynamic value.

## Further your understanding

- Can you update this example to validate that `$view_mode` is a valid view mode and not just a valid string?
- Can you update this example to use a path like `/journey/{node}/{other_node}/{view_node}` so that it displays 2 different nodes? Hint: You won't be able to rely on type hinting along for upcasting in this case.
- How would you read a query string parameter from a path like `/journey/{node}?view_mode=teaser` in the `view` method of the controller?

Refer to the prerequisite tutorial, [Overview: Parameters and Value Upcasting in Routes](https://drupalize.me/tutorial/overview-parameters-and-value-upcasting-routes) for information relevant to these challenges.

## Additional resources

- [Parameters in routes](https://www.drupal.org/docs/8/api/routing-system/parameters-in-routes) (Drupal.org)
- [Symfony route parameters documentation](https://symfony.com/doc/current/routing.html#route-parameters) (symfony.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview: Parameters and Value Upcasting in Routes](/tutorial/overview-parameters-and-value-upcasting-routes?p=3134)

Next
[Set a Dynamic Title for a Route](/tutorial/set-dynamic-title-route?p=3134)

Clear History

Ask Drupalize.Me AI

close