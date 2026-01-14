---
title: "Add Properties to a Configuration Entity Type"
url: "https://drupalize.me/tutorial/add-properties-configuration-entity-type?p=2476"
guide: "[[work-data-modules]]"
order: 27
---

# Add Properties to a Configuration Entity Type

## Content

In this tutorial, you'll learn how to add a property to a configuration entity type in Drupal. [Previously, we created a configuration entity type](https://drupalize.me/tutorial/create-configuration-entity-type) called *video\_preset* and, using Drush, scaffolded the files and code to define a custom configuration entity type. Now, we'll add a new property called *codec* to this configuration entity type and update the code we created in the previous tutorial.

To add this new property to our custom configuration entity type, we need to update our schema file, configuration entity forms, the entity list builder class, and add getter and setter methods to our `ConfigEntityType` class.

## Goal

- Add a new property, `codec`, to the configuration entity type `video_preset` we created in [Create a Configuration Entity Type](https://drupalize.me/tutorial/create-configuration-entity-type).

## Prerequisites

- [Create a Configuration Entity Type](https://drupalize.me/tutorial/create-configuration-entity-type)

## Add a property to a custom configuration entity

To add a new property, *codec*, to our Video preset configuration entity type, we need to update the following files in our custom module, *transcode\_profile*:

- *config/schema/transcode\_profile.schema.yml*
- *src/Entity/VideoPreset.php*
- *src/Form/VideoPresetForm.php*
- *src/VideoPresetListBuilder.php*

### Add the property to the module's schema file

Open *modules/custom/transcode\_profile/config/schema/transcode\_profile.schema.yml* in your IDE.

Add a new property called *codec* using the type `label` and the label `Codec` in the `mapping` array.

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
    codec:
      type: label
      label: 'Codec'
```

### Update the config entity type class

Open *modules/custom/transcode\_profile/src/Entity/VideoPreset.php*.

Add a new protected property `$codec` inside the `VideoPreset` class. Use the Drush-scaffolded properties as a guide.

### Update the attribute

In this same file, update the attribute's `config_export` key and add the `codec` property to the list.

Applying the changes for this and the previous step, the `VideoPreset` config entity type class should now look like this:

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
    'codec'
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

  /**
   * The codec.
   * 
   * @var string
   */
  protected string $codec;

}
```

### Update the entity form class

Add a new textfield form field to the *src/Form/VideoPresetForm* to allow administrators to add codec data when they create a *video\_preset* configuration entity.

Open *modules/custom/transcode\_profile/src/Form/VideoPresetForm.php* in your IDE.

Within the `form()` method, add a new field to the `$form` array for `codec` with the following properties:

| Property | Value |
| --- | --- |
| `#type` | `'textfield'` |
| `#title` | `$this->t('Codec')` |
| `#maxlength` | 255 |
| `#default_value` | `'#default_value' => $this->entity->get('codec')->getValue(),` |
| `#description` | `$this->t('The video codec to use.')` |

The *src/Form/VideoPresetForm.php* file should now look like this:

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

    $form['codec'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Codec'),
      '#maxlength' => 255,
      '#default_value' => $this->entity->get('codec'),
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

### (Optional) Update the list builder class

Now we're ready to update the list builder class. You would only want to add a new property to your list builder class if the value will be both short enough to display in table cell and useful data for the administrator as they peruse the list of configuration entities of this type.

Open *modules/custom/transcode\_profile/src/VideoPresetListBuilder.php*.

Update both the `buildHeader()` and `buildRow()` methods to add a column for the `codec` property.

The *src/VideoPresetListBuilder.php* should now look like this:

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
    $header['codec'] = $this->t('Codec');
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
    $row['codec'] = $entity->get('codec');
    $row['status'] = $entity->status() ? $this->t('Enabled') : $this->t('Disabled');
    return $row + parent::buildRow($entity);
  }

}
```

### Clear Drupal's cache

Before we can see these pages in the administrative UI, we need to [clear Drupal's cache](https://drupalize.me/tutorial/clear-drupals-cache) with `drush cr`.

### Test out new configuration entity property

We've updated all the necessary files, and we're ready to see it in action on our Drupal site.

Using the *Manage* administrative menu, navigate to *Structure* > *Video presets* (*/admin/structure/video-presets*).

Add or edit a video preset configuration entity. You should now see the new *Codec* text field added to the form.

Create 2 video presets with the following values:

| Field | 800x600 | 1024x768 |
| --- | --- | --- |
| Label | 800x600 | 1024x768 |
| Codec | h264 | h264 |
| Enabled | Checked | Checked |

Image

![Video preset entity form with new codec field](../assets/images/config-entities-codec-form-field.png)

After saving the form, you'll be redirected to the listing page, which should display the 2 video preset configuration entities you created.

Image

![Video presets listing page](../assets/images/config-entities-list-with-codec.png)

### Add default configuration entities

Now that we've created video presets, we can use them as a basis for default configuration provided by our module.

1. Export your site's configuration with Drush: `drush config:export`
2. Locate the 2 `transcode_profile.video_preset.*` exported configuration YAML files in your site's configuration sync directory.
3. Copy (don't move) both of the files and paste them into our module's *config/install* directory.
4. Open files (in *transcode\_profile/config/install*) in your IDE.
5. Delete the first line beginning with `uuid` from both files.

The *modules/custom/transcode\_profile/config/install/transcode\_profile.video\_preset/800x600.yml* file should now look like this:

```
langcode: en
status: true
dependencies: {  }
id: 800x600
label: 800x600
description: ''
codec: h264
```

The *modules/custom/transcode\_profile/config/install/transcode\_profile.video\_preset/1024x768.yml* file should now look like this:

```
langcode: en
status: true
dependencies: {  }
id: 1024x768
label: 1024x768
description: ''
codec: h264
```

## Recap

In this tutorial, we added a new property to our custom *Video preset* configuration entity type. We updated the code in several places, including our module's schema file, the config entity type definition class, the config entity form class, and the list builder class.

We created 2 video preset configuration entities, then, after exporting our site's configuration, used the exported configuration objects to create default video preset configuration in our module.

In the [following tutorial](https://drupalize.me/tutorial/use-configuration-entities-modules-settings-form), we'll use these default configuration entities in the *Transcode profile* module settings form.

## Further your understanding

- Explore the [abstract class `ConfigEntityBase`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Config%21Entity%21ConfigEntityBase.php/class/ConfigEntityBase/) and the [interface `ConfigEntityInterface`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Config%21Entity%21ConfigEntityInterface.php/interface/ConfigEntityInterface/). What other methods might you override in your custom configuration entity? What methods might you add?

## Additional resources

- [abstract class `ConfigEntityBase`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Config%21Entity%21ConfigEntityBase.php/class/ConfigEntityBase/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Create a Configuration Entity Type](/tutorial/create-configuration-entity-type?p=2476)

Next
[Use Configuration Entities in a Module's Settings Form](/tutorial/use-configuration-entities-modules-settings-form?p=2476)

Clear History

Ask Drupalize.Me AI

close