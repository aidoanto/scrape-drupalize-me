---
title: "Access an API from the Browser with Cross-Origin Resource Sharing"
url: "https://drupalize.me/tutorial/access-api-browser-cross-origin-resource-sharing?p=3279"
guide: "[[decoupled-headless-drupal]]"
---

# Access an API from the Browser with Cross-Origin Resource Sharing

## Content

JavaScript applications are the most common type of consumers. They are commonly used to create a website that runs in a web browser. Running decoupled applications in the browser will involve Cross-Origin Resource Sharing (CORS), which requires some setup on the Drupal side in order to work.

In this tutorial we'll:

- Learn about what CORS is and when/why we need to care about it
- Configure Drupal to return an appropriate CORS header, enabling browser-based consumers access to our API

By the end of this tutorial you will have a better understanding of CORS, and how to configure Drupal to serve an API that works with CORS.

## Goal

Configure Drupal to support Cross-Origin Resource Sharing.

## Prerequisites

- None.

## Cross-Origin Resource Sharing (CORS)

When our API supports a consumer that runs in the browser we need to make sure our Drupal back end supports CORS. CORS is a security feature that all browsers implement to ensure access control for cross-origin requests. That means that any front-end application that is not under the same domain as the back-end server will need to go through extra validation. This ensures the *same-origin policy*. According to [the Wikipedia article](https://en.wikipedia.org/wiki/Same-origin_policy):

> In computing, the same-origin policy is an important concept in the web application security model. Under the policy, a web browser permits scripts contained in a first web page to access data in a second web page, but only if both web pages have the same origin. An origin is defined as a combination of URI scheme, hostname, and port number. This policy prevents a malicious script on one page from obtaining access to sensitive data on another web page through that page's Document Object Model.

This policy for web browsers is necessary because they make many requests under the hood that the user may not be aware of. Think how a browser makes requests to download fonts and images, to make Ajax requests, etc. Now imagine that we are logged-in to our bank and we get an email that contains the following image:

```
<img src="http://bank.com/transfer.do?acct=MARIA&amount=100000" width="0" height="0" border="0">
```

The browser will see the image tag and it will make that request in an attempt to download the image. It seems obvious that bank.com should be able to control what sites can make those kinds of requests.

### Browsers under the hood

When our browser makes a cross-origin request it takes note that this request needs to be checked for the access control headers. When the response comes back from the server the browser will check if the contents of the `Access-Control-Allow-Origin` header white-lists the domain where the request initiated from. If so, the browser will deliver the response to the JavaScript application. If not, an error will flag that the request could not be finalized.

Depending on how the consumer application issues the request, a preflight request may be sent. A preflight request is a request with the `OPTIONS` HTTP method that the browser sends automatically before issuing the cross-origin request that the consumer application is demanding. The main purpose of this request is to check the access control headers before sending the actual request. This is done because the `OPTIONS` request is usually faster than the actual request. The preflight will happen almost always, although our consumer can skip it if they issue a [simple request](https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS#Simple_requests).

It is the API server's responsibility to populate the appropriate headers to allow sharing resources in cross origin requests.

### CORS support in Drupal

This tutorial provides an example consumer to demonstrate CORS. We can [download the HTML](https://drupalize.me/sites/default/files/tutorials/cors-app.html_.zip) and adapt it to connect to our Drupal instance. This is a very naive and simple consumer application created for this tutorial. It should not be taken as an example of how to build browser-based consumers.

### Update the demo app with our connection details

We need to open *cors-app.html* in our text editor and replace `https://example.org/` with the domain where our Drupal API lives.

### See the application fail

Next we can open *cors-app.html* in our favorite web browser. We will also need to open the developer tools in the browser. Finally we can click *Fetch articles*.

We will see how the browser sends a preflight request, and how it fails because of the missing `Access-Control-Allow-Origin` header (unless we already enabled CORS in Drupal).

Image

![CORS failing](../assets/images/cors-fail.png)

### Configure CORS in Drupal

Drupal core provides support for CORS since 8.2, but it's turned off by default. To turn it on we will need to edit our *sites/default/services.yml* file. If we do not have one, we can create it by copying the contents from *sites/default/default.services.yml*.

Update the `cors.config` section to match the following:

```
   # Configure Cross-Site HTTP requests (CORS).
   # Read https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS
   # for more information about the topic in general.
   # Note: By default the configuration is disabled.
  cors.config:
    enabled: true
    # Specify allowed headers, like 'x-allowed-header'.
    allowedHeaders: ['*']
    # Specify allowed request methods, specify ['*'] to allow all possible ones.
    allowedMethods: ['*']
    # Configure requests allowed from specific origins.
    allowedOrigins: ['*']
    # Sets the Access-Control-Expose-Headers header.
    exposedHeaders: false
    # Sets the Access-Control-Max-Age header.
    maxAge: false
    # Sets the Access-Control-Allow-Credentials header.
    supportsCredentials: false
```

This configuration is very generic, and it will allow any kind of resource sharing. We will need to make sure to update `allowedOrigins` and `allowedMethods` to reflect only the valid domains and HTTP methods that our browser-based applications use. Public APIs can leave these values, since they may not know about the consumers that integrate with the API.

When *services.yml* is updated, we can [clear caches](https://drupalize.me/tutorial/clear-drupals-cache) for the changes to be applied.

#### See the application succeed

We can now go back to *cors-app.html* in our web browser, and click *Fetch articles* with the developer tools open.

We can see how now the articles are appearing in the demo application. More importantly, we can now observe how there are no errors in the console, and that the preflight `OPTIONS` request succeeded. That allowed our `GET` request to be made. The `GET` request is the one that will pull information from the API.

Image

![CORS succeeding](../assets/images/cors-success.png)

## Recap

CORS is a security feature built into web browsers to ensure the *same-origin policy*. Drupal comes with support for CORS, but it's disabled by default. In this tutorial we learned how to access the configuration in Drupal to allow CORS, and how to configure it for our API.

## Further your understanding

- Modify the application demo example so the cross-origin request is [simple](https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS#Simple_requests). Did you see how the `OPTIONS` preflight request is not done in that scenario? CORS is still checked without the preflight request.
- Did you know about [Cross-site request forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery)? Drupal protects your site from it.

## Additional resources

- [MDN web docs about CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS) (developer.mozilla.org)
- [MDN web docs about Same-Origin Policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) (developer.mozilla.org)
- [CORS configuration examples in Drupal](https://www.drupal.org/node/2715637) (Drupal.org)
- [Stack/Cors PHP library used by Drupal](https://github.com/asm89/stack-cors) (github.com)

Downloads

[x6J2aQoj\_oUHMMQcyKkzs-oJ1gclMTu3OVQp52Ywk\_U.jpg.jpg](/sites/default/files/sproutvideo_thumbnails/x6J2aQoj_oUHMMQcyKkzs-oJ1gclMTu3OVQp52Ywk_U.jpg.jpg)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Make an Authenticated Request Using OAuth 2](/tutorial/make-authenticated-request-using-oauth-2?p=3279)

Next
[JSON:API POST Requests: Create an Entity](/tutorial/jsonapi-post-requests-create-entity?p=3279)

Clear History

Ask Drupalize.Me AI

close