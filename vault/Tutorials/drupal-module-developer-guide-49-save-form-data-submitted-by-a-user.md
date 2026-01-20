---
title: "Save Form Data Submitted by a User"
url: "https://drupalize.me/tutorial/save-form-data-submitted-user?p=3242"
guide: "[[drupal-module-developer-guide]]"
order: 49
---

# Save Form Data Submitted by a User

## Content

The `submitForm()` method in a form controller is responsible for handling submitted data. This method can save data to the database (including updating configuration), trigger workflows based on user input, and redirect users after form processing. By the time data reaches `submitForm()`, it has been validated and is ready for use.

In this tutorial, we'll:

- Add a `submitForm()` method to the form controller.
- Save user-provided settings to the database.
- Confirm successful data submission to the user.

By the end of this tutorial, you'll understand how to implement custom submit handling logic in a form.

## Goal

Implement the `submitForm()` method in the settings form controller to save user input to the database.

## Prerequisites

- [Concept: Form Controllers and the Form Life Cycle](https://drupalize.me/tutorial/concept-form-controllers-and-form-life-cycle)
- [Create a Settings Form for the Anytown Module](https://drupalize.me/tutorial/create-settings-form-anytown-module)
- [Validate User Input for the Settings Form](https://drupalize.me/tutorial/validate-user-input-settings-form)

## Video tutorial

Sprout Video

## Handling form submissions

Now that we've [validated our form data](https://drupalize.me/tutorial/validate-user-input-settings-form), we now need to save it to the database. Then we can use it in the `WeatherPage` controller for the output of the */weather* page.

The `submitForm()` method in form controllers allows us to respond to the form's collected data. Common actions include saving information for later retrieval or initiating data-driven workflows. This tutorial will focus on saving the collected settings as configuration data and providing the user with a "success" message.

## Save the user-submitted data

### Update the form controller

Modify *src/Form/SettingsForm.php* to include a `submitForm()` method:

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
      '#title' => $this->t('Market zip-code'),
      '#description' => $this->t('Used to determine weekend weather forecast.'),
      '#default_value' => $this->config(self::SETTINGS)->get('location'),
      '#placeholder' => '90210',
    ];

    $form['weather_closures'] = [
      '#type' => 'textarea',
      '#title' => $this->t('Weather related closures'),
      '#description' => $this->t('List one closure per line.'),
      '#default_value' => $this->config(self::SETTINGS)->get('weather_closures'),
    ];
    return parent::buildForm($form, $form_state);
  }

  /**
   * {@inheritdoc}
   */
  public function validateForm(array &$form, FormStateInterface $form_state): void {
    parent::validateForm($form, $form_state);

    // Verify that the location field contains an integer and that it is 5
    // digits long.
    $location = $form_state->getValue('location');
    $value = filter_var($location, FILTER_VALIDATE_INT);
    if (!$value || strlen((string) $value) !== 5) {
      // Set an error on the specific field. This will halt form processing
      // and re-display the form with errors for the user to correct.
      $form_state->setErrorByName('location', $this->t('Invalid ZIP code'));
    }

  }

  /**
   * {@inheritdoc}
   */
  public function submitForm(array &$form, FormStateInterface $form_state) {
    $this->config(self::SETTINGS)
      ->set('display_forecast', $form_state->getValue('display_forecast'))
      ->set('location', $form_state->getValue('location'))
      ->set('weather_closures', $form_state->getValue('weather_closures'))
      ->save();

    $this->messenger()->addMessage($this->t('Anytown configuration updated.'));
  }

}
```

This new code adds the `submitForm()` method. The method takes 2 arguments:

- `$form`: Contains a definition of the form being submitted.
- `$form_state`: Contains the already validated user-supplied input, and data about the current processing state of the form.

In the submission handler, we:

- Called `$form_state->getValue()` to retrieve user input from the form's fields. The field name (e.g. `'display_forecast'`) matches the key for the field in the `$form` array from the `buildForm()` method.
- Used the configuration data factory service (available via `ConfigFormBase` which our class extends) to first load a copy of the module's current configuration, update it with new values, and save the updated configuration record. We'll go into more details about working with configuration data in [Concept: Configuration API](https://drupalize.me/tutorial/concept-configuration-api).
- Used the messenger service, accessed via `FormBase` (which `ConfigFormBase` extends), to display a success message on the page.

This implementation doesn't do it, but another common task is redirecting the user to another page. This can be accomplished via the `$form_state->setRedirect();` helper.

### Verify it works

In the *Manage* administration menu navigate to *Configuration* > *System* > *Anytown Settings*, submit the form with valid data, and observe the success message. Refreshing the page should show the saved data persisting in the form fields. This works because of the use of the `#default_value` property in the `buildForm()` method.

Example:

Image

![Screenshot of successful form submission](../assets/images/forms--handle-submit_success.png)

In [Retrieve and Update Weather Forecast Settings](https://drupalize.me/tutorial/retrieve-and-update-weather-forecast-settings) we'll make use of the saved configuration data in our `WeatherPage` controller and elsewhere.

## Recap

We've implemented a `submitForm()` method in the Anytown module's configuration form controller, enabling the saving of submitted data to the database.

## Further your understanding

- Is it secure to directly display user-supplied data from `$form_state` in the browser?
- How would you change the `SettingsForm` controller to use the `ForecastClient` service for making an API request with submitted data?

## Additional resources

- [Handle Submitted Form Data](https://drupalize.me/tutorial/handle-submitted-form-data) (Drupalize.Me)
- [Process Submitted Form Data via the Form Controller](https://drupalize.me/tutorial/process-submitted-form-data-form-controller) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Validate User Input for the Settings Form](/tutorial/validate-user-input-settings-form?p=3242)

Next
[Concept: Altering Existing Forms](/tutorial/concept-altering-existing-forms?p=3242)

Clear History

Ask Drupalize.Me AI

close