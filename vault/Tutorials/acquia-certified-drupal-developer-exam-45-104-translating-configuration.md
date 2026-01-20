---
title: "10.4. Translating Configuration"
url: "https://drupalize.me/tutorial/user-guide/language-config-translate?p=2378"
guide: "[[acquia-certified-drupal-developer-exam]]"
order: 45
---

# 10.4. Translating Configuration

## Content

### Goal

Translate the labels on the Recipes view page into Spanish.

### Prerequisite knowledge

- [Section 2.7, “Concept: User Interface, Configuration, and Content translation”](https://drupalize.me/tutorial/user-guide/language-concept "2.7. Concept: User Interface, Configuration, and Content translation")
- [Section 9.3, “Creating a Content List View”](https://drupalize.me/tutorial/user-guide/views-create "9.3. Creating a Content List View")

### Site prerequisites

- The core Configuration Translation module must be installed, and your site must have at least two languages. See [Section 10.1, “Adding a Language”](https://drupalize.me/tutorial/user-guide/language-add "10.1. Adding a Language").
- The Recipes view must exist. See [Section 9.3, “Creating a Content List View”](https://drupalize.me/tutorial/user-guide/views-create "9.3. Creating a Content List View") and [Section 9.4, “Duplicating a View”](https://drupalize.me/tutorial/user-guide/views-duplicate "9.4. Duplicating a View").

### Steps

Sprout Video

The basic steps for translating any configuration on your site are:

1. In the *Manage* administrative menu, navigate to *Configuration* > *Regional and Language* > *Configuration translation* (*admin/config/regional/config-translation*).
2. Locate the configuration item that you would like to translate. For example, to translate the site name, you need to find *System information*. For configuration that is grouped by type (for example, views or date formats), click the *List* button to list all configuration of that type, and then locate the item you are looking for.
3. Click *Translate* for the item you located.
4. Find a button that will let you add a translation in the desired language, and click this button.
5. Enter the translation in the form, and save.

Most configuration is fairly straightforward and intuitive to edit in this manner. Views configuration is an exception, because the translation editing form is nothing like the view editing form, and it is complex and hierarchical rather than being a simple form with just a few fields. As an example of how to translate a view, here are the steps to translate the labels in the Recipes view to Spanish:

1. In the *Manage* administrative menu, navigate to *Configuration* > *Regional and Language* > *Configuration translation* (*admin/config/regional/config-translation*).
2. Click *List* in the *Views* row.
3. Click *Translate* in the Recipes row.
4. Click *Add* in the *Spanish* row. The page *Add Spanish translation for Recipes view* appears.
5. Under *Displays* > *Default Display settings* > *Recipes default display Options*, translate *Display title* from "Recipes" to "Recetas".
6. Under *Displays* > *Default display settings* > *Recipes default display options* > *Exposed form* > *Reset options*, translate *Submit button text* from "Apply" to "Applicar". The other buttons and labels in this section do not appear on the Recipes page or block, and do not need to be translated.

   Image

   ![Translate the Recipes view](../assets/images/language-config-translate-recipes-view.png)
7. Under *Displays* > *Default display settings* > *Recipes default display options* > *Filters* > *(Empty) taxonomy term ID* > *Find recipes using… Expose*, translate *Label* from "Find recipes using…" to "Encontrar recetas usando…".
8. Click *Save translation*.
9. Navigate to the Recipes page and switch to Spanish using the Language switcher block. Verify that the labels have been translated.

### Expand your understanding

- Translate the block display title in the Recent recipes display settings section of the Recipes view.
- Translate the page title in the Vendors view.
- Translate other configuration. Some examples of where to find the translation pages:

  - To translate the site name, navigate in the *Manage* administrative menu to *Configuration* > *System* > *Basic site settings* > *Translate system information* (*admin/config/system/site-information/translate*).
  - To translate the contact form, navigate in the *Manage* administrative menu to *Structure* > *Contact forms* (*admin/structure/contact*). Click *Translate* in the dropdown button in the *Website feedback* row.
  - To translate the name of a menu, navigate in the *Manage* administrative menu to *Structure* > *Menus* (*admin/structure/menu*). Click *Translate* in the dropdown button for the menu whose name you want to translate.
  - Menu links within a menu are considered to be content (not configuration); see [Section 10.2, “Configuring Content Translation”](https://drupalize.me/tutorial/user-guide/language-content-config "10.2. Configuring Content Translation") to enable translation. Once translation is enabled, navigate in the *Manage* administrative menu to *Structure* > *Menus* (*admin/structure/menu*). Click *Edit menu* in the dropdown button for the menu whose links you want to translate. Click *Translate* in the dropdown button for the link you want to translate.
  - To translate field labels on a content type, navigate in the *Manage* administrative menu to *Structure* > *Content types* (*admin/structure/types*). Click *Manage fields* in the dropdown button for the content type whose field labels you want to edit. Click *Translate* in the dropdown button for the field whose label you want to edit.
- Translate content. See [Section 10.3, “Translating Content”](https://drupalize.me/tutorial/user-guide/language-content-translate "10.3. Translating Content").

Was this helpful?

Yes

No

Any additional feedback?

Previous
[10.3. Translating Content](/tutorial/user-guide/language-content-translate?p=2378)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close