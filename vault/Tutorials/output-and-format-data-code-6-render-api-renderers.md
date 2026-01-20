---
title: "Render API Renderers"
url: "https://drupalize.me/tutorial/render-api-renderers?p=2775"
guide: "[[output-and-format-data-code]]"
order: 6
---

# Render API Renderers

## Content

Renderers are the services that take a [render array](https://drupalize.me/tutorial/what-are-render-arrays) and convert it to HTML (or JSON, or any other format). As a module developer, understanding how they work will help you gain a better understanding of what happens behind the scenes when Drupal links an incoming request to your custom controller and then handles the data you return.

In this tutorial we'll:

- Define renderers
- List the renderers available in Drupal core
- Demonstrate how you can create a link that forces the use of a different renderer

By the end of this tutorial, you should understand the role that renderers play in the Drupal render pipeline and when you might want to use one other than the default.

## Goal

Take a closer look at how structured data is converted to HTML or other formats by the Render API and the role of renderers in that process.

## Prerequisites

- [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays)

## What are renderers?

Renderers convert render arrays into HTML.

Renderers are implementations of [`Drupal\Core\Render\RendererInterface`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21RendererInterface.php/interface/RendererInterface/) that are capable of recursively traversing a render array and converting it to the desired output. Renderers are defined by modules as tagged services.

The most commonly used renderers are main content renderers. These are renderers that implement [`Drupal\Core\Render\MainContent\MainContentRendererInterface`](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Render!MainContent!MainContentRendererInterface.php/interface/MainContentRendererInterface/) and are able to render the main content (as received from controllers) into a response of a certain format (HTML, JSON, etc.).

Drupal core contains four `MainContent` renderers and supports rendering into any of the following formats:

- HtmlRenderer (`text/html`)
- AjaxRenderer (`application/vnd.drupal-ajax`)
- DialogRenderer (`application/vnd.drupal-dialog`)
- ModalRenderer (`application/vnd.drupal-modal`)

## Render an array

If you've got a render array, and you just want to convert it to HTML, use the `renderer` service to access `\Drupal\Core\Render\Renderer`.

```
$build['list'] = [
  '#theme' => 'item_list',
  '#items' => $items,
  '#attached' = ['library' => ['custom/styles']],
];

// Convert $build to HTML and attach any asset libraries.
$html = \Drupal::service('renderer')->renderRoot($build['list']);
// Convert to HTML, ignore asset libraries. Useful when you need just the HTML
// and don't care about attached assets.
$plain = \Drupal::service('renderer')->renderPlain($build['list']);
```

## Render a response

Controllers in Drupal that are responsible for responding to an incoming request for a route can return their response in one of two ways: either as a `\Symfony\Component\HttpFoundation\Response` object, or as a "main content" [renderable array](https://drupalize.me/tutorial/what-are-render-arrays). That is, the content that should be displayed within the system content block on the page.

The latter, returning a render array, is far more common in Drupal modules and the most likely way that your custom controller will return its response for a route. When the controller returns a render array the [`MainContentViewSubscriber`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21EventSubscriber%21MainContentViewSubscriber.php/class/MainContentViewSubscriber/) matches the request format (HTML, JSON, etc.) with a main content renderer service that implements the `MainContentRendererInterface`. This selection is generally done by looking at the `?_wrapper_format=` query string parameter, or falling back to the default `HtmlRenderer` if it's not present.

Most renderers act like a wrapper. They take the main content returned from a controller and convert that to HTML, then, depending on the requested format, they wrap that HTML up in a different package. The default `HtmlRenderer` wraps the main content with the rest of the blocks and regions that make up the page you're viewing. Alternative renderers come into play when for some reason or another you want to change the packaging. The most common use case is returning just the "main content" without all the regions and blocks wrapping it, along with some AJAX commands, and/or JavaScript to execute along with the response.

Different renderers allow the same route to be used to retrieve the "main content" in different contexts, which means less code duplication. For example, an AJAX request to a URL, with the intent of displaying any content returned within a modal, doesn't need to include the contents of all the regions and blocks that exist on the page, just the response from the controller associated with the route.

## Create a link that uses a different renderer

Output a link that when clicked opens the linked route in a modal window.

### PHP

Note: You will need to add this use statement above your class declaration:

```
use Drupal\Component\Serialization\Json;
```

The `$build` array (see also inline code comments):

```
$build['node_add_dialog'] = [
  '#type' => 'link',
  '#title' => $this->t('Some text'),
  // $this->getDestinationArray() is used to create a ?destination= style query
  // string so that after a form is submitted in the modal you return to the
  // current page.
  '#url' => Url::fromRoute('node.add', ['node_type' => 'article'], ['query' => $this->getDestinationArray()]),
  '#options' => [
    'attributes' => [
      // Adding the class 'use-ajax' tells the Drupal AJAX system to process
      // this link, and bind an event handler so that when someone clicks on the
      // link we make an AJAX request instead of just linking to the URL
      // directly.
      'class' => ['use-ajax'],
      // This data attribute tells Drupal to use the ModalRenderer
      // (application/vnd.drupal-modal) to handle this particular request rather
      // then the normal MainContentRenderer.
      'data-dialog-type' => 'modal',
      // This contains settings to pass to the Drupal modal dialog JavaScript,
      // in this case setting the width of the modal window that'll be opened.
      'data-dialog-options' => Json::encode(['width' => 700]),
    ],
  ],
  // In order for the above classes and data attributes to do anything we also
  // need to attach the relevant JavaScript.
  '#attached' => ['library' => ['core/drupal.dialog.ajax']],
];
```

### HTML

```
<a href="/node/add/article?destination=/drupal_dev/HEAD/examples/render_example/arrays" class="use-ajax" data-dialog-type="modal" data-dialog-options="{&quot;width&quot;:700}">Some text</a>
```

## Web services and renderers

Because this can be a point of confusion, note that renderers as discussed here have little to do with Drupal's web services APIs. You'll often hear about how render arrays can be "rendered in many different formats", and this is often misinterpreted as "because your content is a render array it can be rendered as JSON data for a RESTful web service." When we say "different formats" in this context we're referring to the above formats like `text/html`, or `application/vnd.drupal-ajax`.

If you're interested in learning more about how [Entities](https://drupalize.me/tutorial/entity-api-overview) and their contents are converted to JSON for things like web services you're probably looking for the [Serialization API](https://www.drupal.org/docs/drupal-apis/serialization-api).

## Recap

In this tutorial, we said that renderers are the code responsible for converting a render array into its HTML (or other format) representation. They work by recursing through the structured data and converting each child element, starting at the bottom of the tree. Main content renderers are the most commonly used. They convert the render array returned by a controller into a proper response. This might be a complete HTML document with all the regions and blocks that make up the current page, or a stripped down version of the content suitable for use in a modal window.

## Further your understanding

- What renderer would be used to display the content for a route in a modal dialog? How is this renderer different than the default?
- This article, [Launching an AJAX modal from a WYSIWYG link and customising the response with MainContentRendererInterface in Drupal 8](https://www.previousnext.com.au/blog/launching-ajax-modal-from-wyswiyg-link-and-customising-response-maincontentrendererinterface), provides an example use case and instructions for defining a custom renderer
- You can view the output from any page using a different renderer by appending the query string `?_wrapper_format=drupal_modal` or another renderer ID. It's not really that useful, but gives you an idea of what's happening
- Read more about the Drupal render pipeline and the use of renderers in our tutorial [Render Pipeline](https://drupalize.me/tutorial/render-pipeline) and [in the documentation](https://www.drupal.org/docs/8/api/render-api/the-drupal-8-render-pipeline).

## Additional resources

- [Documentation for Renderer::render()](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Renderer.php/function/Renderer%3A%3Arender/) provides some good information on the process that Drupal goes through when converting an array to HTML (Drupal.org)
- [Understanding BigPipe vs. SingleFlush render strategies, and #lazy\_builder](https://www.youtube.com/watch?v=NHe9JtIp5fk) (youtube.com)
- [Modal/dialog/ajax is using query parameters instead of accept headers](https://www.drupal.org/node/2488192) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Render Pipeline](/tutorial/render-pipeline?p=2775)

Next
[Render API Callback Properties](/tutorial/render-api-callback-properties?p=2775)

Clear History

Ask Drupalize.Me AI

close