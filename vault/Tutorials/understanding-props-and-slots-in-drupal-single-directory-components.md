---
title: "Understanding Props and Slots in Drupal Single Directory Components"
url: "https://drupalize.me/tutorial/understanding-props-and-slots-drupal-single-directory-components?p=3329"
guide: "[[frontend-theming]]"
order: 23
---

# Understanding Props and Slots in Drupal Single Directory Components

## Content

*Props* and *slots* are the two ways that data can be provided to a single directory component (SDC). They are part of a component's schema definition, and are used to determine the names of variables passed to a component's template file. *Props* pass structured, validated data into a component, while *slots* allow us to inject flexible content such as HTML or nested components. Understanding when and how to use each ensures you can build reusable and adaptable components.

In this tutorial, we'll:

- Learn what props and slots are, and how they differ.
- Discuss how using one or the other impacts the developer experience and use of your components in a UI.
- Practice deciding when to use each for component design.

By the end of this tutorial, you'll know how to choose between props and slots when building components.

## Goal

Understand the difference between props and slots in Drupal single directory components, and learn how to choose the right input type for a component.

## Prerequisites

- [Anatomy of an SDC](https://drupalize.me/tutorial/anatomy-drupal-single-directory-component-sdc)

If your SDC allows data inputs you'll need to define them as props and slots in the *\*.component.yml* file for the component.

## What are props?

Props are **structured inputs**. They carry validated data such as strings, numbers, booleans, or arrays into a component. They are used when you know the type and shape of the expected data, and ensure consistency.

### Example: Declare and use a `title` prop

```
props:
  title:
    type: string
    label: "Card title"
```

```
<h2>{{ title }}</h2>
```

Use props when you need:

- Text labels (titles, headings, captions)
- Booleans to toggle features (for example, show/hide an image)
- Structured values like image URLs or numbers
- To enforce choosing one from a list (enum) like a size input that must be one of small, medium, or large

Learn how to add props to a component in [Add a Component YAML File for a Drupal SDC](https://drupalize.me/tutorial/add-component-yaml-file-drupal-sdc).

## What are slots?

Slots are **unstructured placeholders**. They enable you to inject HTML or nested components into a defined area of a component. Slots must be declared in your component schema, but do not enforce strict typing.

### Example: Declaring and using a `content` slot

```
slots:
  content:
    label: "Main content area"
```

```
<div class="card__content">
  {{ content }}
</div>
```

Use slots when you need:

- Arbitrary HTML markup such as paragraphs or lists
- Nested components like buttons or teasers
- Flexible regions such as card bodies, modal contents, or footers

Learn how to add slots to a component in [Add a Component YAML File for a Drupal SDC](https://drupalize.me/tutorial/add-component-yaml-file-drupal-sdc).

## How props and slots affect UI tools

Single directory components are available for a user to select when building a page layout using UI tools such as Drupal Canvas or UI Patterns. These tools rely on the definitions of props and slots to determine how to present the component's configuration options to the user. For example, should the UI show a dropdown with a list of options to choose from, or a text area for entering content with CKEditor? These UI tools read your *\*.component.yml* file to determine what to present in the UI.

- **Props** typically appear as form fields in the UI. For example, a `title` string prop will show up as a text input, and a boolean prop may render as a checkbox. This allows site builders to configure components with predictable values.
- **Slots** appear as drop zones or content areas. In Drupal Canvas, slots allow editors to drag in text, media, or other components. This makes slots essential for flexible, layout-driven authoring experiences.

Understanding your component's data inputs and properly defining them as either props or slots can directly influence how intuitive and powerful these UI tools become for non-developers.

## Props or slots: Which one should I use?

Choose based on whether the input should be structured or flexible, and how the component will be used in UI tools.

- **Use props** for predictable values such as titles, URLs, flags, or enums.
- **Use slots** for flexible or complex content such as nested components or arbitrary HTML.

## Recap

Props and slots let you pass data into a component. Props define the structure and enforce validation, ensuring consistency and predictability. Slots add flexibility by allowing arbitrary content or nested components. When designing a component, consider what data it should accept, how that data will be used, and how your choices affect tools like Drupal Canvas.

## Further your understanding

- How would you decide between using a prop or a slot when designing a navigation menu component?
- Can you think of a case where a slot might be too flexible, and a prop would be safer?
- What advantages do you gain by combining props and slots in a single component?

## Additional resources

- [What are Props and Slots in Drupal SDC Theming?](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components/what-are-props-and-slots-in-drupal-sdc-theming) (Drupal.org)
- [Add a Component YAML File for a Drupal SDC](https://drupalize.me/tutorial/add-component-yaml-file-drupal-sdc) (Drupalize.Me)
- [Add a Twig Template to Your Single Directory Component](https://drupalize.me/tutorial/add-twig-template-your-single-directory-component) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Create Your First Drupal Single Directory Component (SDC)](/tutorial/create-your-first-drupal-single-directory-component-sdc?p=3329)

Next
[Add a Component YAML File for a Drupal SDC](/tutorial/add-component-yaml-file-drupal-sdc?p=3329)

Clear History

Ask Drupalize.Me AI

close