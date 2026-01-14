---
title: "What Is a Theme?free"
url: "https://drupalize.me/tutorial/what-theme?p=3266"
guide: "[[frontend-theming]]"
order: 1
---

# What Is a Theme?free

## Content

Themes are the part of Drupal that you, and anyone else visiting your Drupal powered application, see when they view any page in their browser. You can think of a theme as a layer, kind of like a screen, that exists between your Drupal content and the users of your site. Whenever a page is requested Drupal does the work of assembling the content to display into structured data which is then handed off to the presentation layer to determine how to visually represent the data provided.

Drupal themes are created by front-end developer. Frequently referred to as *themers*, or *theme developers*. Themes consist of standard web assets like CSS, JavaScript, and images, combined with Drupal-specific templates for generating HTML markup, and YAML files for telling Drupal about the file and features that make up each individual theme.

In this tutorial we'll:

- Explain what a Drupal theme is.
- Explain the role of a Drupal themer in the process of building a Drupal site.
- Get a high level overview of the types of files/code that themes are made of.

By the end of this tutorial you should be able to explain what a Drupal theme is, and the kind of work a Drupal theme developer will be expected to do.

## Goal

Explain what the role of a theme is, and the kind of code they are composed of.

## Prerequisites

- None

Sprout Video

## Themes in Drupal sites

Themes are what make a Drupal website look the way it does. Themers, or theme developers, use HTML, CSS, JavaScript, and other front-end assets in order to implement a design for their site. Each individual theme is a collection of files that define the presentation layer for your application. Themes are generally one of the first places where code is customized for a Drupal site, and are in many cases unique to the specific site they were created for.

Rather than starting from scratch, Drupal themes start from an existing HTML framework and make changes as needed by overriding and changing just the necessary templates. Some themes only need to modify a few select bits, while others may choose to override nearly everything. Either way, if it's HTML, you can change it with a theme.

In order for this to work, every component in Drupal that needs to display something in the browser provides a simple, minimal, HTML template for that element. Whether it's the content of a node, the site logo displayed in the header, or even the header region itself, the required HTML is rendered from a template. These templates can be overridden by a theme in order to change the markup they generate.

Themes are used to:

- Change the HTML markup of anything in Drupal
- Add CSS styles to change the layout, color, or typography on one or more pages
- Use JavaScript to enhance the user experience

Most themes will combine changes to HTML markup with new CSS files that provide the layout and overall graphical treatment of a site, and JavaScript that modifies the ways users interact with the content of the page. Combine all of this, and you can make Drupal look, and feel, like anything you can imagine.

Without having to write any code for a theme you can:

- [Install, enable, and configure an existing theme through the Drupal interface](https://drupalize.me/tutorial/download-install-and-uninstall-themes)
- Download and install new themes from Drupal.org

Once you're ready to start creating your own custom theme or modifying an existing theme you'll want to know about:

- [The structure and organization of a theme's files](https://drupalize.me/tutorial/structure-theme)
- [Describing your theme with an info file](https://drupalize.me/tutorial/describe-your-theme-info-file)
- [Using base themes](https://drupalize.me/tutorial/theme-inheritance-base-themes)
- [Defining regions](https://drupalize.me/tutorial/regions)
- [The Twig template language](https://drupalize.me/tutorial/twig-drupal)
- [Overriding template files](https://drupalize.me/tutorial/override-template-file)
- [Adding CSS, and JavaScript asset libraries](https://drupalize.me/tutorial/attach-asset-library)
- [Using PHP for additional preprocessing of dynamic content](https://drupalize.me/tutorial/what-are-preprocess-functions)

## Background knowledge

Themers are expected to be masters of HTML and CSS. Experience with JavaScript is often important. To fully understand and edit template files, build onto the foundation of a Drupal theme some basic PHP, a bit of YAML, and programming concepts such as variables and conditional statements.

- [Our Favorite HTML and CSS Resources](https://drupalize.me/blog/201409/our-favorite-html-css-tutorials-resources) — Do you need to brush up on HTML or CSS? You’ll get the most out of our Drupal theming tutorials if you already have a good foundation with these basic web technologies. This list contains some of our favorite resources and references around the Internet related to HTML and CSS.
- [JavaScript Resources on MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript) — The Mozilla Developer Network (MDN) provides reference and tutorial documentation for many web technologies. Check out their beginning, intermediate, and advanced JavaScript tutorials, a comprehensive JavaScript reference section, and links to web-based tools for writing and debugging JavaScript code.
- [YAML](https://drupalize.me/videos/introduction-yaml) — As a themer, you’ll need to know how to create, edit, and understand YAML syntax.

## Recap

In this tutorial we learned that themes are the part of Drupal that someone sees and interacts with when the visit any of the pages of your Drupal site. This includes content editors working in the sites administration section. Themes are built using a combination of Drupal-specific files and common web assets. In the Drupal community developers who work on themes are commonly called *themers* or *theme developers*.

## Further your understanding

- What types of files can you expect to find in a Drupal theme? How does this relate to front-end development you've done in the past?
- What should someone study to become a theme developer?

## Additional resources

- [Theming Drupal](https://www.drupal.org/docs/theming-drupal) (Drupal.org)
- [Search for contributed Drupal themes](https://www.drupal.org/project/project_theme) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Download, Install, and Uninstall Themes](/tutorial/download-install-and-uninstall-themes?p=3266)

Clear History

Ask Drupalize.Me AI

close