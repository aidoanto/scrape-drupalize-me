---
title: "Update an Entity When the Form Is Submitted"
url: "https://drupalize.me/tutorial/update-entity-when-form-submitted?p=3243"
guide: "[[drupal-module-developer-guide]]"
---

# Update an Entity When the Form Is Submitted

## Content

Updating entity field values involves loading the entity object, modifying field values, and saving the entity to the database. We'll add a submit handler in our form that uses Entity API methods to update the vendor entity with new attendance data from the form.

In this tutorial, we'll:

- Update and save an entity's field values.
- Implement a submit handler in the attendance form to update the vendor entity with new data.

By the end of this tutorial, you should be able to modify an entity's field values and save the updated entity.

## Goal

Update a vendor entity with field values submitted through the attendance form.

## Prerequisites

- [Create a Form for Editing an Entity](https://drupalize.me/tutorial/create-form-editing-entity)
- [Read an Entity's Field Values](https://drupalize.me/tutorial/read-entitys-field-values)

## Video tutorial

Sprout Video

## Updating entity field values

After loading an entity by its type, use `set()` to modify field values, then `save()` to update the database.

Example:

```
// Load an entity of type 'node' with an ID of 42.
$node = \Drupal::entityTypeManager()->getStorage('node')->load(42);
// Set the value of this field to TRUE. 
$node->set('field_vendor_attending', TRUE);
// Save the new value to the database.
try {
  $node->save();
}
catch (EntityStorageException $exception) {
  // Handle the error.
}
```

## Add a submit handler to the attendance form

Add a submit handler to the form, saving attendance updates to the vendor entity.

Update *src/Form/StatusUpdateForm.php*:

```
<?php 

declare(strict_types=1);

namespace Drupal\anytown_status\Form;

use Drupal\Core\Entity\EntityStorageException;
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

This updated code adds logic to the `submitForm()` method which does the following:

- Reads the `$node` object from the form state. This object was loaded in `formBuild()` and saved to the form state using `$form_state->set('node', $node);`, so that it could be reused in the submit handler. This is a handy way to pass info from the form building process to the submit and validation handlers. It's done completely server-side, so that it's never exposed to the user. This makes it safe from tampering.
- Updates the 3 attendance related fields using the `set()` method and reading the user-submitted field values from `$form_state`.
- Calls `$node->save()` wrapped in a `try/catch` block to allow logging of any errors that arise. If an error occurred here, it would be related to a problem processing the database update.

## Verify it works

Navigate to the *Attendance* tab of a *Vendor* node on your site and verify that the text fields on the form are pre-populated with existing data. Edit the data, and press the *Update status* button. You should be redirected to the *View* tab of the vendor, the attendance field values should be updated, and the message *Thank you for updating your attendance status* should appear on the page.

Example:

Image

![Screenshot showing screen after form update with thank you message.](../assets/images/data--entity-update_saved-vendor.png)

## Recap

In this tutorial, we learned how to update field values for an entity and save the modified entity. We integrated this into the `submitForm()` method of our form controller, so that the changes made by the user are saved to the database when the form is submitted.

## Further your understanding

- What happens if there's an error saving the updated entity?
- How would you manage multi-value fields?

## Additional resources

- [Working with Entity CRUD](https://drupalize.me/tutorial/working-entity-crud) (Drupalize.Me)
- [Handle Submitted Form Data](https://drupalize.me/tutorial/handle-submitted-form-data) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Read an Entity's Field Values](/tutorial/read-entitys-field-values?p=3243)

Next
[Use Parameter Upcasting for Entities in Routes](/tutorial/use-parameter-upcasting-entities-routes?p=3243)

Clear History

Ask Drupalize.Me AI

close