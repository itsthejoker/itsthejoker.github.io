---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true
summary: "This post is about...?"
categories:
  - projects
  - writing
  - thoughts
tags:
  - raspberry pi
  - upcycling
  - terminal
  - perl
---

# Title

{{< lead >}}
Impactful start to the post!
{{< /lead >}}

Remember that you can link to other pages with [link]({{< ref "docs/page_name_without_md" >}})