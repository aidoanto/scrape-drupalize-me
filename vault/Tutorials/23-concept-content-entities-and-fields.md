---
title: "2.3. Concept: Content Entities and Fields"
url: "https://drupalize.me/tutorial/user-guide/planning-data-types?p=2341"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
---

# 2.3. Concept: Content Entities and Fields

## Content

### Prerequisite knowledge

- [Section 1.5, “Concept: Types of Data”](https://drupalize.me/tutorial/user-guide/understanding-data "1.5. Concept: Types of Data")
- [Section 1.2, “Concept: Modules”](https://drupalize.me/tutorial/user-guide/understanding-modules "1.2. Concept: Modules")

### What is a content entity?

A *content entity* (or more commonly, *entity*) is an item of content data, which can consist of text, HTML markup, images, attached files, and other data that is intended to be displayed to site visitors. Content entities can be defined by the core software or by modules.

Content entities are grouped into *entity types*, which have different purposes and are displayed in very different ways on the site. Most entity types are also divided into *entity subtypes*, which are divisions within an entity type to allow for smaller variations in how the entities are used and displayed. Here is a table of some common content entity types:

| Entity type | Entity subtype | Defining Module | Main uses |
| --- | --- | --- | --- |
| Content item | Content type | Node module | Content intended to be the main page area for pages on the site |
|  | **Example:** In the farmers market site example, you might have content types for basic pages, vendor pages, and recipe pages. | | |
| Comment | Comment type | Comment module | Commentary added to content entities (typically to Content item entities) |
|  | **Example:** On a blog site, blog posts might have comments. They are not needed in the farmers market site example. | | |
| User profile | (none) | User module | Data related to a person with a user account (login access) on the site |
|  | **Example:** Every site has at least basic user profiles with user names and email addresses; social networking sites may have more complex user profiles with more information. | | |
| Custom block | Block type | Custom Block module | Text and images in smaller chunks, often displayed in the site header, footer, or sidebar |
|  | **Example:** In the farmers market site example, you might put the hours and location in a sidebar block. | | |
| Taxonomy term | Vocabulary | Taxonomy module | Used to classify other types of content |
|  | **Example:** In the farmers market site example, you might classify Recipe content with an Ingredients taxonomy vocabulary, with taxonomy terms like Carrots and Tomatoes. In a blogging site, blog posts might be classified using a Tags vocabulary, and perhaps also a Categories vocabulary. | | |
| File | (none) | File module | An image or attachment file that is tracked and managed by the site, often attached to other types of content |
|  | **Example:** In the farmers market site example, both Recipe and Vendor pages might have image attachments, which would (behind the scenes) be managed as File entities by the site. | | |
| Contact form | Form type | Contact module | A form that lets site visitors contact site owners |
|  | **Example:** A contact form is needed in the farmers market site example. | | |

### What is a field?

Within entities, the data is stored in individual *fields*, each of which holds one type of data, such as formatted or plain text, images or other files, or dates. Field types can be defined by the core software or by modules.

Fields can be added by an administrator on entity subtypes, so that all entities of a given entity subtype have the same collection of fields available. For example, the Vendor content type in the farmers market example might have fields for the vendor name, a logo image, website URL, and description, whereas the *Basic page* content type might only have fields for the title and page body. When you create or edit entities, you are specifying the values for the fields on the entity.

### Related topics

- [Section 2.5, “Planning your Content Structure”](https://drupalize.me/tutorial/user-guide/planning-structure "2.5. Planning your Content Structure")
- [Section 5.2, “Creating a Content Item”](https://drupalize.me/tutorial/user-guide/content-create "5.2. Creating a Content Item")
- [Section 6.1, “Adding a Content Type”](https://drupalize.me/tutorial/user-guide/structure-content-type "6.1. Adding a Content Type")
- [Section 6.5, “Concept: Taxonomy”](https://drupalize.me/tutorial/user-guide/structure-taxonomy "6.5. Concept: Taxonomy")
- [Section 7.1, “Concept: Users, Roles, and Permissions”](https://drupalize.me/tutorial/user-guide/user-concept "7.1. Concept: Users, Roles, and Permissions")
- [Section 8.1, “Concept: Blocks”](https://drupalize.me/tutorial/user-guide/block-concept "8.1. Concept: Blocks")

**Attributions**

Written and edited by [Jennifer Hodgdon](https://www.drupal.org/u/jhodgdon) and [Grant Dunham](https://www.drupal.org/u/gdunham).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[2.2. Planning Your Site Layout](/tutorial/user-guide/planning-layout?p=2341)

Next
[2.4. Concept: Modular Content](/tutorial/user-guide/planning-modular?p=2341)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close