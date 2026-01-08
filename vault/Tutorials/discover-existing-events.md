---
title: "Discover Existing Events"
url: "https://drupalize.me/tutorial/discover-existing-events?p=2725"
guide: "[[alter-drupal-modules]]"
---

# Discover Existing Events

## Content

Some events are dispatched by Drupal core, some by underlying Symfony components, and some by contributed modules. The list of events that you can subscribe to depends on the modules you've got installed. This can make it tricky to get a complete list.

In this tutorial, we'll look at different ways you can get a complete list of the available events for your Drupal application, and where to find documentation for those events.

## Prerequisites

- [What Are Events?](https://drupalize.me/tutorial/what-are-events)

## Goal

List all events that you could subscribe to within the context of a specific Drupal application.

## Methods for finding events

How to get a list of events:

- [Search for "@Event" documentation tags](#event-tags)
- [Use WebProfiler module](#webprofiler)
- [Use Devel module](#devel)

## Search for `@Event` documentation tags

[By convention](https://www.drupal.org/docs/develop/coding-standards/api-documentation-and-comment-standards#event), the `@Event` tag is used to indicate that the thing being documented is the name of an event triggered by the event dispatcher. This documentation should also include information about why/when the event is triggered and what type of event object subscribers will receive.

As such, one way to get a list of all events is to search through the code base for all instances of the `@Event` docblock tag.

You can see a list of everything tagged with `@Event` at the [bottom of this page](https://api.drupal.org/api/drupal/core%21core.api.php/group/events/). Though note that api.drupal.org examines Drupal core, and not any custom or contributed modules.

In an IDE such as PHPStorm, you can navigate to Edit > Find > Find in files. Enter the text `@Event` and check the File mask: `*.php` option.

## Use WebProfiler module

WebProfiler, formerly a submodule of [Devel module](https://www.drupal.org/project/devel) is now a separate project, but dependent on Devel. WebProfiler may be configured to list event subscribers, including a list of ones that were triggered during a page request. This can be useful if you're trying to figure out which events were dispatched on a certain page request.

### Download and install Devel and WebProfiler

You will need to download and install both Devel and WebProfiler using Composer.

1. Download [Devel](https://www.drupal.org/project/devel) with Composer: `composer require --dev drupal/devel`.
2. Download [WebProfiler](https://www.drupal.org/project/webprofiler) with Composer: `composer require --dev drupal/webprofiler`.
3. Install both modules using the administrative UI (Extend) or Drush (`drush en devel webprofiler`).

### Enable event tracking

The WebProfiler module does not display information about events by default. You can enable it by navigating to Manage > Configuration > Devel settings > WebProfiler (*admin/config/development/devel/webprofiler*). Select the checkbox to activate the "Events" toolbar item and save your changes.

### View profile data

Visit any page on your site. When the WebProfiler toolbar shows up at the bottom of the page, click on the events toolbar icon to get a list of all event subscribers, and information about which were called during that request.

WebProfiler toolbar:

Image

![Showing location of events icon in toolbar](/sites/default/files/styles/max_800w/public/tutorials/images/webprofilter-events-toolbar-icon.png?itok=1x91aOAm)

Example event listing:

Image

![Showing list of events captured by webprofiler](/sites/default/files/styles/max_800w/public/tutorials/images/webprofiler-event-listing.png?itok=XJdnzxmk)

## Use Devel to view/edit an event class

[Devel](https://www.drupal.org/project/devel) by itself provides 1 event-related Drush command (`devel:event`, aliases: `fne`, `fn-event`, `event`). This command guides you through a multistep questionnaire asking you to choose the type of event and an implementation to view or optionally, edit.

```
devel:event
```

Here's an example of its output:

```
drush devel:event

 Enter the event you wish to explore.:
  [0] kernel.controller
  [1] kernel.exception
  [2] kernel.request
  [3] kernel.response
  [4] kernel.terminate
  [5] kernel.view
 > 0

 Enter the number of the implementation you wish to view.:
  [0] Drupal\path_alias\EventSubscriber\PathAliasSubscriber::onKernelController
  [1] Drupal\Core\EventSubscriber\EarlyRenderingControllerWrapperSubscriber::onController
  [2] Drupal\webprofiler\DataCollector\RequestDataCollector::onKernelController
 > 0
```

Whatever you choose on the final step will open up the corresponding file in your configured terminal text editor.

## Recap

The list of events available to subscribe to will vary depending on the modules you've installed. You can get a list of events for your specific Drupal application by either searching for all `@Events` tags in PHP comments, using WebProfiler to see which events were listening or called during a page request, or using Devel's Drush command `drush devel:event` to inspect the code for a given event.

## Further your understanding

- Can you get a list of all the events for your Drupal application?
- Can you find the events that were called during a page request?

## Additional resources

- [List of Drupal core events](https://api.drupal.org/api/drupal/core%21core.api.php/group/events/)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[What Are Events?](/tutorial/what-are-events?p=2725)

Next
[Subscribe to an Event](/tutorial/subscribe-event?p=2725)

Clear History

Ask Drupalize.Me AI

close