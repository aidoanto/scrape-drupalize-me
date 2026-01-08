---
title: "Add Cache Metadata to Render Arrays"
url: "https://drupalize.me/tutorial/add-cache-metadata-render-arrays?p=2723"
guide: "[[output-and-format-data-code]]"
---

# Add Cache Metadata to Render Arrays

## Content

The individual items that make up the content of a page impact the cacheability of that page. In order for Drupal's cache and external caches to better understand how the content varies on a page, module developers use the `#cache` render element property. The `#cache` property defines cacheability metadata for individual elements in a render array.

Additionally, these Render API elements can become fairly complex. The calculation of what the final HTML output should look like often involves looking up content in the database, checking multiple conditions, maybe querying an external API, and various other tasks. This can cause turning a render array into HTML to become quite expensive. In order to speed up this process, the Render API will cache the generated HTML for each element and reuse it on future requests whenever possible -- but only if you tell it to do so.

In this tutorial, we'll look at:

- How render caching impacts the performance of a page
- Defining the cacheability of an item with cache tags, cache contexts, and cache max-age
- Examples of using the `#cache` property in a render array

By the end of this tutorial you should know how, and when, to use the `#cache` property when defining render arrays.

## Goal

Demonstrate how to use the `#cache` property in a render array to define cacheability for an element.

## Prerequisites

