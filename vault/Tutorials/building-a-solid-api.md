---
title: "Building a Solid API"
url: "https://drupalize.me/tutorial/building-solid-api?p=2960"
guide: "[[decoupled-headless-drupal]]"
---

# Building a Solid API

## Content

There's been a lot written about API design, it's probably not surprising there are [several](http://restfulwebapis.com/) [books](http://shop.oreilly.com/product/0636920021223.do) written about the subject. It also seems like nearly every cloud-based service provides an API to allow access to your data. In this tutorial, we'll attempt to condense this information and answer the following questions:

- Are there different types of API paradigms?
- What kinds of considerations do we need to make when building an API for our decoupled site?
- And, what's this REST thing everyone is talking about?

Let's dig into those questions one at a time.

## Goal

Understand the technology behind decoupled Drupal, like building an API and REST.

## Prerequisites

- None.

## What makes a "good" API?

Daniel Jacobson, one of the developers involved in NPR's Create Once Publish Everywhere (COPE) work, [wrote about the criteria for creating a successful API](http://www.danieljacobson.com/blog/231). Jacobson argues, in order to be a "good" API you need to support multiple output formats. Client may prefer to consume your data as XML or JSON, but don't force them to do the conversion. Your API should also support customizable markup, meaning the API easily allows consumers to rename or map the fields that are output. It's also essential to be able to provide partial responses, to allow clients to filter and limit the result sets they're interested in within the request itself. A good API is also documented, and provides tooling like a user interface to query and browse its output. Ideally, a successful API needs to have a comprehensive caching architecture so that it doesn't need to resort to rate limiting. Lastly, a good API is versioned, to allow for the iteration of an evolving API but also support for earlier API releases. We'll see examples of implementing most of these principles as we progress throughout this series.

In building one of these "good" APIs for our project, we're implementing an interface, or a contract, between our back-end Drupal site and what is available to the decoupled front-end. There are [inherent virtues](https://www.lullabot.com/articles/beyond-decoupling-the-inherent-virtues-of-an-api) to this communication interface, including better documentation and the ability to do [test-driven development](http://www.agiledata.org/essays/tdd.html#WhatIsTDD). In fact, there are many reasons to consider a [spec-driven development](http://blogs.mulesoft.com/dev/api-dev/api-best-practices-series-spec-driven-development/) approach. For example, building API first allows you to solicit user feedback which may expose tricky edge cases, or mistakes in your content model that are much easier to fix earlier in the project.

## What is REST?

Recently there is a lot of interest and buzz around REST APIs, but what does REST actually mean? REST stands for Representational State Transfer. The term comes from a dissertation by Roy Fielding on [Architectural Styles and the Design of Network-based Software Architectures](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm). There are very few APIs that meet the criteria of pure REST (as originally defined). It's useful to think of REST as a bit of a continuum, with a few distinct levels of REST support. The steps of this continuum come from something called the [Richardson Maturity Model](http://martinfowler.com/articles/richardsonMaturityModel.html).

## What are the levels of REST support?

### REST Level 0

Level 0, or "the swamp of POX," is for an API that is simply using HTTP as a transport mechanism for data. An API at this level is quite easy to build with Drupal using a module like [Views Datasource](https://www.drupal.org/project/views_datasource). An API at this level might have an endpoint like `/content` which also allows calls to something like `/content?type=article`. Often times there is one single endpoint for all the possible calls supported by this type of API.

### REST Level 1

As we move up the maturity model to level 1, we begin to work with resources. A good sign you're working with an API at this level is that you're working with multiple endpoints, one for each type of data you're working with. Endpoints for this type of API probably look list `/articles`, `/articles/1`, and `/articles/1/delete` but are still probably using a single HTTP method (POST).

### REST Level 2

Level 2 in the Richardson Maturity Model is fairly common, since it's the default provided by frameworks like Ruby on Rails. At this level the API must use HTTP verbs. Rather than using multiple endpoints for an article with the id of 1, you'd have a single endpoint `/article/1`. The HTTP request method (GET, POST, DELETE, PATCH) determines the type of operation being performed on the resource. APIs at this level are extremely common, and can be considered RESTful even though they can't really be considered pure REST.

### REST Level 3

Level 3 introduces something called Hypermedia controls, and Hypertext As The Engine Of Application State (HATEOAS). This is a fancy way of saying your API provides an engine responsible for the representational state transfer (REST) of a resource. While there is no single way to do this, generally it requires that the endpoint for a particular resource documents all the actions that can be performed on it. In this way the API is self-documenting and discoverable.

Steve Klabnik explained HATEOAS in [a simple example on a blog](https://web.archive.org/web/20130115235435/http://timelessrepo.com/haters-gonna-hateoas). Ryan Szrama gave a presentation (with a good list of resources) called [Toward Hyper-Drupal](https://github.com/rszrama/toward-hyperdrupal) which helps explain several of these components in more detail. If you build an API in Drupal by using the JSON:API module, you'll have some support for these HATEOAS links provided for you.

Here is an example for an article endpoint:

```
{
    "data": {
       "type": "node--article",
       "id": "d99f021b-c3c8-41f0-bd8d-c8d02c22e2a1",
       "attributes": {
            "body": {
                "format": "plain_text",
                "summary": "Abdo autem …"
            },
            "changed": 1493584841,
            …
            "status": true,
            "title": "Abico Importunus",
            "uuid": "d99f021b-c3c8-41f0-bd8d-c8d02c22e2a1"
        },
        "links": {
            "self": "http://d8dev.local/jsonapi/node/article/d99f021b-c3c8-41f0-bd8d-c8d02c22e2a1"
        },
        "relationships": {
            …
            "field_image": {
                "data": {
                    "id": "e8eb2b4f-2d94-4c3e-8cc3-9dca66e7b295",
                    "type": "file--file"
                },
                "links": {
                    "related": "http://d8dev.local/jsonapi/node/article/d99f021b-c3c8-41f0-bd8d-c8d02c22e2a1/field_image",
                    "self": "http://d8dev.local/jsonapi/node/article/d99f021b-c3c8-41f0-bd8d-c8d02c22e2a1/relationships/field_image"
                }
            }
        }
    }
}
```

There are several competing data formats to provide the extra linking data specified by HATEOAS. With Drupal, the JSON:API module in Drupal core supports HATEOAS via `links`. And the contributed [JSON:API Hypermedia module](https://www.drupal.org/project/jsonapi_hypermedia) extends this to support custom resource actions.

You may also be wondering how to handle API versions as your site evolves. It's quite common to either include version numbers [in the URL](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design#uri-versioning), or in the [accept header](https://steveklabnik.com/writing/nobody-understands-rest-or-http). This is somewhat possible if you're using the core REST API where you have more control over the URLs at which resources are accessed.

As of right now API versioning is not supported by Drupal's JSON:API module. The JSON:API module **automatically** creates a RESTFul API for your Drupal data model, but the downside is that it's inextricably linked to your site's current data model.

## Designing your API

With a better understanding of REST, we're now ready to look at other considerations that are important in building out an API.

Probably the first step in designing an API is coming up with the object schema that defines the resources you're going to be exposing. In general, it's a good idea to use repeatable property and field names (i.e.: title instead of videoTitle and articleTitle). It's also smart to use consistent date formats. Also, try to use the proper data types, integers for numbers instead of strings as an example. It's also wise to provide references to other objects instead of trying to provide a composite object (whenever possible).

To learn more about designing and implementing an API, see our [Web Services and Decoupled Drupal](https://drupalize.me/topic/web-services-and-decoupled-drupal) topic page.

## Recap

In this tutorial, we learned that a "good API" enables you to output content to multiple formats. There is a lot of buzz around building API that are "RESTful". REST stands for Representational State Transfer. We learned about the different levels of REST support, from basic HTTP data transfer, to using resources, and hypermedia controls.

## Further your understanding

- Discuss with colleague why you want to build an API? What problems will it solve? What challenges will it introduce?

## Additional resources

- [RESTful Web APIs (O'Reilly)](http://restfulwebapis.com/) (restfulwebapis.com)
- [APIs: A Strategy Guide (O'Reilly)](http://shop.oreilly.com/product/0636920021223.do) (shop.oreilly.com)
- Daniel Jacobson, one of the developers involved in NPR's Create Once Publish Everywhere (COPE) work, often [wrote about the criteria for creating a successful API](http://www.danieljacobson.com/blog/231) (danieljacobson.com)
- Mateu Aguiló Bosch wrote [Beyond Decoupling: The Inherent Virtues of an API](https://www.lullabot.com/articles/beyond-decoupling-the-inherent-virtues-of-an-api) (lullabot.com)
- [Introduction to Test Driven Development (TDD)](http://agiledata.org/essays/tdd.html#WhatIsTDD) (agiledata.org)
- Mike Stowe wrote [API Best Practices: Spec Driven Development (Part 2)](https://blogs.mulesoft.com/dev-guides/api-design/api-best-practices-series-spec-driven-development/) (blogs.mulesoft.com)
- Martin Fowler on the [Richardson Maturity Model](http://martinfowler.com/articles/richardsonMaturityModel.html) (martinfowler.com)
- Steve Klabnik explained HATEOAS in [a simple example on a blog](https://web.archive.org/web/20130115235435/http://timelessrepo.com/haters-gonna-hateoas) (web.archive.org)
- Ryan Szrama gave a presentation (with a good list of resources) called [Toward Hyper-Drupal](https://github.com/rszrama/toward-hyperdrupal) (github.com)
- Roy Fielding on [Architectural Styles and the Design of Network-based Software Architectures](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm) (ics.uci.edu)
- [JSON:API Hypermedia module](https://www.drupal.org/project/jsonapi_hypermedia) (Drupal.org)
- [URI versioning](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design#uri-versioning) (learn.microsoft.com)
- [Nobody understands REST or HTTP](https://steveklabnik.com/writing/nobody-understands-rest-or-http) (steveklabnik.com)
- [Web Services and Decoupled Drupal (topic)](https://drupalize.me/topic/web-services-and-decoupled-drupal) (Drupalize.Me)

Downloads

[RESTful HAL links](/sites/default/files/thiprouomucethopruprenilostachaspispasla "thiprouomucethopruprenilostachaspispasla")

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Is Decoupling the Right Choice?](/tutorial/decoupling-right-choice?p=2960)

Next
[Hosting Implications and Considerations](/tutorial/hosting-implications-and-considerations?p=2960)

Clear History

Ask Drupalize.Me AI

close