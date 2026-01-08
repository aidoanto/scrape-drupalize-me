---
title: "Adding Asset Libraries to Custom Layouts"
url: "https://drupalize.me/tutorial/adding-asset-libraries-custom-layouts?p=2653"
guide: "[[layout-builder]]"
---

# Adding Asset Libraries to Custom Layouts

## Content

When defining new layout plugins for Drupal you can add custom CSS and JavaScript via asset libraries. This allows for the creation of layouts with complex structures and interactive elements. Those elements might include grids, tabs, and accordions. Drupal allows you to attach custom CSS and JavaScript directly to a layout plugin, or via the layout's Twig template file.

In this tutorial we'll:

- Define a custom asset library with JavaScript and CSS functionality
- Attach the asset library to the custom layout plugin
- Transform a multicolumn layout into tabs

By the end of this tutorial you should know how to attach custom CSS and JavaScript to a layout plugin to add interactivity and styling.

## Goal

Transform a multicolumn layout into interactive tabs using custom CSS and JavaScript attached to the layout plugin.

## Prerequisites

- [Introduction to Layout Builder](https://drupalize.me/tutorial/introduction-layout-builder)
- [Create a Flexible Layout for a Content Type](https://drupalize.me/tutorial/create-flexible-layout-content-type)
- [Define Custom Layouts in a Module or Theme](https://drupalize.me/tutorial/define-custom-layouts-module-or-theme)
- [What Are Libraries?](https://drupalize.me/tutorial/what-are-asset-libraries)

## Follow these steps

The rest of this tutorial assumes you've followed the steps in [Define Custom Layouts in a Module or Theme](https://drupalize.me/tutorial/define-custom-layouts-module-or-theme) and created a module named *custom\_layouts* that defines a 3-column layout plugin. If you're working on your own code, substitute your module's name in as appropriate.

### Define an asset library

Define an asset library that will contain the JavaScript and CSS for the tabs.

In the custom module's root folder, create a file called *custom\_layouts.libraries.yml*. In this file we'll define JavaScript and CSS assets that will be attached to the layout:

```
tabs:
  version: VERSION
  js:
    js/tabs.js: {}
  css:
    component:
      css/tabs.css: {}
  dependencies:
    - core/drupal
    - core/jquery
```

Learn more about this file in [Define an Asset Library](https://drupalize.me/tutorial/define-asset-library).

### Attach the library to a layout

You can attach a library either via Twig's `attach_library` function or via the `library` property of the *custom\layouts.layouts.yml* file.

We recommend using the Twig method when you're overriding templates for layout plugins defined outside of your module or theme, or when the layout plugin is a dynamic derivative. If you need a refresher on this, see [Attach a Library](https://drupalize.me/tutorial/attach-asset-library).

In this tutorial, we will attach the library using the *library* annotation key that can be added to the layout definition in the *custom\_layouts.layouts.yml* file.

Modify the *custom\_layouts.layouts.yml* file to have the library key like so:

```
custom_layouts_threecol_25_50_25:
  label: 'Three column 25/50/25'
  path: templates/layouts
  template: custom-layouts--threecol-25-50-25
  category: 'Columns: 3'
  default_region: second
  icon_map:
    - [first, second, third]
  regions:
    first:
      label: First
    second:
      label: Second
    third:
      label: Third
  library: custom_layouts/tabs
```

The *library* key's value is the name of the asset library you wish to attach to the layout.

### Adding CSS

The custom layout doesn't look like 3 columns in a row by default. Rather, all columns are rendered one under another as per browser defaults. To make them look like columns we can use flexbox rules.

Create the file *css/tabs.css* in your module. This file name needs to match what's defined in the *custom\_layouts.libraries.yml* above. The content of this file may look something like the following:

```
.layout--threecol-25-50-25 {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.layout__region--first,
.layout__region--third {
  flex-basis:25%;
}

.layout__region--second {
  flex-basis:50%;
}
```

Clear the cache and you should see 3 columns rendered in a row. Since this layout is named *25%-50%-25%* we set the *flex-basis* property accordingly.

Image

![Screenshot of three columns rendered in a row](/sites/default/files/styles/max_800w/public/tutorials/images/three_column_row.png?itok=pg__fj6S)

**Note:** To simplify this example we are applying styles for the desktop. You may want to add breakpoints to adjust the look for smaller screens.

### Modify the Twig template

To transform columns into tabs, we'll need to modify the template to add labels and tab triggers to every column.

Edit the *custom-layouts--threecol-25-50-25.html.twig* file. Add a set of `<div>` tags to use as buttons for the tabs, and a `tab-{N}` and `tab-content` class to each column.

Example:

```
{#
/**
 * @file
 * Default theme implementation for a 3-column layout.
 *
 * This template provides a 3-column 25%-50%-25% display layout.
 */
#}
{%
  set classes = [
    'layout',
    'layout--threecol-25-50-25',
  ]
%}
{% if content|render|trim %}
  <div class="tab-triggers">
    <div class="tab" id="tab-1">Tab 1</div>
    <div class="tab" id="tab-2">Tab 2</div>
    <div class="tab" id="tab-3">Tab 3</div>
  </div>
  <div{{ attributes.addClass(classes) }}>
    <div {{ region_attributes.first.addClass('layout__region', 'layout__region--first', 'layout__region-sidebar', 'region-small', 'tab-1', 'tab-content') }} {% if not region_attributes.first %} class="layout__region layout__region--first layout__region-sidebar region-small tab-1 tab-content" {% endif %}>
      {% if content.first %}
          {{ content.first }}
      {% endif %}
    </div>

    <div {{ region_attributes.second.addClass('layout__region', 'layout__region--second', 'layout__region-main', 'region-medium', 'tab-2', 'tab-content') }} {% if not region_attributes.second %} class="layout__region layout__region--second layout__region-main region-medium tab-2 tab-content" {% endif %}>
      {% if content.second %}
          {{ content.second }}
      {% endif %}
    </div>

    <div {{ region_attributes.third.addClass('layout__region', 'layout__region--third', 'layout__region-sidebar', 'region-small', 'tab-3', 'tab-content') }} {% if not region_attributes.third %} class="layout__region layout__region--third layout__region-sidebar region-small tab-3 tab-content" {% endif %}>
      {% if content.third %}
          {{ content.third }}
      {% endif %}
    </div>

  </div>

{% endif %}
```

In the example above we used the labels *Tab 1*, *Tab 2*, *Tab 3*. You can modify the labels to fit your needs.

Image

![Screenshot of three columns with labels and triggers](/sites/default/files/styles/max_800w/public/tutorials/images/tab_triggers.png?itok=m2rQaKKx)

### Add some JavaScript

To add interactivity, we'll add some JavaScript code that toggles CSS classes to `open` and `closed` tabs.

Add a file called *js/tab.js*, matching what you declared in the *custom\_layouts.libraries.yml* file above, to your module with the following code:

```
(function($, Drupal) {

  'use strict';
  Drupal.behaviors.tabs = {
    attach: function (context, settings) {
      let tab = $('.tab-triggers .tab');
      if (tab.length) {
        tab.on('click', function(e){
          e.preventDefault();
          e.stopPropagation();
          $('.tab-content').removeClass('open');
          $('.tab-content').addClass('closed');
          var id = $(this).attr('id');
          $('.' + id).removeClass('closed').addClass('open');
        });
      }
    }
  };
})(jQuery, Drupal);
```

### Update the CSS

Add the `open` and `closed` classes in your *tabs.css* file to hide and show tabs:

```
.layout--threecol-25-50-25 {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.layout__region--first,
.layout__region--third {
  flex-basis:25%;
}

.layout__region--second {
  flex-basis:50%;
}

.tab-content {
  flex-basis:100%;
}

.open {
  display: block;
}

.closed {
  display: none;
}
```

Clear the cache and press on a tab label. You should notice that the other 2 tabs disappear and the active tab is displayed.

Image

![Screenshot of active tab](/sites/default/files/styles/max_800w/public/tutorials/images/active_tab.png?itok=_pn4SNJp)

Finally, modify the template and add the *open* class to the first tab and the *closed* class to the other two. This way, upon loading the first tab will be open while the other 2 will be closed. Once the user interacts with the triggers, the classes will be switched with JavaScript as we have seen during the previous step.

To better see the changes, add some content to the layout. You should see something similar to the screenshot below.

Image

![Screenshot of demo tabs content](/sites/default/files/styles/max_800w/public/tutorials/images/default_tab.png?itok=Tqd5BYph)

## Recap

In this tutorial, we learned how to define and attach custom CSS and JavaScript to a layout using an asset library. This technique is not limited our tabs example -- it can be used for sliders, accordions, card CTAs with reveal animation, and much more.

## Further your understanding

- What changes need to be made to transform a custom layout into an accordion?
- What other design patterns could be achieved using JavaScript libraries attached to a custom layout?

## Additional resources

- [Layout API](https://www.drupal.org/docs/drupal-apis/layout-api) (Drupal.org)
- [How to register layouts documentation](https://www.drupal.org/docs/drupal-apis/layout-api/how-to-register-layouts) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[How to Add Custom Styles in Drupal's Layout Builder](/tutorial/how-add-custom-styles-drupals-layout-builder?p=2653)

Clear History

Ask Drupalize.Me AI

close