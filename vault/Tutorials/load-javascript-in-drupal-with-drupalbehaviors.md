---
title: "Load JavaScript in Drupal with Drupal.behaviors"
url: "https://drupalize.me/tutorial/load-javascript-drupal-drupalbehaviors?p=2883"
guide: "[[integrate-javascript-drupal]]"
order: 2
---

# Load JavaScript in Drupal with Drupal.behaviors

## Content

Anyone writing JavaScript for Drupal should use the `Drupal.behaviors` API when writing their custom JavaScript functionality. Doing so ensures that your JavaScript is executed at the appropriate times during the life cycle of a page, such as when the page loads, or after new DOM elements have been added via an AJAX request.

In this tutorial we'll look at:

- The problem that `Drupal.behaviors` solves
- How to use `Drupal.behaviors` when writing your JavaScript code

By the end of this tutorial you should be able to explain what the `Drupal.behaviors` API is, and be able to use it in your own JavaScript.

## Goal

Demonstrate how to use the `Drupal.behaviors` API when writing JavaScript that manipulates the DOM.

## Prerequisites

- [JavaScript in Drupal](https://drupalize.me/tutorial/overview-javascript-drupal)

## Why Drupal.behaviors?

Most JavaScript works by manipulating elements in the HTML DOM. As such, JavaScript code generally does some extra work to ensure that the DOM is fully loaded, and the elements you want to interact with are available, before executing. Failure to do so can cause your custom behavior to not function as expected.

The non-Drupal equivalent is using JavaScript's `document.addEventListener("DOMContentLoaded", function(){})`, or jQuery's `$(document).ready()` syntax. Placing your code inside this statement will ensure that it is not executed until the DOM has finished loading.

Drupal takes this a step further using `Drupal.behaviors` to ensure that your JavaScript isn't executed prematurely, and to make sure it's executed again whenever the DOM changes so that your functionality will be applied to any new elements. This generally happens when AJAX requests add new content to the page.

Furthermore, modules or themes that dynamically update the DOM can call `Drupal.attachBehaviors` to ensure that any JavaScript functionality will work for those new elements as well.

Over on the Lullabot blog, Juampy has [a great article](https://www.lullabot.com/articles/understanding-javascript-behaviors-in-drupal), with a real-world example, that explains why this is important.

Unless you have a really good reason not to, you should use the `Drupal.behaviors` API to attach your custom JavaScript to the page.

## Use Drupal.behaviors to attach new functionality

Using `Drupal.behaviors` to attach your functionality requires that you register a new object with the behaviors system. This is done by adding a new object as an element on the `Drupal.behaviors` object.

The new object needs to have at least an `attach` method. Anytime `Drupal.attachBehaviors` is called it will iterate through all behavior objects and call their respective `attach` methods.

```
(function ($, window, Drupal) {

  Drupal.behaviors.exampleTheme = {
    attach: function (context, settings) {
      // Your custom JavaScript goes inside this function ...

      $('.example', context).click(function () {
        $(this).next('ul').toggle('show');
      });
    }
  };

})(jQuery, window, Drupal);
```

Note the use of the closure in this example. The rest of this tutorial assumes you're writing JavaScript code inside a similar closure. Learn more about why in [Wrap Your Custom JavaScript in a Closure](https://drupalize.me/tutorial/wrap-your-custom-javascript-closure).

In order to avoid collisions, the convention is to prefix your object with the name of your module or theme. For example, if our theme is named `icecream` we might do something like:

```
Drupal.behaviors.icecreamAnimation = {};
```

In the event that 2 different projects use the same behavior name whichever one is loaded last will be used, and all others will be silently discarded.

Calls to a behavior object's `attach` method receive two arguments; `context`, and `settings`. The `context` argument contains DOM elements to act on, and the `settings` object contains any JavaScript settings added by Drupal/PHP. [Learn more about using dynamic server-side settings in this tutorial](https://drupalize.me/tutorial/use-server-side-settings-drupalsettings).

## Don't forget context

When calling the `attach` method for all behaviors Drupal passes along a `context` variable. This variable contains the HTML DOM elements that you should attach your custom behaviors to. During the initial page load this will be the complete HTMLDocument; during subsequent calls this will be just the elements that are being added to the page. Using `context` in conjunction with any jQuery selectors in your code ensures you don't attach duplicate behaviors to the same element.

Example:

```
Drupal.behaviors.icecreamAnimation = {
  attach: function(context, settings) {
    $(context).find('a.cool-link').on('click', function() {
      // Do something cool when the link is clicked.
    });
  }
}
```

Forgetting to use the `context` variable in your selectors is a really common mistake that can lead to inefficient code that puts undue load on the browser or make it tricky to find bugs.

## Detach behaviors

The converse to the `attach` method is `Drupal.behaviors.icecreamAnimation.detach`. Any code in the `detach` method will be called whenever content is removed from the DOM. Allowing JavaScript behaviors to be detached from the element before it's removed. This can be especially useful for expensive tasks like polling, which could continue to run in the background even if the DOM element they are working on has been removed.

Implement behavior detaching in your code by adding a `detach` method to your behavior object.

```
Drupal.behaviors.icecreamAnimation.detach = function(context, setting, trigger) {
  // Your code here
}
```

Learn more by reading the [`Drupal.detachBehaviors` documentation](http://read.theodoreb.net/drupal-jsapi/Drupal.html#.detachBehaviors).

Here's an example from Drupal core's File module which applies a behavior to all file upload elements, and then detaches it anytime one is removed from the page.

```
Drupal.behaviors.fileAutoUpload = {
  attach: function (context) {
    ...
  },
  detach: function (context, setting, trigger) {
    if (trigger === 'unload') {
      $(context).find('input[type="file"]').removeOnce('auto-file-upload').off('.autoFileUpload');
    }
  }
};
```

## Behind the scenes

You can learn a lot more about how the attaching and detaching of behaviors works by taking a look at these two functions:

- [`Drupal.attachBehaviors`](http://read.theodoreb.net/drupal-jsapi/Drupal.html#.attachBehaviors) is the code that loops over any registered behavior and calls the `attach` method
- [`Drupal.detachBehaviors`](http://read.theodoreb.net/drupal-jsapi/Drupal.html#.detachBehaviors) is the code that loops over any registered behavior object and calls its `detach` method.

## Recap

In this tutorial we learned why anyone writing JavaScript for Drupal should use the `Drupal.behaviors` API when writing their custom JavaScript functionality. Doing so ensures that your JavaScript is executed at the appropriate times during the life cycle of a page, such as when the page loads, or after new DOM elements have been added via an AJAX request.

Using `Drupal.behaviors` to attach your functionality requires that you register a new object with the behaviors system. This is done by adding a new object as an element on the `Drupal.behaviors` object.

## Further your understanding

- Explain the purpose of using `Drupal.behaviors` in your code.
- Give some examples of things that might trigger Drupal to attempt to attach JavaScript behaviors to the page a second time.
- What would happen if two modules registered a behavior object with the same name? Example `Drupal.behaviors.blakeHall`?
- Update your JavaScript to use the `Drupal.behaviors` instead of `$(document).ready()` or other methods of waiting for the DOM to load.

## Additional resources

- [Blog post on Lullabot.com with practical examples of why Drupal.behaviors are important](https://www.lullabot.com/articles/understanding-javascript-behaviors-in-drupal) (Lullabot.com)
- [JavaScript API overview](https://www.drupal.org/node/2269515) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview: JavaScript in Drupal](/tutorial/overview-javascript-drupal?p=2883)

Next
[Wrap Your Custom JavaScript in a Closure](/tutorial/wrap-your-custom-javascript-closure?p=2883)

Clear History

Ask Drupalize.Me AI

close