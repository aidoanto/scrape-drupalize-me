---
title: "Overview: Drush's Output Formatting System"
url: "https://drupalize.me/tutorial/overview-drushs-output-formatting-system?p=2593"
guide: "[[command-line-tools-drupal]]"
order: 15
---

# Overview: Drush's Output Formatting System

## Content

Some Drush commands return a lot of information -- lists of modules, generators, and status reports, for example. It might be hard to find a property you need in the small command window output. Luckily, the output of Drush commands can be piped to other commands, used as a source for imports, settings for CI, and other DevOps tasks.

In order to accommodate all these different use cases, Drush comes with a formatting system that allows you to format and filter output to meet your needs. This system allows to you specify what fields you want returned when the output contains more than one field. It also allows Drush command output to be formatted as JSON, XML, raw PHP, a table, and more.

In this tutorial we'll:

- Learn how to specify the output format -- and what formats are available
- Limit the fields that are returned in a report
- Learn to filter the output to only the data we're interested in

By the end of this tutorial you'll know how to format a Drush command's output to fit your needs.

## Goal

Introduce Drush's output formatting system and illustrate some common use cases.

## Prerequisites

- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)
- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)

## Drush output formats

Drush commands may produce output that can be rendered in a variety of different ways using the Drush formatting system. Drush commands that support output formats have a `--format` option specified in the command help.

All available formats are listed in the command's help text in the abbreviated version. To see the full version of the output you need to pass the `--verbose` option to the `drush help` command.

For instance, if you run `drush help status` in the command line in the root of your Drupal project you may see something like the following:

```
…
 --format=<json>    Select output format. Available: json, list, var_export, yaml. Default is key-value
…
```

If you add the `--verbose` option to the command like so: `drush help status --verbose` then the `--format` option provides more information:

```
--format=<json> Select output format.

    All available values are:                                       
    - config: A configuration file in executable php format. The variable name is "config", and the variable keys are taken from the output data array's keys.

    - json: Javascript Object Notation.                      
    - list: A simple list of values.
    - php: A serialized php string.
    - print-r: Output via php print_r function.
    - var_export: An array in executable php format.
    - yaml: Yaml output format.

    Default is key-value.
```

The `help` command's output also specifies the default format. In the case of the `drush status` command the default output format is a key-value pair.

## Common available `--format` values

The Drush `--format` flag typically accepts the following options:

- *config* - Outputs a configuration file in executable PHP format. The variable name is "config", and the variable keys are taken from the output data array's keys
- *JSON* - Returns JSON formatted output that can be used as a JSON object
- *list* - A list of values
- *PHP* - A serialized PHP string
- *print-r*- Output via PHP's `print_r()` function
- *var\_export* - An array in executable PHP format
- *yaml* - YAML output format

Let's see the `--format` option in action. In the command line, run `drush status --format=json`. You should see something like shown below:

```
{
    "drupal-version": "9.2.6",
    "uri": "https://user-guide-tests.ddev.site",
    "db-driver": "mysql",
    "db-hostname": "db",
    "db-port": 3306,
    "db-username": "db",
    "db-name": "db",
    "db-status": "Connected",
    "bootstrap": "Successful",
    "theme": "bartik",
    "admin-theme": "seven",
    "php-bin": "/usr/bin/php7.4",
    "php-conf": {
        "/etc/php/7.4/cli/php.ini": "/etc/php/7.4/cli/php.ini"
    },
    "php-os": "Linux",
    "drush-script": "/var/www/html/vendor/drush/drush/drush",
    "drush-version": "10.6.0",
    "drush-temp": "/tmp",
    "drush-conf": [
        "/var/www/html/vendor/drush/drush/drush.yml"
    ],
    "install-profile": "standard",
    "root": "/var/www/html/web",
    "site": "sites/default",
    "files": "sites/default/files",
    "temp": "/tmp"
}
```

Compare it to the standard `drush status` command output. Run `drush status` in the terminal.

```
 Drupal version   : 9.2.6
 Site URI         : https://user-guide-tests.ddev.site
 DB driver        : mysql
 DB hostname      : db
 DB port          : 3306
 DB username      : db
 DB name          : db
 Database         : Connected
 Drupal bootstrap : Successful
 Default theme    : bartik
 Admin theme      : seven
 PHP binary       : /usr/bin/php7.4
 PHP config       : /etc/php/7.4/cli/php.ini
 PHP OS           : Linux
 Drush script     : /var/www/html/vendor/drush/drush/drush
 Drush version    : 10.6.0
 Drush temp       : /tmp
 Drush configs    : /var/www/html/vendor/drush/drush/drush.yml
 Install profile  : standard
 Drupal root      : /var/www/html/web
 Site path        : sites/default
 Files, Public    : sites/default/files
 Files, Temp      : /tmp
```

While key value format (the 2nd example) is more readable, JSON format is more useful for integrations and further development tasks. For example, pipe the output to the `jq` command for further processing:

```
drush status --format=json | jq '."db-status"'
# Connected
```

