
# Notepad REST API — Engineering Specification

## 1. Problem / Change

Build a small REST API for managing text notes.

The API must support the complete CRUD lifecycle for notes:

- Create a note
- Retrieve a note
- List notes
- Update a note
- Delete a note

The API must persist notes so that data survives application restarts.

The implementation should also include:

- Request validation
- Appropriate HTTP status codes
- Automated tests
- Clear separation between API, business logic, and persistence
- Consistent error responses
- A simple way to run the application and tests locally

The goal is to create a small but complete backend service that demonstrates a repeatable engineering workflow:

1. Understand the specification
2. Inspect the existing codebase
3. Plan the change
4. Implement the smallest required change
5. Run tests
6. Fix failures
7. Verify acceptance criteria
8. Report what changed and how it was verified


## 2. Expected Outcome

When the implementation is complete:

- A client can create, read, update, list, and delete notes through HTTP.
- Notes are persisted in a database or other explicitly configured persistent storage.
- Invalid requests are rejected with appropriate validation errors.
- Missing notes return an appropriate `404 Not Found` response.
- Successful operations return appropriate HTTP status codes.
- The API does not lose notes when the application restarts.
- Automated tests cover the main CRUD and validation behavior.
- The project can be built and tested using documented commands.
- The implementation follows the existing project structure and conventions.
- No unrelated parts of the application are changed.


## 3. Scope

### In scope

The implementation must provide:

- Note creation
- Note retrieval by ID
- Note listing
- Note update
- Note deletion
- Persistence
- Input validation
- Error handling
- Automated tests
- Basic API documentation

### Out of scope

Do not implement:

- User authentication
- User accounts
- Authorization
- Sharing notes between users
- Full-text search
- Tags
- Folders
- Rich text editing
- File attachments
- Real-time synchronization
- Pagination unless required by the existing project
- UI/frontend
- Cloud deployment

Do not add features that are not required by this specification.


## 4. Data Model

A note must contain at least:

```text
Note
----
id
title
content
created_at
updated_at
````

### ID

* Every note must have a unique identifier.
* The API must expose the identifier to clients.
* The implementation should use the ID-generation mechanism already established by the project, if one exists.

### Title

* Required.
* Must not be empty or whitespace-only.
* Maximum length: 200 characters.

### Content

* Required.
* Must not be empty or whitespace-only.
* Maximum length: 10,000 characters.

### Timestamps

`created_at`:

* Set when the note is created.
* Must not change during updates.

`updated_at`:

* Set when the note is created.
* Must be updated whenever the note is modified.

## 5. API Contract

### Create Note

```http
POST /notes
Content-Type: application/json
```

Request:

```json
{
  "title": "Shopping List",
  "content": "Milk, bread, and apples"
}
```

Expected successful response:

```http
201 Created
```

Response:

```json
{
  "id": "...",
  "title": "Shopping List",
  "content": "Milk, bread, and apples",
  "created_at": "...",
  "updated_at": "..."
}
```

### Get Note

```http
GET /notes/{id}
```

Expected successful response:

```http
200 OK
```

If the note does not exist:

```http
404 Not Found
```

### List Notes

```http
GET /notes
```

Expected successful response:

```http
200 OK
```

Response:

```json
[
  {
    "id": "...",
    "title": "...",
    "content": "...",
    "created_at": "...",
    "updated_at": "..."
  }
]
```

The API must return all stored notes unless the existing project already defines pagination or another listing convention.

### Update Note

```http
PUT /notes/{id}
Content-Type: application/json
```

Request:

```json
{
  "title": "Updated title",
  "content": "Updated content"
}
```

Expected successful response:

```http
200 OK
```

If the note does not exist:

```http
404 Not Found
```

The update must modify `updated_at`.

The `created_at` value must remain unchanged.

### Delete Note

```http
DELETE /notes/{id}
```

Expected successful response:

```http
204 No Content
```

After successful deletion, attempting to retrieve the note must return:

```http
404 Not Found
```

Deleting a nonexistent note must return:

```http
404 Not Found
```

## 6. Validation

The API must reject invalid note data.

At minimum, reject:

* Missing `title`
* Empty `title`
* Whitespace-only `title`
* Title longer than 200 characters
* Missing `content`
* Empty `content`
* Whitespace-only `content`
* Content longer than 10,000 characters
* Malformed JSON

Validation failures must:

* Return a client-error HTTP status, normally `400 Bad Request` or `422 Unprocessable Entity` according to the existing framework/project convention.
* Return a clear error response.
* Not create or modify a note.

## 7. Error Handling

Errors must use a consistent response structure.

Example:

```json
{
  "error": "Note not found"
}
```

Validation example:

```json
{
  "error": "Validation failed",
  "details": {
    "title": "Title must not be empty"
  }
}
```

The implementation should not expose stack traces, database internals, credentials, or other implementation details in API responses.

## 8. Persistence

Notes must be persisted.

Persistence must satisfy the following:

1. Creating a note stores it permanently in the configured storage.
2. Restarting the application does not remove existing notes.
3. Reading, updating, and deleting notes operate on persisted data.
4. The persistence layer must not be replaced by an in-memory-only implementation.
5. Tests may use an isolated test database/storage.

Use the project's existing persistence technology if one exists.

If no persistence technology exists, choose the simplest appropriate local persistence mechanism that:

* Requires minimal setup
* Supports the required CRUD operations
* Can be used reliably in automated tests
* Is suitable for a small REST API

## 9. Architecture / Design Constraints

Follow the existing architecture and conventions of the repository.

Before modifying code, inspect:

* Project structure
* Existing API endpoints
* Existing models/entities
* Existing database/repository patterns
* Existing error handling
* Existing validation patterns
* Existing test structure
* Existing configuration
* Build and test commands

### Separation of responsibilities

Keep these responsibilities separated where the existing architecture supports it:

```text
HTTP/API layer
      |
      v
