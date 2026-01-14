---
title: "Implement Drupal Functional Test Dependencies"
url: "https://drupalize.me/tutorial/implement-drupal-functional-test-dependencies?p=3264"
guide: "[[test-drupal-sites-automated-tests]]"
order: 13
---

# Implement Drupal Functional Test Dependencies

## Content

Previously, in [Implement a Functional Test](https://drupalize.me/tutorial/implement-functional-test), we learned how to tell `BrowserTestBase` to use the Standard installation profile in order to get our test passing, letting the Standard profile implicitly provide our dependencies. We mentioned that doing so probably wasn't the best decision and that we should *explicitly* declare those dependencies instead.

In this tutorial, we'll walk through how to explicitly declare our test's dependencies. When in doubt, it's generally considered a best practice to be as explicit about the dependencies of our tests as possible. By the end of this tutorial, you should be able to:

- Understand why we want to explicitly declare our dependencies.
- Determine what the dependencies really are and make a list of them.
- Implement each dependency in our list.
- Emerge with a thorough passing test.

## Goal

Be able to explicitly declare dependencies in a functional test within a Drupal site.

## Prerequisites

- A Drupal codebase with development requirements installed through Composer. See [Install Drupal Development Requirements with Composer](https://drupalize.me/tutorial/install-drupal-development-requirements-composer).
- A local development environment. (We recommend that you [Install Drupal Locally with DDEV](https://drupalize.me/tutorial/install-drupal-locally-ddev).)
- [Organize Test Files](https://drupalize.me/tutorial/organize-test-files)
- [Run Drupal Tests with PHPUnit](https://drupalize.me/tutorial/run-drupal-tests-phpunit)
- [Set up a Functional Test](https://drupalize.me/tutorial/set-functional-test)
- [Implement a Functional Test](https://drupalize.me/tutorial/implement-functional-test)

## A brief recap

Let's step back a little bit and get our bearings.

We designed a passing test that checks the basic functionality of the node search form.

It turns out that this test has quite a few dependencies which are conveniently provided by the Drupal Standard profile. The class we're extending, `BrowserTestBase`, defaults to using the *Testing* profile. We got the test passing by overriding the `$profile` property and set it to use `standard`.

Specifying the Standard profile as a dependency isn't a best practice. While it works, it comes with some extra baggage. What part of the Standard profile are we depending on? And likely to cause our test to fail down the road when the profile changes in ways we have no control over. Instead, we need to tell `BrowserTestBase` about each of our test's dependencies.

Let's talk about our test's dependencies and why we have them.

## The Testing profile

By default, `BrowserTestBase` uses a profile called Testing. This profile is fine for most testing needs. It doesn't have a lot of dependencies. It doesn't enable many modules, and it delivers fairly neutral output without theming. This allows for speedier tests which are mostly isolated from the effects of specific profiles, modules, or themes.

## The Standard profile

When we manually walked through our test steps in [Implement a Functional Test](https://drupalize.me/tutorial/implement-functional-test), we used the Standard profile. This profile enables lots of modules and uses the Olivero theme. It also places the search block, which is what we're testing.

## Figuring out our dependencies

We have learned that our test depends on some modules and maybe a profile.

We need the Search form block, and we need to be able to successfully submit it, and view the search results page. This means we'll need a route, and probably a permission to search nodes. We'll need to find out which modules provide the individual system components that we'll use when phpunit runs our test.

### Set up a test class

Let's start by setting up a new test class. Normally, we'd just replace an existing test with this new code, but since we want to keep the code from part one for comparison, let's create a new test class.

The test from part one was called `FrontPageSearchFormTest`.

Let's call the new one `FrontPageSearchFormDependenciesTest`.

For now, we'll just copy over the code from `FrontPageSearchFormTest`, update the class name, remove the `$profile` override. Here's what our new test class looks like:

```
<?php

namespace Drupal\Tests\my_testing_module\Functional;

use Drupal\Tests\BrowserTestBase;

/**
 * Tests basic functionality of search form on the front page.
 *
 * @group demo
 */
class FrontPageSearchFormDependenciesTest extends BrowserTestBase {
  /**
   * {@inheritdoc}
   */
  protected $defaultTheme = 'stark';

  /**
   * Tests that we can submit the search form and get no results.
   *
   * We'll open the front page, enter 'test' into the search form,
   * check for success, then check for the no-results text.
   */
  public function testSearchFormNoResults() {
    // Step 1: Visit '/' path.
    $this->drupalGet('');
    // Step 2. Enter `test` into the search form and submit.
    $inputs = ['keys' => 'test'];
    $this->submitForm($inputs, 'Search');
    // Step 3: Check that the form submitted to a reachable page.
    $this->assertSession()->statusCodeEquals(200);
    // 4. Check for no-results text.
    $this->assertSession()->pageTextContains('Your search yielded no results');
  }
}
```

### Take note of the dependencies

The behavior we're testing depends on the following things:

- The Search module. The Search module provides the search functionality, the block containing the form, and the permission `search content`.
- The Node module. Since we're searching nodes, we'll need the Node module installed. The search results path is dynamically generated based on the type of entities we're searching, `node`, by default.
- The Block module. We're going to need a search form block, so in order to add it, we need the Block module.
- The User module. The Standard profile enables this module, but Testing does not. Therefore, we explicitly need it, since we'll need to log in a user that has `search content` permission.
- The Search form block. The Standard profile provides this block and its themes (Olivero or Stark) both place this block so that it's accessible from the front page.
- A permission. As already mentioned, we'll need to make sure the user has permission to search content.

That's quite a few dependencies. We'll also assume that we're going to write many tests using these dependencies, so we'll move the dependencies to the `setUp()` method.

The `setUp()` method allows us to set up some dependencies before every test method. This allows us to have consistent dependencies for every test.

We call this sort of set up a *fixture*. Our tests will then test against the fixture site.

### Specifying modules

Let's look at the list of dependencies we created previously:

- The Search module
- The Node module
- The Block module
- The User module
- The search form block
- A permission

We need the Search, Node, Block, and User modules. These are the easiest dependencies to add.

Much like the `$profile` property we talked about earlier, we can tell `BrowserTestBase` to enable these modules by overriding the `BrowserTestBase::$modules` value:

```
  protected static $modules = ['search', 'node', 'block', 'user'];
```

Note that `$modules` is a static property.

`BrowserTestBase` will now add Search, Node, Block, and User to the list of modules to enable for this test class.

### Use `setUp()` for our dependencies

Let's assume we're going to all the trouble of setting up these dependencies, so we can re-use them in more than one test method.

That gives us a chance to demonstrate how to use `setUp()`.

Since we're using `setUp()` we also need some class properties to store the things we set up.

In the `setup()` method, we always need to call the parent `setup()`, so that it can also set things up. We'll type hint the return value to `void`. Here's what that looks like:

```
  protected function setUp(): void {
    // Always call the parent setUp().
    parent::setUp();
  }
```

Now we can begin to add our dependencies.

### Place a block with `placeBlock()`

Our shrinking list of dependencies:

- ~~The Search module~~
- ~~The Node module~~
- ~~The Block module~~
- ~~The User module~~
- The search form block
- A permission.

Dealing with the Tools menu block is a little bit tricky. We have to figure out how the Standard profile does it, and then replicate that.

The code part is not very complicated. `BrowserTestBase` gives us a method called `placeBlock()` which will place the block in an arbitrary region on the page. We could specify which region we'd prefer, but we don't actually have a preference in this case.

Here's our `setUp()` method with this code added:

```
  protected function setUp(): void {
    // Always call the parent setUp().
    parent::setUp();
    $this->placeBlock($plugin_id);
  }
```

But what's that `$plugin_id` variable? It should be the plugin name of the block we wish to place. Let's find it.

There are several ways we could go about this. You could export your site's config (e.g. with Drush: `drush cex`), and then look for the appropriate config file. Or, since blocks are placed within a theme's region, and the Standard profile's default theme is Olivero, you could also poke around in *core/themes/olivero/config* (both *install* and *optional*) for the config item for the search block.

You'll recall from the [previous tutorial](https://drupalize.me/tutorial/implement-functional-test) that we care about the Search form block, which we saw in the Olivero theme. We'd be looking for a config file with the keywords, `block`, `olivero`, `search` and `form` in the name. We found 2 files that matched in the *optional* config directory:

- *block.block.olivero\_search\_form\_wide.yml*
- *block.block.olivero\_search\_form\_narrow.yml*

We want to discover the plugin ID of the block. So let's open either of these YAML files and figure it out (hint: they use the same plugin id):

```
uuid: c365e19f-a855-4ae1-b19a-625ce5d67781
langcode: en
status: true
dependencies:
  module:
    - search
  theme:
    - olivero
_core:
  default_config_hash: imMyHD6LYci0gtXq56qr9ZKGHzbEG9uFydrN5EhKtSU
id: olivero_search_form_wide
theme: olivero
region: secondary_menu
weight: -5
provider: null
plugin: search_form_block
settings:
  id: search_form_block
  label: 'Search form (wide)'
  label_display: '0'
  provider: search
  page_id: ''
visibility: {  }
```

The `plugin` key tells us that the plugin ID is `search_form_block`.

Some other plugin IDs might not be so obvious. In that case, we can use this tutorial to help us find existing plugin IDs: [Discover Existing Plugin IDs](https://drupalize.me/tutorial/discover-existing-plugin-types).

We can add `search_form_block` to our `setUp()` using the `placeBlock()` method:

```
  protected function setUp(): void {
    // Always call the parent setUp().
    parent::setUp();
    $this->placeBlock('search_form_block');
  }
```

Now every test method will have a pre-installed Search form block. Since we didn't specify a name for the block, the name will be random, and not 'Search.'

### Grant the user permissions with `createUser()`

Only one dependency remains:

- ~~The Search module~~
- ~~The Node module~~
- ~~The Block module~~
- ~~The User module~~
- ~~The search form block~~
- A permission.

We've got the Search module enabled, which means we have the `search content` permission available to us. Now we need to give the test user permission use the search form. The way we do that is to create a user with one or more permissions. Since we're searching content, it stands to reason that we'll need to give our use permission to `access content` as well.

```
    // Create and log in user.
    $this->drupalLogin(
      $this->createUser([
        'search content',
        'access content',
      ])
    );
```

### Run the test

We've handled all the dependencies:

- ~~The Search module~~
- ~~The Node module~~
- ~~The Block module~~
- ~~The User module~~
- ~~The search form block~~
- ~~A permission.~~

And here's what our test looks like, in the end:

```
<?php

namespace Drupal\Tests\my_testing_module\Functional;

use Drupal\Tests\BrowserTestBase;

/**
 * Tests basic functionality of search form on the front page.
 *
 * @group demo
 */
class FrontPageSearchFormDependenciesTest extends BrowserTestBase {
  /**
   * {@inheritdoc}
   */
  protected $defaultTheme = 'stark';

  /**
   * {@inheritdoc}
   */
  protected static $modules = ['search', 'node', 'block', 'user'];

  /**
   * Set up dependencies for our test.
   */

  protected function setUp(): void {
    // Always call the parent setUp().
    parent::setUp();
    $this->drupalPlaceBlock('search_form_block');

    // Create and log in user.
    $this->drupalLogin(
      $this->createUser([
        'access content',
        'search content'
      ])
    );
  }

  /**
   * Tests that we can submit the search form and get no results.
   *
   * We'll open the front page, enter 'test' into the search form,
   * check for success, then check for the no-results text.
   */
  public function testSearchFormNoResults() {
    // Step 1: Visit '/' path.
    $this->drupalGet('');
    // Step 2. Enter `test` into the search form and submit.
    $inputs = ['keys' => 'test'];
    $this->submitForm($inputs, 'Search');
    // Step 3: Check that the form submitted to a reachable page.
    $this->assertSession()->statusCodeEquals(200);
    // 4. Check for no-results text.
    $this->assertSession()->pageTextContains('Your search yielded no results');
  }
}
```

You'll note that this isn't really very much code. We can accomplish most of this without much typing. But we did have to do a bit of research to determine all the dependencies of our test.

Let's run it:

```
BROWSERTEST_OUTPUT_DIRECTORY=/tmp SIMPLETEST_BASE_URL=http://localhost ./vendor/bin/phpunit -c web/core/ --testsuite functional --group demo --filter FrontPageSearchFormDependenciesTest --printer="\Drupal\Tests\Listeners\HtmlOutputPrinter"

PHPUnit 9.6.15 by Sebastian Bergmann and contributors.

Testing 
.                                                                   1 / 1 (100%)

Time: 00:02.777, Memory: 40.00 MB

OK (1 test, 10 assertions)

HTML output was generated
http://localhost/sites/simpletest/browser_output/Drupal_Tests_my_testing_module_Functional_FrontPageSearchFormDependenciesTest-2-58570090.html
http://localhost/sites/simpletest/browser_output/Drupal_Tests_my_testing_module_Functional_FrontPageSearchFormDependenciesTest-3-58570090.html
http://localhost/sites/simpletest/browser_output/Drupal_Tests_my_testing_module_Functional_FrontPageSearchFormDependenciesTest-4-58570090.html
http://localhost/sites/simpletest/browser_output/Drupal_Tests_my_testing_module_Functional_FrontPageSearchFormDependenciesTest-5-58570090.html
http://localhost/sites/simpletest/browser_output/Drupal_Tests_my_testing_module_Functional_FrontPageSearchFormDependenciesTest-6-58570090.html
http://localhost/sites/simpletest/browser_output/Drupal_Tests_my_testing_module_Functional_FrontPageSearchFormDependenciesTest-7-58570090.html
```

And that final output? What does it look like?

Image

![Image of the passing test output](../assets/images/implement-functional-search-deps-passing-output.png)

You'll see that this does not look like Olivero. You'll also see the block name 'ranlfacg'. That's the random name of the block that we added.

## Time to run tests

Let's look at another factor: Time.

Using the Standard profile, the test takes around 8.9 seconds. Creating only the parts of the fixture that we need, the test takes about 2.7 seconds, as you can see above.

The time difference is not all that great, but it is an improvement. Over hundreds of tests, the extra time will add up, so this is a clear win.

## Recap

In this tutorial, we used quite a few `BrowserTestBase` features to define our dependencies.

- We specified modules to install.
- We used `setUp()` to give us a consistent fixture for all test methods.
- We placed a block and figured out which plugin ID to use.
- We defined a user permission for this content type.
- We saved time during test runs.

## Further your understanding

- What other methods are available to `BrowserTestBase` that might help us define other types of dependencies?

## Additional resources

- [Run Drupal Tests with PHPUnit](https://drupalize.me/tutorial/run-drupal-tests-phpunit) (Drupalize.Me)
- [Set up a Functional Test](https://drupalize.me/tutorial/set-functional-test) (Drupalize.Me)
- [Convert Tests from Simpletest to PHPUnit](https://drupalize.me/tutorial/convert-tests-simpletest-phpunit) (Drupalize.Me)
- [`BrowserTestBase` API documentation](https://api.drupal.org/api/drupal/core%21tests%21Drupal%21Tests%21BrowserTestBase.php/class/BrowserTestBase) (api.drupal.org)
- [PHPUnit Browser test tutorial](https://www.drupal.org/docs/8/phpunit/phpunit-browser-test-tutorial) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Implement a Functional Test](/tutorial/implement-functional-test?p=3264)

Next
[Implement a Unit Test in Drupal](/tutorial/implement-unit-test-drupal?p=3264)

Clear History

Ask Drupalize.Me AI

close