---
title: "Live vs. Local Configuration Management"
url: "https://drupalize.me/tutorial/live-vs-local-configuration-management?p=2478"
guide: "[[drupal-site-administration]]"
---

# Live vs. Local Configuration Management

## Content

Using Drush to work with the Drupal Configuration System is straightforward when working locally. Navigate to the directory containing your site, then issue whatever Drush command you need.

Things become more complicated when multiple environments become involved. Often, a configuration change will need to be made on the production ("live") site and then need to be persisted to a Git repository later. When this occurs, Drush once more provides a solution in the form of the `config-pull` subcommand.

**Note**: Drush 8 and the latest version use different methods and file types for configuration files. This tutorial will demonstrate methods that are compatible with the latest version of Drush with notes related to Drush 8.

## Goal

How to set up and use the `config-pull` subcommand to download configuration from a remote site.

## Prerequisites

- [Overview: Configuration Management in Drupal](https://drupalize.me/tutorial/overview-configuration-management-drupal)
- [Configuration Sync Directory Setup](https://drupalize.me/tutorial/configuration-sync-directory-setup)
- [Drush Site Aliases](https://drupalize.me/tutorial/drush-site-aliases)

## Set up SSH Keys for remote access

One thing that's missing from the alias file is a password. It's bad security practice to save the password in plaintext in your site. While Drush can ask for the password interactively, it's better to set up *SSH keys*.

SSH keys allow you to use public key cryptography instead of entering your password. This is more secure than entering your password, but it does require some set-up.

This tutorial doesn't cover setting up SSH keys, but you can find several tutorials online that can assist you. Linode has an excellent [tutorial on setting up SSH keys](https://www.linode.com/docs/security/authentication/use-public-key-authentication-with-ssh/) for all common desktop operating systems, including Linux, macOS, and Windows.

## Additional SSH key set up for Docker

When using Docker as your local development environment, you may only have Drush installed in the containers, and not on the host operating system. In this case, you can modify your containers to [bind mount](https://drupalize.me/tutorial/use-bind-volumes) the directory containing your SSH keys.

### Create a *docker-compose.override.yml* file

Create and save *docker-compose.override.yml* in the same directory as your Compose file.

Open the override file with your editor of choice and enter the following:

```
  version: '3'
  services:
    container_where_drush_is_run:
      volumes:
        - /path/to/your/.ssh:/path/to/container/.ssh
```

Where:

- `container_where_drush_is_run`: the service name of the container from which Drush is run.
- `/path/to/your/.ssh`: the path to your SSH directory on your host OS, typically `~/.ssh`
- `/path/to/container/.ssh`: the path to the SSH directory inside the container.

Use `docker-compose kill` and `docker-compose up -d` to restart your container set.

## Create a new Drush site alias

Create a site alias file in either the project root or Drupal root's *drush/sites/* directory. See [Drush Site Aliases](https://drupalize.me/tutorial/drush-site-aliases) to learn more.

Fill in the details with credentials for connecting to your server using SSH.

*example.site.yml*:

```
dev:
  host: dev.example.com
  user: www-admin
  root: /path/to/drupal
  uri: https://dev.example.com

stage:
  host: stage.example.com
  user: www-admin
  root: /path/to/drupal
  uri: https://stage.example.com

prod:
  host: prod.example.com
  user: www-admin
  root: /path/to/drupal
  uri: https://www.example.com
```

## Use the alias

Once you have the SSH key created, and the public key distributed to the target remote server, you can start using our drush alias.

Given our example *example.site.yml* file above, we have an alias named `stage`. To instruct Drush to use the alias, we prefix it with an at-symbol (`@`) before the subcommand we wish to run on the remote server:

```
drush @example.stage status
```

This command will verify if the public key is set up correctly, and if we can communicate with the remote site.

## Pull configuration changes

With all of that set up, we can now use Drush's `config-pull`, or `cpull` subcommand:

```
drush cpull @source_site_alias @target_site_alias
```

Where:

- **source\_site\_alias** is the site alias of the remote site we're pulling changes from.
- **target\_site\_alias** is the alias of the site we're into which we're importing changes.

Often you will only have site aliases for remote sites, but not your current, local site. So what do we use for `target_site_alias`? In that case, Drush provides an alias out of the box, `self`. If we were pulling changes from our `prod` alias into a site on our laptop, it would look like this:

```
$ cd /path/to/your/local/site
$ drush cpull @prod @self
```

The above would download configurations from the example site's `prod` environment into the site on our laptop at the path */path/to/your/local/site*.

The `cpull` subcommand does several steps for us:

1. It logs into the remote site specified by `source_site_alias` via SSH.
2. Drush then talks to the Drush that's installed in the remote server, executing a configuration export.
3. Instead of exporting to the site's sync directory, it exports to a Drush specific directory created for the pull operation.
4. Drush then downloads the exported files from the remote server into our local sync directory.
5. Drush then talks to our local site, performing a configuration import.

The wonderful thing about `cpull` is that it does **not** modify the default configuration sync directory of the source site. The `cpull` is transparent, leaving the source site in exactly the same condition as before the operation.

## Persist configuration to Git

The key use of `cpull` is to download any configuration changes made to a remote site -- typically production -- and then persist those changes to a version control system such as git. This is often called "truing up", since it persists live changes with the canonical site configuration in the repository.

To true-up a repository with live changes:

### Open a command prompt and navigate to your site repository

Check the status of your repository with `git status`.

If the repository is not in a clean state, please commit them, delete them with `git reset`, or save them temporarily with `git stash`.

Change to "next release" branch in your repository, typically `develop`.

Perform a `drush cpull`, specifying the source site alias.

Review changes, reverting lines as necessary.

Use git to `add` and `commit` your changes.

## Recap

The `config-pull` command is an effective and useful way to download configuration changes from a remote server into your local environment. This is especially useful when client changes or hotfixes have left the live site with config changes that haven't been persisted to git.

## Further your understanding

- Some configuration changes refer to content. How would you ensure those configuration changes are still valid after a `cpull`?

## Additional resources

- [`config-pull` reference on Drush docs](https://drushcommands.com/drush-8x/config/config-pull/)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Inspect Configuration with Drush](/tutorial/inspect-configuration-drush?p=2478)

Next
[Configuration Interdependencies](/tutorial/configuration-interdependencies?p=2478)

Clear History

Ask Drupalize.Me AI

close