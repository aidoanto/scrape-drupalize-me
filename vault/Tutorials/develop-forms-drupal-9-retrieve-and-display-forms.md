---
title: "Retrieve and Display Forms"
url: "https://drupalize.me/tutorial/retrieve-and-display-forms?p=2734"
guide: "[[develop-forms-drupal]]"
order: 9
---

# Retrieve and Display Forms

## Content

Forms can be displayed as the main content of a route or by using the `form_builder` service to retrieve and display a form directly. Which one you choose will depend on where on the page you want the form to appear.

In this tutorial we'll:

- Go over the two different ways a form can be retrieved and displayed
- Demonstrate how to display a form inside a custom block using the `form_builder` service

By the end of this tutorial you'll know how to retrieve a form and have it rendered anywhere on the page.

## Goal

Display the simple demonstration form inside a custom block plugin.

## Prerequisites

- We'll be displaying the form created in [Define a New Form Controller and Route](https://drupalize.me/tutorial/define-new-form-controller-and-route)
- [Implement a Plugin Using PHP Attributes](https://drupalize.me/tutorial/implement-plugin-using-php-attributes)

## Code examples

The complete code for the examples in this tutorial may be found in the [Examples for Developers'](https://www.drupal.org/project/examples) *form\_api\_example* module.

## 2 ways to display a form

Forms can be displayed in one of 2 ways: (1) as the result of a route, or (2) by invoking the `form_builder` service from within your custom code to retrieve a [render array](https://drupalize.me/tutorial/what-are-render-arrays) that represents the form and using that anywhere render arrays are used.

Image

![Homepage of Drupal site with a form displayed in a block as secondary content, and a form displayed in the primary content area](../assets/images/form-api_display.png)

### Use a route

If you want your form to display as the primary content of a page then you'll want to display your form as the target of a route. This is exactly what we did in [Define a New Form Controller and Route](https://drupalize.me/tutorial/define-new-form-controller-and-route). This is the more commonly used of the 2 options.

It works because routes that point to forms use the `_form` key instead of the standard `_controller` key to tell Drupal that it should use the form builder service when servicing the request.

Let's look at how that works in more detail:

- `\Drupal\Core\Routing\Enhancer\FormRouteEnhancer` defines the `_form` key for the routing system and also defines what to do with the key if it's present.
- If your route does contain a `_form` key, then `\Drupal\Core\Routing\Enhancer\FormRouteEnhancer::enhance` adds a key of `__controller: controller.form:getContentResult` to the route at runtime. This says that the request should be serviced by the `getContentResult()` method of whatever class provides the `controller.form` service. Effectively, whatever object the service container returns for `controller.form` calls `$object->getContentResult()` and uses that as the content of the route.
- The service in this case is an instance of `\Drupal\Core\Controller\HtmlFormController`. When the `getContentResult()` method is invoked, the class defined by `_form` is used along with the `form_builder` service to retrieve the appropriate render array for the form, and that render array is returned as the result of the route.

## Use `FormBuilder` directly

Sometimes you need to display a form in other parts of the page. A common example is displaying a form as the content of a block. In this case, you can use the form builder service to retrieve the render array representation of the form and then add it into any existing render array.

Form processing is handled by the `form_builder` service provided by `\Drupal\Core\Form\FormBuilder`, which is an implementation of `\Drupal\Core\Form\FormBuilderInterface`. When displaying a form we can use the `FormBuilder::getForm()` method to retrieve the render array representation of the form and then insert the returned results into any existing render array.

## Display a form in a block

As an example, let's display the form we created in [Define a New Form Controller and Route](https://drupalize.me/tutorial/define-new-form-controller-and-route) as the content of a custom block.

The code below defines a new custom block plugin that uses the form builder service to retrieve and display a form.

*form\_api\_example/src/Plugins/Block/SimpleFormBlock.php*:

```
<?php

namespace Drupal\form_api_example\Plugin\Block;

use Drupal\Core\Block\Attribute\Block;
use Drupal\Core\Block\BlockBase;
use Drupal\Core\Plugin\ContainerFactoryPluginInterface;
use Drupal\Core\Form\FormBuilderInterface;
use Drupal\Core\StringTranslation\TranslatableMarkup;
use Symfony\Component\DependencyInjection\ContainerInterface;

/**
 * Provides a 'Example: Display a form' block.
 *
 * This example demonstrates the use of the form_builder service, an
 * instance of \Drupal\Core\Form\FormBuilder, in order to retrieve and display
 * a form.
 */
#[Block(
  id: "form_api_example_simple_form_block",
  admin_label: new TranslatableMarkup("Example: Display a form"),
)]
class SimpleFormBlock extends BlockBase implements ContainerFactoryPluginInterface {

  /**
   * Form builder service.
   *
   * @var \Drupal\Core\Form\FormBuilderInterface
   */
  protected $form_builder;

  /**
   * {@inheritdoc}
   */
  public function __construct(array $configuration, $plugin_id, $plugin_definition, FormBuilderInterface $form_builder) {
    parent::__construct($configuration, $plugin_id, $plugin_definition);
    $this->form_builder = $form_builder;
  }

  /**
   * {@inheritdoc}
   */
  public static function create(ContainerInterface $container, array $configuration, $plugin_id, $plugin_definition) {
    return new static(
      $configuration,
      $plugin_id,
      $plugin_definition,
      $container->get('form_builder')
    );
  }

  /**
   * {@inheritdoc}
   */
  public function build() {
    $output = [
      'description' => [
        '#markup' => $this->t('Using form provided by Drupal\form_api_example\Form\SimpleForm'),
      ],
    ];

    // Use the form builder service to retrieve a form by providing the full
    // name of the class that implements the form you want to display. getForm()
    // will return a render array representing the form that can be used anywhere
    // render arrays are used.
    //
    // In this case the build() method of a block plugin is expected to return
    // a render array, so we add the form to the existing output and return it.
    $output['form'] = $this->form_builder->getForm('Drupal\form_api_example\Form\SimpleForm');
    return $output;
  }

}
```

The most important parts of this example are the use of dependency injection to obtain a copy of the form builder service, and using `$this->form_builder->getForm($form_argument)`, where `$form_argument` is the name of the class that implements the form, or an instance of that class, to retrieve a render array representation of the form to display.

## Test that it works

To test that it works, place the newly created block into any region in your theme. Then visit a page where that block will be displayed. Can you see the form? What happens if you fill it out and submit it?

## Recap

In this tutorial, we discussed the 2 different ways you can display a form: either as the content of a route or by using the form builder service to retrieve a render array representation of the form. We then created a block plugin that displays a form as an example of using the form builder service.

## Further your understanding

- Can you find an example of a form being displayed using the form builder service in core?
- What happens if you retrieve and display a form using the form builder service from a theme instead of a module?

## Additional resources

- [Render API Overview](https://drupalize.me/tutorial/render-api-overview) (Drupalize.Me)
- [Block API](https://www.drupal.org/docs/drupal-apis/block-api/block-api-overview) (Drupal.org)
- [Drupal\Core\Form\FormBuilder](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Form%21FormBuilder.php/class/FormBuilder) (api.drupal.org)
- [Examples for Developers project](https://www.drupal.org/project/examples) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Alter an Existing Form with hook\_form\_alter()](/tutorial/alter-existing-form-hookformalter?p=2734)

Next
[Theming Drupal Forms with Twig](/tutorial/theming-drupal-forms-twig?p=2734)

Clear History

Ask Drupalize.Me AI

close