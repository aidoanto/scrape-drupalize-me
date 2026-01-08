---
title: "10.2. Configuring Content Translation"
url: "https://drupalize.me/tutorial/user-guide/language-content-config?p=2378"
guide: "[[acquia-certified-drupal-developer-exam]]"
---

# 10.2. Configuring Content Translation

## Content

### Goal

Make *Custom block*, *Custom menu link*, and *Content* entity types translatable. Select specific subtypes and set which fields of these can be translated.

### Prerequisite knowledge

- [Section 2.3, “Concept: Content Entities and Fields”](https://drupalize.me/tutorial/user-guide/planning-data-types "2.3. Concept: Content Entities and Fields")
- [Section 2.7, “Concept: User Interface, Configuration, and Content translation”](https://drupalize.me/tutorial/user-guide/language-concept "2.7. Concept: User Interface, Configuration, and Content translation")

### Site prerequisites

The core Content Translation module must be installed, and your site must have at least two languages. See [Section 10.1, “Adding a Language”](https://drupalize.me/tutorial/user-guide/language-add "10.1. Adding a Language").

### Steps

Sprout Video

1. In the *Manage* administrative menu, navigate to *Configuration* > *Regional and language* > *Content language and translation* (*admin/config/regional/content-language*).
2. Under *Custom language settings*, check *Content*, *Content block* and *Custom menu link* to make these entity types translatable.

   Image

   ![Custom language settings checklist](/sites/default/files/styles/max_800w/public/user_guide/images/language-content-config_custom.png?itok=7SNS5sAD)
3. Configuration options appear for *Content*, *Content block* and *Custom menu link*. Choose the subtypes you want to translate for each entity type. Check *Basic page* for *Content*, *Basic block* for *Content block* and *Custom menu link* for *Custom menu link*.
4. Verify the settings for the entity types as shown below:

   | Field name | Explanation | Example value |
   | --- | --- | --- |
   | Default language | The default language for the entity subtype | Site’s default language (English) |
   | Show language selector on create and edit pages | Whether or not the language selector should be shown while editing and creating content | Checked |

   Image

   ![Default language and translatability for content types](/sites/default/files/styles/max_800w/public/user_guide/images/language-content-config_content.png?itok=W3_v3DaI)
5. Choose the fields that should be translatable for *Basic page* as shown in the table below. If a field is not translation-dependent, leave it unchecked.

   | Field name | Explanation | Example value |
   | --- | --- | --- |
   | Title | The title of the content | Checked |
   | Authored by | The author | Unchecked |
   | Published | Whether the content has been published or not | Checked |
   | Authored on | Date of publishing | Unchecked |
   | Changed | Date of last update | Unchecked |
   | Promoted to front page | Whether the content will be included in some content views | Unchecked |
   | Sticky at top of lists | Whether the content will be displayed first in some content views | Unchecked |
   | URL alias | Nicer URL for the content | Checked |
   | Body | The main content of the page | Checked |

   Image

   ![Translatable content entity subtypes' fields checklist](/sites/default/files/styles/max_800w/public/user_guide/images/language-content-config_basic_page.png?itok=ChtoTtvg)
6. Similarly, check the appropriate boxes for translatable fields belonging to *Basic block* and *Custom menu link*.
7. Click *Save configuration*.

### Expand your understanding

- [Section 10.4, “Translating Configuration”](https://drupalize.me/tutorial/user-guide/language-config-translate "10.4. Translating Configuration")
- [Section 10.3, “Translating Content”](https://drupalize.me/tutorial/user-guide/language-content-translate "10.3. Translating Content")

### Additional resources

- [Blog post "Multilingual Drupal 8 tidbits, part 5"](http://hojtsy.hu/blog/2013-jun-21/drupal-8-multilingual-tidbits-5-almost-limitless-language-assignment)
- [Blog post "Multilingual Drupal 8 tidbits, part 17"](http://hojtsy.hu/blog/2015-jan-27/drupal-8-multilingual-tidbits-17-content-translation-basics)

**Attributions**

Written and edited by [Laura Vass](https://www.drupal.org/u/lolk) at [Pronovix](https://pronovix.com/), [Jojy Alphonso](https://www.drupal.org/u/jojyja) at [Red Crackle](http://redcrackle.com), and [Jennifer Hodgdon](https://www.drupal.org/u/jhodgdon).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[10.1. Adding a Language](/tutorial/user-guide/language-add?p=2378)

Next
[10.3. Translating Content](/tutorial/user-guide/language-content-translate?p=2378)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close