---
title: "Why Solr?free"
url: "https://drupalize.me/tutorial/why-solr?p=2815"
guide: "[[drupal-site-administration]]"
order: 15
---

# Why Solr?free

## Content

Drupal has long provided a built-in search mechanism, so why do we need anything more? In this tutorial, we introduce Apache Solr, a free and open source search service that has several advantages and features beyond Drupal’s built-in search.

In this tutorial, we'll:

- Define Apache Solr
- Identify Apache Lucene, the legacy name for Solr
- List key features of Solr
- Identify the advantages of Solr compared to Drupal search

## Goal

To understand the advantages that Apache Solr brings Drupal over the out-of-the-box search feature.

## Prerequisites

- General knowledge of Drupal, site building, and the command line.

See the following resources if you need a refresher on any of these areas of knowledge:

- [Introduction to Drupal](https://drupalize.me/guide/introduction-drupal)
- [Build Drupal Sites](https://drupalize.me/guide/build-drupal-sites)
- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)

## Search options for Drupal

When building a Drupal-powered website, there are several different options available to us to provide search for our site. Each has different benefits and consequences:

- Third-party search
- Embedded search
- Search appliances
- Drupal search
- Apache Solr

## Third-party search

The simplest option, of course, is to do nothing at all. Search engines such as Google, DuckDuckGo, Bing, and others will *crawl* your site, reading each page and following each link. When a page has been read, it is added to an *index*, a kind of database used for search systems. Often, we have little to no control over this process. Some search engines allow you to submit your site to be crawled and indexed, while others are wholly opaque.

If the site -- or budget -- is small, this may be the most effective option. After all, a majority of traffic arrives via a search engine. On the other hand, these search engines offer little to no control over how your site is indexed. Relying on external web search engines, while easy, surrenders control of your site's search over to third-party companies. They offer no understanding of how your site works, only the general structure of interlinked pages.

## Embedded search

Some search engine companies offer a customized search experience for a limited number of pages or for a fee. This provides several key advantages. Instead of going to a third-party website to search, search can easily be embedded into your existing site. Search results can be provided for only your website, on your website, and consistent with your website's theme and branding. Depending on the service, you may be able to further customize the search.

## Search appliances

A primary drawback of embedded search is that the actual search data -- the *index* -- is hosted by a third-party company. Again, this may be okay for sites with limited search needs, but it brings legal ramifications. Schools, hospitals, and government sites often deal with *personally identifiable information* (PII) that cannot be hosted off-site.

For this reason, some search companies have offered *search appliances*. A search appliance is a piece of hardware designed to use the search company's proprietary search algorithms to crawl websites while keeping the search data physically co-located with the client.

Search appliances have been on the decline in the last few years, as search companies no longer want to maintain physical devices. Furthermore, open source alternatives have appeared in recent years to consume this market.

## Drupal search

Drupal also provides a basic search mechanism out of the box. The **Search** module is enabled by default when you install Drupal. This module provides a basic, full-text search mechanism. Drupal search is free, open source, and requires very little configuration.

Unfortunately, this built-in search mechanism comes with drawbacks:

- Search is only full-text, with no ability to filter or reduce results out of the box.
- The search system relies heavily on the ability of the underlying database to perform search queries.
- Likewise, search indexes are stored in the database, increasing database size.

Relying on the database for search has serious performance implications. Each search query becomes a unique database query. Each search query now competes with every other database query needed to retrieve content, and render your Drupal site. Aggressive use of Drupal search can even lead to downtime as the database becomes overwhelmed.

## Introducing Apache Solr

Apache Solr is an open source, customizable search system. Like MySQL, Solr is a server application, and can be hosted on commodity hardware such as a Linux-based server. This not only takes the pressure off of the database, we can now host our search data in-house.

Furthermore, Solr is highly customizable, allowing us to tailor not only how results are displayed, but what data on our site is crawled, how, and if any pre- or post-processing must be done. By carefully selecting what is crawled, we can achieve better and more effective results for your site.

Solr is a backend service. It is not intended to offer a user-facing interface to conduct search.

## Lucene and Solr

Apache Solr grew out of an earlier project, Apache Lucene. When reading Solr documentation or installing Solr, you will see this name regularly. Lucene is the core search technology that powers Solr. Lucene can be thought of as a software library, while Solr is a complete application.

## Recap

Drupal offers several different options for implementing search. Apache Solr offers Drupal the ability to delegate search to another application, relieving pressure on the database. Furthermore, as an open source project, it can be hosted in-house. Solr's high customization is thanks to Apache Lucene, the search library which powers Solr.

## Further your understanding

- How can we integrate Solr and Drupal if Solr provides no user-facing UI?

## Additional resources

- [Official Apache Solr site](http://lucene.apache.org/solr/) (lucene.apache.org)
- [Solr Quick Start](http://lucene.apache.org/solr/guide/solr-tutorial.html) (lucene.apache.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Plan a Solr Installation](/tutorial/plan-solr-installation?p=2815)

Clear History

Ask Drupalize.Me AI

close