## Limit the fields in the output

The Drush output formatting system provides a `--fields` option that allows you to specify which fields to include in the output and in what order. For example `drush status --fields=drupal-version,uri` will return only 2 fields: *Drupal version* and *Site URI*. If you are unsure about field names, you can check them in the JSON formatted output.

```
 Drupal version : 8.9.13                      
 Site URI       : http://drupal.dev.localhost
```

You can combine the `--fields` option with the `--format` option. `drush status --fields=drupal-version,uri --format=json`. This will return the 2 selected fields and their values formatted as a JSON object.

```
{
    "drupal-version": "8.9.13",
    "uri": "http://drupal.dev.localhost"
}
```

## Filtering the output

Some Drush commands that provide output as a table support a `--filter` option that allows rows from the output to be selected with simple expressions.

In its simplest form, the `--filter` option takes a string that indicates the value to filter by in the command's default filter field. Not all commands have the default filter field. Most commands will pass a key value pair, with the key being the name of the field, and the value being the value to filter by.

For example, we can filter all modules in the `drush pm:list` output by values in one of the output fields. Running `drush pm:list --filter='package=custom'` will return a list of all custom modules on the site:

```
--------- --------------------------------- ---------- ---------
  Package   Name                              Status     Version  
 --------- --------------------------------- ---------- ---------
  custom    Custom Layouts (custom_layouts)   Enabled             
  Custom    Views Header Link (header_link)   Enabled             
  Custom    News (news)                       Enabled             
  Custom    Recipe (recipe)                   Enabled             
  Custom    Slider (slider)                   Enabled             
  Custom    subscriber (subscriber)           Enabled             
  Custom    test (test)                       Disabled            
  Custom    Custom title sort (title_sort)    Enabled             
 --------- --------------------------------- ---------- ---------
```

In more advanced use cases you may want to use special operators. For example, use the `*=` operator to partially match the value.

For example `drush pm:list --filter='name*=Views'` will return all modules that have the word "Views" present in the module's name:

```
 ------------------ -------------------------------- ---------- ---------- 
  Package            Name                             Status     Version   
 ------------------ -------------------------------- ---------- ---------- 
  Core               Views (views)                    Enabled    8.9.13    
  Core               Views UI (views_ui)              Enabled    8.9.13    
  Chaos tool suite   Chaos Tools Views                Enabled    8.x-3.4   
  (Experimental)     (ctools_views)                                        
  SEO                Metatag: Views (metatag_views)   Disabled   8.x-1.14  
 ------------------ -------------------------------- ---------- ----------
```

Use the `~=` operator to pass regular expressions to the `--filter` option.

To return all modules that have the word "Views" or "Title" in their name run the following `drush pm:list --filter='name~=#(views|title)#i'`:

```
------------------ -------------------------------- ---------- ---------- 
  Package            Name                             Status     Version   
 ------------------ -------------------------------- ---------- ---------- 
  Core               Views (views)                    Enabled    8.9.13    
  Core               Views UI (views_ui)              Enabled    8.9.13    
  Chaos tool suite   Chaos Tools Views                Enabled    8.x-3.4   
  (Experimental)     (ctools_views)                                        
  SEO                Metatag: Views (metatag_views)   Disabled   8.x-1.14  
  Custom             Custom title sort (title_sort)   Enabled              
 ------------------ -------------------------------- ---------- ----------
```

Filter conditions for different fields can be combined by using `&&` and `||` options for `AND` and `OR` conjunctions, respectively.

The Drush `--filter` option is very similar to the `grep` command, but unlike `grep` it performs a semantic search -- a search with respect to specified fields. In contrast, `grep` performs a line search and searches without respect for data semantics. `grep` is more useful when you don't know in what field the value might be present, while the `--filter` option returns more specific results based on the fields.

## Recap

The Drush output formatting system provides options that can be used by the majority of Drush commands to format, filter, and limit the output of the commands. It's especially useful in cases where the output of a command needs to be further processed or used for integrations with CI, migrations, import or any other DevOps tasks.

To see what output options are available for a specific command, use the `drush help` command with the `--verbose` flag.

## Further your understanding

- Can you filter the output of `drush pm:list` for custom modules using `grep`?
- Why do some commands take `--format`, `--fields`, and `--filter` options and some do not?
- Try out the different `--format` options like `var_dump`, `php`, and `print_r` with the `drush status` command. In what scenarios would you use these other options?

## Additional resources

- [Drush official documentation](https://www.drush.org) (drush.org)
- [Drush Git repository](https://github.com/drush-ops/drush) (github.com)
- [Grep documentation](https://www.gnu.org/software/grep/manual/grep.html) (gnu.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Use Drush to Deploy Drupal Updates](/tutorial/use-drush-deploy-drupal-updates?p=2593)

Next
[Automating Drupal Tasks with Drush and Bash Scripts](/tutorial/automating-drupal-tasks-drush-and-bash-scripts?p=2593)

Clear History

Ask Drupalize.Me AI

close