Business/service layer
      |
      v
Persistence/repository layer
      |
      v
Database/storage
```

The API/controller layer should not contain database-specific implementation details.

Business logic should not depend directly on HTTP request/response objects unless the existing architecture explicitly uses that pattern.

The persistence layer should own database/storage operations.

## 10. Existing Code Must Be Preserved

Do not modify unrelated functionality.

Do not:

* Rename unrelated classes/functions
* Reformat unrelated files
* Upgrade dependencies unnecessarily
* Change the database technology unnecessarily
* Change API behavior unrelated to notes
* Remove existing tests
* Disable existing tests
* Modify CI configuration unless required
* Introduce a new framework when the existing framework can support the feature
* Add authentication or authorization
* Add frontend code

If an existing pattern can be reused, reuse it instead of creating a competing pattern.

## 11. Testing Requirements

Automated tests must cover at least:

### Create

* Create a valid note.
* Verify `201 Created`.
* Verify returned note contains an ID.
* Verify title and content are persisted.

### Read

* Retrieve an existing note.
* Verify `200 OK`.
* Verify returned data matches stored data.
* Retrieve a nonexistent note.
* Verify `404 Not Found`.

### List

* List notes.
* Verify `200 OK`.
* Verify created notes appear in the response.

### Update

* Update an existing note.
* Verify `200 OK`.
* Verify updated title/content.
* Verify `updated_at` changes.
* Verify `created_at` does not change.
* Update a nonexistent note.
* Verify `404 Not Found`.

### Delete

* Delete an existing note.
* Verify `204 No Content`.
* Verify the note can no longer be retrieved.
* Delete a nonexistent note.
* Verify `404 Not Found`.

### Validation

Test invalid:

* Missing title
* Empty title
* Whitespace-only title
* Title exceeding maximum length
* Missing content
* Empty content
* Whitespace-only content
* Content exceeding maximum length
* Malformed JSON

### Persistence

At least one test must demonstrate that data is stored using the actual persistence mechanism rather than only an in-memory data structure.

## 12. Test Isolation

Tests must not depend on:

* Manually created database records
* Another developer's local environment
* Test execution order
* A running production service
* External services unless explicitly required

Tests should create their own required data and clean up after themselves.

Tests must be repeatable.

Running the test suite multiple times should produce the same result.

## 13. Configuration

Configuration must not contain hard-coded secrets.

If persistence requires configuration, use the project's existing configuration mechanism.

Local development configuration should be documented.

Test configuration should be isolated from production/development data where practical.

## 14. API Documentation

Document:

* Available endpoints
* HTTP methods
* Request formats
* Response formats
* Validation rules
* Error behavior
* How to run the API
* How to run tests

Use the existing documentation mechanism if one exists.

If the project already uses OpenAPI/Swagger, update it instead of creating separate API documentation.

## 15. Engineering Workflow

The implementation must follow this workflow.

### Step 1 — Inspect

Before writing code, inspect the repository.

Identify:

* Language and framework
* Application entry point
* Existing API structure
* Persistence mechanism
* Model/entity conventions
* Test framework
* Configuration mechanism
* Build/test commands

Do not assume these details.

### Step 2 — Plan

Create a short implementation plan containing:

1. Files/components that need to change
2. New files/components that need to be created
3. Data model changes
4. API changes
5. Persistence changes
6. Tests that will be added
7. Documentation changes

Keep the plan minimal and directly tied to this specification.

### Step 3 — Implement

Implement the smallest change that satisfies the specification.

Prefer:

* Existing project patterns
* Existing dependencies
* Small changes
* Simple designs
* Reusable components

Do not implement speculative features.

### Step 4 — Test

Run the existing test suite.

Then run the newly added tests.

If tests fail:

1. Determine whether the failure is caused by the implementation.
2. Fix the implementation.
3. Re-run the relevant tests.
4. Re-run the full test suite.

Do not simply weaken or remove a test to make it pass.

### Step 5 — Verify

Verify every acceptance criterion.

Do not claim an acceptance criterion is satisfied unless it has been tested or otherwise directly verified.

### Step 6 — Report

The final implementation report should contain:

```text
Summary
- What was implemented

