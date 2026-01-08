---
title: "Apply an Editorial Workflow to a Content Type"
url: "https://drupalize.me/tutorial/apply-editorial-workflow-content-type?p=2501"
guide: "[[drupal-site-administration]]"
---

# Apply an Editorial Workflow to a Content Type

## Content

In order to enforce that an editorial workflow is applied to a specific content type you need to update the workflow's configuration. Then, depending on your needs, you may also need to configure new user roles, giving them permission to transition a content item from one state to another.

This process works for any Content Moderation type workflow -- including the *Editorial* workflow that Drupal provides and any [custom workflows](https://drupalize.me/tutorial/create-custom-workflow) you've created.

In this tutorial we'll:

- Update a workflow so that its rules are applied to a content type
- Review the list of permissions provided by a workflow and see how we can set things up to restrict certain users to only perform specific transitions

By the end of this tutorial you will be able to configure a workflow so that it applies to one or more content types, and configure permissions so only users in a specific role can transition content items from one state to another.

## Goal

Update the custom workflow created in [Create a Custom Workflow](https://drupalize.me/tutorial/create-custom-workflow) so that it applies to the *Article* (or any other) content type.

## Prerequisites

- [Overview of Workflows and Content Moderation](https://drupalize.me/tutorial/overview-workflows-and-content-moderation)
- [Create a Custom Workflow](https://drupalize.me/tutorial/create-custom-workflow)
- This assumes you have at least one [content type configured for your site](https://drupalize.me/series/user-guide/content-structure-chapter).

## Video walk-through

Sprout Video

## Getting started

### Enable the Workflows and Content Moderation modules

Start by enabling the Workflows and Content Moderation modules if they are not already enabled.

[Learn more about enabling modules](https://drupalize.me/tutorial/user-guide/config-install?p=3069).

### See a list of existing workflows

In the Manage administration menu navigate to *Configuration* > *Workflows* (*admin/config/workflow/workflows/manage/*). Here you'll find a list of all the workflows configured for your site. By default, this should contain one workflow named *Copy editing required*.

Image

![Workflows](/sites/default/files/styles/max_800w/public/tutorials/images/workflows.png?itok=IBkdc0bc)

### Edit the workflow

Click the *Edit* button for the *Copy editing required* workflow. (Or whichever workflow you want to edit.) This will take you to a configuration page for the workflow where you can get an overview of the states, transitions, and other options for the workflow.

Image

![Editorial workflow configuration page](/sites/default/files/styles/max_800w/public/tutorials/images/edit-workflow.png?itok=a7fZjbaB)

### Configure the workflow to apply to a content type

In the section, *This workflow applies to:*, click the button labeled *Select* in the *Content types* row.

Image

![Form for choosing a content type, shows checkboxes for each content type, article and basic page, and a Save button.](/sites/default/files/styles/max_800w/public/tutorials/images/edit-workflow-choose-content-type.png?itok=ux2hqLjr)

This will open a form in a modal window which lists the content types configured for your site. Click the checkbox next to any content types you want this workflow to apply to. Then click the button labeled *Save* to save your changes.

After the modal closes, changes to the workflow will be saved. You don't need to also click the *Save* button for the workflow editing form.

**Note:** When you apply a workflow to a content type with existing content all existing content will automatically get the draft or published moderation state depending on the content's publishing status.

At this point you've configured your workflow to apply to one or more content types. Next we'll look at how you can configure who can transition a piece of content from one state to another, as well as where, and how, you can change the state of a piece of content.

## Permissions

Workflows generate a new unique permission for each of the different transitions they contain.

In the case of the default *Editorial* workflow, for example, there are five permissions:

- Editorial workflow: Use Create New Draft transition.
- Editorial workflow: Use Archive transition.
- Editorial workflow: Use Publish transition.
- Editorial workflow: Use Restore transition.
- Editorial workflow: Use Restore to Draft transition.

A transition allows an item of content to move from one workflow state to another. Any user with the permission associated with a transition will be able to perform that transition.

Take for example the `Editorial workflow: Use Publish transition` permission. If a user has just this permission they can create new content as published, and publish existing unpublished (draft) content. They would, however, not be able to archive (unpublish) content.

In [Plan an Editorial Workflow](https://drupalize.me/tutorial/plan-editorial-workflow) we defined a set of jobs that someone might do in an editorial workflow. If you need to restrict which transitions different people are able to perform you can [create new user roles](https://drupalize.me/tutorial/user-guide/user-new-role), [assign one or more of the permissions above to the role](https://drupalize.me/tutorial/user-guide/user-permissions), and then [assign that role to a user](https://drupalize.me/tutorial/user-guide/user-roles).

## Recap

In this tutorial we learned that the *Editorial* workflow is installed when enabling the standard installation profile. It can be applied to any content type via its configuration form. Each transition within the workflow generates a permission to allow a user to move content through that transition. Those permissions can be used in combination with roles to enforce rules regarding who can move content from one state to another.

## Further your understanding

- Can you apply a workflow to the creation of block content?
- What combinations of roles and permissions will you need to enforce your editorial workflow?

## Additional resources

- [Workflows overview](https://www.drupal.org/docs/8/core/modules/workflows/overview) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Create a Custom Workflow](/tutorial/create-custom-workflow?p=2501)

Next
[Manage Moderated Content](/tutorial/manage-moderated-content?p=2501)

Clear History

Ask Drupalize.Me AI

close