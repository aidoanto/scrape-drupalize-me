---
title: "Generate URLs and Output Links"
url: "https://drupalize.me/tutorial/generate-urls-and-output-links?p=3252"
guide: "[[output-and-format-data-code]]"
order: 15
---

# Generate URLs and Output Links

## Content

Linking to things is probably one of the first things you learned how to do as a web developer. Anchor tags are the framework of how the world wide web works. So it's important to know how to create them in Drupal. Chances are you'll be doing a lot of it.

Creating links to things in Drupal, however, is a bit more complicated than just typing out an HTML anchor tag. It requires understanding how URLs are generated from routes, and how to define links as renderable arrays. It can also be tricky because of the multitude of deprecated, but still functioning, ways of creating links.

In this tutorial we'll:

- Use the `\Drupal\Core\Url` class to generate URL objects from routes and external URIs.
- Use the `\Drupal\Core\Link` class to create HTML links within a Drupal module.
- Examine best practices for working with URLs and links in a Drupal module in order to ensure that your code continues to work into the future.

By the end of this tutorial you should be able to link to anything, either internal to your application or external, using Drupal best practices.

## Goal

Use `Url` and `Link` to output a link to anything.

## Prerequisites

- [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays)
- [What Are Render Elements?](https://drupalize.me/tutorial/what-are-render-elements)
- Learn about discovering existing routes in [How to Find a Route in Drupal](https://drupalize.me/tutorial/how-find-route-drupal)

## Quick reference: making URLs and links in Drupal

### Generate URLs with `\Drupal\Core\Url`

```
// From a route.
$url = Url::fromRoute('contact.site_page');
// From a URI.
$url = Url::fromUri('http://example.com');
```

### Create links with `\Drupal\Core\Link`

```
// Link to an internal path defined by a route.
$link = Link::createFromRoute('This is a link', 'entity.node.canonical', ['node' => 42])

// Link to an external URI.
$link = Link::fromTextAndUrl('This is a link', Url::fromUri('http://example.com'));

// Get output as a render array. Preferred.
$link->toRenderable();

// Get output as a string.
$link->toString();
```

## Why is this so complicated?

Why can't I just type some HTML, `<a href="/node/23?name=joe">` and be done with it? There are a bunch of reasons, including:

- When dealing with internal paths, or routes, the actual URL of the page may change based on application state and context. You might have multiple copies of the same site --*dev/test/live*-- with different TLDs for each: *<https://test.example.com/node/42>* vs *<https://www.example.com/node/42>*. Or, your application might live in a subdirectory, <https://example.com/drupal/node/42>
- Content pages can have user-configurable aliases, but you might still need a consistent way to link to them. Routes provide a canonical location; the URL generator can transform a route into an appropriate URL. For example: *<https://example.com/about>* which is actually node "42".
- Links displayed in content might need to have cacheability metadata associated with them
- Links and URLs generated from user input should be sanitized before use
- Links are HTML markup, and should therefore be [render arrays](https://drupalize.me/tutorial/what-are-render-arrays)

## URLs vs. Links

URLs in Drupal are represented as value objects and can be generated using the `\Drupal\Core\Url` class. This should be used whenever you need a URL in a non-HTML context. For example, help text where you actually want to display the URL and not have it be linked. Or when determining the path for a redirect.

**Rule of thumb:** If you just want the URL, use the `Url` class.

Links are HTML markup, albeit very small chunks, and should therefore be represented as [render arrays](https://drupalize.me/tutorial/what-are-render-arrays) any time they are going to be displayed in the context of HTML. The `\Drupal\Core\Link` class provides helpers for quickly creating link content.

**Rule of thumb:** If you want to display a link that someone can follow by clicking on it, use the `Link` class.

## Generating URLs

The `\Drupal\Core\Url` class has a bunch of factory methods for generating URL objects. Once you've got a URL object you can convert it to a string or use it to create a link.

For URIs that are external to Drupal, don't have a corresponding route (e.g. *robots.txt*), are based on user input *and* point at something internal, or represent a Drupal entity you can use `\Drupal\Core\Url::fromUri()`.

### Example using an external URI

```
$url = Url::fromUri('https://drupal.org/about');
```

The rest of these examples work by adding 1 of 3 different schemes as a prefix to the URI pattern.

### Example using an un-routed internal URI

```
$url = Url::fromUri('base:/robots.txt');
```

### Example using user-input for an internal path

```
$url = Url::fromUri('internal:/about/contact');
```

### Example using entity scheme

This exists as a shortcut for creating URLs to entities by following a known pattern.

```
// Pattern is "entity:{entity_type}/{entity_id}"
$url = Url::fromUri('entity:node/42');
```

## Internal route URIs

For URIs that represent an internal Drupal route, which is pretty much everything you might link to within your application itself, you should use `\Drupal\Core\Url::fromRoute()`.

### Examples

```
// From route with no parameters.
$url = Url::fromRoute('contact.site_page');
// From route with additional parameters.
$url = Url::fromRoute('entity.node.canonical', ['node' => 42]);
```

Both of the above factory methods take an optional `$options` argument which can be used to add query string parameters or URL fragments to a URL.

### Example linking to a page with a fragment appended

```
$options = ['fragment' => 'feedback'];
$url = Url::fromRoute('entity.node.canonical', ['node' => 42], $options);
```

Result:

```
/node/42#feedback
```

### Example linking to a page with a query string appended

```
$options = ['query' => ['name' => 'joe', 'hats' => 'no']];
$url = Url::fromRoute('entity.node.canonical', ['node' => 42], $options);
```

Result:

```
/node/42?name=joe&hats=no
```

## Render a link

As mentioned above, links are HTML and should therefore be output as [render arrays](https://drupalize.me/tutorial/what-are-render-arrays). There is a `'#type' => 'link'` [render element](https://drupalize.me/tutorial/what-are-render-arrays) you can use.

Using a `#link` element in a render array. See `\Drupal\Core\Render\Element\Link`.

Here's an example of what this looks like as a render array:

```
$build['link'] = [
  '#type' => 'link',
  '#title' => $this->t('A link to example.com'),
  '#url' => Url::fromUri('https://example.com'),
];
```

You can and should use the factory methods of the `\Drupal\Core\Link` class to create a link object, then use the `Link::toRenderable()` method to help with this.

### Examples of creating links

Create a link to an internal route without having to first generate a URL object:

```
$link = Link::createFromRoute('Text of the link', 'entity.node.canonical', ['node' => 42]);
```

Or, create a link from a string of text and any URL object:

```
$url = Url::fromUri('https://drupal.org/about');
$link = Link::fromTextAndUrl('Text to display', $url);
```

### Examples of converting `Link` objects

Once you've got a `Link` object you can **convert it to a render array**. This is the preferred method for displaying links.

```
$build['link'] = $link->toRenderable();
// Optionally add attributes to the link element.
$build['link']['#attributes'] = ['class' => ['my-link'], 'data-id' => $id];
```

Or you can **output it as a string**.

```
$output = $link->toString();
```

## Additional examples

Entity objects all have an `$entity->toUrl()` and `$entity->toLink()` methods. So if you're already working with an entity object this is a quick way to get a URL or Link object pointing to the entity without having to figure out the appropriate route and parameters.

You can also print links within a Twig template.

```
<a href="{{ url('entity.node.canonical', {'node': node.id }) }}">{{ 'This is a link'|t }}</a>
```

For more details on the handling links in Twig templates see [Create Links with Twig in a Template File](https://drupalize.me/tutorial/create-links-twig-template-file).

Adding links inside a `t()` method requires using a placeholder and passing the link in a string.

```
use Drupal\Core\Link;
use Drupal\Core\Url;
$link = Link::fromTextAndUrl('This is a link', Url::fromRoute('entity.node.canonical', ['node' => 1]));
$this->t('You can click this %link' ['%link' => $link->toString()]);
```

## A few final notes

You might be wondering if there is a service you should use with your controller for these utilities. Links and URLs are generally considered *value objects* and therefore don't need to be injected. You can, and should, just use the classes directly.

```
use \Drupal\Core\Url;
use \Drupal\Core\Link;
```

There are a whole lot of deprecated methods for creating links which still work, but you shouldn't use them. This is a result of the long, and winding, path from the Drupal 7 link generation code to present Drupal code and trying to maintain compatibility during the transition. The information above represents the currently recommended way of creating links and ensures that the code you write will be compatible going forward. You can also read [more about the deprecated options](https://www.drupal.org/node/2491981).

## Recap

Linking to things within the content output by a module requires that you:

1. Determine whether the thing you're linking to is internal and represented by a route, or external.
2. Use one of the factory methods of the `\Drupal\Core\Url` class to generate a URL object.
3. Use the `\Drupal\Core\Link` class to convert a URL object to a renderable array for display.

## Further your understanding

- Can you create a module with a controller that returns a page that displays a link to an external page like *<https://drupal.org>*, and an internal page like */user/1*?
- How would you create a link that points to the front page of your Drupal application?

## Additional resources

- Documentation for the [`Url::fromUri()`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Url.php/function/Url%3A%3AfromUri/) method contains information about the additional options you can use when creating a URL-like fragment and query.

The examples above were gathered from various places including:

- [Change record: l() and url() are removed in favor of a routing based URL generation API](https://www.drupal.org/node/2346779) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add Classes and HTML Attributes to Render Arrays](/tutorial/add-classes-and-html-attributes-render-arrays?p=3252)

Next
[Get Information about the Current User](/tutorial/get-information-about-current-user?p=3252)

Clear History

Ask Drupalize.Me AI

close