---
title: "Is Decoupling the Right Choice?"
url: "https://drupalize.me/tutorial/decoupling-right-choice?p=2960"
guide: "[[decoupled-headless-drupal]]"
---

# Is Decoupling the Right Choice?

## Content

[Andrew Berry](https://www.lullabot.com/who-we-are/andrew-berry), from [Lullabot](https://www.lullabot.com/), has written a great article asking [Should you Decouple?](https://www.lullabot.com/articles/should-you-decouple) Like most architectural decisions there are trade-offs to consider with a decoupled approach. Let's take a look at some of the pros and cons of a decoupled approach. Is it the right choice for your project?

## Goal

Understand the pros and cons of a decoupled approach.

## Prerequisites

- [Decoupling Explained](https://drupalize.me/tutorial/decoupling-explained)

## A solid content API foundation

Building a decoupled site is probably an especially attractive option if you know you need to support multichannel publishing. The more work that goes into content strategy in order to produce reusable content, the easier it will be to support emerging publication mechanisms. If your website is forced to use the same content API as other applications you'll be forced to ensure the API is robust enough to support multiple independent consumers.

With a solid content API as a foundation, it's possible to independently develop any number of front ends. As an example, let's say we have an old Drupal 6 project that is still going strong. We know that eventually the Drupal security team will cease to support our Drupal 6 code base. Leaving our project live in production introduces some potential future security vulnerabilities. If we had built the site with a decoupled approach our front-end would be powered by a well-defined content API. With the contract of this API in place, we'd be able to replicate it in the latest version of Drupal without having to worry about also recreating a Drupal theme.

## Upgrade flexibility

A decoupled approach gives us the flexibility to independently upgrade either the front-end or back-end of our site, without the need to upgrade them both at the same time, in the same project or contract. This decoupling also means that we can be less reliant on front-end Drupal expertise. We can build our website using whatever framework or template system our developers prefer. This month we can build a site based on [Backbone.js](https://backbonejs.org/), next month use [Angular.js](https://angularjs.org/), and then [React](https://facebook.github.io/react/) the month after that – all without touching our back-end code at all. This also reduces the number of responsibilities and complexity of our back-end Drupal site, too, which may make upgrading to future versions easier.

## Many layers, increased complexity

As nice as it may sound, a decoupled approach is certainly not a panacea. Moving from a monolithic to a decoupled architecture increases the number of components that make up your site. This means that in dealing with everything from hosting to monitoring to debugging there are more independent pieces to maintain and track. Figuring out where in the stack a bug is coming from is more difficult with each additional layer involved in responding to a request. Because of this increase in complexity, building a decoupled site often makes more sense in larger teams, when each team has strictly separate areas of concern and is able to work independently towards the API specification. Unless you need to support a large number of external applications, this means that a decoupled approach may not be the best solution for small sites and small teams.

## Reinventing the wheel

Another drawback to decoupled Drupal is the complete loss of Drupal's front-end functionality. Both core and contributed modules provide solutions for previewing unpublished content, localization of the user interface, and accessible markup. With a completely independent front-end you're forced to rebuild these features instead of simply relying on the work Drupal has already solved for us. Another difficulty to acknowledge is that coming up with a [solid content strategy for reusable content](https://karenmcgrane.wordpress.com/2012/09/04/adapting-ourselves-to-adaptive-content-video-slides-and-transcript-oh-my/) is hard. This is especially true if you're dealing with a well-established site where the bulk of content is contained in a single "blobby" body field rather than [discrete, flexible, reusable chunks](https://www.lullabot.com/articles/deblobbing-your-chunks-building-a-flexible-content-model).

## Recap

With a better understanding of the trade-offs of a decoupled architecture, what types of questions should we be asking to decide if it's right for a particular project?

- Are the front-end requirements incredibly rigid, and your development team has little Drupal experience?
- Does the site need to combine data from multiple sources, like a video management system, various content repositories, social media, etc.?
- Are there multiple development teams available that could benefit from working concurrently and independently of one another?
- Does the project require publishing through multiple channels that need to launch simultaneously?
- Are the development team's skills better suited for a site building or API development approach?

The more of these questions you answer "yes" to, the more I would recommend considering a decoupled approach. I'd also recommend going into the project with an understanding that, while there are benefits to the additional layer of abstraction, it ultimately depends on weighing the business value a decoupled approach provides with the extra complexity it creates.

## Further your understanding

- Evaluate your project based on the questions above. Is decoupling the right choice for your project?

## Additional resources

- [Should you Decouple?](https://www.lullabot.com/articles/should-you-decouple) (lullabot.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Decoupling Explained](/tutorial/decoupling-explained?p=2960)

Next
[Building a Solid API](/tutorial/building-solid-api?p=2960)

Clear History

Ask Drupalize.Me AI

close