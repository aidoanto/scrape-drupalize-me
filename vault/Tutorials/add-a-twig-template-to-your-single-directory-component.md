---
title: "Add a Twig Template to Your Single Directory Component"
url: "https://drupalize.me/tutorial/add-twig-template-your-single-directory-component?p=3329"
guide: "[[frontend-theming]]"
---

# Add a Twig Template to Your Single Directory Component

## Content

Drupal single directory components use Twig template files to define their HTML markup and how the values of props and slots are displayed. To discover available props and slots, read the component’s *.component.yml* file. When working with slots, you’ll often choose between rendering a slot as a Twig block (`{% block %}`) or interpolating a variable directly (`{{ variable }}`).

In this tutorial, you’ll:

- Add a *card.twig* file to an existing component directory.
- Read the associated *card.component.yml* schema to identify props and slots you can work with.
- Render props and slots wrapped in custom HTML markup.

By the end of this tutorial, you’ll be able to connect a Twig template to any SDC and render the props and slots passed into the component.

## Goal

Add a Twig template to your SDC, render its props and slots, choose `{{ content }}` or `{% block content %}` as appropriate, and understand how that choice affects how the component is used elsewhere.

## Prerequisites

- [Anatomy of a Drupal Single Directory Component (SDC)](https://drupalize.me/tutorial/anatomy-drupal-single-directory-component-sdc)
- (Optional) [Create Your First Drupal Single Directory Component (SDC)](https://drupalize.me/tutorial/create-your-first-drupal-single-directory-component-sdc)
- [Add a Component YAML File for a Drupal SDC](https://drupalize.me/tutorial/add-component-yaml-file-drupal-sdc)
- [Understanding Props and Slots in Drupal Single Directory Components](https://drupalize.me/tutorial/understanding-props-and-slots-drupal-single-directory-components)
- (Optional) [Configure Your Environment for Theme Development](https://drupalize.me/tutorial/configure-your-environment-theme-development)

## Add markup to the card component

In [the previous tutorial](https://drupalize.me/tutorial/add-component-yaml-file-drupal-sdc) you created a *card.component.yml* file that defines the schema for a card component. Now you’ll take the props and slots that contain dynamic values and output them wrapped in the appropriate HTML markup. This tutorial assumes you’ve already created the directory *components/card/* in your module or theme, and that it contains a *card.component.yml* file populated with the content we added in [Add a Component YAML File for a Drupal SDC](https://drupalize.me/tutorial/add-component-yaml-file-drupal-sdc).

## Create a *card.twig* file

Let's create a Twig template file in our card SDC that outputs the HTML markup for the component.

### Name and place the *.twig* file

Every SDC has a single *.twig* template file. Create the Twig file next to your *.component.yml* file, following the naming convention *{component}.twig*. Use the same directory as the [previously-created](https://drupalize.me/tutorial/add-component-yaml-file-drupal-sdc) *card.component.yml*.

```
my_theme_or_module/
└── components/
    └── card/
        ├── card.component.yml
        └── card.twig
```

### Figure out prop and slot names

To figure out the variables available in your Twig template, let's take a look at the card component’s props and slots in *card.component.yml*.

Here’s an excerpt showing the props and slots of our card component:

```
props:
  properties:
    heading:
      type: string
    url:
      type: string
    card_links:
      type: array
    show_flip_button:
      type: boolean
    count:
      type: integer
    metadata:
      type: object
  required:
    - heading
    - url
slots:
  content:
    title: Content
  body:
    title: Card body
```

- The keys under `props.properties` (`heading`, `url`, and `card_links`, etc.) and under `slots` (`content`) **are the variable names** you will use in your component's template file.
- `props` are strongly typed dynamic inputs you pass.
- `slots` are placeholders for arbitrary markup or nested single directory components.
- Required props appear under `props.required`. In Twig, it’s safe to use a required value directly; for optional props, use a conditional or provide a default.

**Note:** The *.component.yml* file should document all of an SDC’s props and slots, but schemas aren’t the only allowed inputs—Drupal validates what you pass, and undeclared values can still be present. As an SDC author, avoid confusion by defining all props and slots in the schema.

### Work with prop values

Props are strongly typed, and some may be marked as required. To output a prop value in markup, use standard Twig interpolation:

```
<h2>{{ heading }}</h2>
```

Props aren’t always displayed; they often control logic. For example, a boolean flag that enables or disables a feature:

```
{% if show_flip_button %}
  <button class="card-btn" type="button">Add to favorites</button>
{% endif %}
```

Or to set a class:

```
<div class="card{% if show_flip_button %} card--flippable{% endif %}">
  {{ content }}
</div>
```

### Work with slot values

Slots allow passing content into a component when the structure of the content is unknown. A card’s body might be plain text—or it might include links and images. It can be any arbitrary HTML or a nested component.

Slots are typically output in one of two ways:

#### Via interpolation

```
<div>
  {{ content }}
</div>
```

#### As a Twig block

```
<div>
  {% block content %}{% endblock %}
</div>
```

There isn’t one “best” approach; choose based on how the component will likely be used.

This distinction mainly applies when the component is used in another Twig template (for example, a theme’s *node.html.twig*). When a component is used as part of a render array, it matters less.

**tl;dr** (flexible default):

```
<div>
  {% block content %}
    {{ content }}
  {% endblock %}
</div>
```

- If you only output `{% block content %}{% endblock %}`, callers must use `embed` to override the block.
- If you output `{{ content }}`, callers can use either `include` (passing a slot variable) or `embed`.
- If you output `{% block content %}{{ content }}{% endblock %}`, callers can use either `include` or `embed`. This is the most flexible for a “blob of content” slot.
- Use a `{% block %}` when you want to provide a default that can be overridden.

Here are a couple of common examples.

If you’re not sure, this is the most flexible approach. It allows consumers to use either `include` or `embed`:

```
<div>
  {% block content %}
    {{ content }}
  {% endblock %}
</div>
```

A footer with a default “Read more” button that uses a `link_url_prop` prop. Callers can override it via the `footer` slot:

```
<footer>
  {% block footer %}
    <a class="btn" href="{{ link_url_prop }}">Read full story</a>
  {% endblock %}
</footer>
```

### Final card component markup

Here’s the final markup for our *card.twig* template file, taking into account all the props and slots defined in the *card.component.yml* file:

```
{#
Set a default value if none is provided.
#}
{% if count is not defined %}
  {% set count = 1 %}
{% endif %}

<article class="card" data-count="{{ count }}">
  <div class="card-count">#{{ count }}</div>

  <div class="card-inner">
    <!-- FRONT -->
    <div class="card-front">
      {% if metadata.author or metadata.date %}
        <div class="card-meta">
          {% if metadata.author %}<span class="card-author">By {{ metadata.author }}</span>{% endif %}
          {# Convert YYYY-MM-DD to a timestamp, then to the site's "medium" display format #}
          {% if metadata.date %}
            {% set published = metadata.date|date('U')|format_date('medium') %}
            <span class="card-date"> on {{ published }}</span>
          {% endif %}
        </div>
      {% endif %}
      <h2 class="card-title">
        <a href="{{ url }}">{{ heading }}</a>
      </h2>
      <div class="card-content">
        {% block content %}
          {{ content }}
        {% endblock %}
      </div>
      {#
      If showing the flip button, show that on the front but skip the related
      links and put them on the back instead. If not showing the flip button,
      and there are links, show them here.
      #}
      {% if show_flip_button %}
        <button class="flip-button" type="button">Flip</button>
      {% else %}
        {% if card_links %}
          <div class="card-content">
            <ul class="card-links">
              {% for link in card_links %}
                <li><a href="{{ link.url }}">{{ link.title }}</a></li>
              {% endfor %}
            </ul>
          </div>
        {% endif %}
      {% endif %}
    </div>

    {#
    Back of the card is only shown if there is a button to flip it over.
    #}
    {% if show_flip_button %}
      <!-- BACK -->
      <div class="card-back">
        <h2 class="card-title">{{ heading }}</h2>
        {% if card_links %}
          <div class="card-content">
            <ul class="card-links">
              {% for link in card_links %}
                <li><a href="{{ link.url }}">{{ link.title }}</a></li>
              {% endfor %}
            </ul>
          </div>
        {% endif %}
        <button class="flip-button" type="button">Flip back</button>
      </div>
    {% endif %}

  </div>
</article>
```

This is a little more complex than a standard card, but it demonstrates several patterns and sets us up to add JavaScript interactivity in a later tutorial.

**Note:** We pass `metadata.date` as `YYYY-MM-DD` for schema validation, then convert it for display inside the component:

```
metadata.date|date('U')|format_date('medium')
```

This keeps validation strict while showing a reader-friendly date.

### Use it in a *node.html.twig* template

To see this SDC in action, update the *node--card.html.twig* template file (created in [Create Your First Drupal Single Directory Component (SDC)](https://drupalize.me/tutorial/create-your-first-drupal-single-directory-component-sdc)) with the following code:

```
{% set card_links = [
  { title: 'Read more', url: path('entity.node.canonical', { node: node.id() }) }
] %}

{{ include('neo_brutalism:card', {
  heading: label,
  url: path('entity.node.canonical', { node: node.id() }),
  card_links: card_links,
  show_flip_button: true,
  metadata: {
    author: node.uid.entity ? node.uid.entity.label : null,
    date: node.getCreatedTime()|format_date('custom', 'Y-m-d'),
  },
  content: content
}, with_context = false) }}
```

**Note:** The `card.component.yml` schema uses `format: uri-reference` for `card_links[].url`, which allows relative paths (for example, `/node/123`) or absolute URLs. The `metadata.date` prop expects `YYYY-MM-DD`, so we use `format_date('custom', 'Y-m-d')` in the include above.

Image

![Screenshot of card component in all its unstyled glory](../assets/images/add-twig-card-component.png)

### Clear the cache

Run the following command so Drupal recognizes the new component template file:

```
drush cr
```

Now that you’ve got a working Twig template for your component, you can:

- Learn about [using components in a Twig template](https://drupalize.me/tutorial/use-component-twig-template), or [as part of a render array](https://drupalize.me/tutorial/use-component-module-render-arrays).
- [Add CSS and JavaScript to a Drupal SDC](https://drupalize.me/tutorial/add-css-and-javascript-drupal-sdc).

## Recap

In this tutorial, you created a Twig template for a card single directory component, placed and named it so Drupal can find it, read the list of props and slots from a *.component.yml* file to know what variables are available, and used those values to generate the component’s markup—including different ways to print slots.

## Further your understanding

- Can you explain how the way a slot is printed in a Twig template changes how an SDC is used by consumers?
- Try replacing the flip button in the card SDC with a nested button SDC.

## Additional resources

- [Using Single Directory Components](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components/quickstart) (Drupal.org)
- The [SDC Examples module](https://drupal.org/project/sdc_examples) has numerous example *.twig* files to learn from. (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add a Component YAML File for a Drupal SDC](/tutorial/add-component-yaml-file-drupal-sdc?p=3329)

Next
[Add CSS and JavaScript to a Drupal SDC](/tutorial/add-css-and-javascript-drupal-sdc?p=3329)

Clear History

Ask Drupalize.Me AI

close