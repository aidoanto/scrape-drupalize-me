---
title: "API Authentication and Authorization"
url: "https://drupalize.me/tutorial/api-authentication-and-authorization?p=3279"
guide: "[[decoupled-headless-drupal]]"
---

# API Authentication and Authorization

## Content

In a monolithic architecture (non-decoupled) there is an implicit proof that the user in the frontend is the same one in the backend. This empowers the frontend to offload all the authentication and authorization to the backend, typically using a session cookie. In a decoupled architecture, there will be multiple consumers, and some of them will not support using cookies. There are several alternatives to session cookies to authenticate our requests in a decoupled project.

In this tutorial we will:

- Learn about authorization versus authentication
- The impact on a decoupled project of having logged-in users
- Learn about the available options for authentication when using a Drupal backend.

By the end of this tutorial, you should be able to explain the difference between authentication and authorization and know how to get started implementing both in a Drupal-backed web services API.

## Goal

Understand the difference between authorization and authentication and implications of dealing with each when creating a web services API.

## Prerequisites

- [What Are Web Services?](https://drupalize.me/tutorial/what-are-web-services)

## Authorization in Drupal

**Authentication:** The process of verifying that someone is who they say they are.

**Authorization:** The process of determining if that particular person that can do a certain action.

In an airport, we need to provide our passport to prove that we are indeed the person with the plane ticket. That is *authentication*. The security agent will run some checks on our name to make sure we can be granted access to the terminal. That is *authorization*.

Authentication in Drupal is very flexible; there are many different ways to prove that a user is who they say they are. However, there is only one way of authorizing actions, and that is the access system. Most of the time the access system will check that the user has a role that contains a permission allowing an action. JSON:API and all the solutions mentioned in this course, use the built-in access system when interacting with Drupal without any additional work.

## Authentication in a monolithic project

When using Drupal in a traditional way authentication comes out of the box. That is possible because, in that scenario, we have prior knowledge of what the frontend of the application is. We know that in a monolithic Drupal project the frontend is going to be rendered by Drupal. Therefore, communicating the existence of a *currently logged-in user* is just a matter of storing some information in an internal variable that can be passed around.

When an anonymous user comes into the Drupal site, they provide their username and password using a secure form. The Drupal backend creates a cookie with information about the user and sends it back to the browser after processing the form submission. Finally, the browser stores that cookie for future use.

In all subsequent requests to that domain, the browser will check for any eligible cookies, and it will attach them to the request. When the backend gets the cookie that was stored in the browser it will recognize that the request belongs to a user — the one that sent the credentials using the secure form.

We can see two big dependencies for this authentication mechanism to work:

- The consumer needs to support cookies.
- The backend application and the frontend application need to be in the same domain. Otherwise, the consumer will refuse to send the cookie for security reasons.

In traditional Drupal sites, these two requirements are easily met. The role of Drupal is to build a website that is accessible using a web browser. All web browsers in the market have excellent support for cookies. In addition to that, a monolithic Drupal project will always be serving the frontend and the backend under the same domain, since they are the same application.

## Cookie authentication in decoupled projects

In a decoupled environment, we cannot ensure that the consumer supports cookies. In fact, if our API is public anyone can write their own consumers, and we don't know what technology they are using. That means that we don't know if those consumers support cookies or not. Moreover, in a decoupled project we cannot ensure that all consumers are accessed under the same domain. An unknown consumer for our public API will be accessed in an unknown way.

Consider the following scenario for a hypothetical decoupled project:

- All the consumers are to be accessed via a web browser.
- Our organization has control over all the possible consumers, and they are all accessible over the same domain.

Even in that situation, cookie-based authentication will only be a good fit if we can ensure, with certainty, that these conditions will remain true in the future. If we can be sure that we will never have a non-browser based consumer (wearables, phone apps, smart tv, etc.) and that no part of the API that requires authentication will ever be made public, then cookie-based authentication is a good choice.

Even in those very specific situations we don't gain much from using cookie-based authentication, when compared to OAuth2 (see below). In general, it is not recommended to use cookie authentication with decoupled projects.

## Basic auth: one alternative to cookies

Another authentication scheme is [Basic Authentication](https://tools.ietf.org/html/rfc7617). Drupal comes with basic authentication support out of the box. Basic auth is a simple way to authenticate our requests by sending the username and password of a user on each request. To do so, our consumer application will need to do a base64 encoding of `"$username:$password"` and send that to Drupal each time they want to authenticate a request.

Implementing authentication with basic auth in our consumer is straightforward. However, there are several security concerns when using HTTP basic authentication:

- The password is sent over the wire in almost plain text. This can be solved by SSL in transit to the web server. However once it's there, routing applications, server logs, etc. may see the password in plain text.
- The password is sent repeatedly, for each request. That increases the size of an attack window.
- The password is cached by the web browser. It could be silently reused by any other request to the server. (A CSRF attack.)
- The password may be stored permanently in the browser, if the user allows. Another user on the same shared machine could steal the password.

These concerns can be mitigated by using tokens instead of basic auth. That is because:

1. Tokens can be scoped. The server can indicate the actions that a user can perform with a given token, among the ones allowed for that user in Drupal. In contrast, the password can perform all the actions the user can do.
2. Tokens expire rapidly. It is a good practice that authentication tokens are unusable after some time. This does not solve the security issue, but limits the attack window in case of a non-repeatable token capture.

Given all the limitations above, basic authentication is not suited for production environments. However, during the development cycle basic auth is a convenient way to test our authenticated requests against our local environment.

## OAuth 2: a better alternative to cookies

OAuth 2 is a mature open standard for token-based authentication and authorization on the Internet. OAuth 2 allows the user account information to be used by our consumers, without exposing the user's password.

One of the big benefits of OAuth 2 is that it is immensely popular. That translates into many helper libraries and third party services. That will help us build authentication in our consumer applications very quickly.

Another of the benefits of OAuth 2 is that it doesn't have the limitations of cookie authentication. That means that if we set up Drupal to support OAuth 2, then we can be sure that all our consumers will be able to authenticate against our Drupal site.

OAuth 2 will authenticate a request if that request carries a header containing a secret string that matches the records in the backend. In summary, Drupal shares a secret token with a consumer after a user has provided their credentials. After that, any request that contains that secret token can only belong to the user that Drupal shared that token with.

There are many ways to ask Drupal to generate a token, in accordance with the OAuth 2 specification. In all cases the sequence is:

1. A user provides the username and password to prove that they are who they claim to be.
2. Drupal generates a secret random token and stores it in the database associated to that user ID. Drupal also stamps an expiration date in the token, after which the token is useless.
3. Drupal returns the token to the consumer. The consumer stores that token.
4. The consumer makes as many requests as it needs to as an authenticated user by providing the token every time.

Note how after the initial handshake all the proof the consumer needs to send is the token. That means that the consumer application will not send the username and password for each request, which is potentially insecure. If a token is captured because of a critical vulnerability in the consumer application, the attackers will only have access until the token expires.

## Recap

In this tutorial, we learned that in order to send requests that require authentication we need to provide some kind of identity proof for the user. Drupal supports cookie authentication out of the box, but that is most useful for monolithic projects. In decoupled projects an authentication scheme like OAuth 2 will provide a better solution. Additionally, OAuth 2 provides increased security when compared to Basic auth.

## Further your understanding

- In a JavaScript consumer the code is often all publicly accessible. [How would you store a secret token in that scenario?](https://auth0.com/blog/ten-things-you-should-know-about-tokens-and-cookies/#token-storage)

## Additional resources

- [A step-by-step brief explanation of how cookie-based authentication works](https://stackoverflow.com/a/32218069/3060487) (stackoverflow.com)
- A good alternative to OAuth is [JWT](https://tools.ietf.org/html/rfc7519) (tools.ietf.org)
- [Drupal module for JWT](https://www.drupal.org/project/jwt) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Install and Configure Simple OAuth](/tutorial/install-and-configure-simple-oauth?p=3279)

Clear History

Ask Drupalize.Me AI

close