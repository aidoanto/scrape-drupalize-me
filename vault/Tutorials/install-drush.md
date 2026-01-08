---
title: "Install Drush"
url: "https://drupalize.me/tutorial/install-drush?p=3234"
guide: "[[drupal-module-developer-guide]]"
---

# Install Drush

## Content

Drush, the Drupal Shell, is a utility for module developers and administrators. While it does ship with DDEV, it doesn't come standard with Drupal core and must be installed separately via Composer.

In this tutorial we'll:

- Install Drush with Composer
- Verify that Drush is working

By the end of this tutorial, you should have a working copy of the Drush utility installed in your development environment.

## Goal

Install Drush and verify that it's working.

## Prerequisites

- [Concept: Drupal Development Environment](https://drupalize.me/tutorial/concept-drupal-development-environment)
- [Set Up Your Development Environment](https://drupalize.me/tutorial/set-your-development-environment)
- [Using Composer to Download and Update Files](https://drupalize.me/tutorial/user-guide/install-composer?p=2368)
- [Installing a Module](https://drupalize.me/tutorial/user-guide/config-install?p=2343)

## Video tutorial

Sprout Video

### Install Drush using Composer

We recommend that you install Drush on a per-project basis using Composer.

```
composer require drush/drush
```

**Note:** If you're using [our DDEV configuration](https://drupalize.me/tutorial/set-your-development-environment), Drush is already included.

Learn more about installing Drush in [Install Drush Using Composer](https://drupalize.me/tutorial/install-drush-using-composer).

### Verify that it's working

Run the `status` command to verify Drush is working and can connect to your Drupal application.

```
./vendor/bin/drush status
```

Example output:

```
Drupal version   : 10.2.4
Site URI         : https://module-developer-guide.ddev.site
DB driver        : mysql
DB hostname      : db
DB port          : 3306
DB username      : db
DB name          : db
Database         : Connected
Drupal bootstrap : Successful
Default theme    : honey
Admin theme      : claro
PHP binary       : /usr/bin/php8.1
PHP config       : /etc/php/8.1/cli/php.ini
PHP OS           : Linux
PHP version      : 8.1.21
Drush script     : /var/www/html/vendor/bin/drush
Drush version    : 12.4.3.0
Drush temp       : /tmp
Drush configs    : /var/www/html/vendor/drush/drush/drush.yml
Install profile  : standard
Drupal root      : /var/www/html/web
Site path        : sites/default
Files, Public    : sites/default/files
Files, Temp      : /tmp
```

**Note:** We can call Drush in various ways. For example, `./vendor/bin/drush status`, `drush status`, and `ddev drush status` are all valid depending on the context. In this guide, we'll always use the `drush {command}` format. You can modify the exact format to match your environment.

## Simplify how you call Drush

It's common to see Drush calls documented as `drush status`, without the `./vendor/bin/drush` prefix. Older versions of Drush supported a project called drush-launcher, which would allow you to run the `drush` command in any directory, and it would seek out and execute the appropriate project-specific binary. That script no longer works, but not all documentation has been updated.

You can do any of the following:

- Always call Drush using the full path like `./vendor/bin/drush status`.
- Use an environment like DDEV that handles aliasing `./vendor/bin/drush` to `drush` for you. From outside the DDEV web container, use `ddev drush`. From inside the container (via `ddev ssh`), use `drush` to run Drush commands.
- Add Drush to your `$PATH` or use one of the various script options from [this issue](https://github.com/drush-ops/drush/issues/5828) until the community settles on a new standard.

## Recap

In this tutorial, we installed Drush using Composer and verified that it's working by running the `drush status` command and seeing it return results without errors. In a DDEV environment, Drush commands can be run outside the `web` container by prefixing the command with `ddev`. For example, `ddev drush status`. From inside the `web` container (after running `ddev ssh`), Drush commands do not need to be prefixed (`drush status`).

## Further your understanding

- Run the `drush` command with no additional arguments to see a list of available commands. Which commands do you think will be useful for module development?
- Why is Drush installed using the `--dev` Composer flag?
- How can you use Drush to get a one-time login link for your site? What happens when you go to the link?

## Additional resources

- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0) (Drupalize.Me)
- [Install Drush Using Composer](https://drupalize.me/tutorial/install-drush-using-composer) (Drupalize.Me)
- [Drush documentation](https://www.drush.org/12.x/) (drush.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Set Up Your Development Environment](/tutorial/set-your-development-environment?p=3234)

Clear History

Ask Drupalize.Me AI

close