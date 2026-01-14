---
title: "Tail: Command Line Debugfree"
url: "https://drupalize.me/tutorial/tail-command-line-debug?p=880"
guide: "[[command-line-tools-drupal]]"
order: 44
---

# Tail: Command Line Debugfree

## Content

Sprout Video

This is an introduction to the Tail command, available on Unix/Linux systems. Tail has many applications, but this video concentrates on its basic usage and useful options, as they pertain to Drupal developers.

You'll learn how to take a quick peek at recent log messages from a single log file, how to do the same thing with multiple logs, as well as watching log files in real time! We'll finish up with a practical application, to see why this is useful.

Commands used in this video:

To view the documentation (or manual) for the tail command:  
`man tail`

To show the last 20 lines of the webserver's access log file:  
`tail /var/log/apache2/access.log`

To show the last 20 lines of the webserver's error log file:  
`tail /var/log/apache2/error.log`

To show the last 20 lines of the webserver's error log file and continue to print new lines added to the file:  
`tail -f /var/log/apache2/access.log`

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Setting up Bash Aliases](/tutorial/setting-bash-aliases?p=880)

Clear History

Ask Drupalize.Me AI

close