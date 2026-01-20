---
title: "Modern Web Services with JSON:API and GraphQL"
url: "https://drupalize.me/tutorial/modern-web-services-jsonapi-and-graphql?p=2960"
guide: "[[decoupled-headless-drupal]]"
order: 8
---

# Modern Web Services with JSON:API and GraphQL

## Content

In the last several years REST has been the de facto standard for web services. However, there are several common problems when developing websites and digital experiences with the traditional REST implementations. Luckily, those issues have solutions, either complete or partial.

Modern web service specifications like [JSON:API](http://jsonapi.org) and [GraphQL](http://graphql.org) implement those solutions, although they differ slightly in their implementation.

In this tutorial we will learn about:

- The problems of traditional REST implementations
- Common solutions to those problems, and how JSON:API and GraphQL deal with them

By the end of this tutorial you'll be able to explain some of the common pitfalls of REST-based APIs, and how JSON:API and GraphQL address those issues.

## Goal

Examine problems of traditional REST implementations, and the common solutions to those problems.

Sprout Video

## Problems in traditional REST

When building digital experiences using REST you usually encounter the following problems:

- Multiple round trip requests from the consumer to the server.
- Bloated responses with more information than we need.
- Difficulties finding relevant content, and creating curated listings.

Bear in mind that we have to find a solution to these problems while muttering [our mantra](https://drupalize.me/tutorial/separation-concerns-content-vs-presentation): *Drupal does not serve a particular front-end, it serves many*. So we will be building solutions without imposing any particular visual design.

### Multiple round trips

Drupal is a great content management system with spectacular data modeling tools. This empowers users to build rich content models that make extensive use of relationships. In turn, this enables reuse of the content in different contexts for our projects. When using Drupal as a coupled solution, the system connects the different small units of content with the intention of assembling the desired presentation as HTML. In that scenario, these units of content are stored in the database and are connected together using [database joins](https://en.wikipedia.org/wiki/Join_(SQL)).

When using a REST solution we have a similar scenario, where for each type of those units of content we have a REST resource. Given a unit of content we can interact with it using an HTTP request, but when we assemble these related units of content we don't have the *join* capability to include everything in a single go. Instead we have to make additional HTTP requests to fetch each small unit of content from the consumer.

Given that we are making Drupal oblivious to any particular visual design in a decoupled scenario, it has to be the consumers who list the related entities to include in one single request. We will call this technique **resource embedding**. Resource embedding will allow consumers to call out the relationships that they want to include in the response. It is also possible to embed related entities on entities that were in turn embedded as well.

Imagine that we are building an Android app for a magazine. For that example the consumer needs to render a small block about the author underneath each of the articles. In that scenario, the consumer can request:

> Give me article with ID 12. Embed the user specified in the uid relationship. Also embed the image entity specified in the profile\_picture relationship on that user. Finally, give me the location entity in the field\_city relationship on the user.

We will need to transform that long consumer request to the appropriate syntax, but this is the information that we will get back.

Image

![The schematics of a response with the emdedded resources described above.](../assets/images/embedding-levels.png)

You can see that there are three embedding levels, encoded by colors. Without resource embedding, each level contains information about a resource that the consumer cannot start requesting until the parent response has come back from the server. The Android app wouldn't know that the user they want to display is user 36 until the response for the article has come back. You can see how the time spent waiting on responses -- so we can request more related data -- increases with the number of nesting levels. With resource embedding, the Android app will get all the information it needs from the API server in a single request.

JSON:API, HAL, GraphQL, etc. all have different syntaxes for resource embedding. We will focus on JSON:API in the following tutorials to learn how to get embedded resources using a Drupal backend.

### Bloated responses

Another common problem is that traditional REST implementations are atomic around entities. You either request an entity or you don't. In Drupal that means that we are returning all the fields that exist in a given entity. We have seen in [the tutorial about presentation logic](https://drupalize.me/tutorial/detect-presentation-your-data-model) that there are many fields that are important for Drupal, but a consumer will not be interested in all of them.

In order to simplify the response and only get the relevant fields back from the server, many API backends implement sparse field sets. We can think about sparse fieldsets as a table of resource entity types along with the list of relevant fields for it. That way an Apple TV consumer can request:

> Give me information about The Voice. Include information for the seasons and the contestants. For the show include only the cover image and the title, for the season include only the season number, and for the contestants include only their name and profile picture.

You can see how we are combining resource embedding and sparse field sets in the request above to get **all the information that we need, and only the information that we need, in a single request**.

Again, JSON:API and GraphQL have different ways to express sparse field sets. We will talk about sparse fieldsets in JSON:API in a separate tutorial.

### Discovering content

In the examples above I have assumed that the Android app knows that it needs to request article 12, and the Apple TV app knows how to get data about *The Voice*. In a real project you would never hard-code an ID in your consumer. This means that you need a way to find your content.

Finding content is a concept that feels natural to us. We are used to search engines and querying relational databases. In a decoupled project this will not be any different. We will need a way to have lists of entities for a particular resource. That way a consumer can request all the available articles for the site, for instance. Moreover we will need to have some sort of filtering capabilities so we can ask for **only** the articles created in the last 7 days.

When using coupled Drupal, Views is a fantastic solution to accomplish this. However it is not a viable solution for decoupled backends since -- as the name implies -- a view is heavily tied to a particular design. When building a view you select *in the backend* the fields, filters, etc. that the front-end will need. That is against the spirit of *Drupal does not serve a particular front-end, it serves many*.

We will see that *almost* all the modern decoupling solutions provide default listings of content when you request a resource without any particular ID. In addition to that they provide a way to limit the items that you get back based on filters applied on the fields for those items. This enables, for instance, an iPad app to display a menu with *the bands having one of the members whose birthday is this week, sorted by popularity*, for a side block in a musical magazine.

We will also be talking extensively about collections, filters, sorting and pagination for JSON:API in later tutorials.

## Recap

Traditional REST implementations have been criticized because they have significant shortcomings:

1. They require multiple requests from the consumer to the server with introduced wait time.
2. They return more information than we need, wasting bandwidth.
3. Difficulties to find relevant content, and to create curated listings.

However, more modern web service solutions -- like JSON:API and GraphQL -- solve these issues using:

1. Resource embedding.
2. Sparse field sets.
3. Collections with sorting and filters.

## Further your understanding

- See how [resource embedding can improve your application's performance significantly](https://www.lullabot.com/articles/modern-decoupling-is-more-performant).
- See sparse [fieldsets in action](http://jsonapi.org/examples/) in the JSON:API examples.
- Learn how [GraphQL implements collections and filters with their own query syntax](http://graphql.org/learn/queries/#arguments).

## Additional resources

- Watch this [DrupalCon presentation about the how JSON:API solves these problems in Drupal](https://www.youtube.com/watch?v=ogs7qAWSlnQ).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Detect Presentation in Your Data Model](/tutorial/detect-presentation-your-data-model?p=2960)

Next
[Web Service Documentation](/tutorial/web-service-documentation?p=2960)

Clear History

Ask Drupalize.Me AI

close