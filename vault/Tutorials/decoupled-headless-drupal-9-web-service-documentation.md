---
title: "Web Service Documentation"
url: "https://drupalize.me/tutorial/web-service-documentation?p=2960"
guide: "[[decoupled-headless-drupal]]"
order: 9
---

# Web Service Documentation

## Content

When you are implementing an HTTP API for a decoupled project, one of the critical, but often overlooked, aspects is the API documentation. Documenting your API will allow front-end developers (and you six months from now) to learn how to use that particular API.

In Drupal, there are several modules that can read your site configuration and generate documentation for you automatically.

In this tutorial we're going to:

- Learn about the importance of good documentation.
- Decide whether or not to use an existing specification for our API such as JSON:API or GraphQL.
- Review options for automatically generating documentation.

By the end of this tutorial you'll be able to decide whether or not using an existing documentation specification is a good fit for your project, and choose an option based on those available for use with Drupal.

## Goal

Explain the importance of documenting your API, and choose whether or not you'll use an an existing specification to auto-generate documentation based on Drupal's data model.

Sprout Video

## The importance of good documentation

Just like any other programming interface, HTTP APIs are a set of conventions that the back end application (Drupal in our case) exposes to allow consumer applications to fulfill their purposes. Thus an API can be viewed as the contract between the back end and the front end side of the application. For a healthy contractual relationship, all the parties involved need to be aware of the contents of the contract. In our case, that means that we need to expose and maintain a document explaining the data structures of our API -- also known as the data model -- and how to interact with them. Not only do we need to expose that, but we also need to make sure that any changes that happen are propagated to the documentation.

Good API documentation will describe:

- How to interact with the API to extract the relevant content from it, and to create/update/delete content in it. These interaction rules can stay the same across different technologies (RoR, Drupal, Laravel, etc.) and across different Drupal sites.
- The shape of the data structures representing each of the content types exposed in the API. This data model is heavily dependent on the site configuration, so it's likely to change from site to site based on the content model.

## Using an API specification

I created APIs that I designed from the ground up in the past. While that was a rewarding technical experience, I learned that the developers of the consumer applications needed to have a clear understanding of how to use that API. That led me to create thorough documentation about how to tailor development to mesh with the API that I designed. If you are like me, writing documentation is **not** the thing that you love the most about your job.

Over time, I realized that there were some flaws in the original design, so I had to fix them. That meant that I had to run back to the documentation to amend that too. The actual API and the documentation went out of sync pretty quickly. When I had to write my next HTTP API, I took it upon myself to research existing specifications that were both widely used and well documented.

Implementing such specification has the following immediate benefits:

- It removes the need to discuss how this API works, since the specification already states all that.
- It plans ahead for some features that you will likely need, even if you don't realize it now. This will prevent you from having to run back to add features that were not initially planned.
- It includes detailed documentation of how it works. That documentation is the specification itself.

In addition to all those, choosing *popular* specifications (such as [JSON:API](http://jsonapi.org/format/) or [GraphQL](http://facebook.github.io/graphql/)) has other benefits like:

- There is a lot of feedback online about them, highlighting their pros and cons and pointing out their gotchas and hidden gems.
- There are many tools that interact with APIs that follow those specifiations.

## Auto-generated documentation

Even when you go through the effort of writing good documentation for your API, it may go out of date soon.

Imagine that you have an HTTP API for your Drupal project, and that you have written the documentation for all of the resources available, and all the properties in each resource as well. Every time you alter a resource in some way, like adding a new field to a content type, you will need to update the documentation. Remember that having bad documentation can be worse than having no documentation at all.

A big advantage of using Drupal to power your web service is that Drupal knows about the entity types and fields that are exposed through your API. When you save a boolean field in your content type, Drupal stores a lot of information as typed data definitions. It stores things like the name of the field, the data type, a description of the field, if the field is single value or multivalue, and more.

Modules like [OpenAPI](https://www.drupal.org/project/openapi) and [Schemata](https://www.drupal.org/project/schemata) leverage this information to generate documentation for the most commonly used web services you can expose in Drupal. These modules ensure that the documentation is always up-to-date and accurate since it is generated by the same internals that power the web service itself. That means that there is no need for a human to write and update documentation.

The [Schemata](https://www.drupal.org/project/schemata) module produces documentation in the [JSON Schema](http://json-schema.org) format. This format that is designed for machine consumption. [OpenAPI](https://www.drupal.org/project/openapi) installed alongside [OpenAPI UI](https://www.drupal.org/project/openapi_ui) and a compatible UI library (e.g. Swagger UI or ReDoc) provides a way to view documentation for APIs installed on your Drupal site (like JSON:API and REST modules). The main advantage of the Schemata module is that you can use the generated JSON schema information about the API to automate many other processes. That includes generating [human-readable documentation](http://json-schema.org/implementations.html#documentation-generation). Learn more about Schemata in our tutorial, [Automatic Documentation with Schemata](https://drupalize.me/tutorial/automatic-documentation-schemata).

## Further your understanding

- Do you have a plan for creating, and maintaining, documentation for your project? What is it?
- Read about [JSON:API](http://jsonapi.org/), and [GraphQL](http://graphql.org/learn/) to learn more about these specifications.
- Is there an existing specification that you think will work well for your project? Why?

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Modern Web Services with JSON:API and GraphQL](/tutorial/modern-web-services-jsonapi-and-graphql?p=2960)

Next
[Automatic Documentation with Schemata](/tutorial/automatic-documentation-schemata?p=2960)

Clear History

Ask Drupalize.Me AI

close