---
title: "9.2. Concept: The Parts of a View"
url: "https://drupalize.me/tutorial/user-guide/views-parts?p=2449"
guide: "[[acquia-certified-drupal-developer-exam]]"
order: 25
---

# 9.2. Concept: The Parts of a View

## Content

### Prerequisite knowledge

- [Section 2.3, “Concept: Content Entities and Fields”](https://drupalize.me/tutorial/user-guide/planning-data-types "2.3. Concept: Content Entities and Fields")
- [Section 2.4, “Concept: Modular Content”](https://drupalize.me/tutorial/user-guide/planning-modular "2.4. Concept: Modular Content")
- [Section 9.1, “Concept: Uses of Views”](https://drupalize.me/tutorial/user-guide/views-concept "9.1. Concept: Uses of Views")
- [Section 5.1, “Concept: Paths, Aliases, and URLs”](https://drupalize.me/tutorial/user-guide/content-paths "5.1. Concept: Paths, Aliases, and URLs")
- [Section 8.1, “Concept: Blocks”](https://drupalize.me/tutorial/user-guide/block-concept "8.1. Concept: Blocks")

### What are the parts of a view?

When you are editing a view in the administrative interface, you will see the following parts (or sections), which allow you to specify what data to output, in what order, and in what format:

Display
:   Each view can have one or more displays, each of which produces one type of output. Options for display types include:

    Page
    :   Makes output at a particular URL, for the main page content at that URL.

    Block
    :   Makes output in a block, which can be placed on pages.

    Feed
    :   Makes an RSS or another type of feed.

    Attachment
    :   Makes output that you can attach to another display.

Format
:   Depending on the display type, you can choose to output your data in a table, grid, HTML list, or another format. Some formats also give you a second choice that lets you output either rendered entities or fields; other formats do not give you this choice (for example, if you use a table format, you must always use fields).

Fields
:   Depending on the format choice, you may be able to choose which content fields are output. For example, if you were making a view of recipe content items, in a block display you might show only the recipe names, while in a full page display you might also show an image field because you have more space.

Filter criteria
:   Filters limit the data to be output, based on criteria such as whether the content has been published or not, the type of content, or a field value. For instance, to make a view of recipe content items, you would need to filter to the Recipe content type, and to published recipes. Filters can also be *exposed*, which means that users will have a form where they can choose their own filter values. You might use this on a Recipe page to let users filter for recipes with certain ingredients.

Sort criteria
:   Defines the order to present the output, which can be based on any content field.

Contextual filters
:   Contextual filters are like regular filters, except that the values come from the *context* of the view display, such as the full URL of the page being displayed, the current date or time, or some other value that can be detected by the view calculation.

Relationships
:   Relationships allow you to expand what is displayed in your view, by relating the base content being displayed to other content entities. Relationships are created using fields on the base content that relate it to the other content; one example is that all regular content items have an author field, which references the user account of the person who authored the content. Once you have created a relationship, you can display fields from the referenced entity in the view.

### Related topics

[Section 9.3, “Creating a Content List View”](https://drupalize.me/tutorial/user-guide/views-create "9.3. Creating a Content List View")

**Attributions**

Written and edited by [Surendra Mohan](https://www.drupal.org/u/surendramohan) and [Jennifer Hodgdon](https://www.drupal.org/u/jhodgdon).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[9.1. Concept: Uses of Views](/tutorial/user-guide/views-concept?p=2449)

Next
[9.3. Creating a Content List View](/tutorial/user-guide/views-create?p=2449)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close