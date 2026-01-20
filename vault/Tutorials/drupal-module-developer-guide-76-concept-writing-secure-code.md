---
title: "Concept: Writing Secure Codefree"
url: "https://drupalize.me/tutorial/concept-writing-secure-code?p=3246"
guide: "[[drupal-module-developer-guide]]"
order: 76
---

# Concept: Writing Secure Codefree

## Content

In the world of Drupal development, ensuring the security of custom code is paramount. Drupal's security standards and features offer a robust foundation, but developers must also adhere to security best practices to safeguard against vulnerabilities. From sanitizing output to prevent cross-site scripting (XSS) attacks to using Drupal's database abstraction layer to avert SQL injection, Drupal empowers developers to write secure code. But it's still up to you, the developer, to do so.

In this tutorial, we'll:

- Provide an overview of these practices.
- Introduces additional resources to increase your security expertise.

By the end of this tutorial, you should be able to articulate some of the common security risks and mitigation strategies for Drupal modules.

## Goal

Learn best practices for developing secure custom code within Drupal.

## Prerequisites

- [Chapter 13. Security and Maintenance](https://drupalize.me/course/user-guide/security-chapter)

## Follow Drupal's coding standards

In addition to rules about how to format your code, Drupal's coding standards also include recommendations for using Drupal's internal APIs to help write secure code. We'll go into this more in [Lint Your Code with PHP\_CodeSniffer](https://drupalize.me/tutorial/lint-your-code-phpcodesniffer).

## Sanitize output to prevent XSS

Drupal’s Twig templating engine automatically filters output to prevent XSS attacks. Developers should avoid using the `| raw` filter in Twig templates unless absolutely necessary and ensure proper use of the `t()` function and `Html::escape()` for manual output sanitization.

We discussed the `t()` function in [Output Translatable Strings](https://drupalize.me/tutorial/output-translatable-strings).

### Prevent SQL injection

Drupal’s Entity API and database abstraction layer offer built-in protections against SQL injection. Developers should use these tools instead of crafting raw SQL queries.

See [Concept: Entity API and Data Storage](https://drupalize.me/tutorial/concept-entity-api-and-data-storage).

### CSRF protection

Drupal includes built-in CSRF protection for routes that perform actions, significantly reducing the risk of cross-site request forgeries. Developers should ensure that any custom routes performing actions leverage this protection.

### Use Drupal's API for data validation

Use Drupal's Form API and validation mechanisms to ensure user input is properly validated. This will reduce the risk of injection attacks and data tampering.

See [Add Custom Validation to User Entities](https://drupalize.me/tutorial/add-custom-validation-user-entities) and [Validate User Input for the Settings Form](https://drupalize.me/tutorial/validate-user-input-settings-form).

### Regular module and core updates

Keeping Drupal core and contributed modules updated is crucial for security. Updates often include patches for security vulnerabilities.

See [13.3. Concept: Security and Regular Updates](https://drupalize.me/tutorial/user-guide/security-concept).

## Learning and implementing security practices

- Drupal.org offers comprehensive [documentation on writing secure code](https://www.drupal.org/docs/security-in-drupal/writing-secure-code-for-drupal) and a detailed overview of Drupal's security features.
- The [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/) provides a framework for security best practices that Drupal adheres to.
- Snyk's guide on [securing Drupal 10](https://snyk.io/blog/5-ways-to-secure-drupal-10/) discusses common vulnerabilities and mitigation strategies, including Content Security Policy (CSP) implementation and XSS prevention.

## Recap

Writing secure code in Drupal is crucial for maintaining the integrity and trustworthiness of Drupal sites. By following Drupal's security best practices and using its robust security features, developers can protect sites from common vulnerabilities.

## Further your understanding

- Explore Drupal’s API documentation for functions that help sanitize output and validate input.
- Review the security advisories posted on Drupal.org to understand common vulnerabilities and learn how they were addressed.

## Additional resources

- [Writing secure code](https://www.drupal.org/docs/security-in-drupal/writing-secure-code-for-drupal) (Drupal.org)
- [Drupal Coding Standards](https://www.drupal.org/docs/develop/standards) (Drupal.org)
- [Drupal Security Team](https://www.drupal.org/drupal-security-team) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Concept: Coding Standards](/tutorial/concept-coding-standards?p=3246)

Clear History

Ask Drupalize.Me AI

close