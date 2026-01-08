---
title: "2.5. Planning your Content Structure"
url: "https://drupalize.me/tutorial/user-guide/planning-structure?p=2341"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
---

# 2.5. Planning your Content Structure

## Content

### Goal

Make a plan for the content structure of the site (which type and subtype of entity to use for which content), and which pages will contain listings of content.

### Prerequisite knowledge

- [Section 2.3, “Concept: Content Entities and Fields”](https://drupalize.me/tutorial/user-guide/planning-data-types "2.3. Concept: Content Entities and Fields")
- [Section 2.4, “Concept: Modular Content”](https://drupalize.me/tutorial/user-guide/planning-modular "2.4. Concept: Modular Content")
- [Section i.6, “Guiding Scenario”](https://drupalize.me/tutorial/user-guide/preface-scenario "i.6. Guiding Scenario")

### Steps

Sprout Video

1. Brainstorm about what content your site needs to contain, which could include content that visitors would be looking for, as well as content that you want to show to visitors. The result could be the description in [Section i.6, “Guiding Scenario”](https://drupalize.me/tutorial/user-guide/preface-scenario "i.6. Guiding Scenario").
2. For each identified piece of content, decide which content entity type would be the best fit. In doing this, you’ll need to consider where and how the content will be used and edited on the site. For example, in the farmers market site scenario, you might want to display the hours and location of the farmers market on the sidebar of every page. For that content, a single custom block makes sense. As another example, you might decide that pages displaying information about each vendor should be content items managed by the core Node module, because you want vendors to be able to edit their own listings. The core Node module permission system lets you do this easily.

   These decisions do not necessarily always have only one right answer; for instance, you could decide that vendor pages should be user profiles instead of content items, but if you did that the content would be tied to a specific user account, and it would not be as easy to later change the ownership of a vendor page to a different user account.
3. Within each content entity type you identified, decide what division into entity subtypes would make sense. For example, in the farmers market site example, you would probably decide that under the Content item entity type, there should be one content type for basic pages (Home and About), one for vendor pages, and one for recipe pages.
4. For each entity subtype you decided on, decide what fields are needed. For instance, the Vendor content type might need fields for the vendor name, web page URL, image, and description.
5. Decide on what entity listings are needed, which could be entire pages or smaller areas on the page. For each listing, you’ll need to determine which entities should be listed. Then you’ll need to decide in what order and with what filtering options they should be displayed; for example, you might want to give the site visitor the option to search by keyword, to filter the list down to a subset, or to sort the list. You’ll also need to decide what information from the entities should be shown, which might result in adding to the list of fields you determined in the previous step. The farmers market site, for example, needs to have a Recipes listing page that lists content items of type Recipe, with the ability to filter by ingredients, so that means that the Recipe content type needs an Ingredients field.
6. For each identified field on each entity subtype, identify what type of data it should contain (such as plain text, formatted text, a date, an image file, etc.), and how many values should be allowed. Most fields are single-valued, but for example, a Recipe should allow for multiple values in its Ingredients field.
7. Consider which fields would be best as references to taxonomy term entities: fields whose values should be chosen from a list of allowed values. Allowed values that are expected to change and grow over time, are good candidates. An example is the Ingredients field for the Recipe content type.
8. Consider which fields should reference other content entities. An example is that since vendors will be submitting recipes, a field will be needed on the Recipe content type that references the Vendor content item for the vendor who submitted the recipe.

Here’s an example of the resulting content structure for the farmers market scenario example site:

| Entity type | Entity subtype | Examples | Fields |
| --- | --- | --- | --- |
| Content item | Basic page | Home page, about page | Title, page body |
| Content item | Vendor | A page for each vendor at the market | Vendor name, page body, image, URL |
| Content item | Recipe | A page for each submitted recipe | Recipe name, page body, image, reference to Vendor who submitted it, Ingredients taxonomy |
| Custom block | (generic) | Copyright notice for footer, Hours and location for sidebar | No special fields |
| Taxonomy term | Ingredients | Carrots, tomatoes, and other recipe ingredients | No special fields |
| Contact form | (generic) | Generic contact form | Name, email, subject, message |
| User profile | (none) | Will not be displayed on site | No special fields |

And here are the listings the site needs:

| Page or page area | Entity type and subtype | Filter/sort/pagination | Fields displayed |
| --- | --- | --- | --- |
| Vendors page | Vendor content items | All vendors, alphabetical, paged | Image, vendor name, trimmed body |
| Recipes page | Recipe content items | Filter by ingredients, alphabetical, paged | Image, recipe name |
| Recent recipes sidebar | Recipe content items | List 5 most recent | Image, recipe name |

### Expand your understanding

- [Section 6.1, “Adding a Content Type”](https://drupalize.me/tutorial/user-guide/structure-content-type "6.1. Adding a Content Type")
- [Section 6.3, “Adding Basic Fields to a Content Type”](https://drupalize.me/tutorial/user-guide/structure-fields "6.3. Adding Basic Fields to a Content Type")
- [Section 6.6, “Setting Up a Taxonomy”](https://drupalize.me/tutorial/user-guide/structure-taxonomy-setup "6.6. Setting Up a Taxonomy")

### Related concepts

[Section 6.5, “Concept: Taxonomy”](https://drupalize.me/tutorial/user-guide/structure-taxonomy "6.5. Concept: Taxonomy")

Was this helpful?

Yes

No

Any additional feedback?

Previous
[2.4. Concept: Modular Content](/tutorial/user-guide/planning-modular?p=2341)

Next
[2.6. Concept: Editorial Workflow](/tutorial/user-guide/planning-workflow?p=2341)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close