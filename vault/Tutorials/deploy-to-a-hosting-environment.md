---
title: "Deploy to a Hosting Environment"
url: "https://drupalize.me/tutorial/deploy-hosting-environment?p=2467"
guide: "[[command-line-tools-drupal]]"
order: 7
---

# Deploy to a Hosting Environment

## Content

This tutorial provides an overview of the concept of an "artifact" and provides step-by-step instructions for deploying a Composer-managed Drupal application to a hosting environment.

In this tutorial we'll:

- Define what an "artifact" is
- Look at how to use Composer and a build process to create and deploy an artifact
- Talk about the benefits of this approach

By the end of this tutorial you should have a general understanding of the steps required in order to deploy a Composer-managed project into production.

## Goal

Learn the concept of "production as an artifact of development" and how to deploy a Composer-managed Drupal application to a production hosting environment.

## Prerequisites

- [Use Composer with Your Drupal Project](https://drupalize.me/tutorial/use-composer-your-drupal-project)
- A Composer-managed Drupal application ready to be deployed to a hosting environment

## Production as an artifact of development

If you followed the Composer best practices expounded in [Anatomy of a Composer Project](https://drupalize.me/tutorial/anatomy-composer-project), then your repository does not have Drupal core or any contributed modules committed to it. You may wonder, "How can I deploy and host a project that is missing Drupal core files?"

To answer that question, let's explore a fundamental software development concept: production as an artifact of development.

This concept may not be well known in the Drupal community, but it soon will be. It has long been fundamental to many software development frameworks, and with Drupal's adoption of Composer, it's time to get on board.

You may have heard terms like "build", "compile", and "artifact" used in the context of software development. Many software languages build or compile code into artifacts. For example:

- Java developers compile their code into a *.jar* file.
- iOS developers export code into a iOS App (IPA) files.
- PHP developers often build Phar files to "archive" their code.

The process of building source code into an artifact that is then distributed to the end-user is predicated on the idea that our source (development) code should be different from our production code. Development toolchain doesn't belong in our production environment. Our production code should be optimized for serving it to a user. To quote Michelle Craychee's DrupalCon Presentation [Production is an Artifact of Development](https://events.drupal.org/neworleans2016/sessions/production-artifact-development):

> The tools that build the thing are not the thing itself. A production-ready Drupal repository is the product of our development chain.

> Drupal project repositories include myriad development tools from a *Vagrantfile* to a *Gemfile* from Composer to Behat. We commit our SASS but deploy our CSS. We commit instructions to build the thing but deploy the thing.

In the context of managing a Drupal application with Composer, following this practice requires that we perform an operation on our (source) repository that transforms it into a shippable, hostable, production-ready artifact.

Ideally, this process should be scripted and would be executed in a Continuous Integration workflow that also tests the artifact and pushes it to its destination.

For this tutorial, we will limit our scope to reviewing the manual steps necessary to generate the artifact.

## Generating a shippable artifact

Let's start with a public service announcement: **Never run Composer commands on a production environment. Ever.**

You should generate an artifact locally or on a continuous integration server and then push it to a production environment. Never generate an artifact in production. Apart from it implying a flawed development workflow, executing a Composer command in production may:

- Temporarily or permanently break your application if your application code is executed during the installation or update process. These processes are not atomic.
- Consume all of the available memory on the production machine.

First, let's use Git to switch to a separate branch that is used exclusively for artifact generation. We don't want to co-mingle our source code with our artifact. It's a common convention to create a build branch by simply appending "-build" to the name of your maintenance branch. For instance, if you maintain your project's code on the `master` branch, you would use `master-build` to generate your artifact.

Assuming that the `master-build` branch already exists, we would execute:

```
git checkout master-build
git merge master
```

Next, we need to install *only our production Composer dependencies.* That is to say, we will install everything in our *composer.json*'s `require` array and nothing in its `require-dev` array. We can do this by executing:

```
composer install --no-dev --optimize-autoloader
```

Note that in addition to the `--no-dev` option, which will cause `require-dev` dependencies to be removed/omitted, we also use the `--optimize-autoloader`. This alone can **improve the performance of your Drupal application by [up to 37%](http://mouf-php.com/optimizing-composer-autoloader-performance)**. This is not used during development because it prevents dynamic detection of new classes in Composer dependencies.

Next, we need to tell Git to commit all of the third party packages that we typically do not commit to our source repository. For this tutorial, we will use the straightforward method of force committing those directories. Again, this process should ideally be scripted. The following commands cover the most common project organization strategy, but you'll want to verify you've included everything required for your project.

```
git add -f vendor/
git add -f web/core
git add -f web/modules/contrib
git add -f web/themes/contrib
git add -f web/profiles/contrib
git add -f web/libraries
```

Let's assume that we are releasing the 1.0.0 tag for our application. We would:

```
git commit -m "Adding Composer dependencies in preparation for 1.0.0 release."
git tag 1.0.0 -m "Adding great new features."
git push origin 1.0.0
```

We can then checkout the 1.0.0 tag in our hosting environment and visit the site via a web browser.

## Automating the generation process

Ideally, the artifact generation process will be automated and executed in a Continuous Integration workflow via a tool like Jenkins, [Travis CI](https://travis-ci.org/), etc.

A typical Drupal continuous integration workflow would look something like this:

1. Install Composer dependencies.
2. Execute code validation tests (e.g., PHPCS, PHPLOC, etc.)
3. Install Drupal
4. Execute tests (e.g., PHPUnit, Behat, etc.)
5. Generate artifact
6. Push artifact to a hosting environment

There are contributed tools that provide this automation for you:

- [Acquia BLT](https://github.com/acquia/blt/)
- [Artifice](https://github.com/grasmash/artifice)

Alternatively, you may wish to write your own scripts. If you're already a proficient PHP developer, you should consider scripting your deployment process using [Robo](http://robo.li/), a modern Task Runner for PHP.

## Recap

In this tutorial, we learned that production code should be an artifact of the development code. We reviewed manual steps for generating a shippable artifact using Composer. We also reviewed options for automating this process via continuous integration.

## Further your understanding

- Why should production be an artifact of development?
- What belongs in production that does not belong in development (source code)?
- What belongs in development (source code) that does not belong in production?
- How can you use Composer to generate an artifact?

## Additional resources

- [Presentation: Production is an Artifact of Development DrupalCon](https://events.drupal.org/neworleans2016/sessions/production-artifact-development) (events.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Use Composer with Your Drupal Project](/tutorial/use-composer-your-drupal-project?p=2467)

Next
[Troubleshoot Common Composer Issues](/tutorial/troubleshoot-common-composer-issues?p=2467)

Clear History

Ask Drupalize.Me AI

close