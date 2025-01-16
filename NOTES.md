# Project Notes

---

## Discovered issues

### 2024-09-13: Does not use file search, sends incorrect API request

- **Description**: After asking to stop playing spotify, the program sends a request
  to "https://audio-service.example.com/stop" without checking spotify api files.
- **Agent details**:
    - **model**: `ft:gpt-4o-mini-2024-07-18:personal:http-agent-2024-09-12:A6cjB9mD`
- **Steps to Reproduce**:
    1. send message "{'method': 'POST', 'url': 'http://localhost:8000//', 'body': {'user_request': 'can you stop playing
       spotify'}}"
- **Cause**: unknown

### 2025-01-11: Doesn't want to take actions in the correct order

- **Description**: After asking to stop playing spotify, tries immediately sending api request without know any api
  details. Even when implicitly stated to do that it checks the api info once but doesn't check it again with
  operation_id.
- Agent detail:
    - **model**: `gpt-4o-mini`
- **Steps to Reproduce**:
    1. Start discord server to send the request with discord.
    2. Send following message on discord so that it can read it:
       "I want you to pause spotify playback. In order to do that first check spotify for all operations, find one that
       pauses the playback, check api info again for this specific operation id, then send api request with the correct
       details. Then send me a response by checking the discord api and finding the operation to sand response with this
       api."
- **Cause**: Problems with executing actions step by step.
- **Possible fixes**: Decrease the size of function responses (e.g. return only operations_ids without summaries),
  split retrieve_api_info function into two functions one with operations_id, one without,
  add chain-of-thought reasoning and reprompting at each step.