---
title: "Functional JavaScript Testing with Nightwatch.js"
url: "https://drupalize.me/tutorial/functional-javascript-testing-nightwatchjs?p=3263"
guide: "[[test-drupal-sites-automated-tests]]"
---

# Functional JavaScript Testing with Nightwatch.js

## Content

The testing suite for the Drupalize.Me site uses a different strategy for functional JavaScript testing. We use a tool called [Nightwatch.js](http://nightwatchjs.org/) that allows us to write our tests in JavaScript that runs commands against a web browser. This browser automation allows us to test the types of interactions that a typical user of our website might encounter. It also allows us to test JavaScript code using JavaScript, and execute our tests in different browsers. In this tutorial we'll take a look at how to set up Nightwatch.js, and what the syntax looks like for a couple of basic tests.

## Goal

- Learn how to set up and configure Nightwatch.js for your project
- Understand the basic syntax for creating a test
- Learn how to run Nightwatch.js tests

## Prerequisites

- [Node.js and npm installed](https://nodejs.org/en/download/package-manager/) on your system.
- [Java Development Kit (JDK)](http://www.oracle.com/technetwork/java/javase/downloads/index.html) with at least version 7.

## Installing Nightwatch.js

Assuming you already have node.js and npm installed on your system, you can install nightwatch.js by running `npm install -g nightwatch`. This will make Nightwatch available anywhere on your system.

However, it's not quite that easy. There are more pieces involved to configure a working setup.

Nightwatch.js just helps simplify the use of the [Web Driver API](https://www.w3.org/TR/webdriver). This API can be used to standardize common browser tasks like clicking links, submitting forms, or navigating between pages. In order to have a fully working setup we also need a Web Driver server. The most popular choice here is Selenium. Mozilla, Google, and Microsoft all have versions of web driver servers that you [can use along with Nightwatch](https://nightwatchjs.org/guide/getting-started/introduction.html#browser-support-table). There are also services like [Sauce Labs](https://saucelabs.com/) that provide Selenium servers as a service.

The easiest way to get Selenium running on our machine is to download the jar file from the [downloads page](https://selenium-release.storage.googleapis.com/index.html). You can then start Selenium using:

`java -jar selenium-server-standalone-{VERSION}.jar`

With nightwatch.js installed, and a Selenium server running, we're ready to start configuring our test suite.

## Nightwatch.js configuration

In the Drupalize.Me codebase we have a separate directory for all of the code and configuration that supports our various testing suites. Here is a look at what our Nightwatch directory looks like:

Image

![Nightwatch directory file organization](../assets/images/nightwatch_directory.png)

Notice that we're using a `nightwatch.config.js` to pass along configuration information to Nightwatch at run time. There are a couple of options we can use to specify additional configuration information. The easiest method is to create a nightwatch.json file in the directory that will contain our tests. This approach has some drawbacks that you're likely to encounter relatively quickly. Instead of creating a `nightwatch.json` file for our configuration we'll create a file called `nightwatch.config.js`. Our configuration will be exported as a JavaScript module. If you're unfamiliar with modules in JavaScript, they are a mechanism you can use to share code. The [Eloquent JavaScript site](https://eloquentjavascript.net/10_modules.html) has a great introduction to this module concept if it is new to you. For now, we'll simply start our configuration file by creating the skeleton of a module in the `nightwatch.config.js` file.

```
module.exports = {}
```

By using a JavaScript module to encapsulate our configuration instead of a simple json file we are able to use dynamic variables in our configuration, add comments, and execute any other JavaScript code we might need to run prior to executing our test suite. For example, in the Drupalize.Me codebase we use this to set up the directory names where we store screen shots for tests that fail (`assets`), code that ensures we have the Selenium server and appropriate web drivers available as expected (`global.js`), and a directory to store reports of each test run (`reports`).

The [configuration guide in the Nightwatch documentation](https://nightwatchjs.org/guide/configuration/settings.html) is a comprehensive resource for detailing all of the options for this configuration file. We'll build up a simple example with some common options (and the ones that we use in testing this site).

```
module.exports = {
  'src_folders' : [ 'tests' ], // The directory name where you store test files.
  'globals_path': './global.js',
  'custom_command_path': './custom-commands',
  'test_settings': {
    'default': {
      'launch_url': 'http://local.example.com',
      'selenium_port': 9515
      'selenium_host': 'localhost',
      'desiredCapabilities' : {
        'browserName' : 'chrome',
        'javascriptEnabled': true,
        'acceptSslCerts' : true,
        'chromeOptions' : {
          // Remove --headless if you want to watch the browser execute these
          // tests in real time.
          'args' : ["--no-sandbox", "--headless"]
        }   
      },  
      'screenshots': {
        'enabled': true, // if you want to keep screenshots
        'path': './screenshots' // save screenshots here
      },  
      'globals': {
        'waitForConditionTimeout': 5000 // sometimes internet is slow, so wait.
      },
    }
  }
}
```

The configuration object that we're exporting in this file tells Nightwatch that it can find our test files in a directory called `tests`. It will also load the `global.js` file which makes sure our site is accessible, and Selenium and the various web drivers are where we expect them to be. We're also specifying a directory `custom-commands` where we can create our own utility commands. In the Drupalize.Me codebase these custom commands include things like logging in and out of the site, filling out the payment forms, and creating random text strings of various lengths.

The `test_settings` portion of our configuration object is perhaps the most important. Here we tell Nightwatch what url it should launch by default when starting a test run. We also specify the port and hostname of the Selenium server, and which browser we will be testing against. It's also possible to provide additional test environments beyond the `default` environment we've configured here. In fact, it's a good idea to create configuration for any of the environments you may want to test against. At Drupalize.Me we have configuration to test against our local development servers, our shared development server, and our QA server. This makes it easy for us to quickly run our test suite against different environments to provide a sanity check against failing tests.

## Writing a test

With the configuration in place we're ready to start writing tests. We'll start with a simple test that checks for a particular string of text on our homepage. Since our configuration file specifies that our tests will be found in a `tests` directory we'll place our test there. It's also worth noting that you can create additional organizational structure inside of this directory based on your needs. In the Drupalize.Me codebase we organize our tests based on membership type and status, so we're going to create a sub-directory for anonymous users. We'll start our homepage tests in the file `tests/anonymous_user/homepage.js`.

```
module.exports = {
  '@tags': ['homepage', 'anon'],
  'Anonymous Homepage' : function (browser) {
    browser.url(browser.launch_url)
    .waitForElementVisible('body')
    .assert.containsText('body', 'Our trainers are talented teachers with over 35 years of combined Drupal experience. They make learning fun and effective.')
    .end();
  }
}
```

Our file contains a test exported as a JavaScript module. The `@tags` object provides some metadata about the types of things this test contains. We'll see how these tags are used later in the tutorial when we look at running tests. Next we have our test `Anonymous Homepage`. This contains a function, which is passed a `browser` object, which defines the steps and assertions for our actual test case. In this example we tell the browser to open a page with the `launch_url` address. You may notice that the `launch_url` was specified in our configuration file. Nightwatch includes these configuration settings and makes them available to the browser object that is passed into our tests.

Once the browser navigates to our `launch_url` we tell it to wait until the `<body>` element is visible. This ensures that our page is loaded before we attempt any additional steps. There are two main ways you can test your page using Nightwatch, these are by using the `expect` and `assert` methods. In our test here we use `assert` to ensure that the `<body>` tag on our homepage contains the string "Our trainers are talented teachers with over 35 years of combined Drupal experience. They make learning fun and effective." If this string is present, our test will pass successfully.

The `expect` assertion syntax is a bit more verbose, but thanks to Nightwatch it makes your test code read a bit more like proper English. We could rewrite the `assert` statement in our test using `expect` like so:

```
browser.expect.element('body').to.be.visible;
  .expect.element('body').text.to.contain('Our trainers are talented teachers with over 35 years of combined Drupal experience. They make learning fun and effective.');
```

Either approach is perfectly valid syntax. The method you choose to use in your tests is largely a matter of personal preference. You can find the full documentation for both `expect` and `assert` in the [Nightwatch.js API Reference](https://nightwatchjs.org/api/) documentation.

Let's take a look at a slightly more complex example. We'd like to write a test to make sure our site administrators can create blog posts on our site. First we'll create a new sub-directory inside `tests` called `site_administrator`. Inside that directory we'll create a file called `create_blog.js`. Here's what that file might look like:

```
var randomString = require('random-string');

module.exports = {
  '@tags': ['blog', 'site_administrator'],
  before: function(browser) {
    browser.login('[email protected]', 'Reputat10n')
  },

  'Create new blog post': function(browser) {
    browser.url(browser.launch_url + '/node/add/blog-post')
      .setValue('input[id=edit-title]', 'Shake It Off')
      .setValue('textarea.text-summary', 'Best choice artist for Dance Music Friday - Taylor Swift')
      .setValue('textarea.text-full', randomString())
      .setValue('fieldset.node-form-options input#edit-status.form-checkbox', 1)
      .click('div.form-actions input[id=edit-submit]')
      .pause(2000)
      .assert.containsText('div.messages.status', 'Blog post Shake It Off has been created')
      .end();
  },
}
```

In this test, just like in our first example, we're exporting a JavaScript module that contains our actual test code. But you may notice that we're also doing a couple of other interesting things as well. First we're requiring an additional module from npm `random-string`. If you're following along on your local environment you can install this module with `npm install random-string`. We'll use this to create random strings of text when creating our content. You may also notice that before we define our `Create new blog post` test we have specified a `before` property on our test object. This function will be executed before our test runs. Here we're using it to call a custom `login` command to make sure we'll be viewing the pages in our test as an authenticated site administrator.

Within the test function itself we navigate our browser to the blog post creation page (`launch_url + '/node/add/blog-post'`). We then use the `setValue` method to fill out the node form, providing a title, summary, and body text. This method can also be used to check checkboxes, like the one specifying that our blog post should be published. We then use the `click` method to save our post. The `pause` method sets a time out for our test runner to give the site time to actually create our new piece of content. After this two second pause we use `assert` to look for Drupal's message area and ensure that it contains a status message that our blog post has been created.

There are dozens of additional commands you can use with Nightwatch that allow you to do things like get and set cookie values, change the size of your browser window, and take screenshots. Covering all of these is beyond the scope of this tutorial, but the [API Reference](https://nightwatchjs.org/api/) documentation is a great resource for learning more.

## Running tests

Now that we've written a couple of tests, let's figure out how to run them. How we go about executing Nightwatch will depend in part on how it was installed. If you installed Nightwatch globally on your system (with `npm install -g nightwatch`) you can just run `nightwatch` from the command line right from the directory that holds your configuration file. If you didn't install Nightwatch globally you may need to provide the full path to the Nightwatch file (likely in `node_modules/.bin/nightwatch`). For our purposes here, we're going to assume Nightwatch is globally installed and we can just execute it directly.

With Nightwatch you can run the entire test suite, a single test, or some combination based on the flags and options you provide on the command line. It's worth noting that we don't need to explicitly include our configuration file here because we've used a naming convention where it will be automatically discovered. It's typically included with the `-c` or `--config` flag.

To start, we could run our homepage test with the command:

```
nightwatch tests/anonymous_user/homepage.js
```

And here is what our expected output will look like:

```
[Anonymous User / Homepage] Test Suite
==========================================

Running:  Anonymous Homepage
✔ Element <body> was visible after 22 milliseconds.
✔ Testing if element <body> contains text: "Our trainers are talented teachers with over 35 years of combined Drupal experience. They make learning fun and effective.".

OK. 2 assertions passed. (3.434s)
```

Remember those `@tags` we included in our tests earlier? They become especially useful as our test suite grows ever larger. We can use the `--tags` or `--skiptags` command to limit the tests we run to a particular tag. With this we can run our anonymous user tests with `nightwatch --tags anon` instead of needing to know the exact paths of each file that tests anonymous user behavior.

There are many additional command line options you can use while running tests. The [Nightwatch guide Running Tests](https://nightwatchjs.org/guide/running-tests/) covers all of the options in depth.

## Recap

In this tutorial we learned how to use Nightwatch.js to perform functional JavaScript tests of our site. We learned how to install and configure Nightwatch, what the basic syntax for writing tests looks like, and some of the options we can use to run our tests. Nightwatch allows us to write tests that can run against multiple browsers, and since it's independent of Drupal it can be used to test non-Drupal sites as well.

## Further your understanding

- Using the Nightwatch.js documentation, try modifying your *nightwatch.config.js* file to support multiple test environments.
- What command line option could you pass to Nightwatch so that it only runs test files with the string 'homepage' in the file name?

## Additional resources

- [Installing node.js](https://drupalize.me/videos/install-nodejs-and-nodejs-drupal-module?p=2348) (Drupalize.Me)
- [Installing node.js with a package manager](https://nodejs.org/en/download/package-manager/) (nodejs.org)
- [Nightwatchjs Docs: Getting Started](https://nightwatchjs.org/guide/getting-started/) (Nightwatchjs.org)
- [API reference](https://nightwatchjs.org/api/) (Nightwatchjs.org)
- [Leverage JS for JS testing (using Nightwatch)](https://www.drupal.org/project/drupal/issues/2869825) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Run Functional JavaScript Tests](/tutorial/run-functional-javascript-tests?p=3263)

Next
[Run Drupal Tests with the run-tests.sh Script](/tutorial/run-drupal-tests-run-testssh-script?p=3263)

Clear History

Ask Drupalize.Me AI

close