---
title: "Layout Builder Design Patterns"
url: "https://drupalize.me/tutorial/layout-builder-design-patterns?p=2653"
guide: "[[layout-builder]]"
---

# Layout Builder Design Patterns

## Content

Like many things in Drupal, there are multiple ways to solve the same problem when using Layout Builder. The Layout Builder system is very flexible. In order to be successful when using it, it helps to plan ahead and think through your specific use-case. Picking a pattern, and sticking to it, will help ensure your configuration is more maintainable, and easier for others to understand. While there's nothing to prevent you from mixing and matching, in our experience we've found it's helpful to at least set some ground rules.

In this tutorial we'll outline 3 different patterns to use with Layout Builder, and the pros and cons of each. We'll include:

- Using content fields in scenarios where a few pages use Layout Builder, but the majority of the site's layout is done via the theme and is generally not configurable by editors.
- Using a blocks-based approach to layouts for scenarios where you want to use Layout Builder instead of the traditional blocks and regions approach and allow editors to make changes via the UI.
- And finally, using an Entity view modes approach for sites that rely heavily on Layout Builder and contain lots of interrelated content types with complex layout requirements.

By the end of this tutorial you should have a better understanding of how to approach using Layout Builder for your specific use-case, and the advantages and disadvantages of different common patterns.

## Goal

Explain 3 commonly-used approaches to using Layout Builder and the advantages and disadvantages of each.

## Prerequisites

