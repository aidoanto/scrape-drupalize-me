---
title: "2.7. Concept: User Interface, Configuration, and Content translation"
url: "https://drupalize.me/tutorial/user-guide/language-concept?p=2341"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
order: 7
---

# 2.7. Concept: User Interface, Configuration, and Content translation

## Content

### Prerequisite knowledge

- [Section 1.5, “Concept: Types of Data”](https://drupalize.me/tutorial/user-guide/understanding-data "1.5. Concept: Types of Data")
- [Section 1.2, “Concept: Modules”](https://drupalize.me/tutorial/user-guide/understanding-modules "1.2. Concept: Modules")
- [Section 2.3, “Concept: Content Entities and Fields”](https://drupalize.me/tutorial/user-guide/planning-data-types "2.3. Concept: Content Entities and Fields")

### What languages does the software support?

The base language for the software that your site runs (core software, modules, and themes) is English. However, using this software you can create a site whose default language is not English, in which case anyone viewing the site should see only that language (assuming that the site is fully translated). You can also use this software to create a multi-lingual site, with a language switcher that site visitors can use to switch to their preferred language. You need to have the core Language module installed in order to use a language other than English on the site.

### What can be translated on your site?

There are three types of information that you can translate, each with its own method for translating:

User interface text
:   Built-in text present in the core software, modules, and themes. This can be translated from the base English language of the software into the language(s) of your site. Typically, rather than needing to translate this text yourself, you can download translations. You need to have the core Interface Translation module installed in order to translate this text, and the core Update Manager module installed in order to automatically download translations.

Configuration text
:   Text whose structure and initial values are defined by the core software, modules, and themes, but that you can edit. Examples include the labels for fields in your content types, header text in views, your site name, and the content of automatic email messages that your site sends out. After creating configuration text in the default language of your site, you can translate it into other languages. For default configuration supplied by the core software, modules, and themes, translation is included with the downloads of user interface text translations. You need to have the core Configuration Translation module installed in order to translate this text.

Content text and files
:   If your site is multilingual, you can configure the content fields on your site to be translatable. After creating content in one language, you can translate it into other languages. Fields can contain textual information or uploaded files, and for each field on each entity subtype, you can configure it to be translatable or non-translatable. You need to have the core Content Translation module installed in order to translate this text.

### What information will remain in English on my site?

Even if the default language of your site is not English, you will still see English text on certain administrative pages used to manage configuration. The reason is that when you edit configuration, you are editing the base, untranslated configuration values; translating configuration is a separate operation. For example, if you visit the *Menus* administration page, you will see menu names in English (for the menus that were set up when you installed your site), and if you click an *Edit menu* link, you will be editing the English name and description of the menu. To edit the menu name in a different language, you would need to have the core Configuration Translation module installed, and use the *Translate* link to edit the translated menu information.

### Related topics

- [Section 10.1, “Adding a Language”](https://drupalize.me/tutorial/user-guide/language-add "10.1. Adding a Language")
- [Section 10.2, “Configuring Content Translation”](https://drupalize.me/tutorial/user-guide/language-content-config "10.2. Configuring Content Translation")
- [Section 10.3, “Translating Content”](https://drupalize.me/tutorial/user-guide/language-content-translate "10.3. Translating Content")
- [Section 10.4, “Translating Configuration”](https://drupalize.me/tutorial/user-guide/language-config-translate "10.4. Translating Configuration")

**Attributions**

Written by [Jennifer Hodgdon](https://www.drupal.org/u/jhodgdon).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[2.6. Concept: Editorial Workflow](/tutorial/user-guide/planning-workflow?p=2341)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close