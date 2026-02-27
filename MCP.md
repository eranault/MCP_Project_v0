This file serves as a protocol flow to make sure I understand how an MCP works. 

1. Claude connects to our MCP server
2. Claude asks: "What tools do we have?"
3. Server responds: "I have: analyze_cv, score_job_match, rewrite_bullets"
4. Claude decides to use analyze_cv
5. Claude sends: { "tool": "analyze_cv", "args": { "cv_text": "..." } }
6. Server runs our Python function
7. Our server sends back the result
8. Claude uses that result in its response to the user


We will use stdio for local  testing and streamble-http for deployment.

Architecture : 

┌─────────────────────────────────────────────────────┐
│                    Claude / AI Model                │
│         (the "brain" making decisions)              │
└─────────────────────┬───────────────────────────────┘
                      │  MCP Protocol (JSON-RPC)
                      ▼
┌─────────────────────────────────────────────────────┐
│                  MCP Server                    │
│  ┌──────────┐  ┌──────────┐  ┌─────────────────┐   │
│  │  Tools   │  │Resources │  │    Prompts      │   │
│  │(actions) │  │  (data)  │  │  (templates)    │   │
│  └────┬─────┘  └────┬─────┘  └────────┬────────┘   │
└───────┼─────────────┼─────────────────┼─────────────┘
        │             │                 │
        ▼             ▼                 ▼
┌─────────────────────────────────────────────────────┐
│              Business Logic                    │
│     (Anthropic API, databases, external APIs)       │
└─────────────────────────────────────────────────────┘



