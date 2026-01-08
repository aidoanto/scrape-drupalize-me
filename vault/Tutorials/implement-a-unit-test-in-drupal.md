---
title: "Implement a Unit Test in Drupal"
url: "https://drupalize.me/tutorial/implement-unit-test-drupal?p=3264"
guide: "[[test-drupal-sites-automated-tests]]"
---

# Implement a Unit Test in Drupal

## Content

Let's write somewhat strict unit tests in a Drupal module. By the end of this tutorial, you will be able to:

- Understand what makes a unit test different from other types of tests.
- Determine the specifications of a unit test.
- Use mocking to isolate units under test, and to force code flow to achieve high coverage.

We'll start out with a brief introduction to unit tests. Then we'll look at a contrived example of a Drupal controller class for illustration purposes. Next, we'll test two units of this controller class, each requiring different mock styles.

## Goal

Design, write, and run a unit test within a Drupal module.

## Prerequisites

- [Install Drupal Locally with DDEV](https://drupalize.me/tutorial/install-drupal-locally-ddev)
- [Install Drupal Development Requirements with Composer](https://drupalize.me/tutorial/install-drupal-development-requirements-composer)
- Command line access.
- We'll be working on code from the *testing\_example* module from [Examples for Developers](https://www.drupal.org/project/examples).
- [Introduction to Testing in Drupal](https://drupalize.me/tutorial/introduction-testing-drupal)
- [Software Testing Overview](https://drupalize.me/tutorial/software-testing-overview)

## Watch: Implement a Unit Test in Drupal

Sprout Video

## Contents

1. [What is a unit test?](#what_is_a_unit_test)
2. [Introducing the `ContrivedController` class](#intro_contrived_controller_class)
3. [Our goal: isolation](#our_goal_isolation)
4. [Writing a unit test](#writing_unit_test)
5. [Set up a skeleton test](#set_up_skeleton_test)
6. [Design your test](#design_your_test)
7. [Start with "easy"](#start_with_easy)
8. [Determine what to mock](#determine_what_to_mock)

- [What is a mock?](#what_is_a_mock)

1. [Mock a `ContrivedController`](#mock_contrived_controller)
2. [Use reflection to expose a protected method](#use_reflection_to_expose_protected_method)
3. [Use a data provider method](#use_a_data_provider_method)

- [What's a data provider?](#what_is_a_data_provider)

1. [Test `handCount()` with a mocked translation service](#test_handcount_with_mocked_translation_service)
2. [Bonus: Analyze `getStringTranslationStub()`](#bonus_analyze_getstringtranslationstub)
3. [Mock `add()` to isolate `handCount()`](#mock_add_to_isolate_handcount)

- [The Principle of Isolation](#principle_of_isolation)
- [The Principle of Coverage](#principle_of_coverage)

1. [Re-run the test one more time](#rerun_test)

## What is a unit test?

A *unit test* is a test that limits its scope to only testing a small part of a program in a highly deterministic way.

A *unit* is the smallest piece of executable code or a clearly-defined small piece of the code. The smallest piece of executable code in PHP is a function or method. Generally in PHP, a unit test will test a function or method. The goal of a unit test is to isolate the behavior of the unit so that very little other code needs to be executed for the test to run.

A looser definition of unit test could be: a test that extensively mocks a lot of dependencies in order to isolate a well-defined part of the code from the effects of other code. This version of the definition doesn't strictly confine the unit to being a function or method.

Either definition is reasonable, as long as we uphold the principles of isolation and coverage.

What are isolation and coverage? We'll learn more about coverage later, but let's talk about isolation using an example class we want to test.

## Introducing the `ContrivedController` class

Let's contrive an example: a Drupal controller class.

A Drupal controller class does a lot of things. It will typically have a service injection pattern, which means it requires external services to operate normally. It will also have a build method which will create a render array for Drupal to render into HTML.

But a controller class might also have utility methods that don't actually need the services and don't depend on the render array.

In this case, we can write tests which isolate the utility methods from the service discovery part and also from the build method.

Let's make up a controller class like that, right now, because if we had one, it would be useful for teaching unit tests, wouldn't it?

Here it is, in a basic form:

```
class ContrivedController implements ContainerInjectionInterface {

  use StringTranslationTrait;

  /**
   * {@inheritdoc}
   */
  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('string_translation')
    );
  }

  /**
   * Construct a new controller.
   */
  public function __construct(TranslationInterface $translation) {
    $this->setStringTranslation($translation);
  }

  /**
   * A controller method which displays a sum in terms of hands.
   */
  public function displayAddedNumbers($first, $second) {
    return [
      '#markup' => '<p>' . $this->handCount($first, $second) . '</p>',
    ];
  }

  /**
   * Generate a message based on how many hands are needed to count the sum.
   */
  protected function handCount($first, $second) {
    $sum = abs($this->add((int)$first, (int)$second));
    if ($sum <= 5) {
      $message = $this->t('I can count these on one hand.');
    }
    else if ($sum <= 10) {
      $message = $this->t('I need two hands to count these.');
    }
    else {
      $message = $this->t("That's just too many numbers to count.");
    }
    return $message;
  }

  /**
   * Add two numbers.
   */
  protected function add($first, $second) {
    return $first + $second;
  }
```

This [class](https://git.drupalcode.org/project/examples/-/blob/9.x-1.x/testing_example/src/Controller/ContrivedController.php) is also present in the *testing\_example* module in the [Examples for Developers](https://www.drupal.org/project/examples) project.

Let's suppose we want to concentrate our efforts on the `add()` and `handCount()` methods. We want to make sure those methods work properly now and continue to work properly into the future--even if we modify all the other parts of the controller class.

These two methods receive arguments, add them together, and create a message telling how many hands are required to count to the number. `handCount()` assumes five fingers per hand.

We could test this in a number of different ways. We could write a functional test and then pass in various numbers on the controller path. This would cause Drupal to pass those values along to the build method, and then to our utility methods. Based on the text that was rendered into HTML by the whole system, we could deduce that the `add()` and `handCount()` methods were functioning properly.

That's not a terrible test. Any test is better than no test. But there are a few things wrong with this approach. The biggest problem is that it assumes the whole Drupal system is available and operating properly. If there is a change to the way controllers work in Drupal, our test might fail for reasons that aren't immediately clear. Worse, our test might pass even though `add()` or `handCount()` is buggy. We can't definitively say.

A functional test also requires that in order to run the test, the testing framework has to set up and tear down a whole Drupal installation for each request. This will extend the time our test takes. It might not matter that much for one test, but for a hundred, it will add up.

This brings us to the principle of isolation.

## Our goal: isolation

Our goal is to test `add()` and `handCount()`. We aren't testing anything in Drupal itself, or even anything else in the controller class.

If we set up a *functional* test, we're depending on code that we aren't testing, and, in fact, don't want to test.

So ideally, we'd be able to isolate the methods we want to test from the rest of Drupal and also from the other methods in `ContrivedController`.

Choosing to isolate the method from the rest of the code is what makes the test a unit test. We are isolating a unit (first `add()`, then `handCount()`) from the rest of code.

## Write a unit test

As you can see, this controller is very contrived. This is a silly controller class that has one-line methods which we could maintain just by reading them instead of testing them.

However, writing a unit test of this controller class' helper methods will illustrate some concepts about unit tests in general.

Real code in the wild might have far more complex methods which will be more of a challenge to isolate. The extent to which complex code is a challenge to isolate is roughly the same as the extent to which that code is hard to maintain. So the more coverage we have in isolation, the more we can rely on the test to tell us when some part of it is behaving in a way we don't expect.

Let's start down the path of writing a unit test...

### Set up a skeleton test

The first thing to do is to add a test to your module.

Follow the steps in [Set up a Functional Test](https://drupalize.me/tutorial/set-functional-test) and substitute the `Unit` namespace. Or you may get the code from *testing\_example* and modify as needed.

Set up the failing test, make sure the test runner can discover it and fails it, then change it to a passing test, re-run, and make sure it passes. This might seem like too much effort, but it's a good habit to get into. This way we always know that our test is passing or failing for the reasons we think it is.

### Design your test

There are many different ways to design your own isolated unit test. For instance, if you are writing the code, you can write the test at the same time to prove to yourself that it's working as you write it.

You might also need to write tests of specific behaviors. For instance, if you need to fix a bug in some code, you might write a unit test which proves that the bug is fixed, and then test your changes to the code by running the test. You can work the other way, too: Write a test that passes when the bug is present and make it fail. Then change the test so it passes when the bug is absent.

All kinds of options are available when the time and effort required to run the test is very small.

But let's step back from these advanced ideas and start learning how to write a simple unit test.

Our test will isolate and verify three behaviors of the controller class:

1. We will verify that the `add()` method does, in fact, add two numbers that we input.
2. We will verify that the `handCount()` method delivers the correct message, based on the result of `add()`.
3. We will verify that the `handCount()` method delivers the correct message, based on input numbers.

We will use *test doubles* to isolate these behaviors from the rest of the dependencies of the controller class. We will also use test doubles to isolate `handCount()` from `add()`.

### Start with "easy"

Let's start by naively testing the `add()` method. Who knows? Maybe it will be enough. (Hint: It won't. But we need to start somewhere.)

In an ideal world, we'd be able to just make a new `ContrivedController` class and call its `add()` method, and then assert against the result. That would be easy, and we could just pass in numbers and verify that the result is what we expect.

Easy, right?

Here's a test class to do that:

```
class ContrivedControllerTest extends UnitTestCase {

  public function testAdd() {
    // Make a new controller.
    $controller = new ContrivedController();
    // Call add() on the controller.
    $this->assertEquals(4, $controller->add(2,2));
  }

}
```

Sometimes this is all you need to do. As mentioned, it's not enough in this example, but unit test don't have to be complicated.

Now if you were to try to run this test, you would see the following error:

```
Testing
E

Time: 15.77 seconds, Memory: 64.00MB

There was 1 error:

1) Drupal\Tests\testing_example\Unit\Controller\ContrivedControllerTest::testAdd
TypeError: Argument 1 passed to Drupal\testing_example\Controller\ContrivedController::__construct() must implement interface Drupal\Core\StringTranslation\TranslationInterface, none given, called in /drupal/modules/examples/testing_example/tests/src/Unit/Controller/ContrivedControllerTest.php on line 11
```

What does this error mean? Let's find out...

### Determine what to mock

The error from the last step is saying that we need to have a `TranslationInterface` object to pass into the `__construct()` method when we make a new `ContrivedController`.

This is good and reasonable for the container injection pattern, but can be a challenge for us. We only want a `ContrivedController` object, and we don't want to build out a translation service just so we can add two numbers.

So this leaves us with two options:

1. Mock a `TranslationInterface` object to pass in the constructor of the `ContrivedController` object.
2. Mock a `ContrivedController` object so that we can tell it to ignore `__construct()`.

These options might seem strange. You might not really be sure what a mock is at this point, so the idea of mocking the class we're testing is a bit of a head-scratcher.

So let's back up a little bit and figure out what a mock is, so that we can decide from between our two options.

#### What is a mock?

Before we answer that question, we have to add this disclaimer: We're using "mock" here to refer generally to "test doubles". (See [Introduction to Testing in Drupal](https://drupalize.me/tutorial/introduction-testing-drupal) for further explanation.)

A mock is a special class or object which allows us to control the outcome for some dependencies. The point of a mock is to short-circuit the behavior of dependencies, allowing us to isolate the unit under test from those dependencies.

For instance, if our controller needs a service, we might mock the service to get the result we want, so that our test only ever sees the behavior of the code that consumes that service, and not the service itself.

In our case we have two methods we're going to test: `add()` and `handCount()`. `handCount()` needs the translation service. If you look at it, you see that it uses `$this->t()`, which is the translation method.

```
  protected function handCount($first, $second) {
    $sum = abs($this->add((int)$first, (int)$second));
    if ($sum <= 5) {
      $message = $this->t('I can count these on one hand.');
    }
    [ ..etc.. ]
```

So in order to test `handCount()`, we might mock the translation service to work a certain limited way because we aren't testing the translation service. We're testing `handCount()` and not `t()`. `handCount()` is our unit.

But in the case of `add()`, we don't need a translation service at all. Here's the whole of `add()`:

```
  protected function add($first, $second) {
    return $first + $second;
  }
```

Yes, it's a contrived example, but you'll see that it doesn't use any service. It has no dependencies at all. It doesn't call out to any other methods, and it only requires that we input values as arguments.

In this case, we deduce that since `TranslationInterface` is not a dependency of `add()`, and since we want to test `add()`, we should do whatever we can to make sure there are no `TranslationInterface` objects to deal with in this test.

This leads us to choose the second option from above: Mock a `ContrivedController` object so that we can tell it to ignore `__construct()`.

### Mock a `ContrivedController`

In order to test `add()` we need a `ContrivedController` object. When we create a `ContrivedController` object, we want to bypass the constructor. In order to bypass the constructor, we have to mock `ContrivedController`. And in order to mock `ContrivedController` we need to learn how to create a mock.

Let's do that.

Here's the beginning:

```
  public function testAdd() {
    // Mock a controller.
    $controller = $this->getMockBuilder(ContrivedController::class)
      ->disableOriginalConstructor()
      ->getMock();
    // Call add() on the controller.
    $this->assertEquals(4, $controller->add(2,2));
  }
```

Let's walk through this.

#### Get the mock builder

```
$controller = $this->getMockBuilder(ContrivedController::class)
```

The first step is to get the mock builder. The mock builder uses a fluent interface to generate a mock. That means the `getMockBuilder()` method returns an object that we can then call other methods on to specify our mock.

You'll also note the `ContrivedController::class` pattern. For PHP versions 5.5 and above, you can use this to get a string with the name of the class. This is preferable to using just a string with the class name, because if you move the class to a new namespace, the test will be unable to find it and the fix will be to change the `use` statement, rather than hunting down all the string literals referring to it.

#### Bypass `__construct()`

```
->disableOriginalConstructor()
```

The reason we're doing all this is to avoid calling `__construct()`. That way we don't have to produce a `TranslationInterface` object that we don't need for the test. So we call `disableOriginalConstructor()` on the mock builder.

#### Get the mock object

```
->getMock();
```

Finally, we get the actual mock object from the builder. This object can be used the same way any other object is used, and if you call `get_class()` on it, the result will be `Drupal\testing_example\Controller\ContrivedController`.

#### Run the test again

OK, we're moving forward. If we run the test as shown above, we get another error:

```
There was 1 error:

1) Drupal\Tests\testing_example\Unit\Controller\ContrivedControllerTest::testAdd
Error: Call to protected method Drupal\testing_example\Controller\ContrivedController::add() from context 'Drupal\Tests\testing_example\Unit\Controller\ContrivedControllerTest'
```

So now instead of having a problem with the constructor, we have a problem with `add()`. Let's solve that in the next step.

### Use reflection to expose a protected method

In the previous step we developed a test method:

```
  public function testAdd() {
    // Mock a controller.
    $controller = $this->getMockBuilder(ContrivedController::class)
      ->disableOriginalConstructor()
      ->getMock();
    // Call add() on the controller.
    $this->assertEquals(4, $controller->add(2,2));
  }
```

This led to our discovery that `add()` is a protected method and we must somehow gain access to it.

Thankfully, there's some PHP magic we can use to accomplish this called [Reflection](http://php.net/manual/en/class.reflectionmethod.php).

Let's apply reflection to `add()` in our test method.

```
  public function testAdd() {
    // Mock a controller.
    $controller = $this->getMockBuilder(ContrivedController::class)
      ->disableOriginalConstructor()
      ->getMock();
    // Use reflection to make add() public.
    $ref_add = new \ReflectionMethod($controller, 'add');
    $ref_add->setAccessible(TRUE);
    // Call add() on the controller.
    $this->assertEquals(4, $ref_add->invokeArgs($controller, [2,2]));
  }
```

Let's walk through the reflection part.

#### Create a `\ReflectionMethod`

```
    $ref_add = new \ReflectionMethod($controller, 'add');
```

Here we create a `\ReflectionMethod` object for our controller object and its `add()` method.

When we create a `\ReflectionMethod` object, we tell it which class or object that contains the method, and the name of the method. So we tell it the controller mock object, `$controller` and a string for the name of the method we want to reflect: `'add'`.

#### Make the protected method accessible to our test

```
    $ref_add->setAccessible(TRUE);
```

Remember that the `add()` method is `protected`? Well, let's tell our reflection object to treat it as if it were `public`. The way we do that is with `setAccessible(TRUE)`.

#### Invoke the reflection method

```
    // Call add() on the controller.
    $this->assertEquals(4, $ref_add->invokeArgs($controller, [2,2]));
```

The change here is this part: `$ref_add->invokeArgs()`. This invokes the reflection method we just set up, with the arguments passed in as an array. This is the same as saying `add(2,2)`, but we have to use the `ReflectionMethod` in order to bypass `add()`'s `protected` visibility.

#### Re-run the test

And now that we've un-protected the `add()` method, we see this result:

```
./vendor/bin/phpunit -c core/ --testsuite unit --filter ContrivedControllerTest
PHPUnit 4.8.36 by Sebastian Bergmann and contributors.

Testing
.

Time: 15.33 seconds, Memory: 64.00MB

OK (1 test, 1 assertion)
```

Success!

We have used mocking and reflection to isolate the `add()` method from its class' dependencies, and determined that it behaves the way we expect it to behave.

But we're not done yet. There's still something missing from this test. It needs to be able to test more than one set of numbers.

### Use a data provider method

In the last step, we successfully determined that our `add()` method knows that two plus two equals four.

Surely, however, there must be some value it can't add properly?

Remember, this controller class is contrived. This is an extremely trivial example. Adding two numbers is probably not a behavior that needs extensive testing. However, if it were more complex, you'd want to be sure and find all the edge cases and make sure they behaved as expected.

Let's add a data provider so we can feed in many different data sets to `add()`.

#### What's a data provider?

If you make a test method, such as `testAdd()` and you annotate it with `@dataProvider provideTestAdd` then you can return an array of arrays from a method called `provideTestAdd()`. All the values of that array will be fed in as arguments to `testAdd()`. You can then create data sets to test many permutations using the same test code.

Let's look at our old test, converted to use a data provider:

```
  /**
   * Data provider for testAdd().
   */
  public function provideTestAdd() {
    return [
      [4, 2, 2],
    ];
  }

  /**
   * @dataProvider provideTestAdd
   */
  public function testAdd($expected, $first, $second) {
    $controller = $this->getMockBuilder(ContrivedController::class)
      ->disableOriginalConstructor()
      ->getMock();
    $ref_add = new \ReflectionMethod($controller, 'add');
    $ref_add->setAccessible(TRUE);
    $this->assertEquals($expected, $ref_add->invokeArgs($controller, [$first, $second]));
  }
```

Let's look at the things we changed.

```
  public function provideTestAdd() {
    return [
      [4, 2, 2],
    ];
  }
```

This is our data provider method. We could name it anything. But instead of a random string, we used a naming convention and named it `provideTestAdd()`. The convention here is to start with `provide` and then the name of the method we're providing it to. In this case, `testAdd()` is the test method and `provideTestAdd()` is the name of the data provider method. This naming convention is generally accepted in Drupal core development but you could adopt your own.

This provider method returns an array of arrays. Each sub-array will be sent as arguments to the method. We can see one sub-array in the code above: `[4, 2, 2]`. This means the values 4, 2, and 2 will be sent to `testAdd()`, as if we had called `testAdd(4, 2, 2)`. If you want to send more data sets, add another array for each one.

```
  /**
   * @dataProvider provideTestAdd
   */
  public function testAdd($expected, $first, $second) {
```

Here we see the `@dataProvider` annotation in the test method docblock. This tells PHPUnit which method is the data provider.

Since we now have a data provider and we're sending three values per data set, we have to add three arguments to the method signature: `$expected`, `$first`, and `$second`.

It's a convention that the expected value is the first argument but it's not required.

```
    $this->assertEquals($expected, $ref_add->invokeArgs($controller, [$first, $second]));
```

This used to say `$this->assertEquals(4, $ref_add->invokeArgs($controller, [2, 2]))`. We've substituted the argument variables for the numbers in the assertion. In this case, adding the first and second numbers (2 and 2) should result in the expected number, 4.

Now we can return additional data sets from the data provider method, and see what happens. Here's an interesting one:

```
  public function provideTestAdd() {
    return [
      [4, 2, 2],
      [0, NULL, '']
    ];
  }
```

This data set passes the test because PHP converts NULL and the empty string to 0 during math operations.

You can hopefully see how it's relatively easy to experiment with our code if we have unit tests. We can insert our new edge cases into the data provider and then run the test, with relative ease and speed.

If we encounter a bug in the future, we're equipped to insert extra test cases into our data set to ensure that the data reproduces the bug, and then later we can ensure that the bug is fixed when the test passes.

So that's how we'll test `add()`. We still don't get any cake though, because we still need to test `handCount()`.

### Test `handCount()` with a mocked translation service

A few steps back, we determined that in order to test `add()` we needed to mock `ContrivedController` in order to avoid the constructor method.

We also saw that in order to test `handCount()` we shouldn't mock `ContrivedController` and instead we needed to mock the translation service.

So let's do that here.

First, let's rough out the test method. This won't be quite correct but it gives some code to read:

```
  /**
   * @dataProvider provideTestHandCount
   */
  public function testHandCount($expected, $first, $second) {
    // Get a mock translation service.
    $mock_translation = ???????
    // Create a new controller with our mocked translation service.
    $controller = new ContrivedController($mock_translation);

    // Set up a reflection for handCount().
    $ref_hand_count = new \ReflectionMethod($controller, 'handCount');
    // Set handCount() to be public.
    $ref_hand_count->setAccessible(TRUE);
    // Check out whether handCount() meets our expectation.
    $this->assertEquals($expected, $ref_hand_count->invokeArgs($controller, [$first, $second]));
  }
```

This is all very similar to `testAdd()`, except that we're not mocking the `ContrivedController` object, and instead of reflecting `add()` we're reflecting `handCount()`.

This might stick out as incomplete, however:

```
    // Get a mock translation service.
    $mock_translation = ???????
```

#### How will we get a mocked translation service?

It turns out our Drupal core test base class, [`UnitTestCase`](https://api.drupal.org/api/drupal/core%21tests%21Drupal%21Tests%21UnitTestCase.php/class/UnitTestCase/), has a method which provides a mocked translation service, called [`getStringTranslationStub()`](https://api.drupal.org/api/drupal/core%21tests%21Drupal%21Tests%21UnitTestCase.php/function/UnitTestCase%3A%3AgetStringTranslationStub/). It's so common to need a mocked translation service for unit tests that Drupal core has a default implementation. This implementation will meet our needs. We can say this:

```
    // Get a mock translation service.
    $mock_translation = $this->getStringTranslationStub();
```

We'll walk through `getStringTranslationStub()` in a bonus step. For now, we'll just use the mocked translation service it provides.

All the mock does is return a translation object for the same string as was passed in, without any actual translation.

Note that our method above also has a data provider. Let's figure out how that works.

```
  public function provideTestHandCount() {
    return [
      ['I can count these on one hand.', 0, 0],
      ['I can count these on one hand.', 1, 0],
      ['I can count these on one hand.', 0, 1],
      ['I need two hands to count these.', 5, 5],
      ['That\'s just too many numbers to count.', 5, 6],
      ['That\'s just too many numbers to count.', 6, 5],
    ];
  }
```

You'll see that we have many data sets, because we're testing many edge cases of `handCount()`.

So that's good. We have isolated `handCount()` from the translation service and verified that it works with some values.

Are we done yet? Not quite. Our test of `handCount()` is still coupled to `add()`. That means it's not isolated.

What happens to our test if a bug is introduced into `add()`? It could cause our test of `handCount()` to fail, even though `handCount()` is working fine.

We'll address that, but first: a brief interlude.

### Bonus: Analyze `getStringTranslationStub()`

In the last step we used [`UnitTestCase::getStringTranslationStub()`](https://api.drupal.org/api/drupal/core%21tests%21Drupal%21Tests%21UnitTestCase.php/function/UnitTestCase%3A%3AgetStringTranslationStub/) to get a mocked string translation service. Let's look at that method:

```
  /**
   * Returns a stub translation manager that just returns the passed string.
   *
   * @return \PHPUnit_Framework_MockObject_MockObject|\Drupal\Core\StringTranslation\TranslationInterface
   *   A mock translation object.
   */
  public function getStringTranslationStub() {
    $translation = $this->getMock('Drupal\Core\StringTranslation\TranslationInterface');
    $translation->expects($this->any())
      ->method('translate')
      ->willReturnCallback(function ($string, array $args = [], array $options = []) use ($translation) {
        return new TranslatableMarkup($string, $args, $options, $translation);
      });
    $translation->expects($this->any())
      ->method('translateString')
      ->willReturnCallback(function (TranslatableMarkup $wrapper) {
        return $wrapper->getUntranslatedString();
      });
    $translation->expects($this->any())
      ->method('formatPlural')
      ->willReturnCallback(function ($count, $singular, $plural, array $args = [], array $options = []) use ($translation) {
        $wrapper = new PluralTranslatableMarkup($count, $singular, $plural, $args, $options, $translation);
        return $wrapper;
      });
    return $translation;
  }
```

The first thing you'll see is that instead of using a mock builder, as we did earlier, this method just calls `getMock()`. This is another way of getting a mock object:

```
$translation = $this->getMock('Drupal\Core\StringTranslation\TranslationInterface');
```

Let's walk through the mock implementation of `translate()` to see how it works:

```
    $translation->expects($this->any())
      ->method('translate')
      ->willReturnCallback(function ($string, array $args = [], array $options = []) use ($translation) {
        return new TranslatableMarkup($string, $args, $options, $translation);
      });
```

Again, this is a fluent interface, so each subsequent line performs a method on the object returned by the previous one.

```
    $translation->expects($this->any())
```

The first thing it does is set an expectation of `any`. That means the `translate()` method can be called any number of times on our mock. In other circumstances, you could set an expectation that a mocked method will be called a specific number of times or that it won't ever be called. That would look like this:

```
$mock->expects($this->once())
$mock->expects($this->exactly(15))
$mock->expects($this->never())
// etc...
```

The next line names the method being mocked. In this case, 'translate'.

```
->method('translate')
```

The next few lines are a bit complicated. They tell the mock that when the `translate()` method is called, the anonymous function should process the input and return a `TranslatableMarkup` output. This allows us to define a simplified behavior so that the test is in control of what happens, instead of the real service code.

```
->willReturnCallback(function ($string, array $args = [], array $options = []) use ($translation) {
  return new TranslatableMarkup($string, $args, $options, $translation);
});
```

In this case, the anonymous function has the same argument signature as [`TranslationInterface::translate()`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21StringTranslation%21TranslationInterface.php/function/TranslationInterface%3A%3Atranslate/). This way it can take any set of arguments and use them appropriately.

You can also specify other types of return values for a mocked method. You can have the method return a specific value or map values to inputs or a list of values which will be returned on subsequent calls. These enable you to specify how you isolate the code under test from other methods.

The best source of information about all these things is the [PHPUnit test doubles documentation](https://phpunit.de/manual/4.8/en/test-doubles.html).

However, we still haven't isolated `handCount()` from `add()`, have we? Let's do that.

### Mock `add()` to isolate `handCount()`

One reason for writing a unit test is to make sure the code works while you're writing it. But it should also make sure the code continues to work as expected while you're maintaining it.

So if we have two methods, such as `handCount()` and `add()`, we might want to make sure `handCount()` does the right thing, even if `add()` is changed or broken in some way in the future.

For instance, if we modified `add(2, 2)` and it were to return `-46135489`, then clearly `add()` is broken. And if our test of `handCount()` depends on `add()` giving us 4, then our test of `handCount()` will break, too. This might lead us to wonder where the problem really lies, since both tests are failing.

So therefore, we might want to make a test which isolates `handCount()` from `add()`, and remove the ambiguity.

In our contrived example, the relationship between `handCount()` and `add()` is not very complex. But imagine if `add()` were `performHardMathThatIsComplexAndTakesALongTime()` instead. In that circumstance, we'd want to be sure that `handCount()` really does what it's supposed to do, without having to spend time performing the math, and more importantly, assuming that the method performed the math correctly.

So let's set up a strict isolation test of `handCount()`, so we can further explore the principles of isolation and code coverage.

#### The principle of isolation

`handCount()` has two dependencies: The translation service and `add()`.

In our previous test, we mocked up the translation service so `handCount()` would use a "fake" translation service. This demonstrates one degree of isolation: We're making it so that the behavior we're testing won't be altered by the behavior of a real translation service, which can be quite complex.

But what about `handCount()`'s other dependency: `add()`? We mocked the translation service, but we haven't mocked `add()`. This means whatever changes happen to `add()` will effect the test outcome of `handCount()`. Our existing unit test of `handCount()` can't be said to be isolated from its dependencies because we're still calling `add()`.

#### The principle of coverage

If we analyze `handCount()` further, we see that it has three main code paths, which we'll number here:

```
  protected function handCount($first, $second) {
    $sum = abs($this->add((int)$first, (int)$second));
    if ($sum <= 5) {
      // Code path #1.
      $message = $this->t('I can count these on one hand.');
    }
    else if ($sum <= 10) {
      // Code path #2.
      $message = $this->t('I need two hands to count these.');
    }
    else {
      // Code path #3.
      $message = $this->t("That's just too many numbers to count.");
    }
    return $message;
  }
```

We can design a test with the goal of causing all the different code paths to be executed at some point. This is called code coverage.

For instance, if we force `add()` to return 0, then `handCount()` should flow into code path #1. If we force `add()` to return 10, then we should see an exercise of code path #2, and if we force `add()` to return 11, then we should see code path #3.

Well, guess what: We can force `add()` to do whatever we want, much like we forced the behavior of the translation service. We can perform some analysis like we just did, and then come up with some test cases that will allow us to force all the code paths we want to cover.

In `handCount()`, each code path results in a different output. But this is not always the case. We could be writing a test for code that is much more complex, and for that we might have to do a lot more analysis to maximize code coverage.

But the data sets for complete code coverage of `handCount()` should not be that hard to analyze: Values from 0 to 5 should be counted on one hand, 5-10 should be two-handers, and 10+ should be too many numbers to count on one hand.

So here's a test that forces `add()` to return those values:

```
  /**
   * Data provider for testHandCountIsolated().
   */
  public function providerTestHandCountIsolated() {
    $data = [];

    // Add one-hand data.
    foreach(range(0,5) as $sum) {
      $data[] = ['I can count these on one hand.', $sum];
    }

    // Add two-hand data.
    foreach(range(6, 10) as $sum) {
      $data[] = ['I need two hands to count these.', $sum];
    }

    // Add too-many data.
    foreach(range(11, 15) as $sum) {
      $data[] = ['That\'s just too many numbers to count.', $sum];
    }

    return $data;
  }

  /**
   * @dataProvider providerTestHandCountIsolated
   */
  public function testHandCountIsolated($expected, $sum) {
    // Mock a ContrivedController, using a mocked translation service.
    $controller = $this->getMockBuilder(ContrivedController::class)
      ->setConstructorArgs([$this->getStringTranslationStub()])
      // Specify that we'll also mock add().
      ->setMethods(['add'])
      ->getMock();

    // Mock add() so that it returns our $sum when it's called with (0,0).
    $controller->expects($this->once())
      ->method('add')
      ->with($this->equalTo(0), $this->equalTo(0))
      ->willReturn($sum);

    // Use reflection to make handCount() public.
    $ref_hand_count = new \ReflectionMethod($controller, 'handCount');
    $ref_hand_count->setAccessible(TRUE);

    // Invoke handCount().
    $message = (string) $ref_hand_count->invokeArgs($controller, [0, 0]);

    // Assert our expectations.
    $this->assertEquals($expected, $message);
  }
```

This is all very similar to `testHandCount()` from previous steps. There is, however, a difference worth talking about:

```
    // Mock add() so that it returns our $sum when it's called with (0,0).
    $controller->expects($this->once())
      ->method('add')
      ->with($this->equalTo(0), $this->equalTo(0))
      ->willReturn($sum);
```

This sets up an expectation for the `add()` method: If `add()` is called with anything other than `add(0, 0)`, it won't return our `$sum`, and will in fact fail the test.

We do this because it doesn't matter what the input values are. We only care about the output of `add()` in order to direct the output. But we also want other developers to run into this as a problem if they try to input different values. If they change the test and don't always pass in (0, 0), then the test will complain to them.

The other big change is that we super-charged the data provider. We have algorithmically assembled an array based on our expectations. We use `foreach()` loops to add data sets to the data array.

There are plenty of edge cases we could add, such as -1, but we will leave that as an exercise for the reader.

This might lead us to an obvious question: If we have `testHandCount()`, why do we need `testHandCountIsolated()`? And if we have `testHandCountIsolated()` why would we need `testHandCount()`?

We need them both because this way we have a highly-deterministic view of how `handCount()` works. We can safely say that we have exercised all expected code paths within `handCount()`, in a way that does not depend on `add()` being correct. `handCount()` only cares how many hands it takes to count a number, not how that number was calculated.

With both of these tests, we are able to say that `handCount()` works the way we expect.

And, as stated previously, this is a highly-contrived example. If either `handCount()` or `add()` were at all complex, this sort of isolated testing from different angles would be much more important, and the need for it might be more obvious.

### Re-run the test one more time

There are no further steps. We're done. Let's re-run the test one more time.

```
./vendor/bin/phpunit -c core/ --testsuite unit --filter ContrivedControllerTest
PHPUnit 4.8.36 by Sebastian Bergmann and contributors.

Testing
........................

Time: 15.79 seconds, Memory: 64.00MB

OK (24 tests, 40 assertions)
```

Congratulations!

## Recap

In this tutorial, we have begun to scratch the surface of unit testing here and illustrated some useful patterns for making thorough tests.

## Further your understanding

- Write a unit test using the patterns and tips described in this tutorial. How did it go?

## Additional resources

- [PHPUnit in Drupal](https://www.drupal.org/docs/automated-testing/phpunit-in-drupal) (Drupal.org)
- Lots of good hair-splitting about what to call your test double: [A better PHP testing experience Part II: Pick your test doubles wisely](https://matthiasnoback.nl/2014/07/test-doubles/) (matthiasnoback.nl)
- [PHPUnit documentation: Test Doubles](https://phpunit.de/manual/4.8/en/test-doubles.html) (phpunit.de)
- Assertion types not covered in this tutorial: [PHPUnit documentation: Assertions](https://phpunit.de/manual/4.8/en/appendixes.assertions.html) (phpunit.de)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Implement Drupal Functional Test Dependencies](/tutorial/implement-drupal-functional-test-dependencies?p=3264)

Next
[Convert Tests from Simpletest to PHPUnit](/tutorial/convert-tests-simpletest-phpunit?p=3264)

Clear History

Ask Drupalize.Me AI

close