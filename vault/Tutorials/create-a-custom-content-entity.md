---
title: "Create a Custom Content Entity"
url: "https://drupalize.me/tutorial/create-custom-content-entity?p=2607"
guide: "[[work-data-modules]]"
---

# Create a Custom Content Entity

## Content

The Drupal Entity API makes it easy to define new custom content entity types. And in most cases, whenever you want to store custom content in Drupal, you should use the Entity API instead of making CRUD queries directly to the database. This ensures your code is more consistent and allows you to take advantage of all the features of the Entity API, like access control, Views module integration, and automatic JSON:API support. As well as making it easier for others to extend your custom content by ensuring all the proper hooks and lifecycle events get invoked when new content items get created, updated, and deleted.

In this tutorial, we'll:

- Walk through the process of creating a custom content entity

By the end of this tutorial, you'll be able to create your own custom content entity contained in a module.

## Goal

Create a custom content entity.

## Prerequisites

This tutorial applies a number of concepts, which we'll walk through with code examples. If you want to better understand these concepts, refer to the following tutorials:

- [Entity API Implementation Basics](https://drupalize.me/tutorial/entity-api-implementation-basics)
- [Composer Configuration for Drupal](https://drupalize.me/tutorial/composer-configuration-drupal)
- [Overview: Info Files for Drupal Modules](https://drupalize.me/tutorial/overview-info-files-drupal-modules)
- [Define Permissions for a Module](https://drupalize.me/tutorial/define-permissions-module)
- [Overview: Menu Links in a Module](https://drupalize.me/tutorial/overview-menu-links-module)
- [PHP Attributes](https://drupalize.me/tutorial/php-attributes)
- [Form API Overview](https://drupalize.me/tutorial/form-api-overview)

## A note about the code examples in this tutorial

Most of the code examples discussed in this tutorial are part of the [Examples for Developers project](https://www.drupal.org/project/examples). If you have the Examples project included in your demo site, *and* you follow the steps in this tutorial to create a module called *content\_entity\_example*, you will have duplicate module names in your site's system, and you will run into problems installing or testing out the module for learning purposes.

Examples in this tutorial, as well as examples provided in Examples for Developers, are for educational purposes only and should not be run as-is on a production site.

## Create a module for the custom content entity

In this tutorial, we'll create a content entity type called "Contact" with a basic administrative interface for creating, updating, and listing our entities. We'll use the content entity example from the [Examples module](https://www.drupal.org/project/examples), with a few modifications on how routing is handled. The [complete code example is available here](https://git.drupalcode.org/project/examples/-/tree/3.x/modules/content_entity_example). The module that's going to hold our new content entity is going to be called "Content Entity Example Module" (`content_entity_example`).

*Note:* File and directory names are relative to *PROJECT\_ROOT/DRUPAL\_ROOT*.

### Set up the custom module

We need a module to encapsulate the content entity-related files.

Create a new directory, *content\_entity\_example* inside *modules/custom*:

```
modules
├── contrib
├── custom
│   └── content_entity_example
```

### Create an info file

We need an [info file](https://drupalize.me/tutorial/overview-info-files-drupal-modules) for our module to be recognized by Drupal. Create the file */modules/custom/content\_entity\_example/content\_entity\_example.info.yml* with the following text:

```
name: 'Content Entity Example'
type: module
description: 'Demonstrates how to create a content entity.'
core_version_requirement: ^10 || ^111
package: 'Custom'
dependencies:
  - drupal:options
  - drupal:user
```

### Define basic permissions

[Static permissions for a module in Drupal](https://drupalize.me/tutorial/define-permissions-module) are also defined in a YAML file. Add some basic "create", "read", "update", "delete", and "administer" permissions by adding a */modules/custom/content\_entity\_example/content\_entity\_example.permissions.yml* file with the following text:

```
'delete contact entity':
  title: Delete entity content.
'add contact entity':
  title: Add entity content
'view contact entity':
  title: View entity content
'edit contact entity':
  title: Edit entity content
'administer contact entity':
  title: Administer settings
```

### Create a routing file

While we could manually define routes for the content entity's *canonical*, *edit-form*, and *delete-form* routes in our module's routing YAML file, we're going to use a core route provider class instead. (We'll specify that in the [attribute](https://drupalize.me/tutorial/php-attributes) for our content entity.) However, we still need to define routes to the *settings form* and the *add-form* in a module routing YAML file.

In practice, you'll encounter code that mixes route provider classes with manually defined routes. Learn both approaches, but use a route provider whenever possible.

> It's possible to use both a YAML file and a provider class for entity routes at the same time. Avoid duplicating route names between the two: if a duplicate route name is found in both locations, the one in the YAML file takes precedence; regardless, such duplication can be confusing. ([api.drupal.org](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/group/entity_api))

Add the YAML file */modules/custom/content\_entity\_example/content\_entity\_example.routing.yml* with the following text:

```
content_entity_example.contact_settings:
  path: '/admin/structure/content_entity_example_contact_settings'
  defaults:
    _form: '\Drupal\content_entity_example\Form\ContactSettingsForm'
    _title: 'Contact settings'
  requirements:
    _permission: 'administer contact entity'

content_entity_example.contact_add:
  path: '/content_entity_example_contact/add'
  defaults:
    # Calls the form's 'add' controller, defined in the contact entity.
    _entity_form: content_entity_example_contact.add
    _title: 'Add contact'
  requirements:
    # Use the entity's access controller. _entity_create_access tells the router
    # to use the access controller's checkCreateAccess() method instead of
    # checkAccess().
    _entity_create_access: 'content_entity_example_contact'
```

### Define menu links

[Modules can provide various types of menu links](https://drupalize.me/tutorial/overview-menu-links-module). We're going to add [menu links](https://drupalize.me/tutorial/add-menu-link-module), [action links](https://drupalize.me/tutorial/add-action-link-module) and [local task links (tabs)](https://drupalize.me/tutorial/add-local-task-link-module) for our content entity.

Image

![Contact entity link types](/sites/default/files/styles/max_800w/public/tutorials/images/content_entity_example_links.png?itok=muYLlC0j)

A module defines its menu links in a YAML file (*MODULE.links.menu.yml*). The menu link definition includes the menu link's title, the route, a description, and weight.

Create the file */modules/custom/content\_entity\_example/content\_entity\_example.links.menu.yml* with the following YAML-formatted text:

```
# Defines the menu links for this module

entity.content_entity_example_contact.collection:
  title: 'Content Entity Example: Contacts Listing'
  route_name: entity.content_entity_example_contact.collection
  description: 'List Contacts'

content_entity_example_contact.settings:
  title: Contact Settings
  description: 'Configure Contact entity'
  route_name:  content_entity_example.contact_settings
  parent: system.admin_structure
```

### Create local task (tabs)

The tabs, or local tasks, that show up when viewing a contact entity include the "list", "view", "edit", and "delete" operations. Similar to what you see as an administrator at the top of a node. These links are created in the */modules/custom/content\_entity\_example/content\_entity\_example.links.task.yml* file.

Create the file */modules/custom/content\_entity\_example/content\_entity\_example.links.task.yml* with the following contents:

```
# Define the 'local' links for the module

contact.settings:
  title: 'Contact Settings'
  route_name: content_entity_example.contact_settings
  base_route: content_entity_example.contact_settings

entity.contact.view:
  title: 'View'
  route_name: entity.content_entity_example_contact.canonical
  base_route: entity.content_entity_example_contact.canonical

entity.contact.edit_form:
  title: 'Edit'
  route_name: entity.content_entity_example_contact.edit_form
  base_route: entity.content_entity_example_contact.canonical

entity.contact.delete_form:
  title: 'Delete'
  route_name:  entity.content_entity_example_contact.delete_form
  base_route:  entity.content_entity_example_contact.canonical
  weight: 10

entity.contact.collection:
  title: 'Contacts'
  route_name: entity.content_entity_example_contact.collection
  base_route: system.admin_content
  weight: 9
```

### Create action links for the module

Lastly, we can create the action link (to add a new contact) in */modules/custom/content\_entity\_example/content\_entity\_example.links.action.yml*:

```
# All action links for this module

content_entity_example.contact_add:
  # Which route will be called by the link
  route_name: content_entity_example.contact_add
  title: 'Add contact'

  # Where will the link appear, defined by route name.
  appears_on:
    - entity.content_entity_example_contact.collection
    - entity.content_entity_example_contact.canonical
```

With that scaffolding out of the way, we're finally ready to actually create our custom contact entity. (As noted previously, the *.module* file is optional. You would need one if you planned to implement hooks in your module, and you can always create it later.)

```
modules
├── contrib
└── custom
    └── content_entity_example
        ├── content_entity_example.info.yml
        ├── content_entity_example.links.action.yml
        ├── content_entity_example.links.menu.yml
        ├── content_entity_example.links.task.yml
        ├── content_entity_example.permissions.yml
        └── content_entity_example.routing.yml
```

## Create a new entity type

In order for Drupal to recognize our new entity type, we need to register our entity via a `#[ContentEntityType]` *attribute*. We're going to add an attribute to the class that will encapsulate the behavior of our contact entity.

### Create a PHP file for the entity attribute and class

We'll start by creating the file that will hold the PHP class for the custom content entity, adding the `namespace` and `use` statements, the attribute, and a placeholder for the class declaration.

Add the PHP file (and necessary directories) */modules/custom/contact\_entity\_example/src/Entity/Contact.php* with the following contents:

```
<?php

namespace Drupal\content_entity_example\Entity;

use Drupal\Core\Entity\Attribute\ContentEntityType;
use Drupal\Core\Entity\EntityStorageInterface;
use Drupal\Core\Field\BaseFieldDefinition;
use Drupal\Core\Entity\ContentEntityBase;
use Drupal\Core\Entity\EntityTypeInterface;
use Drupal\content_entity_example\ContactInterface;
use Drupal\Core\Entity\EntityChangedTrait;
use Drupal\user\EntityOwnerTrait;
use Drupal\Core\StringTranslation\TranslatableMarkup;

/**
 * Defines the ContentEntityExample entity.
 *
 * @ingroup content_entity_example
 *
 * The following attribute is the actual definition of the entity type which
 * is read and cached. Don't forget to clear caches after changes.
 */
#[ContentEntityType(
  id: 'content_entity_example_contact',
  label: new TranslatableMarkup('Contact entity'),
  handlers: [
    'list_builder' => 'Drupal\content_entity_example\Entity\Controller\ContactListBuilder',
    'views_data' => 'Drupal\views\EntityViewsData',
    'access' => 'Drupal\content_entity_example\ContactAccessControlHandler',
    'form' => [
      'add' => 'Drupal\content_entity_example\Form\ContactForm',
      'edit' => 'Drupal\content_entity_example\Form\ContactForm',
      'delete' => 'Drupal\Core\Entity\ContentEntityDeleteForm',
    ],
    'route_provider' => [
      'html' => 'Drupal\Core\Entity\Routing\AdminHtmlRouteProvider',
    ],
  ],
  list_cache_contexts: ['user'],
  base_table: 'contact',
  admin_permission: 'administer contact entity',
  entity_keys: [
    'id' => 'id',
    'label' => 'name',
    'uuid' => 'uuid',
    'owner' => 'user_id',
  ],
  links: [
    'canonical' => '/content_entity_example_contact/{content_entity_example_contact}',
    'add-form' => '/content_entity_example_contact/add',
    'edit-form' => '/content_entity_example_contact/{content_entity_example_contact}/edit',
    'delete-form' => '/contact/{content_entity_example_contact}/delete',
    'collection' => '/content_entity_example_contact/list',
  ],
  field_ui_base_route: 'content_entity_example.contact_settings',
)]
class Contact extends ContentEntityBase implements ContactInterface {

}
```

#### A closer look at the `#[ContentEntityType]` attribute

Drupal uses the metadata provided by the `ContentEntityType` attribute to define some of the behavior of our contact entities.

Core provides generic handler implementations that do most of the heavy lifting. If you need to customize a handler, you should extend the core-provided class and implement only your use-case-specific logic. Find details about which classes you should extend for each handler in the [API topic documentation for Entity API](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/group/entity_api) (api.drupal.org)

- The `id` and `label` values provide the unique identifier and human-readable name of our entity type.
- `handlers` define the classes used for various operations on our contacts, like building lists or generating an edit form. Notice that we're using a `route_provider` from core. This will provide the basic edit, delete, and canonical pages for entities of this type. We specified `Drupal\Core\Entity\Routing\AdminHtmlRouteProvider`, which extends `\Drupal\Core\Entity\Routing\DefaultHtmlRouteProvider` and provides the entity administrative pages and forms in the site's administrative theme.
- The `base_table` defines the table name used to store data about these entities. This table is automatically created when our module is installed. To make this entity type available in the Views query builder, we've also added the default `views_data` handler.
- The `entity_keys` property tells Drupal how to access fields for our entity. Links provide the paths to perform standard tasks. The full documentation of properties that can be used in an entity type definition can be seen in the class definition of [`\Drupal\Core\Entity\EntityType`](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Entity!EntityType.php/class/EntityType).
- The `views_data` handler defines the class that exposes our content entity to Views. Learn more about exposing your custom entity to Views in [Expose Custom Entities to Views](https://drupalize.me/tutorial/expose-custom-entities-views).

Notice that our `Contact` class extends core's `ContentEntityBase` class. It's worth taking the time to look at [the source code for this class](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21ContentEntityBase.php/class/ContentEntityBase/) to get a sense of the properties and methods available to our implementation. Also, notice that our `Contact` class is implementing an interface `ContactInterface`. We'll create this next.

See [ContentEntityType Attribute: Properties Reference](https://drupalize.me/tutorial/contententitytype-attribute-properties-reference) for a complete list of attribute properties and example values.

### Create an interface

Create the file */modules/custom/content\_entity\_example/src/ContactInterface.php*. (Note that this file should live directly in the *src* directory and **not** inside *src/Entity*.) Populate it with the following contents:

```
<?php

namespace Drupal\content_entity_example;

use Drupal\Core\Entity\ContentEntityInterface;
use Drupal\user\EntityOwnerInterface;
use Drupal\Core\Entity\EntityChangedInterface;

/**
 * Provides an interface defining a Contact entity.
 *
 * We have this interface so we can join the other interfaces it extends.
 *
 * @ingroup content_entity_example
 */
interface ContactInterface extends ContentEntityInterface, EntityOwnerInterface, EntityChangedInterface {

}
```

The interface itself isn't very sophisticated. It extends a few core interfaces but provides no new custom functionality. But, it's considered a best practice for your entity to implement an interface, because this allows other module developers to better understand the behavior of your custom entity in case they want to override or extend it.

### Fill in entity class with methods (and traits)

There's an important method to add to our `Contact` class: the `baseFieldDefinitions` method. You should already be familiar with the concept of base fields from [the Entity API basics](https://drupalize.me/tutorial/entity-api-implementation-basics) tutorial.

The class also uses 2 traits: the `EntityChangedTrait` trait, which allows it to record timestamps of save operations, and `EntityOwnerTrait`, which contains entity owner ID getter and setter methods.

**Note:** In order for the `EntityOwnerTrait` to work as designed, the **owner** *entity\_key* specified in the attribute needs to match the corresponding owner `$fields` key in `baseFieldDefinitions()`, for example, `user_id`.

| In ContentEntityType attribute | In baseFieldDefinitions() |
| --- | --- |
| `entity_keys => owner =>` **user\_id** | `$fields['user_id']` |

Here's what the implementation looks like in our `Contact` class (*src/Entity/Contact.php*):

```
class Contact extends ContentEntityBase implements ContactInterface {

  use EntityChangedTrait;
  use EntityOwnerTrait;

  /**
   * {@inheritdoc}
   *
   * When a new entity instance is added, set the user_id entity reference to
   * the current user as the creator of the instance.
   */
  public function preSave(EntityStorageInterface $storage) {
    parent::preSave($storage);
    if (!$this->getOwnerId()) {
      // If no owner has been set explicitly, make the anonymous user the owner.
      $this->setOwnerId(0);
    }
  }

  /**
   * {@inheritdoc}
   *
   * Define the field properties here.
   *
   * Field name, type and size determine the table structure.
   *
   * In addition, we can define how the field and its content can be manipulated
   * in the GUI. The behaviour of the widgets used can be determined here.
   */
  public static function baseFieldDefinitions(EntityTypeInterface $entity_type) {

    // In ContentEntityBase, baseFieldDefinitions defines fields
    // id, uuid, revision, langcode, and bundle.
    $fields = parent::baseFieldDefinitions($entity_type);

    // Also add any default base field definitions from EntityOwnerTrait. When using any other
    // entity traits in your code, you should check to see if the trait provides any default
    // base fields and make sure you call that method.
    $fields += static::ownerBaseFieldDefinitions($entity_type);

    // If you want to override any definitions of fields otherwise defined
    // in ContentEntityBase::baseFieldDefinitions, do so here.

    // Name field for the contact.
    // We set display options for the view as well as the form.
    // Users with correct privileges can change the view and edit configuration.
    $fields['name'] = BaseFieldDefinition::create('string')
      ->setLabel(t('Name'))
      ->setDescription(t('The name of the Contact entity.'))
      ->setSettings([
        'max_length' => 255,
        'text_processing' => 0,
      ])
      // Set no default value.
      ->setDefaultValue(NULL)
      ->setDisplayOptions('view', [
        'label' => 'above',
        'type' => 'string',
        'weight' => -6,
      ])
      ->setDisplayOptions('form', [
        'type' => 'string_textfield',
        'weight' => -6,
      ])
      ->setDisplayConfigurable('form', TRUE)
      ->setDisplayConfigurable('view', TRUE);

    $fields['first_name'] = BaseFieldDefinition::create('string')
      ->setLabel(t('First Name'))
      ->setDescription(t('The first name of the Contact entity.'))
      ->setSettings([
        'max_length' => 255,
        'text_processing' => 0,
      ])
      // Set no default value.
      ->setDefaultValue(NULL)
      ->setDisplayOptions('view', [
        'label' => 'above',
        'type' => 'string',
        'weight' => -5,
      ])
      ->setDisplayOptions('form', [
        'type' => 'string_textfield',
        'weight' => -5,
      ])
      ->setDisplayConfigurable('form', TRUE)
      ->setDisplayConfigurable('view', TRUE);

    // Owner field of the contact.
    // Entity reference field, holds the reference to the user object.
    // The view shows the username field of the user.
    // The form presents an autocomplete field for the username.
    // The key in $fields['user_id'] needs to match whatever is set in
    // the 'owner' entity key in the attribute, in order for the
    // EntityOwnerTrait to work as designed.
    $fields['user_id'] = BaseFieldDefinition::create('entity_reference')
      ->setLabel(t('User Name'))
      ->setDescription(t('The Name of the associated user.'))
      ->setSetting('target_type', 'user')
      ->setSetting('handler', 'default')
      ->setDisplayOptions('view', [
        'label' => 'above',
        'type' => 'author',
        'weight' => -3,
      ])
      ->setDisplayOptions('form', [
        'type' => 'entity_reference_autocomplete',
        'settings' => [
          'match_operator' => 'CONTAINS',
          'match_limit' => 10,
          'size' => 60,
          'placeholder' => '',
        ],
        'weight' => -3,
      ])
      ->setDisplayConfigurable('form', TRUE)
      ->setDisplayConfigurable('view', TRUE);

    // Role field for the contact.
    // The values shown in options are 'administrator' and 'user'.
    $fields['role'] = BaseFieldDefinition::create('list_string')
      ->setLabel(t('Role'))
      ->setDescription(t('The role of the Contact entity.'))
      ->setSettings([
        'allowed_values' => [
          'administrator' => 'administrator',
          'user' => 'user',
        ],
      ])
      // Set the default value of this field to 'user'.
      ->setDefaultValue('user')
      ->setDisplayOptions('view', [
        'label' => 'above',
        'type' => 'string',
        'weight' => -2,
      ])
      ->setDisplayOptions('form', [
        'type' => 'options_select',
        'weight' => -2,
      ])
      ->setDisplayConfigurable('form', TRUE)
      ->setDisplayConfigurable('view', TRUE);

    $fields['created'] = BaseFieldDefinition::create('created')
      ->setLabel(t('Created'))
      ->setDescription(t('The time that the entity was created.'));

    $fields['changed'] = BaseFieldDefinition::create('changed')
      ->setLabel(t('Changed'))
      ->setDescription(t('The time that the entity was last edited.'));

    return $fields;
  }

}
```

### Create the entity list builder controller

In our entity class' attribute, we referenced an **entity list builder controller** which we'll create now. Create a *Controller* directory inside *src/Entity* and then add a new file (and necessary directory) *modules/custom/content\_entity\_example/src/Entity/Controller/ContactListBuilder.php* with the following PHP code:

```
<?php

namespace Drupal\content_entity_example\Entity\Controller;

use Drupal\Core\Entity\EntityInterface;
use Drupal\Core\Entity\EntityTypeInterface;
use Drupal\Core\Entity\EntityListBuilder;
use Drupal\Core\Entity\EntityStorageInterface;
use Drupal\Core\Routing\UrlGeneratorInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;

/**
 * Provides a list controller for the content_entity_example entity.
 *
 * @ingroup content_entity_example
 */
class ContactListBuilder extends EntityListBuilder {

  /**
   * The url generator.
   *
   * @var \Drupal\Core\Routing\UrlGeneratorInterface
   */
  protected $urlGenerator;

  /**
   * {@inheritdoc}
   */
  public static function createInstance(ContainerInterface $container, EntityTypeInterface $entity_type) {
    return new static(
      $entity_type,
      $container->get('entity_type.manager')->getStorage($entity_type->id()),
      $container->get('url_generator')
    );
  }

  /**
   * Constructs a new ContactListBuilder object.
   *
   * @param \Drupal\Core\Entity\EntityTypeInterface $entity_type
   *   The entity type definition.
   * @param \Drupal\Core\Entity\EntityStorageInterface $storage
   *   The entity storage class.
   * @param \Drupal\Core\Routing\UrlGeneratorInterface $url_generator
   *   The url generator.
   */
  public function __construct(EntityTypeInterface $entity_type, EntityStorageInterface $storage, UrlGeneratorInterface $url_generator) {
    parent::__construct($entity_type, $storage);
    $this->urlGenerator = $url_generator;
  }

  /**
   * {@inheritdoc}
   *
   * We override ::render() so that we can add our own content above the table.
   * parent::render() is where EntityListBuilder creates the table using our
   * buildHeader() and buildRow() implementations.
   */
  public function render() {
    $build['description'] = [
      '#markup' => $this->t('Content Entity Example implements a Contacts model. These contacts are fieldable entities. You can manage the fields on the <a href="@adminlink">Contacts admin page</a>.', [
        '@adminlink' => $this->urlGenerator->generateFromRoute('content_entity_example.contact_settings'),
      ]),
    ];
    $build['table'] = parent::render();
    return $build;
  }

  /**
   * {@inheritdoc}
   *
   * Building the header and content lines for the contact list.
   *
   * Calling the parent::buildHeader() adds a column for the possible actions
   * and inserts the 'edit' and 'delete' links as defined for the entity type.
   */
  public function buildHeader() {
    $header['id'] = $this->t('ContactID');
    $header['name'] = $this->t('Name');
    $header['first_name'] = $this->t('First Name');
    $header['role'] = $this->t('Role');
    return $header + parent::buildHeader();
  }

  /**
   * {@inheritdoc}
   */
  public function buildRow(EntityInterface $entity) {
    /* @var $entity \Drupal\content_entity_example\Entity\Contact */
    $row['id'] = $entity->id();
    $row['name'] = $entity->toLink()->toString();
    $row['first_name'] = $entity->first_name->value;
    $row['role'] = $entity->role->value;
    return $row + parent::buildRow($entity);
  }

}
```

### Create the form classes

We need to create the **form controllers** referenced by the routing file. Let's create those now, and then we'll be ready to install our module. We'll use a class provided by core for the `delete-form` (`Drupal\Core\Entity\ContentEntityDeleteForm`), which we specified as a delete form handler class in our entity's attribute.

Create the directory *src/Form*. All the form controller class files will be added to this directory.

#### *ContactForm.php*

Create the file *modules/custom/content\_entity\_example/src/Form/ContactForm.php* with the following PHP code:

```
<?php

namespace Drupal\content_entity_example\Form;

use Drupal\Core\Entity\ContentEntityForm;
use Drupal\Core\Language\Language;
use Drupal\Core\Form\FormStateInterface;

/**
 * Form controller for the content_entity_example entity edit forms.
 *
 * @ingroup content_entity_example
 */
class ContactForm extends ContentEntityForm {

  /**
   * {@inheritdoc}
   */
  public function buildForm(array $form, FormStateInterface $form_state) {
    /* @var $entity \Drupal\content_entity_example\Entity\Contact */
    $form = parent::buildForm($form, $form_state);
    $entity = $this->entity;

    $form['langcode'] = [
      '#title' => $this->t('Language'),
      '#type' => 'language_select',
      '#default_value' => $entity->getUntranslated()->language()->getId(),
      '#languages' => Language::STATE_ALL,
    ];
    return $form;
  }

  /**
   * {@inheritdoc}
   */
  public function save(array $form, FormStateInterface $form_state) {
    $form_state->setRedirect('entity.content_entity_example_contact.collection');
    $entity = $this->getEntity();
    $result =  $entity->save();

    $message_arguments = ['%label' => $this->entity->label()];

    if ($result == SAVED_NEW) {
      $this->messenger()->addStatus($this->t('New contact %label has been created.', $message_arguments));
    }
    else {
      $this->messenger()->addStatus($this->t('The contact %label has been updated.', $message_arguments));
    }
  }

}
```

#### *ContactSettingsForm.php*

Create the file *modules/custom/content\_entity\_example/src/Form/ContactSettingsForm.php* with the following PHP code:

```
<?php

namespace Drupal\content_entity_example\Form;

use Drupal\Core\Form\FormBase;
use Drupal\Core\Form\FormStateInterface;

/**
 * Class ContentEntityExampleSettingsForm.
 *
 * @ingroup content_entity_example
 */
class ContactSettingsForm extends FormBase {

  /**
   * Returns a unique string identifying the form.
   *
   * @return string
   *   The unique string identifying the form.
   */
  public function getFormId() {
    return 'content_entity_example_settings';
  }

  /**
   * {@inheritdoc}
   */
  public function submitForm(array &$form, FormStateInterface $form_state) {
    // Empty implementation of the abstract submit class.
  }

  /**
   * {@inheritdoc}
   */
  public function buildForm(array $form, FormStateInterface $form_state) {
    $form['contact_settings']['#markup'] = 'Settings form for ContentEntityExample. Manage field settings here.';
    return $form;
  }

}
```

This is only a placeholder for an actual settings form. To learn how to create a settings form for a configuration entity (much the same process), see [Create a Settings Form in a Module](https://drupalize.me/tutorial/create-settings-form-module).

### Create the access control handler class

Now, let's create the **access handler class** referenced in the attribute for `content_entity_example_contact`.

Create the file *modules/custom/content\_entity\_example/src/ContactAccessControlHandler* with the following contents:

```
<?php

namespace Drupal\content_entity_example;

use Drupal\Core\Access\AccessResult;
use Drupal\Core\Entity\EntityAccessControlHandler;
use Drupal\Core\Entity\EntityInterface;
use Drupal\Core\Session\AccountInterface;

/**
 * Access controller for the contact entity.
 */
class ContactAccessControlHandler extends EntityAccessControlHandler {

  /**
   * {@inheritdoc}
   *
   * Link the activities to the permissions. checkAccess() is called with the
   * $operation as defined in the routing.yml file.
   */
  protected function checkAccess(EntityInterface $entity, $operation, AccountInterface $account) {
    // Check the admin_permission as defined in your #[ContentEntityType]
    // attribute.
    $admin_permission = $this->entityType->getAdminPermission();
    if ($account->hasPermission($admin_permission)) {
      return AccessResult::allowed();
    }
    switch ($operation) {
      case 'view':
        return AccessResult::allowedIfHasPermission($account, 'view contact entity');

      case 'update':
        return AccessResult::allowedIfHasPermission($account, 'edit contact entity');

      case 'delete':
        return AccessResult::allowedIfHasPermission($account, 'delete contact entity');
    }
    return AccessResult::neutral();
  }

  /**
   * {@inheritdoc}
   *
   * Separate from the checkAccess because the entity does not yet exist. It
   * will be created during the 'add' process.
   */
  protected function checkCreateAccess(AccountInterface $account, array $context, $entity_bundle = NULL) {
    // Check the admin_permission as defined in your #[ContentEntityType]
    // attribute.
    $admin_permission = $this->entityType->getAdminPermission();
    if ($account->hasPermission($admin_permission)) {
      return AccessResult::allowed();
    }
    return AccessResult::allowedIfHasPermission($account, 'add contact entity');
  }

}
```

### Install the module

Install the module using Drush (`drush en content_entity_example`) or using the *Manage* administrative menu, navigate to *Extend* and enable the Content Entity Example module in the Custom group.

Navigate to *content\_entity\_example\_contact/list* and *admin/structure/content\_entity\_example\_contact\_settings* to view the pages we created with this module.

Here is the listing view of our contact entities in action:

Image

![Contact entity listing](/sites/default/files/styles/max_800w/public/tutorials/images/contact_entity_listing_example.png?itok=jDPR5sd7)

## Generate custom content entity code with Drush

[Drush](https://drupalize.me/topic/drush) provides some code generation and scaffolding tools, including one that will generate scaffolding for a custom content entity. See the tutorial, [Scaffold a Custom Content Entity Type with Drush Generators](https://drupalize.me/tutorial/scaffold-custom-content-entity-type-drush-generators), to walk through and learn the process of generating a custom content entity with Drush.

## Recap

In this tutorial, we looked at the requirements for creating a custom entity type. We created a new module, an `*EntityType` attribute and a new class to encapsulate the behavior of a contact entity. Now that we understand the key components that go into creating a new entity type, we can use Drush to help speed up our development process in the future.

## Further your understanding

- Walk through the files generated by Drush when creating a content entity. Can you modify the default boilerplate to provide the functionality of the contact entity in the Examples module?
- Take a look at the node module and the *Node.php* class. Are there any surprises or useful things implemented there that could enhance the behavior of our contact entity?
- What would be the next step if we wanted to add relationships between our contact entities to build a basic customer relationship management tool?

### What about revisionable entities?

- Does your content entity need to support **revisions**? Refer to the following resources to learn how to make your entity revisionable or how to update your entity to be revisionable:

  - [Make an entity revisionable](https://www.drupal.org/docs/drupal-apis/entity-api/making-an-entity-revisionable) (Drupal.org)
  - [Change record: Revision metadata fields are now defined in the entity annotation](https://www.drupal.org/node/2831499) (Drupal.org)
  - [Change record: Support for automatic entity updates has been removed (examples given on how to convert an entity to be revisionable)](https://www.drupal.org/node/3034742)

The [Drush content entity generator](https://drupalize.me/tutorial/scaffold-custom-content-entity-type-drush-generators) has an option for making your entity revisionable.

## Additional resources

- Review the [ContentEntityType Attribute Properties Reference](https://drupalize.me/tutorial/contententitytype-attribute-properties-reference) (Drupalize.Me)
- [Scaffold a Custom Content Entity Type with Drush Generators](https://drupalize.me/tutorial/scaffold-custom-content-entity-type-drush-generators) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Entity API Implementation Basics](/tutorial/entity-api-implementation-basics?p=2607)

Next
[ContentEntityType Attribute: Properties Reference](/tutorial/contententitytype-attribute-properties-reference?p=2607)

Clear History

Ask Drupalize.Me AI

close