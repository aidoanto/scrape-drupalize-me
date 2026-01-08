---
title: "10.3. Translating Content"
url: "https://drupalize.me/tutorial/user-guide/language-content-translate?p=2378"
guide: "[[acquia-certified-drupal-developer-exam]]"
---

# 10.3. Translating Content

## Content

### Goal

Translate the home page to Spanish.

### Prerequisite knowledge

[Section 2.7, “Concept: User Interface, Configuration, and Content translation”](https://drupalize.me/tutorial/user-guide/language-concept "2.7. Concept: User Interface, Configuration, and Content translation")

### Site prerequisites

- The Home content item must exist. See [Section 5.2, “Creating a Content Item”](https://drupalize.me/tutorial/user-guide/content-create "5.2. Creating a Content Item").
- The core Content Translation module must be installed, and your site must have at least two languages. See [Section 10.1, “Adding a Language”](https://drupalize.me/tutorial/user-guide/language-add "10.1. Adding a Language").
- The *Basic page* content type must be configured to be translatable. See [Section 10.2, “Configuring Content Translation”](https://drupalize.me/tutorial/user-guide/language-content-config "10.2. Configuring Content Translation").

### Steps

Sprout Video

1. In the *Manage* administrative menu, navigate to *Content* (*admin/content*).
2. Locate the home page. You can search for it by entering "Home" in the title field.
3. Select *Translate* from the dropdown button in the row of the Home content item. The page *Translations of Home* appears.
4. Click *Add* in the row *Spanish*.

   Image

   ![Adding a content translation](/sites/default/files/styles/max_800w/public/user_guide/images/language-content-translate-add.png?itok=cPNjwvy1)
5. Note that the user interface has switched to Spanish. To switch it back to English, remove the first instance of *es* in the browser’s URL. For example, if your URL looks like *example.com/es/node/5/translations/add/en/es*, remove the *es* that comes immediately after *example.com*.
6. Fill in the fields as shown below.

   | Field name | Explanation | Value |
   | --- | --- | --- |
   | Title | Translated title of the page | Página principal |
   | Body | Translated body of the page | Bienvenido al mercado de la ciudad - ¡el mercado de agricultores de tu barrio! Horario: Domingos de 9:00 a 14:00. Desde Abril a Septiembre Lugar: parking del Banco Trust número 1. En el centro de la ciudad |
   | URL alias > URL alias | Translated address of the webpage | pagina-principal |
7. Click *Save (this translation)*.
8. Go to your site’s home page to view the newly translated page.

### Expand your understanding

- Follow the steps above to translate more content on your site.
- [Section 10.4, “Translating Configuration”](https://drupalize.me/tutorial/user-guide/language-config-translate "10.4. Translating Configuration")

Was this helpful?

Yes

No

Any additional feedback?

Previous
[10.2. Configuring Content Translation](/tutorial/user-guide/language-content-config?p=2378)

Next
[10.4. Translating Configuration](/tutorial/user-guide/language-config-translate?p=2378)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close