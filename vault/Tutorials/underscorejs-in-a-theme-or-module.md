---
title: "Underscore.js in a Theme or Module"
url: "https://drupalize.me/tutorial/underscorejs-theme-or-module?p=2883"
guide: "[[integrate-javascript-drupal]]"
---

# Underscore.js in a Theme or Module

## Content

## This page is archived

We're keeping this page up as a courtesy to folks who may need to refer to old instructions. We don't plan to update this page.

### Alternate resources

See the related [change record](https://www.drupal.org/node/3273118) for information on how to update your Underscore code with vanilla JS.

Underscore.js is a very small library which provides several utility functions and helpers to make working with JavaScript a little bit easier. In this tutorial we'll take a look at a part of the library, learn where the full library is documented, and see how we can make use of Underscore.js in a custom block on our Drupal site.

## Goal

Learn about the Underscore.js library and how to use it in a Drupal site.

## Prerequisites

- [JavaScript in Drupal](https://drupalize.me/tutorial/overview-javascript-drupal)

## Underscore.js library removed from Drupal 10

The Underscore.js library was deprecated in Drupal 9.4.0 and marked as "internal usage only". It was removed in Drupal 10.0.0. Learn more in this change record: [Underscore library is deprecated](https://www.drupal.org/node/3273118).

## What is Underscore.js?

Underscore.js is a very mature and well-documented JavaScript library. In the project's own words:

> Underscore is a JavaScript library that provides a whole mess of useful functional programming helpers without extending any built-in objects. It’s the answer to the question: “If I sit down in front of a blank HTML page, and want to start being productive immediately, what do I need?” ...and the tie to go along with jQuery's tux and Backbone's suspenders.

## Background: Underscore.js

The first release of the project came in 2009, so to say Underscore has been around a while is a bit of an understatement. The best way to investigate and learn what Underscore.js is all about is via the [project documentation](https://underscorejs.org/). Another interesting learning resource is the [annotated source](https://underscorejs.org/docs/underscore-esm.html) of Underscore.js itself. Browsing the 100+ functions that compose the library will give you an idea of how Underscore.js can make data manipulation in JavaScript easier.

The first important thing to realize is that Underscore documentation refers to *collections*. Collections can be either JavaScript objects or arrays. The first two functions, and the two we'll be looking at in detail in the exercise below, are [each](https://underscorejs.org/#each) and [map](https://underscorejs.org/#map). We will also take a look at the [template](https://underscorejs.org/#template) compilation built into Underscore.

## What problem are we going to solve with Underscore.js?

Before we dig into an example, let's set up the problem we're going to solve. In our example exercise we want to display the top contributed modules from Drupal.org (by download count) in a block on our site. In order to do this we first need to find a way to identify the top modules, then we need to create a custom block in which we can display them. Normally this could all be done in PHP from within a custom module, but let's assume the data we retrieve about the modules can be used in multiple places on our site. Rather than processing all of the Drupal.org data on the server, we will send it all to the client as a large JSON object. We will then use the Underscore.js library to help us filter and display the data we're interested in. Here is the raw data from <https://drupal.org/project/usage>.

Image

![https://www.drupal.org/project/usage](/sites/default/files/styles/max_800w/public/tutorials/images/project_usage.png?itok=75wTeXaw)

Rather than just scraping this HTML, we can make use of [the API provided by Drupal.org](https://www.drupal.org/drupalorg/api). We're going to be querying by node type (`project_module`) and then sorting the results by `field_download_count` to see the most popular modules first. The URL we're interested in is:

```
https://www.drupal.org/api-d7/node.json?type=project_module&sort=field_download_count&direction=DESC
```

This API request contains far more data than we need to make our simple block. Ordinarily we could make this request within the PHP of our custom module, and handle all of the filtering there. For this particular example, let's assume we're going to make use of some of this data elsewhere on our site. In order to reuse the data from our custom module we're going to add the entire JSON response to `drupalSettings`.

## Display the block

Writing a custom module to display a block is beyond the scope of this tutorial. You can either [download the module's zip file here](https://drupalize.me/sites/default/files/tutorials/do_projects.zip) or refer to [Creating custom blocks](https://www.drupal.org/docs/creating-custom-modules/creating-custom-blocks) on Drupal.org.

So we don't have to wait on a network request while developing our module, I've saved the response from the Drupal.org API in a local file called *do\_project.listing.json*. Here is the `DoProjectListingBlock::build` from our custom module:

```
  /**
   * {@inheritdoc}
   */
public function build() {
  $build = [];
  // The underscore library is already available via dependencies.
  // Make an http request to the drupal.org API.
  // https://www.drupal.org/api-d7/node.json?type=project_module&sort=field_download_count&direction=DESC
  // Pass the full JSON along to the page via drupalSettings.
  $do = file_get_contents(drupal_get_path('module', 'do_projects') .'/do_project.listing.json');
  $do_json = json_decode($do);

  $build['do_project_listing_block'] = array(
    '#markup' => 'Implement DoProjectListingBlock.',
    '#attached' => array(
      'library' => array(
        'do_projects/do_projects.projects'
      ),
      'drupalSettings' => array(
        'doProjects' => array(
          'projects' => $do_json
        )
      )
    )
  );
```

## The returned JSON object

By passing the JSON along from the Drupal.org API, it will be available in our front-end and accessible via the `drupalSettings` object at `drupalSettings.doProjects.projects`. From a quick examination in the browser's console we can see just how much data is actually provided by the API.

Image

![doProjects snippet](/sites/default/files/styles/max_800w/public/tutorials/images/drupalsettings.doprojects.snip_.png?itok=gM6REZDh)

## Filter the JSON object with Underscore.js

Filtering the large amount of API data into an object that is easier to work with is where the Underscore.js library can really help us out. We will create a new JavaScript file `doProjects.js` for the library specified in the `DoProjectListingBlock::build` method in our module. This file needs to create a Drupal behavior for our module. We can then make use of Underscore's map function to iterate over all of this JSON and pick out just the module name (`title` field) and download count (`field_download_count`).

```
(function ($, Drupal, drupalSettings) {

    Drupal.behaviors.doProjectsBehavior = {
       attach: function (context, settings) {
         // This is where we're storing the JSON from the Drupal.org API response.
         var projects = drupalSettings.doProjects.projects;

         var modules = {};
         // Use underscore to filter the API response to only the fields we care about
         // title and download count.
         _.map(projects.list, function (project, i) {
             modules[project.title] = project.field_download_count;
           });
       }
    }
})(jQuery, Drupal, drupalSettings);
```

By using `map` we now have a new object `modules` that contains each Drupal.org module's name and download count.

## Add HTML with Underscore templates

With our data filtered, we're going to make use of Underscore's built-in template compilation to make building the HTML output of our block a little easier.

First, we define the actual template string we're going to pass data into.

```
  var output = _.template("<li><%= title %>: <%= download_count %></li>");
```

Since we're going to wrap each project in a list item (`<li>`) tag we also need to set up the main unordered list. With that in place we'll use the `each` function to render our template once for each module.

```
  var blockContent = '<ul>';
// Using the each method we can iterate over our modules object and pass the
// values through our Underscore template.
_.each(modules, function(count, name) {
  blockContent += output({"title": name, "download_count": count});
});

blockContent += '</ul>';
```

Lastly, we'll replace the content of our custom block with the value of `blockContent`.

```
  $('#block-doprojectlistingblock-2.content').html(blockContent);
```

After enabling our custom module, and adding our new block to the second sidebar, we can see our hard work in action:

Image

![module count block](/sites/default/files/styles/max_800w/public/tutorials/images/module_count_block.png?itok=6qObTarW)

While this example may seem a bit contrived, the Underscore.js library can greatly simplify your code any time you're dealing with relatively large and complex JSON objects. The library contains more than 100 utility functions for making your JavaScript more functional. To further your understanding of Underscore, try improving on the example `doProjects.js` by using the `filter` method.

## Recap

In this tutorial we took a look at a part of the Underscore.js library, learned where the full library is documented, and saw how we could make use of Underscore.js in a custom block on our Drupal site.

## Further your understanding

- Try improving on the example `doProjects.js` by using the `filter` method.
- Learn more about [using server-side settings with drupalSettings](https://drupalize.me/tutorial/use-server-side-settings-drupalsettings).

## Additional resources

- [Underscore library is deprecated](https://www.drupal.org/node/3273118) (Drupal.org)
- [Underscorejs.org and documentation](http://underscorejs.org) (underscorejs.org)
- [A contributors' library for Underscore](http://documentcloud.github.io/underscore-contrib/) (GitHub.io)
- [Adding Custom Blocks to your custom Module](https://www.drupal.org/node/2465705) (Drupal.org)
- [Drupal.org’s APIs](https://www.drupal.org/drupalorg/api) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Modernizr.js in a Theme or Module](/tutorial/modernizrjs-theme-or-module?p=2883)

Next
[Backbone.js in a Theme or Module](/tutorial/backbonejs-theme-or-module?p=2883)

Clear History

Ask Drupalize.Me AI

close