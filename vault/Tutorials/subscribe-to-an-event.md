---
title: "Subscribe to an Event"
url: "https://drupalize.me/tutorial/subscribe-event?p=2725"
guide: "[[alter-drupal-modules]]"
---

# Subscribe to an Event

## Content

Modules can declare their interest in being notified when a specific event, or events, are triggered by implementing an event subscriber. This can be used to react to events in order to add your own logic, or to alter Drupal's existing functionality.

In this tutorial we'll cover how to subscribe to an event from your own module. After completing this tutorial you should be able to subscribe to any event and ensure that your custom code is executed when the specific event is triggered.

## Prerequisites

- [What Are Events?](https://drupalize.me/tutorial/what-are-events)

## Goal

Subscribe to an event and execute custom code anytime the specific event is triggered.

## Quick start

If you're already familiar with subscribing to events and just want to dive into writing some code [Drush](https://drupalize.me/tutorial/install-drush-using-composer) has a handy [generator command](https://drupalize.me/tutorial/develop-drupal-modules-faster-drush-code-generators) to help you get started.

```
drush generate service:event-subscriber
```

## Subscribing to events

Modules can subscribe to one or more events by:

- [Defining a service tagged with 'event\_subscriber'](#define-a-service)
- [Defining a class for your subscriber service that implements `\Symfony\Component\EventDispatcher\EventSubscriberInterface` and subscribes to one or more events](#define-class)

## Define an event subscriber service

The first thing you need to do is define a new service tagged with the "event\_subscriber" tag. This is done in the *MYMODULE.services.yml* file of your module.

Example from *events\_example/events\_example.services.yml*

```
# Subscribing to an event requires you to create a new service tagged with the
# 'event_subscriber' tag. This tells the service container, and by proxy the
# event dispatcher service, that the class registered here can be queried to get
# a list of events that it would like to be notified about.
services:
  # Give your service a unique name, convention is to prefix service names with
  # the name of the module that implements them.
  events_example_subscriber:
    # Point to the class that will contain your implementation of
    # \Symfony\Component\EventDispatcher\EventSubscriberInterface
    class: Drupal\events_example\EventSubscriber\EventsExampleSubscriber
    tags:
      - {name: event_subscriber}
```

This is done so that during compilation of the service container your event subscriber class can be located and used to retrieve a list of the events that you would like to subscribe to. As a performance optimization this list is then compiled into the container for quicker retrieval in the future.

Read [the documentation about defining and tagging services](https://api.drupal.org/api/drupal/core%21core.api.php/group/container/) for more details.

## Define an event subscriber class

The next step is to define the new class we listed in our service definition above. This class needs to implement the `\Symfony\Component\EventDispatcher\EventSubscriberInterface` interface.

This class has 2 responsibilities:

- Define a `getSubscribedEvents()` method that returns a list of events we're interested in subscribing to and the name of the method to call when that event is triggered
- For each subscribed event define a public method that receives an Event object as it's argument and contains the code we want to execute when the specified event is triggered

In order to proceed you'll need to know what event(s) you want to subscribe to. Learn how to [discover existing events](https://drupalize.me/tutorial/discover-existing-events).

Example from [events\_example/src/EventSubscriber/EventsExampleSubscriber.php](https://git.drupalcode.org/project/examples/-/blob/4.0.x/modules/events_example/src/EventSubscriber/EventsExampleSubscriber.php?ref_type=heads):

```
<?php

namespace Drupal\events_example\EventSubscriber;

use Drupal\events_example\Event\IncidentEvents;
use Drupal\events_example\Event\IncidentReportEvent;
use Drupal\Core\Messenger\MessengerTrait;
use Drupal\Core\StringTranslation\StringTranslationTrait;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

/**
 * Subscribe to IncidentEvents::NEW_REPORT events and react to new reports.
 *
 * In this example we subscribe to all IncidentEvents::NEW_REPORT events and
 * point to two different methods to execute when the event is triggered. In
 * each method we have some custom logic that determines if we want to react to
 * the event by examining the event object, and the displaying a message to the
 * user indicating whether that method reacted to the event.
 *
 * By convention, classes subscribing to an event live in the
 * Drupal/{module_name}/EventSubscriber namespace.
 *
 * @ingroup events_example
 */
class EventsExampleSubscriber implements EventSubscriberInterface {

  use StringTranslationTrait;
  use MessengerTrait;

  /**
   * {@inheritdoc}
   */
  public static function getSubscribedEvents() {
    // Return an array of events that you want to subscribe to mapped to the
    // method on this class that you would like called whenever the event is
    // triggered. A single class can subscribe to any number of events. For
    // organization purposes it's a good idea to create a new class for each
    // unique task/concept rather than just creating a catch-all class for all
    // event subscriptions.
    //
    // See EventSubscriberInterface::getSubscribedEvents() for an explanation
    // of the array's format.
    //
    // The array key is the name of the event your want to subscribe to. Best
    // practice is to use the constant that represents the event as defined by
    // the code responsible for dispatching the event. This way, if, for
    // example, the string name of an event changes your code will continue to
    // work. You can get a list of event constants for all events triggered by
    // core here:
    // https://api.drupal.org/api/drupal/core%21core.api.php/group/events/.
    //
    // Since any module can define and trigger new events there may be
    // additional events available in your application. Look for classes with
    // the special @Event docblock indicator to discover other events.
    //
    // For each event key define an array of arrays composed of the method names
    // to call and optional priorities. The method name here refers to a method
    // on this class to call whenever the event is triggered.
    $events[IncidentEvents::NEW_REPORT][] = ['notifyMario'];

    // Subscribers can optionally set a priority. If more than one subscriber is
    // listening to an event when it is triggered they will be executed in order
    // of priority. If no priority is set the default is 0.
    $events[IncidentEvents::NEW_REPORT][] = ['notifyBatman', -100];

    // We'll set an event listener with a very low priority to catch incident
    // types not yet defined. In practice, this will be the 'cat' incident.
    $events[IncidentEvents::NEW_REPORT][] = ['notifyDefault', -255];

    return $events;
  }

  /**
   * If this incident is about a missing princess notify Mario.
   *
   * Per our configuration above, this method is called whenever the
   * IncidentEvents::NEW_REPORT event is dispatched. This method is where you
   * place any custom logic that you want to perform when the specific event is
   * triggered.
   *
   * These responder methods receive an event object as their argument. The
   * event object is usually, but not always, specific to the event being
   * triggered and contains data about application state and configuration
   * relative to what was happening when the event was triggered.
   *
   * For example, when responding to an event triggered by saving a
   * configuration change you'll get an event object that contains the relevant
   * configuration object.
   *
   * @param \Drupal\events_example\Event\IncidentReportEvent $event
   *   The event object containing the incident report.
   */
  public function notifyMario(IncidentReportEvent $event) {
    // You can use the event object to access information about the event passed
    // along by the event dispatcher.
    if ($event->getType() == 'stolen_princess') {
      $this->messenger()->addStatus($this->t('Mario has been alerted. Thank you. This message was set by an event subscriber. See @method()', ['@method' => __METHOD__]));
      // Optionally use the event object to stop propagation.
      // If there are other subscribers that have not been called yet this will
      // cause them to be skipped.
      $event->stopPropagation();
    }
  }

  /**
   * Let Batman know about any events involving the Joker.
   *
   * @param \Drupal\events_example\Event\IncidentReportEvent $event
   *   The event object containing the incident report.
   */
  public function notifyBatman(IncidentReportEvent $event) {
    if ($event->getType() == 'joker') {
      $this->messenger()->addStatus($this->t('Batman has been alerted. Thank you. This message was set by an event subscriber. See @method()', ['@method' => __METHOD__]));
      $event->stopPropagation();
    }
  }

  /**
   * Handle incidents not handled by the other handlers.
   *
   * @param \Drupal\events_example\Event\IncidentReportEvent $event
   *   The event object containing the incident report.
   */
  public function notifyDefault(IncidentReportEvent $event) {
    $this->messenger()->addStatus($this->t('Thank you for reporting this incident. This message was set by an event subscriber. See @method()', ['@method' => __METHOD__]));
    $event->stopPropagation();
  }

}
```

And that's it. Our custom code is now triggered anytime code elsewhere in the system dispatches the `IncidentEvents::NEW_REPORT` event. This same process will work for subscribing to any event triggered by Drupal or the Symfony components in use.

## Recap

In this tutorial we:

- Created a new event subscriber class whose `getSubscribedEvents()` method returned a list of events we wanted to react to
- Implemented custom methods on an event subscriber class that get called whenever the event we subscribed to is triggered
- Defined our event subscriber class as a new service tagged with the "event\_subscriber" tag

## Further your understanding

- What 2 things is the event subscriber class responsible for doing?
- Can you write the code required to subscribe to the `Kernel::REQUEST` event? And on each request check to see if the site is in maintenance mode and redirect to another domain like offline.example.com if it is?
- Can you get a list of all the events that you could potentially subscribe to in your application?

## Additional resources

- [Learn how to dispatch an event](https://drupalize.me/tutorial/dispatch-event) (Drupalize.Me)
- [Events API documentation](https://api.drupal.org/api/drupal/core%21core.api.php/group/events/) (api.drupal.org)
- Drupal uses Symfony's event dispatcher component under the hood. Learn more about [how the Symfony event dispatcher works](https://symfony.com/doc/current/components/event_dispatcher.html) to gain a better understanding of the system (symfony.com)
- [Learn about plugins](https://drupalize.me/tutorial/what-are-plugins), another common method of extending Drupal (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Discover Existing Events](/tutorial/discover-existing-events?p=2725)

Next
[Dispatch an Event](/tutorial/dispatch-event?p=2725)

Clear History

Ask Drupalize.Me AI

close