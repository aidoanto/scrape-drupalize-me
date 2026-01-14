---
title: "Overview: Theming Viewsfree"
url: "https://drupalize.me/tutorial/overview-theming-views?p=2670"
guide: "[[views-drupal]]"
---

# Overview: Theming Viewsfree

## Content

Like most output in Drupal, Views relies on Twig templates for a significant amount of its rendering. In this tutorial we'll identify where you can find the default Views templates within your file system, what the common templates are for, and how to name your templates so that they are applied to specific views.

By the end of this tutorial, you should be able to:

- Identify where to find default views templates
- Understand which templates apply to what part of a view
- Get a sense of the template suggestions and how to use them to limit where your custom templates are applied
- Identify a view's machine name
- Identify a display's machine name
- Identify a field's machine name

## Goal

Understand how to override a Views template.

## Prerequisites

We will be applying concepts in Drupal theming. If you are new to theming in Drupal, you might find it helpful to walk through our guide, [Hands-On Theming](https://drupalize.me/guide/hands-on-theming).

Examples and screenshots in this tutorial are from the demo site we set up in:

- [Set up Demo Site with Views and Content](https://drupalize.me/tutorial/set-demo-site-views-and-content)

If you are new to Views, check out these Drupal User Guide tutorials:

- [Concept: Uses of Views](https://drupalize.me/tutorial/user-guide/views-concept)
- [Concept: The Parts of a View](https://drupalize.me/tutorial/user-guide/views-parts)

## Theming views

When working with views we often want to change the style for how the list of content is displayed to our site visitors. Some style options are available as configuration options we can change when editing a view, while other parts of the view are handled with Twig template files. It is not always easy to identify which mechanism controls what part of the view, so we've created this image to help.

Image

![A view with the different template sections highlighted and labeled](../assets/images/twig-theming--overview.png)

Each of the sections highlighted are controlled by a Twig template.

| Color | Section | Template Name | Description |
| --- | --- | --- | --- |
| Orange | Wrapper | *views-view.html.twig* | This section represents the view's wrapper template. All other parts of the view are contained within the wrapper. |
| Gold | Format | *views-view-FORMAT.html.twig* | (Replace *FORMAT* with the machine name of the format, e.g. `unformatted`, `grid`, `list`, `table`, `rss`.) This section represents the view's format template. This section is controlled by a template specific to the format we've selected for our view. |
| Blue | Row Style | *views-view-fields.html.twig* | The blue sections represents an individual row that contains our fields. It isn't always controlled by an individual template. It depends on the chosen *Format* for the view. |
| Green | Field | *views-view-field.html.twig* | The green sections represent individual fields within out view. Fields can have their own unique *Style Settings* that are configured when editing the view. Those settings will affect the content as it appears within the green highlighted section. |

## Locating views template files

Like many Twig templates in Drupal, the default templates for the Views module can be found within a folder named *templates* within the module's folder. The full path to this folder within our Drupal installation is */core/modules/views/templates*. A direct copy of these templates are also located in the Drupal core theme, Stable here: *core/themes/stable/templates/views*.

If you've [configured your environment for theme development](https://drupalize.me/tutorial/configure-your-environment-theme-development) and view source on a page with a view embedded on it, you will be able to view the theme information for each part of the view, including which template is being used.

Image

![Screenshot of the templates folder within the views module](../assets/images/twig-theming--templates-location.png)

We never want to edit the template files in this location. Instead, we want to override individual templates by copying them from this folder into our theme's folder.

## Override templates in our theme

To customize a template we need to copy the file into a folder named *templates* within our custom theme.

For example, if we wanted to override the Wrapper template for every view on our site we would copy the file *core/modules/views/templates/views-view.html.twig* to a folder named *templates* within our theme. Here is an animation that illustrates copying a view template to a custom theme.

Image

![Animated GIF showing how to copy a template from the views module into our custom theme](../assets/images/twig-theming--copy-template.gif)

After copying a template to our theme the Views module will discover and make use of our custom template going forward. We are free to edit the new template copy as much as we like.

## Template suggestions

In addition to overriding templates site-wide, we can also override templates in a way that targets specific views we create. We do this by naming our new template file according to a specific pattern that the Views module expects. These patterns are called *Template Suggestions*. The views module provides a number of template suggestions out of the box.

The template suggestions the Views module expects will follow this pattern:

```
{template name}--{view-name}--{display-id}--{field-id}.html.twig
```

Let's break that pattern down a little bit to better understand the pieces.

| Placeholder | Description | Examples |
| --- | --- | --- |
| *{template name}* | This is the file name for the default template, without the file extensions. | *views-view*, *views-view-grid*, *views-mini-pager* |
| *{view name}* | This is the machine name for the view we want to override templates for. Replace underscores in the machine name with dashes. | *baseball-players*, *baseball-awards*, *taxonomy-term* |
| *{display id}* | The ID for the view *display* that we want to override templates for. Replace underscores in the display ID with dashes. | *page-1*, *block-2* |
| *{field id}* | The unique identifier for a field in our view. This part of the pattern only applies when working with field templates. | *field-player-award-year* |

## How to find template suggestion information

Now that we have a pattern to follow for naming our templates, let's look at where we can find this information in the Views interface.

### Find a view's machine name

The easiest way to find a view's machine name is on the administration page that shows a list of all views on our site.

From the administration dashboard, navigate to Structure > Views (*admin/structure/views*). In this list of views is a column for each view's machine name.

Image

![Screenshot of the administration list of views with the machine name column highlighted](../assets/images/twig-theming--locate-view-machine-name.png)

### Find the display ID

The display ID for any view display is located on the view's edit form in the *Advanced* column as *Machine Name*.

Image

![Screenshot of a view edit form with the advanced column open and the display's machine name highlighted](../assets/images/twig-theming--locate-display-id.png)

To locate the Display ID for another display on our view, we need to switch to the display we want and then locate the *Machine Name* within the **Advanced** section.

### Find a field ID

A field's ID is a little trickier to locate. To find these we need to edit a field and temporarily enable some options in the field's configuration form.

1. From the view's edit form select the field we want to identify.
2. In the field's configuration form, open the section labeled **Rewrite Results**.
3. Select the checkbox labeled *Override the output of this field with custom text*. This will display some additional configuration options.
4. Open the new section labeled **Replacement Patterns**.

Image

![Screenshot of a field's configuration modal form with the replacement patterns highlighted](../assets/images/twig-theming--locate-field-id.png)

Here we can see a list of some of the fields on our view and their field IDs. The field ID is the part of the list between the curly braces, not including the double-curly braces. For example, the image above lists the following items as replacement patterns:

- `{{ field_player_award_award }} ==`
- `{{ field_player_award_year }} == Year`

The field IDs for those replacement patterns are *field\_player\_award\_award* and *field\_player\_award\_year*. To use a field ID in a template file name, change the underscores (`_`) to hyphens (`-`).

After locating the ID for the field we want to template, select the button labeled *Cancel* at the bottom of the modal window so that we do not save the changes for the field.

## Using template suggestions

Now that we have a pattern to follow and know where to get the values we need, let's look at a few examples to help illustrate how the pattern can be used.

| View Name | Display ID | Template to Override | Resulting Filename |
| --- | --- | --- | --- |
| *baseball\_players* | *page\_1* | *views-view.html.twig* (Wrapper) | *views-view--baseball-players--page-1.html.twig* |
| *taxonomy\_term* | *block\_2* | *views-view-grid.html.twig* (Format) | *views-view-grid--taxonomy-term--block-2.html.twig* |
| *who\_s\_online* | (All displays) | *views-mini-pager.html.twig* (Mini pager) | *views-mini-pager--who-s-online.html.twig* |
| (All views) | *block\_1* | *views-view.html.twig* (Wrapper) | *views-view--block-1.html.twig* |

Note that the view name and display ID placeholders are optional. The Views module will use our template for *All* views or displays for the placeholders we leave off. **The more specific our template file name, the fewer views our template will affect.** Using specific template file names allows us to manage many different custom templates for many different views and view displays.

## Recap

In this tutorial, we learned how to find the location necessary to override a template for a view -- or part of a view. We learned which patterns are used in template suggestions for Views and how to locate the necessary information in order to override a template for a part of a view.

## Further your understanding

- When you [configure your environment for theme development](https://drupalize.me/tutorial/configure-your-environment-theme-development), can you locate template information in the HTML source code of a rendered view?

## Additional resources

- [Configure Your Environment for Theme Development](https://drupalize.me/tutorial/configure-your-environment-theme-development) (Drupalize.Me)
- [Hands-On Theming](https://drupalize.me/guide/hands-on-theming) (Drupalize.Me)
- [public function ViewExecutable::buildThemeFunctions](https://api.drupal.org/api/drupal/core%21modules%21views%21src%21ViewExecutable.php/function/ViewExecutable%3A%3AbuildThemeFunctions) - Curious how Views decides which theme functions to call? This method provides a full array of possible theme functions to try for a given hook. (api.drupal.org)
- [Views template files](https://api.drupal.org/api/drupal/core%21modules%21views%21views.theme.inc/group/views_templates) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Create a Page with a Contextual Filter](/tutorial/create-page-contextual-filter?p=2670)

Next
[Override a View's Wrapper Template](/tutorial/override-views-wrapper-template?p=2670)

Clear History

Ask Drupalize.Me AI

close