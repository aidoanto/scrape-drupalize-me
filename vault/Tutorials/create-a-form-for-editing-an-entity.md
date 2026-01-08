---
title: "Create a Form for Editing an Entity"
url: "https://drupalize.me/tutorial/create-form-editing-entity?p=3243"
guide: "[[drupal-module-developer-guide]]"
---

# Create a Form for Editing an Entity

## Content

Adding the new vendor attendance feature starts with adding a custom module, and defining the form controller with a simplified user interface. This is mostly accomplished using concepts that we've already explored, so we'll use this as a chance to practice what we've learned.

In this tutorial, we'll:

- Construct a new module, form controller, and route.
- Discover how to create *local tasks* for an enhanced administrative UI.

By the end of this tutorial you should be able to navigate to the *Attendance* tab of *Vendor* node to access a simplified UI.

## Goal

Create a new module, and a custom form with our new interface.

## Prerequisites

- [Create an Info File for a Module](https://drupalize.me/tutorial/create-info-file-module-mdg)
- [Create a Route for the Weather Page](https://drupalize.me/tutorial/create-route-weather-page)
- [Add a Parameter to a Route](https://drupalize.me/tutorial/add-parameter-route)
- [Concept: Form Controllers and the Form Life Cycle](https://drupalize.me/tutorial/concept-form-controllers-and-form-life-cycle)
- [Use a Service In a Controller](https://drupalize.me/tutorial/use-service-controller)

## Test your existing knowledge

Before diving in, try to complete the following tasks on your own. Then proceed to the detailed instructions below to check your initial work and continue.

- Create a new `anytown_status` module.
- Define `StatusUpdateForm` form controller with a checkbox labeled "Attending", and text fields for "Contact name" and "Contact email".
- Define a route for the form with the path `/node/{node}/status` and pass `{node}` to the form controller.

There are 2 new tasks, which you can try as well:

- Inject the entity type manager service into your form and use it to load the full `$node` object from the ID in the route.
- Add a *local task* link that creates a tab on the node page linked to the new route.

## Video tutorial

Sprout Video

## Create the `StatusUpdateForm` form and related route

### Create a new module

Given its distinct functionality, let's put our code in a separate module called *anytown\_status*.

Create *anytown\_status.info.yml* inside *modules/custom/anytown\_status* if it doesn't already exist.

```
name: 'Anytown Status'
type: module
description: 'UI for easy vendor status updates.'
package: Custom
core_version_requirement: ^10 || ^11
```

### Add a new route

Define a route in *anytown\_status.routing.yml*:

```
anytown_status.status_update:
  # This slug allows for URLs like /node/42/status.
  path: '/node/{node}/status'
  defaults:
    _title: 'Weekly status update'
    _form: 'Drupal\anytown_status\Form\StatusUpdateForm'
  requirements:
    # This isn't a great permission for this task, but we'll fix it later.
    _permission: 'access content'
```

This defines a route that points to the new form controller. We'll update the access control later in [Use Parameter Upcasting for Entities in Routes](https://drupalize.me/tutorial/use-parameter-upcasting-entities-routes).

### Add a local task link

Add a new tab on the node page with *anytown\_status.links.task.yml*:

```
anytown_status.node.attendance_form:
   route_name: anytown_status.status_update
   base_route: entity.node.canonical
   title: Attendance
   weight: 10
```

This is something we haven't seen before. It's the code responsible for adding a *Local task*. Local task links are the tabs you see when logged in as an administrator viewing a node (View, Edit, Delete). We're adding a new one named "Attendance". A local task definition consists of:

- A unique name `anytown_status.node.attendance_form`. It's common to prefix the name with the name of your module.
- A `route_name` that indicates the route this link should point to.
- A `base_route` that indicates the route that this task is local to.
- A `title` that contains the human-readable text of the link.

### Create the form controller

Create the file *anytown\_status/src/Form/StatusUpdateForm.php*:

```
<?php

declare(strict_types=1);

namespace Drupal\anytown_status\Form;

use Drupal\Core\Entity\EntityTypeManagerInterface;
use Drupal\Core\Form\FormBase;
use Drupal\Core\Form\FormStateInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

/**
 * Provides an Anytown Status form.
 */
class StatusUpdateForm extends FormBase {

  /**
   * The entity type manager.
   *
   * @var \Drupal\Core\Entity\EntityTypeManagerInterface
   */
  protected EntityTypeManagerInterface $entityTypeManager;

  /**
   * Constructs a new StatusUpdateForm.
   *
   * @param \Drupal\Core\Entity\EntityTypeManagerInterface $entity_type_manager
   *   The entity type manager.
   */
  public function __construct(EntityTypeManagerInterface $entity_type_manager) {
    $this->entityTypeManager = $entity_type_manager;
  }

  /**
   * {@inheritdoc}
   */
  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('entity_type.manager')
    );
  }

  /**
   * {@inheritdoc}
   */
  public function getFormId(): string {
    return 'anytown_status_status_update';
  }

  /**
   * Form building callback.
   *
   * @param array $form
   *   Form array.
   * @param \Drupal\Core\Form\FormStateInterface $form_state
   *   Form state.
   * @param int|null $node
   *   ID of the node to edit the status for passed in from the route's {node}
   *   slug.
   *
   * @return array
   *   The form array.
   *
   * @throws \Drupal\Component\Plugin\Exception\InvalidPluginDefinitionException
   * @throws \Drupal\Component\Plugin\Exception\PluginNotFoundException
   */
  public function buildForm(array $form, FormStateInterface $form_state, int $node = NULL): array {
    // Load the current node.
    $node = $this->entityTypeManager->getStorage('node')->load($node);

    // Verify that it is a vendor node.
    if ($node->bundle() !== 'vendor') {
      throw new NotFoundHttpException();
    }

    // Save the $node object into the form state, temporary storage, so that we
    // can use it later in the submit handler without having to load it again.
    $form_state->set('node', $node);

    $form['attending'] = [
      '#type' => 'checkbox',
      '#title' => $this->t('Attending'),
      '#description' => $this->t('Check this box if you plan to attend this weekends market.'),
    ];

    $form['contact_name'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Contact name'),
      '#required' => TRUE,
    ];

    $form['contact_email'] = [
      '#type' => 'email',
      '#title' => $this->t('Contact email'),
      '#required' => TRUE,
    ];

    $form['actions'] = [
      '#type' => 'actions',
      'submit' => [
        '#type' => 'submit',
        '#value' => $this->t('Update status'),
      ],
    ];

    return $form;
  }
  
  public function submitForm(array &$form, FormStateInterface $form_state) {
  // Handle submitted form data.
  }

}
```

This code does 2 things we haven't seen before:

- Uses the entity type manager service to load an entity object: `$node = $this->entityTypeManager->getStorage('node')->load($node);`. Entities are always loaded via the entity type manager and not via direct database queries, so that your code can remain agnostic about how the data is stored.
- Checks the entity object's bundle to see if the node being loaded is a vendor or not.

We added an empty required `submitForm()` method so that we can install the module. We'll come back to this in [Update an Entity When the Form Is Submitted](https://drupalize.me/tutorial/update-entity-when-form-submitted).

### Verify it works

Enable the module either via the UI, or with Drush. Then, in your browser navigate to a Vendor page via *Manage* > *Content* (*/admin/content*). There should be a new tab at the top of each page alongside the existing *Edit* tab named *Attendance*. Clicking on that tab should take you to the new form.

Example:

Image

![Screenshot shows form in Attendance tab on a Vendor page](/sites/default/files/styles/max_800w/public/tutorials/images/data--setup-content-types_form-example.png?itok=Qeu2KMVT)

## Recap

In this tutorial, we created a new module named *anytown\_status* that holds the code for our custom vendor attendance tracking feature. We defined a new form with a simplified UI, a route, and local task, which allows a user to navigate to the form via the user interface. Next, we'll populate form fields with existing entity data.

## Further your understanding

- Reflect on trying to create the form on your own. What areas could use more practice?
- How would you set form fields' default values using current field values?

## Additional resources

- [Form API Overview](https://drupalize.me/tutorial/form-api-overview) (Drupalize.Me)
- [Define a New Form Controller and Route](https://drupalize.me/tutorial/define-new-form-controller-and-route) (Drupalize.Me)
- [Form generation](https://api.drupal.org/api/drupal/core%21core.api.php/group/form_api/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add Fields to the Vendor Content Type](/tutorial/add-fields-vendor-content-type?p=3243)

Next
[Read an Entity's Field Values](/tutorial/read-entitys-field-values?p=3243)

Clear History

Ask Drupalize.Me AI

close