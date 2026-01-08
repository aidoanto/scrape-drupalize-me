---
title: "Modernizr.js in a Theme or Module"
url: "https://drupalize.me/tutorial/modernizrjs-theme-or-module?p=2883"
guide: "[[integrate-javascript-drupal]]"
---

# Modernizr.js in a Theme or Module

## Content

In developing the theme for your website it's important to take accessibility into account. Making your site available and functional for as many users as possible is always a good idea. Progressive enhancement and graceful degradation are key, but how do you go about accounting for the minute differences between browser capabilities? This is where the Modernizr.js library can help you out.

Modernizr is a collection of browser detection tests which allow you, in either CSS or JavaScript, to determine if a particular browser supports a large list of features. From there it can automatically add classes to your page depending on the results of a particular feature test. It can also be used to create additional custom tests. In this tutorial we'll take a look at a few of the feature detection tests that Modernizr natively supports as well as how a custom test can be added to a Drupal theme.

## Goal

Learn about the Modernizr.js library and how to use it to determine if a particular browser supports the features you are using in your site.

## Prerequisites

- [JavaScript in Drupal](https://drupalize.me/tutorial/overview-javascript-drupal)
- [What Are Asset Libraries?](https://drupalize.me/tutorial/what-are-asset-libraries)
- [Define an Asset Library](https://drupalize.me/tutorial/define-asset-library)
- [Attach an Asset Library](https://drupalize.me/tutorial/attach-asset-library)

## What is the Modernizr.js library?

Modernizr.js is a library which provides fast and easy feature detection tests. It allows us to write code that progressively enhances or gracefully degrades in our theme without having to memorize which browsers support which features, and without writing any unreliable user agent sniffing code. Drupal includes *modernizr.js* as an asset library in core. This means that making use of Modernizr is as easy as [attaching the asset library](https://drupalize.me/tutorial/attach-asset-library) from within our theme. Once we have the *modernizr.js* script available in our theme we can use it to do feature detection tests in either JavaScript or CSS. It's also incredibly easy to add our own custom tests. Modernizr also provides a reliable method for testing media queries from within JavaScript. We'll take a look at examples of all of this after seeing what kinds of features Modernizr can test.

The sheer number of features Modernizr can detect can be a bit overwhelming. Rather than reproduce the entire list here, take a look at the [Features detected by Modernizr](https://modernizr.com/docs) heading in the official documentation. Modernizr is capable of testing for everything from ambient light events to web workers. It's important to note that as of the 8.0 release the only test included in the *modernizr.js* library in core is for touch events. Modernizr can be used to write custom tests, but if you want to make use of any of the other built-in tests you'll need a custom build of *modernizr.js* and to override the asset library included in core. Thankfully, Modernizr makes that a pretty easy process.

The Modernizr team has included a helpful [interactive custom build tool](https://modernizr.com/download) which makes building a customized Modernizr library a snap. Since these customized builds only include a particular subset of tests, the resulting file size of the library will be as small as possible. This minimizes the amount of JavaScript loaded when the library is used, which helps improve front-end performance. It's beyond the scope of this tutorial, but the [Modernizr documentation](https://modernizr.com/docs) includes additional notes on using [npm](https://www.npmjs.com) and [Grunt](http://gruntjs.com/) to allow you to customize Modernizr without using this interactive download tool.

For our custom build, we're going to add tests for Cross-Origin Resource Sharing, Cookies, and Emoji. We're also going to add options for `Modernizr.addTest()`, `Modernizr.mq()`, `Modernizr.testAllProps()`, and `Modernizr.testProp()`. This will ensure we can still add our own custom features tests with the `addTest` method, and additionally test media queries from within JavaScript with `Modernizr.mq()`. It's worth noting that this subset of functionality does not include everything included by Drupal core. This may cause some unexpected behavior, but will be fine for our examples. If you're curious about what tests Drupal core's version of Modernizr includes you can find out by looking at the top of the `modernizr.min.js` file (`http://modernizr.com/download/?-details-inputtypes-touchevents-addtest-prefixes-setclasses-teststyles`).

## Add a custom Modernizr build to Drupal

After we've made our customization selections and clicked the build button we're given the option to copy or download our custom build. We can also download the command line configuration (and grunt configuration) for our customized build. If we include the configuration file in our custom theme, it will be easy to tell what options and tests we've included in our build without trying to read minified JavaScript. Now that we have these two files, *modernizr-custom.js* and *modernizr-config.json* we can add them to our Drupal theme.

We can override the Modernizr library provided by core by adding to our theme's *THEMENAME.info.yml* file. We're going to continue using the [Retro theme (.zip)](https://drupalize.me/sites/default/files/tutorials/retro-drupal-10.zip) from the [Attach an Asset Library](https://drupalize.me/tutorial/attach-asset-library) tutorial. In *retro.info.yml* we can specify our override for Modernizr using [libraries-override](https://www.drupal.org/theme-guide/8/assets#override-extend):

```
  libraries-override:
    # Replace the core modernizr library with our custom build.
    core/modernizr:
      js:
        assets/vendor/modernizr/modernizr.min.js: js/modernizr-custom.js
```

With this change, and the *modernizr-custom.js* file we downloaded in place, we need to [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) in order to see the changes on our site. There are two easy ways to verify that our changes have been successful. First, and easiest, is to turn off JavaScript aggregation. With aggregation off, we can view source and see the full path to the *modernizr.js* script being loaded. If everything is working as expected, we should see this path as */themes/custom/retro/js/modernizr-custom.js*. Another way to tell if we're using our custom build is to inspect the source and take a look at the classes added to the root `<html>` element. Since we've added tests for cross-origin resource-sharing (CORS), canvas, cookies and emoji we will see corresponding classes in our HTML. Here is a look at the classes in Chrome, Safari and Firefox:

Image

![Modernizr classes in multiple browsers](/sites/default/files/styles/max_800w/public/tutorials/images/browser-tests_1.png?itok=YEpFHImp)

## Modernizr feature detection in JavaScript

Modernizr adds classes, based on the tests we've specified in our custom build, to the root `<html>` element on each page of our site. We can now add CSS to account for the presence (or absence) of a particular feature. Similar tests are also available to our custom JavaScript. If we want to know if a particular browser supports emoji, we can check the `Modernizr.emoji` property. Properties are set on the Modernizr object for each test included in our build. If we open up the web inspector console, we can run code like this:

```
  if (Modernizr.emoji) {
    alert('Use emoji!')
  } else {
    console.log('no emoji for you');
  }
```

We can also add our own tests to Modernizr. For example, if we wanted some of our code to only be executed on Mondays we could add:

```
  Modernizr.addTest('itsMonday', function() {
    var d = new Date();
    return d.getDay() === 1;
  });
```

Adding a test like this then makes `Modernizr.itsmonday` elsewhere in our code just like the other built-in tests.

We can also use modernizr.js to detect media queries from within JavaScript.

```
  if (Modernizr.mq('(min-width: 9000px)')) {
    // Show something extra for crazy-big screens.
  }
```

The [updated Retro theme (.zip)](https://drupalize.me/sites/default/files/tutorials/retro-modernizr.zip "Retro theme with updated Modernizr") now includes our Modernizr override, and our custom emoji JavaScript which makes use of Modernizr tests. Look through the official library documentation. What other kinds of functionality would be useful to test for in your theme?

## Recap

Modernizr is a collection of browser detection tests which allow you, in either CSS or JavaScript, to determine if a particular browser supports a large list of features. From there it can automatically add classes to your page depending on the results of a particular feature test. It can also be used to create additional custom tests.

## Further your understanding

- [Create a theme to play with theme development concepts](https://drupalize.me/guide/hands-on-theming), add the Modernizr library, and play around with it.

## Additional resources

- [Modernizr.com](https://modernizr.com)
- [Modernizr.com API](https://modernizr.com/docs#modernizr-api)
- [Retro theme with updated Modernizr (.zip)](https://drupalize.me/sites/default/files/tutorials/retro-modernizr.zip "Retro theme with updated Modernizr") (Drupalize.Me)

Downloads

[Retro theme with updated Modernizr](/sites/default/files/thacaphathuhicleclibredredanaluuarospouostuwreuaswatroswugamuslamojispuwrinagiwriswodawotrastotropispuspubapupruspicrouovometochiwistowrophihithuchistadrouastobenafrocetuph "thacaphathuhicleclibredredanaluuarospouostuwreuaswatroswugamuslamojispuwrinagiwriswodawotrastotropispuspubapupruspicrouovometochiwistowrophihithuchistadrouastobenafrocetuph")

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Standardize Your JavaScript with ESLint](/tutorial/standardize-your-javascript-eslint?p=2883)

Next
[Underscore.js in a Theme or Module](/tutorial/underscorejs-theme-or-module?p=2883)

Clear History

Ask Drupalize.Me AI

close