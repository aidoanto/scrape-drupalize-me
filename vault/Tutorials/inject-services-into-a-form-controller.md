---
title: "Inject Services into a Form Controller"
url: "https://drupalize.me/tutorial/inject-services-form-controller?p=2734"
guide: "[[develop-forms-drupal]]"
---

# Inject Services into a Form Controller

## Content

Eventually you'll want to do something with the information your form collects beyond just printing it to the screen. It's generally considered a best practice to keep business logic out of your form controller so that it can be reused. In order to accomplish that you'll generally define your business logic in a service, and then call out to that service from your form controller. Or, you can make use of one of the existing services provided by Drupal core to save data.

In this tutorial we'll:

- Use dependency injection to inject a service into a form controller
- Make use of a service injected into a form controller from within the `buildForm()` and `submitForm()` methods

By the end of this tutorial you'll understand how to inject one or more services into your form controller and then make use of them.

**Note:** As of Drupal 10.2, regular controllers can use `AutowireTrait` for automatic dependency injection. However, form controllers do not yet support autowiring and still require the manual `create()` method approach demonstrated in this tutorial. Learn more about autowiring in [Create a Route and Controller](https://drupalize.me/tutorial/create-route-and-controller).

## Goal

Update the code for the form we defined in [Define a New Form Controller and Route](https://drupalize.me/tutorial/define-new-form-controller-and-route), and [Process Submitted Form Data via Form Controller](https://drupalize.me/tutorial/process-submitted-form-data-form-controller) so that the temporary storage service is injected into our form controller using dependency injection.

## Prerequisites

- [Define a New Form Controller and Route](https://drupalize.me/tutorial/define-new-form-controller-and-route)
- [Process Submitted Form Data via Form Controller](https://drupalize.me/tutorial/process-submitted-form-data-form-controller)
- [Services](https://drupalize.me/topic/services)
- [Dependency Injection](https://drupalize.me/topic/dependency-injection)

## Inject the temporary storage service

Building on the form controller we previously created, follow these steps to inject the temporary storage service and replace the existing calls to the global `\Drupal` object with calls to the injected service.

Form controllers require the manual `create()` method pattern for dependency injection. Unlike regular controllers (which can use `AutowireTrait` as of Drupal 10.2), form controllers do not yet support autowiring.

### Override the `create()` method on your controller

Since our form controller extends `FormBase`, which already implements `\Drupal\Core\DependencyInjection\ContainerInjectionInterface` we can start by overriding the `create()` method so that our controller takes responsibility for defining it.

Copy and paste the definition of the `create()` method below (or from `FormBase`) into the definition of `\Drupal\form_api_example\Form\SimpleForm`.

```
/**
 * {@inheritdoc}
 */
public static function create(ContainerInterface $container) {
  return new static();
}
```

### Inject the desired service

Update the line `return new static();` so that when a new instance of the controller is created by `static()` it passes an instance of the temporary storage service to the class constructor.

```
/**
 * {@inheritdoc}
 */
public static function create(ContainerInterface $container) {
  return new static(
    $container->get('tempstore.private')
  );
}
```

Make sure you also add the use statement for `use Symfony\Component\DependencyInjection\ContainerInterface;`.

Learn about existing services provided by core in [Discover and Use Existing Services](https://drupalize.me/tutorial/discover-and-use-existing-services). See how to define your own new service in [Create a Service](https://drupalize.me/videos/create-service).

### Add a new property to store the injected service

Add a private property to `\Drupal\form_api_example\Form\SimpleForm` named `$tempStoreFactory` which we'll use to store the injected service.

```
/**
 * Private temporary storage factory.
 *
 * @var \Drupal\Core\TempStore\PrivateTempStoreFactory
 */
private $tempStoreFactory;
```

### Override the `__constructor()` method on your controller

Update the `\Drupal\form_api_example\Form\SimpleForm` classes constructor so that it receives the temporary storage factory service as an argument, and then saves it to the new `$tempStoreFactory` property.

```
/**
 * {@inheritdoc}
 */
public function __construct(PrivateTempStoreFactory $tempStoreFactory) {
  $this->tempStoreFactory = $tempStoreFactory;
}
```

Make sure you add the use statement for `use Drupal\Core\TempStore\PrivateTempStoreFactory;`.

### Use the injected service in your form controller

Finally, replace instances of `\Drupal::service('tempstore.private')` with `$this->tempStoreFactory`.

In `buildForm()`:

```
// Retrieve previously saved data from the tempstore if it exists.
$tempstore = $this->tempStoreFactory->get('form_api_example');
$title = $tempstore->get('title');
```

And in `submitForm()`:

```
$tempstore = $this->tempStoreFactory->get('form_api_example');
$tempstore->set('title', $title);
```

This video demonstrates how to use dependency injection to inject a service into a standard controller. The process is almost exactly the same when using a form controller.

Sprout Video

## Recap

In this tutorial, we walked through the steps required to use dependency injection with our form controller class, overriding the `create()` and `__construct()` methods, injecting the temporary storage service, and then updating our existing code to use the injected service rather than the global `\Drupal` object. This ensures that our code follows best practices. While regular controllers can use autowiring (Drupal 10.2+), form controllers still require this manual approach.

## Further your understanding

- What other services provided by Drupal core might be useful in the context of handling form data?
- Look at `\Drupal\user\Form\UserLoginForm` for an example of a form in core that uses multiple services. Which services is it using and what is it using them for?

## Additional resources

- [Discover and Use Existing Services](https://drupalize.me/tutorial/discover-and-use-existing-services) (Drupalize.me)
- [Create a Service](https://drupalize.me/videos/create-service) (Drupalize.me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add Input Elements to a Form](/tutorial/add-input-elements-form?p=2734)

Next
[Provide Default Values for Form Elements](/tutorial/provide-default-values-form-elements?p=2734)

Clear History

Ask Drupalize.Me AI

close