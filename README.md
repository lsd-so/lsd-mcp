# LSD MCP server

![Getting trending repositories using LSD](/media/github_trending.gif)

We treated Claude to psychedelic therapy on LSD and now it can just do things.

## Contents

* [Quickstart](#quickstart)
  * [Dependencies](#dependencies)
  * [Giving Claude LSD](#giving-claude-lsd)
  * [Claude on LSD](#claude-on-lsd)
  * [Failed to start MCP server](#failed-to-start-mcp-server)
* [What is MCP?](#what-is-mcp)
* [What is LSD?](#what-is-lsd)
* [Capabilities](#capabilities)

## Quickstart

### Dependencies

To run the MCP server, you'll need both [Python](https://www.python.org/) and [uv](https://docs.astral.sh/uv/) installed. To use the MCP server, you'll need to download either the [Claude desktop app](https://claude.ai/download) or [another MCP client](https://modelcontextprotocol.io/clients).

To use LSD, you'll need to sign up and [create an API key](https://lsd.so/profile) so your queries are privately associated to only your account. You can do so [for free with a Google account](https://lsd.so/connect).

### Giving Claude LSD

1. Clone this repository onto your computer

```
$ git clone https://github.com/lsd-so/lsd-mcp.git
$ cd lsd-mcp
```

2. Update the values in the `.env` file with `LSD_USER` containing the email you have an account on LSD with and `LSD_API_KEY` containing the API key you obtained from the profile page.

```
LSD_USER=<your_email_here>
LSD_API_KEY=<api_key_from_your_profile_page>
```

3. Give LSD to Claude

```
$ uv run mcp install app.py
```

4. Restart the Claude desktop app and, now, Claude should be able to do trippy things on LSD.

### Claude on LSD

If it's the first time in a chat session where you'd like to have Claude use LSD, because we're not popular enough to get caught in Anthropic's crawls, you'll need to first leverage our custom prompt which feeds in our documentation as part of the assistance.

![Using custom prompt](/media/prompt.gif)

See the [`write_lsd_sql` function](https://github.com/lsd-so/lsd-mcp/blob/main/app.py#L48) if you're interested in how it works but it just boils down to a [convenient rule we added to our SCAN keyword](https://lsd.so/docs/database/language/keywords/scan#example) enabling a developer or LLM to retrieve the documentation for our language in markdown ([if you'd like to run it yourself](https://lsd.so/app?query=SCAN%20https%3A%2F%2Flsd.so%2Fdocs)).

```
SCAN https://lsd.so/docs
```

### Failed to start MCP server

![Using custom prompt](/media/error.jpeg)

If you encounter error messages when starting Claude desktop along the lines of the following message:

```
Failed to start MCP server: Could not start MCP server LSD: Error: sapawn uv ENOENT
```

If this is your first time using an MCP server on your computer than, to remedy the error shown above, follow the instructions [under the **Add the Filesystem MCP Server** step](https://modelcontextprotocol.io/quickstart/user#2-add-the-filesystem-mcp-server) to create a `claude_desktop_config.json` file.

Then, in the location [where `claude_desktop_config.json` is stored](https://modelcontextprotocol.io/quickstart/user#2-add-the-filesystem-mcp-server) (is `~/Library/Application Support/Claude/claude_desktop_config.json` if you're running on a Mac), modify the value of the `command` key under `mcpServers -> LSD` to contain the full path to running `uv` (run `which uv` in your terminal if you don't already know what it is).

```diff
{
  "mcpServers": {
    "LSD": {
-      "command": "uv",
+      "command": "/Users/your_name/.local/bin/uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "--with",
        "psycopg2-binary",
        "mcp",
        "run",
        "/Users/y/testing-mcp/lsd-mcp/app.py"
      ]
    }
  }
}
```

Once you've done that, restart Claude desktop and the problem should be resolved. If not, please [file an issue](https://github.com/lsd-so/lsd-mcp/issues/new?template=Blank+issue).

## What is MCP?

MCP, short for [model context protocol](https://modelcontextprotocol.io/introduction), provides a communication layer between [Claude](https://claude.ai) and computer-accessible interfaces such as [the filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) or [web APIs](https://github.com/modelcontextprotocol/servers/tree/main/src/slack). If a limiting factor of LLMs was its detachment from the "real world" since it's just a text generating model, MCP allows users and developers to bring Claude to life.

## What is LSD?

LSD, a [DSL](https://en.wikipedia.org/wiki/Domain-specific_language) for the web, enables developers to connect the internet to your applications as though it were a [postgres compatible database](https://lsd.so/docs/database/postgres). Rather than present [a new semantic web ontology](https://xkcd.com/927/) or [make a new internet](https://urbit.org/), LSD SQL provides a dynamic declarative language that sits atop the existing one.

Designed to target browsers instead of [an architecture](https://llvm.org/), LSD allows for [powerful parallelization](https://lsd.so/docs/database/language/keywords/dive#example) while preserving simplicity with just-in-time tables meaning you can just get data without running a CREATE TABLE beforehand.

## Capabilities

From a high level, Claude can see, interact, and communicate with the web like a human. Here's a recording of Claude going to the MCP documentation, diving into the links corresponding to their SDKs, then returning the markdown content.
