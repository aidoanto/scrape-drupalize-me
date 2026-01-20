---
title: "Plan an Editorial Workflow"
url: "https://drupalize.me/tutorial/plan-editorial-workflow?p=2501"
guide: "[[drupal-site-administration]]"
order: 53
---

# Plan an Editorial Workflow

## Content

Many sites are built around their content, especially Drupal sites. To manage this content, a strict editorial workflow is often highly desirable to make sure the content is drafted, reviewed, published, updated, and archived when ready.

In this tutorial we'll:

- Discuss the various components you'll need to define before you can start building a custom editorial workflow
- Provide an example editorial workflow plan

By the end of this tutorial you will better understand the use case for content moderation, and be able to create an editorial workflow plan for your use-case.

## Goal

List the different roles, states, and transitions required to achieve a specific editorial workflow.

## Prerequisites

- [Overview of Workflows and Content Moderation](https://drupalize.me/tutorial/overview-workflows-and-content-moderation)

## Why use moderation?

Traditionally in Drupal core, the option for a content workflow has been *published* or *unpublished*. This works well on basic sites, but consider these two use cases:

- A page of content is already published and live to users, but content authors now want to make a number of changes to the content without users seeing the changes until they are ready.
- There is a large team of content authors, and a strict review process, so content authors cannot publish content without review.

Both of these cases require functionality that goes beyond what's capable with only a published/unpublished checkbox.

## Out-the-box

Drupal core's standard installation profile already ships with an editorial workflow. This has 3 states: "draft", "published", and "archived", including the relevant transitions between these states. This covers the first use case outlined in the previous section. However, this workflow does not have a review step, so does not really cater to the second use case.

## Where to start?

Planning a workflow can often take longer than configuring and setting it up. A great place to start are personas. Think about the types of people who will be interacting with the site's content. For example:

- **Content authors** - The person who creates the content, but may not have sufficient permissions to publish it.
- **Reviewers** - Someone who is able to review and publish the content.
- **Legal reviewers** - There may be multiple steps of reviewing. Reviewing for legal reasons could be one of these.
- **Site admins** - This person may need to be able to take control of any content.

Another way to think about this might be to consider the various Drupal user roles you have configured for your site.

## How is content moderated?

Once you have nailed down the *who*, think about the *how*. The moderation states that will be assigned to each item of content is key. Having too many states will end in confusion, but too few will prevent users from doing their job.

It may also be necessary to have multiple states which serve the same purpose, but their name denotes a difference. Take the *Reviewer* and *Legal reviewer* personas discussed earlier. These may require the use of both a *Needs review* and *Needs legal review* moderation state. Under the hood, these states are exactly the same, in that they have the same effect on the content when applied. But for editorial purposes they label the person responsible for the work.

Transitions are also a key component in the workflow. It does not make sense to be able to transition between all the moderation states. Think about how the content will flow between the states, and between the personas mapped out earlier.

Don't forget to think about reverse transitions too. If a page of content is moved to *needs review* and the reviewer does not wish to publish it, it might need to go back to *draft*, or maybe even another state, such as *needs updating*.

## Make a plan

We recommend you start by making a list of the roles, states, and transitions you think you'll need. Then share that list with someone in each of the various roles to get their feedback and ensure their needs are met.

Image

![Illustration of the plan described below, including Roles, States, and Transitions.](../assets/images/plan.png)

### Roles/Personas

- Author
- Technical reviewer
- Copy editor
- Publication manager

### States

- Draft
- Needs technical review
- Needs copy editing
- Scheduled for publication
- Coming soon
- Published

### Transitions

These are the paths that content can take from one state to another.

- Draft → Needs technical review - creates an edit
- Needs technical review → Draft
- Needs technical review → Needs copy editing
- Needs copy editing → Scheduled for publication - creates an edit
- Scheduled for publication → Published
- Scheduled for publication → Coming soon
- Coming soon → Published
- Published → Draft - creates an edit

Some of these states, like "needs technical review", and "scheduled for publication", are non-editing states. That means that content will transition through that state without changes being made to the content. But we want them to exist in order to ensure the workflow is followed. A technical reviewer can suggest changes, and send something back to draft, but they won't actually make changes. The author needs to incorporate the changes.

Others states, like copy editing, result in edits being made. Any time an edit is made we want to make sure we save a new revision. When planning your workflows it's a good idea to keep track of when a state change should result in a new revision being created.

With a plan in place, you're now ready to start configuring the *Workflows* and *Content Moderation* modules to facilitate your editorial workflow.

## Recap

Before you start configuring the *Workflows* and *Content Moderation* modules it's a good idea to have a plan. Personas are a helpful tool to plan the content workflow. Think about how they interact with the content, which moderation states they will work with, and then how content will transition in and out of those states.

## Further your understanding

- What are the different roles that someone might fill in your editorial workflow?
- Make a list of the states that a piece of content might be in your editorial workflow.
- Diagram the different paths that a piece of content can take to get from one state to another. Remember that sometimes things might move backwards.

## Additional resources

- [Concept: Editorial Workflow](https://drupalize.me/tutorial/user-guide/planning-workflow?p=3076) (Drupal User Guide)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[What Are Revisions?](/tutorial/what-are-revisions?p=2501)

Next
[Create a Custom Workflow](/tutorial/create-custom-workflow?p=2501)

Clear History

Ask Drupalize.Me AI

close