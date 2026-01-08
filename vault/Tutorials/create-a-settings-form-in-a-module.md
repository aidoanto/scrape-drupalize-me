---
title: "Create a Settings Form in a Module"
url: "https://drupalize.me/tutorial/create-settings-form-module?p=2476"
guide: "[[work-data-modules]]"
---

# Create a Settings Form in a Module

## Content

When you are developing a module in Drupal, you can make certain functionality user-configurable. You can see this on *Extend* (*admin/modules*) in Drupal's administrative UI by looking for the *Configure* link near the module's description. To accomplish this, your module needs to define default settings in *config/install/transcode\_profile.settings.yml*, create a settings form that will read those settings as the values for corresponding form fields, and update the settings when the form is submitted with updated values.

In this tutorial, we'll create a settings form that will be used as the module's *Configure* link in the Extend UI, as well as a menu link in an appropriate place in the administrative area. We'll use [Drush](https://drupalize.me/topic/drush), a command-line utility for Drupal, to speed up the process. We'll also create a default settings YAML file so that the settings form has something to read and update.

By the end of this tutorial, you should be able to get a configuration form up and running inside a custom module that will read and update a configuration object's values.

## Goal

Create a configuration form that will read and update a module's settings.

## Prerequisites

- [Install Drupal Locally with DDEV](https://drupalize.me/tutorial/install-drupal-locally-ddev)
- [Provide Initial Settings with Simple Configuration](https://drupalize.me/tutorial/provide-initial-settings-simple-configuration)
- [Form API Overview](https://drupalize.me/tutorial/form-api-overview)

**Note:** This skill is also covered in the [Drupal Module Developer Guide](https://drupalize.me/guide/drupal-module-developer-guide), created for newcomers to module development in Drupal, in the tutorial, [Create a Settings Form for the Anytown Module](https://drupalize.me/tutorial/create-settings-form-anytown-module).

## Set up module and default settings

If necessary, generate a custom module using Drush (`drush generate module`). For this tutorial, we'll use an example module called `transcode_profile`.

Inside the module, [if you haven't already](https://drupalize.me/tutorial/provide-initial-settings-simple-configuration), create the file: *config/install/transcode\_profile.settings.yml* with the following contents:

```
profile_name: '1920x1080 h264'
enable_transcoding: 1
```

## Create a new configuration form and menu link

Let's use the Drush command, `drush generate form:config` to scaffold a settings form. Then, we'll update the generated files as needed. This command will scaffold a form that extends `ConfigFormBase` and add the necessary methods to read and edit a configuration object's values in a form.

### Scaffold a configuration form for a module

```
drush generate form:config
```

Default answers appear in square brackets. Hit Enter to accept the default value or enter a custom value.

| Prompt | Value | Notes |
| --- | --- | --- |
| Module machine name | **`transcode_profile`** | Enter the machine name of the module whose settings will be configured by this form. |
| Module name | **`Transcode profile`** | The regular name of the module. |
| Class | **`SettingsForm`** | The name of the PHP class for this settings form. A generic but descriptive name works fine because it will contain your module's PSR-4 namespace. |
| Create a route? | **`Yes`** | A *route* tells Drupal what code to call when a user visits a certain path. |
| Route name | **`transcode_profile.settings`** | Namespace route with the machine name of the containing module. |
| Route path | **`/admin/config/media/transcode_profile/settings`** | Using the Manage administrative menu, navigate to *Configuration* (*/admin/config/*). Select an appropriate section for your module's settings. Choose a link in that section to view the path element relative to */admin/config*. Enter the path you want to use for your module's settings form here. |
| Route title | **`Transcode profile settings`** | The title of the settings form page. |
| Route permission | **`administer site configuration`** | Enter the appropriate permission string. |
| Create menu link? | **`Yes`** | Yes. We'll need to edit this file later to add a `parent` key. |
| Link title | **`Transcode profile settings`** | The default value will be the Route title you entered previously. |
| Link description | **`Configure settings for the Transcode profile module.`** | Enter a brief description of what a user can expect to configure using this form. |

```
 The following directories and files have been created or updated:
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
 • /var/www/html/web/modules/custom/transcode_profile/transcode_profile.links.menu.yml
 • /var/www/html/web/modules/custom/transcode_profile/transcode_profile.routing.yml
 • /var/www/html/web/modules/custom/transcode_profile/config/schema/transcode_profile.schema.yml
 • /var/www/html/web/modules/custom/transcode_profile/src/Form/SettingsForm.php
```

Open the files in your IDE to see the code that was scaffolded.

### Add a `configure` key to your module's info file

1. Open your module's info file (e.g., *modules/custom/transcode\_profile/transcode\_profile.info.yml*) in your IDE.
2. At the end of the file on a new line, add the key, `configure:` and the route to the settings form as the value, for example: `configure: transcode_profile.settings`. This will give Drupal the information it needs to add a **Configure** link to the module's listing on the *Extend* (*admin/modules*).

### Edit the menu links YAML file

To add a link to the *Configuration* menu, you'll need to know the name of the route of the "parent" section. For example, we want to list Transcode profile settings under *Configuration* > *Media* (*/admin/config/media*). The parent section is "Media" and the route for *Media* is `system.admin_config_media`. (Learn more in [How to Find a Route in Drupal](https://drupalize.me/tutorial/how-find-route-drupal).)

Open *modules/custom/transcode\_profile/transcode\_profile.links.menu.yml* and add a parent key with the value, `system.admin_config_media`.

```
transcode_profile.settings:
  title: Transcode profile settings
  description: Configure settings for Transcode profile module.
  parent: system.admin_config_media
  route_name: transcode_profile.settings
  weight: 10
```

### Edit the schema file

Open the generated schema file in *modules/custom/transcode\_profile/config/schema/transcode\_profile.schema.yml*. Update it with the keys and data types from *config/install/transcode\_profile.settings.yml*:

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
```

### Add fields to the `buildForm` method

Right now the settings form contains scaffolded code only. We need to update the `SettingsForm` class and add fields that use the appropriate field type that is appropriate for updating values inside our module's settings configuration object. We'll use the schema to help us choose the appropriate field type.

Open *modules/custom/transcode\_profile/src/Form/SettingsForm.php* in your IDE. Update the `buildForm()` method and add fields using the Form API for each property of the settings object.

| Setting name | Property's data type | Form API field type (`#type`) |
| --- | --- | --- |
| `profile_name` | `string` | `textfield` |
| `enable_transcoding` | `boolean` | `checkbox` |

{data-line="33-42,69-70}

```
<?php

declare(strict_types=1);

namespace Drupal\transcode_profile\Form;

use Drupal\Core\Form\ConfigFormBase;
use Drupal\Core\Form\FormStateInterface;

/**
 * Configure Transcode profile settings for this site.
 */
final class SettingsForm extends ConfigFormBase {

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
    $form['profile_name'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Profile name'),
      '#default_value' => $this->config('transcode_profile.settings')->get('profile_name'),
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
  public function validateForm(array &$form, FormStateInterface $form_state): void {
    // @todo Validate the form here.
    // Example:
    // @code
    //   if ($form_state->getValue('example') === 'wrong') {
    //     $form_state->setErrorByName(
    //       'message',
    //       $this->t('The value is not correct.'),
    //     );
    //   }
    // @endcode
    parent::validateForm($form, $form_state);
  }

  /**
   * {@inheritdoc}
   */
  public function submitForm(array &$form, FormStateInterface $form_state): void {
    $this->config('transcode_profile.settings')
      ->set('profile_name', $form_state->getValue('profile_name'))
      ->set('enable_transcoding', $form_state->getValue('enable_transcoding'))
      ->save();
    parent::submitForm($form, $form_state);
  }

}
```

### Install the module and view the form

Install the module with Drush:

```
drush en transcode_profile
```

Using the *Manage* administration menu navigate to *Configuration* > *Media* > *Transcode profile settings* (*/admin/config/media/transcode\_profile/settings*) and verify that you can both navigate to the form successfully (that the route was correct) and that the default values were what you entered in *config/install/transcode\_profile.settings.yml*.

### Verify that the form updates the configuration object

Verify that the settings form updates the `transcode_profile.settings` configuration object using Drush.

In a terminal window, view the configuration object's property values using Drush:

```
drush config:get transcode_profile.settings

_core:
  default_config_hash: _w7QAHEoK0BZeM1cJPKCTcYpjnqC3KvVfISalZWhbGs
profile_name: '1920x1080 h264'
enable_transcoding: true
```

In your browser, return the form ((*/admin/config/media/transcode\_profile/settings*)), uncheck `Enable transcoding?`, and press **Save**.

Back in your terminal, run the `config:get` command again and verify that the value of `enable_transcoding` is now `false`.

```
drush cget transcode_profile.settings

_core:
  default_config_hash: _w7QAHEoK0BZeM1cJPKCTcYpjnqC3KvVfISalZWhbGs
profile_name: '1920x1080 h264'
enable_transcoding: false
```

If it's not working as expected, edit the `SettingsForm` class and verify that you've added the correct property names in both the `buildForm()` and `submitForm()` methods. (See the steps above for details.)

## Recap

In this tutorial, we created a settings form that can read and update a configuration object's values. We used Drush as a tool to scaffold the files we needed, then we updated the files to ensure that we included a Configure link for the module on the Extend page, a link in the Configuration menu and administrative page, default settings and a schema, a settings form with fields that corresponded to the properties in our configuration object using an appropriate field type for the type of data being stored.

## Further your understanding

- How would go about adding a property to the settings configuration object? What are all the files and places you would need to update?

## Additional resources

- [Create a Settings Form for the Anytown Module](https://drupalize.me/tutorial/create-settings-form-anytown-module) (Drupalize.Me)
- [Add a Menu Link in a Module](https://drupalize.me/tutorial/add-menu-link-module)
- [How to Find a Route in Drupal](https://drupalize.me/tutorial/how-find-route-drupal)

Downloads

[vaticliuich](/sites/default/files/vaticliuich)

[jiphejislikuphechoprebrefrifrevus](/sites/default/files/jiphejislikuphechoprebrefrifrevus)

[westicleslulustibrakashamuswibristethuliclathaprowrebruslophocrefricruwrupropashihishosiprinudranotrastatatriuiwipruthecrofrugislola](/sites/default/files/westicleslulustibrakashamuswibristethuliclathaprowrebruslophocrefricruwrupropashihishosiprinudranotrastatatriuiwipruthecrofrugislola)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Provide Initial Settings with Simple Configuration](/tutorial/provide-initial-settings-simple-configuration?p=2476)

Next
[Use Simple Configuration in a Form](/tutorial/use-simple-configuration-form?p=2476)

Clear History

Ask Drupalize.Me AI

close