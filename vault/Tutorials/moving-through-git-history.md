---
title: "Moving Through Git History"
url: "https://drupalize.me/tutorial/moving-through-git-history?p=1469"
guide: "[[command-line-tools-drupal]]"
---

# Moving Through Git History

## Content

Sprout Video

## Overview

There are a lot of different ways to reference a specific commit in Git. This lesson takes a look at the various ways in which you can navigate through the history of a project by cloning the Drupal core repository from Drupal.org and looking at its contents. We'll learn about pointers to each commit, or what Git refers to as a Treeish, and how we can use those as parameters to different commands.

The git log alias that Blake is using to pretty-up his log is:

```
lg = log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative
```

You can find out more about adding Git aliases in [Git Aliases and Other Fun Configuration](https://drupalize.me/tutorial/git-aliases-and-other-fun-configuration).

## Additional resources

- [Reference: gitrevisions](https://git-scm.com/docs/gitrevisions) (git-scm.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Working with Git Branches and Tags](/tutorial/working-git-branches-and-tags?p=1469)

Next
[Reviewing Changes and Using Git Diff](/tutorial/reviewing-changes-and-using-git-diff?p=1469)

Clear History

Ask Drupalize.Me AI

close