# Project Brief

## Project name

dmx-playground — Notepad REST API

## What it does

A small REST API for managing text notes. Clients create, read, list, update, and delete notes over HTTP. Notes persist across application restarts.

This repository is also a local playground for learning dmx (AI SDLC loops) by implementing that API.

## Primary goals

- Deliver a complete CRUD notes API with validation, consistent errors, automated tests, and basic API docs.
- Keep the service small and local: easy to run and test on a developer machine.
- Practice a repeatable engineering workflow: spec → plan → implement the smallest change → test → verify acceptance criteria.

## Scope

**In this codebase**

- Note CRUD (`POST/GET/PUT/DELETE /notes`, `GET /notes/{id}`)
- Persistence that survives restart
- Request validation and consistent error responses
- Automated tests for CRUD, validation, missing resources, and persistence
- Basic API documentation (how to run, endpoints, request/response, validation)

**Not in this codebase**

- Authentication, accounts, authorization
- Sharing, search, tags, folders, rich text, attachments, realtime sync
- Frontend / UI
- Cloud deployment
- Pagination unless a later implementation choice requires it
