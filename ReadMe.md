# PCO MCP

This is a small example MCP server for interacting with Planning Center Online.

Currently, it's limited to pulling information about upcoming plans in PCO services.

## Installation

This demo is intended to work with Claude desktop. To use it, make sure you have Claude desktop installed on your machine, as well as a current version of Python an [uv](https://docs.astral.sh/uv/getting-started/installation/).

Once you have these dependencies installed, rename the .env.example file to .env and fill in your PCO API credentials.

Then, run the `install.sh` script to configure Claude to use this MCP server. 