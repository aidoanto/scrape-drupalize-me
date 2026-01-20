---
title: "Overview: Content Delivery Networks (CDNs) and Drupal"
url: "https://drupalize.me/tutorial/overview-content-delivery-networks-cdns-and-drupal?p=3091"
guide: "[[drupal-site-administration]]"
order: 45
---

# Overview: Content Delivery Networks (CDNs) and Drupal

## Content

Content Delivery Networks (CDNs) play an important role in making a Drupal-powered site fast and secure. The distributed nature of CDNs allows serving web assets such as HTML files, JavaScript, CSS, and media assets through servers located in close geographical proximity to the users, thereby reducing the physical distance data has to travel between the user and the server, and improving performance.

In addition to providing a performance boost, CDNs may also act as a firewall and protect sites from common attacks such as DDoS. The popularity of CDNs has been growing over the past few years, and integrating with them has also gotten easier. Most Drupal web operation platforms, such as Acquia and Pantheon, offer integrations with CDNs out-of-the-box. Even if your hosting platform doesn't provide a CDN, you can always set up your Drupal site to use one.

In this tutorial we'll:

- Define what a CDN is and what it can offer for your site
- Learn about popular CDNs used with Drupal sites
- Review some contributed modules that you can use to help integrate your Drupal site with a CDN

By the end of this tutorial you should be able to define what a CDN is, list CDNs with Drupal integrations, and describe the steps you will need to take to set up your site to work with a CDN.

## Goal

Introduce Drupal developers to the concept of Content Delivery Networks and the role they play in hosting secure and performant Drupal sites.

## Prerequisites

- None

## What is a CDN and why use one?

A Content Delivery Network (CDN) is a geographically distributed network of servers distributing content to users with minimal delay through strategically located Points of Presence (PoPs) geographically close to users' locations. CDNs serve the data and provide a caching layer, accelerating webpage performance. Depending on the configuration, CDNs also act as a web firewall and remedy some site security risks and attack vectors.

Without a CDN, the site origin (Drupal in this case) handles the users' requests. Static files and media assets are downloaded to the user's browser and stored locally. Subsequent requests by the same user will utilize local assets instead of downloading them from the origin. A different user, even from a similar location to the previous user, won't be able to take advantage of preloaded assets and will have to download their own copy of the static files for the page.

CDNs are situated between the user's browser and the Drupal origin server, and store static web assets in a data center located close to the user when the original request is made. The next time another user makes the request, the static files are provided via the CDN, and the user can take advantage of the cache and accelerated loading times.

CDNs are essential for serving performant global sites with a large distributed user base. CDNs minimize latency and reduce bandwidth costs. They also increase content availability and redundancy by decreasing hardware load and mitigating traffic spikes and DDoS attacks.

## Popular CDNs and their contributed modules

Some web operations platforms like Acquia and Pantheon provide CDN integrations and Varnish implementations. To learn more about the specifics of caching on Acquia and Pantheon, refer to [Set Up Advanced Caching on Acquia Cloud Hosting](https://drupalize.me/tutorial/set-advanced-caching-acquia-cloud-hosting) and [Set Up Advanced Caching on Pantheon Hosting](https://drupalize.me/tutorial/set-advanced-caching-pantheon-hosting) tutorials. If your hosting provider already provides integrations with a specific CDN we recommend you use that one.

If you host on a different platform, you may want to consider one of the these popular CDNs that have Drupal API integrations available via contributed modules. The Drupal integration can make it easier to set up initially. It will also help with purging cached data from the CDN when content is updated in Drupal, ensuring the CDN isn't serving stale content to users.

### Fastly

[Fastly](https://www.fastly.com/) is a real-time CDN that improves the performance of sites, mobile applications, and APIs. The service utilizes a highly customized and distributed version of Varnish, an open-source web accelerator, enabling you to control configuration settings and implement changes in real-time.

Fastly released an out-of-the-box integration module for Drupal, enabling users to easily configure and manage their Fastly service from within their Drupal dashboard.

The [Fastly](https://www.drupal.org/project/fastly) module can be downloaded and installed with Composer. The module comes with an existing configuration. To take advantage of it, you need to have a Fastly account and install the module.

### CloudFlare

[CloudFlare](https://www.cloudflare.com/) (<https://www.cloudflare.com/>) is a free reverse proxy, firewall, and global CDN that can be implemented without installing server software or hardware. In addition, CloudFlare helps protect sites from malicious activity, including comment spam, email harvesting, SQL injection, cross-site scripting, and DDoS attacks.

The [CloudFlare](https://www.drupal.org/project/cloudflare) module provides cache clearing by path and tag (available with the enterprise version of CloudFlare). The CloudFlare module requires the [Purge](https://www.drupal.org/project/purge) module and CloudFlare API credentials. To read full installation instructions, refer to the [CloudFlare Getting started guide](https://github.com/d8-contrib-modules/cloudflare/blob/8.x-1.x/docs/freetier_setup.md) for the free tier.

## Required setup to use a CDN

CDNs integrate with your site at the DNS level. The exact steps vary depending on the CDN of your choice and its interface. You need to make an account on the CDN platform of your choice. Through the CDN dashboard, point CDN to your hosting server and point Name Servers at your Domain Registrar to the CDN servers. This way, the domain name will point to the CDN, and the CDN will point to the hosting provider for your site. Refer to the setup guidelines of your CDN of choice after creating an account on their platform.

## Recap

Content delivery networks (CDNs) allow static assets to be cached and delivered through a distributed network of PoPs. CDNs can help manage traffic spikes and improve the performance and security of a site. There are CDNs with existing Drupal integrations that make them easy to set up and use with Drupal powered sites.

## Further your understanding

- We mentioned static assets being served by a CDN. Can a CDN serve dynamic content? Why? Why not?
- Describe what a PoP is and how it helps to make a site more performant.

## Additional resources

- [Dries Buytaert’s blog post on “Making Drupal 8 fly”](https://dri.es/making-drupal-8-fly) (dri.es)
- [Fastly module](https://www.drupal.org/project/fastly) (Drupal.org)
- [CloudFlare module](https://www.drupal.org/project/cloudflare) (Drupal.org)
- [Fastly CDN](https://www.fastly.com/) (fastly.com)
- [CloudFlare CDN](https://www.cloudflare.com/) (cloudflare.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Set Up Advanced Caching on Acquia Cloud Hosting](/tutorial/set-advanced-caching-acquia-cloud-hosting?p=3091)

Next
[What Is Server Scaling?](/tutorial/what-server-scaling?p=3091)

Clear History

Ask Drupalize.Me AI

close