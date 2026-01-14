---
title: "Create Your First Drupal Single Directory Component (SDC)free"
url: "https://drupalize.me/tutorial/create-your-first-drupal-single-directory-component-sdc?p=3329"
guide: "[[frontend-theming]]"
order: 53
---

# Create Your First Drupal Single Directory Component (SDC)free

## Content

In this tutorial, you’ll create and render a simple single directory component (SDC) in Drupal. You’ll set up the required files, call the component from a template, and confirm that Drupal renders it with its styles automatically attached.

By following along, you will:

- Scaffold the files for a basic card component.
- Reference the component in a node template.
- See how Drupal renders the component’s HTML and CSS together.

When you’re done, you’ll have a complete working example of a Drupal single directory component.

## Goal

Create and render a basic card single directory component (SDC) to learn how its files work together and how Drupal uses them during rendering.

## Prerequisites

- [Anatomy of a Drupal Single Directory Component (SDC)](https://drupalize.me/tutorial/anatomy-drupal-single-directory-component-sdc)
- Drupal 10.3 + installed and running. See [Install Drupal Locally with DDEV](https://drupalize.me/tutorial/install-drupal-locally-ddev).
- Theme or module where you can place component files (e.g., *themes/custom/mytheme*). This tutorial uses a theme named *neo\_brutalism*. You can create your own theme with the [Starterkit theme generator](https://drupalize.me/tutorial/start-new-theme-starterkit).
- (Optional) [Configure Your Environment for Theme Development](https://drupalize.me/tutorial/configure-your-environment-theme-development)
- [Clear Drupal's Cache](https://drupalize.me/tutorial/clear-drupals-cache)
- [Concept: View Modes and Formatters](https://drupalize.me/tutorial/user-guide/structure-view-modes)

## Create the “card-simple” SDC

Let’s create a new component called `card-simple`.

### Create the component directory

Inside your custom theme or module, create the directory *components/card-simple/*. This directory will hold all the files for your new card component.

Learn more about the structure of an SDC in [Anatomy of a Drupal Single Directory Component (SDC)](https://drupalize.me/tutorial/anatomy-drupal-single-directory-component-sdc).

### Add a *.component.yml* file

Create the file, *components/card-simple/card-simple.component.yml*, with the following content:

```
$schema: https://git.drupalcode.org/project/drupal/-/raw/HEAD/core/assets/schemas/v1/metadata.schema.json
name: card-simple
description: A simple card component.

props:
  type: object
  properties:
    heading:
      type: string
      title: Heading
    url:
      type: string
      title: URL
    count:
      type: integer
      title: Count
    metadata:
      type: object
      title: Metadata

slots:
  content:
    title: Content
```

This file defines the component and the props and slots that pass dynamic content into it.

- **props:** One or more inputs for a component whose *data type and structure is well-defined*, containing **properties** which are mapped to variables in the component's Twig template file.
- **slots:** One or more inputs for a component consisting of a nested component or other *arbitrary HTML* whose data structure is unknown

We’ll go into more depth about the *.component.yml* file and defining props and slots in [Add a Component YAML File for a Drupal SDC](https://drupalize.me/tutorial/add-component-yaml-file-drupal-sdc).

### Add a Twig template file for the component

Create the file *components/card-simple/card-simple.twig* with the following content:

```
{% if count is not defined %}
  {% set count = 1 %}
{% endif %}

<article class="card-simple" data-count="{{ count }}">
  <div class="card-count">#{{ count }}</div>

  <div class="card-inner">
    <div class="card-front">
      {% if metadata.author or metadata.date %}
        <div class="card-meta">
          {% if metadata.author %}<span class="card-author">By {{ metadata.author }}</span>{% endif %}
          {% if metadata.date %}<span class="card-date"> on {{ metadata.date }}</span>{% endif %}
        </div>
      {% endif %}
      <h2 class="card-title">
        <a href="{{ url }}">{{ heading }}</a>
      </h2>
      <div class="card-content">{{ content }}</div>
    </div>
  </div>
</article>
```

This template outputs the props and slots into the card’s HTML.

### Add CSS to your component

Create the file *components/card-simple/card-simple.css* with the following content:

```
.card-simple {
  background: #fafafa;
  border: 6px solid #111111;
  box-shadow: 6px 6px 0 0 #111111;
  height: auto;
  margin: 2rem;
  padding: 1rem;
  position: relative;
  width: 300px;
}

.card-simple .card-count {
  background: #ff00cc;
  border-bottom: 4px solid #111111;
  box-shadow: -4px 4px 0 0 #111111;
  color: #fafafa;
  font-size: 0.875rem;
  font-weight: 800;
  padding: 0.25rem 0.5rem;
  position: absolute;
  right: 0;
  top: 0;
  z-index: 3;
}

.card-simple .card-meta {
  border-bottom: 2px solid #111111;
  display: flex;
  font-size: 0.875rem;
  gap: 1rem;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
}

.card-simple .card-author,
.card-simple .card-date {
  font-weight: 700;
}

.card-simple .card-title {
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  line-height: 1.75rem;
  margin: 0.75rem 0;
}

.card-simple .card-content {
  line-height: 1.4;
  padding: 0 1rem 1rem;
}
```

This file contains styles that Drupal will automatically attach whenever the component is rendered.

We’ll expand on adding CSS and JavaScript assets to a component in [Add CSS and JavaScript to a Drupal SDC](https://drupalize.me/tutorial/add-css-and-javascript-drupal-sdc).

### Clear caches

With the component files in place, [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) so Drupal can register your new single directory component.

```
drush cr
```

## Use the SDC in a node template file

By default, Drupal won’t use a component unless it’s referenced in a template. In this following steps, you’ll connect your card component to a custom node template for the card view mode, so you can see the SDC in action.

### Create a card view mode for nodes

A custom view mode lets you control when a specific template is used.

1. Go to *Structure* > *Display modes* > *View modes* (*admin/structure/display-modes/view*) and select *+ Add view mode*.
2. In the *Choose view mode entity type* modal, select *Content*.
3. In the *Create view mode modal*:

   - *Name:* enter *`Card`* (Drupal will create a machine name like `node.card`).
   - *Description:* optional.
   - *Enable this view mode for the following Content types:* check *Article*.
4. Click Save.
5. Go to *Structure* > *Content types* > *Article* > *Manage display*, then select the *Card* tab.
6. Move all fields **except *Body*** to the *Disabled* section. The node title is a base field (the entity label), so it doesn’t appear in Manage display. We’ll output fields and metadata directly in the template for this view mode.
7. Configure the display of the *Body* field. Hide the label and use the *Trimmed* formatter (and limit to 100 characters).
8. Save the changes to the *Card* display.

Image

![Manage display settings for Article showing Body field using Trimmed (100 characters) for the Card view mode.](../assets/images/hello-world--manage-display-settings.png)

**Note:** If you [generated demo content with Devel](https://drupalize.me/tutorial/set-demo-site-theming-practice), some content may include long summaries. The *Summary or trimmed* formatter displays the summary as-is. For a predictable excerpt in this tutorial, use the *Trimmed* formatter and limit character count as described above, or create content without a summary.

### Add a node template to your theme

Create the file *templates/content/node--card.html.twig* in your theme. (In this tutorial, our theme is *neo\_brutalism*. Replace that with your theme’s machine name.) After clearing the cache, Drupal will use this file whenever a node is rendered in the *Card* view mode.

**Note:** The template file name comes from the view mode’s machine name. For `node.card`, Drupal looks for *node--card.html.twig*. If your view mode's machine name is `node.my_card`, in this step, create the file *node--my-card.html.twig*.

Learn more about [template overrides](https://drupalize.me/tutorial/override-template-file).

Example *node--card.html.twig*:

```
{#
Renders the article using the "card-simple" component.
Change `neo_brutalism` to your theme's machine name.
#}

{{ include('neo_brutalism:card-simple', {
  heading: node.title.value,
  url: path('entity.node.canonical', { node: node.id() }),
  metadata: {
    author: node.uid.entity ? node.uid.entity.label : null,
    date: node.getCreatedTime()|format_date('medium')
  },
  content: content.body
}, with_context = false) }}
```

- `node.id` vs `node.id()`: Either will work to get the node ID. Twig's dot operator can call a no-argument method when you access an attribute; `node.id` ends up calling `id()` on `\Drupal\Core\Entity\EntityInterface::id()`.
- `date` data type: The `format_date` function needs a numeric type, so we can use `getCreatedTime()` on the node object to get a numeric timestamp that `format_date` can convert to use the "medium" date format configured in the admin UI. The function name makes it clear what is happening. You could also pass `node.created.value` to `format_date()`. If you pass `node.created` (without `.value`) to `format_date()`, you'll get a PHP error because `node.created` is a `FieldItemList` field object, not a numeric timestamp.
- Why `with_context = false` at the end of the `{{ include }}`? It prevents variables from the parent template from leaking into the component, avoiding name collisions (for example, `content`, `title`, `url`) and ensuring the component only uses the props/slots you explicitly pass in its *.component.yml*. See the [Twig documentation for `include`](https://twig.symfony.com/doc/3.x/functions/include.html) to learn more.
- While the overall order of dynamic output is controlled by the template (because we’re not printing `{{ content }}` wholesale), any time you print a specific item from the `content` render array (for example, `content.body`), the system uses that field’s display settings (set in the *Manage display* UI).

### Clear the cache

Run the following command so Drupal recognizes the new template file:

```
drush cr
```

### Preview your new template and component

View a node in the *Card* view mode. One way to do this is to update the default front page view to use the *Card* view mode instead of *Teaser* when displaying nodes. Using the *Manage* administrative menu, go to *Structure* > *Views* and edit the *Frontpage* view (*/admin/structure/views/view/frontpage*). Under *Format*, select *Teaser* and change it to `Card`.

Image

![Views configuration showing Format set to Show content using the Card view mode, filtered to Article content](../assets/images/hello-world--frontpage-view-config_1.png)

Save the view and go back to the homepage. You should now see a styled card with the title, metadata, and a body snippet.

Image

![Homepage list of Article nodes rendered with the Card view mode using the single directory component](../assets/images/hello-world--frontpage-list-using-card.png)

## Recap

In this tutorial, you created a single directory component named `card-simple` with three files inside our theme's *components/card-simple* directory:

- *card-simple.component.yml*: Defines metadata, props, and slots for the SDC.
- *card-simple.twig*: Contains the component’s markup.
- *card-simple.css*: Defines styles for the component.

You then referenced the component from a custom node template for the card view mode (*templates/content/node--card.html.twig*) and confirmed that Drupal rendered it with its styles automatically attached. You now have a working example you can adapt for other templates and components.

## Further your understanding

- What changes would you make to the *card-simple.component.yml* file to add another prop, such as a subtitle?
- How could you adjust the CSS to change the card’s size or colors?
- Where else in your theme could you include this component to reuse it?

## Additional resources

- [Quickstart (Using Single Directory Components)](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components/quickstart) (Drupal.org)
- [Template Design with Twig](https://drupalize.me/topic/template-design-twig) (Drupalize.Me)
- [Twig documentation for `include`](https://twig.symfony.com/doc/3.x/functions/include.html) (twig.symfony.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Anatomy of a Drupal Single Directory Component (SDC)](/tutorial/anatomy-drupal-single-directory-component-sdc?p=3329)

Next
[Understanding Props and Slots in Drupal Single Directory Components](/tutorial/understanding-props-and-slots-drupal-single-directory-components?p=3329)

Clear History

Ask Drupalize.Me AI

close