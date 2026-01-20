---
title: "Add a Component YAML File for a Drupal SDC"
url: "https://drupalize.me/tutorial/add-component-yaml-file-drupal-sdc?p=3329"
guide: "[[frontend-theming]]"
order: 55
---

# Add a Component YAML File for a Drupal SDC

## Content

The component YAML file, with the suffix *.component.yml*, is the heart of every Drupal single directory component (SDC). This file describes how consumers can **pass data** (*props*) and **nest content** (*slots*) into the component. Similar to a PHP interface, the schema defined in a *.component.yml* file acts as a contract that tells consumers (both developers and low-code tools) what data a component accepts and what shape it expects.

In this tutorial, you’ll learn what each key in a component's YAML file does. You’ll see how the file names the component, describes its API, and helps low-code tools validate and expose your component. Then we’ll create a new *card* component with a *card.component.yml* file.

By following along, you will:

- Reinforce your understanding of where a Drupal component's YAML file lives and why it matters.
- Break down each top-level key—`$schema`, `name`, `description`, `props`, and `slots`.
- Learn more about what you can put into a *.component.yml* file.

By the end of this tutorial, you’ll have a discoverable *card.component.yml* file for a new `card` SDC and a mental model for how Drupal uses it.

## Goal

Understand the purpose and structure of a component YAML file and create a new *card.component.yml* file that describes the structure of the inputs it accepts along with metadata about the component.

## Prerequisites

