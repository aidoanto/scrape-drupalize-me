---
title: "Drush Site Aliases"
url: "https://drupalize.me/tutorial/drush-site-aliases?p=2593"
guide: "[[command-line-tools-drupal]]"
---

# Drush Site Aliases

## Content

Drush commands are commonly run in the Drupal **docroot**, the directory where Drupal's files live. This is a relatively simple task on your local development environment. But if you're working on multiple sites and each of those sites has one or more remote environments that you connect to via SSH, workflows quickly become complicated. Creating and using Drush site aliases allows you to run Drush commands on any site, local or remote, that you have credentials to access, from any location on your computer that has access to a Drush executable.

Imagine you've got a Drupal project with dev, test, and live environments in the cloud somewhere. And you need to clear the cache on the dev environment. You could SSH to that environment, and execute `drush cr` there. Or, after configuring a site alias you could do something like:

```
drush @provider.dev cr -y
```

And Drush will connect to the remote environment and clear the cache.

Site aliases allow bundling the configuration options (`--uri`, `--root`, etc.) for a specific remote server under an alias. This reduces the amount of typing required. Even more importantly, it helps teams agree on a common definition for environments like `@dev`, `@test`, and `@live` by committing their configurations to version control.

In this tutorial we'll:

- Define what a Drush site alias is
- Understand the use case for aliases
- Learn how to configure and use Drush site aliases

By the end of this tutorial, you should understand how Drush site aliases work, how to create Drush site aliases, and how to use them in a Drush command.

## Goal

Define what site aliases are and learn how to implement them.

## Prerequisites

- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)
- [Drush Configuration](https://drupalize.me/tutorial/drush-configuration)
- Drupal site installed and running in 2 places, for example, on your local computer and a live hosted site. To learn how to install Drupal, see [Chapter 3 of the Drupal User Guide](https://drupalize.me/series/user-guide/installation-chapter) and to learn how to set up a local development site see [11.8. Making a Development Site](https://drupalize.me/tutorial/user-guide/install-dev-making?p=3072), also in the Drupal User Guide.
- You will need to know the SSH credentials to connect to your remote (live) site if you want to set up a Drush site alias for it. To learn more about SSH, watch [Using SSH and SCP](https://drupalize.me/videos/using-ssh-and-scp?p=1149).

## How Drush connects to a site

When using Drush, you typically `cd` to the directory containing your Drupal site, i.e. the **docroot**, and execute the `drush` command from within the Drupal docroot. The reason for this is that Drush uses several checks to determine how to connect to a Drupal site:

- Is the current directory a Drupal docroot?
- Is the current directory a subdirectory of the Drupal docroot?
- ...and several more checks.

An alternative to using `cd` to change to the Drupal root directory is to pass the `--root` and `--uri` options to Drush to tell it which Drupal project you want to run commands against.

Using these flags, and others, Drush can be used to manage a remote Drupal site. Drush can open an SSH connection to the remote server, execute the provided command on the remote host, and then display the results locally. This is a common way to access a stage, test, or QA server.

Drush site aliases provide a way for teams to share short names that refer to the `@live`, `@stage`, `@dev`, and any other shared remote environments for a project. The alias file is typically located in the *PROJECT\_ROOT/drush/sites* directory and the file has to be named *self.sites.yml* for it to be automatically discovered. And contains the configuration required to connect to the various remote environments rather than requiring you to pass all the options to every command.

**Note:** Drush must be installed on the remote environment for this to work!

## The site alias file

A Drush site alias file has the following naming convention: *{COLLECTION}.site.yml*

The first part of the filename, in this case, *{COLLECTION}*, identifies a collection of site alias. The *.site.yml* suffix identifies the file as a Drush site aliases file, as long as it is saved in a Drush-discoverable location (more on that below).

Inside a *\*.site.yml* file the top-level YAML array keys identify the various environments, for example, `dev`, `staging`, `prod`. Nested key are configuration for that specific environment.

Example:

```
prod:
  # Fully qualified domain name.
  host: server.domain.com
  # Use to login as via SSH.
  user: admin
  # Location of the Drush root directory on the remote file system.
  root: /path/to/live/drupal/web
  # Publicly accessible URI of the remote server.
  uri: https://my-site.com
```

Once an alias is defined, you can run any command on the remote server from your own machine like so:

```
drush @prod status

drush @dev user:login --uid=1
```

## Drush-discoverable locations

Drush will search for alias files (*\*.site.yml*) in the following locations:

1. (Preferred) A *\*.site.yml* file in */drush/sites* in the Drupal docroot, e.g. *PROJECTROOT/DRUPALROOT/drush/sites/example.site.yml*.
2. (Preferred) A *\*.site.yml* file in */drush/sites* one directory level above the Drupal docroot, e.g. *PROJECTROOT/drush/sites/example.site.yml*.
3. In any path set in `drush.alias-path` (in the array `drush` with the key `alias-path`) in [a *drush.yml* configuration file](https://drupalize.me/tutorial/drush-configuration). This tells Drush where to find the site alias file(s), if they're not in a default discoverable location. Useful for example if you want to include a *global* alias file.
4. In any path passed via the switch, `--alias-path` on the command line.

**Note:** Drush will *not* search recursively in the above locations. Alias files should be placed directly in one of the listed locations.

## Groups of aliases

If you would like to organize your site aliases into one or more groups, then create a directory in a site alias discoverable location with the name of the group. For example, let's say you manage several sites for a particular client. You could name the group after the client and then place the various site alias files within that directory.

For example:

```
docroot # Drupal files and directories
  └── drush
      ├── drush.yml # optional, see step 1 above
      └── sites
          └── icecream # Name of group
                └── vanilla.site.yml # Drush site alias file
                └── chocolate.site.yml # Drush site alias file
                └── strawberry.site.yml # Drush site alias file
```

You could then target the site "vanilla" within the group "icecream" as follows:

```
drush @icecream.vanilla.dev
```

The pattern is `@{optional-directory}.{file-name}.{key-in-YAML-file}`.

**Tip:** Some hosting providers generate aliases files for their users and allow downloading them to local machines or CI containers.

## The built-in "self" alias

Drush treats a file named *self.site.yml* in either the project root's or docroot's *drush/sites* directory in a special manner. If your current working directory is the project or Drupal root, you can refer to your alias by just the environment key, for example:

```
cd PATH/TO/PROJECT
drush @live cache:rebuild
```

Instead of:

```
drush @self.live cache:rebuild
```

Assuming that the *self.site.yml* contained a key, `live`, with SSH credentials to a Drupal site, this command would rebuild the cache on that site instance.

The take-away here is that if you're using a shorthand alias with only the environment key, Drush will look for a *self.site.yml* in a Drush-discoverable location in the project or docroot for the environment key and connection credentials.

## Create a Drush alias file

Now that you're familiar with the concepts, let's walk through the process of creating a Drush alias file. This is a fairly generic walk-though. Use the information explained earlier in the tutorial to customize the file, its location, and its name to meet your use-case.

### Create an empty file to use for Drush aliases

Create an empty Drush alias file (*example.site.yml*) in a Drush-discoverable location.

Example 1: *drush/sites* in the Drupal docroot.

```
docroot # Drupal files and directories
  └── drush
      ├── drush.yml # optional, see step 1 above
      └── sites
          └── example.site.yml # Drush site alias file
... # Other Drupal files and directories
```

Example 2: *drush/sites* in the project root, one level above the Drupal docroot.

```
docroot # Drupal files and directories
drush
├── drush.yml # optional, see step 1 above
└── sites
    └── example.site.yml # Drush site alias file
... # Other project files and directories
```

### Add site information to alias file

You can add information about different instances or environments of your site in the *example.site.yml* file. For example, the following defines two aliases, `prod` and `stage`:

*example.site.yml*:

```
prod:
  host: prod.domain.com
  user: www-admin
  root: /path/to/drupal
  uri: https://www.example.com

stage:
  host: stage.domain.com
  user: www-admin
  root: /path/to/drupal
  uri: https://stage.example.com
```

Example derived from [Drupal Composer project's *drush/sites/self.site.yml*](https://github.com/drupal-composer/drupal-project/blob/8.x/drush/sites/self.site.yml).

The above defines two aliases, `prod` and `stage`, with the following information:

- **host**: The hostname to use when connecting over SSH. Note that this can be different from the site's URI!
- **user**: The remote username that can connect to the host over SSH
- **root**: The path on the remote server to our site's *docroot*
- **uri**: The URL of the site we're managing.

### (Optional) Create a Drush configuration file

If you want to save your alias file in a location other than a default discoverable location, such as *PROJECTROOT/drush/sites* or *DRUPALROOT/drush/sites*, you will first need to set up a Drush configuration file and specify the directory location of the site alias file(s) in the `drush.alias-path` key of your *drush.yml* configuration file.

Follow the instructions in [example.drush.yml](https://github.com/drush-ops/drush/blob/master/examples/example.drush.yml) under "Directories and Discovery" to create a *drush.yml* file in a Drush-discoverable location of your choice.

## Drush site aliases documentation

You can get basic help and command examples for Drush site aliases with the following command:

```
drush help site:alias
```

Or for more detailed documentation, use the Drush command:

```
drush topic docs:aliases
```

Which information is also contained in [example.site.yml](https://github.com/drush-ops/drush/blob/master/examples/example.site.yml) hosted in the *drush-ops/drush* repository.

## Recap

In this tutorial we learned what Drush site aliases are and how to add a site alias configuration file to our project or Drupal root's *drush/sites* directory. Our example site aliases file contained a collection of settings related to specific environments of our site, including the information required to connect to the site via SSH.

## Further your understanding

- Set up a site aliases file for a site you are currently working on.
- Learn how to set up and use the `config-pull` subcommand to download configuration from a remote site. See [Live vs. Local Configuration Management](https://drupalize.me/tutorial/live-vs-local-configuration-management).

## Additional resources

- [Example drush.yml to configure Drush settings](https://github.com/drush-ops/drush/blob/master/examples/example.drush.yml)
- [Example site.yml to configure Drush site aliases](https://github.com/drush-ops/drush/blob/master/examples/example.site.yml) (github.com)
- [Live vs. Local Configuration Management](https://drupalize.me/tutorial/live-vs-local-configuration-management) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Automating Drupal Tasks with Drush and Bash Scripts](/tutorial/automating-drupal-tasks-drush-and-bash-scripts?p=2593)

Next
[Drush Configuration](/tutorial/drush-configuration?p=2593)

Clear History

Ask Drupalize.Me AI

close