---
title: "6.5. Concept: Taxonomy"
url: "https://drupalize.me/tutorial/user-guide/structure-taxonomy?p=2412"
guide: "[[acquia-certified-drupal-developer-exam]]"
order: 6
---

# 6.5. Concept: Taxonomy

## Content

### Prerequisite knowledge

- [Section 2.3, “Concept: Content Entities and Fields”](https://drupalize.me/tutorial/user-guide/planning-data-types "2.3. Concept: Content Entities and Fields")
- [Section 6.4, “Concept: Reference Fields”](https://drupalize.me/tutorial/user-guide/structure-reference-fields "6.4. Concept: Reference Fields")

### What is Taxonomy?

*Taxonomy* is used to classify website content. One common example of taxonomy is the tags used to classify or categorize posts in a blog website; the farmers market website could use an ingredients taxonomy to classify recipes. Individual taxonomy entities are known as *terms* (the blog tags or recipe ingredients in these examples); and a set of terms is known as a *vocabulary* (the set of all blog post tags, or the set of all recipe ingredients in these examples). Technically, taxonomy terms are an entity type and the entity subtypes are the vocabularies. Like other entities, taxonomy terms can have fields attached; for instance, you could set up an image field to contain an icon for each term.

An individual vocabulary can organize its terms in a hierarchy, or it could be flat. For example, blog tags normally have a flat structure, while a recipe ingredients vocabulary could be hierarchical (for example, tomatoes could be a sub-term of vegetables, and under tomatoes, you could have green and red tomatoes).

Taxonomy terms are normally attached as reference fields to other content entities, which is how you can use them to classify content. When you set up a taxonomy reference field, you can let users enter terms in two ways:

Free tagging
:   New terms can be created right on the content editing form.

Fixed list of terms
:   The list of terms is curated and managed outside the content editing form, and users can only choose from the existing list when editing content.

Taxonomy reference fields can be added to any entity, such as user accounts, custom blocks, or regular content items. If you use them to classify regular content items, your site will automatically be set up with taxonomy listing pages for each term; each of these pages lists all of the content items that are classified with that term. For example, if you created several recipes that all had carrots as an ingredient, you might see something like this on the Carrots taxonomy listing page:

Image

![Taxonomy listing page - Carrots](../assets/images/structure-taxonomy_listingPage_carrots.png)

### Related topics

- [Section 6.6, “Setting Up a Taxonomy”](https://drupalize.me/tutorial/user-guide/structure-taxonomy-setup "6.6. Setting Up a Taxonomy").
- The listing pages are views, which are covered in [Chapter 9, *Creating Listings with Views*](https://drupalize.me/course/user-guide/views-chapter "Chapter 9. Creating Listings with Views").

**Attributions**

Adapted and edited by [Surendra Mohan](https://www.drupal.org/u/surendramohan), [Jennifer Hodgdon](https://www.drupal.org/u/jhodgdon), and [Jojy Alphonso](https://www.drupal.org/u/jojyja) at [Red Crackle](http://redcrackle.com) from ["Organizing content with taxonomies"](https://www.drupal.org/docs/7/organizing-content-with-taxonomies/organizing-content-with-taxonomy) and ["About taxonomy"](https://www.drupal.org/docs/7/organizing-content-with-taxonomies/about-taxonomies), copyright 2000-2026 by the individual contributors to the [Drupal Community Documentation](https://www.drupal.org/documentation).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[6.4. Concept: Reference Fields](/tutorial/user-guide/structure-reference-fields?p=2412)

Next
[6.6. Setting Up a Taxonomy](/tutorial/user-guide/structure-taxonomy-setup?p=2412)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close