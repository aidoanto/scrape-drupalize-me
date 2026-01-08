---
title: "What Are Core Web Vitals?"
url: "https://drupalize.me/tutorial/what-are-core-web-vitals?p=3091"
guide: "[[drupal-site-administration]]"
---

# What Are Core Web Vitals?

## Content

Over the history of the Internet, the single *Page Speed* metric evolved into various parameters that influence user experience. These metrics are commonly referred to as *Core Web Vitals*. Together, they paint a comprehensive picture of the performance of your site from an end user's perspective. These metrics are considered by Google and other search engines when assigning SEO scores.

Knowing what these metrics are, and what they are intended to measure, is an important part of creating a performance profile for your site. This knowledge can also help you find solutions for common performance issues.

In this tutorial, we'll:

- Define the metrics that make up the *Core Web Vitals*
- Point to additional resources where you can learn more about each metric

By the end of this tutorial, you should know which performance metrics are considered Core Web Vitals and what aspects of site performance they cover.

## Goal

Introduce Core Web Vitals metrics to developers.

## Prerequisites

- None

## Overview of Core Web Vitals metrics

[Core Web Vitals](https://web.dev/vitals/) is an initiative by Google to provide unified guidance for the language we use, and the signals we measure, that are essential to delivering a great user experience on the web. The Core Web Vitals consists of the following:

- **Largest Contentful Paint (LCP)**: Marks the time when the browser paints the largest text or image (generally the thing people came to the page to see). It's a measure of loading performance. This metric is healthy when it’s below 2.5 seconds.
- **Cumulative Layout Shift (CLS)**: Measures the movement of visible elements within the viewport; measures visual stability. This metric is healthy when it’s below 0.1.
- **First Input Delay (FID) or Time to Interactive (TTI)**: The amount of time it takes for the page to become fully interactive; measures interactivity. FID can be measured as part of TBT. A healthy measurement is below 100 milliseconds.
- **Total Blocking Time (TBT)**: Sum of all periods between FCP (First Contentful Paint) and TTI when task length exceeded 50ms, expressed in milliseconds.

To learn more about the Core Web Vitals, [follow this guide](https://product.webpagetest.org/core-web-vitals).

These metrics are not specific to Drupal. But Drupal's performance, caching, and how you author the CSS, HTML and JavaScript in your theme can all impact them.

## Recap

Core Web Vitals are a set of metrics that provide a comprehensive overview of a site's performance and user experience. In effect, they measure what it *feels* like for someone to engage with your application. Scores of Core Web Vitals metrics are known to influence the SEO of your site.

## Further your understanding

- Use the Lighthouse extension in Google Chrome or Webpagetest to scan your site for Core Web Vitals.
- Why was page speed replaced by Core Web Vitals?

## Additional resources

- [Core Web Vitals guide](https://product.webpagetest.org/core-web-vitals) (webpagetest.org)
- [Core Web Vitals overview](https://web.dev/vitals/) (web.dev)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Drupal Performance Profiling: Tools and Methodologies](/tutorial/drupal-performance-profiling-tools-and-methodologies?p=3091)

Next
[Analyze Drupal Site Performance with Lighthouse](/tutorial/analyze-drupal-site-performance-lighthouse?p=3091)

Clear History

Ask Drupalize.Me AI

close