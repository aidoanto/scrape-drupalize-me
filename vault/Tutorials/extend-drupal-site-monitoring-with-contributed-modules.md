---
title: "Extend Drupal Site Monitoring with Contributed Modules"
url: "https://drupalize.me/tutorial/extend-drupal-site-monitoring-contributed-modules?p=3091"
guide: "[[drupal-site-administration]]"
---

# Extend Drupal Site Monitoring with Contributed Modules

## Content

There's no magical set of *right* tools to use to monitor a Drupal site's performance and health. While thinking about performance monitoring, you need to optimize your approach depending on the number of applications you manage, their complexity, business needs, and the skill-set of your team. Based on these factors, you may choose to use one of the core or contributed modules, go with third-party solutions and services, or some combination of both.

Drupal core comes with a couple of modules that allow you to monitor the health and performance of the site including Syslog, Database Logging, and the status reports provided by the System module. There are also numerous community-contributed modules, a sampling of which we'll cover here.

In this tutorial, we'll:

- List some contributed modules that are commonly used for monitoring a Drupal site
- Provide an overview of what each module does

By the end of this tutorial you should be able to list a few contributed modules that might be useful for monitoring your Drupal application and define what each one does.

## Goal

Introduce some common Drupal modules for monitoring performance and site health.

## Prerequisites

- None

## Overview of Drupal monitoring modules

The Drupal community contributed various modules that help monitor the performance and health of Drupal sites. In this tutorial, we’ll cover some of them that we've had experience with, and we encourage you to explore more contributed modules on your own.

The benefits of using modules to perform these monitoring tasks are the ease of setup and maintenance. You already have to keep your site up-to-date so this adds very little additional overhead. There's generally no additional cost associated with them either. The downside of modules is the potential scalability of the solution, especially if you have many sites to monitor. Additionally, they may lack integration with other third party systems like SMS alerts.

These modules allow you to monitor PHP performance, web request time, site logs and errors, uptime of the site, Drupal health metrics such as security updates and status report.

## Drupal Remote Dashboard

[Drupal Remote Dashboard](https://www.drupal.org/project/drd) is a duo of modules. This module allows monitoring Drupal's status report metric, uptime, and security updates for multiple Drupal applications from one dashboard. It also allows performing operations such as cleaning caches, running cron, installing and uninstalling modules from the dashboard.

To set up monitoring, you need 2 pieces:

- The dashboard site. You can use any Drupal application or build one specifically for use as a dashboard
- The Drupal Remote Dashboard Agent module installed on all the sites you want to monitor

The Drupal Remote Dashboard Agent monitors the site and sends periodic reports to the Drupal Remote Dashboard hosting site. Drupal Remote Dashboard provides an overview of the aggregated information.

Drupal Remote Dashboard is a scalable solution and can provide insights into the statuses of an unlimited number of Drupal applications. It also has no dependency on third party systems, which can be a project requirement, especially for data privacy purposes.

You can read more about the project, and how to start with it, in the [Drupal Remote Dashboard documentation](https://www.drupal.org/docs/contributed-modules/drupal-remote-dashboard).

## Monolog

[Monolog](https://www.drupal.org/project/monolog) is a contributed module that integrates Drupal's built in logging with the open-source logging library of the same name.

[The Monolog library](https://github.com/Seldaek/monolog) allows monitoring PHP and server errors, warnings and notices. Logs can be written to files, sockets, and databases. The library integrates with various mail handlers to allow for notifications.

Monolog library also allows for integration with various logging services, including New Relic, Sentry, and Loggy. It is supported by many PHP projects other than Drupal. So it may be a familiar option to developers who have experience using Monolog elsewhere.

The Drupal module provides a configurable interface for logging levels and handlers.

## Production Check and Production Monitor

The [Production Check and Production Monitor modules](https://www.drupal.org/project/prod_check) are an evolution of [Performance Project](https://www.drupal.org/project/performance) that was once part of the Devel ecosystem and was removed from it.

Before launch, there are checks you need to perform to ensure your site is ready for being live and follows standard best practices.

The Production Check module performs production readiness checks on your Drupal application. The Production Monitor module monitors the status of these checks and allows you to gather information from multiple sites into one monitoring dashboard.

The modules are independent. If you have only one site to monitor, you may not need the Production Monitor module.

## Raven

The [Raven module](https://www.drupal.org/project/raven) provides integration with [Sentry](https://sentry.io/welcome/), an open-source application monitoring platform.

Sentry monitors can capture Drupal log messages, fatal, JavaScript, and server errors. It also allows monitoring performance and provides tracing mechanisms to help identify poor-performing parts of applications such as costly API calls and slow database queries.

Raven provides Drupal configuration options for types of errors captured by Sentry instances. To use Raven, you’ll need to connect to a Sentry service. You can use either a hosted Sentry solution or a self-hosted Sentry Docker image.

## New Relic

[New Relic (newrelic.com)](https://newrelic.com/) is a third-party monitoring service for site performance. New Relic allows you to monitor, debug and improve performance for the entire stack of your Drupal application.

New Relic includes common metrics like response time, uptime status, and number of requests. It allows you to identify slow routes; for example, you can analyze Drupal views routes. One of the most common use cases is an uptime monitor that can be used to send notifications to various channels if the application is offline. Another one is a deployment monitor. New Relic can track deployments and send notifications every time the deployment is finished. The developer can then analyze deployment throughput such as server stats, memory usage, and slow queries.

The [New Relic module](https://www.drupal.org/project/new_relic_rpm), while not required to use New Relic, enhances your site’s integration with New Relic and allows deeper visibility into the Drupal hooks system.

## Recap

The Drupal community has contributed a variety of modules that help with monitoring a site. These modules provide mechanisms for advanced error capturing, notification and alert generation, automation of security updates, and site status overview. Some modules are targeted for one site, while others allow monitoring and logging of information from an unlimited number of applications.

The best monitoring tool is the one that surfaces the data in a way that you will use. Logging errors and other performance-related metrics won't be helpful at all if you're not reviewing the logs and looking for anomalies.

## Further your understanding

- Choose one of the described modules, read through their installation and configuration instructions, and try setting it up for your project.
- Read the Sentry documentation.
- Read the New Relic documentation.

## Additional resources

- [Sentry](https://sentry.io/welcome/) (sentry.io)
- [New Relic](https://newrelic.com/) (newrelic.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Debug Drupal Cache Misses and Low Hit Rates](/tutorial/debug-drupal-cache-misses-and-low-hit-rates?p=3091)

Next
[Set Up Advanced Caching on Pantheon Hosting](/tutorial/set-advanced-caching-pantheon-hosting?p=3091)

Clear History

Ask Drupalize.Me AI

close