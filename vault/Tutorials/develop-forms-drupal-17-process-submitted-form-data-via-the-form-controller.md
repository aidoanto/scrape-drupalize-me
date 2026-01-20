---
title: "Process Submitted Form Data via the Form Controller"
url: "https://drupalize.me/tutorial/process-submitted-form-data-form-controller?p=3256"
guide: "[[develop-forms-drupal]]"
order: 17
---

# Process Submitted Form Data via the Form Controller

## Content

When you create a custom form for Drupal and your module defines the form controller, the best way to handle processing of submitted data is via the `submitForm()` method of your controller. This method is called *automatically* by the Form API during the process of handling a user-submitted form. It can be used to save incoming data to the database, trigger a workflow based on user input, and instruct the Form API where to send the user after form processing has completed.

In this tutorial we'll:

- Demonstrate how to add a `submitForm()` method to a form controller class
- Access the value(s) of form input elements via the `$form_state` object
- Set a redirect after performing processing in a form submission handler

By the end of this tutorial you should know how to access the values of a submitted form, and how to write custom processing code inside of the `submitForm()` method of a form controller.

## Goal

Add processing logic to a form that displays the content input by the user on the screen and saves it as temporary data.

## Prerequisites

- [Form API Life Cycle](https://drupalize.me/tutorial/form-api-life-cycle)
- [Handle Submitted Form Data](https://drupalize.me/tutorial/handle-submitted-form-data)
- [Define a New Form Controller and Route](https://drupalize.me/tutorial/define-new-form-controller-and-route) - We'll be expanding on the form started in this tutorial.

## Retrieving the values from form fields

The `$form_state` object passed into your `submitForm()` method has a couple of handy methods for working with user-submitted data.

- `$form_state->getValue($key, $default = '')`: Returns the submitted and sanitized form value for a specific key.
- `$form_state->getValues()`: Returns the submitted and sanitized form values for all elements.
- `$form_state->cleanValues()`: Same as `getValues()` but with values for Form API internal elements removed.

## Processing data with a `submitForm()` method

Every form controller is required to have a `submitForm()` method. If your code defines the controller, this is a great place to implement your custom logic for handling processing of user input. See `\Drupal\Core\Form\FormInterface`.

### Add a `submitForm()` method to your controller

If it doesn't already exist, start by defining a new method.

```
public function submitForm(array &$form, FormStateInterface $form_state) {
	// This is where your custom processing logic goes.
}
```

In this case `$form` will contain a copy of the form array that defined the form initially presented to the user. This can be useful if your submission-handling logic needs additional information about the form that's being processed.

### Retrieve the field values

Using the `$form_state` object, retrieve the values from the form that you need to operate on. In this case we'll retrieve the value of the *title* element.

```
$title = $form_state->getValue('title');
```

At this point it's safe to assume that values have all been validated and are ready for use. The validation processing of your form has already been called. If any errors were raised, Drupal would prevent execution from reaching this point.

### Process collected data

Finally, use whatever PHP logic is required to perform your application-specific processing of the collected data. In this example we'll use the `$messenger` service to display the value on the screen. When extending `FormBase` the `$messenger` service is already available. If you're not extending form base, or the service isn't available, you can use inject it into your class using [dependency injection](https://drupalize.me/tutorial/discover-and-use-existing-services).

We'll also save the collected data into the user's session so that we can retrieve it again later and make use of it.

```
public function submitForm(array &$form, FormStateInterface $form_state) {
  // Get the value of the title element.
  $title = $form_state->getValue('title');
  // Log the value to be displayed by the messaging system.
  $this->messenger->addStatus($this->t('You specified a title of %title.', ['%title' => $title]));

  // Save the value of the title field as temporary/session data.
  $tempstore = \Drupal::service('tempstore.private')->get('form_api_example');
  $tempstore->set('title', $title);
}
```

**Note:** This example uses the *tempstore.private* service as a way to store per-user data for demonstration purposes. [Learn more about using the temporary storage service](http://karimboudjema.com/en/drupal/20190315/saving-temporary-values-form-private-tempstore-drupal-8).

### Optional redirect

After completing processing of the data collected by your form you'll need to determine what you want the user to do next. This is usually accomplished in one of two ways: redirect them to another page, or display the same form again and ask them to enter another record.

If you want to redisplay the form, you don't have to do anything, as this is the default behavior. After the execution of all submission handlers is complete the form will be rebuilt and displayed again, just like the first time the user viewed it. You might want to add a "success" message to confirm to the user that their previous action was completed. Something like this would do the trick:

```
$this->messenger->addStatus($this->t('%title has been saved. Please add another record.', ['%title' => $title]));
```

Alternatively, you could redirect the user to another page. A common example is to redirect the user to a page that displays the results of the action that was just performed. For example, displaying the node page after the node has been saved. Another example is redirecting to a static "thanks" page. This is done using the `$form_state->setRedirect($route_name, array $route_parameters, array $options)` or `$form_state->setRedirectUrl(Url $url)` methods. Using these methods, instead of actually performing the redirect directly, allows the Form API to continue with any additional processing it might need to do. For example, if another module added an additional `#submit` callback it would be called after your `submitForm()` method, so if you forced the redirect here it would cause that code to never get executed.

Here are few redirect examples:

#### Redirect to an internal Drupal route

```
$form_state->setRedirect('mymodule.thanks');
```

#### Redirect to an entity by using its route

Note: This will only work if `$this->entity` is set in your class.

```
/** @var \Drupal\node\Entity\Node $node */
$node = $this->entity;
$form_state->setRedirect(
  'entity.node.canonical',
  ['node' => $node->id()]
);
```

#### Redirect to the node's path where the form is embedded

If the form is placed on a node, you can use `routeMatch()->getParameter`, which returns the fully-loaded node object. You can then get the node's ID and construct a path to redirect to the node's page where the form is embedded. See [routeMatch::getParameter](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Routing%21RouteMatch.php/function/RouteMatch%3A%3AgetParameter/) (api.drupal.org)

```
$node = \Drupal::routeMatch()->getParameter('node');
$form_state->setRedirect(
  'entity.node.canonical',
  ['node' => $node->id()]
);
```

#### Redirect to a URI, or other web address

```
$url = Drupal\core\Url::fromUserInput('/thanks');
$form_state->setRedirectUrl($url);
```

[Learn more about constructing routes and URLs](https://drupalize.me/tutorial/generate-urls-and-output-links).

## Recap

In this tutorial we looked at how you can access the values of a submitted form for processing within a `submitForm()` method of your form controller. Our example extracted the value of the title field from our form, displayed it to the user using the `$messenger` service, and then saved it for later use using the temporary storage service.

## Further your understanding

- Update your form to redirect to a page at the path */thanks*.
- Give an example of when you might use `$form_state->getValues()` instead of `$form_state->getValue()`
- Explore the *form\_api\_example/src/Form/BuildDemo.php* example in the [Examples for Developers project](https://www.drupal.org/project/examples).

## Additional resources

- [Documentation for `FormStateInterface`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Form%21FormStateInterface.php/interface/FormStateInterface/) (api.drupal.org)
- [Examples for Developers project](https://www.drupal.org/project/examples) (Drupal.org)
- [What Are Hooks?](https://drupalize.me/tutorial/what-are-hooks) (Drupalize.Me)
- [Saving temporarily values of a form with Private Tempstore in Drupal 8](http://karimboudjema.com/en/drupal/20190315/saving-temporary-values-form-private-tempstore-drupal-8) (karimboudjema.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Process Submitted Form Data with a Callback](/tutorial/process-submitted-form-data-callback?p=3256)

Clear History

Ask Drupalize.Me AI

close