---
title: "Use Lazy Builders and Placeholders"
url: "https://drupalize.me/tutorial/use-lazy-builders-and-placeholders?p=2723"
guide: "[[output-and-format-data-code]]"
order: 20
---

# Use Lazy Builders and Placeholders

## Videos

- [YouTube Video](//www.youtube.com/embed/JwzX0Qv6u3A)

## Content

The Render API is capable of detecting poorly-cacheable (highly dynamic) parts of a page and rendering them later using a process called *auto-placeholdering*. This works by using `#lazy_builder` callbacks to lazy load certain very dynamic subtrees of a render array. The place in the array where that very dynamic content would appear is first assigned a placeholder. At the very last moment it is replaced with the actual content.

This allows Drupal to do things like cache the overall page in the *Dynamic Page Cache* despite parts of the page being too dynamic to be worth caching. It also allows the Render API to assemble a page using cache fragments combined with non-cacheable elements.

In this tutorial we'll:

- Discuss what lazy builders are and how they work in conjunction with placeholders to speed up the rendering pipeline
- Cover some common gotchas for lazy builders
- Look at some example code that implements a lazy builder callback

By the end of this tutorial, you should know how and when to use the `#lazy_builder` property of a render array and how Drupal uses placeholders to increase the cacheability of content and speed up the rendering process.

## Goal

Use a `#lazy_builder` callback to construct the portion of a render array that contains uncacheable data including the current date/time and the user's name.

## Prerequisites

- [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays)
- Not required, but closely related to [Render API caching](https://drupalize.me/tutorial/add-cache-metadata-render-arrays)

## What are lazy builders?

A `#lazy_builder` is a callback function or method that serves as a substitute for an element, or an entire subtree, of a render array. These builder methods are called by the renderer, return a renderable array, and the returned array is substituted into the position occupied by the `#lazy_builder` element.

This, combined with Drupal's powerful [system for providing cacheability metadata in render arrays](https://drupalize.me/tutorial/add-cache-metadata-render-arrays) allows Drupal to determine, based on how dynamic the contents of the callback are, whether the `#lazy_builder` should be rendered during the initial page load or a via second pass using something like [Big Pipe](https://www.drupal.org/docs/8/core/modules/big-pipe/overview) or [ESI](https://www.w3.org/TR/esi-lang/).

Simply put, when rendering an array, whenever a `#lazy_builder` is encountered, the renderer replaces it with a placeholder. The placeholder contains information about which callback to call and the arguments to pass to it. The renderer then continues traversing the array and converting it to HTML. The resulting HTML, including placeholders, is cached. Then, depending on the rendering strategy being used, the placeholders are each replaced with their dynamic content. On subsequent requests that cached outer array can be reused while the placeholders are once again dynamically updated. Check out the diagram from the [render pipelines tutorial](https://drupalize.me/tutorial/render-pipeline) for more about this.

By default Drupal uses a single-flush rendering strategy. That is, placeholders are all replaced immediately and the complete content is returned. However, modules like Big Pipe introduced a multi-tiered rendering strategy, where the content is returned to the browser with the placeholders still intact. Then, JavaScript is used to call the defined lazy builder and replace the placeholder with the relevant content. This allows the initial content to be delivered to the page quickly from cache and the highly dynamic placeholder content will be filled in when it's available.

This example shows the difference between single-flush and Big Pipe rendering:

## When should I use a lazy builder?

As a rule of thumb, you should considering using a lazy builder whenever the content you're adding to a render array is:

- Content that would have a high cardinality if cached. For example, a block that displays the user's name. It can be cached, but because it varies by user, it's also likely to result in cached objects with a low hit rate.
- Content that cannot be cached or has a very high invalidation rate. For example, displaying the current date/time, or statistics that need to be as up-to-date as possible at all times.
- Content that requires a lengthy and potentially slow assembly process. For example, a block displaying content from a third-party API where requesting content from the API incurs overhead.

When specifying `#cache` in your render array consider providing a `#lazy_builder` to build out the render array in case of a cache miss. These of course are not the only use cases, but hopefully this list helps get you thinking about when you should use a lazy builder in your code.

## Use a `#lazy_builder`

You can use a lazy builder in your render array by specifying the key `#lazy_builder` for an element. The value is an array; the first value of that array is the name of the callback, and the second value is an array of arguments to pass to the callback.

Example:

```
$build['lazy'] = [
  '#lazy_builder' => [
    // Function or method to call.
    $this::class . '::lazyDateFormat',
    ['Y-m-d']
  ]
];
```

## Callback formats

Callbacks for a lazy builder can take a variety of different formats. In most cases you'll probably use either option #1 or #3 below.

#1. Call the `build()` method on `$this` class:

```
$build['item']['#lazy_builder'] = [static::class . '::build', ['argument1', 'argument2']];
```

#2. Call the `build()` method, or any other method, on a class that implements `Drupal\Core\Security\TrustedCallbackInterface`:

```
use Drupal\render_example\LazyBuilder;
$build['item']['#lazy_builder'] = [LazyBuilder::class . '::build', ['argument1', 'argument2']];
```

#3. Call a service. Use this whenever you need to inject additional dependencies into the class performing the lazy building operation. You'll need to first declare a new service, and then reference the service by its name.

```
$build['item']['#lazy_builder'] = ['service.name:method', ['argument1', 'argument2']];
```

For more on defining a method for a function to use as a callback see [Render API Callback Properties](https://drupalize.me/tutorial/render-api-callback-properties)

## A note on callback arguments

Lazy builders need to be able to perform their operations in isolation. They will not necessarily have the same state or context as the code where they are defined. Therefore, a lazy builder callback can receive any number of arguments, but all arguments **must** be primitive types (string, bool, int, float, NULL). If, for example, you need to make use of the current user, you would not pass the `$user` object. Instead, provide the lazy builder with the user's ID, and then use that within the lazy builder to load the appropriate object.

Additionally, arguments should only be passed from an object that is already provided to a parent element. Otherwise, if the render array is standalone (not a child of any parent element), then the arguments should be retrieved inside the callback itself.

## Some example code

The following code example is taken from the [Examples for Developers project](https://www.drupal.org/project/examples) and has had some unrelated portions of the example code removed to make it easier to read.

```
<?php

namespace Drupal\render_example\Controller;

use Drupal\Core\Controller\ControllerBase;
use Drupal\Core\Security\TrustedCallbackInterface;
use Drupal\examples\Utility\DescriptionTemplateTrait;
use Drupal\user\Entity\User;
use Symfony\Component\DependencyInjection\ContainerInterface;
use Drupal\Component\Utility\Variable;
use Drupal\Core\Session\AccountInterface;

class RenderExampleController extends ControllerBase implements TrustedCallbackInterface {
  use DescriptionTemplateTrait;

  /**
   * Current user.
   *
   * @var \Drupal\user\UserInterface
   */
  protected $currentUser;

  /**
   * Constructs a new BlockController instance.
   *
   * @param \Drupal\Core\Session\AccountInterface $current_user
   *   The current user.
   */
  public function __construct(AccountInterface $current_user) {
    $this->currentUser = $current_user;
  }

  /**
   * {@inheritdoc}
   */
  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('current_user')
    );
  }

  /**
   * {@inheritdoc}
   */
  protected function getModuleName() {
    return 'render_example';
  }

  /**
   * Examples of defining content using renderable arrays.
   */
  public function arrays() {
    // ...
    $build = array();

    // A #lazy_builder callback can be used to build a highly dynamic section of
    // a render array from scratch. This, combined with the use of placeholders,
    // allows the renderer to cache some, but not all, portions of a render
    // array. Without #lazy_builders, if any element in the render tree is
    // uncacheable the whole tree would need to be re-rendered every time.
    //
    // The general rendering flow is as follows:
    // - Check for cached version of output from previous rendering, if it
    //   exists replace any placeholders in the rendered output with their
    //   dynamic content as generated by the #lazy_builder callback, and return
    //   the resulting HTML.
    // - If no cached version exists render the array to HTML, when an element
    //   that can be placeholdered is encountered insert a placeholder, cache
    //   the HTML after rendering for next time, replace the placeholders with
    //   their dynamic content, and return the resulting HTML.
    //
    // This is especially noticeable when used in conjunction with modules like
    // Big Pipe which do rendering of a page in multiple passes vs. the default
    // single flush renderer.
    //
    // See \Drupal\block\BlockViewBuilder::viewMultiple() for an example from
    // core.
    $build['lazy_builder'] = [
      // Set the value of the #lazy_builder property to an array, the first key
      // of the array is the method, service, or function, to call in oder to
      // generate the dynamic data. The second argument is an array of any
      // arguments to pass to the callback. Arguments can be only primitive
      // types (string, bool, int, float, NULL).
      '#lazy_builder' => [
        static::class . '::lazyBuilder',
        [$this->currentUser->id(), 'Y-m-d'],
      ],
      // #lazy_builder callbacks can be used in conjunction with
      // #create_placeholder to tell the renderer that instead of simply calling
      // the #lazy_builder code right away, to instead insert a placeholder and
      // delay execution of the #lazy_builder code until it's needed.
      //
      // This is somewhat analogous to the way Drupal uses the PSR-4 autoloading
      // standard to "lazy" load PHP files that contain the definition of a
      // class only if, and when, that class is used.
      //
      // To force a element to use a placeholder set #create_placeholder to
      // TRUE.
      //
      // Preferably you would include #cache metadata (see above) and allow
      // the Render API to use that metadata to automatically determine based on
      // the existence of high-cardinality cache contexts in the subtree whether
      // or not the element should use a placeholder.
      '#create_placeholder' => TRUE,
    ];

    // ...

    return $build;
  }

  /**
   * Example #lazy_builder callback.
   *
   * Demonstrates the use of a #lazy_builder callback to build out a render
   * array that can be substituted into the parent array wherever the cacheable
   * placeholder exists.
   *
   * This method is called during the process of rendering the array generated
   * by \Drupal\render_example\Controller\RenderExampleController::arrays().
   *
   * @param int $user_id
   *   UID of the user currently viewing the page.
   * @param string $date_format
   *   Date format to use with \Drupal\Core\Datetime\DateFormatter::format().
   *
   * @return array
   *   A renderable array with content to replace the #lazy_builder placeholder.
   */
  public static function lazyBuilder($user_id, $date_format) {
    $account = User::load($user_id);

    $build = [
      'lazy_builder_welcome' => [
        '#markup' => '<p>' . \Drupal::translation()->translate('Your name is: @name', ['@name' => $account->getDisplayName()]) . '</p>',
      ],
      'lazy_builder_time' => [
        '#markup' => '<p>' . \Drupal::translation()->translate('The current time is @time', ['@time' => \Drupal::service('date.formatter')->format(REQUEST_TIME, 'custom', $date_format)]) . '</p>',
      ],
    ];

    // In order to demonstrate the use of lazy builders we use sleep here to
    // simulate an expensive request.
    sleep(3);
    return $build;
  }

  /**
   * {@inheritDoc}
   */
  public static function trustedCallbacks() {
    // For security reasons we need to declare which methods on this class are
    // safe for use as a callback.
    return ['lazyBuilder'];
  }

}
```

## Auto-placeholders

Generally when using a `#lazy_builder` you don't need to set `'#create_placeholder' = TRUE`. In fact, you should only do this if you know for absolute certain that you'll always want to use a placeholder when rendering this content.

In most cases, you can let Drupal figure out whether it should use a placeholder on the first pass and render the complete content later, or just render the complete content now. This is known as auto-placeholdering. Drupal uses the cacheability metadata provided for an element in a render array, as well as any metadata bubbled up from the lazy builder, to determine the best course of action for the current rendering strategy.

[Read more about auto-placeholdering](https://www.drupal.org/docs/drupal-apis/render-api/auto-placeholdering).

## Recap

In this tutorial we learned how Drupal's Render API uses `#lazy_builder` callbacks and placeholders to improve the cacheability of a page even when parts of it are too dynamic to be cached themselves. We also looked at how modules like Big Pipe can use an alternative rendering strategy to delay the rendering of highly dynamic placeholder content by calling the appropriate `#lazy_builder` only after the static parts of the page have already been loaded from cache.

## Further your understanding

- Can you give an example of when you would use a `#lazy_builder` in your own module? How about when it is unnecessary?
- List some other websites that you use on a regular basis that use a placeholder rendering strategy to improve initial page load times
- Enable the Big Pipe module on a development site, log in, and navigate around. Can you see the multi-pass rendering strategy in action? How does it change the perceived time-to-load of a page?

## Additional resources

- [Read more about caching render arrays](https://drupalize.me/tutorial/add-cache-metadata-render-arrays) and the [render pipeline](https://drupalize.me/tutorial/render-pipeline) (Drupalize.Me)
- [Auto-placeholdering](https://www.drupal.org/docs/drupal-apis/render-api/auto-placeholdering) (Drupal.org)
- [This presentation](https://www.youtube.com/watch?v=DMKD91jB58g) by Fabian Franz and Wim Leers is a fantastic introduction to Drupal's caching and lazy builders (youtube.com)
- [This presentation on caching in Drupal 8](https://youtu.be/gkATpbhecPw?t=2427) has a whole section on placeholders (youtube.com)
- [This issue](https://www.drupal.org/node/2478483) where placeholders and `#lazy_builder` were added to Drupal has a lot of background information in the summary that is worth reading (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add Cache Metadata to Render Arrays](/tutorial/add-cache-metadata-render-arrays?p=2723)

Clear History

Ask Drupalize.Me AI

close