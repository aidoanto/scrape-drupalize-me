---
title: "Wrap Your Custom JavaScript in a Closure"
url: "https://drupalize.me/tutorial/wrap-your-custom-javascript-closure?p=2883"
guide: "[[integrate-javascript-drupal]]"
order: 3
---

# Wrap Your Custom JavaScript in a Closure

## Content

Maybe you've heard of anonymous closures but you're not quite sure how they apply in Drupal, or why using them is considered a best-practice. Anonymous closures allow you to avoid accidentally clashing with anything in the global scope, as well as to alias the jQuery object to the more commonly used `$`. This is necessary because Drupal runs jQuery in no-conflict mode. This tutorial will look at the syntax used for placing your custom JavaScript code inside an anonymous closure, and why it's a good idea to do so.

In this tutorial we'll:

- Explain what a closure is (briefly), and what immediately invoked function expressions are
- Show how typically Drupal JavaScript gets wrapped in a closure
- Provide a copy/paste example you can use in your own code

By the end of this tutorial you should be able to explain what an anonymous closure is, and how to use one in your custom JavaScript for Drupal.

## Goal

Understand the purpose of the anonymous closure you see in almost every Drupal JavaScript file.

## Prerequisites

- None

## Wrap your Drupal-specific JavaScript with this closure

If you've looked at any of the JavaScript files included in Drupal's core, you've probably come across something like this (from */core/modules/block/js/block.js*):

```
// "iffy" closure.
(function ($, window, Drupal) {

  // My custom JavaScript code ...
  Drupal.behaviors.blockSettingsSummary = {
    attach: function attach() {
      // ... <snip>
  };

})(jQuery, window, Drupal);
```

**Pro tip:** Writing your own JavaScript for Drupal? Copy and paste the above code, then replace the innards with your custom code.

If you've ever wondered why Drupal JavaScript files start with a parentheses, and are entirely wrapped in this strange looking function-thing, or if you've ever had to open another JavaScript file to copy and paste this type of syntax, you're in the right place. In this tutorial we're going to figure out what Drupal is doing here by learning about anonymous closures.

## Variable scope and anonymous closures

In order to understand what Drupal is doing here it's important to understand variable scope in JavaScript. Within a function you have access to variables in both the local and global scope. In practice this looks something like this:

```
  var name = 'Blake';

  function friendlyGreeting() {
    var greeting = 'Howdy ';

    return greeting;
  }

  console.log(friendlyGreeting() + name);
```

If you execute this code in the console of your browser's developer tools you'll see the string, 'Howdy Blake', logged. Within the scope of the function `friendlyGreeting` the variable `greeting` has local scope while the variable `name` has global scope. The `friendlyGreeting` function has access to both variables in its local scope as well as those in the global scope. The interesting thing happening here is that outside of the `friendlyGreeting` function we do not have access to the `greeting` variable. Essentially we've made `greeting` a private variable by wrapping it in a function. Another interesting property of the `friendlyGreeting` function is that it *remembers* the context in which it is executed. This is why the `name` variable is available inside the function. The relationship where a nested function has access to the arguments and variables passed into an outer function is what we mean by a *closure*.

## IIFE (*iffy*)

But wait, what else is going on with those parentheses in the examples from Drupal core? These parentheses are an example of an [immediately invoked function expression](http://benalman.com/news/2010/11/immediately-invoked-function-expression/) (IIFE).

The initial opening parentheses defines an anonymous function which helps prevent the function's scope from polluting the global scope of the entire application. Since, thanks to closures, the global application state is available within our nested function, it is easier to maintain cleaner interactions between JavaScript files and reduces the overall likelihood of collisions in the global namespace. You can pass arguments to your anonymous function by including them as arguments at the end of the function definition. In fact, this is what actually causes the anonymous function to be executed (ie: the immediately invoked part of the *IIFE*).

Here is a simple example of a IIFE in action.

```
  (function(greeting, name) {
    console.log(greeting + ' ' + name);
  })('Howdy', 'Blake');
```

## Recap

We've created an anonymous function, and immediately invoked it passing in the parameters `Howdy` and `Blake`. Running this in our developer console produces the same logging text we saw in the regular function example above. If we try to access either the `greeting` or the `name` variable from outside of our anonymous function we'll see that they are undefined. They are only in scope from within our anonymous function. Hopefully by now it's clear why Drupal uses the IIFE best practice to define the JavaScript provided by modules and themes.

## Further your understanding

- Can you find other examples in Drupal core of IIFEs?
- How do IIFE simplify the JavaScript for code that depends on jQuery? (Hint: it has to do with the syntax required for working with `noConflict` mode)
- How do closures impact Drupal's use of [strict mode](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode)?

## Additional resources

- [How do JavaScript closures work](http://stackoverflow.com/questions/111102/how-do-JavaScript-closures-work) (stackoverflow.com)
- [Let's Learn JavaScript Closures](https://medium.freecodecamp.com/lets-learn-javascript-closures-66feb44f6a44) (medium.freecodecamp.com)
- [Closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures) (developer.mozilla.org)
- [Immediately-Invoked Function Expression](http://benalman.com/news/2010/11/immediately-invoked-function-expression/) (benalman.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Load JavaScript in Drupal with Drupal.behaviors](/tutorial/load-javascript-drupal-drupalbehaviors?p=2883)

Next
[Use Server-Side Settings with drupalSettings](/tutorial/use-server-side-settings-drupalsettings?p=2883)

Clear History

Ask Drupalize.Me AI

close