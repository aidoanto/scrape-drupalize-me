---
title: "Use a Component in a Twig Template"
url: "https://drupalize.me/tutorial/use-component-twig-template?p=3329"
guide: "[[frontend-theming]]"
---

# Use a Component in a Twig Template

## Content

Learn how to embed a Drupal single directory component (SDC) in a Twig template like *node.html.twig*. This tutorial explains how to pass props and slots to the component, how to determine the correct namespace and name, and how to choose between Twig’s `{% include %}` and `{% embed %}` when rendering an SDC. This technique is most often used by theme developers who override templates and compose a page using single directory components. A common scenario is expressing your design system as components in a theme, then overriding templates to use those components.

In this tutorial, we will:

- Reference a component from a parent Twig template file.
- Pass props and slot values to a component from that template.
- Decide when to use `{% include %}` or `{% embed %}` based on the component's slot structure.

By the end of this tutorial, you’ll be able to embed a component into a Twig template and pass values to both its props and slots.

## Goal

Create a *node--card.html.twig* template file that uses a Drupal single directory component named *card* to render nodes.

## Prerequisites

- Experience with [Drupal theme development](https://drupalize.me/guide/frontend-theming)
- Familiarity with [Twig](https://drupalize.me/topic/template-design-twig) syntax
- A working single directory component (SDC) with the provided schema in your enabled module or theme.
- [Add a Component YAML File for a Drupal SDC](https://drupalize.me/tutorial/add-component-yaml-file-drupal-sdc)
- [Add a Twig Template to Your Single Directory Component](https://drupalize.me/tutorial/add-twig-template-your-single-directory-component)
- [Add CSS and JavaScript to a Drupal SDC](https://drupalize.me/tutorial/add-css-and-javascript-drupal-sdc)
- [Configure Your Environment for Theme Development](https://drupalize.me/tutorial/configure-your-environment-theme-development)

## Common use cases for Drupal SDCs

Whenever possible, put your custom markup, CSS, and JavaScript into single directory components (SDCs). Then use a combination of template overrides (that call SDCs) and layout tools that support SDCs to compose your pages. This approach plays nicely with tools like Layout Builder today—and Drupal Canvas as it matures.

A common scenario: your site has a *Card* view mode for nodes and a *card* SDC in your design system. You want the view mode’s markup to come from the single directory component. Create a view-mode-specific template, e.g. *node--card.html.twig*, and render the *card* SDC from there—bridging traditional Twig templates and SDCs. This is what we did in [Create Your First Drupal Single Directory Component (SDC)](https://drupalize.me/tutorial/create-your-first-drupal-single-directory-component-sdc).

Another common use case: theme node entities via *node.html.twig* and use SDCs for field formatting, calls-to-action (CTAs), headers, and so on. Override the template and embed SDCs using Twig features. That’s what we’ll demonstrate here.

The nice thing about an SDC-based approach: you can override a template today and switch to a layout builder later. Tools like Layout Builder—and Drupal Canvas when it arrives—integrate with the same SDCs.

To use an SDC in Twig, you’ll typically choose one of:

- `{% include 'theme_name:component_name' with { props } only %}` to pass props and slots to the component, or
- `{% embed 'theme_name:component_name' with { props } only %}` if you need to override Twig-block-based slots.

Which you use depends on how the component’s slots are defined. We'll demonstrate that below.

### Read the *.component.yml* file

Each SDC includes a *.component.yml* file that defines the names of props and slots that the component expects. Use this file to learn what values are available and required.

For example:

```
props:
  type: object
  properties:
    heading:
      type: string
    url:
      type: string
    show_flip_button:
      type: boolean
  required:
    - heading
    - url
slots:
  content:
    title: Content
```

This tells you the component expects a `heading`, `url`, and optionally `show_flip_button`, plus a `content` slot.

### Determine how the slot is defined

If the **component does not have any slots**, use `include()`.

If the component has slots, check **the component’s Twig file** (for example, *components/card/card.twig*) to see how a slot (e.g., `content`) is rendered. If it contains:

- `{{ content }}`: you can use `include()` and pass a `content` variable.
- `{% block content %}`: you must use `embed` and override that block with `{% block content %}{% endblock %}`.
- `{% block content %}{{ content }}{% endblock %}`: you can use either `embed` and override that block, or `include()`.

Props are always passed as key-value pairs.

### Find the component's provider and name

Components are referenced using the format `{provider}:{component}`. For example, `neo_brutalism:card` refers to a component named *card* inside the *components/* directory of a theme (or module) called *neo\_brutalism*. You'll need to know this because it's how we reference it in our `include()` or `embed` statements.

### Create a template for the "Card" view mode

In [Create Your First Drupal Single Directory Component (SDC)](https://drupalize.me/tutorial/create-your-first-drupal-single-directory-component-sdc) we created both the *Card* view mode and the *templates/node--card.html.twig*, so you may already have this in your theme. If so, **skip this step**.

This step assumes your site has been configured with a view mode named *Card*.

In your theme, create the file *templates/content/node--card.html.twig*, and clear caches. This uses the [template override](https://drupalize.me/tutorial/override-template-file) feature and tells Drupal that whenever it displays a node in the *Card* view mode it should use this template. This leverages the default [theme hook suggestion](https://drupalize.me/tutorial/discover-existing-theme-hook-suggestions) `node--{VIEW_MODE}.html.twig`.

### Render the component in the Twig template file

Now that we have a Twig template file, and we know the name plus slots/props for the SDC we want to use, we can edit *node--card.html.twig*. Regarding how to pass slots, the component’s *card.twig* defines the `content` slot like this:

```
{% block content %}
  {{ content }}
{% endblock %}
```

Which means we can use either `include()` or `embed`.

Edit *node--card.html.twig* to look like one of the following options.

#### Option A: Use `include()`

Use `include()` and pass the `content` slot as a variable:

```
{# themes/custom/your_theme/templates/node--card.html.twig #}
{% set card_links = [{
  title: "Read more",
  url: url
}] %}

{{ include('neo_brutalism:card', {
  heading: label,
  url: url,
  card_links: card_links,
  show_flip_button: true,
  content: content
}, with_context = false) }}
```

The use of `with_context = false` is optional but recommended because it prevents variable leakage. By default, Twig `include` passes all variables from the parent scope. Here, we pass **only** what we specify. The `with … only` in the `embed` example in the next option has the same effect. Sometimes you do want everything; for example, if your theme has an SDC that is a one-to-one replacement for *node.html.twig* you could do `include('my_theme:node')` as the entire template. (See the [Radix contributed theme](https://www.drupal.org/project/radix) which implements this approach.)

#### Option B: Use `embed`

Alternatively, use `embed` and override the `content` block:

```
{# themes/custom/your_theme/templates/node--card.html.twig #}
{% set card_links = [{
  title: "Read more",
  url: url
}] %}

{% embed 'neo_brutalism:card' with {
  heading: label,
  url: url,
  card_links: card_links,
  show_flip_button: true,
  content: content
} only %}
  {% block content %}
    <h3>Content:</h3>
    {{ content }}
  {% endblock %}
{% endembed %}
```

**Tip:** If your template doesn’t already have a `url` variable, define one:

```
{# Ensure `url` exists. Many node templates already provide it. #}
{% if url is not defined and node is defined %}
{% set url = path('entity.node.canonical', { node: node.id() }) %}
{% endif %}
```

**Note:** While our example renders a single SDC, you can use multiple components in one template.

### Test it out

To verify this is working we need to visit a page on your site that displays one or more nodes using card view mode so that the *node--card.html.twig* template file is used to render the node and the *neo\_brutalism:card* SDC is embedded from there. An easy way to do that is to edit the default front page View (if you're still using it) and change the format to an *Unformatted list* that shows entities using the *Content view mode* for rows with *Card* selected as the *View mode* for *Row style options*.

The result should be a list of nodes rendered with the *Card* view mode—using your custom SDC.

Image

![The frontpage view using the card view mode which uses the card SDC](../assets/images/use-sdc-twig--final-result.png)

## Troubleshooting

When you render an SDC via `include()` or `embed`, Drupal validates props against the schema. If types or formats don’t match, you’ll see an `InvalidComponentException`.

### Missing props

If you see an error like:

```
Component render failed: Missing required prop: heading
```

That usually means the component is expecting a prop that wasn’t passed in. Double-check the *.component.yml* to ensure you’re passing all required props and that names match exactly.

### Format and validation errors

Validation happens in Twig, too.

When you render an SDC via include() or embed, Drupal validates props against the schema. If types or formats don’t match, you’ll see an `InvalidComponentException`.

- Make sure booleans are `true`/`false` (not `"true"`/`"false"` strings).
- Pass integers/numbers as numbers, not strings.
- For optional props, guard usage with `if var is defined` or provide defaults.
- Match the schema exactly for nested objects/arrays (keys, types, required fields).

### URL formats

- If a prop uses `format: uri-reference`, relative paths like `/node/123` are valid.
- If a prop uses `format: uri`, pass an **absolute** URL.

```
{# uri-reference (relative OK) #}
{% set link = path('entity.node.canonical', { node: node.id() }) %}

{# uri (absolute required) #}
{% set link_abs = url('entity.node.canonical', { node: node.id() }) %}
```

### Date formats

If a prop uses `format: date`, pass `YYYY-MM-DD`:

```
node.getCreatedTime()|format_date('custom','Y-m-d')
```

Convert a date to a friendly display that uses user-configured date formats **inside the component**:

```
metadata.date|date('U')|format_date('medium')
```

## Recap

In this tutorial, you added a Twig template that renders content using a Drupal single directory component. You referenced the component, passed values to its props and slots, chose between `include()` and `embed` based on how the component’s slots were defined, and updated a view to test the changes.

## Further your understanding

- Can you replace *node.html.twig* entirely with a *node* component?
- Try adding custom preprocess logic for the *node--card.html.twig* to prepare props dynamically.
- Create additional SDCs (e.g., button, header, field value) and use them to compose a *node.html.twig* template’s output.

## Additional resources

- [Use a Component in a Module via Render Arrays](https://drupalize.me/tutorial/use-component-module-render-arrays) (Drupalize.Me)
- [Twig include function](https://twig.symfony.com/doc/3.x/functions/include.html) (twig.symfony.com)
- [Twig embed tag](https://twig.symfony.com/doc/3.x/tags/embed.html) (twig.symfony.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Use a Component in a Module via Render Arrays](/tutorial/use-component-module-render-arrays?p=3329)

Next
[Override an Existing Single Directory Component](/tutorial/override-existing-single-directory-component?p=3329)

Clear History

Ask Drupalize.Me AI

close