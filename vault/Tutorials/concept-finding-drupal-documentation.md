---
title: "Concept: Finding Drupal Documentation"
url: "https://drupalize.me/tutorial/concept-finding-drupal-documentation?p=3234"
guide: "[[drupal-module-developer-guide]]"
order: 5
---

# Concept: Finding Drupal Documentation

## Content

To become an effective module developer, you'll need to know how to navigate and use Drupal's extensive documentation. In this tutorial, you'll learn about the types of documentation available to Drupal developers, including API references, community-contributed documents, and best practices for using these resources.

## Goal

Familiarize developers with the types of Drupal documentation, where to find them, and how to effectively use these resources.

## Prerequisites

- None.

## Understanding Drupal's documentation

Drupal offers an array of documentation resources. Each serves a different purpose depending on what task you're working on as a module developer.

### Community-contributed documentation

Located at: <https://www.drupal.org/docs>

This wiki-like documentation is written and maintained by the Drupal community. There's a lot of content in this wiki, it's of varying quality, and can be difficult to navigate due to unlimited scope. But don't let that dissuade you, as it's full of good information and examples. Look here for practical examples of using Drupal's APIs in real-world scenarios. And for more in-depth explanations of best practices, and why certain decisions were made.

For developers, scan the top-level pages of <https://www.drupal.org/docs/develop>. Or search the content using a Google search like [`site:drupal.org caching render arrays`](https://www.google.com/search?q=site%3Adrupal.org+caching+render+arrays&ie=UTF-8).

### Official API documentation

Located at: <https://api.drupal.org>

This technical API documentation is the primary reference for Drupal's functions, classes, and interfaces. This is most similar to the [documentation for PHP on php.net](https://www.php.net/docs.php). It consists of:

- Topical pages that provide an overview of a Drupal core subsystem like [this one on using Ajax](https://api.drupal.org/api/drupal/core%21core.api.php/group/ajax).
- Reference documentation for specific classes, methods, and functions. For example [how to use the `t()` function](https://api.drupal.org/api/drupal/core%21includes%21bootstrap.inc/function/t/).
- Aggregate pages that list things like all [services](https://api.drupal.org/api/drupal/services/) or [constants](https://api.drupal.org/api/drupal/constants/).

Use [api.drupal.org](https://api.drupal.org) if you’re writing a Drupal module and want to know how to call a specific API, what arguments to pass to a function or method, or the names of things like specific hooks, services, or events.

### Change records

Located at: <https://www.drupal.org/list-changes/drupal>

Change records document any API changes between versions of Drupal core. They are helpful in understanding how to update your code to ensure it remains compatible as Drupal core changes over time.

### Examples for Developers project

Located at: <https://www.drupal.org/project/examples>

The Examples for Developers project contains modules which illustrate best practices for implementing various Drupal APIs. These modules can be enabled individually, so you can see the effects of the code. All the code for each module in this project is extensively commented and provides an implementation that you can use for reference. Be aware that the examples are not always up-to-date with the latest versions of Drupal. Check the project's issue queue for suggested updates. And treat the examples as demonstrations only, not production-ready code.

### Drupal coding standards

Located at: <https://www.drupal.org/docs/develop/standards>

This guide contains documentation for Drupal coding standards which apply to code inside Drupal projects. Learn more in [What Are Drupal Coding Standards?](https://drupalize.me/tutorial/what-are-drupal-code-standards)

### Module-specific documentation

Some contributed modules provide module-specific documentation. Start with the module's project page on Drupal.org. There you'll find an extended description of the module's features and links to documentation. Within the project's codebase, look for a README file, and any *{MODULE\_NAME}.api.php* files in the root directory of the module's source code.

### Drupal Answers (drupal.stackexchange.com)

Located at: <https://drupal.stackexchange.com>

Ask and answer questions about all things Drupal. An active community of Drupal developers participate in this Stack Exchange.

### The Weekly Drop

Located at: <https://theweeklydrop.com>

A weekly email newsletter with curated links to current news, new tutorials, and other happenings in the community. Use this to keep up with major changes and additions to Drupal core, and examples of how others are implementing Drupal's APIs in real-world scenarios.

## Participate in the community

One of the best ways to learn Drupal, and get answers to your questions, is to participate in the global Drupal community. As an open source project, Drupal relies on the efforts of community members to improve documentation and define new best practices. Those who participate in the community (via documentation or other means) will find it easier to get answers to their own questions when they arise.

### Contributor Guide

Located at: <https://www.drupal.org/community/contributor-guide>

The Drupal Contributor Guide can help explore contribution opportunities within the Drupal project. Whether you are new to contributing to the Drupal project and community, or are an experienced contributor looking for a new task or role, you can use this guide to explore the possibilities.

### Drupal Slack

Learn more at: <https://drupal.org/slack>

Within the Drupal Slack's channels, you can ask and answer questions, connect with others in the community, and contribute to discussions on specific topics.

## Best practices for using documentation

1. **Start with the official API docs**: When learning a new aspect of Drupal or troubleshooting, begin with the official API documentation.
2. **Explore community contributions**: For practical implementation and examples, explore community-contributed documents and the Examples for Developers project.
3. **Refer to module documentation**: Always read the documentation of the modules you are working with or planning to integrate into your site.
4. **Participate in the community**: Engage with the Drupal community through forums and discussions for additional insights and support.

## Recap

In this tutorial, we described the kinds of documentation you'll want to know about and use as a Drupal module developer. Sources vary from community-contributed guides, code examples, standards, and official API documentation. Which source you use will depend on what you're doing. Follow best practices like starting with the official API documentation, exploring community-contributed docs, reading *README* or *MODULE.api.php* files in a module's source code. Engage with other folks in the community to ask and answer questions, and you'll be on your way to successfully developing modules for Drupal sites.

## Further your understanding

- Can you locate the Drupal coding standards documentation?
- How can you figure out what the name of a specific Drupal core service is?
- In what ways can community-contributed documentation enhance your module development skills?

## Additional resources

- [Drupal Community Documentation](https://www.drupal.org/documentation) (Drupal.org)
- [Drupal API Reference](https://api.drupal.org/api/drupal) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: How Drupal Builds a Page](/tutorial/concept-how-drupal-builds-page?p=3234)

Next
[Concept: Drupal Development Environment](/tutorial/concept-drupal-development-environment?p=3234)

Clear History

Ask Drupalize.Me AI

close