- [Anatomy of a Drupal Single Directory Component (SDC)](https://drupalize.me/tutorial/anatomy-drupal-single-directory-component-sdc)
- (Optional) [Create Your First Drupal Single Directory Component (SDC)](https://drupalize.me/tutorial/create-your-first-drupal-single-directory-component-sdc)

## Anatomy of a *.component.yml* file

The table below describes the different top-level keys of a *.component.yml* file:

| Key | Description |
| --- | --- |
| `$schema` | URL of the JSON Schema that defines the metadata format. |
| `name` | Human-readable name of the component. |
| `description` | Human-readable description of the component. |
| `props` | JSON Schema describing the data inputs (properties) the component accepts. |
| `slots` | Named placeholders for markup content passed into the component. |
| `group` | Optional grouping label used by UI browsers to categorize components. |
| `status` | Status can be: "experimental", "stable", "deprecated", "obsolete". |
| `dependencies` | Array of library machine names this component relies on. |
| `libraryOverrides` | Overrides CSS/JS libraries attached automatically; lets you replace, disable, or add assets for this component only. |
| `replaces` | Declares that this component replaces another component. |

## The `$schema` key

Every *.component.yml* file should start with a `$schema` declaration. It’s not required, but there are a few good reasons to include it.

Example:

```
$schema: https://git.drupalcode.org/project/drupal/-/raw/HEAD/core/assets/schemas/v1/metadata.schema.json
```

This URL points to the canonical JSON Schema that describes all valid top-level keys (name, description, props, and so on) and the keywords you can use inside them.

When your code editor (like *PhpStorm* or *VS Code*) sees this line, it can:

1. Autocomplete valid keys and values as you type.
2. Show inline documentation pulled directly from the schema.
3. Highlight errors the moment a value doesn’t match the schema.

Drupal doesn’t fetch this file at runtime—it’s for developer tooling and CI validation only.

### Different schema versions

`HEAD` always resolves to the latest schema in Drupal core. You can pin to a specific version, or even a commit, to avoid unexpected changes; in practice, most projects simply track `HEAD`. Because Drupal’s metadata schema follows JSON Schema draft-07, teams can also point `$schema` to a custom JSON file for project-specific conventions or experiments.

For example, during the development of Drupal Canvas, this feature has been used to introduce and test possible new keys that make it easier for Drupal Canvas to use an SDC.

## Defining props (component properties)

One of the most important roles of a *.component.yml* file is defining the schema of the props a component accepts. As a developer, you’ll use props to pass data to a component when you need **strongly typed, reusable data inputs**—numbers, booleans, or structured objects that drive logic rather than markup.

Defining a props schema is ***optional* for themes** but ***mandatory* for modules**. However, skipping props means Drupal can’t validate your input, and many UI tools such as *Layout Builder* and *Drupal Canvas* won’t be able to expose your component. In practice, treat the `props` section as **necessary** for any component you plan to share or use in low-code builders, regardless if the component is in a module or theme.

### Benefits of defining a props schema

It's best practice to define a schema for your component's props. Why?

- Only components that have schemas can override other components.
- Schemas help you identify problems with your components early.
- Schemas future-proof your component. Schemas enable contributed modules and core projects under development to be able to automatically generate forms for the user when placing the component using the administrative UI.

Since props schemas are optional for themes, you can force all components within your theme to require a `props` schema by adding the following to your theme's *.THEMENAME.info.yml*:

```
enforce_prop_schemas: true
```

### How to define a props schema

Props are defined inside the `props` object using the **JSON Schema draft-07** vocabulary. (See <https://json-schema.org/draft-07>.)

Drupal validates props passed from:

- Twig `include()`
- `#component` render arrays

When provided, Drupal feeds any data passed to the component through the JSON Schema defined in `props`. If the data fails validation, Drupal logs an error and prevents rendering, helping you catch mistakes and giving you instant feedback. This helps improve both the developer experience (DX) and that of end users.

### How do you define a schema for props?

1. Provide individual property definitions inside the top level `props:` key.
2. For each prop, specify at minimum a `type`.
3. Use `title` and `description` to improve UX in low-code builders.
4. Mark required props under `required:`.
5. No top-level `schema` key under `props` is needed.

Example:

```
props:
  type: object
  properties:
    heading:
      type: string
      title: Heading
      description: Text to display as the heading.
    count:
      type: integer
      title: Count
  required:
    - heading
```

Property keys (like `heading` and `count`) are used to derive the variable names available in the component’s Twig template. In this instance, `heading` maps to `{{ heading }}`.

### Components with no props

Even if your component doesn’t accept any props, declare an explicit empty schema so UI tools and validators behave predictably:

```
props:
  type: object
  additionalProperties: false
  properties: {}
```

#### Property definition keys

At a minimum, define a `type`, `title`, and `description`. You can also use other keys to further describe a property:

| Key | Purpose |
| --- | --- |
| `type` | Primitive or complex JSON Schema data type (`string`, `integer`, `object`, etc.). |
| `title` | Short, human-readable label shown in UI builders. |
| `description` | Longer help text that explains the purpose of the property. |
| `default` | Value used when the consumer passes nothing. |
| `enum` | List of allowed values (works with several types, commonly `string`). |
| `pattern` | Regular expression the string value must match. |
| `format` | Semantic hint such as `email`, `uri`, or `date`. UI widgets can change based on this. |
| `maximum` / `minimum` | Numeric boundaries for `number` and `integer` types. |
| `maxLength` / `minLength` | Character length boundaries for `string` types. |
| `items` | JSON Schema definition for each element of an `array`. |
| `properties` | Nested property definitions for an `object` type. |
| `required` | Array of property names that must be provided (used inside an `object` definition). |
| `oneOf` / `anyOf` / `allOf` | Combine or constrain multiple schemas for advanced validation scenarios. |
| `examples` | Sample values to show in documentation or UI hints. |

### Format tips and gotchas

- JSON Schema supports advanced keywords such as `enum`, `pattern`, and `format` (e.g., `format: uri`). Use them to catch invalid data early.
- Use `format: uri-reference` if you want to allow relative paths like `/node/123`. Use `format: uri` only when an absolute URL is required. Pass the value from the consuming template (for example, *node.html.twig*) using `path()` for relative paths or `url()` for absolute URLs.
- `format: date` expects `YYYY-MM-DD`. Pass the ISO string from the consuming template, then format it inside the component’s Twig template (for example, *components/card/card.twig*) for display:

  ```
  {{ metadata.date|date('U')|format_date('medium') }}
  ```

We'll use these tips and techniques as we build our example *card* component.

### Choosing a `type`

The JSON Schema spec defines a handful of primitive `type` values you'll use most often:

| `type` | Accepts | Sample value | When to use |
| --- | --- | --- | --- |
| `string` | Plain text | `"Bicycle"` | Titles, names, paths, UUIDs |
| `integer` | Whole numbers | `42` | Counts, index positions |
| `number` | Integers or floats | `3.14` | Measurements, ratings |
| `boolean` | `true` or `false` | `true` | Flags—e.g., `show_flip_button` |
| `array` | Ordered list | `["red", "green"]` | Multiple items of the same shape |
| `object` | Key/value map | `{ "url": "?", "title": "?" }` | Nested data with named fields |
| `null` | The literal `null` | `null` | Rare—use to explicitly allow “no value” |

You can also combine types with `oneOf`, `anyOf`, or `allOf` for advanced cases, but aim to keep props predictable: one prop, one data shape.

Want to see where these types come from? Open the metadata schema linked in `$schema` or the [JSON Schema specification](https://json-schema.org/) for a full list of keywords and examples.

## Defining slots

Slots are placeholders for markup rather than scalar data. Developers define slots for a component when the shape of the data is intentionally unknown. For example, when you want to allow inserting varied HTML content, or even other SDCs, as the body of a card component.

Example slot definitions:

```
slots:
  content:
    title: Content
  body:
    title: Card body
    description: Complete HTML body for the card; overrides the heading prop and content slot.
```

Slot keys (like `content` and `body`) are used to derive the names of the variables available in the component’s Twig template. For an overview of how slots fit into an SDC’s structure, see [Anatomy of a Drupal Single Directory Component (SDC)](https://drupalize.me/tutorial/anatomy-drupal-single-directory-component-sdc).

Each slot definition accepts:

- `title`: A human-readable name for the slot.
- `description`: A description of the slot used by different UI tools.
- `required`: (optional) Mark a slot as required.

## Using `libraryOverrides`

The `libraryOverrides` key in a component’s *.component.yml* file lets you fine-tune the CSS and JavaScript asset library that Drupal automatically creates and attaches when the component is rendered. You can use it to:

- Add extra CSS or JavaScript files to a component.
- Declare dependencies on other libraries (for example, when your JavaScript uses Drupal’s `once` library).

Examples:

```
libraryOverrides:
  css:
    theme:
      card.css: {}
      card--dark.css: {}
  js:
    card.flip.js: { minified: true }
  dependencies:
    - core/drupal
    - core/once
```

When you declare a top-level key under `libraryOverrides`—such as `css`, `js`, or `dependencies`—you take complete control of that part of the asset library. Drupal will not merge in the auto-attached files for that key.

- If you override `css`, you must list every CSS file you want included, including the component’s own *{component}.css* file, plus any additional files you add.
- If you override `js`, you must list every JavaScript file you want included, including *{component}.js*.
- If you override `dependencies`, you must declare all dependencies you want attached.

Files or dependencies not listed under the overridden key will not be included.

## Using `replaces`

The `replaces` key declares that this component supersedes another component. Drupal will automatically substitute the new component when a builder or template asks for the old one—allowing you to roll out improvements without breaking existing content.

Example:

```
name: fancy-card
replaces:
  - another_theme:card
```

## Add a card component

Now that we understand what can go in a Drupal SDC *.component.yml* file, let’s add a *.component.yml* for a new card component in a custom theme or module.

### Create a directory for the card component

If it doesn’t already exist, create the directory *components/card/* inside your module or theme.

### Add the *card.component.yml* file

Create the new *card.component.yml* file inside the *card/* directory and populate it with the following:

```
$schema: https://git.drupalcode.org/project/drupal/-/raw/HEAD/core/assets/schemas/v1/metadata.schema.json
name: card
description: A flippable, brutalist card component.

props:
  type: object
  properties:
    heading:
      type: string
      title: Heading
      description: Text to display as the heading.
    url:
      type: string
      title: URL
      description: URL to link the card to.
      format: uri-reference
    card_links:
      type: array
      title: Related links
      description: An array of link objects with URL and title.
      items:
        type: object
        properties:
          url:
            type: string
            format: uri-reference
          title:
            type: string
        required:
          - url
          - title
    show_flip_button:
      type: boolean
      title: Show flip button
      description: When true, display a button that flips the card to reveal additional content on the back.
    count:
      type: integer
      title: Count
      description: When displayed in a series, this is the card number.
    metadata:
      type: object
      title: Metadata
      description: Author and date for content displayed in the card.
      properties:
        author:
          type: string
          title: Content author
        date:
          type: string
          format: date
          title: Content publication date
  required:
    - heading
    - url

slots:
  content:
    title: Content
  body:
    title: Card body
    description: Complete HTML body for the card; overrides the heading prop and content slot.
```

### Clear the cache

Run the following command so Drupal discovers the new *card* component:

```
drush cr
```

### (Optional) Examine what Drupal knows about your component

The *card* component, with only a *components/card/card.component.yml* file, doesn’t do anything except exist on Drupal’s radar. You can examine what Drupal currently knows about the *card* SDC by running:

```
drush php:eval "print_r(\Drupal::service('plugin.manager.sdc')->getDefinition('neo_brutalism:card', FALSE));"
```

**Note:** Replace `neo_brutalism` with the *provider* name—the module or theme that contains your component—and `card` with the name of your component (the component directory name).

In the next tutorial, we'll [add a Twig template file to the *card* component](https://drupalize.me/tutorial/add-twig-template-your-single-directory-component) and use the component in a template file.

## Recap

In this tutorial, we discussed the role of the Drupal *.component.yml* file, saw where it resides in a single directory component, learned how to describe props and slots with JSON Schema for reliable validation (validated from both Twig includes and render arrays), explored major top-level keys—including `$schema`, `name`, `description`, `group`, `status`, `dependencies`, `libraryOverrides`, and `replaces`—and built a complete card component schema. We are now ready to [add a template file for our component](https://drupalize.me/tutorial/add-twig-template-your-single-directory-component) using the variables that we defined in our component's YAML file.

## Further your understanding

- Explore the [JSON Schema specification](https://json-schema.org/)
- Can you create a schema for a complex prop like an image that contains a URI, a title, and alt text?

## Additional resources

- [Annotated example component.yml](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components/annotated-example-componentyml) (Drupal.org)
- [Metadata JSON Schema](https://git.drupalcode.org/project/drupal/-/raw/HEAD/core/assets/schemas/v1/metadata.schema.json) (git.drupalcode.org)
- [JSON Schema specification](https://json-schema.org/) (json-schema.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Understanding Props and Slots in Drupal Single Directory Components](/tutorial/understanding-props-and-slots-drupal-single-directory-components?p=3329)

Next
[Add a Twig Template to Your Single Directory Component](/tutorial/add-twig-template-your-single-directory-component?p=3329)

Clear History

Ask Drupalize.Me AI

close