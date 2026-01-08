---
title: "Render API Callback Properties"
url: "https://drupalize.me/tutorial/render-api-callback-properties?p=2775"
guide: "[[output-and-format-data-code]]"
---

# Render API Callback Properties

## Content

Some Render API properties, like `#pre_render`, `#element_validate`, and `#lazy_builder` are considered callable. Rather than receiving a static value, they contain a pointer to code that should be called at a specific time during the process of rendering a render element. Callbacks are used in some cases to return a value that can be substituted into the render array, and in other cases given the opportunity to manipulate the current element in the array directly.

In this tutorial, we'll:

- Look at what callbacks are
- List some common callback properties
- Show various ways that callback code can be defined
- Discuss how to choose which method to use

By the end of this tutorial, you should be able to define an appropriate value for any Render API property that expects a callback, and define the logic that is executed when the callback is triggered.

## Goal

Understand how callback properties work in render arrays and how to set an appropriate value for one.

## Prerequisites

- [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays)
- [What Are Render Elements?](https://drupalize.me/tutorial/what-are-render-elements)
- [Implement Any Hook](https://drupalize.me/tutorial/implement-any-hook)

## Properties whose value is callable

Some Render API properties are callable. Instead of having a hard-coded static value that gets used when rendering the array, they contain a pointer to some code elsewhere in the system that should be executed. During rendering, when the property is encountered, the renderer dispatches control to the defined callback, which performs its internal logic and then returns control to the renderer.

In this context *callable* is a reference to the [PHP callable type](https://www.php.net/manual/en/language.types.callable.php).

Callbacks receive arguments that usually include the element and all of its children for which the callback property was defined, and any other application context or state relative to the specific callback. For example, a callback that is responsible for validating the submitted value of a form element would also have access to the relevant form state object so that it could set errors on the form if any are encountered.

In some cases callbacks are able to alter the element in question. The result is propagated back into the array being rendered. A `#pre_render` callback, for example, is called early on in the rendering process and can alter the associated element. It might add additional child elements, or alter the value of previously defined properties, based on the callback's internal logic.

Callbacks can be quite powerful once you know how to leverage them. In the rest of this tutorial we'll look at how you can define a callback and assign it as the value of a callback property.

The value of a callback property is always an array with one or two values in it. The first is a pointer to the code that should be invoked. The second is an optional array of arguments that will be passed to the defined callback. Some callbacks, like `#pre_render` receive a predetermined set of arguments, while others like `#lazy_builder` take user-defined arguments.

## Commonly-used callback properties

This isn't a complete list, but it does represent the more commonly-used callable properties and what they are used for:

- **`#access_callback`**: Code to call to check access. Use in place of `#access`. Receives one argument: `$element`.
- **`#pre_render`**: Array of callables, which are called just before the element is rendered. Usually used to expand or alter a render element based on application context or state. Receives one argument: `$element`. Return value: an altered `$element`.
- **`#lazy_builder`**: A lazy builder callback typically generates `#markup` and/or placeholders. See [Use Lazy Builders and Placeholders](https://drupalize.me/tutorial/use-lazy-builders-and-placeholders).
- **`#element_validate`**: Array of callables which are called to validate the input of a specific element in a form. **Arguments:** `$element`, `$form_state`, and `$form`. [Learn about using form validation callbacks](https://drupalize.me/tutorial/validate-form-input).

There are several different ways you can define and invoke a callback. We'll go through all of them, in roughly the order that you're most likely to use them.

## Callback methods

Common use cases:

- When writing a controller (page or form) that defines a new render array and assigning a callback to one of the elements in that array, you can define a static method on the controller class as the callback. This helps to keep all the code in a single location.
- When [defining a new render element type](https://drupalize.me/tutorial/define-new-render-element-type) that has a callback as one of the default property values.
- When [defining a new plugin instance](https://drupalize.me/tutorial/implement-plugin-using-php-attributes) that contains a render array, you can define a static method on the plugin class as the callback. This helps keep all the code in a single location.

[For security reasons](https://www.drupal.org/node/2966725) the class where the callback method is defined must implement `Drupal\Core\Security\TrustedCallbackInterface`. Or, `RenderElementInterface` which most controllers already do. Specifically, you'll need to implement `TrustedCallbackInterface::trustedCallbacks()` and return an array listing all the methods on the current class that can be used as the target of a callback.

Example implementation of `TrustedCallbackInterface::trustedCallbacks()`:

```
/**
  * {@inheritdoc}
  */
public static function trustedCallbacks() {
  return ['myCallbackMethod'];
}
```

Static method on the current class:

```
$build['item'] = [
  '#markup' => $this->t('This item has a #pre_render callback.'),
  '#pre_render' => [$this::class, 'myCallbackMethod'],
];
```

There are a few ways you can specify the callback to use, and they correspond to the [PHP callable type](https://www.php.net/manual/en/language.types.callable.php). Note that Render API callback properties usually expect an array of callables, this is because it's possible for a single element to have multiple callbacks. The examples below are expressed in the array format you would typically see.

Examples:

- `['methodName']`: A string that is the name of a method on the controller method where the render array is defined.
- `['ClassName::methodName']`: A string that is the full name of the class, and the method, to call. You'll frequently see this written as `[static::class . '::methodName']`.
- `[[static::class, 'methodName']]`: An array whose first member is the class name and second member is the method to call.
- `[function($element) { ... }]`: An inline function.

You can also use a static method on *any class* not just the controller, as long as that class implements `TrustedCallbackInterface`. A common use case is using `hook_form_alter()` or `hook_page_alter()` to modify an existing render array and assign a new callback property to any element in the array.

Example class containing a callback method:

```
use Drupal\Core\Form\FormStateInterface;

class CallbackClass implements TrustedCallbackInterface {

  /**
   * {@inheritdoc}
   */
  public static function trustedCallbacks() {
    // Return an array of strings containing the name(s) of each method on the
    // class that can be used as a callback.
    return ['elementValidate'];
  }

  /**
   * #element_validate callback.
   */
  public static function elementValidate(&$element, FormStateInterface $form_state, $form) {
    // Validate the element's value ...
    if ($form_state->getValue('myfield') === 'Elizabeth')) {
      $form_state->setError($element, 'That name is already used. Please choose a different one.');
    }
  }
}
```

And in your *.module* file implement `hook_form_alter()` like so:

```
use Drupal\Core\Form\FormStateInterface;
use Drupal\example\CallbackClass;

/**
 * Implements hook_form_alter().
 */
function example_form_alter(&$form, FormStateInterface $form_state, $form_id) {}
	$form['item']['#element_validate'] = [CallbackClass::class, ['elementValidate']];
}
```

### Passing arguments to callbacks

If you need to pass additional information to the callback method, add it as a custom property to the render element, and then access that value within the callback.

Example:

```
$build['item'] = [
  // This is just a made-up property, make sure the name starts with a
  // '#' or Drupal will think it is a child render element and not a property.
  '#_custom_value' = 42,
  '#markup' => $this->t('This item has a #pre_render callback.'),
  '#pre_render' => [function($element) {
    if (isset($element['#_custom_value'])) {
      $element['asdf'] = ['#markup' => 'The custom value is' . $element['#_custom_value']];  
    }
    
    return $element;
  }],
];
```

## Callback to a service

For more complex operations (especially those that rely on the use of one or more services) where a static method on a class won't work, you can define a new service and use that as the target for the callback operation. By doing it this way, you can use dependency injection to retrieve the required services and ensure your callbacks are testable and extendable.

Common use case:

- Any time you need to make use of another service to complete your callback's logic.

For example: Define a new service. (Example excerpts from the [Flag module](https://git.drupalcode.org/project/flag/-/tree/8.x-4.x)).

Excerpt from *[flag.services.yml](https://git.drupalcode.org/project/flag/-/blob/8.x-4.x/flag.services.yml)*:

```
services:
  flag.link_builder:
    class: Drupal\flag\FlagLinkBuilder
    arguments: ['@entity.manager', '@flag']
```

Excerpt from *[src/FlagLinkBuilder.php](https://git.drupalcode.org/project/flag/-/blob/8.x-4.x/src/FlagLinkBuilder.php)*

```
<?php

namespace Drupal\flag;

use Drupal\Core\Entity\EntityTypeManagerInterface;
use Drupal\flag\FlagServiceInterface;

/**
 * Provides a lazy builder for flag links.
 */
class FlagLinkBuilder implements FlagLinkBuilderInterface {

  /**
   * The entity manager.
   *
   * @var \Drupal\Core\Entity\EntityTypeManagerInterface
   */
  protected $entityTypeManager;

  /**
   * The flag service.
   *
   * @var \Drupal\flag\FlagServiceInterface
   */
  protected $flagService;

  /**
   * Constructor.
   *
   * @param \Drupal\Core\Entity\EntityTypeManagerInterface $entity_manager
   *   The entity manager.
   * @param \Drupal\flag\FlagServiceInterface $flag_service
   *   The flag service.
   */
  public function __construct(EntityTypeManagerInterface $entity_manager, FlagServiceInterface $flag_service) {
    $this->entityTypeManager = $entity_manager;
    $this->flagService = $flag_service;
  }

  /**
   * {@inheritdoc}
   */
  public function build($entity_type_id, $entity_id, $flag_id) {
    $entity = $this->entityTypeManager->getStorage($entity_type_id)->load($entity_id);
    $flag = $this->flagService->getFlagById($flag_id);

    $link_type_plugin = $flag->getLinkTypePlugin();
    return $link_type_plugin->getAsFlagLink($flag, $entity);
  }

}
```

Notice how the `flag.link_builder` service being defined makes use of the `@entity.manager` and `@flag` services. They're injected in the constructor, and then used in the `build()` method, which is the target of the `#lazy_builder` callback below.

Usage example:

```
$build['flag_' . $flag->id()] = [
  '#lazy_builder' => ['flag.link_builder:build', [
    $entity->getEntityTypeId(),
    $entity->id(),
    $flag->id(),
  ]],
  '#create_placeholder' => TRUE,
];
```

When using a service as the target of a callback, the syntax is `{service_name}:{method}`, where `{service_name}` is the unique ID of the service you would use to request it from the service container, and `{method}` is the name of the method on the resulting service object to call. See [Discover and Use Existing Services](https://drupalize.me/tutorial/discover-and-use-existing-services) for more information about how services are defined.

## Recap

In this tutorial, we learned that some render array properties contain pointers to code that should be triggered by the Render API at specific points during the process of rendering an element. These pointers are known as callbacks. We listed some common callback style properties and their use case, and then looked at the ways you can declare the callback that should be invoked.

## Further your understanding

- What are some additional properties (not listed above) that function as callbacks?
- Convert an already-defined section of a render array to use a `#lazy_builder` callback.
- Explore the File module's use of a `#pre_render` callback for the `#managed_file` element type in *core/modules/file/src/Element/ManagedFile.php*. It's a great example of doing some complex processing in a render element.

## Additional resources

- [Use Lazy Builders and Placeholders](https://drupalize.me/tutorial/use-lazy-builders-and-placeholders) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Render API Renderers](/tutorial/render-api-renderers?p=2775)

Clear History

Ask Drupalize.Me AI

close