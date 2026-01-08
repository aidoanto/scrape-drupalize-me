---
title: "Define a Custom Views Style Plugin"
url: "https://drupalize.me/tutorial/define-custom-views-style-plugin?p=2939"
guide: "[[views-drupal]]"
---

# Define a Custom Views Style Plugin

## Content

Style plugins are responsible for determining how to output a set of rows. Individual rows are rendered by row plugins. Drupal core provides style plugins that include grid, HTML list, table, and unordered list styles. If you need to render the results in a different way, for example as tabs or accordions, or have special markup based on your project requirements, you may want to write a custom style plugin for Views. The advantage of this approach versus overriding the templates in a theme is that you may reuse this plugin in different views throughout the site, or even on different sites.

In this tutorial we'll:

- Learn how to create a custom Views style plugin and render output in the form of an accordion using the HTML5 `<details>` element.
- Demonstrate how to use a custom style plugin when building a view.

By the end of this tutorial you should know how to declare custom Views style plugins.

## Goal

Build a Views style plugin that renders the output as an accordion, with one accordion element per row.

## Prerequisites

- [Overview: Views Plugins](https://drupalize.me/tutorial/overview-views-plugins)
- [Implement a Plugin Using PHP Attributes](https://drupalize.me/tutorial/implement-plugin-using-php-attributes)

## Set up

This tutorial assumes that your site has an *Article* content type, though it should work with any content that Views can list.

This also assumes you've already defined a module named *news*, or that you're adding this code to another existing module, and that the module is enabled.

## Follow these steps

### Define a style plugin

Style plugins live in the `Plugin/Views/style` PRS-4 sub-namespace, and use `\Drupal\views\Attribute\ViewsStyle` attributes. Note that directory names are case-sensitive. Your final directory structure may look like the following:

```
news
├── news.info.yml
└── src
    └── Plugin
          └── views
                └── style
                      └── AccordionViewsStyle.php
```

### Define the plugin attributes and class

In your module, create the file *src/Plugin/views/style/AccordionViewsStyle.php* file and add the following to it:

```
namespace Drupal\news\Plugin\views\style;

use Drupal\core\form\FormStateInterface;
use Drupal\Core\StringTranslation\TranslatableMarkup;
use Drupal\views\Attribute\ViewsStyle;
use Drupal\views\Plugin\views\style\StylePluginBase;

/**
 * Style plugin to render rows as accordions.
 *
 * @ingroup views_style_plugins
 */
#[ViewsStyle(
  id: "accordion",
  title: new TranslatableMarkup("Accordion"),
  help: new TranslatableMarkup("Render rows as accordions"),
  theme: "views_view_accordion",
  display_types: ["normal"]
)]
class AccordionViewsStyle extends StylePluginBase {
  /**
   * {@inheritdoc}
   */
  protected $usesRowPlugin = TRUE;

  /**
   * Does the style plugin support custom css class for the rows.
   *
   * @var bool
   */
  protected $usesRowClass = TRUE;

  /**
   * Set default options.
   */
  protected function defineOptions() {
    $options = parent::defineOptions();
    $options['summary_text'] = ['default' => ''];
    return $options;
  }

  /**
   * Style options form.
   */
  public function buildOptionsForm(&$form, FormStateInterface $form_state) {
    parent::buildOptionsForm($form, $form_state);
    $form['summary_text'] = [
      '#title' => $this->t('Summary text'),
      '#description' => $this->t('Text to appear in the summary, leave blank if you don\'t want any text to appear.'),
      '#type' => 'textfield',
      '#size' => '30',
      '#default_value' => $this->options['summary_text'],
    ];
  }

}
```

Your `AccordionViewsStyle` class will need to have an `ViewsStyle` attribute to tell Views about your style plugin definition. It may also contain an optional `@ingroup` property for documentation purposes.

The `ViewsStyle` attribute contains the following properties:

- *id*: The unique ID of your custom plugin
- *title* and *help*: Text that is displayed in the Views UI for site builders
- *theme*: Defines the template file used to generate the HTML output with the *.html.twig* extension excluded. It's similar to a [theme hook suggestion](https://drupalize.me/tutorial/what-are-template-files).
- *display\_types*: The type(s) of the displays the plugin can be used with. The value *normal* means that the plugin can be used with all display types. Other possible values that are available in Drupal core are: *feed*, *block*, *page*, and *attachment*.

In the `AccordionViewsStyle` we override the `$usesRowPlugin` and `$usesRowClass` variables to change their settings. We also define two methods: `defineOptions()`, and `buildOptionsForm()`.

- `defineOptions()`: This method defines options that will be exposed in the Views UI to site builders to customize the style's output. Aside from the parent options, we defined a custom option to set the text used as the clickable `<summary>` element that toggles the accordion `<details>` element.
- `buildOptionsForm()`: This method provides a form that allows editors to customize style plugin options. We need to add form fields for each to options we added in `defineOptions()`. In this case we add a text field that will store custom summary text configured by the user.

### Implement `hook_theme()` and a preprocess function

In the attributes for the style plugin, we identified that it will be using `views_view_accordion` as the theme implementation. We need to tell Drupal about this new theme hook using `hook_theme()`. We also need to provide a [preprocess function](https://drupalize.me/tutorial/what-are-preprocess-functions) that will form an array of variables out of the view results. These variables will be available in the template file for the plugin.

In the root of the `news` module, create the *news.module* file (if you don't have one already) and add the following code:

```
/**
 * Implements hook_theme().
 */
function news_theme($existing, $type, $theme, $path) {
  \Drupal::moduleHandler()->loadInclude('news', 'inc', 'news.theme');
  return [
    'views_view_accordion' => [
          'file' => 'news.theme.inc',
    ],
  ];
}
```

In the code above we implement `hook_theme()`. In our implementation we load an include file, *news.theme.inc*, that will hold the preprocess function implementation. It will also return an array with a key that matches the name of the theme hook specified in the plugin attribute's *theme* property.

Next, create the file *news.theme.inc* in the root of *news* module with the following code:

```
use Drupal\Core\Template\Attribute;

/**
 * Prepares variables for Views unformatted rows templates.
 *
 * Default template: views-view-unformatted.html.twig.
 *
 * @param array $variables
 *   An associative array containing:
 *   - view: The view object.
 *   - rows: An array of row items. Each row is an array of content.
 */
function template_preprocess_views_view_accordion(&$variables) {
  $view = $variables['view'];
  $rows = $variables['rows'];
  $style = $view->style_plugin;
  $options = $style->options;
  $variables['default_row_class'] = !empty($options['default_row_class']);
  foreach ($rows as $id => $row) {
    $variables['rows'][$id] = [];
    $variables['rows'][$id]['content'] = $row;
    $variables['rows'][$id]['title'] = $options['summary_text'];
    $variables['rows'][$id]['attributes'] = new Attribute();
    if ($row_class = $view->style_plugin->getRowClass($id)) {
      $variables['rows'][$id]['attributes']->addClass($row_class);
    }
  }
}
```

Here we define the function `template_preprocess_views_view_accordion()`. The name of the function follows the pattern `template_preprocess_{theme_attribute_property_value}`, where `{theme_attribute_property_value}` matches the value specified in the *theme* property of the attribute on the style plugin. This works the same as a preprocess function in a theme, except in modules it's common to use `template_` as the prefix rather than `THEMENAME_`. This ensures the preprocess function will be executed regardless of what theme is used.

In this function we loop over the rows of data returned by Views and build an array of variables that will be available in our Twig template file. This isn't required, as the data already exists in `$variables['row']`, but it makes our template file cleaner.

### Create a Twig template file

Next, add a template file. Template files need to be located in the *templates* sub-directory of the module. In the root of *news* module, create a new folder called *templates* and add a file named *views-view-accordion.html.twig*. Note that the name of the file matches the *theme* property we defined in the attribute, and in the `hook_theme()` implementation, but the underscores (`_`) have been replaced with hyphens (`-`).

The content of the Twig template file may look something like the following:

```
{#
/**
 * Default theme implementation for Views accordion.
 *
 * @ingroup themeable
 */
#}
{% if title %}
  <h3>{{ title }}</h3>
{% endif %}
{% for row in rows %}
  <details {{ row.attributes }}>
    <summary>{{ row.title|t }}</summary>
    {{- row.content -}}
  </details>
{% endfor %}
```

Here we check if the display has a `title` to display (this is the content of the summary text option in our style plugin). Then we loop over each row and create a `<details>` element with its content.

In this example we don't rely on any CSS or JavaScript libraries to provide accordion functionality. We use the HTML5 *details* element instead. However, if your style plugin needs additional styling you can:

- [Define an Asset Library](https://drupalize.me/tutorial/define-asset-library)
- Then [attach it to the template](https://drupalize.me/tutorial/attach-asset-library) using `{{ attach_library('mymodule/mylibrary') }}`
- Or attach it to the `$variables` inside the preprocess function

### Create a view and test it out

Once you've completed your code you'll need to [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache). Then using the Views UI build a view of *Articles* with a block display limited to 5 items. In the format section you should see the custom option we just created; select it.

Press on *settings* next to it and update the configuration as desired. Alter other view configurations to match the requirements of your project and place the block somewhere on your website.

Your view should look something like the screenshot below:

Image

![Screenshot of news view using accordion style plugin](/sites/default/files/styles/max_800w/public/tutorials/images/accordion_view.png?itok=0rRVIW4I)

Scroll down to the preview area, and you should see your news items being rendered as accordions:

Image

![Screenshot of news view preview using accordion style plugin](/sites/default/files/styles/max_800w/public/tutorials/images/accordion_view_preview.png?itok=kmI4zp59)

## Recap

In this tutorial we created a custom Views style plugin that renders results as accordions. This required creating the `AccordionViewsStyle` class with an `ViewsStyle` attribute, as well as an implementation of `hook_theme()` and a corresponding preprocess function to generate the desired HTML output in a way that can be overridden by a theme developer.

## Further your understanding

- We exposed a text input to specify the summary text for accordions. How could you modify this to allow users to choose a field whose value is used for the `<summary>` element instead?
- What other configuration options could be exposed? How would you go about adding them?
- How would you override the plugin's HTML output from a theme?

## Additional resources

- [Hook\_theme documentation](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Render!theme.api.php/function/hook_theme/) (api.drupal.org)
- [Views style plugins documentation](https://api.drupal.org/api/drupal/core!modules!views!src!Plugin!views!style!StylePluginBase.php/group/views_style_plugins/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Define a Custom Views Access Plugin](/tutorial/define-custom-views-access-plugin?p=2939)

Clear History

Ask Drupalize.Me AI

close