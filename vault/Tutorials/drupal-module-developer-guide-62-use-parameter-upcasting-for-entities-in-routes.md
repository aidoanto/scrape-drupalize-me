---
title: "Use Parameter Upcasting for Entities in Routes"
url: "https://drupalize.me/tutorial/use-parameter-upcasting-entities-routes?p=3243"
guide: "[[drupal-module-developer-guide]]"
order: 62
---

# Use Parameter Upcasting for Entities in Routes

## Content

If we use parameter upcasting in our entity route definition, we can simplify code in the `StatusUpdateForm` controller. Parameter upcasting works by instructing Drupal to load entity objects referenced in a route's path automatically. This approach reduces boilerplate code related to the entity type manager service and entity object loading.

In this tutorial, we'll:

- Define parameter upcasting and its advantages.
- Update the `StatusUpdateForm` controller with type hinting to use parameter conversion services.
- Refine our route definition's access checking for entity-specific verification.

By the end of this tutorial you should be able to use parameter upcasting to load full entity objects through an updated route definition.

## Goal

Simplify controller code with route parameter upcasting.

## Prerequisites

- [Create a Form for Editing an Entity](https://drupalize.me/tutorial/create-form-editing-entity)
- [Read an Entity's Field Values](https://drupalize.me/tutorial/read-entitys-field-values)
- [Add a Parameter to a Route](https://drupalize.me/tutorial/add-parameter-route)

## Video tutorial

Sprout Video

## What is parameter upcasting?

Consider the routing path `/node/{node}/status`. A common routing need is to convert the value stored in the `{node}` parameter (an integer acting as the node ID) into another value (the `Node` object that represents the node). Instead of writing code that injects the entity type manager service and then loads the relevant entity object, we can use parameter upcasting instead.

**Parameter upcasting** is the process of converting the raw value stored in a route parameter (like a node ID integer) into a complex data type (like the full `Node` object).

Parameter upcasting is handled by Drupal's parameter converter services. These services match the parameter names and types defined in the route to the type hints of arguments in the controller method. For example, if a route has a `{node}` parameter, and the controller method accepts a `NodeInterface $node` argument, the parameter converter service will load the full node object and pass that instead of just the ID value. Upcasting works for any entity type.

Learn more about parameter upcasting in [Overview: Parameters and Value Upcasting in Routes](https://drupalize.me/tutorial/overview-parameters-and-value-upcasting-routes).

## Update our route to use upcasting

Let's simplify the code in our form controller by updating the `anytown_status.status_update` route to use upcasting. Our controller will get the full node object matching the ID in the requested path.

### Add type hinting to the controller

Modify *src/Form/StatusUpdateForm.php*:

```
<?php

declare(strict_types=1);

namespace Drupal\anytown_status\Form;

use Drupal\Core\Entity\EntityStorageException;
use Drupal\Core\Form\FormBase;
use Drupal\Core\Form\FormStateInterface;
use Drupal\node\NodeInterface;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

/**
 * Provides an Anytown Status form.
 */
class StatusUpdateForm extends FormBase {

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
   * @param \Drupal\node\NodeInterface|null $node
   *   ID of the node to edit the status for.
   *
   * @return array
   *   The form array.
   */
  public function buildForm(array $form, FormStateInterface $form_state, NodeInterface $node = NULL): array {
    // Verify that it is a vendor node.
    if ($node->bundle() !== 'vendor') {
      throw new NotFoundHttpException();
    }

    // Save the $node object into the form state, temporary storage, so that we
    // can use it later in the submit handler without having to load it again.
    $form_state->set('node', $node);

    $form['title'] = [
      '#type' => 'item',
      '#markup' => $this->t('Updating status for vendor: <strong>@vendor</strong>', ['@vendor' => $node->getTitle()]),
    ];

    $form['attending'] = [
      '#type' => 'checkbox',
      '#title' => $this->t('Attending'),
      '#description' => $this->t('Check this box if you plan to attend this weekends market.'),
      // We intentionally leave off the #default_value because we always want
      // to zero this out and require them to check the box (or not) but not
      // assume that we can save the same status from last week.
    ];

    $form['contact_name'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Contact name'),
      '#required' => TRUE,
      '#default_value' => $node->get('field_vendor_contact_name')->value,
    ];

    $form['contact_email'] = [
      '#type' => 'email',
      '#title' => $this->t('Contact email'),
      '#required' => TRUE,
      // Same effect as using $node->get('field_vendor_contact_email') but uses
      // magic property getter.
      '#default_value' => $node->field_vendor_contact_email->value,
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

  /**
   * {@inheritdoc}
   */
  public function submitForm(array &$form, FormStateInterface $form_state): void {
    // Get the node object we saved in the buildForm method.
    /** @var \Drupal\node\NodeInterface $node */
    $node = $form_state->get('node');

    // Read the values from our form fields, and use them to update the fields
    // on the vendor node.
    $node->set('field_vendor_attending', $form_state->getValue('attending'));
    $node->set('field_vendor_contact_name', $form_state->getValue('contact_name'));
    $node->set('field_vendor_contact_email', $form_state->getValue('contact_email'));

    try {
      // Persist the changes to the database.
      $node->save();

      // Set a success message and redirect to the node view page.
      $this->messenger()->addStatus($this->t('Thank you for updating your attendance status.'));
      $form_state->setRedirectUrl($node->toUrl());
    }
    catch (EntityStorageException $exception) {
      // Log the error.
      $this->logger('anytown_status')->error($exception->getMessage());
      // And display a message to the user.
      $this->messenger()->addError($this->t('An error occurred while saving. Please try again.'));
    }
  }

}
```

The most important part of this update is the use of `NodeInterface $node = NULL` instead of `int $node = NULL` in the signature of the `buildForm()` method. This type hint instructs Drupal to invoke the entity storage service and load the appropriate node object, and then pass that to the controller instead of the node ID. This allows us to simplify our custom code because we can remove code from the controller that was used to load the node object.

Learn more about how upcasting works in [Use Parameters in a Route](https://drupalize.me/tutorial/use-parameters-route).

### Update the routing file

Edit *anytown\_status.routing.yml*:

```
anytown_status.status_update:
  path: '/node/{node}/status'
  defaults:
    _title: 'Weekly status update'
    _form: 'Drupal\anytown_status\Form\StatusUpdateForm'
  requirements:
    _entity_access: 'node.update'
  options:
    parameters:
      node:
        type: entity:node
        bundle:
          - vendor
```

With this code in place:

- The `{node}` slug in the path will be converted to a `Node` entity, which opens up options for using the entity to further define the route.
- We can use `_entity_access` requirements to be more specific about access control. The value `node.update` says that only users who have permission to edit the *current* entity should have access to the route.
- The `options` configuration takes this a step further by limiting the route to only *Vendor* nodes.

Learn more about route access checking in [Add Access Checking to a Route](https://drupalize.me/tutorial/add-access-checking-route).

### Verify it works

[Clear the cache](https://drupalize.me/tutorial/clear-drupals-cache), so Drupal gets the new route definition.

In your browser navigate to a Vendor page and select the *Attendance* tab to verify the form at `/node/{node}/status` still works as expected.

## Recap

This tutorial introduced parameter upcasting for simplifying controller code by automatically converting route parameters into entity objects. We updated the `StatusUpdateForm` to use this feature, making our code more efficient.

## Further your understanding

- How can parameter upcasting benefit your module development?
- Locate examples of parameter upcasting in core modules. Are there uses for non-entity values?

## Additional resources

- [Overview: Parameters and Value Upcasting in Routes](https://drupalize.me/tutorial/overview-parameters-and-value-upcasting-routes) (Drupalize.Me)
- [Use Parameters in a Route](https://drupalize.me/tutorial/use-parameters-route) (Drupalize.Me)
- [Parameter upcasting](https://www.drupal.org/docs/8/api/routing-system/parameters-in-routes/parameter-upcasting-in-routes) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Update an Entity When the Form Is Submitted](/tutorial/update-entity-when-form-submitted?p=3243)

Next
[Add Custom Validation to User Entities](/tutorial/add-custom-validation-user-entities?p=3243)

Clear History

Ask Drupalize.Me AI

close