---
title: "Use Configuration Entities in a Module's Settings Form"
url: "https://drupalize.me/tutorial/use-configuration-entities-modules-settings-form?p=2476"
guide: "[[work-data-modules]]"
---

# Use Configuration Entities in a Module's Settings Form

## Content

While we've already created configuration entity forms for creating, editing, and deleting configuration entities, in this tutorial, you'll learn how to use configuration entity data in the context of a module's settings (configuration) form. We'll refactor the [module settings form we created previously](https://drupalize.me/tutorial/create-settings-form-module) and replace the textfield form element with a dropdown select list of our custom *video preset* configuration entities [we created in another tutorial](https://drupalize.me/tutorial/create-configuration-entity-type).

By the end of this tutorial, you should be able to:

- Load configuration entities using an injected `entity_type.manager` service
- Update the module settings form to use a select list of configuration entities
- Save the settings form with the refactored field

## Goal

Load and list configuration entities into a select list in our module's settings form.

## Prerequisites

- [Create a Settings Form in a Module](https://drupalize.me/tutorial/create-settings-form-module)
- [Default Configuration in a Module](https://drupalize.me/tutorial/default-configuration-module)
- [Create a Configuration Entity Type](https://drupalize.me/tutorial/create-configuration-entity-type)
- [Add Properties to a Configuration Entity Type](https://drupalize.me/tutorial/add-properties-configuration-entity-type)
- [Concept: Services and the Container](https://drupalize.me/tutorial/concept-services-and-container)
- [Concept: Dependency Injection](https://drupalize.me/tutorial/concept-dependency-injection)

## Where we left off

This is what the Transcode profile settings form currently looks like:

Image

![The Transcode profile settings form currently](../assets/images/transcode-profile-settings-form-before.png)

Currently, the module settings form is getting an editable simple configuration object whose values can be viewed and updated using this form.

## Refactor the Transcode profile settings form

We're going to refactor *src/Form/SettingsForm.php* so that it updates the `transcode_profile.settings` configuration object to store a video preset ID which corresponds to the ID of a video preset configuration entity stored on our site.

To do this we'll change the `profile_name` field to `video_preset_id` and change the form render element `#type` from `textfield` to `select`. To retrieve a list of stored video preset configuration entities to populate options in the select element, we can inject and use the `entity_type.manager` service, a key service of Drupal's Entity API.

**Open *modules/custom/transcode\_profile/src/Form/SettingsForm.php* in your IDE** and let's get started.

### Inject the required services into `SettingsForm`

To use the `entity_type.manager` service in our form we need to override the `__construct()` and `create()` functions in the `SettingsForm` class, and add a new properties for each service.

```
use Drupal\Core\Config\ConfigFactoryInterface;
use Drupal\Core\Config\TypedConfigManagerInterface;
use Drupal\Core\Entity\EntityTypeManager;
use Drupal\Core\Form\ConfigFormBase;
use Drupal\Core\Form\FormStateInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;

class SettingsForm extends ConfigFormBase {
  /**
   * The entity type manager.
   *
   * @var \Drupal\Core\Entity\EntityTypeManager
   */
  protected $entityTypeManager;

  /**
   * SettingsForm constructor.
   *
   * @param \Drupal\Core\Config\ConfigFactoryInterface $config_factory
   *   The config factory service.
   * @param \Drupal\Core\Config\TypedConfigManagerInterface $typedConfigManager
   *   The typed config manager.
   * @param \Drupal\Core\Entity\EntityTypeManagerInterface $entity_type_manager
   *   The entity type manager.
   */
  public function __construct(ConfigFactoryInterface $config_factory, TypedConfigManagerInterface $typedConfigManager, EntityTypeManagerInterface $entity_type_manager) {
    // Call the parent constructor, with the required services.
    parent::__construct($config_factory, $typedConfigManager);
    // Store the entity type manager service so we can use it later.
    $this->entityTypeManager = $entity_type_manager;
  }

  /**
   * {@inheritdoc}
   */
  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('config.factory'),
      $container->get('config.typed'),
      $container->get('entity_type.manager')
    );
  }
```

### Update the module's default settings object

In the [previous tutorial](https://drupalize.me/tutorial/add-properties-configuration-entity-type), we used the `VideoPreset` entity form to create two *video preset* configuration entities. We then exported our site's configuration and copied values from the corresponding exported YAML files into two new default configuration files in *transcode\_profile/config/install*. This ensures that we have at least 2 video preset configuration entities listed as options in the select element in our settings form.

But we also need to update *transcode\_profile/config/install/transcode\_profile.settings.yml* to use an ID of a video preset config entity instead of a `profile_name` string.

Update *transcode\_profile/config/install/transcode\_profile.settings.yml* so that it looks like this:

```
video_preset_id: 800x600
enable_transcoding: 1
```

The value of `video_preset_id` matches the `id` key of the default configuration object (*transcode\_profile/config/install/transcode\_profile.video\_preset.800x600.yml*):

```
langcode: en
status: true
dependencies: {  }
id: 800x600
label: 800x600
description: ''
codec: h264
```

### Create an array to store options

Locate the `buildForm()` method in our module's *src/Form/SettingsForm.php*. At the top of this method, retrieve the `video_preset` configuration entities from storage using the `entity_type.manager` service which our class' property `entityTypeManager` references and store them in a variable named `$video_presets`.

```
$video_presets = $this->entityTypeManager->getStorage('video_preset')->loadMultiple();
```

Create a new variable to store the options for the select form element.

```
$video_preset_options = [];
```

Loop over and populate this array, setting the key of the array element to the `id` of the *video\_preset* and the value to the `label`:

```
foreach($video_presets as $video_preset) {
  $video_preset_options[$video_preset->id()] = $video_preset->label();
}
```

### Refactor the `profile_name` form element

Refactor the `profile_name` form element to make the following changes:

- Rename the element to `$form['video_preset']`
- Change the `#type` from `textfield` to `select`.
- Remove the `#size` and `#maxlength` properties.
- Change the `#default_value` to `$config->get('video_preset_id')` (the renamed key in *transcode\_profile/config/install/transcode\_profile.settings.yml*)
- Add an `#options` property and set it equal to `$video_preset_options` we created in the previous step.

Our `buildForm()` method now looks like this, incorporating the changes we made in this and the previous step:

```
  /**
   * {@inheritdoc}
   */
  public function buildForm(array $form, FormStateInterface $form_state): array {
    $video_presets = $this->entityTypeManager->getStorage('video_preset')->loadMultiple();
    $video_preset_options = [];
    foreach ($video_presets as $video_preset) {
      $video_preset_options[$video_preset->id()] = $video_preset->label();
    }

    $form['video_preset'] = [
      '#type' => 'select',
      '#title' => $this->t('Video preset'),
      '#default_value' => $this->config('transcode_profile.settings')->get('video_preset_id'),
      '#options' => $video_preset_options,
    ];
    $form['enable_transcoding'] = [
      '#type' => 'checkbox',
      '#title' => $this->t('Enable transcoding?'),
      '#default_value' => $this->config('transcode_profile.settings')->get('enable_transcoding'),
    ];

    return parent::buildForm($form, $form_state);
  }
```

### Update `submitForm()` to the refactored field name

In our refactoring, we updated the form field key to `$form['video_preset']` and the configuration settings key to `video_preset_id`, so we need to reflect those changes in the `submitForm()` method.

Update the `submitForm()` method so that `video_preset_id`. The method should now look like this:

```
public function submitForm(array &$form, FormStateInterface $form_state) {
  parent::submitForm($form, $form_state);

  $this->config('transcode_profile.settings')
    ->set('video_preset_id', $form_state->getValue('video_preset'))
    ->set('enable_transcoding', $form_state->getValue('enable_transcoding'))
    ->save();
}
```

The form will now update and save our `transcode_profile.settings` configuration object. Here's what *src/Form/SettingsForm.php* should look like now:

```
<?php

declare(strict_types=1);

namespace Drupal\transcode_profile\Form;

use Drupal\Core\Config\ConfigFactoryInterface;
use Drupal\Core\Config\TypedConfigManagerInterface;
use Drupal\Core\Entity\EntityTypeManager;
use Drupal\Core\Form\ConfigFormBase;
use Drupal\Core\Form\FormStateInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;

class SettingsForm extends ConfigFormBase {
  /**
   * The entity type manager.
   *
   * @var \Drupal\Core\Entity\EntityTypeManager
   */
  protected $entityTypeManager;

  /**
   * SettingsForm constructor.
   *
   * @param \Drupal\Core\Config\ConfigFactoryInterface $config_factory
   *   The config factory service.
   * @param \Drupal\Core\Config\TypedConfigManagerInterface $typedConfigManager
   *   The typed config manager.
   * @param \Drupal\Core\Entity\EntityTypeManagerInterface $entity_type_manager
   *   The entity type manager.
   */
  public function __construct(ConfigFactoryInterface $config_factory, TypedConfigManagerInterface $typedConfigManager, EntityTypeManagerInterface $entity_type_manager) {
    // Call the parent constructor, with the required services.
    parent::__construct($config_factory, $typedConfigManager);
    // Store the entity type manager service so we can use it later.
    $this->entityTypeManager = $entity_type_manager;
  }

  /**
   * {@inheritdoc}
   */
  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('config.factory'),
      $container->get('config.typed'),
      $container->get('entity_type.manager')
    );
  }

  /**
   * {@inheritdoc}
   */
  public function getFormId(): string {
    return 'transcode_profile_settings';
  }

  /**
   * {@inheritdoc}
   */
  protected function getEditableConfigNames(): array {
    return ['transcode_profile.settings'];
  }

  /**
   * {@inheritdoc}
   */
  public function buildForm(array $form, FormStateInterface $form_state): array {
    $video_presets = $this->entityTypeManager->getStorage('video_preset')->loadMultiple();
    $video_preset_options = [];
    foreach ($video_presets as $video_preset) {
      $video_preset_options[$video_preset->id()] = $video_preset->label();
    }

    $form['video_preset'] = [
      '#type' => 'select',
      '#title' => $this->t('Video preset'),
      '#default_value' => $this->config('transcode_profile.settings')->get('video_preset_id'),
      '#options' => $video_preset_options,
    ];
    $form['enable_transcoding'] = [
      '#type' => 'checkbox',
      '#title' => $this->t('Enable transcoding?'),
      '#default_value' => $this->config('transcode_profile.settings')->get('enable_transcoding'),
    ];

    return parent::buildForm($form, $form_state);
  }

  /**
   * {@inheritdoc}
   */
  public function submitForm(array &$form, FormStateInterface $form_state) {
    parent::submitForm($form, $form_state);

    $this->config('transcode_profile.settings')
      ->set('video_preset_id', $form_state->getValue('video_preset'))
      ->set('enable_transcoding', $form_state->getValue('enable_transcoding'))
      ->save();
  }

}
```

### Reset module configuration to defaults

Let's test it out.

To ensure our default configuration is loaded properly, uninstall and install *transcode\_profile* module.

```
drush pm-uninstall transcode_profile
drush pm-install transcode_profile
```

### Test the form

Using the *Manage* menu, go to *Configuration* > *Media* > *Transcode profile settings* (*admin/config/media/transcode\_profile/settings*). The *Video preset* select field option should be set to `800x600`. Select `1024x768` and click the **Save** button. The Video preset field should now display the value `1024x768`. If the value didn't update, re-check the `submitForm()` method.

Image

![The Transcode profile settings form after being updated.](../assets/images/transcode-profile-settings-using-video-presets.png)

You can check that the settings configuration object value is updated by the form using Drush.

```
drush config:get transcode_profile.settings

_core:
  default_config_hash: QEbDimEi_f_8TtuvZNJrKAyFYWa0GXf2gIR-wPRGB3c
enable_transcoding: true
video_preset_id: 1024x768
```

Return to the form in the browser, update a value and run `drush config:get transcode_profile.settings` again to verify that the values have been updated as expected.

## Recap

In this tutorial, we refactored the *Transcode profile* module settings configuration object and settings form to point to Video preset configuration entities. We updated *transcode\_profile/config/install/transcode\_profile.settings.yml* and changed the `profile_name` key to `video_preset_id` and set the value to `800x600`, which corresponds to the `id` property of one of our default Video preset configuration entities, also stored in our module's *config/install* directory. We updated our module's *src/Form/SettingsForm.php* to inject the entity\_type.manager service so that we could retrieve a list of video preset configuration entities to populate the options of a select list field in our form. Then we refactored both the `buildForm()` and `submitForm()` methods so that the `transcode_profile.settings` configuration object would be loaded and saved correctly with our changes.

## Further your understanding

- Can you figure out how to provide radio buttons instead of a dropdown select list for the Transcode Profile settings form? (See the [Form API reference](https://api.drupal.org/api/drupal/elements) for help.)

## Additional resources

- [EntityTypeManager](https://api.drupal.org/api/drupal/core!lib!Drupal.php/function/Drupal%3A%3AentityTypeManager) class (api.drupal.org)
- [Configuration API](https://api.drupal.org/api/drupal/core%21core.api.php/group/config_api/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add Properties to a Configuration Entity Type](/tutorial/add-properties-configuration-entity-type?p=2476)

Clear History

Ask Drupalize.Me AI

close