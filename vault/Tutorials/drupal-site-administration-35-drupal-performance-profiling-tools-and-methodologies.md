---
title: "Drupal Performance Profiling: Tools and Methodologies"
url: "https://drupalize.me/tutorial/drupal-performance-profiling-tools-and-methodologies?p=3091"
guide: "[[drupal-site-administration]]"
order: 35
---

# Drupal Performance Profiling: Tools and Methodologies

## Content

Performance profiling allows you to see an overview of how your Drupal application stacks up against your users' needs and business requirements. A good profile will help you understand where the performance bottlenecks are and where you should focus your efforts in order to achieve the best results when optimizing your application.

There are many profiling tools available to help you analyze your Drupal site's performance. Some are free -- like the browser’s built-in development tools, the Lighthouse Chrome extension, and XHProf. Some are paid -- like New Relic, Blackfire, and other profiling SaaS solutions.

In this tutorial we'll:

- Outline the general concepts and goals of performance profiling
- List some available profiling tools and their features

By the end of this tutorial you should be able to describe what performance profiling is, and list the tools commonly used to establish a performance profile for a Drupal site.

## Goal

Define what performance profiling is and list some commonly used tools for profiling Drupal applications.

## Prerequisites

- [What Are Core Web Vitals?](https://drupalize.me/tutorial/what-are-core-web-vitals)

## What is performance profiling?

Performance profiling is the process of measuring various metrics that impact the overall performance (perceived and real) when Drupal serves a request. Or in plain English -- when a user goes to your site, how fast does the page load? Performance profiling lets you identify slow operations (often called bottlenecks) and begin to optimize them for better performance.

The goal of performance profiling is to ensure that you're focusing your development effort on making the changes that are going to have the biggest impact on the speed at which your application can serve pages. It eliminates the need to guess, cross your fingers, and hope you're fixing the right things.

Profiling is an essential step in an application's life cycle. It can be done before the site launches, and again after adding new features. Web profiling is crucial because every Drupal instance is unique, and you cannot predict the outcome of all the modules, libraries, and code you add to your site. It is also critical for applications with a substantial legacy codebase and features. These features are often fragile and contribute to performance loss.

The profiling process tries to answer 3 questions:

- Which sections of the site are slow?
- What is slowing these sections down?
- How does it slow them down?

Profiling tools and browser extensions allow you to analyze the site: both page by page and as a whole. An advanced setup and configuration for profiling will enable us to connect the performance metrics to events such as deployments, background processes like imports, migrations, cron runs, and costly user interactions such as rendering an extensive view, using a search, and bulk saving content. These all help to further narrow the focus of our optimization efforts, and quickly identify any regressions.

## The performance profiling process

- Figure out *what* is slow
- Figure out *why* it is slow
- Make adjustments
- Test again and compare

At the beginning of the profiling process, you need to identify if the performance loss is happening throughout the entire site or on specific pages. Performance monitors like New Relic or Blackfire allow you to gather site performance data over time and identify a performance baseline. Then you can see when a page deviates from that baseline.

If your entire application is slow, start by identifying a couple of crucial representative pages to narrow down your focus and dive deeper.

If you recognize some specific pages that are slower than others, focus on them.

Once you've narrowed your focus to a specific page, choose one of the free or paid tools to run in-depth performance tests. Measure key performance indicators, and web vitals, with browser development tools, Lighthouse (that comes with Chrome), WebPageTest, or any paid profiling tool. Record, and review, the rendering timeline. Most of these tools provide a list of recommendations for performance improvement and help identify the bottlenecks. These recommendations are good starting points for performance improvement work.

After you have identified the bottlenecks and know *what* is slowing your site down (slow queries, external libraries, non-optimized images, etc.), you can see *how* it slows the site down. Find the affected part of the call stack. Start from the request to the server and go to a fully rendered and interactive page.

Depending on the part of the rendering process where the bottleneck occurs, you may go with different ways of remediation. Then, after adjustments, you can rerun tests and compare the results with the previous run.

## Performance profiling tools commonly used with Drupal

Various performance profiling and monitoring tools are available to help you measure the performance of your Drupal application. In this section we will point out some of them, but we encourage you to explore additional options on your own.

Keep in mind that profiling is both an ongoing task where you're constantly monitoring for deviations, and the last step of big feature development for certain types of code. Profiling tools can be divided into 2 categories: the ongoing monitoring tools that help to measure metrics over time, and the one-time quick scan tools that help with debugging and isolating particular performance related aspects.

Here are some of the tools we use:

### Browser development tools and extensions

Browser development tools are free and provide performance insights in every browser. They work well for quick check-in tasks before deep dives. The downside is a lack of long-term recording of results functionality, scheduling of tests, and advanced configuration options.

Common browser development tools include:

- The developer tools built into all major browsers for profiling networks requests and core web vitals
- Lighthouse or WebPageSpeed Test

### XHProf

[XHProf](https://www.php.net/manual/en/intro.xhprof.php) is a profiling tool for PHP code. XHProf tracks the amount of memory and execution time and call stack order for each function call. It allows you to spot bottlenecks in the code and identify optimization pathways. For example, XHProf can help identify which functions are taking the longest to execute. Start your optimization with that area.

XHProf is a PHP extension that can be installed on any of your environments, including your local, and has a Drupal [contributed module](https://www.drupal.org/project/xhprof). XHProf requires additional setup and configuration on your site environments including local, dev, test and production.

Once enabled, XHProf records a snapshot of each request, and provides a UI for analyzing the recorded data.

Many commonly used Drupal development environments like DDEV, Lando, and MAMP have XHProf support built in.

### Xdebug

[Xdebug](https://xdebug.org/) is a debugging and profiling tool for PHP applications. It allows you to analyze the performance of the Drupal application and find bottlenecks.

Xdebug is a PHP extension that can be installed on any environment but is most commonly used in a local environment through integration with your IDE or code editor of choice. While effective for local debugging, it may not be an ideal solution for production site profiling.

Once enabled, Xdebug's profiler records a snapshot of each request in CacheGrind format. The recorded data can be viewed using any CacheGrind compatible UI. The phpStorm IDE also has [built in support for displaying xdebug profiling data](https://www.jetbrains.com/help/phpstorm/profiling-with-xdebug.html#enable-profiling-with-xdebug).

Many commonly used Drupal development environments like DDEV, Lando, and MAMP have Xdebug support built in.

**Note:** Xdebug and XHProf expose much of the same data, use whichever works for you. If you're not sure, we recommend starting with XHProf.

### New Relic

[New Relic](https://newrelic.com/) is a paid SaaS profiling application. Its use is nearly ubiquitous among Drupal hosting providers.

The New Relic platform lets you gain insights into the entire web stack. It also allows correlating infrastructure health with performance issues. New Relic provides a live view of the network, infrastructure, applications, and end-user experience. New Relic exposes slow queries, function calls, and blocking resources. It also provides integrations with various platforms and notifications systems and reveals events for monitoring and subscriptions. It allows for recording your application performance over time.

We recommend checking to see if your hosting provider has New Relic support built-in, and if so, it's worthwhile to learn how to use the tool. The New Relic agent software can also be installed on nearly any platform if you're self-hosting.

### Blackfire

[Blackfire](https://www.blackfire.io/) is another commonly used SaaS solution for monitoring PHP based web applications like Drupal.

Blackfire allows you to implement a complete performance management strategy with monitoring, testing, and profiling. It observes your application and notifies the team if something goes wrong. It also generates in-depth reports for application profiling.

Blackfire Profiler is a tool that measures how your code consumes resources at run-time. It enables to find performance bottlenecks and understand the code's behavior. Paired with the visualization tools, you can get a complete picture of your call stack.

Both New Relic and Blackire are especially useful for monitoring and observing the performance of an application over time. And for profiling Drupal as just one part of a larger software stack that includes hardware, a web server, database servers, cache layers, PHP, and more.

## Recap

Performance profiling is a process of identifying performance bottlenecks in your web application. It answers the questions of *what* slows down your application, and *why* it slows the application down. This process helps to understand how to build performance optimization strategies and where to focus your efforts. Various free and paid profiling tools and services are available to help with the process.

## Further your understanding

- Use the browser based performance profiling tools to analyze your site's front page.
- Install XHProf on your localhost and try analyzing some PHP code.

## Additional resources

- [Profiling documentation on drupal.org](https://www.drupal.org/docs/develop/profiling-drupal) (Drupal.org)
- [XHProf official documentation](https://github.com/tideways/php-xhprof-extension) (github.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Boost Drupal Performance with Contributed Modules](/tutorial/boost-drupal-performance-contributed-modules?p=3091)

Next
[What Are Core Web Vitals?](/tutorial/what-are-core-web-vitals?p=3091)

Clear History

Ask Drupalize.Me AI

close