---
title: "Overview: Benchmarking and Performance Budgets"
url: "https://drupalize.me/tutorial/overview-benchmarking-and-performance-budgets?p=3091"
guide: "[[drupal-site-administration]]"
---

# Overview: Benchmarking and Performance Budgets

## Content

Sites evolve over time. We're constantly adding and removing modules, modifying content, authoring custom plugins, and changing design elements. All of these changes impact our application's performance -- some more so than others. But if you're not measuring it, you can't know when your site inadvertently gets slower or by how much.

If you are responsible for a site's performance, it might be good to look into benchmarking it and establishing a performance budget early on, then monitor it on an ongoing basis. Many tools, paid and free, allow measuring key web performance indicators and backend code and server performance.

One-time measurements can be useful for immediate debugging, or when figuring out if that big new feature is going to have a negative impact on performance. But for long-term projects, it's helpful to have known baseline values and an established performance budget to see whether your performance improves or declines over time with every new feature.

Establishing the baseline (performance budget) and comparing future measurements is called *site performance benchmarking*.

In this tutorial, we'll:

- Learn the basics concepts of benchmarking
- Learn a benchmarking process and best practices
- List some commonly used tools for benchmarking Drupal

By the end of this tutorial, you should understand the concept of a performance budget, know when to benchmark your site, and list some tools available to help.

## Goal

Introduce performance budget and benchmarking concepts, processes, and tools to Drupal developers.

## Prerequisites

