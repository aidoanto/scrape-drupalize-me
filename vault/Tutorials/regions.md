---
title: "Regions"
url: "https://drupalize.me/tutorial/regions?p=3267"
guide: "[[frontend-theming]]"
---

# Regions

## Content

Themes define the regions that are available for site administrators to place blocks in, creating a layout framework within which the components that compose a page can be placed. As a theme developer you'll need to determine what regions are necessary to accommodate your design's layout, while also ensuring it'll work with the way Drupal uses blocks to place content onto the page. Deciding what regions to create requires knowledge of how Drupal works and a clear vision of the design you're trying to achieve.

In this tutorial we'll:

- Explain what regions are and how they relate to themes
- Describe how regions are handled internally within Drupal
- Demonstrate things to keep in mind when planning the regions for your custom theme

By the end of this tutorial you should be able to describe what a region is, explain how Drupal themes use regions to place content, and get started dissecting your own designs into regions.

## Goal

Understand what Drupal uses regions for, and why defining regions is the responsibility of a theme.

## Prerequisites

- [Describe Your Theme with an Info File](https://drupalize.me/tutorial/describe-your-theme-info-file)

Sprout Video

## What is a region?

Regions are areas of a page into which content gets placed. Content is assigned to regions via blocks. If you think of blocks as the base elements used to compose a page, then regions provide the containers within the page where an administrator can place blocks. Regions give your site layout, and your markup its structure.

Themes define regions. Since the theme ultimately controls the layout of a page, it must also specify the set of regions that an administrator can place content into, and how those regions are represented in the HTML markup of the page. A header region might be rendered as an HTML `<header>` and a left sidebar might be an `<aside>` or a `<div>` depending on the requirements of the theme.

Image

![Screenshot of Bartik regions demo](../assets/images/bartik-regions-demo.png)

## Plan your theme's regions

Take the time to evaluate the design you are implementing, the functional needs of your site, how you want it to behave on different viewport sizes, and the type of information you need to display when planning out the regions for your theme. You can always add or remove regions later on in the process, but starting out with a solid foundation will make implementing your theme much smoother in the long run.

When planning regions it's also important to think about *blocks*. How will blocks be used to fill the region, and what that means from both a markup and an administrative UI standpoint. For example, your site's header may contain a logo, a main menu, and a search field. Each of these three elements (with maybe the logo as an exception depending on how you handle it) is represented by a block in Drupal. So you could in theory create a single *header* region and place all three blocks into that region. Or you could create a *header* and a *navigation* region.

Example *header* only:

```
<region>
  <block logo />
  <block main_menu />
  <block search />
</region>
```

Example with multiple regions:

```
<region>
  <block logo />
</region>
<region>
  <block main_menu />
  <block search />
</region>
```

Keep in mind how this could impact a site administrator who needs to figure out what region to place a block into. If your theme will be used by multiple different sites, more regions might help make expectations clearer. If it's a one-off theme and you also control block placement, a single header region may be sufficient.

### Drawing boxes on your wireframes

One of the best ways to get an idea of what regions your theme is going to need is to start with a wire-frame, or a design comp for your theme, get out some crayons, and start drawing boxes around things and labeling them. I generally like to start by trying to identify the things that will be blocks. Then I use that to determine what regions I'm going to need.

Image

![Image showing page with blocks highlighted](../assets/images/concept-regions-blocks.png)

When doing an exercise like this it is important to look at more than one page. Different pages have different content and layout needs. Look for elements that are common to many pages like headers, navigation, and footer, as well as those that only appear in specific designs like a hero image, or a list of "More like this" content at the bottom of an article.

Once you've begun to figure out the blocks on your site, you can begin to think about how those might fit into regions. Keep in mind that not all regions have to have content in them on every page.

Image

![Another image demonstrating regions](../assets/images/concept-regions-regions.png)

### Planning regions for a responsive design

When planning out your regions, keep in mind how the content placed in each region will respond when the site is displayed at different sizes or on different devices. Consider, for example, a page with two columns when displayed on a desktop: content in the left column, and navigation, search bar, ads, and an author bio in the right column, in that order (Figure 1). When the page is viewed at smaller widths, you want to display the navigation and search above the main content, and the ads and author bio below the main content (Figure 2).

#### Figure 1

Image

![region demonstration](../assets/images/concept-regions_03.png)

#### Figure 2

Image

![region demonstration](../assets/images/concept-regions_07.png)

In order to accommodate the smaller layout you'll likely want to create three distinct regions. One holds content, one holds items that appear above the content on mobile devices, and another holds content that appears below the content on mobile devices. Because all blocks placed into a region are grouped together inside of a containing `<div>` that corresponds to the region, this makes the process of creating flexible layouts like this in CSS much easier. It also ensures that when an administrator is adding a new block that wasn't accounted for in the original designs, that it's easy for them to select where that block will appear in the page flow.

## Themes define regions

Regions are represented in a theme's *.info.yml* file as key/value pairs where the key is the internal name of the region used to identify the region in code, and the value is the human readable name used in the user interface when identifying the region. For this reason it's important to use key/value pairs and region names that make sense both in code, and in the UI so that it is easy for anyone to understand the intended use.

The content of a region consists of any blocks placed into the region that are visible on the page currently being viewed, and is generally output in a theme's *page.html.twig* template file inside of wrapping markup like a `div` intended to provide layout and structure.

### Example

```
{% if page.footer %}
<footer role="contentinfo">
  {{ page.footer }}
</footer>
{% endif %}
```

## Default regions

If a theme does not specify a set of regions, Drupal will assume the default set of regions, which correspond with those that are used by the *core/modules/system/templates/page.html.twig* template.

From the documentation for *page.html.twig*, the default regions are:

- page.header: Items for the header region.
- page.primary\_menu: Items for the primary menu region.
- page.secondary\_menu: Items for the secondary menu region.
- page.highlighted: Items for the highlighted content region.
- page.help: Dynamic help text, mostly for admin pages.
- page.content: The main content of the current page.
- page.sidebar\_first: Items for the first sidebar.
- page.sidebar\_second: Items for the second sidebar.
- page.footer: Items for the footer region.
- page.breadcrumb: Items for the breadcrumb region.

## Understanding page\_top and page\_bottom

The page\_top and page\_bottom regions are a special case. Unlike all other regions, which are accounted for in the *page.html.twig* template, these two are used in the *html.html.twig* template—a file that is relatively uncommon to override in a custom theme. The idea is that modules can rely on these two regions being present and use them to output markup at the very top or very bottom of any page. Like, for example, the analytics tracking code placed into the footer of every page by the Google Analytics module, or the markup required for the administrative menu output by Toolbar. Generally when creating a custom theme you'll create your own *page.html.twig* and add your new regions there, but leave the *html.html.twig* intact.

## Hidden regions

You might notice that some of the regions listed above are missing from the options on the Blocks administration page. Both page\_top and page\_bottom are hidden regions, which Drupal intentionally excludes from the user interface so that site administrators can not use the UI to place content into them. Rather, hidden regions act as a placeholder where modules or themes can programmatically add markup. Themes may declare additional hidden regions.

Only regions that have already been declared can be hidden. Use of this feature isn't very common in custom themes, but understanding how it works is important in being able to form a complete picture of how features like page\_top and page\_bottom work.

## Recap

In this tutorial we learned that themes define regions. Drupal then allows site administrators to place page elements into a region. The theme wraps those regions in the necessary markup to achieve the desired layout. Figuring out what regions to declare in your theme requires understanding both your design requirements, and how site administrators will use the tools Drupal provides for placing blocks into regions.

## Further your understanding

- Explain: why are regions defined by themes?
- Regions are optional, so what happens if your theme doesn't define any regions?
- On a screenshot of your website, or one of your favorite news sites, see if you can draw boxes that identify the regions that might be used to create a Drupal theme for this site.

## Additional resources

- Regions are defined in a theme's [.info.yml file](https://drupalize.me/tutorial/describe-your-theme-info-file) (Drupalize.Me)
- Regions are displayed in [a template file](https://drupalize.me/tutorial/what-are-template-files) (Drupalize.Me)
- [Adding Regions to a Theme](https://www.drupal.org/node/2469113) (Drupal.org)
- [Core's page.html.twig file](https://api.drupal.org/api/drupal/core%21modules%21system%21templates%21page.html.twig/11.x) (api.drupal.org)
- [Thinking about regions in your theme](https://drupalize.me/videos/theming-component) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Use a Base Theme](/tutorial/use-base-theme?p=3267)

Next
[Add Regions to a Theme](/tutorial/add-regions-theme?p=3267)

Clear History

Ask Drupalize.Me AI

close