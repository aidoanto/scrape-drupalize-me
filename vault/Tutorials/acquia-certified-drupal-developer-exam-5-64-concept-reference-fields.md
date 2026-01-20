---
title: "6.4. Concept: Reference Fields"
url: "https://drupalize.me/tutorial/user-guide/structure-reference-fields?p=2412"
guide: "[[acquia-certified-drupal-developer-exam]]"
order: 5
---

# 6.4. Concept: Reference Fields

## Content

### Prerequisite knowledge

[Section 2.3, “Concept: Content Entities and Fields”](https://drupalize.me/tutorial/user-guide/planning-data-types "2.3. Concept: Content Entities and Fields")

### What is a reference field?

A *reference field* is a field that represents a relationship between an entity and one or more other entities, which may belong to the same or different entity type. The three most commonly-used reference fields are:

Content reference
:   A reference to a content item. For example, you might want to connect recipes to the vendors who submitted them. You would set up a content reference field called Submitted by referencing Vendor content items on the Recipe content type.

Taxonomy term reference
:   A reference to a taxonomy term. For example, you might want to connect recipes to their ingredients. You would set up a taxonomy term reference field called Ingredients on the Recipe content type. This reference field will point to the vocabulary Ingredients.

User reference
:   A reference to a user account. For example, you might want to connect recipes with their chefs. You would set up a user reference field called Chefs on the Recipe content type.

### Related topics

[Section 6.5, “Concept: Taxonomy”](https://drupalize.me/tutorial/user-guide/structure-taxonomy "6.5. Concept: Taxonomy")

**Attributions**

Written and edited by [Surendra Mohan](https://www.drupal.org/u/surendramohan), and [Jojy Alphonso](https://www.drupal.org/u/jojyja) at [Red Crackle](http://redcrackle.com).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[6.3. Adding Basic Fields to a Content Type](/tutorial/user-guide/structure-fields?p=2412)

Next
[6.5. Concept: Taxonomy](/tutorial/user-guide/structure-taxonomy?p=2412)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close