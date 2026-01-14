---
title: "Use Simple Configuration in a Form"
url: "https://drupalize.me/tutorial/use-simple-configuration-form?p=2476"
guide: "[[work-data-modules]]"
order: 25
---

# Use Simple Configuration in a Form

## Content

Now that we have some default simple configuration stored in a settings YAML file, let's utilize it in a form that our site administrators can use to update those values. We'll make use of some services and methods in Drupal's Configuration API in order to retrieve, update, and save simple configuration values with a form.

## Goal

Retrieve configuration data for use in a form using Drupal's `config.factory` service.

## Prerequisites

- [Configuration Data Types](https://drupalize.me/tutorial/configuration-data-types)
- [Create a Settings Form in a Module](https://drupalize.me/tutorial/create-settings-form-module) (Walk through this tutorial before continuing, in order to have a code starting point.)

Sprout Video

## Retrieve a configuration object

To retrieve a configuration object that we can update with user-submitted values, we'll use Drupal's `config.factory` service. We can either make a static call or extend a class that already provides access.

If you're not extending a class that already provides access to Drupal's `config.factory` service, you can make a static call to `getEditable()` on Drupal's `config.factory` service.

Assuming a configuration file named `transcode_profile.adminsettings.yml` (which we created in [Create a Settings Form in a Module](https://drupalize.me/tutorial/create-settings-form-module)) consisting of:

```
profile_name: "1920x1080 h264"
enable_transcoding: 1
```

Here's how you could make a static call to `config.factory` to retrieve the editable `transcode_profile.adminsettings` configuration object. We need the editable version because we want to be able to update the configuration values using our form.

```
$config = \Drupal::service('config.factory')->getEditable('transcode_profile.adminsettings');
```

Then, in your form's `submitForm()` method in your custom form class, call the `config.factory`'s' `set()` and `save()` functions to update the configuration object. Here's how that would look:

```
public function submitForm(array &$form, FormStateInterface $form_state) {
  parent::submitForm($form, $form_state);

  $config = \Drupal::service('config.factory')->getEditable('transcode_profile.adminsettings');

  $config->set('profile_name', $form_state->getValue('profile_name'));
  $config->set('enable_transcoding', $form_state->getValue('enable_transcoding'));

  // Save the configuration.
  $config->save();
}
```

In practice, however, you will most likely want to extend Drupal's `ConfigFormBase` class, which provides direct access to the `config.factory` service.

## A base class for system configuration forms

The Drupal class `ConfigFormBase` is "a base class for implementing system configuration forms."

You can find documentation for `ConfigFormBase` on api.drupal.org [here](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Form%21ConfigFormBase.php/class/ConfigFormBase).

## Get the editable configuration object

We can use the `config()` method to retrieve an editable configuration object for use in our form.

In order for `config()` to return an editable config object, we need to implement `getEditableConfigNames()` in our form class and return an array of the names of the configuration object we want:

```
protected function getEditableConfigNames() {
    return [
      'transcode_profile.adminsettings',
    ];
  }
```

With that, we can assign `$this->config('transcode_profile.adminsettings')` to a variable and use it in our form to load default field values.

For example, in `AdminSettingsForm::buildForm()`:

```
$config = $this->config('transcode_profile.adminsettings');
```

Now we're ready to load in default values of our configuration's properties to use in our form.

## Load default form values from configuration

Since our class extends `ConfigFormBase`, which in turn extends `FormBase`, we have access to the following methods which we will use to build, validate, and save our configuration settings form.

| Name | Description |
| --- | --- |
| `public function ConfigFormBase::buildForm` | Form constructor. Overrides `FormInterface::buildForm` |
| `public function FormBase::validateForm` | Form validation handler. Overrides `FormInterface::validateForm` |
| `public function ConfigFormBase::submitForm` | Form submission handler. Overrides `FormInterface::submitForm` |

Additionally, in our class we need to implement `getFormId()` to fulfill the `FormInterface` that the abstract class `FormBase` implements. This enables us to give our form an ID.

To get the default values for our `profile_name` and `enable_transcoding` fields, we'll call `get()` on the `$config` variable we created above.

Here is our form class, extending `ConfigFormBase` and retrieving, updating, and saving our simple configuration data, `transcode_profile.adminsettings`.

```
<?php
namespace Drupal\transcode_profile\Form;
use Drupal\Core\Form\ConfigFormBase;
use Drupal\Core\Form\FormStateInterface;
/**
 * Class AdminSettingsForm.
 *
 * @package Drupal\transcode_profile\Form
 */
class AdminSettingsForm extends ConfigFormBase {
  /**
   * {@inheritdoc}
   */
  protected function getEditableConfigNames() {
    return [
      'transcode_profile.adminsettings',
    ];
  }
  /**
   * {@inheritdoc}
   */
  public function getFormId() {
    return 'admin_settings_form';
  }
  /**
   * {@inheritdoc}
   */
  public function buildForm(array $form, FormStateInterface $form_state) {
    $config = $this->config('transcode_profile.adminsettings');
    $form['profile_name'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Profile Name'),
      '#description' => $this->t('Video transcode profile name'),
      '#maxlength' => 64,
      '#size' => 64,
      '#default_value' => $config->get('profile_name'),
    ];
    $form['enable_transcoding'] = [
      '#type' => 'checkbox',
      '#title' => $this->t('Enable transcoding'),
      '#description' => $this->t('Enables video transcoding'),
      '#default_value' => $config->get('enable_transcoding'),
    ];
    return parent::buildForm($form, $form_state);
  }
  /**
   * {@inheritdoc}
   */
  public function validateForm(array &$form, FormStateInterface $form_state) {
    parent::validateForm($form, $form_state);
  }
  /**
   * {@inheritdoc}
   */
  public function submitForm(array &$form, FormStateInterface $form_state) {
    parent::submitForm($form, $form_state);
    $this->config('transcode_profile.adminsettings')
      ->set('profile_name', $form_state->getValue('profile_name'))
      ->set('enable_transcoding', $form_state->getValue('enable_transcoding'))
      ->save();
  }
}
```

## Recap

In this tutorial, we learned how to retrieve simple configuration data using either a static call to Drupal's `config.factory` service or through direct access via extending `ConfigFormBase`. We then used this configuration data in our form's default values and updated our form's `submitForm()` method to update and save the configuration with user-submitted form values.

## Further your understanding

- Find other examples of this pattern of retrieving an editable configuration object by implementing `getEditableConfigNames()` and `config()` by exploring [some of these 31 files that declare their use of `ConfigFormBase`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Form%21ConfigFormBase.php/class/uses/ConfigFormBase/). [AccountSettingsForm.php](https://api.drupal.org/api/drupal/core%21modules%21user%21src%21AccountSettingsForm.php/11.x) is a good place to start.

## Additional resources

- [abstract class ConfigFormBase](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Form%21ConfigFormBase.php/class/ConfigFormBase) (api.drupal.org)
- [class Config](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Config%21Config.php/class/Config) (api.drupal.org)
- [Configuration API](https://api.drupal.org/api/drupal/core%21core.api.php/group/config_api) (api.drupal.org)
- [Discover and Use Existing Services](https://drupalize.me/tutorial/discover-and-use-existing-services) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Create a Settings Form in a Module](/tutorial/create-settings-form-module?p=2476)

Next
[Create a Configuration Entity Type](/tutorial/create-configuration-entity-type?p=2476)

Clear History

Ask Drupalize.Me AI

close