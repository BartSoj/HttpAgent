# Project Notes

---

## Discovered issues

### 2024-09-13: Does not use file search, sends incorrect API request

- **Description**: After asking to stop playing spotify, the program sends a request
  to "https://audio-service.example.com/stop" without checking spotify api files.
- Agent details:
    - **model**: `ft:gpt-4o-mini-2024-07-18:personal:http-agent-2024-09-12:A6cjB9mD`
- **Steps to Reproduce**:
    1. send message "{'method': 'POST', 'url': 'http://localhost:8000//', 'body': {'user_request': 'can you stop playing
       spotify'}}"
- **Cause**: unknown