Files changed
- List of important files

Tests
- Commands executed
- Test results

Acceptance criteria
- PASS/FAIL for each criterion

Notes
- Any assumptions
- Any limitations
- Any follow-up work
```

# 16. Acceptance Criteria

## AC-1 — Create a note

Given a valid title and content,

when the client sends `POST /notes`,

then the API creates and persists the note,

and returns `201 Created` with the created note.

## AC-2 — Unique note ID

Every created note has a unique ID.

## AC-3 — Retrieve a note

Given an existing note,

when the client sends `GET /notes/{id}`,

then the API returns `200 OK` and the correct note.

## AC-4 — Missing note

Given an ID that does not exist,

when the client sends `GET /notes/{id}`,

then the API returns `404 Not Found`.

## AC-5 — List notes

Given multiple persisted notes,

when the client sends `GET /notes`,

then the API returns `200 OK` and includes the persisted notes.

## AC-6 — Update a note

Given an existing note,

when the client sends `PUT /notes/{id}` with valid data,

then the API updates the note and returns `200 OK`.

## AC-7 — Preserve creation timestamp

When a note is updated,

then `created_at` remains unchanged.

## AC-8 — Update modification timestamp

When a note is updated,

then `updated_at` reflects the update.

## AC-9 — Update missing note

Given an ID that does not exist,

when the client sends `PUT /notes/{id}`,

then the API returns `404 Not Found`.

## AC-10 — Delete a note

Given an existing note,

when the client sends `DELETE /notes/{id}`,

then the API deletes the note and returns `204 No Content`.

## AC-11 — Deleted note is unavailable

After a note is successfully deleted,

when the client requests that note,

then the API returns `404 Not Found`.

## AC-12 — Delete missing note

Given an ID that does not exist,

when the client sends `DELETE /notes/{id}`,

then the API returns `404 Not Found`.

## AC-13 — Validate title

The API rejects notes with:

* Missing title
* Empty title
* Whitespace-only title
* Title longer than 200 characters

## AC-14 — Validate content

The API rejects notes with:

* Missing content
* Empty content
* Whitespace-only content
* Content longer than 10,000 characters

## AC-15 — Validation does not modify data

When validation fails,

then no note is created or modified.

## AC-16 — Consistent errors

API errors use the documented error-response structure.

## AC-17 — Persistence survives restart

Given a persisted note,

when the API is stopped and restarted,

then the note remains available.

## AC-18 — Automated tests

Automated tests cover:

* Create
* Read
* List
* Update
* Delete
* Missing resources
* Validation
* Persistence

## AC-19 — Tests are repeatable

The complete test suite can be executed repeatedly without requiring manual setup or producing inconsistent results.

## AC-20 — Existing functionality remains intact

All existing tests pass after the implementation.

No unrelated API behavior is changed.

## AC-21 — Documentation

A developer can determine from the project documentation:

* How to start the API
* How to run the tests
* What endpoints are available
* What request/response formats are expected
* What validation rules apply

# 17. Definition of Done

The work is considered complete only when:

* [ ] All required CRUD endpoints exist.
* [ ] Notes are persisted.
* [ ] Validation is implemented.
* [ ] Error handling is implemented.
* [ ] Automated tests are present.
* [ ] All tests pass.
* [ ] Persistence behavior is tested.
* [ ] Existing tests still pass.
* [ ] API documentation is updated.
* [ ] Every acceptance criterion has been verified.
* [ ] No unrelated functionality was changed.
* [ ] The final implementation report lists the tests that were executed.

```
