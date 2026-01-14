---
title: "Define a New Render Element Type"
url: "https://drupalize.me/tutorial/define-new-render-element-type?p=2775"
guide: "[[output-and-format-data-code]]"
order: 4
---

# Define a New Render Element Type

## Content

Modules can provide new [render element types](https://drupalize.me/tutorial/what-are-render-elements) -- a powerful way to encapsulate complex logic into a reusable component. This can help to cut down on code repetition, and allow other module developers to build on your work. In this tutorial we'll:

- Define a recipe for creating a new render element type
- Look at the code for the marquee element type from the *render\_example* module in the [Examples for Developers project](https://www.drupal.org/project/examples).

By the end of this tutorial you should be able to implement a new render element type in your own module and make use of it when defining content as part of a render array.

## Goal

Define a new `marquee` render element type that can be used via the `#type` property of a render array in order to display content in an HTML `<marquee>` tag.

## Prerequisites

- [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays)
- [What Are Render Elements?](https://drupalize.me/tutorial/what-are-render-elements)
- [Implement a Plugin Using PHP Attributes](https://drupalize.me/tutorial/implement-plugin-using-php-attributes)

## Render element type recipe

1. [Determine whether you're creating a standard render element or a form element](#kind)
2. [Choose a unique name for your render element type](#name)
3. [Create a new plugin that defines your render element type](#plugin)
4. [Optionally, add a theme hook and associated Twig template file](#theme)

## Render element or form element?

### Generic elements

Generic render element plugins:

- Implement [`\Drupal\Core\Render\Element\ElementInterface`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21ElementInterface.php/interface/ElementInterface)
- Attribute class is [`\Drupal\Core\Render\Attribute\RenderElement`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Attribute%21RenderElement.php/class/RenderElement)
- Usually extend the [`\Drupal\Core\Render\Element\RenderElementBase`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21RenderElementBase.php/class/RenderElementBase) base class

### Form input elements

Render elements representing form input elements like `<input type="textfield">` or `<textarea>`:

- Implement [`\Drupal\Core\Render\Element\FormElementInterface`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21FormElementInterface.php/interface/FormElementInterface)
- Attribute class is [`\Drupal\Core\Render\Attribute\FormElement`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Attribute%21FormElement.php/class/FormElement)
- Usually extend the [`\Drupal\Core\Render\Element\FormElementBase`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Element%21FormElementBase.php/class/FormElementBase) base class

## Choose a unique name

Every render element type needs to have a unique name. This will be used as the ID for the plugin and as the value of the `#type` property, when using the element as part of a render array. It's best practice for contributed or custom modules to use their module name as a prefix for the name of the new render element type.

In this example we'll use `marquee` as the name.

## Define a plugin

Based on the choices you made above regarding the type of render element as well as the name, you can [define a new plugin](https://drupalize.me/tutorial/implement-plugin-using-php-attributes). Render element plugins go in the `Drupal\MODULENAME\Element` namespace.

In the example code below, we're defining a new `marquee` element type. A developer can use this element type in their code to wrap content using a marquee tag. Content is defined using the `#content` property.

The marquee element allows you to specify additional attributes for the `<marquee>` tag via render array properties including `#direction`, `#loop`, and `#scrollamount`, the values of which are any valid value from the HTML spec for the marquee tag. The `#scrollamount` property has some additional trickery. If you specify the value `'random'`, a preprocess method on the render element type will insert a random valid `scrollamount` value.

The render element plugin should contain the required `getInfo()` method, as well as any other optional methods used as [callbacks for properties](https://drupalize.me/tutorial/render-api-callback-properties) like `#pre_render` or `#validate`. This keeps the code that defines an element all in one place.

### Example

*render\_example/src/Element/Marquee.php*

```
<?php

namespace Drupal\render_example\Element;

use Drupal\Core\Render\Attribute\RenderElement;
use Drupal\Core\Render\Element\RenderElementBase;

/**
 * Provides a marquee render element.
 *
 * New render element types are defined as plugins. They live in the
 * Drupal\{module_name}\Element namespace and implement
 * \Drupal\Core\Render\Element\ElementInterface. They are attributed with either
 * \Drupal\Core\Render\Attribute\RenderElement or
 * \Drupal\Core\Render\Attribute\FormElement. And extend either the
 * \Drupal\Core\Render\Element\RenderElementBase, or
 * \Drupal\Core\Render\Element\FormElementBase base classes.
 *
 * In the attribute below we define the string "marquee" as the ID for this
 * plugin. That will also be the value used for the '#type' property in a render
 * array. For example:
 *
 * @code
 * $build['awesome'] = [
 *   '#type' => 'marquee',
 *   '#content' => 'Whoa cools, a marquee!',
 * ];
 * @endcode
 *
 * View an example of this custom element in use in
 * \Drupal\render_example\Controller\RenderExampleController::arrays().
 *
 * @see plugin_api
 * @see render_example_theme()
 */
#[RenderElement('marquee')]
class Marquee extends RenderElementBase {

  /**
   * {@inheritdoc}
   */
  public function getInfo() {

    // Returns an array of default properties that will be merged with any
    // properties defined in a render array when using this element type.
    // You can use any standard render array property here, and you can also
    // add custom properties that are specific to your new element type.
    return [
      // See render_example_theme() where this new theme hook is declared.
      '#theme' => 'render_example_marquee',
      // Define a default #pre_render method. We will use this to handle
      // additional processing for the custom attributes we add below.
      '#pre_render' => [
        [self::class, 'preRenderMarquee'],
      ],
      // This is a custom property for our element type. We set it to blank by
      // default. The expectation is that a user will add the content that they
      // would like to see inside the marquee tag. This custom property is
      // accounted for in the associated template file.
      '#content' => '',
      '#attributes' => [
        'direction' => 'left',
        'loop' => -1,
        'scrollamount' => 'random',
      ],
    ];
  }

  /**
   * Pre-render callback; Process custom attribute options.
   *
   * @param array $element
   *   The renderable array representing the element with '#type' => 'marquee'
   *   property set.
   *
   * @return array
   *   The passed in element with changes made to attributes depending on
   *   context.
   */
  public static function preRenderMarquee(array $element) {
    // Normal attributes for a <marquee> tag do not include a 'random' option
    // for scroll amount. Our marquee element type does though. So we use this
    // #pre_render callback to check if the element was defined with the value
    // 'random' for the scrollamount attribute, and if so replace the string
    // with a random number.
    if ($element['#attributes']['scrollamount'] == 'random') {
      $element['#attributes']['scrollamount'] = abs(rand(1, 50));
    }
    return $element;
  }

}
```

The code above gets us the ability to use `marquee` in a render array like so:

```
$build['awesome'] = [
  '#type' => 'marquee',
  '#content' => 'Whoa cools, a marquee!',
  '#attributes' => [
    'scrollamount' => 'random',
    'direction' => 'right',
    'scrolldelay' => 5,
  ],
];
```

But it doesn't actually result in any HTML markup being output yet. For that we need to define a theme hook and associated template file.

## Add a theme hook and Twig template file

After the defaults defined in the `Marquee::getInfo()` method defined above are applied to our render array as part of the [render pipeline](https://drupalize.me/tutorial/render-pipeline), it'll look more like this:

```
$build['awesome'] = [
  '#type' => 'marquee',
  '#theme' => 'render_example_marquee',
  '#content' => 'Whoa cool, a marquee!',
  '#attributes' => [
    'scrollamount' => 'random',
    'direction' => 'right',
    'scrolldelay' => 5
  ],
  '#pre_render' => array(
    array('\Drupal\render_example\Element\Marquee', 'preRenderMarquee'),
  ),
];
```

The addition of that `'#theme' => 'render_example_marquee'` property means that from here on our render element will use the theme hook `render_example_marquee` when converting this element to HTML. You can read more about how this works, as well as how to define new theme hooks like this and associate them with Twig template files in the tutorial [Output Content with a Template File](https://drupalize.me/tutorial/output-content-template-file).

Another way to get a custom render element to output HTML is by using existing theme hooks in the `getInfo()` method, essentially making your element a wrapper with some additional defaults. Alternatively, use a preprocess method to convert your element to one or more other existing element types which have their own associated theme hooks. See `\Drupal\file\Element\ManagedFile::processManagedFile()` for an example of this.

## Recap

In this tutorial we looked at defining new custom render element types for use in conjunction with the `#type` property of a render array. Doing so allows us to encapsulate display logic into a reusable component that we can use in many places with a minimal amount of repetition in our code. We learned that render element types are plugins. In order to create new ones you first need to add a new `Element` plugin which extends either the `RenderElementBase` or `FormElementBase` base class.

## Further your understanding

- Can you give an example of when it might be beneficial to define a new render element type in your own code?
- The most complex, and therefore possibly most informative, render element type in Drupal core is the `#managed_file` element type. Take a look at the `\Drupal\file\Element\ManagedFile` plugin for some inspiration.

## Additional resources

- [Learn how to use an existing render element type in a render array](https://drupalize.me/tutorial/use-render-element-types-render-array) (Drupalize.Me)
- [Render API overview](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21theme.api.php/group/theme_render/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[What Are Render Elements?](/tutorial/what-are-render-elements?p=2775)

Next
[Render Pipeline](/tutorial/render-pipeline?p=2775)

Clear History

Ask Drupalize.Me AI

close