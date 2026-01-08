---
title: "Best Practice Drupal Developmentfree"
url: "https://drupalize.me/tutorial/best-practice-drupal-development?p=3292"
guide: "[[develop-drupal-sites]]"
---

# Best Practice Drupal Developmentfree

## Content

Today's Drupal developer needs more than just a text editor and FTP. Best practice Drupal development involves a suite of tools, processes, and more than one server environment.

This tutorial is directed toward an audience that is not familiar with best practices in Drupal Development and methods involving version control with Git, IDEs, local development environments, and deployment environments (i.e. stage, live). Here we're providing a high-level overview of these topics with links to dive deeper if you need more information.

In this tutorial, we'll cover:

- Introduce Version Control Systems such as Git
- Discuss how Git can be used to deploy to remote web servers
- Review programming-centric text editors and Integrated Development Environments
- Identify the need for a local development environment.
- Explain shared deployment environments including production and stage.

## Goal

Understand the basics and best practices for Drupal development.

## Prerequisites

General knowledge of Drupal, site building, and the command line.

See the following resources if you need a refresher on any of these areas of knowledge:

- [Introduction to Drupal](https://drupalize.me/guide/introduction-drupal)
- [Build Drupal Sites](https://drupalize.me/guide/build-drupal-sites)
- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)

## Track changes with Git

Years ago, it was common to only work on a local copy of your site and upload any and all changed files using FTP. If you needed to recreate your development environment on a new computer, you would typically download the entire site to your system including a database.

While this approach worked, it came with significant drawbacks. If a file wasn't transferred correctly or didn't transfer at all, it could take hours of examining logs and debugging before you could uncover the problem. Worse, you didn't know exactly what changes were made. An accidental change to a file might take down your entire site.

Today, we largely solved those problems by relying on a *Version Control System* (VCS). A VCS is used to monitor all changes made to a collection of files (a *repository*), who made those changes, and when. Most VCSes also have the ability to distribute code to remote servers as well. This allows you to share your site code with a team of developers, while assuring everyone has the most up-to-date files and all changes are tracked.

There are many different VCS systems out there, but the most popular used by Drupal developers is Git. Git has a number of advantages: It's fast, completely open source, and available for multiple platforms including Linux, macOS, and Windows.

## Remote repositories

Git is a special kind of VCS in that it's a *Distributed Version Control System*. There's nothing in how Git operates that relies on any particular copy of the repository being the "right" one. If Git is used for distributing code, then how can we be sure everyone has the same set of changes?

The answer is, you decide! Well, your team decides: Typically, a single copy of the repository is denoted the "canonical" repository. Whatever is pushed to it is considered the standard for all others to follow. This is called a *remote repository*. In Git, the canonical remote repository is called the "origin."

The origin server can be anything accessible to Git, but it is typically managed by a web application or service. GitHub, GitLab, and Bitbucket are all examples of Git-managing web applications. These add a user-friendly UI along with features such as access control, code reviews, time-tracking, reports, and even deployment.

Learn more from the resources listed on the [Git topic page](https://drupalize.me/topic/git).

## Git deploy

Whenever the repository is *cloned* to a system, it contains a complete copy of everything in that repository. Unlike FTP, only new changes need to be transferred, instead of all the site's code. For this reason, many Drupal sites leverage this deploy code to production.

In a *git deploy* setup, the site code is cloned to a production web server just as you would to your laptop. As you develop, new features and updates are pushed to the origin. When you are ready to make those changes live, you log in to the web server and then pull those changes down from the origin.

Sometimes there are some files you don't want to commit to your repository. The most important of these is the database configuration in `settings.php`, but it can also include generated CSS files, API keys, and the contents of the Drupal files directory. To allow for this, these files are locations are listed in a `.gitignore` file. Typically, there's just one `.gitignore` in the root directory of the repository, but there can be one in any directory to add further ignore rules.

## Text-editors and IDEs

Now that you have all your files tracked in Git, you'll need something to edit the files. In the past you might have used an editor that was included on your system out of the box such as Notepad or TextEdit. While these provide the bare minimum functionality, today there are many text editors available that are specifically geared toward programming work. Popular options include Sublime Text, Atom Editor, Notepad++, and many, many others. These editors offer features such as syntax highlighting, search, formatting and encoding support, and even auto-completion.

Many choose to use an *Integrated Development Environment* over a text editor. IDEs bundle additional utilities and features to support a particular programming language, application, or workflow. Many Drupal developers rely on PhpStorm or NetBeans in which to work on their sites. While not necessary, an IDE can be a great asset when developing custom modules and themes.

Learn more about the PhpStorm IDE from the resources listed on the [PhpStorm topic page](https://drupalize.me/topic/phpstorm).

## Local development environment

Before you can upload your new site code to your server for all to use, it's critical that you test it locally. The rather generically named *local development environment* (sometimes just called "your local") provides a full web server stack on your laptop for you to test. Since only you have access to this environment, no one else is affected when bugs or typos occur.

A local dev environment for Drupal involves at least 3 components: A web server, a runtime to execute PHP code, and a database server. Once configured, you can run and test your site code just as though it were running on a public web server.

Learn more about development environments from the resources listed on the [Development Environments topic page](https://drupalize.me/topic/development-environments).

## Shared environments

Your local environment has one big downside, however: it's local. There's no easy way to share it with other members of your team, much less with your client. This is where *shared environments* come in.

There are often at least 2 shared environments, but there can be as many as 4:

- **Production** is the live site. It's the one that's associated with the site's domain and where all traffic is directed to.
- **Stage**, sometimes called "pre-prod" or "develop", is the dress rehearsal for the next version of your site. All of your team members should have access to stage. Stage is also often used for client demos.
- **Test** is used to try out code that is currently in development on server hardware that more closely matches production.
- **QA** is used not by developers for new code, but by testers to check and validate problems encountered by users in production. Sometimes called "sim-prod", it is set up to mimic (simulate) the production environment.

Not all Drupal projects have or need all of these environments. Smaller sites and teams often only need production and stage. The QA environment is typically only needed for sites that have dedicated testing personnel.

## Recap

In this tutorial, we reviewed Drupal development best practices. We've learned about version control systems such as Git and how it can be used to track and share code to your entire team. We covered options for editing code such as programming-centric text editors and IDEs. Finally, we covered how to test and run your code, from your local development environment to shared server environments including production.

## Further your understanding

- Why would we need a separate shared environment for testing?

## Additional resources

- [GitHub's interactive Git tutorial](https://try.github.io/) (github.io)
- [Git-flow cheat sheet](https://danielkummer.github.io/git-flow-cheatsheet/), a visual guide to a branching strategy used by many Drupal development teams (danielkummer.github.io)
- [Building a Drupal site with Git (Drupal.org)](https://www.drupal.org/node/803746) (Drupal.org)
- [Git](https://drupalize.me/topic/git) (Drupalize.Me)
- [PhpStorm](https://drupalize.me/topic/phpstorm) (Drupalize.Me)
- [Development Environments](https://drupalize.me/topic/development-environments) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Annotations](/tutorial/annotations?p=3292)

Clear History

Ask Drupalize.Me AI

close