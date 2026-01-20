---
title: "Tips for Theming with Layout Builder"
url: "https://drupalize.me/tutorial/tips-theming-layout-builder?p=2653"
guide: "[[layout-builder]]"
order: 11
---

# Tips for Theming with Layout Builder

## Content

One of the challenges that comes with Layout Builder is increased complexity of front-end development. Layout Builder offers site administrators increased flexibility regarding the placement and use of fields and blocks; a theme developer needs to account for this. Depending on how Layout Builder is used, this could mean a small number of new combinations, or virtually infinite combinations. Therefore, predicting and theming all of these combinations becomes a difficult but necessary task in order to ensure maintainability and overall design consistency.

In this tutorial we'll look at some things we've found helpful to consider when theming Layout Builder including:

- Design, and theme, atomic components
- Limit the number of possible combinations of fields by using entity view modes
- Handle edge cases

By the end of this tutorial you should have a better understanding of how using Layout Builder can impact theme development, and how to account for it.

## Goal

Provide tips for theme developers who are working with Layout Builder, or theming Layout Builder based pages.

## Prerequisites

- [Introduction to Layout Builder](https://drupalize.me/tutorial/introduction-layout-builder)

## Theming sites with blocks in Layout Builder

### Challenge

Theming blocks to work fluidly in all possible theme region or layout section placements, and at all possible mobile breakpoints, can be challenging. Given that most Drupal projects have an ever-growing set of blocks, this can get more challenging with time.

One also needs to make sure the combinations of these blocks work well together.

### Recommendations

1. Know which blocks are used, and which can be ignored, in order to limit scope
2. Design, and theme, blocks as self-contained components

To be successful, the design and theming paradigm should be mostly atomic. That is, each component that can placed into a layout (blocks and fields) should be self-contained. Components should not rely on the combination and placement of other components and should specifically be themed in isolation.

It is also important to identify early on what blocks will be supported in Layout Builder and what layout sections will be allowed per content type. Then limit the block set to the agreed upon instances, reducing the number of overall components that require theming.

[Layout Builder Restrictions](https://www.drupal.org/project/layout_builder_restrictions) module can be helpful in this case and will allow you to establish a manageable inventory of blocks and components that need theming.

Focus on managing specific use-cases, and don't commit to supporting Layout Builder in general. Outline which blocks you will support and in which regions, and align everyone on the team with this information.

## Theming sites with unrestricted use of Layout Builder

### Challenge

Once installed, Layout Builder can fully replace traditional Drupal content type display management. It can be tempting to omit fields for a content type and instead build pages with inline blocks using nodes as page containers. This notion, combined with the fact that Layout Builder can be configured to allow for per-node customizations, a large number of layouts, and many possible combinations of elements, can allow your overall site design to quickly spiral out of control.

While the flexibility and customizations are tempting, these decisions result in additional maintenance and theming overhead.

This freedom can end up putting pressure on editors to make design decisions that they may not be comfortable making.

### Recommendations

You probably do not want a free-for-all where editors can design and layout pages in whatever way they want. And, it's a good idea to ensure the use of fields on content types to collect content, and not replace fields with blocks.

To make theming easier, and the results more predictable, we recommend grouping fields in view modes and using view mode blocks and template overrides instead of placing each field individually. To learn more about this technique see [Implement the Layout Builder View Modes Pattern](https://drupalize.me/tutorial/implement-layout-builder-view-modes-pattern).

It might be best to start small and introduce Layout Builder on your project for modular landing pages. Introducing it on full node displays for all content types can create an overhead and present challenges that become difficult to resolve.

## Handle edge case block placements

### Challenge

There might be situations in your design where you would like certain blocks to appear differently depending on where they are displayed. This could be in a specific region, or a section of a layout.

For example, let's envision an *Art Object* block that shows a picture and metadata about an object. Every time we place the block in the Layout Builder it renders as a full width block with picture on the left and text on the right.

There's also a region in the layout with a special style applied to it so all of the blocks placed there will form a masonry grid, rather than being rendered full width. We want our *Art Object* block to become part of the masonry grid whenever it's placed in this region, without requiring editors to do anything other than place the block in the region.

### Recommendations

When an edge case presents itself, you may want to identify a style for that layout section and customize the styling with added CSS classes. Layout Builder adds contextual CSS classes you can use to target a block within a specific section. If necessary, you can also customize the CSS classes used for each section.

This way you can ensure that if the block is in this specially styled region or section it displays correctly.

The contributed [Layout Builder Styles](https://www.drupal.org/project/layout_builder_styles) module allows you to define styles that can be applied to a layout section.

Using modern front-end techniques, such as flexbox, in these applied styles can be crucial to keeping the breakpoints and code bloat to a minimum. It is especially important when Layout Builder is used with a lot of allowed flexibility, and you need to support many variations of blocks and field placements.

## Recap

In this tutorial we covered some common challenges related to theming Layout Builder content. We provided recommendations for addressing them that will help keep your code maintainable. The key takeaway is that using Layout Builder can lead to a large number of possible ways that fields and blocks can be combined. As designers and theme developers, we need to do our best to plan for all of those permutations in order to ensure consistency.

## Further your understanding

- What other approaches could you take to make theming easier?
- How does Layout Builder lead to theme code bloat?

## Additional resources

- [Layout Builder documentation](https://www.drupal.org/docs/8/core/modules/layout-builder) (Drupal.org)
- [DrupalCon Seattle 2019 presentation: "Layout Builder in the Real World"](https://events.drupal.org/seattle2019/sessions/layout-builder-real-world) (events.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Comparison of Layout-Building Approaches in Drupal](/tutorial/comparison-layout-building-approaches-drupal?p=2653)

Next
[Add Views to a Layout](/tutorial/add-views-layout?p=2653)

Clear History

Ask Drupalize.Me AI

close