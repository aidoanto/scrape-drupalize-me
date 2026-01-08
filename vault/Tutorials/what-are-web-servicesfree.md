---
title: "What Are Web Services?free"
url: "https://drupalize.me/tutorial/what-are-web-services?p=2960"
guide: "[[decoupled-headless-drupal]]"
---

# What Are Web Services?free

## Content

The term *web services* has been around for quite a while. Given that web services is such a broad topic, let's define what web services are and how we are going to refer to them throughout this series so we are all on the same page.

This tutorial is an introduction to web services that will help you:

- Learn what a web service is.
- Understand that this series focuses on HTTP web services, and mostly on REST principles.
- Get some examples of APIs in the wild and what type of consumers they have.

By the end of this tutorial, you'll be able to define what web services are, and how we'll use the term in the context of these tutorials.

## Goal

Review the formal and practical definitions of web services, and how they are used in our digital life.

## Formal definitions

According to the W3C, a web service is *a software system designed to support interoperable machine-to-machine interaction over a network*. In other words, a web service is any software that allows two or more programs (*machine-to-machine*) to exchange information and/or instructions (*interoperable interaction*) across the Internet or a local area network.

During this series we will see how a web service can be used to architect your digital project by decoupling the front end and back end components. We will achieve this by using a specific type of web service, an HTTP API. An HTTP API (many times just API) is a web service that communicates over the internet using the (plain text based) HTTP protocol.

Sprout Video

## Web services you already use

The importance of web services is highlighted by their omnipresence in our digital life. Most phone applications that interact with content use web services to fetch the content they need to display. They also use web services to allow you to create content. Some examples of these applications are Twitter, Facebook, your local newspaper, weather reports, Siri, Alexa, and the app for that sushi place you love.

Even applications that don't deal with a lot of content also use web services to perform their interactions. These include a smart lights controller app, FitBit trackers, the position in Google Maps, or chat services such as Telegram.

Another interesting aspect of web services is who has access to them. Many of these APIs are open to the public, so anyone can write software that integrates with them. This is the case of Netflix and GitHub (among many others). Some others only exist for internal use, like the encrypted messaging system of your home's silent alarm.

Even if web services are ubiquitous, there are times when they are not the best solution for a particular problem. In [Is Decoupling the Right Choice?](https://drupalize.me/tutorial/decoupling-right-choice) Blake Hall discusses when it is a good idea to use a web service in your Drupal digital project.

There is a great variety of types and shapes of web services. In this series, we will focus on content APIs in Drupal, our favorite content management system.

## Drupal HTTP APIs

For the purpose of this series, we are going to talk about APIs as the collection of features provided by Drupal modules that allow us to read and write content (nodes, taxonomy terms, users, etc.) and configuration (blocks, menus, permissions, etc.) using HTTP messages. It's worth noting that you will not need to deal with the HTTP protocol because you will most certainly use a library that abstracts that.

During the course of this series, we will assume some level of familiarity with HTTP concepts such as its methods (often called *verbs*) and headers. However, we'll briefly introduce these concepts along the way as well.

The modules that we will use in this series will follow the REST (representational state transfer) principles, which are a set of opinionated guidelines on how to structure your HTTP APIs.

## Recap

Web services are a great tool to transport information in a distributed environment, whether it is content or the demand to execute a remote action. They are present in some way or another in every *connected* tool we use.

## Further your understanding

- Can you think of any services or applications you use on a day-to-day basis that rely on web services?
- How do you intend to use web services in your own projects?

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Hosting Implications and Considerations](/tutorial/hosting-implications-and-considerations?p=2960)

Next
[Separation of Concerns: Content vs. Presentation](/tutorial/separation-concerns-content-vs-presentation?p=2960)

Clear History

Ask Drupalize.Me AI

close