- [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays)
- [Cache API Overview](https://drupalize.me/tutorial/cache-api-overview)

## Render caching

Because [renderers](https://drupalize.me/tutorial/render-api-renderers) work by converting the innermost child of the array to HTML first and then proceeding outwards, the Render API can be smart about using cached versions of elements deeper in the tree even when a parent element might be invalidated and need to be re-rendered. For example, if a new item is added to the primary menu that block needs to be re-rendered, but if the block containing the footer and all of its children hasn't changed there's no need to re-render that block.

Note: Not *all* elements in a render array are cached, only those that provide cache keys. As a module developer it is your job to understand what fragments of any render array you define should be cached.

Information about an individual element's cacheability, the various contexts in which it is rendered, and how it affects any child elements or the parent element are contained within the `#cache` property, which is valid for any render element.

As a module developer, when you define content in a render array you should also take a few minutes to think about the cacheability of that content. We like the thought process [outlined in the documentation](https://www.drupal.org/docs/8/api/render-api/cacheability-of-render-arrays):

1. *Why* should I cache this? Is this something that's expensive to render? If the answer is "yes", then what identifies this particular representation? These are your *[cache keys](https://drupalize.me/tutorial/cache-api-overview)*.
2. *How* does the thing I'm rendering vary per combination of permissions, per URL, language, or something else? This is your *[cache context](https://drupalize.me/tutorial/cache-api-overview)*.
3. *What* causes the thing to become outdated? Which other things does it depend on that might also become outdated? These are your *[cache tags](https://drupalize.me/tutorial/cache-api-overview)*.
4. *When* does the thing I'm rendering become outdated? Is it only valid for a specific time period? This is your *[cache max-age](https://drupalize.me/tutorial/cache-api-overview)*.

## The `#cache` property

Use the `#cache` property of elements in a render array to specify the cacheability of that item. The value of the `#cache` property is an array with the following, optional, key-value pairs:

- **keys**: An array of one or more keys that identify the element. If `keys` is set, the cache ID is created automatically from these keys.
- **tags**: An array of one or more cache tags identifying the data this element depends on.
- **contexts**: An array of one or more cache context IDs. These are converted to a final value depending on the request. (For instance, `user` is mapped to the current user's ID.)
- **max-age**: A time in seconds. Zero seconds means it is not cacheable. `\Drupal\Core\Cache\Cache::PERMANENT` means it is cacheable forever. Note: this isn't directly related to the HTTP `Cache-Control` header's `max-age` parameter, see [below](#anonymous_user_page_cache_and_the_max-age_setting) for more.
- **bin**: Specify a cache bin to cache the element in. Default is `default`.

Regardless of whether an element is going to be cached by the Render API, you should always set appropriate values for context, tags, and max-age. These values are bubbled up to the response cache and affect the cacheability of the page as a whole. Keys should be set if you want to cache an individual element within a render array. For example, cache the rendering of the node element and all of its children.

## Example code

Here are some theoretical examples that demonstrate how to use the `#cache` property. These examples should also give you some ideas about how you might think about your data and its variability.

This element never changes; you can cache it forever:

```
$build['example'] = [
  '#markup' => $this->t('Drupal is the coolest'),
  '#cache' => [
    'max-age' => \Drupal\Core\Cache\Cache::PERMANENT,
  ],
];
```

This element is expensive to calculate, so we want to cache it, but it's also somewhat time-sensitive. For our use case we can cache for up to 2 minutes, but then we need to refresh the data.

```
$build['example'] = [
  '#markup' => $this->t('Hello, it is currently @date_time', ['@date_time' => date('H:i')]),
  '#pre_render' => [$this, 'superSlowPreRender'],
  '#cache' => [
    // Cache for 120 seconds and then invalidate.
    'max-age' => 120,
  ],
];
```

This element can be cached, but it contains the name of the currently logged-in user, so we need to make sure that it varies per user so people don't see the wrong name. We also need to flush the item if the user changes their name:

```
$current_user = \Drupal::currentUser();

$build['example'] = [
  '#markup' => $this->t('Hello %name', ['%name' => $current_user->getAccountName()]),
  '#cache' => [
    // The "current user" depends on the request, so we use the 'user' context
    // which tells Drupal to vary by user for this element.
    'context' => ['user'],
    // We also need to indicate that we want to update this if the user edits
    // their name, so we add the appropriate tags so that Drupal can invalidate
    // this element if the user entity changes.
    //
    // In this case the $current_user object is an instance of AccountInterface
    // which is not actually a complete User entity object. So we need to first
    // load the complete entity, and then call the getCacheTags() method.
    'tags' => \Drupal\user\Entity\User::load($current_user->id())->getCacheTags(),
  ],
];
```

**Tip:** Entities, like the user account in this case, should have a `::getCacheTags()` method that returns any tags for that object. So, `$node->getCacheTags()` would return `node:5`. Rather than hard coding these, or trying to memorize patterns, use these methods instead.

This element contains the rendered output of some custom data we've pulled in from an external API. We want to cache this portion of the render array so that in future rendering passes it can be reused. The query parameters used to query the API vary depending on context, so we want to ensure that we store different versions of the cached data depending on query parameters. Once we have the data, we can cache it for up to 2 minutes:

```
$build['example'] = [
  '#markup' => $this->t('Content pulled from external API'),
  '#pre_render' => [$this, 'pullExternalContent'],
  '#cache' => [
    'keys' => ['custom_api_query', 'parameter_1', 'parameter_2'],
    'max-age' => 120,
  ],
];
```

## Anonymous user page cache and the `max-age` setting

The core Internal Page Cache module is responsible for setting the `max-age` value of the HTTP `cache-control` header. It does so by looking at the cacheable metadata of all the elements on the page, determining if the page is cacheable, and, if so, setting the `max-age` value to the configured time. This `cache-control` HTTP header is subsequently used by reverse proxy servers like Varnish, CDNs, and the user's browser to determine how long they can cache the HTML of the page. However, there are 2 issues with the module that you should be aware of.

1. You can only configure a site-wide TTL (Time To Live) for the page cache. This means all pages, regardless of what is set in the `max-age` cacheability data of the render arrays, will get the same TTL.
2. The `max-age` set in `#cache` is still used by the render cache.

The [Cache Control Override module](https://www.drupal.org/project/cache_control_override) can handle bubbling up `max-age` to the page response level to control the `Cache-Control` `max-age` parameter. If you need per-page control of the `max-age` TTL value, this is a good place to start.

### Page cache kill switch

You can disable the page cache entirely, regardless of any cacheability metadata for the content of the page, using the `page_cache_killswitch` service.

Example:

```
\Drupal::service('page_cache_kill_switch')->trigger();
```

This will force the `Cache-Control` header for any response that executes the above code to `must-revalidate, no-cache, private`. Which is effectively saying you want Drupal to calculate the HTML for the page every time it is viewed. Be careful! This can significantly slow down the page's response time. It's still a good idea to set appropriate cacheability metadata on the renderable content of the page so that render caching can still work.

[Read more about the limitations of the `max-age` property](https://www.drupal.org/docs/drupal-apis/cache-api/cache-max-age#s-limitations-of-max-age).

## Recap

In this tutorial, we learned that the `#cache` property of elements in a render array is used to define that particular item's cacheability. During the rendering process, elements in a render array that are expensive to calculate can be cached. Those cached fragments can then be reused in the future to speed up rendering. Even if you're not allowing an individual element to be cached by giving it cache keys, it's still best practice to provide cacheability metadata, because that data bubbles up the tree and can be used by parent items to determine whether the cache needs to be flushed.

## Further your understanding

- Can you give an example of when you would set the `context` key of the `#cache` property of an element in a render array?
- How does render caching improve Drupal's overall performance when displaying a page?
- How do you define something as not cacheable at all? Can you give an example of something you would never want to cache under any circumstances?

## Additional resources

- [Use Lazy Builders and Placeholders](https://drupalize.me/tutorial/use-lazy-builders-and-placeholders) (Drupalize.Me)
- [Cacheability of render arrays](https://www.drupal.org/docs/8/api/render-api/cacheability-of-render-arrays) (Drupal.org)
- [`RendererInterface::render()` documentation](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21RendererInterface.php/function/RendererInterface%3A%3Arender/) (api.drupal.org)
- [Some quick render array examples](https://www.drupal8.ovh/en/tutoriels/158/cache-drupal-8-render-arrays) (drupal8.ovh)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Cache API Overview](/tutorial/cache-api-overview?p=2723)

Next
[Use Lazy Builders and Placeholders](/tutorial/use-lazy-builders-and-placeholders?p=2723)

Clear History

Ask Drupalize.Me AI

close