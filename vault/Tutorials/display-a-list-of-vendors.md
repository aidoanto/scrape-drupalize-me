---
title: "Display a List of Vendors"
url: "https://drupalize.me/tutorial/display-list-vendors?p=3243"
guide: "[[drupal-module-developer-guide]]"
---

# Display a List of Vendors

## Content

Drupal allows site administrators to configure *view modes*, defining an entity's display. As module developers, we use *view builders* to transform an entity object into a renderable array, respecting site-specific configurations without hard-coding display details.

In this tutorial, we'll:

- Introduce view builders and explain their significance in entity rendering.
- Develop a route and controller for a new */attending* page
- Use an entity query to retrieve vendor nodes and render them with view builders

By the end of this tutorial, you'll know how to display entities using a site-specific *teaser* view mode.

## Goal

Create a page to display a list of attending vendors, rendered using the *teaser* view mode.

## Prerequisites

- [Concept: Entity Queries](https://drupalize.me/tutorial/concept-entity-queries)
- [Concept: Render API](https://drupalize.me/tutorial/concept-render-api)
- [6.10. Concept: View Modes and Formatters](https://drupalize.me/tutorial/user-guide/structure-view-modes)
- [Create a Route for the Weather Page](https://drupalize.me/tutorial/create-route-weather-page)
- [Create a Controller for the Weather Page](https://drupalize.me/tutorial/create-controller-weather-page)
- [Reset Vendor Status with Cron](https://drupalize.me/tutorial/reset-vendor-status-cron).

## Video tutorial

Sprout Video

## A new page to display attending vendors

We need to create a new page at the path */attending* that will list the vendors who are attending the upcoming market. We can use an entity query to get a list of vendors, then use view builders to display the rendered entities. Here's an example of what this should look like:

Image

![Screenshot of new page displaying vendors attending this week](/sites/default/files/styles/max_800w/public/tutorials/images/data--entity-query_attending.png?itok=xILzlp26)

We will add this feature to the Anytown module.

**Note**: You absolutely can, and in most cases *should*, build this page using Views. For the purposes of this guide, this use case serves as a good practice using entity query and entity view builders.

## Understanding view builders

*View modes* in Drupal (*full*, *teaser*, etc.) define how entities are displayed. Different view modes provide different displays of the same content. Site administrators configure these modes, choosing the fields to display and their formatters. View builders convert entity objects to renderable arrays based on view mode configurations.

When displaying entities in custom code it's best practice to use a view builder, and respect the user-defined view modes.

To render a `$node` object using a specific view mode, you can use the entity type manager to access the entity type specific view builder. Here's an example:

```
$node = \Drupal::entityTypeManager()->getStorage('node')->load($nid);
$view_mode = 'teaser';
$renderable_node = \Drupal::entityTypeManager()->getViewBuilder('node')->view($node, $view_mode);
```

### Create a route for the "attending" page

Add a new route definition to the *anytown/anytown.routing.yml* file for the */attending* page:

```
anytown.attending:
  path: '/attending'
  defaults:
    _title: 'Vendors attending this week'
    _controller: '\Drupal\anytown\Controller\Attending::build'
  requirements:
    _permission: 'access content'
```

### Add a controller for the "Attending" page

Create the file *anytown/src/Controller/Attending.php* with the following code:

```
<?php

declare(strict_types=1);

namespace Drupal\anytown\Controller;

use Drupal\Core\Controller\ControllerBase;

/**
 * Controller for attending page.
 */
class Attending extends ControllerBase {

  /**
   * Callback to display list of vendors attending this week.
   *
   * @return array
   *   List of vendors attending this week.
   */
  public function build(): array {
    // Build a query to get vendor IDs.
    $query = $this->entityTypeManager()->getStorage('node')->getQuery()
      // Only vendors this user has the permission to view.
      ->accessCheck()
      // Only published entities.
      ->condition('type', 'vendor')
      ->condition('field_vendor_attending', TRUE);

    $node_ids = $query->execute();
    if (count($node_ids) > 0) {
      // Load the actual vendor node entities.
      $nodes = $this->entityTypeManager()->getStorage('node')->loadMultiple($node_ids);

      $view_builder = $this->entityTypeManager()->getViewBuilder('node');

      // We're going to display each vendor twice. Once in an unordered list
      // that we'll use for a summary at the top of the page. And then again
      // using the configured 'teaser' view mode below that list. This allows us
      // to demonstrate both rendering individual fields and complete entities.
      $vendor_list = [];
      $vendor_teasers = [];

      foreach ($nodes as $vendor) {
        // For the summary list we want their name, which is the label field.
        $vendor_list[$vendor->id()] = [];
        $vendor_list[$vendor->id()]['name'] = [
          '#markup' => $vendor->label(),
        ];
        // And, the email address from the field_vendor_contact_email field
        // rendered using the configured formatter for the 'default' view mode.
        // But we're also going to explicitly hide the field label regardless of
        // what's configured for the view mode.
        // See \Drupal\Core\Field\FieldItemListInterface::view().
        // Calling view() on the field is a wrapper for using the viewBuilder
        // like so
        // $view_builder->viewField($vendor->field_vendor_contact_email);
        // The most common options here are likely 'label', and 'type' which
        // should be the ID of a field formatter plugin to use. If not type is
        // specified the field types `default_formatter` is used.
        $vendor_list[$vendor->id()]['contact'] = $vendor->get('field_vendor_contact_email')->view(['label' => 'hidden']);

        // Then, we also want to render the entire node, using the 'teaser'
        // view mode. This will return the render array for displaying the node
        // content.
        $vendor_teasers[$vendor->id()] = $view_builder->view($vendor, 'teaser');
      }

      // Alternatively, we could render teasers for all vendors at once using
      // $vendor_teasers = $view_builder->viewMultiple($nodes, 'teaser');.

      $build = [
        'vendor_list' => [
          '#theme' => 'item_list',
          '#items' => $vendor_list,
        ],
        'vendor_teasers' => $vendor_teasers,
      ];
    }
    else {
      $build = [
        '#markup' => $this->t('No vendors are currently attending this week.'),
      ];
    }

    return $build;
  }

}
```

The parts of this code that we haven't seen before include:

- Getting the view builder handler from the entity type manager: `$view_builder = $this->entityTypeManager()->getViewBuilder('node');`
- Using the view builder to retrieve the render array representation of a node: `$vendor_teasers[$vendor->id()] = $view_builder->view($vendor, 'teaser');`
- Calling the `->view()` method of a field instance to get the render array representation of an individual field's data.

### Verify it works

You'll need to [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) before Drupal will find your new page.

Then, navigate to the new */attending* page and verify that it displays a list of vendors who are attending the upcoming market. If no vendors are displayed, edit a vendor entity so the attending checkbox is checked. Try changing the configuration of the *teaser* view mode and verify the changes are reflected on the */attending* page.

## Recap

In this tutorial, we created a new page at */attending* that displays a list of the vendors attending the upcoming market. We used an entity query to get a list of vendor nodes. Then rendered them using view builders in order to respect the site-specific *teaser* configuration.

## Further your understanding

- Can you update the implementation of the */attending* page, so that a site administrator can configure which view mode to use?
- When would you use entity query and view builders instead of creating a view using the Views UI module?

## Additional resources

- [Entities are now rendered by a view builder](https://www.drupal.org/node/1819308) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Reset Vendor Status with Cron](/tutorial/reset-vendor-status-cron?p=3243)

Next
[Concept: Custom Entity Types](/tutorial/concept-custom-entity-types?p=3243)

Clear History

Ask Drupalize.Me AI

close