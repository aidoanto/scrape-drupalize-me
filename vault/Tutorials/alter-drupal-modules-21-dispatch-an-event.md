---
title: "Dispatch an Event"
url: "https://drupalize.me/tutorial/dispatch-event?p=2725"
guide: "[[alter-drupal-modules]]"
order: 21
---

# Dispatch an Event

## Content

Modules or subsystems can dispatch events in order to allow another developer to subscribe to those events and react to what's happening within the application. As a module developer you'll learn how to:

- Define and document new events
- Define new event objects
- Use the event dispatcher service to alert event subscribers when specific conditions are met in your own code.

By the end of this tutorial, you should be able to explain the use case for dispatching events, and be able to trigger one more events from within your own code.

## Prerequisites

- [What Are Events?](https://drupalize.me/tutorial/what-are-events)

## Goal

Learn how to dispatch one or more events by defining a new event and using the event dispatcher service to trigger the event at the appropriate time.

This requires us to:

- [Define a new static class with constants for unique event names](#static-class)
- [Define an event class that extends `\Symfony\Component\EventDispatcher\Event`](#event-class)
- [Use the 'event\_dispatcher' service in your code to dispatch an event](#dispatcher)

## Prerequisites

- [What Are Events?](https://drupalize.me/tutorial/what-are-events)

Sprout Video

## When to dispatch an event

Dispatching (or triggering) an event allows your code to communicate about the things that it is currently doing with other components in the system, giving those other components a chance to optionally react. This allows your logic to be extensible without modifying your code.

You should dispatch an event any time your code performs an operation that others might want to react to. Examples include creating, updating, loading or deleting data managed by your module, or turning a particular feature of your module on or off.

## Example use case

We're going to develop a system that allows users to fill out an incident report in which they choose an incident type, and provide a detailed description of the incident. Example incidents we will create involve a cat stuck in a tree, the Joker, and a missing princess.

When the form is submitted we'll collate the data from the incident response form into an event object, and then dispatch a new "incident reported" event. This will allow anyone to subscribe to be notified when an incident is reported. They may then read the report and determine to take action, or simply ignore the event.

In this tutorial we'll use code from the [Examples for Developers project's event\_example module](https://git.drupalcode.org/project/examples/-/blob/4.0.x/modules/events_example/src/EventSubscriber/EventsExampleSubscriber.php?ref_type=heads) *events\_example* module (making some adjustments to account for deprecated code).

## Define an event name

Every event needs to have a unique name. This is how [event subscribers](https://drupalize.me/tutorial/subscribe-event) can identify the event(s) that they are interested in. Best practice is to create a new static class with constants for each unique event name. This allows the individual events to be documented and easier for others to discover. It also ensures that code using the constants won't have to be updated in the incident that an event's unique name changes.

### Create a new class

There is no requirement about where these classes live. Convention is to put them in the `Drupal\{my_module}\Event` namespace.

Define each event as a constant on the `IncidentEvents` class. The value of the constant is a string, and the string should be unique. Convention is to prefix event names with the name of the module or subsystem that is providing the event.

The docblock for each event constant should define the circumstances under which the event is dispatched. Other developers will use this information in order to determine if this the correct event to subscribe to for their use case. The docblock should contain an `@Event` tag so that documentation parsers and other tools can more easily discover existing events.

Example: *events\_example/src/Event/IncidentEvents.php*:

```
<?php

namespace Drupal\events_example\Event;

/**
 * Defines events for the events_example module.
 *
 * It is best practice to define the unique names for events as constants on a
 * static class. This provides a place for documentation of the events, as well
 * as allowing the event dispatcher to use the constants instead of hard coding
 * a string.
 *
 * In this example we're defining one new event:
 * 'events_example.new_incident_report'. This event will be dispatched by the
 * form controller \Drupal\events_example\Form\EventsExampleForm whenever a new
 * incident is reported. If your application dispatches more than one event
 * you can use a single class to document multiple events -- just add a new
 * constant for each. Group related events together with a single class;
 * define another class for unrelated events.
 *
 * The docblock for each event name should contain a description of when, and
 * under what conditions, the event is triggered. A module developer should be
 * able to read this description in order to determine whether this is
 * the event that they want to subscribe to.
 *
 * Additionally, the docblock for each event should contain an "@Event" tag.
 * This is used to ensure documentation parsing tools can gather and list all
 * events.
 *
 * Example: https://api.drupal.org/api/drupal/core%21core.api.php/group/events/
 *
 * In core \Drupal\Core\Config\ConfigCrudEvent is a good example of defining and
 * documenting new events.
 *
 * @ingroup events_example
 */
final class IncidentEvents {

  /**
   * Name of the event fired when a new incident is reported.
   *
   * This event allows modules to perform an action whenever a new incident is
   * reported via the incident report form. The event listener method receives a
   * \Drupal\events_example\Event\IncidentReportEvent instance.
   *
   * @Event
   *
   * @see \Drupal\events_example\Event\IncidentReportEvent
   *
   * @var string
   */
  const NEW_REPORT = 'events_example.new_incident_report';

}
```

Both the event dispatcher, and event subscribers, can refer to the unique *events\_example.new\_incident\_report* event via the static variable `IncidentEvents::NEW_REPORT`.

## Define an event class

When an event is dispatched, all subscribers receive an Event object as an argument. The event object contains information about the event being triggered, as well as any additional contextual information for the event. In our example, the custom event object has access to the incident report.

Example: *events\_example/src/Event/IncidentReportEvent.php*

```
<?php

namespace Drupal\events_example\Event;

// Note: For Drupal 8.x and 9.0.x use Symfony\Component\EventDispatcher\Event.
// The class Drupal\Component\EventDispatcher\Event was introduced in Drupal
// 9.1.x as a backwards compatibility layer to allow more easily upgrading to
// Symfony 5 for Drupal 10.
// @link https://www.drupal.org/node/3159012
#use Symfony\Component\EventDispatcher\Event;
use Drupal\Component\EventDispatcher\Event;

/**
 * Wraps an incident report event for event subscribers.
 *
 * Whenever there is additional contextual data that you want to provide to the
 * event subscribers when dispatching an event you should create a new class
 * that extends \Symfony\Component\EventDispatcher\Event.
 *
 * See \Drupal\Core\Config\ConfigCrudEvent for an example of this in core.
 *
 * @ingroup events_example
 */
class IncidentReportEvent extends Event {

  /**
   * Incident type.
   *
   * @var string
   */
  protected $type;

  /**
   * Detailed incident report.
   *
   * @var string
   */
  protected $report;

  /**
   * Constructs an incident report event object.
   *
   * @param string $type
   *   The incident report type.
   * @param string $report
   *   A detailed description of the incident provided by the reporter.
   */
  public function __construct($type, $report) {
    $this->type = $type;
    $this->report = $report;
  }

  /**
   * Get the incident type.
   *
   * @return string
   */
  public function getType() {
    return $this->type;
  }

  /**
   * Get the detailed incident report.
   *
   * @return string
   */
  public function getReport() {
    return $this->report;
  }

}
```

Subscribers now have access to the incident type, and report via the `getType()` and `getReport()` methods of the event class.

## Dispatch an event using the event dispatcher

Finally, in your code, you need to dispatch the event at the appropriate time. This notifies all subscribers that the event has just taken place. In our case, this is whenever someone submits the incident response form. This is done using the `event_dispatcher` service, and calling the `dispatch()` method. It takes two arguments: the name of the event to dispatch, and the `Event` instance to pass to each subscriber.

Generally this is done inside a controller within your custom code. In the MVC paradigm, controllers are responsible for orchestrating the flow of an application. That includes dispatching events.

Example from `\Drupal\events_example\Form\EventsExampleForm` in *events\_example/src/Form/EventsExampleForm.php*. Pay particular attention to the `submitForm()` method:

```
<?php

namespace Drupal\events_example\Form;

use Drupal\Core\Form\FormBase;
use Drupal\Core\Form\FormStateInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;
use Symfony\Component\EventDispatcher\EventDispatcherInterface;
use Drupal\events_example\Event\IncidentEvents;
use Drupal\events_example\Event\IncidentReportEvent;

/**
 * Implements the SimpleForm form controller.
 *
 * The submitForm() method of this class demonstrates using the event dispatcher
 * service to dispatch an event.
 *
 * @see \Drupal\events_example\Event\IncidentEvents
 * @see \Drupal\events_example\Event\IncidentReportEvent
 * @see \Symfony\Component\EventDispatcher\EventDispatcherInterface
 * @see \Drupal\Component\EventDispatcher\ContainerAwareEventDispatcher
 *
 * @ingroup events_example
 */
class EventsExampleForm extends FormBase {

  /**
   * The event dispatcher service.
   *
   * @var \Symfony\Component\EventDispatcher\EventDispatcherInterface
   */
  protected $event_dispatcher;

  /**
   * Constructs a new UserLoginForm.
   *
   * @param \Symfony\Component\EventDispatcher\EventDispatcherInterface $event_dispatcher
   *   The event dispatcher service.
   */
  public function __construct(EventDispatcherInterface $event_dispatcher) {
    // The event dispatcher service is an implementation of
    // \Symfony\Component\EventDispatcher\EventDispatcherInterface. In Drupal
    // this is generally an instance of the
    // \Drupal\Component\EventDispatcher\ContainerAwareEventDispatcher service.
    // This dispatcher improves performance when dispatching events by compiling
    // a list of subscribers into the service container so that they do not need
    // to be looked up every time.
    $this->event_dispatcher = $event_dispatcher;
  }

  /**
   * {@inheritdoc}
   */
  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('event_dispatcher')
    );
  }

  /**
   * {@inheritdoc}
   */
  public function buildForm(array $form, FormStateInterface $form_state) {
    $form['incident_type'] = [
      '#type' => 'radios',
      '#required' => TRUE,
      '#title' => t('What type of incident do you want to report?'),
      '#options' => [
        'stolen_princess' => $this->t('Missing princess'),
        'cat' => $this->t('Cat stuck in tree'),
        'joker' => $this->t('Something involving the Joker'),
      ],
    ];

    $form['incident'] = [
      '#type' => 'textarea',
      '#required' => FALSE,
      '#title' => t('Incident report'),
      '#description' => t('Describe the incident in detail. This information will be passed along to all crime fighters.'),
      '#cols' => 60,
      '#rows' => 5,
    ];

    $form['actions'] = [
      '#type' => 'actions',
    ];

    $form['actions']['submit'] = [
      '#type' => 'submit',
      '#value' => $this->t('Submit'),
    ];

    return $form;
  }

  /**
   * {@inheritdoc}
   */
  public function getFormId() {
    return 'events_example_form';
  }

  /**
   * {@inheritdoc}
   */
  public function submitForm(array &$form, FormStateInterface $form_state) {
    $type = $form_state->getValue('incident_type');
    $report = $form_state->getValue('incident');

    // When dispatching or triggering an event, start by constructing a new
    // event object. Then use the event dispatcher service to notify any event
    // subscribers.
    $event = new IncidentReportEvent($type, $report);

    // Dispatch an event by specifying which event, and providing an event
    // object that will be passed along to any subscribers.

    // As of Drupal 9.1.x, the argument order has switched.
    // @see https://www.drupal.org/node/3159012
    $this->event_dispatcher->dispatch($event, IncidentEvents::NEW_REPORT);
  }

}
```

Notice that the special `IncidentReportEvent` object is created and passed to the `dispatch()` method. Now, any subscriber to the `IncidentEvents.NEW_REPORT` event will receive the `IncidentReportEvent` and data collected from the form.

## Optimized for speed

Instantiating a copy of every event subscriber, and then calling the `getSubscribedEvents()` method on each one in order to create a list of listeners is a big performance drain, especially if you've instantiated an object which declares that it's listening to an event that's never dispatched. It would be better if event subscribers were lazy-loaded, as needed. Drupal accomplishes this by requiring that event subscribers are registered with the services container, where it can then cache the list of subscribers, and the events that they are interested in, and call them only as needed.

When reading the data in your *MYMODULE.services.yml* file, one of the things Drupal looks for is service tags. These are indicators to the service container compiler that this particular service should be registered, or used, in a special way. When adding an event subscriber we tag our service(s) with the aptly named, `event_subscriber` tag.

Example:

```
tags: 
  - {name: event_subscriber}
```

When this tag is encountered, the compiler instantiates a copy of the tagged service class, calls the `getSubscribedEvents()` method for each, and retains a list of all their combined responses.

This list is then compiled into the service container. If you're curious you can see it in the `getEventDispatcherService()` method of the container. When an event is dispatched via `\Drupal\Component\EventDispatcher\ContainerAwareEventDispatcher` this cached list of event subscribers is used and speeds up performance considerably.

Thus, if you're adding new event subscribers you'll need to [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) before Drupal detects them.

## Recap

In this tutorial we explained the use case for dispatching events and showed you how to trigger one more events from within your own code.

## Further your understanding

- Can you update the events\_example module and add a new event, `IncidentEvents.REPORT_VALIDATION` that is dispatched when the form is being validated?
- `\Drupal\Core\Config\ConfigEvents`, and `\Drupal\Core\Config\Config` provide a good example of dispatching events in core

## Additional resources

- [Learn how to subscribe to an event](https://drupalize.me/tutorial/subscribe-event) (Drupalize.me)
- [Events API documentation](https://api.drupal.org/api/drupal/core%21core.api.php/group/events/) (Drupal.org)
- [Symfony event dispatcher documentation](http://symfony.com/doc/current/components/event_dispatcher.html) (Symfony.com)
- [Change record: Symfony Event class deprecated, EventDispatcher::dispatch() argument order changed](https://www.drupal.org/node/3159012) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Subscribe to an Event](/tutorial/subscribe-event?p=2725)

Clear History

Ask Drupalize.Me AI

close