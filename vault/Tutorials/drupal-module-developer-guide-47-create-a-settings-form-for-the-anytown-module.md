---
title: "Create a Settings Form for the Anytown Module"
url: "https://drupalize.me/tutorial/create-settings-form-anytown-module?p=3242"
guide: "[[drupal-module-developer-guide]]"
order: 47
---

# Create a Settings Form for the Anytown Module

## Content

Settings forms are commonly used in Drupal modules to allow administrators to manage a module's configuration. This tutorial will guide you through creating a settings form for the Anytown weather forecast module, enabling site administrators to customize the location for weather forecasts.

In this tutorial, we'll:

- Define a new form controller for a settings form.
- Build a `$form` array with options for the settings form.
- Associate the form with a route and menu item.

By the end of this tutorial, you'll have a custom settings form that administrators can access.

## Goal

Create a settings form that will eventually allow site administrators to change the weather forecast location.

## Prerequisites

- [Overview: Drupal's Form API](https://drupalize.me/tutorial/overview-drupals-form-api)
- [Concept: Form Controllers and the Form Life Cycle](https://drupalize.me/tutorial/concept-form-controllers-and-form-life-cycle)
- [Concept: Render API](https://drupalize.me/tutorial/concept-render-api)
- Builds on work previously done in [Create a Route for the Weather Page](https://drupalize.me/tutorial/create-route-weather-page), and [Define A Menu Item](https://drupalize.me/tutorial/define-menu-item)

## Video tutorial

Sprout Video

The weather forecast service in our *anytown* module currently uses a hard-coded ZIP code. To make the module reusable, we'll enable administrators to configure the forecast location through a UI. We'll also allow them to update weather-related closures on the */weather* page. The steps include:

1. Creating a settings form accessible to users.
2. Validating user input.
3. Saving data as configuration, then using it elsewhere in the code.

Let's tackle the first part: defining the form controller and its `$form` array, then linking it to a route and a menu item. The form will include a text field for a ZIP code and a textarea field to capture information about weather-related closures.

## Create a configuration form for the Anytown module

### Create the form controller class

Create *src/Form/SettingsForm.php* in the *anytown* module with the following content:

```
<?php 

declare(strict_types=1);

namespace Drupal\anytown\Form;

use Drupal\Core\Form\ConfigFormBase;
use Drupal\Core\Form\FormStateInterface;

/**
 * Configure Anytown settings for this site.
 */
final class SettingsForm extends ConfigFormBase {

  /**
   * Name for module's configuration object.
   */
  const SETTINGS = 'anytown.settings';

  /**
   * {@inheritdoc}
   */
  public function getFormId(): string {
    return self::SETTINGS;
  }

  /**
   * {@inheritdoc}
   */
  protected function getEditableConfigNames(): array {
    return [self::SETTINGS];
  }

  /**
   * {@inheritdoc}
   */
  public function buildForm(array $form, FormStateInterface $form_state): array {
    $form['display_forecast'] = [
      '#type' => 'checkbox',
      '#title' => $this->t('Display weather forecast'),
      '#default_value' => $this->config(self::SETTINGS)->get('display_forecast'),
    ];

    $form['location'] = [
      '#type' => 'textfield',
      '#title' => $this->t('ZIP code of market'),
      '#description' => $this->t('Used to determine weekend weather forecast.'),
      '#default_value' => $this->config(self::SETTINGS)->get('location'),
      '#placeholder' => '90210',
    ];

    $form['weather_closures'] = [
      '#type' => 'textarea',
      '#title' => $this->t('Weather-related closures'),
      '#description' => $this->t('List one closure per line.'),
      '#default_value' => $this->config(self::SETTINGS)->get('weather_closures'),
    ];
    return parent::buildForm($form, $form_state);
  }

}
```

This defines a new `SettingsForm` controller that:

- Extends `Drupal\Core\Form\ConfigFormBase` to gain access to the utility methods it provides for getting and setting configuration data.
- Sets the unique form ID to `anytown.settings`. Form IDs need to be unique, and it's common to prefix the ID with the name of your module.
- Associates the form with the configuration data object named `anytown.settings`. This is part of integrating with Drupal's configuration management API which we'll cover in more detail in [Concept: Configuration API](https://drupalize.me/tutorial/concept-configuration-api).
- Defines a form in the `buildForm()` method with checkbox, textfield, and textarea form elements. The `#default_value` for each form element will be populated with any previously saved configuration data using the config factory provided by extending `ConfigFormBase` (after we add a `submitForm()` method later in this guide).

Learn more about the different form elements and using them in a `$form` array in [Form Element Reference](https://drupalize.me/tutorial/form-element-reference)

### Add a new route for the form

Edit *anytown.routing.yml* to add the `anytown.settings` route definition:

```
# Route definitions for the anytown module.

# Each route needs a unique identifier. We recommend prefixing the route name
# with the name of your module. Indented under the route name is the definition
# of the route. A routing.yml file can contain any number of routes.
anytown.weather_page:
  # The URL path where this page will be displayed. {style} represents a
  # placeholder and will be populated by whatever is entered into that position
  # of the URL. Its value is passed the controller's build method.
  path: '/weather/{style}'
  defaults:
    # Title of the page used for things like <title> tag.
    _title: 'Weather at the market'
    # Defines which method, on which class, should be called to retrieve the
    # content of the page.
    _controller: '\Drupal\anytown\Controller\WeatherPage::build'
    # Default value for {style} if it's not present.
    style: 'short'
  requirements:
    # What permissions a user needs to have in order to view this page.
    _permission: 'view weekly weather'

# Settings form route.
anytown.settings:
  path: '/admin/config/system/anytown'
  defaults:
    _title: 'Anytown Settings'
    # For form controllers use _form instead of _controller. This tells Drupal
    # to use the build, validate, submit workflow for a form.
    _form: 'Drupal\anytown\Form\SettingsForm'
  requirements:
    _permission: 'administer site configuration'
```

This creates a route named `anytown.settings` that points to the new form controller. The use of `_form` instead of `_controller` is significant because it tells Drupal to handle the page using the form builder service.

### Add a menu item for the route

To provide UI navigation, edit *anytown.links.menu.yml* to add:

```
# Menu links for the anytown module.

# Each link needs a unique name. We recommend prefixing links with the name of
# your module. A links.menu.yml file can contain any number of link definitions.
anytown.weather:
  title: Weather
  description: Check this week's weather.
  menu_name: main
  # From anytown.routing.yml.
  route_name: anytown.weather_page

anytown.settings:
  title: Anytown Settings
  parent: system.admin_config_system
  route_name: anytown.settings
  weight: 10
```

This adds a menu item that points to the Anytown Settings form. The `parent` key sets the location of the new page under the *System* section on the *Configuration* page.

### Verify the form display

[Clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) so Drupal finds your changes.

Then, in the *Manage* administration menu, navigate to *Configuration* > *System* > *Anytown Settings* (*admin/config/system/anytown*), and verify that the new form is displayed. (Settings won't be saved until [we add a submit handler](https://drupalize.me/tutorial/save-form-data-submitted-user).)

Image

![Screenshot of the Anytown Settings form](../assets/images/forms--create-settings-form.png)

## Using Drush to generate a configuration form

Now that you understand how to manually create a configuration form for a module, you can speed up the process using [Drush](https://drupalize.me/tutorial/install-drush) to scaffold the necessary files and code. Learn how in the video below:

Sprout Video

## Recap

We've created a form controller for a settings form and added form elements in the `buildForm()` method. We added a route definition for the settings form, adding our form controller's PSR-4 namespace to the `_form` key of the new route. Then we added a link to the settings form on the Configuration administrative page. The page displays the form, but the form doesn't yet create or update the `anytown.settings` configuration object.

## Further your understanding

- How would you make the ZIP code text field required?
- How could you position the settings form under the *Web services* section of the *Configuration* page?

## Additional resources

- [Define a New Form Controller and Route](https://drupalize.me/tutorial/define-new-form-controller-and-route) (Drupalize.Me)
- [Form Element Reference](https://drupalize.me/tutorial/form-element-reference) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Form Controllers and the Form Life Cycle](/tutorial/concept-form-controllers-and-form-life-cycle?p=3242)

Next
[Validate User Input for the Settings Form](/tutorial/validate-user-input-settings-form?p=3242)

Clear History

Ask Drupalize.Me AI

close