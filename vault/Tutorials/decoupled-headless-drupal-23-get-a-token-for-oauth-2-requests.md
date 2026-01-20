---
title: "Get a Token for OAuth 2 Requests"
url: "https://drupalize.me/tutorial/get-token-oauth-2-requests?p=3279"
guide: "[[decoupled-headless-drupal]]"
order: 23
---

# Get a Token for OAuth 2 Requests

## Content

To authenticate a request against the API server, we must send an authentication token along with the request. For that, we need first to obtain the token from the server. The various ways we can get a token from the server are called grants. Using one of them, we will obtain an access token and a refresh token.

In this tutorial, we will:

- Learn how OAuth 2 grants work
- Learn how to generate and request authentication tokens
- Learn how to generate and request refresh tokens

By the end of this tutorial, you should be able to use the OAuth 2 *authorization code* flow (using PKCE) to authenticate a user and obtain access and refresh tokens that your API client can use to make authenticated requests.

## Goal

Use the OAuth 2 authorization code grant (with PKCE) to obtain tokens that can be used to make authenticated requests.

## Prerequisites

- [Install and Configure Simple OAuth](https://drupalize.me/tutorial/install-and-configure-simple-oauth)

## Video tutorial

Sprout Video

## OAuth 2 grants

OAuth 2 supports several methods for acquiring an access token. These methods are referred to as *grants*. The [Simple OAuth](https://drupal.org/project/simple_oauth) module supports the following grants:

- [Authorization code grant](https://datatracker.ietf.org/doc/html/rfc6749#section-4.1) (with optional [@PKCE](https://datatracker.ietf.org/doc/html/rfc7636))
- [Refresh grant](https://tools.ietf.org/html/rfc6749#section-1.5)
- [Client credentials grant](https://tools.ietf.org/html/rfc6749#section-4.4)

Other grants, such as the password grant and implicit grant, which were previously supported by the module, are no longer recommended due to security concerns.

From this list, we will need to choose the grant that is most applicable to each situation. It is not a matter of preference or popularity; each grant will be the best in different situations. Visit [the documentation](http://oauth2.thephpleague.com/authorization-server/which-grant/) to decide which grant to use for each scenario.

Even if requesting an OAuth 2 token is simply a matter of making a properly formatted POST request, it is likely that there are helper libraries available to ease this process for our consumer. This is, again, because we are using a popular standard.

## Authorization code grant with PKCE

The [authorization code grant with PKCE](https://datatracker.ietf.org/doc/html/rfc7636) is the recommended approach for public clients such as JavaScript or mobile applications. Instead of sending user credentials directly to the API, the client first redirects the user to Drupal’s authorization server, where the user logs in and authorizes access.

### What is PKCE?

PKCE (Proof Key for Code Exchange) is an extension to the authorization code flow that prevents certain attacks and enables the secure exchange of OAuth from public clients. ([OAuth.net](https://oauth.net/2/pkce/))

For native and browser-based apps, it is considered best practice to use the authorization code flow with the PKCE extension. This flow is similar to the regular authorization code flow, except that **PKCE replaces the client secret** with a one-time code challenge. This means the client app doesn’t have to store a client secret. But the client app will have to implement code to generate these one-time strings.

If you've ever used GitHub or Facebook to sign in to an application before, you've seen this flow in action.

The flow works like this:

### Create a code verifier and challenge

The client generates a random string (the verifier) and derives a hashed version (the challenge).

**Note:** See below for examples of how to generate these one-time use codes.

### Redirect to the authorization endpoint

The client generates a URL with all the necessary query string parameters and then opens that URL. Each parameter has a specific purpose:

- `response_type=code`: tells the server we want an authorization code.
- `client_id`: identifies the application making the request. We created this in a [previous tutorial](https://drupalize.me/tutorial/install-and-configure-simple-oauth).
- `redirect_uri`: where the authorization server should send the user (and the generated authorization code) after approval.
- `code_challenge`: the hashed string derived from the code verifier.
- `code_challenge_method`: the algorithm used to create the challenge (typically S256).
- `scope`: specifies what level of access the application is requesting. You can find this in Drupal.

Example:

```
https://example.org/oauth/authorize
?response_type=code
&client_id=react_app
&redirect_uri=https://client.example.org/callback
&code_challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM
&code_challenge_method=S256
&scope=oauth
```

### User logs in and authorizes

Drupal prompts the user to authenticate and approve the request.

### Receive authorization code

The client receives an authorization code via the redirect URI. After successfully approving the request Drupal redirects to the *redirect url* with the authorization code in the query string.

### Exchange code for tokens

The client extracts the `?code=\` value from the URL and makes a POST request to the token endpoint:

```
http --form POST https://example.org/oauth/token \
  grant_type=authorization_code \
  client_id=react_app \
  code=SplxlOBeZQQYbYS6WxSbIA... \
  redirect_uri=https://client.example.org/callback \
  code_verifier=dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk
```

The server responds with both an access token and a refresh token. The access token is used in the `Authorization` header when making API requests.

In the above example `code_challenge`, and `code_verifier` are hard coded values that already pair together. In the real world, though, you'll want to generate unique values for those fields for every request. Here are a few examples of how to generate `code_challenge` and `code_verifier` that will work together.

Note that your `code_verifier` should be URL-safe and between 43–128 characters.

Bash (pkce.sh):

```
#!/usr/bin/env bash

# Generate code_verifier.
code_verifier=$(openssl rand -base64 64 | tr '+/' '-_' | tr -d '=' | cut -c1-96)

# Create the SHA256-based code_challenge
code_challenge=$(printf '%s' "$code_verifier" \
  | openssl dgst -sha256 -binary \
  | openssl base64 \
  | tr '+/' '-_' | tr -d '=')

echo "code_verifier:  $code_verifier"
echo "code_challenge: $code_challenge"
```

Run it: `chmod +x pkcs.sh && ./pkcs.sh`

PHP (pkce.php):

```
<?php
// Generate a random code_verifier.
$random = random_bytes(64);
$code_verifier = rtrim(strtr(base64_encode($random), '+/', '-_'), '=');

// Derive the S256 code_challenge.
$hash = hash('sha256', $code_verifier, true);
$code_challenge = rtrim(strtr(base64_encode($hash), '+/', '-_'), '=');

echo "code_verifier:  $code_verifier\n";
echo "code_challenge: $code_challenge\n";
```

Run it: `php pkce.php`

JavaScript / Node.js (pkce.js):

```
// Generate a random code_verifier.
function generateCodeVerifier(length = 64) {
  const array = new Uint8Array(length);
  crypto.getRandomValues(array);
  return base64UrlEncode(array);
}

// Create a code_challenge from the verifier.
async function generateCodeChallenge(verifier) {
  const encoder = new TextEncoder();
  const data = encoder.encode(verifier);
  const digest = await crypto.subtle.digest('SHA-256', data);
  return base64UrlEncode(new Uint8Array(digest));
}

// Helper: base64url encoding
function base64UrlEncode(arrayBuffer) {
  return btoa(String.fromCharCode(...arrayBuffer))
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');
}

// Example usage:
(async () => {
  const verifier = generateCodeVerifier();
  const challenge = await generateCodeChallenge(verifier);
  console.log('code_verifier:', verifier);
  console.log('code_challenge:', challenge);
})();
```

Run it: `node pkce.js`

Each of those code examples will output `code_verifier` and `code_challenge` that you can use in your authorization code grant request.

## Refresh grant

Access tokens typically expire after a short period. Instead of requiring the user to complete the entire authorization process again, you can use a refresh token to request a new access token.

Example request:

```
http --form POST https://react-tutorials-2.ddev.site/oauth/token \
  grant_type=refresh_token \
  client_id=react_app \
  refresh_token=xyz123
```

The authentication server (Drupal) will respond with a new set of tokens.

## Recap

In this tutorial, we learned how to obtain an authentication token using the authorization code grant with PKCE. We also learned how to refresh the access token using the refresh grant.

## Further your understanding

- Is there an OAuth 2 client library for your consumer that can simplify the process of interacting with OAuth? Which grants does it support?
- Can you generate a token using the [client credentials grant](http://oauth2.thephpleague.com/authorization-server/client-credentials-grant/)? Try to imagine a situation where that grant would be the best option.
- Did you know all the tokens returned by Simple OAuth are JWT tokens? You can add extra information to the tokens by superseding the [`TokenEntityNormalizer`](https://git.drupalcode.org/project/simple_oauth/blob/6.0.x/src/Normalizer/TokenEntityNormalizer.php?ref_type=heads).

## Additional resources

Listed below are video tutorials about the different types of grants supported by Simple OAuth:

- [Client credentials grant](https://www.youtube.com/watch?v=B6xlW7RsUUk&index=7&list=PLZOQ_ZMpYrZtqy5-o7KoDhM3n6M0duBjX) (youtube.com)
- [Authentication code grant](https://www.youtube.com/watch?v=khh8MmY9jm4&index=8&list=PLZOQ_ZMpYrZtqy5-o7KoDhM3n6M0duBjX) (youtube.com)
- [Implicit grant](https://www.youtube.com/watch?v=sZbzcCXMmEA&list=PLZOQ_ZMpYrZtqy5-o7KoDhM3n6M0duBjX&index=9) (youtube.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Install and Configure Simple OAuth](/tutorial/install-and-configure-simple-oauth?p=3279)

Next
[Make an Authenticated Request Using OAuth 2](/tutorial/make-authenticated-request-using-oauth-2?p=3279)

Clear History

Ask Drupalize.Me AI

close