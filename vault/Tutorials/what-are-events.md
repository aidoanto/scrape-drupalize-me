---
title: "What Are Events?"
url: "https://drupalize.me/tutorial/what-are-events?p=2626"
guide: "[[symfony-drupal-developers]]"
---

# What Are Events?

## Content

Drupal uses events to allow modules and various subsystems to communicate with one another in an object-oriented manner. Understanding how the Event API works is critical knowledge for all module developers. In this tutorial we'll:

- Explain what events are
- Discuss the use case for subscribing to events
- Give an example use case for dispatching events

By the end of this tutorial you should be able to explain what events are, understand when to use them in your own code, and know where to learn more about how to do so.

## Goal

Explain what events are and why we use them. Provide direction for people who want to learn more about working with events in their code.

## Prerequisites

- None.

## Events in Drupal

Events in Drupal allow various system components to interact and communicate with one another while remaining independent, or decoupled. The event system is built on the [Symfony event dispatcher component](http://symfony.com/doc/current/components/event_dispatcher.html), and is an implementation of the [Mediator design pattern](https://en.wikipedia.org/wiki/Mediator_pattern).

As an application grows in complexity, and components are added, it becomes necessary for those components to communicate with one another. Rather than having objects refer to one another explicitly, which can turn into a maintenance nightmare, communication is instead facilitated by a mediator object. This reduces the dependencies between communicating objects, thereby lowering the coupling, and creating a code base that's easier to maintain.

During the process of responding to a request, Drupal and the underlying Symfony components will trigger (or dispatch) various events, notifying any subscribers that now is the time to do their thing. Some events are triggered on every request (e.g. "the request has started"), and others are triggered when specific code paths are executed (e.g. "a configuration object was updated").

When writing custom code you can dispatch events to notify other components in the system about actions taken by your code. For example, the [Recurly module](https://www.drupal.org/project/recurly) works with the [Recurly web service](https://recurly.com) to facilitate subscription billing. The Recurly web service handles the recurring logic, and charging of subscribers. Whenever a charge is made Recurly sends a ping notification to the Drupal Recurly module. The module receives the incoming notice, opens its contents, and uses that to make changes within Drupal. It would be impossible for the Recurly module to hard-code every possible action that someone might want to take when a user cancels their subscription. Instead, it takes the incoming notice, wraps it in an Event object, and then dispatches a new "recurly ping received" event, to which any number of different modules can subscribe and do things like cancel the Drupal user's account, send an email, display a message, or anything else you as a PHP developer could conceive of.

Event subscribers respond to specific events being triggered and perform custom logic. Which could be anything from updating related settings when a configuration change occurs in another module, to redirecting a request after inspecting the request parameters.

If you've used JavaScript you've probably worked with events before. In JavaScript, you can do things like subscribe to the `onClick` event of a link. When a user clicks on the link the browser dispatches an `onClick` event, and your custom code gets executed.

Image

![Comic strip showing a report (event) being dispatched to a subscriber (Batman) via a dispatcher.](../assets/images/eventdispatchercomic.png)

Still not quite sure? Sometimes abstract patterns are easier to understand if you can ground them in something you know. Check out this post on our blog which uses a superhero themed analogy to unravel the event/subscriber workflow: [Responding to Events in Drupal](https://drupalize.me/blog/responding-events-drupal).

## Working with events

As a module developer you'll do two different things with events:

- Subscribe to existing events to react with custom logic whenever those events occur. [Learn how to subscribe to an event](https://drupalize.me/tutorial/subscribe-event)
- Dispatch a new event when critical actions happen in your code. Giving other components the option to react, while remaining decoupled and thus easier to maintain. [Learn how to dispatch an event](https://drupalize.me/tutorial/dispatch-event)

## Recap

Events allow various components to interact and communicate with one another while remaining decoupled. You can subscribe to an event in order to be notified when the event occurs and execute custom code. Modules can dispatch new events so that other modules can extend and enhance critical functionality while remaining independent.

## Further your understanding

- Can you describe a use case where you would dispatch an event from your custom module?
- [Get a list of all events for your Drupal site](https://drupalize.me/tutorial/discover-existing-events)
- Drupal's event system is based on the [Symfony event dispatcher component](http://symfony.com/doc/current/components/event_dispatcher.html). If you understand how events work in Symfony you should be able to pick it up in Drupal without too much trouble.
- [Learn about plugins](https://drupalize.me/tutorial/what-are-plugins), another common method of extending Drupal

## Additional resources

- [Responding to Events in Drupal](https://drupalize.me/blog/responding-events-drupal) (Drupalize.Me)
- [Drupal Events API documentation](https://api.drupal.org/api/drupal/core%21core.api.php/group/events/) (api.drupal.org)
- [Events in Symfony](http://symfony.com/doc/current/event_dispatcher.html) (symfony.com)

Was this helpful?

Yes

No

Any additional feedback?

Clear History

Ask Drupalize.Me AI

close