---
title: "Customize Theme Settings"
url: "https://drupalize.me/tutorial/customize-theme-settings?p=3261"
guide: "[[develop-forms-drupal]]"
order: 22
---

# Customize Theme Settings

## Content

In Drupal's *Appearance* UI, all themes get a *theme settings form*. As a theme developer, you can customize the theme settings form, enabling site administrators to have more control over the appearance of the theme.

In this tutorial, we'll show you how to add admin-configurable settings to your theme. In the process of doing this, we'll use a variety of theme and module development skills and assume you have some familiarity with using Drupal's Form API, Configuration API, and theme system (see *Prerequisites*).

By the end of this tutorial, you will be able to provide custom theme settings that an administrator can use to modify the appearance of the theme.

## Goal

Add a theme setting that allows an administrator to choose from a list of background colors for the header region.

## Prerequisites

- [Describe Your Theme with an Info File](https://drupalize.me/tutorial/describe-your-theme-info-file)
- [Add Regions to a Theme](https://drupalize.me/tutorial/add-regions-theme)
- [Define an Asset Library](https://drupalize.me/tutorial/define-asset-library)
- [Attach an Asset Library](https://drupalize.me/tutorial/attach-asset-library)
- [Theme Settings Overview](https://drupalize.me/tutorial/theme-settings-overview)
- [Change Theme Settings](https://drupalize.me/tutorial/change-theme-settings)
- [Configure Your Environment for Theme Development](https://drupalize.me/tutorial/configure-your-environment-theme-development)
- [Synchronize Configuration with the UI](https://drupalize.me/tutorial/synchronize-configuration-ui)
- [Synchronize Configuration with Drush](https://drupalize.me/tutorial/synchronize-configuration-drush)
- [Inspect Configuration with Drush](https://drupalize.me/tutorial/inspect-configuration-drush)
- [Default Configuration in a Module](https://drupalize.me/tutorial/default-configuration-module)
- [What Are Preprocess Functions?](https://drupalize.me/tutorial/what-are-preprocess-functions)
- [Add Logic with THEMENAME.theme](https://drupalize.me/tutorial/add-logic-themenametheme)
- [Form API Overview](https://drupalize.me/tutorial/form-api-overview)
- [Add Input Elements to a Form](https://drupalize.me/tutorial/add-input-elements-form)

## Contents

- [Overview: Customizing theme settings](#overview-customizing-theme-settings)
- [Add a setting to a theme](#add-a-setting-to-a-theme)
- [Define setting defaults and a schema](#define-setting-defaults-and-a-schema)
- [Apply theme settings to a theme](#apply-theme-settings-to-a-theme)

## Overview: Customizing theme settings

A *theme settings form* is special type of *settings form* in Drupal. Its purpose is to show each theme's current settings values and update settings when the value is changed upon form submission.

If you want to give site administrators more control over certain aspects of the theme, you can add custom settings with their default values in configuration files, and corresponding form fields in your theme's settings form. The core Drupal theme, Olivero, does this, which you can see in its theme settings form in the section, "Olivero Utilities".

Image

![Screenshot of Olivero Utilities in the Olivero theme settings form](../assets/images/custom-theme-settings-olivero-utilities.png)

While [modules are responsible for providing their own settings form](https://drupalize.me/tutorial/create-settings-form-module) to manage their module's configuration, installed themes are provided a [theme settings form](https://drupalize.me/tutorial/theme-settings-overview) out-of-the-box. To add settings to a theme, a theme developer can alter the default system theme settings form for a custom theme by implementing `hook_form_system_theme_settings_alter()`.

When a theme contains an implementation of [`hook_form_system_theme_settings_alter()`](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Render!theme.api.php/function/hook_form_system_theme_settings_alter) in a file named *theme-settings.php* (located in the root of the theme), Drupal will automatically find and execute this hook.

If you want to dive deeper into how and why this works:

- The API for altering the theme settings form is defined in *core/lib/Drupal/Core/Render/theme.api.php*, which you can also view on Drupal API: [theme.api.php > function hook\_form\_system\_theme\_settings\_alter](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Render!theme.api.php/function/hook_form_system_theme_settings_alter).
- The *theme-settings.php* file must have this name, as specified in [*core/modules/system/src/Form/ThemeSettingsForm.php*](https://git.drupalcode.org/project/drupal/-/blob/10.1.x/core/modules/system/src/Form/ThemeSettingsForm.php#L357).
- You can [read the code for Olivero's custom theme settings](https://git.drupalcode.org/project/drupal/-/blob/10.1.x/core/themes/olivero/theme-settings.php) in *core/themes/olivero/theme-settings.php*.

## Add a setting to a theme

Using [Olivero's *theme-settings.php* as an example](https://git.drupalcode.org/project/drupal/-/blob/10.1.x/core/themes/olivero/theme-settings.php) we can learn from, let's add a new setting to our custom theme, *icecream* which will allow administrators to choose from a pre-set list of colors for the header region. Here's an overview of the process we'll take:

1. Create a new *theme-settings.php* file in the root of our custom theme directory.
2. Using [PHP](https://drupalize.me/topic/php) and [Form API](https://drupalize.me/tutorial/form-api-overview), implement a [form alter hook](https://drupalize.me/tutorial/alter-existing-form-hookformalter) that will target our theme's settings form and add a new section and field to it.
3. Update values in the theme settings form (using the administrative UI) to save default settings for new and existing theme settings in our site's active configuration.
4. Export the theme's configuration to a YAML file.
5. Move the exported theme configuration YAML file we exported to our theme's *config/install* directory, so that the default settings are applied when the theme is installed.
6. In a preprocess function, use the new setting to add a class to the attributes array for our target region.
7. Add some CSS that sets the background-color for all possible class names.

### Set up the custom *icecream* theme

We'll be customizing settings for our custom theme, *icecream*. Inside *themes*, create the directory *icecream* and an [info file](https://drupalize.me/tutorial/describe-your-theme-info-file) named *icecream.info.yml* with the following contents:

```
# THEMENAME.info.yml file for Ice Cream example theme.
name: Ice Cream
type: theme
base theme: stable9
description: 'A great theme for warm summer days.'
package: Custom
core_version_requirement: ^9 || ^10

libraries:
  - icecream/global-styling

regions:
  header: 'Header'
  content: 'Content'
  content_bottom: 'Content (bottom)'
  primary_menu: 'Primary menu'
  banner_top: 'Banner (top)'
  banner_bottom: 'Banner (bottom)'
  footer: 'Footer'
  page_top: 'Page top'
  page_bottom: 'Page bottom'
```

Finally, define a `global-styling` asset library (*icecream.libraries.yml*) and create a corresponding CSS file (*css/global.css*).

*icecream.libraries.yml*:

```
global-styling:
  version: 1.0
  css:
    theme:
      css/global.css: {}
```

### Create the *theme-settings.php* file

In *themes/icecream*, create the PHP file, *theme-settings.php*. The filename, and its location in the root directory of your theme alongside the theme's *.info.yml* are required.

### Implement `hook_form_system_theme_settings_alter()`

In *themes/icecream/theme-settings.php*, implement `hook_form_system_theme_settings_alter()`, which is a [form alter hook](https://drupalize.me/tutorial/alter-existing-form-hookformalter) for the form, `system_theme_settings`. It should look something like the code block below. *Note:* Change instances of `Ice Cream` or `icecream` to use your theme's name, if applicable.

```
<?php

/**
 * @file
 * Functions to support Ice Cream theme settings.
 */

use Drupal\Core\Form\FormStateInterface;

/**
 * Implements hook_form_FORM_ID_alter() for system_theme_settings.
 */
function icecream_form_system_theme_settings_alter(&$form, FormStateInterface $form_state) {
  $form['icecream_settings']['icecream_colors'] = [
    '#type' => 'fieldset',
    '#title' => t('Ice Cream colors'),
  ];
  $form['icecream_settings']['icecream_colors']['site_branding_bg_color'] = [
    '#type' => 'select',
    '#title' => t('Header site branding background color'),
    '#options' => [
      'strawberry' => t('Strawberry'),
      'vanilla' => t('Vanilla'),
      'chocolate' => t('Chocolate'),
    ],
    '#default_value' => theme_get_setting('site_branding_bg_color'),
  ];
}
```

The Ice Cream theme settings form should now look like this:

Image

![Screenshot of Ice Cream settings form with new field](../assets/images/custom-theme-settings-ice-cream-altered-form.png)

A couple things to note:

- We don't need to do any extra processing to save the `site_branding_bg_color` setting value. The value is automatically saved. This is a unique feature of **settings forms** in Drupal.
- Notice that we're using `theme_get_setting()` to set the default value of this field instead of something like `$config->get('site_branding_bg_color')`. This is unique case for **theme** settings.

### Test that the correct form was altered

1. **If you've already installed the theme**, you may need to [clear caches](https://drupalize.me/tutorial/clear-drupals-cache).
2. **If you haven't yet installed the theme**, install it and then navigate to the settings form.
3. Verify that at the bottom of the form, there is a new `fieldset` labeled "Ice Cream colors" and a new dropdown (`select`) field labeled "Header site branding background color" with 3 options in the select field: "Strawberry", "Vanilla", and "Chocolate".

Before this can work, we'll need to add a schema for the setting, `site_branding_bg_color`, and set its default value.

## Define setting defaults and a schema

Theme settings and their default values are set in the theme's *config/install/THEME.settings.yml*. The settings *schema* (which defines each settings structure) lives in the theme's *config/schema/THEME.schema.yml*.

We'll use the Configuration Manager to get the contents for *icecream.settings.yml*. And then we'll grab Olivero's schema and edit it for our theme.

### Change 1 system default theme setting

On the *Appearance* page, next to the Ice Cream theme, select **Settings**, and change at least 1 setting. For example, de-select **User verification status in comments** then **Save configuration**. This will ensure that a settings file for the theme will be available when exporting configuration.

### Export single item simple configuration of theme

1. Using the *Manage* administrative menu, navigate to *Configuration* > *Development* > *Configuration synchronization* > *Export* > *Single item* (*admin/config/development/configuration/single/export*).
2. For *Configuration type*, select *Simple configuration*.
3. For *Configuration name*, select *THEME.settings*, where *THEME* is the directory name of your custom theme, for example, `icecream.settings`.
4. In the text area field labeled, *Here is your configuration:*, select and copy that text. (Notice how the corresponding filename is a caption for this field. This is the file we'll create in the next step.)

### Create a *config/install/icecream.settings.yml* file

1. Create *icecream.settings.yml* (and necessary directories) inside */themes/icecream/config/install*.
2. Paste the contents from the single item configuration export into *config/install/icecream.settings.yml*.
3. Change the `comment_user_verification` value back to `1`, to turn it on by default, when the theme is first installed.

*themes/icecream/config/install/icecream.settings.yml*:

```
features:
  node_user_picture: 1
  comment_user_picture: 1
  comment_user_verification: 1
  favicon: 1
logo:
  use_default: 1
favicon:
  use_default: 1
site_branding_bg_color: strawberry
```

The *themes/icecream/config/install/icecream.settings.yml* file defines the [default configuration](https://drupalize.me/tutorial/default-configuration-module) settings for the Ice Cream theme. The default values are applied when the theme is installed.

### Copy an existing theme's schema

To create a schema, we're going to take a shortcut and copy/paste from the core theme Olivero's theme settings schema. Which we'll edit to match our theme's settings.

Find Olivero's settings in *core/themes/olivero/config/schema/olivero.schema.yml*:

```
# Schema for the configuration files of the Olivero theme.

olivero.settings:
  type: theme_settings
  label: 'olivero settings'
  mapping:
    third_party_settings:
      type: mapping
      label: 'Third party settings'
      mapping:
        shortcut:
          type: mapping
          label: 'Shortcut'
          mapping:
            module_link:
              type: boolean
              label: 'Module Link'
    mobile_menu_all_widths:
      type: integer
      label: 'Mobile menu all widths'
    site_branding_bg_color:
      type: string
      label: 'Site branding background color'
    base_primary_color:
      type: color_hex
      label: 'Base Primary Color'
```

Copy the contents of this file.

### Create *config/schema/icecream.schema.yml*

1. Create the file *icecream.schema.yml* inside *themes/icecream/config/schema* (create the *schema* directory, too).
2. Open *icecream.schema.yml* in a code editor of your choice and paste in the contents of Olivero's *olivero.schema.yml*.
3. Update instances of "Olivero" to "Ice Cream".
4. Change `olivero.settings` to `icecream.settings`.
5. Remove everything under the top-most `mapping` list except `site_branding_bg_color`, which we'll use as a setting in our theme.

The *icecream.schema.yml* file should now look like this:

```
# Schema for the configuration files of the Ice Cream theme.

icecream.settings:
  type: theme_settings
  label: 'Ice Cream settings'
  mapping:
    site_branding_bg_color:
      type: string
      label: 'Site branding background color'
```

#### Customizing your theme settings schema

When it comes to customizing your own custom theme, for each custom setting you have in your theme, under `THEME.settings:` > `mapping`, indent 2 spaces and create a new list where the key is your theme setting name. On the next line, indent 2 spaces and define `type` and `label`, as you see in the example above. For `type` values, use a valid scalar type: `boolean`, `integer`, `float`, `string`, `uri`, or `email`.

To learn more, see the tutorial, [Configuration Data Types](https://drupalize.me/tutorial/configuration-data-types).

*Note*: The bare minimum theme settings schema file, for the `icecream` theme with no custom theme settings would be:

```
icecream.settings:
  type: theme_settings
  label: 'Ice Cream settings'
```

### Test the theme settings form

1. Let's [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) for good measure and test that our theme settings form updates the setting values as expected.
2. Using the *Manage* administrative menu, navigate to *Appearance* and click **Settings** for the *Ice Cream* theme.
3. Change a value or two; for example, de-select the box for "User verification in comments" and under "Ice Cream colors" change the **Header site branding background color** to **Vanilla**. Click **Save configuration**.
4. Using the *Manage* administrative menu, navigate to *Configuration* > *Development* > *Configuration synchronization* > *Export* > *Single item*.
5. Configuration type should be **Simple configuration**. From the **Configuration name** dropdown field, select **icecream.settings**. You should now see the new values listed in the next field, as the values that we saved in the database, or "active configuration", are now able to be exported to *icecream.settings.yml*. If you wanted, you could update *icecream.settings.yml* with the new contents here, if you wanted these values to be the new defaults.

## Apply theme settings to a theme

For theme settings to be really useful, they need to update the behavior of the theme, like changing the appearance of the site in some way.

To do this, we can use the theme setting value in a variable that is ultimately used in a template file. For example, we'll use Drupal's [Render API](https://drupalize.me/tutorial/render-api-overview) and a [preprocess function](https://drupalize.me/tutorial/what-are-preprocess-functions) to add the theme setting as a [class attribute](https://drupalize.me/tutorial/add-classes-and-html-attributes-render-arrays) that is output inside a `<div>` in the header region.

### Decide where the setting will be applied

Let's target the header region and add a class attribute set to the value of the `site_branding_bg_color` theme setting.

### Locate the template file of your target

In order to determine how we'll apply the setting, we need to locate and examine the template file that contains our target element. Then we can decide whether it's necessary to override the template file, or if we can use a preprocess function alone.

1. [Set up your local Drupal environment for theme development](https://drupalize.me/tutorial/configure-your-environment-theme-development). (At the very least, turn on Twig debug mode.)
2. Ensure that a [block is placed in the header region](https://drupalize.me/tutorial/user-guide/block-place?p=3068) of your theme; for example, place the site branding block in the header region.
3. Navigate to the home page of your site and using your browser's development tools, "Inspect element" or "View page source".
4. Search for `region--header` in the HTML source and locate the HTML for the header region in the HTML source. Your HTML will be unique to your theme and your site configuration. If you're following along and using the *icecream* theme, it'll look something like this:

```
<!-- THEME DEBUG -->
<!-- THEME HOOK: 'region' -->
<!-- FILE NAME SUGGESTIONS:
   * region--header.html.twig
   x region.html.twig
-->
<!-- BEGIN OUTPUT from 'core/themes/stable9/templates/layout/region.html.twig' -->
  <div>
```

*Note:* We have a few choices here of which "layer" of the header we want to target, and that would affect which template file and theme hook we target. We're targeting this layer because the template file already outputs `attributes` in this `<div>` tag, as we'll see in the next step.

### Examine the template file

Open the template file that's being used in a code editor. In our case, we want to use the value of our theme setting as a class attribute on the header region's container `<div>`. (At the moment we observe no attributes in this tag--it's just an empty `<div>`.)

1. Open *core/themes/stable9/templates/layout/region.html.twig*.
2. Note whether there is already an `attributes` variable in use in our target HTML element. (Hint: There is!)
3. Since there is, then we can use a preprocess function (`hook_preprocess_region`) to add a class to the attributes, and we can skip overriding the template file.

*core/themes/stable9/templates/layout/region.html.twig*:

```
{#
/**
 * @file
 * Theme override to display a region.
 *
 * Available variables:
 * - content: The content for this region, typically blocks.
 * - attributes: HTML attributes for the region <div>.
 * - region: The name of the region variable as defined in the theme's
 *   .info.yml file.
 *
 * @see template_preprocess_region()
 */
#}
{% if content %}
  <div{{ attributes }}>
    {{ content }}
  </div>
{% endif %}
```

### If necessary, override the template file

If there isn't already an `attributes` variable printed inside the target HTML element or you need a more specifically-applied template or you want to use your theme setting in some other unique way in the template, then you'll need to [override the template file](https://drupalize.me/tutorial/override-template-file) and edit it as needed.

### Implement a preprocess hook to add a new variable

Now we're ready to add a class to the attributes variable for our `region` theme hook. As we saw earlier, the Twig debug output gives us the preprocess function that affects this "layer" of the page.

```
@see template_preprocess_region()
```

We implement this hook in our theme's *icecream.theme* file, [a PHP file which contains all our theme's preprocess hook implementations](https://drupalize.me/tutorial/add-logic-themenametheme).

1. In the root of your custom theme directory, create the file *icecream.theme*, if it doesn't already exist.
2. Edit *themes/icecream/icecream.theme*. We can add a class to the attributes array like this:

```
<?php

/**
 * Implements hook_preprocess_region().
 */
function icecream_preprocess_region(&$variables) {
  if ($variables['region'] == 'header') {
    $variables['attributes']['class'][] = theme_get_setting('site_branding_bg_color');
  }
}
```

In this code:

- We targeted the header region, so that the class attribute will not get added to every region.
- We added to the class attributes array with the current value of our `site_branding_bg_color` theme setting.

Since an attribute (a class) now exists, Drupal's [Render API](https://drupalize.me/tutorial/render-api-overview) will incorporate that into the output for the class attributes of the header region.

### Clear the cache

[Clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) since we've added a new preprocess function (or if you've overridden a template file).

### Add styles for all possible class names

Our theme settings form's new custom field `site_branding_bg_color` has 3 possible values, `strawberry`, `vanilla`, and `chocolate`. Let's add those as class selectors and define styles for each of them.

1. Edit *icecream/css/global.css*, and add styles for each class (representing each possible value of your theme setting). Your styles might look something like this:

```
.vanilla {
  background-color: #FFFDD0;
}

.chocolate {
  background-color: chocolate;
}

.strawberry {
  background-color: pink;
}
```

### Test it out

1. View your site in a browser. The background color for the header region should have changed to the selected color.
2. View the page source and notice how the previously empty `<div>` tag now has a class attribute with the value of the `site_branding_bg_color` theme setting, for example `<div class="strawberry">`.
3. Change the theme setting value via the *Appearance* > Ice Cream > **Settings** page and navigate back to the site to observe whether the header region background color changed as expected.

## Recap

In this tutorial, we added a custom theme setting in our theme. We altered the system theme settings form and added a field that corresponded to the new setting. Then we added a configuration schema for the setting and default values. Finally, we decided where we would apply the setting (as a class attribute in the header region), and implemented a preprocess hook to add to the class attributes with our theme setting value.

## Further your understanding

- Explore other theme's *theme-settings.php* file and their resulting forms in *Appearance*. What can you learn from those examples?
- We used a pre-set list of colors in a `<select>` dropdown element for administrators to choose the background color. Using Olivero's theme settings form as an example, how would you go about adding a color-picker widget to a theme settings form?
- Learn more about how [themes now support post update functions](https://www.drupal.org/node/3259199), which may come in handy if you need to update your settings schema after the theme has been installed.

## Additional resources

- [Add Variables to a Template File](https://drupalize.me/tutorial/add-variables-template-file) (Drupalize.Me)
- [Override a Template File](https://drupalize.me/tutorial/override-template-file) (Drupalize.Me)
- [Classes and Attributes in Twig Templates](https://drupalize.me/tutorial/classes-and-attributes-twig-templates) (Drupalize.Me)
- [Provide Initial Settings with Simple Configuration](https://drupalize.me/tutorial/provide-initial-settings-simple-configuration) (Drupalize.Me)
- [Create advanced theme settings](https://www.drupal.org/docs/8/theming-drupal-8/creating-advanced-theme-settings) (Drupal.org)
- [API documentation for `theme_get_setting()`](https://api.drupal.org/api/drupal/core%21includes%21theme.inc/function/theme_get_setting/) (api.drupal.org)
- Change record: [Themes support post update functions](https://www.drupal.org/node/3259199) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Create a Settings Form in a Module](/tutorial/create-settings-form-module?p=3261)

Clear History

Ask Drupalize.Me AI

close