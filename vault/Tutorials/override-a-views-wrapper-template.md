---
title: "Override a View's Wrapper Template"
url: "https://drupalize.me/tutorial/override-views-wrapper-template?p=2670"
guide: "[[views-drupal]]"
---

# Override a View's Wrapper Template

## Content

Now that we understand what templates are and how we can use them, let's override some templates! In this tutorial we'll copy the views wrapper template to our theme and override it so that we can customize the markup for the Baseball Players view. Then we'll modify the template so that our view's pager appears both above and below our table of players.

## Goal

Display the Baseball Players view pager both above and below the table of Players.

## Prerequisites

- [Overview: Theming Views](https://drupalize.me/tutorial/overview-theming-views)
- [Describe Your Theme with an Info File](https://drupalize.me/tutorial/describe-your-theme-info-file)

For this tutorial, we've created a custom theme in *themes/bartik2* with an info file (*themes/bartik2/bartik2.info.yml*) with the following contents:

```
name: Bartik 2
type: theme
base theme: bartik
description: 'A quick demo theme.'
package: Custom
core_version_requirement: ^8 || ^9 || ^10
```

Enable the theme and set it as default on the *Appearance* page (*admin/appearance*) in the administrative UI.

Examples and screenshots in this tutorial are from the demo site we set up in:

- [Set up Demo Site with Views and Content](https://drupalize.me/tutorial/set-demo-site-views-and-content)

If you are new to Views, check out these Drupal User Guide tutorials:

- [Concept: Uses of Views](https://drupalize.me/tutorial/user-guide/views-concept)
- [Concept: The Parts of a View](https://drupalize.me/tutorial/user-guide/views-parts)

## Watch: Override a View's Wrapper Template

Sprout Video

## Override the wrapper template for a view

In the following steps, we'll copy the default *views-view.html.twig* template to our custom theme and rename it to apply only to a specific view.

From the site administration page, visit Structure > Views (*admin/structure/views*).

Locate the view *Baseball Players* and take note of the machine name for this view: `baseball_players`.

Image

![Screenshot of list of views showing Baseball Players view](/sites/default/files/styles/max_800w/public/tutorials/images/twig-theming-wrapper--find-machine-name.png?itok=dSNv-S3M)

Locate the default *views-view.html.twig* template and copy it by right-clicking the file, then selecting File > Copy. The template can be found at *core/modules/views/templates/views-view.html.twig*.

Image

![Screenshot of core views templates folder with views-view.html.twig template selected](/sites/default/files/styles/max_800w/public/tutorials/images/twig-theming-wrapper--template-copy.png?itok=L9nzkUdk)

Paste it (File > Paste) into your theme's *templates* folder. (Create the *templates* directory first if it doesn't already exist.) Rename the copied template file to *views-view--baseball-players.html.twig*. In this example, our theme is named `bartik2`, so the resulting file is *themes/bartik2/templates/views-view--baseball-players.html.twig*. Replace *bartik2* with the machine name of your theme.

To construct the new template file name, we added `--` and our view's machine name after *views-view*. We also replaced all underscores (`_`) with dashes (`-`) in the view's machine name.

Image

![Screenshot of custom theme templates folder with new template](/sites/default/files/styles/max_800w/public/tutorials/images/twig-theming-wrapper--template-paste-rename.png?itok=A7I-NHZa)

## Modify the template and create another pager

Next we'll edit our new template and copy the pager so that it appears both above and below the view's content.

Open the new *views-view--baseball-players.html.twig* template in your favorite code editor. It should look approximately like this:

```
{%
  set classes = [
    dom_id ? 'js-view-dom-id-' ~ dom_id,
  ]
%}
<div{{ attributes.addClass(classes) }}>
  {{ title_prefix }}
  {{ title }}
  {{ title_suffix }}

  {% if header %}
    <header>
      {{ header }}
    </header>
  {% endif %}

  {{ exposed }}
  {{ attachment_before }}

  {% if rows -%}
    {{ rows }}
  {% elseif empty -%}
    {{ empty }}
  {% endif %}
  {{ pager }}

  {{ attachment_after }}
  {{ more }}

  {% if footer %}
    <footer>
      {{ footer }}
    </footer>
  {% endif %}

  {{ feed_icons }}
</div>
```

Locate the line of code that is the pager (`{{ pager }}`), copy that line, and paste it above the line that checks if the view has rows (`{% if rows -%}`). The resulting template should have two lines of code that contain `{{ pager }}`. It should look approximately like this:

```
{%
  set classes = [
    dom_id ? 'js-view-dom-id-' ~ dom_id,
  ]
%}
<div{{ attributes.addClass(classes) }}>
  {{ title_prefix }}
  {{ title }}
  {{ title_suffix }}

  {% if header %}
    <header>
      {{ header }}
    </header>
  {% endif %}

  {{ exposed }}
  {{ attachment_before }}

  {{ pager }}
  {% if rows -%}
    {{ rows }}
  {% elseif empty -%}
    {{ empty }}
  {% endif %}
  {{ pager }}

  {{ attachment_after }}
  {{ more }}

  {% if footer %}
    <footer>
      {{ footer }}
    </footer>
  {% endif %}

  {{ feed_icons }}
</div>
```

Notice that we are printing out the `pager` variable twice now.

Next we need to rebuild our site cache so that Drupal can locate our new template. We can do this by going to the Configuration > Development > Performance (*admin/config/development/performance*) and selecting **Clear all caches**.

Image

![Screenshot of the Performance page and the Clear all caches button](/sites/default/files/styles/max_800w/public/tutorials/images/twig-theming-wrapper--clear-caches.png?itok=MtDEuaAK)

## See our new template in action

Now we can visit the baseball players page (From the administrative menu, select Back to site, the select the Baseball Players tab (*baseball-players*)). We should find that there are two pagers on the page. One pager appears above the view's content and the other pager appears below the view's content.

Image

![Screenshot of the Baseball Players view with a pager at the top](/sites/default/files/styles/max_800w/public/tutorials/images/twig-theming-wrapper--two-pagers-top.png?itok=sgEOWNfm)

...

Image

![Screenshot of the Baseball Players view with a pager at the bottom](/sites/default/files/styles/max_800w/public/tutorials/images/twig-theming-wrapper--two-pagers-bottom.png?itok=RNQkWDXQ)

## Recap

Overriding Views templates is a powerful way to customize your website. Beyond simply duplicating pagers, this technique provides developers a way to create distinct and beautiful lists of content. Combined with overriding other Views templates, we have almost full control over how our Views look and function.

## Further your understanding

- Modify our new template further to make it even more distinct by adding an image or icon at the top of the page.
- Override the *views-mini-pager.html.twig* template for the Baseball Players view and change the `››` and `‹‹` arrows to use the words "Next" and "Previous".

## Additional resources

- [Hands-On Theming](https://drupalize.me/guide/hands-on-theming) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview: Theming Views](/tutorial/overview-theming-views?p=2670)

Clear History

Ask Drupalize.Me AI

close