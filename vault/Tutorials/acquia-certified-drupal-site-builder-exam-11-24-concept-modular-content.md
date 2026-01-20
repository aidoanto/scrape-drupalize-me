---
title: "2.4. Concept: Modular Content"
url: "https://drupalize.me/tutorial/user-guide/planning-modular?p=2341"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
order: 11
---

# 2.4. Concept: Modular Content

## Content

### Prerequisite knowledge

- [Section 2.3, “Concept: Content Entities and Fields”](https://drupalize.me/tutorial/user-guide/planning-data-types "2.3. Concept: Content Entities and Fields")
- [Section 2.2, “Planning Your Site Layout”](https://drupalize.me/tutorial/user-guide/planning-layout "2.2. Planning Your Site Layout")

### What is modular content?

Given that the content of your site is stored in a database, it is desirable to make the content *modular*, meaning that certain pages on your site, rather than being edited as a whole page, are instead generated automatically from other content items. For instance, in the farmers market site scenario, you might create individual content items for recipes. If the recipe content items have a field that keeps track of ingredients, then your site could include a composite page that would list recipes, and allow visitors to search for a recipe that contained some particular ingredient they had bought at the market.

Smaller sections of pages can also be generated as composites. For instance, recipe content items could have a field that keeps track of which vendor submitted the recipe (see [Section 6.4, “Concept: Reference Fields”](https://drupalize.me/tutorial/user-guide/structure-reference-fields "6.4. Concept: Reference Fields")), with the vendor details edited in separate vendor content items. This would allow you to do the following on your site:

- On each Recipe page, there could be an area that displays some information about the vendor that submitted the recipe, such as their name and market stall number.
- Each vendor page could have a section that lists the recipes they have submitted.

The key idea is that each piece of information is only edited in one place. When vendor information is updated, all recipe pages that display that vendor information are automatically updated; when a recipe is submitted by a vendor, it is automatically displayed on the vendor page. The core Views module is the usual way to use modular content to create composite pages and page sections; see [Section 9.1, “Concept: Uses of Views”](https://drupalize.me/tutorial/user-guide/views-concept "9.1. Concept: Uses of Views") for more information. Also, *view modes* are useful for defining different ways to display each content item; see [Section 6.10, “Concept: View Modes and Formatters”](https://drupalize.me/tutorial/user-guide/structure-view-modes "6.10. Concept: View Modes and Formatters") for more information.

### Related topics

- [Section 2.5, “Planning your Content Structure”](https://drupalize.me/tutorial/user-guide/planning-structure "2.5. Planning your Content Structure")
- [Section 6.1, “Adding a Content Type”](https://drupalize.me/tutorial/user-guide/structure-content-type "6.1. Adding a Content Type")
- [Section 6.3, “Adding Basic Fields to a Content Type”](https://drupalize.me/tutorial/user-guide/structure-fields "6.3. Adding Basic Fields to a Content Type")
- [Section 6.4, “Concept: Reference Fields”](https://drupalize.me/tutorial/user-guide/structure-reference-fields "6.4. Concept: Reference Fields")
- [Section 6.10, “Concept: View Modes and Formatters”](https://drupalize.me/tutorial/user-guide/structure-view-modes "6.10. Concept: View Modes and Formatters")
- [Section 9.1, “Concept: Uses of Views”](https://drupalize.me/tutorial/user-guide/views-concept "9.1. Concept: Uses of Views")

**Attributions**

Written by [Jennifer Hodgdon](https://www.drupal.org/u/jhodgdon).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[2.3. Concept: Content Entities and Fields](/tutorial/user-guide/planning-data-types?p=2341)

Next
[2.5. Planning your Content Structure](/tutorial/user-guide/planning-structure?p=2341)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close