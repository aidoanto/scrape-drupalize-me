---
title: "Render Pipeline"
url: "https://drupalize.me/tutorial/render-pipeline?p=2775"
guide: "[[output-and-format-data-code]]"
---

# Render Pipeline

## Content

This tutorial looks at the steps that Drupal goes through to obtain a render array for an incoming HTTP request, transform the render array into HTML, and then return it to your browser. We provide an outline of the process and links to resources for more in-depth information. We also take a more thorough look at the `HtmlRenderer` which converts a render array into HTML. Knowing how the render arrays you write in your code are ultimately used can help you optimize Drupal's Render API to describe your module's content.

## Goal

Understand the process that Drupal goes through to convert a request into a valid response, and how that relates to Drupal's Render API.

## Prerequisites

- [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays)
- [What Are Render Elements?](https://drupalize.me/tutorial/what-are-render-elements)

The render pipeline is the process that Drupal goes through to convert an HTTP request into a valid response, effectively how Drupal renders an HTML page for your browser.

At a very high level, the system consists of the following steps:

1. Receive an HTTP request in the form of a `Request` object
2. Call appropriate controller based on route. Controller returns a render array
3. Trigger a `VIEW` event
4. `\Drupal\Core\EventSubscriber\MainContentViewSubscriber` determines which content renderer to use based on format negotiation. (e.g. HTML vs. JSON)
5. `RenderEvents::SELECT_PAGE_DISPLAY_VARIANT` event used to determine which page layout variant to use. For example, if the blocks module is enabled, use `BlockPageVariant` and add blocks to decorate the page. Also allows modules like Panels or Page Manager to provide their own page variants.
6. Renderer is used to convert the render array returned by the controller into a string of content
7. A `Response` object containing the generated content is sent back to the requesting client

This process is documented in detail on Drupal.org starting with [The Drupal 8 render pipeline](https://www.drupal.org/docs/8/api/render-api/the-drupal-8-render-pipeline). And this talk, [Drupal 8's render pipeline](https://www.youtube.com/watch?v=CIxYGqY8nPs) goes into even more depth. It's from 2015, but still accurate. We would rate this as "useful to know, but probably not required" unless you're *really* curious about how Drupal services a request from beginning to end.

## The renderer

We do think it is valuable to fully understand how the HTML Renderer (`\Drupal\Core\Render\MainContent\HtmlRenderer`) in particular converts a render array into HTML. This is step #6 in the outline above. Knowing this, you'll better understand how render arrays are used, and therefore how to describe your module's content, or manipulate the content of another module.

The following illustration depicts the path used to render an array to HTML:

Image

![Flow chart showing steps that HtmlRenderer goes through. See HtmlRenderer::render() documentation](/sites/default/files/styles/max_800w/public/tutorials/images/render-api-flowchart.png?itok=GlmAsiKF)

[View full size image](https://drupalize.me/sites/default/files/tutorials/images/render-api-flowchart.png).

The [documentation for \Drupal\Core\Render\RendererInterface::render()](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Renderer.php/function/Renderer%3A%3Arender) goes over this in detail as well.

For more on the role of renderers, how they work, and using other renderers read our tutorial [Render API Renderers](https://drupalize.me/tutorial/render-api-renderers).

## Recap

This tutorial outlines the process that Drupal goes through to convert an incoming request into a render array, transform the render array into HTML, and return a response. It includes links to useful documentation for anyone who wants to understand the process in-depth. This isn't likely required knowledge for most module developers, but understanding it will absolutely help you learn to make better use of render arrays in your own code.

## Further your understanding

- Stepping through the rendering process in a debugger can be an informative exercise. Start by setting a breakpoint in `\Drupal\Core\Render\MainContent\HtmlRenderer::renderResponse()`, maybe on the line `$this->renderer->render()`
- [Learn about the use of placeholders to improve rendering times](https://drupalize.me/tutorial/use-lazy-builders-and-placeholders)

## Additional resources

- [The Drupal 8 render pipeline](https://www.drupal.org/docs/8/api/render-api/the-drupal-8-render-pipeline) (Drupal.org)
- [Documentation for \Drupal\Core\Render\RendererInterface::render()](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21Renderer.php/function/Renderer%3A%3Arender) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Define a New Render Element Type](/tutorial/define-new-render-element-type?p=2775)

Next
[Render API Renderers](/tutorial/render-api-renderers?p=2775)

Clear History

Ask Drupalize.Me AI

close