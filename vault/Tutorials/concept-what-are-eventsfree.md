---
title: "Concept: What Are Events?free"
url: "https://drupalize.me/tutorial/concept-what-are-events?p=3240"
guide: "[[drupal-module-developer-guide]]"
---

# Concept: What Are Events?free

## Content

The event system in Drupal enables different components to interact and communicate. Through events, a component can announce important actions to interested modules, providing a flexible way to extend functionality. This system is central to Drupal's event-driven architecture.

In this tutorial, we'll:

- Define events and their operation.
- Provide examples of dispatching and subscribing to events.
- Contrast events with hooks.

By the end of this tutorial you should be able to understand the event system's fundamentals in Drupal, and how modules can use it for extending and modifying functionality.

## Goal

Understand how Drupal employs the event subscriber pattern to enhance core functionality.

## Prerequisites

- [Concept: What Are Hooks?](https://drupalize.me/tutorial/concept-what-are-hooks)
- [Concept: Dependency Injection](https://drupalize.me/tutorial/concept-dependency-injection)

## What are events in Drupal?

Events allow parts of a Drupal application to communicate and respond to each other's actions. The dispatch of an event signals subscribing components, which can execute logic in response. This modular design pattern is widely used in software development to facilitate interaction among code components.

Drupal's event system utilizes [Symfony's EventDispatcher component](https://symfony.com/doc/current/components/event_dispatcher.html). By familiarizing yourself with Symfony's component, you can recognize the same patterns in Drupal's event system.

### Event subscribing

Event subscribing is how components indicate interest in event notifications. Event subscribers react to event triggers with custom logic. For example:

- Updating settings when a certain configuration change occurs
- Redirecting a request after parameter inspection

Subscribing to an event involves:

- Defining a service with an `event_subscriber` tag.
- Creating a class for the service that implements `EventSubscriberInterface`

Here's an example service definition of an event subscriber:

```
services:
  events_example_subscriber:
    class: Drupal\events_example\EventSubscriber\EventsExampleSubscriber
    tags:
      - {name: event_subscriber}
```

Here's an example corresponding subscriber service class:

```
class EventsExampleSubscriber implements EventSubscriberInterface {
  public static function getSubscribedEvents() {
    // List the event(s) you want to subscribe too, and the method to call when
    // the event is dispatched.
    return [CustomEvent::EVENT_NAME => 'onCustomEvent'];
  }

  public function onCustomEvent(CustomEvent $event) {
    // React to the event.
  }
}
```

**Tip:** Use `drush generate:service:event-subscriber` to scaffold code for an event subscriber.

- The events that Drupal core dispatches are listed in this [Events documentation](https://api.drupal.org/api/drupal/core%21core.api.php/group/events/).
- To learn how to discover available events that your module can subscribe to, see [Discover Existing Events](https://drupalize.me/tutorial/discover-existing-events).
- Details on event subscription are in [Subscribe to an Event](https://drupalize.me/tutorial/subscribe-event).

### Event dispatching

Event dispatching alerts subscribers about an action. It provides contextual data about the event to subscribers. Dispatching an event entails:

1. **Defining an event**: Establish a unique identifier and an event data-representing class for the event.
2. **Dispatching an event**: Use Drupal's event dispatcher service to announce the event.

Event dispatching example:

```
$event_dispatcher = \Drupal::service('event_dispatcher');
$event = new CustomEvent($data);
$event_dispatcher->dispatch(CustomEvent::EVENT_NAME, $event);
```

You can dispatch events in your own code whenever your logic takes significant actions that you want to allow others to respond to. For example if your module receives web hooks from a third party, you can dispatch an event that allows others to also take action.

For dispatching details, see [Dispatch an Event](https://drupalize.me/tutorial/dispatch-event).

## Events vs. hooks

In [Concept: What Are Hooks?](https://drupalize.me/tutorial/concept-what-are-hooks), we introduced hooks as a means for modules to respond to other components' actions. While hooks have historically been Drupal's primary extension mechanism, events offer an object-oriented solution. Some Drupal functionalities are efficiently managed with hooks. But events are mandatory for certain actions due to Drupal's reliance on underlying Symfony components.

As a module developer you'll encounter hooks more frequently, but you'll need to know how to work with both.

## Recap

Events are integral to Drupal's architecture, enabling component interaction and action response. They allow modules to flexibly enhance Drupal's behavior in a decoupled manner. Understanding both events and hooks is essential for module developers.

## Further your understanding

- Consider how events might decouple your custom module's components.
- How could changing an event subscriber's priority ensure its precedence among multiple subscribers?
- Evaluate the benefits of events over hooks for specific module functionalities.

## Additional resources

- [What Are Events?](https://drupalize.me/tutorial/what-are-events) (Drupalize.Me)
- [Events](https://api.drupal.org/api/drupal/core%21core.api.php/group/events/) (api.drupal.org)
- [Subscribe to and dispatch events](https://www.drupal.org/docs/develop/creating-modules/subscribe-to-and-dispatch-events) (Drupal.org)
- [Symfony EventDispatcher](https://symfony.com/doc/current/components/event_dispatcher.html) (symfony.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: What Are Hooks?](/tutorial/concept-what-are-hooks?p=3240)

Next
[Discover Hooks and Their Documentation](/tutorial/discover-hooks-and-their-documentation?p=3240)

Clear History

Ask Drupalize.Me AI

close