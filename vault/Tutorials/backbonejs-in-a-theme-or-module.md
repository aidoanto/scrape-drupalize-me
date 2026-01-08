---
title: "Backbone.js in a Theme or Module"
url: "https://drupalize.me/tutorial/backbonejs-theme-or-module?p=2883"
guide: "[[integrate-javascript-drupal]]"
---

# Backbone.js in a Theme or Module

## Content

## This page is archived

We're keeping this page up as a courtesy to folks who may need to refer to old instructions. We don't plan to update this page.

### Alternate resources

The public Backbone and Underscore core libraries have been removed. These dependencies are now deprecated and for internal use only. Backbone.js will eventually be removed from Drupal core. Read more at [drupal 10.0.0 release notes (Frontend (CSS and JavaScript) dependency changes)](https://www.drupal.org/project/drupal/releases/10.0.0).

It's probably not too surprising that a library called Backbone aims to provide structure to your front-end JavaScript code and applications. In this tutorial we'll take a look at how Backbone.js goes about achieving that goal, and how you can make use of it on your Drupal site. We'll first take a high-level look at the main components that make up the Backbone.js library. With that basic understanding in place we'll look at an example of how you might integrate Backbone.js into a Drupal site.

## Goal

Learn about Backbone.js and explore an example of integrating it into a Drupal site.

## Prerequisites

- [JavaScript in Drupal](https://drupalize.me/tutorial/overview-javascript-drupal)

## Backbone library deprecated and will be removed

The Backbone library was deprecated in Drupal 9.4.0/10.0.0 and marked as "internal usage only". It will be removed in a future version of Drupal and no new code should depend on it being in core. The functionality provided by Backbone will be replaced with Vanilla JS. Learn more in [[META] Re-evaluate use of Backbone.js in core](https://www.drupal.org/project/drupal/issues/3145958).

## Backbone: structure for a complex front end

As websites have evolved from simple, static informational documents to full-blown interactive applications, the complexity of front-end code has exploded. As the interactions on your site become more and more complex, it becomes increasingly difficult to reason about the state of a particular piece of data on the page, especially if its "state" is shared and displayed in multiple locations. The increasing popularity of front-end JavaScript frameworks has a lot to do with this increasing client-side complexity. One of the earlier, and most popular, frameworks is Backbone.js. Rather than relying on manipulating the DOM with jQuery, and having to deal with complicated selectors, nested callbacks and the difficulty of managing shared state, Backbone.js can help provide structure to our application. This, ultimately, makes it easier to model and reason about the code. In this tutorial we're going to take a quick look at the main pieces that make up the Backbone.js library. Then we'll see how you might begin to leverage it with a Drupal site to minimize page refreshes.

## Introducing Backbone's main components

Just like with [Underscore.js](https://drupalize.me/tutorial/underscorejs-theme-or-module), the [annotated Backbone.js source code](https://backbonejs.org/docs/backbone.html) is a really good resource for fully understanding the library. From a high level, the Backbone team describes the framework this way:

> Philosophically, Backbone is an attempt to discover the minimal set of data-structuring (models and collections) and user interface (views and URLs) primitives that are generally useful when building web applications with JavaScript.

Backbone.js itself is small, lightweight, and agnostic about which template library you use to render the views in your application. It's also mature, having originally been released in 2010, and has a demonstrated history of scaling well. One look at the list of [example](https://en.wikipedia.org/wiki/Backbone.js) [applications](https://backbonejs.org/#examples) will give you a sense of how many other large sites rely on Backbone.js.

### Model

The first main Backbone component we need to understand is the [Model](https://backbonejs.org/#Model). When you bundle the data attributes, computed properties, validation rules and behavior for a given portion of your site you're building a model. In Backbone.js models are explicitly created by calling `Backbone.Model.extend({})` and passing in an object that captures the data, functionality, and structure you're trying to encapsulate. Later in this tutorial, on our example Drupal site, we're going to create a simple model called Posts. You can probably already guess what some of the data attributes and methods our Post model might have.

### Collection

Another handy Backbone.js primitive is the [Collection](https://backbonejs.org/#Collection). A collection is simply a list of ordered models. You might already guess that we could reason about a listing of posts on the page as a collection. Collections have their own set of helper methods to make it easier to do things like sort, slice, compare collections, and sync them back to the database.

### Views

Once we have the data on our pages modeled properly we need to figure out how to display that data. This is where Backbone's Views come in. Views themselves don't actually determine the HTML that gets rendered, since Backbone allows you to use any templating library you like. Instead views in Backbone terms are simple organizational objects (associated with models) that allow the interface to be updated after corresponding changes to the data in a model without the entire page being refreshed. In other words, views are a place to bind events together between the data model layer and the template responsible for displaying that data on the page. In the Drupal blog example we would use views to handle overriding the behavior of the "read more" and pager links on a node listing page.

### URLs

The other key component in Backbone.js that we haven't already covered are URLs. In order to make our new application search engine friendly, and allow users to share URLs, we need a way to update the URL of the page we're on (without triggering a page refresh). We're also going to need to find a way to handle the URL route, on the client side, and map that to a particular action. Another way to think about this is that any particular view that you'd like to render independently needs its own URL pattern so Backbone knows which template to render (with which arguments).

Let's dig in to each of these primitives in more detail by looking at examples in Drupal. We'll use blog posts and the Drupal core module, Quick Edit, to illustrate these concepts.

## Example: Create a Backbone Model for a blog post

For a simple example, we're going to look at how we could create Backbone.js Models for a Drupal-based blog. The home page of the blog will be Drupal's traditional listing of node teasers with a "read more" link and a pager at the bottom. It would be really nice if the read more link and the pager links didn't trigger page refreshes and instead could just load new data in the main content area of our site. The good news is we can use Backbone.js to make this happen relatively easily. If you're not already familiar with building a REST API in Drupal to expose data as JSON it might be a good idea to first visit [this tutorial](https://drupalize.me/videos/exposing-your-api-drupal-8), and read this [blog post](https://drupalize.me/blog/201401/introduction-restful-web-services-drupal-8).

The two endpoints we need for our application need to be able to return data for a single post (*node/#*) and a post listing with support for a pager (*node?page=#*). The actual data we need from our REST API will be more clear as we figure out our Backbone Model and Collection. Here is an example response from a REST export display created with Drupal's Views module:

Image

![Node listing from a Views REST export display](/sites/default/files/styles/max_800w/public/tutorials/images/api-views-node-listing-json.png?itok=AaQqrvU5)

For our simple blog example we're only going to create one Backbone Model. We can get a good idea of which data attributes we need to track in our blog model based on the API response we see from Drupal above. We won't be making use of all of the attributes Drupal exposes by default, so let's simplify these down to: title, path, body, teaser, author, published date, and node id. It's important to note that often times we might not be building both the front and back end of a site. When we're consuming a 3rd party API from Twitter or GitHub we may have to filter the API data on the client. In this case the API coming from our Drupal site is easy to manipulate using Drupal's Views module, so we don't have to do any client-side filtering.

First, we create our Post model. When we define this model we can add any number of methods, helper functions, or computed data attributes that might come in handy in developing our application.

```
var Post = Backbone.Model.extend({

  initialize: function() {... },
  constructor: function() {... },
  parse: function(data, options) {
    // This is kind of like a preprocess function.
    // If the API returned more data than we're interested in we might want
    // to pick out just the values we are interested in.
    var posts = _.map(data, function(item) {
      return _.pick(item, 'title', 'path', 'body', 'teaser', 'author', 'created', 'nid');
    });
  },
  // Defaults can be set up to account for missing properties for a given node.
  defaults: {
      'title': '',
      'path': '',
      'body': '',
      'teaser': '',
      'author': '',
      'created': '',
      'nid': '',
  },
  // A computed property: Check the data for this Post to see if we're looking at
  // something published in the last month
  isNew: function(post) {
    var currentDate = new Date();
    var timeAgo = currentDate.getTime() - post.created;
    if (timeAgo <= 60*60*24*30 ) return true;
  }
});
```

By default when you create any instance of a model in Backbone, the initial attribute values passed into the instance will be set on the model. In the case of our Post model, the defaults probably don't make sense, but it's a handy feature to know about when you need it.

The [Backbone.js documentation](https://backbonejs.org/#Model) outlines all of the various helper methods available for working with models. The most useful are `get()`, `set()`, and `clear()`. Beyond the scope of this tutorial is the `sync()` method. This can be incredibly useful to save the updated state of your model back to the server. Functionality like this could be used, for example, for in-line editing. In fact if you'd like to see this in more detail within Drupal core, take a look at the Quick Edit module (*core/modules/quickedit/js/models* in particular).

## Example: Backbone Collections of blog posts

Now that we have a basic model created for posts, let's take a look at collections. [Collections in Backbone.js](https://backbonejs.org/#Collection) are ordered sets of models. They have their own set of helper methods for dealing with things like comparing, slicing, popping, sorting, cloning, etc. Additionally they have a `fetch()` method for retrieving data from a remote server. To create a collection we extend the Backbone Collection object, and let it know which model the collection contains:

```
Backbone.Collection.extend({
  model: Post
});
```

Just like with models, collections have a `sync()` method which can be used to save data to the server. The [Backbone.sync](http://backbonejs.org/#Sync) function can be used for creating, reading, updating or deleting data. Once the sync request is made, by default it returns a [jQuery jqXHR object](https://api.jquery.com/jQuery.ajax/#jqXHR). This response can then be used to trigger other callbacks or fire off other events that propagate to any model or collection that is bound to them. Using the Quick Edit module again as an example, *EntityModel.js* handles saving data via the `entitySaverAjax` function which in turn calls `Drupal.ajax()`. Defined in *core/misc/ajax.js* `Drupal.ajax()` is a simple convenience wrapper around jQuery's AJAX function. While the Drupal AJAX API provides these utility wrappers, it's also possible to rely on [jQuery's AJAX API](https://api.jquery.com/jQuery.ajax/) as well.

## How Backbone renders HTML

In order to actually render HTML with Backbone.js there are a couple of things of which we need to be aware. First, as they say in the official [Backbone.js documentation](https://backbonejs.org/#View):

> Backbone views are almost more convention than they are code — they don't determine anything about your HTML or CSS for you, and can be used with any JavaScript templating library.

This means that in order to render HTML we need to not only create Backbone Views, but also decide on a template library. For simplicity's sake, in this example we'll use in-line HTML and the built in [template functions provided by Underscore.js](https://underscorejs.org/#template). Referring to the Quick Edit module as our example, we can see in-line HTML being utilized as templates in *core/modules/quickedit/js/theme.js*.

If views in Backbone aren't actually responsible for defining a template, or controlling what HTML is rendered on the page what purpose do they serve? Views' basic function is that of glue code, connecting the render method of a view to events registered in a model, like changing data values. In order to understand how views do this, we should first take a look at [Events](https://backbonejs.org/#Events)

## Manage state changes with Backbone Events

Backbone Events can be bound to any object. This means that any object can bind a callback function that will be invoked when a particular named event is triggered by another object. If we look again at the Quick Edit module, and in particular the EntityModel's initialization method we can see this event binding in action: *core/modules/quickedit/js/models/EntityModel.js*

```
initialize: function () {
this.set('fields', new Drupal.quickedit.FieldCollection());

// Respond to entity state changes.
this.listenTo(this, 'change:state', this.stateChange);

// The state of the entity is largely dependent on the state of its
// fields.
this.listenTo(this.get('fields'), 'change:state', this.fieldStateChange);

// Call Drupal.quickedit.BaseModel's initialize() method.
Drupal.quickedit.BaseModel.prototype.initialize.call(this);
},
```

The EntityModel is using Backbone's `listenTo()` method to register callbacks for the `change:state` event. When this event fires both `this.stateChange` and `this.fieldStateChange` will be called with the appropriate arguments.

## Example: Backbone Events in Quick Edit module

Another, but different, example of event registration in Quick Edit module can be found in *EditorView.js*. The `initialize` method of the view registers an event listener: *core/modules/quickedit/js/views/EditorView.js*

```
initialize: function (options) {
  this.fieldModel = options.fieldModel;
  this.listenTo(this.fieldModel, 'change:state', this.stateChange);
},
```

Taking a closer look at the callback registered by this event the `stateChange` function:

```
 stateChange: function (fieldModel, state) {
  var from = fieldModel.previous('state');
  var to = state;
  switch (to) {
  ...
      case 'saving':
          // When the user has indicated he wants to save his changes to this
          // field, this state will be entered. If the previous saving attempt
          // resulted in validation errors, the previous state will be
          // 'invalid'. Clean up those validation errors while the user is
          // saving.
          if (from === 'invalid') {
            this.removeValidationErrors();
          }
          this.save();
          break;
```

Following this `save()` function we find that it's tracking a `fieldModel`, `editorModel` and something called `backstageId` used to handle intermediate data. It then loads the `quickedit` form and handles saving it via AJAX using `Drupal.quickedit.util.form.ajaxifySaving()`.

It is by registering these event listeners that Backbone's Events can be used to either update data within a model or trigger a re-rendering of a view. Backbone.js has [several built-in events](https://backbonejs.org/#Events-catalog) that are worth becoming familiar with when figuring out how to bind your models and views together.

## Example: Backbone Views in Quick Edit module

Views, acting predominantly as glue between models and the templates that become DOM elements, contain modules configuration code. Creating a view can be done by extending the `Backbone.View` object. A good illustrative example can be found in *core/modules/quickedit/js/views/EntityToolbarView.js* (snippets of which are shown below):

```
Drupal.quickedit.EntityToolbarView = Backbone.View.extend(/** @lends Drupal.quickedit.EntityToolbarView# */{

events: function () {
  var map = {
    'click button.action-save': 'onClickSave',
    'click button.action-cancel': 'onClickCancel',
    'mouseenter': 'onMouseenter'
  };
  return map;
},
initialize: function (options) {

  // Rerender whenever the entity state changes.
  this.listenTo(this.model, 'change:isActive change:isDirty change:state', this.render);
  // Also rerender whenever a different field is highlighted or activated.
  this.listenTo(this.appModel, 'change:highlightedField change:activeField', this.render);
  // Rerender when a field of the entity changes state.
  this.listenTo(this.model.get('fields'), 'change:state', this.fieldStateChange);

  // Initial render.
  this.render();
}
```

Then `render()` method calls `$(Drupal.theme('quickeditEntityToolbarFence'))` which then renders the actual template specified in *core/modules/quickedit/js/theme.js*.

## Explore more examples in core

The flexibility of Backbone.js is simultaneously a strength and a weakness. Understanding the architecture of Backbone.js applications can be a bit tricky because of this flexibility. In my experience the excellent examples provided by core (in both the Quick Edit and Contextual modules) can really help illustrate how Models and Views can be used to reduce the complexity around dynamic functionality and provide additional structure to JavaScript.

## Recap

In this tutorial we looked at how Backbone aims to provide structure to your front-end JavaScript code and applications. We looked at the main components that make up the Backbone.js library and an example of how you could integrate Backbone.js into a Drupal site.

## Further your understanding

- Explore the Quick Edit and Contextual modules to see how they implement Backbone.js.

## Additional resources

- [Backbone.js library](https://backbonejs.org) (backbonejs.org)
- [Annotated Backbone.js source code](https://backbonejs.org/docs/backbone.html) (Backbonejs.org)
- [Example: TODO MVC Backbone.js](https://backbonejs.org/examples/todos/index.html) (Backbonejs.org)
- [Backbone.js Examples and Tutorials](https://github.com/jashkenas/backbone/wiki/Tutorials%2C-blog-posts-and-example-sites) from jashkenas (the original author of Backbone.js on github.com)
- [Exposing Your API in Drupal 8](https://drupalize.me/videos/exposing-your-api-drupal-8?p=2360) (Drupalize.Me)
- [An Introduction to RESTful Web Services in Drupal 8](https://drupalize.me/blog/201401/introduction-restful-web-services-drupal-8) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Underscore.js in a Theme or Module](/tutorial/underscorejs-theme-or-module?p=2883)

Clear History

Ask Drupalize.Me AI

close