- [Analyze Drupal Site Performance with WebPageTest](https://drupalize.me/tutorial/analyze-drupal-site-performance-webpagetest)

## Performance budget

We often set budgets related to spending money. Essentially saying, "Given my current inputs, goals, and requirements, the most I can spend on things in this category is $X." Sometimes you might move money from one pool to another. But you can't spend beyond your total. The concept is the same when budgeting for your web application's performance.

A performance budget sets limits for specific performance metrics of the site: time to interactive, overall page load time, first contentful paint, max time per database query, max POST request size, etc., as well as for a combination of metrics that set thresholds measured over time. Then we establish a practice of only "spending" within that budget.

### What should you set your budget to?

Depending on your business goals and needs for the audience of your site, certain metrics may be more important than others. For instance, if your site is promoting a photography studio, setting too-strict image size limits may affect the needs of your audience to examine high-resolution images. In this case, other functionality may be reduced to stay within a budget - like only light-weight JavaScript libraries can be used, no third-party libraries, and a limited number of externally hosted assets and fonts. No strict guidelines dictate which metric should or shouldn’t be part of your budget.

An effective way to stick to the budget is to set measurable and reachable goals upfront. Analyses of the competitive sites in your industry can help draw some inspiration for the metrics and help understand where your site stands against its peers. The process of continuous measurement of the performance characteristics of your site and comparing them to the baseline budget is called *benchmarking*.

## Overview of benchmarking

Benchmarking is the process of comparing key metrics over time. This can be done on the same site, or across the competition. Periodic (but regular) site benchmarking provides an insight into how new features affect application performance. Comparative benchmarking allows insights into your business competition and understanding of your site’s place among its peers.

To be effective, you need to focus on metrics and measure them over time, either against your site or against your site and its competition. Different performance measurement tools gather different metrics.

For *front-end performance benchmarking*, and *comparative benchmarking*, we recommend starting with the metrics recognized by Google since they influence SEO and your site’s placement in the search results. Those metrics are called Core Web Vitals and include Largest Contentful Paint (LCP), Cumulative Layout Shift (CLS), First Input Delay (FID), Time to Interactive (TTI), and Total Blocking Time (TBT). To learn more about these metrics please refer to [Analyze Drupal Site Performance with WebPageTest](https://drupalize.me/tutorial/analyze-drupal-site-performance-webpagetest).

These metrics are universal and can be measured on the fly against any site without access to its code or server environment.

*backend performance benchmarking* is typically done during developing new features or debugging if your site monitoring tools indicate slow requests or queries.

For internal benchmarking during the process of new feature development, you may want to benchmark the backend parameters of the site instead of the front-end performance. Those parameters reflect how well your code performs under load and may include the execution time of the PHP methods, the request processing time, the number of slow queries, and their execution time.

In addition to common Core Web Vitals, you can establish your own site-specific metrics where it makes sense. For example, if a main feature of your site is search, you might want to consider a metric related to how quickly search queries are handled. If your application interacts with other third party systems you may want to measure the performance of those interactions.

## Benchmarking process

Regardless of the type of benchmarking, the process starts with establishing a performance budget and a baseline. If you are at the beginning of development and have an established performance budget, you may use the required values as your initial benchmarks.

If you don’t have a set value yet and are planning to benchmark only against your site, an excellent place to start could be checking measurements against the default Drupal installation with the demo theme and demo content. For example, you can install the Umami installation profile and use it as a base. Remember, if you don't have something to compare your measurement to, all you have is a number.

Suppose you already have a site and are planning to develop significant new features. In that case, we recommend starting by measuring Core Web Vitals and backend performance before the development cycle and repeating the process after each deployment to monitor improvements or losses over time.

For comparative benchmarking, you need to find a site or sites that will act as benchmarks. It may be sites in the same industry or sites of similar size. Various databases show statistics for site speed and performance statistics for reference. [Refer to this article as a starting point for site speed stats](https://www.websitebuilderexpert.com/building-websites/website-load-time-statistics/).

Once you choose the benchmark site, run the performance tests against it and your application. It’s important to compare a select amount of similar pages with similar content, variety of web assets, and amount of DOM nodes. Development tools in the browser of your choice can provide insights into DOM elements and page composition; the network tab will allow insights into the number of requests on the page. Use this data to choose equivalent pages from your site and benchmark site.

Run performance measurements across multiple browsers and devices to ensure complete coverage and a well-rounded picture of your user’s experience. For bigger applications with fluctuating traffic, it might be beneficial to set up periodic background tests. These tests will help you understand how your site performs throughout the day and how traffic and user patterns affect the performance.

## Benchmarking tools

Benchmarking tools allow performing the benchmarking processes manually or automatically on a schedule. Some tools often used with Drupal sites are listed below:

- **Apache Bench (ab)**: is a tool for benchmarking your Apache Hypertext Transfer Protocol (HTTP) server. It is designed to give you an impression of how your current Apache installation performs. This tool shows you how many requests per second your Apache installation can serve. While the tool was originally designed to benchmark Apache it can be used with nginx or any other HTTP server.
- **Siege**: is an HTTP load testing and benchmarking utility. It was designed to let web developers measure their code under load to see how it will stand up to web traffic. Siege supports basic authentication, cookies, HTTP, HTTPS, and FTP protocols. It lets its user hit a server with a configurable number of simulated clients.
- **Apache JMeter**: is open-source software designed to load test functional behavior and measure performance. JMeter can be scripted using JMX files (which can also be used with some cloud based tools) and simulate more complex user interactions including navigating among pages.
- **Blackfire.io**: Cloud-based SaaS tool that allows monitoring, profiling, and testing. Commonly used with Drupal.
- **New Relic**: Cloud-based SaaS tool that allows you to set up ongoing site monitoring and measuring of your application's performance. Includes ability to monitor Core Web Vitals, and server load parameters like CPU load, Disk Usage, etc.

The tools we mentioned are just a tiny fraction of a wide variety of free and paid tools, services, and applications available for developers on the route to performance optimization. These are ones we've personally used and had success with.

## Recap

By prioritizing performance and making it part of your development workflow and process, you can improve the UX of your web application and ensure its success and competitive advantage. Using a performance budget requires establishing a baseline, and maximum allowed values, specific to your application and business goals. Then continuously measuring key metrics to ensure they stay within the defined budget.

Benchmarking measures 1 or multiple front-end and backend performance metrics and compares them to the baseline or the competition sites. Various tools and services provide immediate or periodic measurements of the performance budget metrics and guide development and optimization efforts.

## Further your understanding

- What are some of the things that are unique to your web application that would be good to benchmark?
- What backend performance metrics might be useful to measure? Why?
- When would you focus on backend performance vs. front-end performance?

## Additional resources

- [Performance budgets](https://developer.mozilla.org/en-US/docs/Web/Performance/Performance_budgets) (mozilla.org)
- [Article about web page speed statistics](https://www.websitebuilderexpert.com/building-websites/website-load-time-statistics/) (websitebuilderexpert.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[What Is Server Scaling?](/tutorial/what-server-scaling?p=3091)

Next
[Profile a Drupal Site with Apache Bench](/tutorial/profile-drupal-site-apache-bench?p=3091)

Clear History

Ask Drupalize.Me AI

close