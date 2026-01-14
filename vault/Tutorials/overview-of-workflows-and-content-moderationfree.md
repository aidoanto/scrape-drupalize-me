---
title: "Overview of Workflows and Content Moderationfree"
url: "https://drupalize.me/tutorial/overview-workflows-and-content-moderation?p=2501"
guide: "[[drupal-site-administration]]"
---

# Overview of Workflows and Content Moderationfree

## Content

The Workflows and Content Moderation modules allow an editorial team to put any type of content administered in Drupal through a customized editorial workflow and moderation process. Workflow states, such as *draft*, *ready for review*, or *approved* are defined using the Workflows module. The ability to attach moderation states to *entity bundles* -- a common example being content types -- is configurable by the Content Moderation module.

Both modules have stable releases and are perfectly safe to use in production.

In this tutorial we'll:

- Learn about the use case for Workflows and Content Moderation modules
- Define the role that each module performs
- Define some common terms you'll need to understand when working with these two modules

By the end of this tutorial you will have a good understanding of what the Workflows and Content Moderation modules are, what different functionality they provide, and the permissions made available by the modules.

## Goal

Define what features the Workflows and Content Moderation provide and how they work together.

## Prerequisites

- [1.2 Concept: Modules](https://drupalize.me/tutorial/user-guide/understanding-modules?p=3081) (Drupal User Guide)
- [2.3. Concept: Content Entities and Fields](https://drupalize.me/tutorial/user-guide/planning-data-types?p=3076) (Drupal User Guide)
- [2.6. Concept: Editorial Workflow](https://drupalize.me/tutorial/user-guide/planning-workflow?p=3076) (Drupal User Guide)
- [Chapter 4. Basic Site Configuration](https://drupalize.me/series/user-guide/config-chapter) (Drupal User Guide)
- [Chapter 7. Managing User Accounts](https://drupalize.me/series/user-guide/user-chapter) (Drupal User Guide)

## Use cases

This illustration (created by Sam Mortenson) does a great job of introducing Workflows and Content Moderation. We'll go into more detail throughout this tutorial.

Image

![Illustration showing a common editorial workflow using Workflows and Content Moderation. Explained in more detail below.](../assets/images/cmc.png)

The combination of Workflows and Content Moderation modules allow you to create and enforce editorial processes that conform to your organization's specific needs. By default, Drupal core provides for a very minimal workflow. A piece of content can be either published, or not. If you need something more complex than that, you need Workflows and Content Moderation.

As an example, on this site, the content we produce goes through a number of different steps before it's published and made available to the public.

- **Draft:** A subject-matter expert (SME) creates a draft of the tutorial, and fleshes out the majority of the content
- **Technical review:** Another SME, often someone from the community, reviews the Draft content for correctness
- **Revisions:** Revisions are made to address feedback, add screenshots, and clean up formatting
- **Copy editing:** The content is copy edited and reviewed to ensure it meets our style guide
- **Final review:** The content gets one last review, ensuring all links are accurate and working, that titles are correct, and that metadata is properly applied
- **Published:** The tutorial is published and made available to members

Different people are responsible for different parts of this process. Additionally, certain transitions from one state to another require sign-off before they can happen. For example, only a copy editor should be able to move something from copy editing to final review.

Using the Workflows and Content Moderation modules this publishing process can be facilitated within Drupal.

## Workflows

The Workflows module provides one or more workflows, defined as a set of states and transitions between them.

A **state** is a particular condition that something can be in at a specific time. For example, a content node can be in a published state or an unpublished state.

A **transition** is the process of moving from one state to another.

You can think of the Workflows module as a sort of state machine. It defines a set of states and rules about how you can transition between those states.

To see a list of currently configured workflows in the Manage administration menu navigate to *Configuration* > *Workflows* (admin/config/workflow/workflows). The configuration page for the Workflows module lists all existing workflows and provides a link to create a new workflow.

Image

![Workflows configuration page](../assets/images/workflows.png)

However, without the Content Moderation module, or another module that depends on Workflows, when installed it will display a message stating the need for a module that implements a workflow type.

## Workflow type

A *workflow type* denotes how a workflow can be used. Workflow types are defined by modules as [plugins that implement](https://drupalize.me/tutorial/implement-plugin-using-php-attributes) `\Drupal\workflows\WorkflowTypeInterface`.

For example, Content Moderation allows a workflow to be attached to an entity type or bundle. And [*Workflows Field*](https://www.drupal.org/project/workflows_field) provides a field that can be added to an entity type for choosing a state within a workflow. The workflow type can also denote things like default states, the initial state, extra configuration for a state, transition, or workflow.

Image

![Workflow type setting](../assets/images/workflow_type.png)

## Content Moderation

The Content Moderation module allows a workflow to be attached to an entity type or bundle. The only requirement is that the entity type supports revisions. If the entity type supports bundles, a different workflow can be assigned to each bundle. Otherwise, only one workflow per entity type is possible.

Remember: Workflows provides the state machine but doesn't prescribe how it should be used to manage the state of an entity. Content Moderation supplies:

- A `WorkflowType` plugin that integrates with the Revision API
- Storage for individual states on content entities
- Configuration that defines which bundles should have content moderation applied
- Permissions for who can use various transitions when applied to content

The most common use case is to use workflows with nodes (entity type), and attach them to different content types (bundles) like *blog\_post*, or *page*.

To understand how content moderation works you need to be familiar with the concepts of published, and default revisions, for content entities.

Content entities, without any additional modules enabled, support a published/unpublished state. This is used by the core Node module to determine viewing permissions for content. For example, all site visitors might be able to view published content, while only administrators can view unpublished content.

Content entities support revision tracking. As content is revised, Drupal stores the older revisions so that they can be compared or reverted at a later point. The default revision is the one that is currently in the published state -- essentially, the one that a user will see by default when they navigate to the page.

The workflow type within Content Moderation takes control over these two core features. When you define a new state you can choose if that state maps to a published or unpublished status. As the content moves from one state to another, its published status will be updated automatically to match that of the current state.

Likewise, a state can be set as a *default revision*, which will make the entity the default when it’s moved to this state. However, when a state is set as *published* it would automatically make the entity the default revision too.

## Permissions

The only permission defined by Workflows module is *Administer workflows*, which provides full permission to create and edit workflows.

Content Moderation uses a number of permissions:

- *View any unpublished content* allows content moderators to see unpublished content and potentially move it to the next state
- *View the latest version* allows users to view revisions that are newer than the current default revision. For example, an unpublished edit to an existing content item. This permission requires Content Moderation’s *View any unpublished content* or the *Node* module's *View own unpublished content* permission

Content Moderation then creates a permission for each transition per workflow. For example, “Editorial workflow: Use Archive transition” allows only users with this permission to move entities with the Editorial workflow from the published state to the archived state. This is particularly useful for different moderators to move content between states that they are responsible for.

Image

![Drupal's permissions UI matrix showing list of permissions described above.](../assets/images/content-moderation-overview-permissions.png)

## Contributed modules

While this list is likely to change rapidly as the ecosystem around Content Moderation and Workflows expands, here are a few contributed modules we think are worth checking out:

- [Content Moderation Notifications](https://www.drupal.org/project/content_moderation_notifications): Allows notifications to be sent via email when a piece of content is transitioned from one state to another.
- [Moderation Scheduler](https://www.drupal.org/project/moderation_scheduler): Schedule nodes to be published at specified dates in the future. Alternate option [Scheduler content moderation integration](https://www.drupal.org/project/scheduler_content_moderation_integration).
- [Moderation Sidebar](https://www.drupal.org/project/moderation_sidebar): Provides an off-canvas menu with options to moderate the current entity.
- [Moderation Dashboard](https://www.drupal.org/project/moderation_dashboard): Provides a per-user dashboard that contains useful blocks related to managing moderated content.

## Recap

In this tutorial we learned that the Workflows module allows the creation of new workflows, which are a combination of states and transitions. The Content Moderation module allows the workflows to be attached to content.

## Further your understanding

- Think of a workflow that involves more than published/unpublished states. What new states and transitions would you need to define in order to facilitate this workflow?
- What new workflows could you apply to your existing editorial process to improve things?
- The [Workflows Field](https://www.drupal.org/project/workflows_field) module is a contrib module available that depends on Workflows module. It's a great example of how workflows in Drupal can be used in different ways.

## Additional resources

- [Workflows overview](https://www.drupal.org/docs/8/core/modules/workflows/overview) (Drupal.org)
- [Content Moderation overview](https://www.drupal.org/docs/8/core/modules/content-moderation/overview) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[What Are Revisions?](/tutorial/what-are-revisions?p=2501)

Clear History

Ask Drupalize.Me AI

close