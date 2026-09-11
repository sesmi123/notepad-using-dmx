---
description: AI SDLC project configuration. Read by every prompt to determine workflow mode, ticketing provider, integration branch, production branch, and service credentials.
alwaysApply: true
---

# AI SDLC — Project Configuration

## Workflow

workflow:     sdlc

## Core Settings

ticketing:           none
branch_base:         main         # integration — feature PRs merge here
production_branch:   main         # production — releases, hotfixes, tags

## GitHub

owner:  {REQUIRED}
repo:   {REQUIRED}