- [Introduction to Layout Builder](https://drupalize.me/tutorial/introduction-layout-builder)
- [Create a Flexible Layout for a Content Type](https://drupalize.me/tutorial/create-flexible-layout-content-type)

## Getting started

In this tutorial we assume that you have a strong understanding of what Layout Builder is and that you know how to define new layouts. This tutorial covers advanced concepts related to Layout Builder techniques and strategies.

## Pattern #1: Content fields

### When to use this pattern

- Limited flexibility is required on a small number of content types to handle edge cases.
- The majority of the site doesn't use Layout Builder and instead utilizes standard theme regions for layout.
- The site has a large volume of contributors with different abilities.
- This approach allows consistency in content representation while still allowing for some flexibility.

### Problem and motivation

Imagine that you manage a site for a non-profit organization. This organization conducts conferences and events for farmers across the country. Most events are smaller scale like a local farmers' meetup where people get together and discuss strategies and daily problems. A few events are larger, like conventions and conferences that are attended by thousands of people.

On your website you have an *Event* content type with *Image gallery*, *Description* and *Date* fields. For the majority of the events this content type presents your information successfully, with no changes. It has a beautiful layout with an image gallery on the left and events details in the right column.

However, when the event does not have pictures to show in the gallery, the gallery field is hidden and the description takes the full width of the screen -- becoming too wide and hard to read.

On the other side of this spectrum, bigger events often have lots of pictures; it would be nice if in this case the gallery had a wider column on the page or perhaps was featured at the top, while dates and descriptions could be split into a 2-column layout.

Those are valid points but they are edge cases when compared to the majority of events, so it doesn't make sense to have special content types for them. It would be nice to give editors the ability to layout the fields based on the content they are entering.

### Technique

Using Layout Builder with a *content fields approach* is designed to solve the outlined problem. In this scenario, Layout Builder is configured to allow editors to customize event layouts per-node while having a default layout used by most events.

Coming back to the example, the default layout for the event content type will consist of 2 columns: a left column containing an image gallery field, and a right column containing the description and date fields.

Then by using the option to allow custom layouts per-node, editors will be able to adjust the layout on an as needed basis.

The key to this approach is that Layout Builder acts mostly like the *Manage display* section of the content type settings, but with more flexibility. The page consists of the fields of the content type -- they are all nicely displayed by default, but can be adjusted at will via the Drupal UI without changing the theme's code.

In this approach standard blocks provided by Views or other modules are displayed via the *Block layout* configuration within the theme's regions, giving editors little or no control over when and where they are displayed.

This approach works best in combination with the [Layout Builder Restrictions module](https://drupalize.me/tutorial/use-layout-builder-restrictions-configure-available-layouts-and-blocks), which makes it possible to allow editors to modify the layout, but still impose restrictions on what can be altered rather than giving them the full control offered by Layout Builder.

Image

![Diagram of Layout Builder setup with fields](../assets/images/fields_drawing.png)

### Advantages

One advantage of this approach is the ease of setup. It also has predictable results since blocks are limited to the content type fields. This allows for easy theming since the number of possible combinations is limited and strictly defined.

### Disadvantages

Such a strict setup provides some flexibility, but does not allow for more creative or complicated solutions. It also makes it difficult to interact with other components on the site (like Views blocks and other Drupal blocks) and forces editors to use theme regions to place them.

## Pattern #2: Layout Builder fields + blocks

### When to use this pattern

- You need to allow a mix of fields and a limited set of blocks on content page layouts.
- The available blocks are applicable for the majority of content items in the content type, and can be placed in the default layout of the content type.
- It doesn't work well when the blocks vary from node to node and the layouts are complex and differ per node, as it becomes harder to predict the variety of use cases and pre-theme the results.

### Problem and motivation

Let's come back to our non-profit website. We already set up Layout Builder for the event content type and everything has been working fantastic. Then during a website brainstorming session one of the stakeholders suggested that it would be nice to show related events on an individual event page to boost engagement and allow people to explore different events.

While this could be solved with theme regions and a Views block that lists related events, your editors expressed interest in showing this block in place of the image gallery when the gallery is empty, or underneath the primary event content for bigger events that have promotional media.

### Technique

The scenario above can be addressed with the mixed technique of using blocks together with fields inside the Layout Builder interface. It starts with the same setup as the first pattern. Then the [Layout Builder Restrictions Module](https://drupalize.me/tutorial/use-layout-builder-restrictions-configure-available-layouts-and-blocks) needs to be configured to whitelist a view of related events and any other blocks that might be used within the event nodes.

In this approach some, but maybe not all, standard blocks are displayed on the page via Layout Builder. This gives editors more control over when, and where, they appear, but potentially reduces consistency from page-to-page.

Image

![Diagram of Layout Builder setup with fields and blocks](../assets/images/fields_blocks.png)

### Advantages

This technique allows you to incorporate standard Drupal building elements such as blocks and Views inside Layout Builder, and minimizes the need to rely on the theme's regions. It also allows for less clutter on the *Block layout* page and makes it more manageable since inline blocks will not be shown there.

### Disadvantages

Mixing blocks and fields makes it more unpredictable for themers as it expands the variety of use cases. This can increase the initial development / theming cost and also makes it harder to maintain in the future.

## Pattern #3: Entities and view modes

### When to use this pattern

- Your website relies on Layout Builder to a great extent.
- It works well for websites with many different layouts and content types, and where individual pages often require a unique layout.
- You want to give content editors the greatest amount of flexibility without requiring them to modify the theme.
- You have the time, and resources, to make the upfront investment required to ensure consistent theming and configuration for a large number of possible layouts.

### Problem and motivation

Imagine that you are managing a large-scale digital publishing website. Your client has a team of editors that create stories on a daily basis. Each story is a unique piece of digital art and requires the editorial team to have as much flexibility as possible.

It is possible to achieve this using the first 2 techniques by not setting up many restrictions. However, this can lead to challenges as certain blocks and fields get used in combination with layout sections that were not tested or themed together.

In the process of solving these requests you may also notice that CSS classes and HTML markup differ based on the context in which fields and blocks are used. This can present challenges to maintenance of the theme as the number of CSS/HTML permutations grows.

### Technique

The problem described above has 2 parts: allow editors to have as much flexibility as possible while giving some predictability for the front-end developers; and minimize the theme maintenance burden. The approach is similar in concept to component based design systems.

To accomplish this you'll make a list of all the different *Sections* in a layout that content can be placed into. For example: *Hero area*, *Highlight cards*, *Description*, *Video area*, etc.

Then instead of placing individual fields into those sections, create corresponding view modes, and use those in the Layout Builder. Following the above example, you could create the following view modes: *Hero*, *Highlight*, and *Video*. Theming is then applied to the view modes.

This technique allows us to customize content templates and set up classes and markup that will stay consistent regardless of layout section. Later these view modes can be used outside of the Layout Builder context, in Views for example, further reducing the need for additional theming.

Learn how to implement this technique in the tutorial, [Implement the Layout Builder View Modes Pattern](https://drupalize.me/tutorial/implement-layout-builder-view-modes-pattern).

Image

![Diagram of Layout Builder setup with view modes](../assets/images/view_modes.png)

### Advantages

This technique produces consistent markup and classes and facilitates reusability. It also allows for flexibility with guiding restrictions as opposed to a full restricted list of blocks and components.

This also has the benefit of better revision tracking as you rely on the content type revisions mechanisms. It also has better multilingual support.

### Disadvantages

Requires more planning at the beginning for definition of view modes and templates.

## Recap

In this tutorial we covered 3 different approaches for building Drupal sites with Layout Builder. These techniques vary in initial setup efforts, development time, and flexibility of the final setup. The field based technique is better suited for smaller scale applications of Layout Builder, while the view modes technique allows more flexibility and variety while facilitating reusability and ease of maintenance.

We realize that there is no one approach that will work for every use-case. Even if you don't follow one of those patterns, we encourage you to take the time to think through how your use of Layout Builder will grow, and what that means for maintainability in the long term.

## Further your understanding

- What other approaches could you use while building sites with Layout Builder?
- What technique do you think will work best for your project? Why?

## Additional resources

- [Layout Builder documentation](https://www.drupal.org/docs/8/core/modules/layout-builder) (Drupal.org)
- [Layout API](https://www.drupal.org/docs/drupal-apis/layout-api) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Use Layout Builder Restrictions to Configure Available Layouts and Blocks](/tutorial/use-layout-builder-restrictions-configure-available-layouts-and-blocks?p=2653)

Next
[Implement the Layout Builder View Modes Pattern](/tutorial/implement-layout-builder-view-modes-pattern?p=2653)

Clear History

Ask Drupalize.Me AI

close