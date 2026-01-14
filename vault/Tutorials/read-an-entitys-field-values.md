---
title: "Read an Entity's Field Values"
url: "https://drupalize.me/tutorial/read-entitys-field-values?p=3243"
guide: "[[drupal-module-developer-guide]]"
---

# Read an Entity's Field Values

## Content

Entity objects are loaded using the entity type manager service (technically, the entity storage manager). Field values are read from the entity object. Doing this, instead of directly accessing data in the database, ensures that our custom code can remain agnostic about any underlying data storage logic. Reading field values is a common task, and we'll practice it by loading a vendor entity and using existing field values to pre-populate the new vendor attendance form.

In this tutorial, we'll:

- Load an entity using the entity type manager service.
- Access raw values of entity fields.
- Use `#default_value` in Form API to pre-populate form fields.

By the end of this tutorial, you'll be able to get raw field values from entities.

## Goal

Extract field data from a vendor entity to autofill the *Attendance* form fields, which will help vendors quickly register their attendance.

## Prerequisites

- [Concept: Field API and Fieldable Entities](https://drupalize.me/tutorial/concept-field-api-and-fieldable-entities)
- [Create a Form for Editing an Entity](https://drupalize.me/tutorial/create-form-editing-entity)

## Video tutorial

Sprout Video

## Pre-populating the attendance form

To make the form started in [Create a Form for Editing an Entity](https://drupalize.me/tutorial/create-form-editing-entity) easier to use, we can pre-populate the form fields with whatever data is currently stored in the database. To do this we need to load the vendor node entity, and then read the values of those specific fields.

In Drupal, we **do not read field values directly from the database**. Because it's possible for the database schema to change, we do not want to hard code things like table names and relationships in our module.

## Identifying field machine names

We need to know a field's machine name if we want to get its values. Since field names are set by users when defining the site's data structure, you'll first need to figure out the correct name. We can do this using Drush or through the UI.

### Identify a field with Drush

Get a list of fields using the `drush field:info` command.

Example:

```
drush field:info node vendor

---------------------------- ---------- ------------------- -------------
Field name                   Required   Field type          Cardinality
---------------------------- ---------- ------------------- -------------
body                                    text_with_summary   1
field_main_image             ✔          image               1
field_vendor_attending                  boolean             1
field_vendor_contact_email              email               1
field_vendor_contact_name               string              1
field_vendor_url                        link                1
---------------------------- ---------- ------------------- -------------
```

### Identify a field in the administrative UI

You can find a list of fields by using the *Manage* administration menu to navigate to *Reports* > *Field list* (*admin/reports/fields*).

Example:

Image

![Screenshot of the Field List page in the UI listing fields in the system](../assets/images/data--entity-read_field-list.png)

## Accessing field data

Use the entity type manager service to load entities and access field values.

### Load an entity

```
$entity_type = 'node';
$storage = \Drupal::entityTypeManager()->getStorage($entity_type);

// Load a single entity by its ID.
$node = $storage->load(1);
```

### Access a field instance

```
$field = $node->get('field_vendor_contact_name');
```

### Retrieve a raw field value

```
$contact_name = $node->get('field_vendor_contact_name')->value;
```

### Accessing base fields

Base fields may have separate helper methods for accessing their values.

Example:

```
$title = $node->getTitle();
```

## Set form field default values

Update *src/Form/StatusUpdateForm.php* to pre-populate form fields:

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
  
  public function submitForm(array &$form, FormStateInterface $form_state) {
    // Handle submitted form data.
  }

}
```

In this updated code we:

- Added a `title` element to the Form API array that display the name of the vendor that's currently being edited.
- Added a `#default_value` property to both text fields to pre-populate them with existing data.
- The code from the previous tutorial already loaded the `$node` object, but now we better understand how that works.

## Verify it works

Navigate to a *Vendor* node on your site. Edit the vendor node and enter values for **Vendor Contact Name** and **Vendor Contact Email** if they are empty. Navigate to the *Attendance* tab and verify that the text fields on the form are pre-populated with data from the vendor.

## Recap

In this tutorial, we demonstrated how to load entities and get field values to use in a custom entity editing form in a module. We used the field data to pre-populate a field's default value, creating a better user experience for our vendors.

## Further your understanding

- Why use the entity type manager over direct database queries?
- Explain the different methods for accessing entity fields: `$node->get('field_name')->value` vs. `$node->field_name->value`.

## Additional resources

- [Working with Entity CRUD](https://drupalize.me/tutorial/working-entity-crud) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Create a Form for Editing an Entity](/tutorial/create-form-editing-entity?p=3243)

Next
[Update an Entity When the Form Is Submitted](/tutorial/update-entity-when-form-submitted?p=3243)

Clear History

Ask Drupalize.Me AI

close