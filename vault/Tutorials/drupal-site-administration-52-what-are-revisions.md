---
title: "What Are Revisions?free"
url: "https://drupalize.me/tutorial/what-are-revisions?p=2501"
guide: "[[drupal-site-administration]]"
order: 52
---

# What Are Revisions?free

## Content

Drupal has had revisions for a long, long time. However, they have often been under-utilized. Understanding how revisions work and how the Content Moderation module works with them is important to for being able to take full advantage of the systems features.

In this tutorial we'll:

- Explain what the different types of revisions are
- Understand when, and how, revisions are created

By the end of this tutorial you should have an understanding of what each type of revision is, how they're created, and how to work with them.

## Goal

Define what pending, default, and past revisions are, and when they are used, so that when you create a custom editorial workflow you'll have a better understanding of how revisions are used.

## Prerequisites

- [Overview of Workflows and Content Moderation](https://drupalize.me/tutorial/overview-workflows-and-content-moderation)
- [6.1. Adding a Content Type](https://drupalize.me/tutorial/user-guide/structure-content-type?p=3071) (Drupal User Guide)
- [6.3. Adding Basic Fields to a Content Type](https://drupalize.me/tutorial/user-guide/structure-fields?p=3071) (Drupal User Guide)

## What is a revision?

When content like a blog post is edited, Drupal can be configured to retain a copy of the current version, and create a new version alongside it. Over time, you might end up with many different versions of the same blog post, each reflecting a previous variant. While all of these different copies are stored in the database, only one of them is the one that's used when you navigate to the blog post in your browser.

This is similar to tracking changes in a Word document, or being able to review the history of a file in a version control system like Git.

Image

![Diagram showing past revisions on the left, default revision in the middle, pending revisions on the right, illustrating the flow from previous to current to future.](../assets/images/revisions.png)

## What is a default revision?

When visiting a page of content, or when a custom block is loaded on a page, Drupal needs to decide which revision to load. Therefore, a revision is singled out as the *default revision*, indicating that without any other context this is the one that should be used.

This is also commonly referred to as the published revision.

Drupal's default behavior when saving content is to create a new revision that contains any updates, and then make that new revision the default revision, unless something steps in to change that. Content Moderation is one such module that can apply a series of criteria to decide whether the content should be saved as a default revision or a pending revision.

## What is a pending revision?

Using modules like Content Moderation it is possible to create a revision that is newer than the currently published revision. This is called a pending revision.

Pending revisions are not a new concept to Drupal. However, they are now more visible with modules such as Content Moderation exposing them.

Before Content Moderation was added to Drupal core a module such as Workbench Moderation was needed to create a pending revision. When saving a new content revision without such a module, each revision is saved as a default revision.

## What is a past revision?

Once a new default revision is created, the old revision then become a past revision. You can think of past revisions as representing a previous state of the content, while a pending revision represents a possible future state.

There is a lot of continuing work within Drupal Core to better define and handle what is and what isn't a past revision. Recently, this has been focused on translations to allow each translation of an entity to maintain a rigid revision structure.

## Creating a pending revision

A pending revision has always been possible in Drupal, and was sometimes called a forward revision or draft revision. However, it had not been possible via the UI in core until Content Moderation arrived.

The editorial workflow, which ships with Content Moderation, has three states: draft, published, and archived. The published and archived states both are set to create a default revision. The draft revision doesn’t have this setting set, meaning it won’t create a forward revision. Therefore, if the current state of a revision is published or archived, moving the content to draft would create a pending revision. The first revision of an entity always has to be a default revision. Therefore, creating an entity with the draft workflow state will create a default revision, but with an unpublished publishing status, if the entity type supports publishing.

When creating a new workflow, as long as there is state with the default revision setting, and state without it, it’d be possible to create a pending revision. This will allow the content authors to create a default revision, the one users see when they visit the page. Then create a non-default revision after that, which will create a pending revision.

## Recap

In this tutorial we learned that a default revision is the one site visitors see. Pending revisions are newer, often draft content. Past revisions are older (they used to be the default revision), and provide a historical record of changes.

## Further your understanding

- Pending revisions are a new concept. They have sometimes been described as forward revisions or draft revisions. There is [ongoing discussion](https://www.drupal.org/project/drupal/issues/2940575) to further define and document pending revisions, specifically regarding use cases like sequential vs. non-sequential pending revisions.

## Additional resources

- In Drupal 7 the [Workbench Moderation](https://www.drupal.org/project/workbench_moderation) module provides the ability to have pending/draft revisions.

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview of Workflows and Content Moderation](/tutorial/overview-workflows-and-content-moderation?p=2501)

Next
[Plan an Editorial Workflow](/tutorial/plan-editorial-workflow?p=2501)

Clear History

Ask Drupalize.Me AI

close