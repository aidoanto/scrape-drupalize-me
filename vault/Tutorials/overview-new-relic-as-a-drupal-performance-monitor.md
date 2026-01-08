---
title: "Overview: New Relic as a Drupal Performance Monitor"
url: "https://drupalize.me/tutorial/overview-new-relic-drupal-performance-monitor?p=3091"
guide: "[[drupal-site-administration]]"
---

# Overview: New Relic as a Drupal Performance Monitor

## Content

[New Relic](https://newrelic.com/) is a monitoring service that provides insights into your application stack from front-end performance to the server and infrastructure metrics. New Relic uses a combination of aggregating server logs, and pre-built (or custom) *monitors* to track the metrics that are most important to your application. The collected data can be organized into custom dashboards, and alerts can be set up and issued per customizable conditions.

In this tutorial, we'll:

- Learn about different New Relic modules and their purpose
- Review some default dashboard components and reports
- Discuss how to use the information in New Relic to understand the health of your Drupal application

By the end of this tutorial, you should understand the basics of using New Relic and the insights it offers to monitor and improve the performance of your Drupal site.

## Goal

Demonstrate how to use the New Relic service as a Drupal performance monitor.

## Prerequisites

- None

## Why New Relic?

Other application monitoring platforms provide the same feature set as New Relic. Monitoring is a big, and competitive, business. We've chosen to cover New Relic here because it's the one we've seen used most often in conjunction with Drupal. Hosting platforms like Pantheon and Acquia include it as part of their offerings. But the concept of using a third party tool to monitor key metrics and provide real-time notifications when those metrics exceed defined thresholds remains the same regardless of the tool you choose to use.

We recommend starting out by using whatever tools are available with your existing hosting platform. If there aren't any, adding New Relic is a solid choice.

## Overview of New Relic

New Relic (<https://newrelic.com/>) is mainly known as an Application Performance Monitor (APM) due to its most popular module. But the New Relic application is more than an APM module. It consists of multiple modules such as a Customer Experience cluster of modules (mobile, browser, and synthetics modules), Application Performance modules (APM and infrastructure monitors), and the Alerts and AI module.

The Customer Experience cluster consists of the following modules:

- **Browser**: Monitors the front-end user experience of your application, including [Core Web Vitals](https://drupalize.me/tutorial/what-are-core-web-vitals).
- **Mobile**: Monitors native or hybrid applications
- **Synthetics**: A testing module that allows performing tests under different conditions, times, and locations to ensure that the user can accomplish a goal or perform micro-transaction. For example; ping the front page to ensure the site is up.

The Application Performance cluster consists of the following modules:

- **APM**: Application performance monitoring. Monitors the back-end of your Drupal application including databases, external calls, and PHP code.
- **Infrastructure**: Monitors your infrastructure: CPU, memory, and processes running at any given time. It’s focused on the server hardware and any infrastructure plugins.

The **Alerts and AI** module processes the information from all the modules and integrates it with New Relic's alerts and reports. It allows analyzing issues and activity, setting up anomaly detection policies and alerts, and insights into error rates and detection gaps.

## Setting up New Relic

If you host on a platform that supports New Relic integration, such as Pantheon and Acquia, then the New Relic agent will be pre-installed on your server environment. Follow the platform's documentation to activate New Relic and get access to the monitors.

If you host on an self-managed platform, you may need to set up an agent yourself. Follow this [quick installation guide](https://docs.newrelic.com/docs/new-relic-solutions/get-started/quick-launch-guide) to get started.

In this tutorial, we assume that you have the agent set up for your application and can access the New Relic dashboard and reports.

## Overview of the APM module

Select an application link inside the New Relic dashboard. You’ll land inside the APM dashboard. The landing page of the APM dashboard gives a one-stop overview of the application's health.

The chart in the top left corner shows the average web transaction time - the average time the service spends processing web requests.

Image

![Screenshot of web transaction time report](/sites/default/files/styles/max_800w/public/tutorials/images/web_transaction_time.png?itok=FTDdGIy-)

If you see transactions (usually representative of a user viewing a page on your site) that take over 200ms, they may need further investigation. Transactions that took longer than two seconds are traced so you can dive deeper into what series of events resulted in a slow transaction. The top five slowest transactions are logged in the report at the bottom of the page. The sidebar menu can also dive into detailed information about the transactions.

Image

![Screenshot of 5 slowest transactions report](/sites/default/files/styles/max_800w/public/tutorials/images/slowest_transactions_report.png?itok=CdZ9-e1p)

Next to the transaction time report is the [Apdex score](https://www.apdex.org/) report. Apdex is an industry standard to measure a user's satisfaction with the response time of web applications and services. It's represented as a score from 0-1. The closer your score is to 1, the better your app performs. The default value for a satisfactory experience is 0.5 seconds. You can set a different target for your app under the settings section.

Image

![Screenshot of Apdex score](/sites/default/files/styles/max_800w/public/tutorials/images/apdex_score.png?itok=WzfQSWT_)

The throughput report shows how many requests the service processes per minute. This report is helpful to see the busiest service in your infrastructure.

Image

![Screenshot of web throughput](/sites/default/files/styles/max_800w/public/tutorials/images/web_throughput.png?itok=ZF3fh5v_)

The final report on this screen is an error rate. It’s the percentage of transactions that result in an error during a particular time range. New Relic sends all errors to the *error inbox* found under the *Triage* section of the menu so that developers can proactively address them and make changes to the application before the user experience degrades too much.

### Overview of transactions reports

One of the most used reports is the transactions report. Transactions are a way to break down the Drupal application into a series of requests. When a user lands on a page that sends one or more requests to the server, it results in transactions. The *Transactions* view shows which piece of code (for example, Drupal controller) is responsible for the transaction and which part of the stack (PHP, MySQL, and external cache service) takes what time in the particular transaction.

You should see a detailed transaction report if you select the *Transactions* item in the sidebar menu and then select an individual transaction.

Image

![Screenshot of detailed transaction report](/sites/default/files/styles/max_800w/public/tutorials/images/detailed_transaction_report.png?itok=OSMPKt-f)

Each transaction gets an Apdex score, and you can also see the historical performance for it to identify any recent changes.

Traces show detailed information for slow transactions. Transactions with an Apdex score of 0.4 or below receive a trace. Database queries are helpful in identifying slow queries in your application. Typically, those queries come from Views blocks and pages with many joins. This information can help you figure out where to start putting effort when trying to improve the performance of your site.

### Overview of the application services monitors

New Relic exposes the details of services and components used in the application’s infrastructure. To view the overview of all services, visit the *Service Map* section of the menu. It shows a map diagram of the services and their connections.

To see external services, navigate to the *External Services* section of the navigation. This section shows all called and consumed by the application external services, their throughput, error rate, and response time.

Usually your hosting platform will have configured this for you in New Relic, but if necessary you can add your own service monitors.

### Drupal-specific monitors and features

A New Relic APM agent installed for the Drupal application captures metrics specific to Drupal sites. When these metrics are collected, a *Drupal* tab appears in the New Relic user interface.

The PHP agent collects metrics for the following:

- **Modules**: Indicates time spent within each Drupal module.
- **Hooks**: Time spent within each Drupal hook.
- **Views**: These metrics show time spent within a view's `view::execute` method.

These metrics allow seeing the slowest parts of your application code at a glance. They help to identify views with slow queries or performance bottlenecks in your custom code.

### Triage tools

New Relic comes with triage tools that aid in debugging and error logging. The reports are under the *Triage* section of the sidebar interface. This section contains access to the error inbox and the logs view.

Error logs view allows setting custom time ranges for errors and seeing error details, including error URL and type, message, count, and the time frame when the error occurred. If you dive deeper into the error, you should see the stack trace of the error.

## Overview of the Browser module

The browser agent is installed automatically by the APM agent. It doesn’t require any particular setup. If you navigate to the Browser section of the New Relic dashboard, you will see reports related to the front-end performance of your application.

At the top, it has pages with JavaScript error reports, which shows the rate of JavaScript errors over time. This report is followed by Core Web Vitals metrics: Largest Contentful Paint (LCP), First Input Delay (FID), and Cumulative Layout Shift (CLS).

Image

![Screenshot of core web vitals report](/sites/default/files/styles/max_800w/public/tutorials/images/core_web_vitals.png?itok=a0p-sqsX)

The rest of the summary view consists of detailed reports on the Core Web Vitals metrics by device type, URL, and browser.

### Browser module monitors

The browser module comes with analytics monitors that measure user behaviors and allow the isolation of the metric by user agents. Monitors measure page view response time per URL, session traces, AJAX requests, and throughput per browser and device.

The *JS Errors* monitor provides a detailed view of JavaScript errors with traces, URLs, and rates. It also reflects the time frame in which the error first appeared.

## Overview of Synthetics

Synthetic monitoring is a suite of automated, scriptable tools to monitor your Drupal applications. It allows you to proactively measure the uptime of critical pages and simulate user traffic.

Synthetics continually monitors your site to ensure that your content isn’t just available but fully functional.

Synthetic monitoring browser tests send a real, Selenium-powered Google Chrome browser to your site from around the world to ensure that your content is always up.

Synthetics also allows monitoring deployments in build automation and CI/CD pipelines and sending alerts if any issues arise.

If you want to learn advanced Synthetics setup, follow the [Introduction to Synthetics tutorial](https://docs.newrelic.com/docs/synthetics/synthetic-monitoring/getting-started/get-started-synthetic-monitoring/)

## Recap

New Relic is a powerful application reporting and monitoring suite of tools that cover the entire stack of your application, from infrastructure and servers to PHP code, MySQL, and front-end browser user experience.

New Relic comes with a collection of modules covering different parts of the stack. It also provides a variety of ways to customize the monitors, reports, dashboards, and alerts so that you can fine-tune the tools to focus on your business needs and proactively identify issues.

## Further your understanding

- Read the New Relic Synthetics documentation and set up an uptime monitor for your site
- Review the Transactions report for your site. Can you trace where they are coming from? Can you think of ways to optimize the underlying code?
- Go through the next tutorial, [Profile a Drupal Site with New Relic](https://drupalize.me/tutorial/profile-drupal-site-new-relic).

## Additional resources

- [New Relic documentation](https://docs.newrelic.com/) (newrelic.com)
- [New Relic quick installation guide](https://docs.newrelic.com/docs/new-relic-solutions/get-started/quick-launch-guide) (newrelic.com)
- [Introduction to Synthetics tutorial](https://docs.newrelic.com/docs/synthetics/synthetic-monitoring/getting-started/get-started-synthetic-monitoring/) (newrelic.com)
- [Profile a Drupal Site with New Relic](https://drupalize.me/tutorial/profile-drupal-site-new-relic) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Profile a Drupal Site with Apache Bench](/tutorial/profile-drupal-site-apache-bench?p=3091)

Next
[Profile a Drupal Site with New Relic](/tutorial/profile-drupal-site-new-relic?p=3091)

Clear History

Ask Drupalize.Me AI

close