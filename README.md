# LSD MCP server

GIF with claude taking in some prompt and then doing LSD things in background before surfacing back to user some impressive information

We treated Claude to psychedelic therapy on LSD and now it can just do things.

## Contents

* [Quickstart](#quickstart)
* [What is MCP?](#what-is-mcp)
* [What is LSD?](#what-is-lsd)
* [Capabilities](#capabilities)

## Quickstart

You'll need both [Python](https://www.python.org/) and the [Claude desktop app](https://claude.ai/download) installed. To get started, clone this repository onto your computer.

```bash
$ git clone git@github.com:lsd-so/mcp.git
```

## What is MCP?

MCP, short for [model context protocol](https://modelcontextprotocol.io/introduction), provides a communication layer between [Claude](https://claude.ai) and computer-accessible interfaces such as [the filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) or [web APIs](https://github.com/modelcontextprotocol/servers/tree/main/src/slack). If a limiting factor of LLMs was its detachment from the "real world" since it's just a text generating model, MCP allows users and developers to bring Claude to life.

## What is LSD?

LSD, a [DSL](https://en.wikipedia.org/wiki/Domain-specific_language) for the web, enables developers to connect the internet to your applications as though it were a [postgres compatible database](https://lsd.so/docs/database/postgres). Rather than present [a new semantic web ontology](https://xkcd.com/927/) or [make a new internet](https://urbit.org/), LSD SQL provides a dynamic declarative language that sits atop the existing one.

Designed to target browsers instead of [an architecture](https://llvm.org/), LSD allows for [powerful parallelization](https://lsd.so/docs/database/language/keywords/dive#example) while preserving simplicity with just-in-time tables meaning you can just get data without running a CREATE TABLE beforehand.

## Capabilities

From a high level, Claude can see, interact, and communicate with the web like a human. Here's an example of Claude writing LSD SQL to make an order on OpenTable.
