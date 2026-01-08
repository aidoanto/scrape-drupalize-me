---
title: "Set a Dynamic Title for a Route"
url: "https://drupalize.me/tutorial/set-dynamic-title-route?p=3134"
guide: "[[develop-custom-pages]]"
---

# Set a Dynamic Title for a Route

## Content

When defining a route and subsequently displaying the page, often we need to calculate the page title based on route parameters or other logic. In these cases, we can't just hard code the value into the `_title` configuration of the route. To set a dynamic title for a page, we'll use the route's `_title_callback` option, and point to a PHP callback that contains the logic that computes the title of the page.

In this tutorial we'll:

- Learn how to use the `_title_callback` route configuration option to dynamically set a page title
- Explain how arguments are provided to the title callback method
- Update the route and controller from a previous tutorial to use a dynamic title callback

By the end of this tutorial, you should be able to configure a route so that its title can be set dynamically using route parameters, instead of hard-coding the title with a static string of text.

## Goal

Update the route definition for a page so that the title is set dynamically and makes use of route parameter values.

## Prerequisites

- [Use Parameters in a Route](https://drupalize.me/tutorial/use-parameters-route)
- [Create a Route and Controller](https://drupalize.me/tutorial/create-route-and-controller)

## Overview

In [Use Parameters in a Route](https://drupalize.me/tutorial/use-parameters-route) we created a route that uses parameters from the URL to determine which node to display and which view mode to use. The title for the route, the primary heading (`<h1>`), and `<title>` elements of the page, contain a hard-coded value. It would be nice if we could make these elements contain the node's title instead.

To calculate the value you want use as the page title based on route parameters, we need to define the `_title_callback` configuration option for the route, which will point to a PHP callable (usually a method on the primary route controller) which will compute and return the value to use for the route title. This dynamic value will in turn be used as the value for the page's `<h1>` and `<title>` elements.

### Edit the route definition to include `_title_callback`

First, add a `defaults._title_callback` configuration option to your route, and remove the no longer necessary `defaults._title` option. The `_title_callback` should point to a PHP method or function that will compute the title. In most cases the best thing to do is add a method to the same class that `_controller` points to perform this calculation.

The following code adds a `_title_callback` to the example route we created in [Use Parameters in a Route](https://drupalize.me/tutorial/use-parameters-route) and removes the `defaults._title` line.

Example from *journey.routing.yml*:

```
journey.node_viewer:
  path: '/journey/{node}/{view_mode}'
  defaults:
    _controller: '\Drupal\journey\Controller\NodeViewer::view'
    # Use a PHP callback to calculate the title for the route.
    _title_callback: '\Drupal\journey\Controller\NodeViewer::titleCallback'
    view_mode: 'full'
  requirements:
    _entity_access: 'node.view'
    node: '\d+'
    view_mode: '\w+'
```

### Define the callback method

Next, edit the file that contains the controller class and add the method your route now points to. In our case that's `\Drupal\journey\Controller\NodeViewer::titleCallback`.

Example *src/Controller/NodeViewer.php*:

```
<?php
/**
 * @file
 * Render a node using the provided view mode.
 */

namespace Drupal\journey\Controller;

use Drupal\Core\Controller\ControllerBase;
use Drupal\node\NodeInterface;

class NodeViewer extends ControllerBase {

  /**
   * Display a node using the provided view mode.
   *
   * @param \Drupal\node\NodeInterface $node
   *   Node object from the route.
   * @param string $view_mode
   *   View mode from the route.
   *
   * @return array
   *   Render array with content for the page.
   */
  public function view(NodeInterface $node, string $view_mode) {
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

  /**
   * Callback for setting the route title.
   *
   * @param \Drupal\node\NodeInterface $node
   *   Node object from the route.
   * @param string $view_mode
   *   View mode from the route.
   *
   * @return string
   *   Title to use for the route.
   */
  public function titleCallback(NodeInterface $node, string $view_mode) {
    return $this->t('Viewing %node using view mode %view_mode', ['%node' => $node->label(), '%view_mode' => $view_mode]);
  }
}
```

The `_title_callback` method, `public function titleCallback(NodeInterface $node, string $view_mode)` in this case gets its arguments in the same way the primary `_controller` callback method does. Through a combination of route parameters and type hinting. It doesn't need to match the arguments for the `view()` method, and all arguments are optional. Learn more about how arguments are passed to the controller in [Overview: Parameters and Value Upcasting in Routes](https://drupalize.me/tutorial/overview-parameters-and-value-upcasting-routes).

Once you've made your changes [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) and then view a URL for your route (e.g. `/journey/42/teaser`) and the main `<h1>` for the page and the `<title>` element should both now contain the dynamically calculated route title.

## Recap

In this tutorial, we created a route and controller that will allow us to dynamically set the value of the page title based on parameters passed to the route. This is accomplished using the `_title_callback` route configuration option. The value for `_title_callback`, as its name suggests, points to a PHP callback method, usually on the same controller as the primary view method. This callback takes arguments in the same way as does the primary callback method for the controller.

## Further your understanding

- Can you explain why and when you would use a `_title_callback` instead of a `_title` when configuring a route?
- How does the value returned from `_title_callback` affect the title of a menu item that points to the route?
- What other route configuration options accept a callback method? (Tip: they all work the same way.)

## Additional resources

- [Overview: Parameters and Value Upcasting in Routes](https://drupalize.me/tutorial/overview-parameters-and-value-upcasting-routes) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Use Parameters in a Route](/tutorial/use-parameters-route?p=3134)

Next
[Define Permissions for a Module](/tutorial/define-permissions-module?p=3134)

Clear History

Ask Drupalize.Me AI

close