---
title: "Create a Configuration Entity Type"
url: "https://drupalize.me/tutorial/create-configuration-entity-type?p=2476"
guide: "[[work-data-modules]]"
---

# Create a Configuration Entity Type

## Content

In this tutorial, we’re going to walk through the process of creating a custom configuration entity type in Drupal in a custom module. We'll be using Drush's `generate entity:configuration` command to create and update the files in our example module. After Drush has generated and updated the files for our configuration entity, we'll walk through each file and see how they define data structure, metadata, an administrative interface, and menu links for a configuration entity in Drupal.

By the end of this tutorial, you should be able to:

- Use Drush to generate a configuration entity type
- Identify files associated with a configuration entity and summarize the purpose and function of the code inside each file

## Goal

Create a configuration entity type using Drush and understand each of the files associated with it.

## Prerequisites

- [Create a Settings Form in a Module](https://drupalize.me/tutorial/create-settings-form-module)
- [Drush](https://drupalize.me/topic/drush)
- [Overview: Menu Links in a Module](https://drupalize.me/tutorial/overview-menu-links-module)
- [PHP Attributes](https://drupalize.me/tutorial/php-attributes)
- [Form API Overview](https://drupalize.me/tutorial/form-api-overview)
- [Overview: Info Files for Drupal Modules](https://drupalize.me/tutorial/overview-info-files-drupal-modules)
- [Define Permissions for a Module](https://drupalize.me/tutorial/define-permissions-module)

## Use Drush to generate a configuration entity

We can use Drush to generate a custom configuration entity that stores video presets.

If you haven't already created a custom module, then you will need to do that first before continuing. Use the Drush command `drush generate module` and follow the interactive prompts to create a module called *transcode\_profile*.

### Generate the configuration entity type using Drush

Open a terminal, and in your project, run the Drush command `drush generate entity:configuration`.

| Prompt | Description |
| --- | --- |
| Module machine name | Enter `transcode_profile` or the name of your custom module that should contain this config entity type. |
| Entity type label | Enter the singular label of the configuration entity, e.g., `Video preset`. |
| Entity type ID | Enter the entity type ID, e.g., `video_preset`. |

```
 The following directories and files have been created or updated:
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
 • /var/www/html/web/modules/custom/transcode_profile/transcode_profile.links.action.yml
 • /var/www/html/web/modules/custom/transcode_profile/transcode_profile.links.menu.yml
 • /var/www/html/web/modules/custom/transcode_profile/transcode_profile.permissions.yml
 • /var/www/html/web/modules/custom/transcode_profile/transcode_profile.routing.yml
 • /var/www/html/web/modules/custom/transcode_profile/config/schema/transcode_profile.schema.yml
 • /var/www/html/web/modules/custom/transcode_profile/src/VideoPresetInterface.php
 • /var/www/html/web/modules/custom/transcode_profile/src/VideoPresetListBuilder.php
 • /var/www/html/web/modules/custom/transcode_profile/src/Entity/VideoPreset.php
 • /var/www/html/web/modules/custom/transcode_profile/src/Form/VideoPresetForm.php
```

### Review the configuration entity class

The generated configuration entity class will have a "CamelCase" name of the entity type ID you entered in the `drush generate entity:configuration` prompt, saved in your module's *src/Entity* directory.

Open *modules/custom/transcode\_profile/src/Entity/VideoPreset.php* in your IDE. This class:

- Defines an [attribute](https://drupalize.me/tutorial/php-attributes), `#[ConfigEntityType]`, that defines the essential metadata for this class.
- Extends `ConfigEntityBase` and adds 3 example properties. These 3 properties are also described in the scaffolded *config/schema/transcode\_profile.schema.yml* file.

```
<?php

declare(strict_types=1);

namespace Drupal\transcode_profile\Entity;

use Drupal\Core\Config\Entity\ConfigEntityBase;
use Drupal\Core\Entity\Attribute\ConfigEntityType;
use Drupal\Core\Entity\EntityDeleteForm;
use Drupal\Core\StringTranslation\TranslatableMarkup;
use Drupal\transcode_profile\Form\VideoPresetForm;
use Drupal\transcode_profile\VideoPresetInterface;
use Drupal\transcode_profile\VideoPresetListBuilder;

/**
 * Defines the video preset entity type.
 */
#[ConfigEntityType(
  id: 'video_preset',
  label: new TranslatableMarkup('Video preset'),
  label_collection: new TranslatableMarkup('Video presets'),
  label_singular: new TranslatableMarkup('video preset'),
  label_plural: new TranslatableMarkup('video presets'),
  config_prefix: 'video_preset',
  entity_keys: [
    'id' => 'id',
    'label' => 'label',
    'uuid' => 'uuid',
  ],
  handlers: [
    'list_builder' => VideoPresetListBuilder::class,
    'form' => [
      'add' => VideoPresetForm::class,
      'edit' => VideoPresetForm::class,
      'delete' => EntityDeleteForm::class,
    ],
  ],
  links: [
    'collection' => '/admin/structure/video-preset',
    'add-form' => '/admin/structure/video-preset/add',
    'edit-form' => '/admin/structure/video-preset/{video_preset}',
    'delete-form' => '/admin/structure/video-preset/{video_preset}/delete',
  ],
  admin_permission: 'administer video_preset',
  label_count: [
    'singular' => '@count video preset',
    'plural' => '@count video presets',
  ],
  config_export: [
    'id',
    'label',
    'description',
  ],
)]
final class VideoPreset extends ConfigEntityBase implements VideoPresetInterface {

  /**
   * The example ID.
   */
  protected string $id;

  /**
   * The example label.
   */
  protected string $label;

  /**
   * The example description.
   */
  protected string $description;

}
```

See also the [ContentEntityType Attribute: Properties Reference](https://drupalize.me/tutorial/contententitytype-attribute-properties-reference) for an explanation of the properties described in this attribute. Most of the properties for a `ContentEntityType` also apply to `ConfigEntityType`.

### Review the configuration schema

In [Create a Settings Form in a Module](https://drupalize.me/tutorial/create-settings-form-module), we created the */config/schema/transcode\_profile.schema.yml*. When we ran `drush generate entity:configuration`, this file was updated to add a schema for the 3 example properties of our configuration entity, `id`, `label`, and `description`.

Open *modules/custom/transcode\_profile/config/schema/transcode\profile.schema.yml* in your IDE.

```
# Schema for the configuration files of the Transcode profile module.
transcode_profile.settings:
  type: config_object
  label: 'Transcode profile settings'
  mapping:
    profile_name:
      type: string
      label: 'Profile name'
    enable_transcoding:
      type: boolean
      label: 'Enable transcoding?'

transcode_profile.video_preset.*:
  type: config_entity
  label: Video preset
  mapping:
    id:
      type: string
      label: ID
    label:
      type: label
      label: Label
    uuid:
      type: string
    description:
      type: string
```

### Review the interface

Note that Drush scaffolded an empty interface. We'll update it as we add custom properties to our config entity in later tutorials.

Open *modules/custom/transcode\_profile/src/VideoPresetInterface.php*

```
<?php

declare(strict_types=1);

namespace Drupal\transcode_profile;

use Drupal\Core\Config\Entity\ConfigEntityInterface;

/**
 * Provides an interface defining a video preset entity type.
 */
interface VideoPresetInterface extends ConfigEntityInterface {

}
```

### Review the form

This form will be used by administrators to create new `video_preset` configuration entities.

Open *modules/custom/transcode\_profile/src/Form/VideoPresetForm.php* in your IDE:

```
<?php

declare(strict_types=1);

namespace Drupal\transcode_profile\Form;

use Drupal\Core\Entity\EntityForm;
use Drupal\Core\Form\FormStateInterface;
use Drupal\transcode_profile\Entity\VideoPreset;

/**
 * Video preset form.
 */
final class VideoPresetForm extends EntityForm {

  /**
   * {@inheritdoc}
   */
  public function form(array $form, FormStateInterface $form_state): array {

    $form = parent::form($form, $form_state);

    $form['label'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Label'),
      '#maxlength' => 255,
      '#default_value' => $this->entity->label(),
      '#required' => TRUE,
    ];

    $form['id'] = [
      '#type' => 'machine_name',
      '#default_value' => $this->entity->id(),
      '#machine_name' => [
        'exists' => [VideoPreset::class, 'load'],
      ],
      '#disabled' => !$this->entity->isNew(),
    ];

    $form['status'] = [
      '#type' => 'checkbox',
      '#title' => $this->t('Enabled'),
      '#default_value' => $this->entity->status(),
    ];

    $form['description'] = [
      '#type' => 'textarea',
      '#title' => $this->t('Description'),
      '#default_value' => $this->entity->get('description'),
    ];

    return $form;
  }

  /**
   * {@inheritdoc}
   */
  public function save(array $form, FormStateInterface $form_state): int {
    $result = parent::save($form, $form_state);
    $message_args = ['%label' => $this->entity->label()];
    $this->messenger()->addStatus(
      match($result) {
        \SAVED_NEW => $this->t('Created new example %label.', $message_args),
        \SAVED_UPDATED => $this->t('Updated example %label.', $message_args),
      }
    );
    $form_state->setRedirectUrl($this->entity->toUrl('collection'));
    return $result;
  }

}
```

### Review the list builder class

Just like with [content entities](https://drupalize.me/tutorial/create-custom-content-entity), configuration entities need a page that lists all the user-defined configuration entities of a certain type.

In the `#[ConfigEntityType]` attribute of our `VideoPreset` class, under `handlers`, the `list_builder` value is `VideoPresetListBuilder::class`. This value could also use the full PSR-4 namespace of the class.

This class builds a table that will list all our `video_preset` configuration entities for administrators.

Open */modules/custom/transcode\_profile/src/VideoPresetListBuilder.php* in your IDE:

```
<?php

declare(strict_types=1);

namespace Drupal\transcode_profile;

use Drupal\Core\Config\Entity\ConfigEntityListBuilder;
use Drupal\Core\Entity\EntityInterface;

/**
 * Provides a listing of video presets.
 */
final class VideoPresetListBuilder extends ConfigEntityListBuilder {

  /**
   * {@inheritdoc}
   */
  public function buildHeader(): array {
    $header['label'] = $this->t('Label');
    $header['id'] = $this->t('Machine name');
    $header['status'] = $this->t('Status');
    return $header + parent::buildHeader();
  }

  /**
   * {@inheritdoc}
   */
  public function buildRow(EntityInterface $entity): array {
    /** @var \Drupal\transcode_profile\VideoPresetInterface $entity */
    $row['label'] = $entity->label();
    $row['id'] = $entity->id();
    $row['status'] = $entity->status() ? $this->t('Enabled') : $this->t('Disabled');
    return $row + parent::buildRow($entity);
  }

}
```

### Review the permissions YAML file

A custom permission, `Administer video preset` was created by Drush and included in our module's *transcode\_profile.permissions.yml* file. This permission is then used to gate access to configuration entity administrative routes in *transcode\_profile.routing.yml*.

Open *modules/custom/transcode\_profile/transcode\_profile.permissions.yml* in your IDE:

```
administer video_preset:
  title: 'Administer video preset'
```

### Review the updates to the routing YAML file

As we see in *src/Entity/VideoPreset.php*, the `#[ConfigEntityType]` attribute defines a set of standard administrative pages for listing, adding, editing, and deleting `video_preset` configuration entities. Routes for each of these pages were added by Drush. A route for the [settings form we previously created](https://drupalize.me/tutorial/create-settings-form-module) is also listed here.

Open *modules/custom/transcode\_profile/transcode\_profile.routing.yml* in your IDE:

```
transcode_profile.settings:
  path: '/admin/config/media/transcode_profile/settings'
  defaults:
    _title: 'Transcode profile settings'
    _form: 'Drupal\transcode_profile\Form\SettingsForm'
  requirements:
    _permission: 'administer site configuration'

entity.video_preset.collection:
  path: '/admin/structure/video-preset'
  defaults:
    _entity_list: 'video_preset'
    _title: 'Video preset configuration'
  requirements:
    _permission: 'administer video_preset'

entity.video_preset.add_form:
  path: '/admin/structure/video_preset/add'
  defaults:
    _entity_form: 'video_preset.add'
    _title: 'Add a video preset'
  requirements:
    _permission: 'administer video_preset'

entity.video_preset.edit_form:
  path: '/admin/structure/video-preset/{video_preset}'
  defaults:
    _entity_form: 'video_preset.edit'
    _title: 'Edit a video preset'
  requirements:
    _permission: 'administer video_preset'

entity.video_preset.delete_form:
  path: '/admin/structure/video-preset/{video_preset}/delete'
  defaults:
    _entity_form: 'video_preset.delete'
    _title: 'Delete a video preset'
  requirements:
    _permission: 'administer video_preset'
```

### Review the menu links YAML file

Drush updated our module's [menu link file](https://drupalize.me/tutorial/overview-menu-links-module) to add a link from the *Structure* administrative page (see the `parent` key) to the "collection" administrative page for *Video presets*.

Open *modules/custom/transcode\_profile/transcode\_profile.links.menu.yml* in your IDE:

```
transcode_profile.settings:
  title: Transcode profile settings
  description: Configure settings for Transcode profile module.
  parent: system.admin_config_media
  route_name: transcode_profile.settings
  weight: 10

entity.video_preset.overview:
  title: Video presets
  parent: system.admin_structure
  description: 'List of video presets to extend site functionality.'
  route_name: entity.video_preset.collection
```

### Review the action links YAML file

Then, once a user lands on the "collection" page, an [action link](https://drupalize.me/tutorial/add-action-link-module) displays, which adds a button link to "Add video preset".

Open *modules/custom/transcode\_profile/transcode\_profile.links.action.yml* in your IDE:

```
entity.video_preset.add_form:
  route_name: 'entity.video_preset.add_form'
  title: 'Add video preset'
  appears_on:
    - entity.video_preset.collection
```

### Clear caches

Before we can see these pages in the administrative UI, we need to [clear Drupal's cache](https://drupalize.me/tutorial/clear-drupals-cache) with `drush cr`.

### View configuration entity administrative pages

1. Using the *Manage* administration menu, navigate to *Structure* (*admin/structure*).
2. Navigate to *Video presets* (*admin/structure/video-preset*), which takes you to the "collection" page, which will list all video preset configuration entities as they are created.
3. On this page, click the action link (button) **+ Add video preset** to view the form for creating a new video preset configuration entity.

As you can see, by using Drush to generate a new configuration entity type, we can quickly scaffold the necessary files that encapsulate the behavior of the configuration entity.

## Recap

In this tutorial, we used Drush to scaffold the files we need to create a custom configuration entity type. We reviewed the files that were generated and previewed the administrative pages in a browser.

## Further your understanding

- Compare the process of [creating a content entity type](https://drupalize.me/tutorial/create-custom-content-entity) with creating a configuration entity type.

## Additional resources

- [ContentEntityType Attribute: Properties Reference](https://drupalize.me/tutorial/contententitytype-attribute-properties-reference) (Drupalize.Me)
- [Configuration API](https://api.drupal.org/api/drupal/core%21core.api.php/group/config_api/) (api.drupal.org)
- [Configuration schema/metadata documentation](https://www.drupal.org/docs/drupal-apis/configuration-api/configuration-schemametadata#properties) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Use Simple Configuration in a Form](/tutorial/use-simple-configuration-form?p=2476)

Next
[Add Properties to a Configuration Entity Type](/tutorial/add-properties-configuration-entity-type?p=2476)

Clear History

Ask Drupalize.Me AI

close