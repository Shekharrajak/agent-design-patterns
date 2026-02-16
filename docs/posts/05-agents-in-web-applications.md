---
description: Full-stack agent architecture, streaming UIs, background jobs, and frontend patterns.
---

# Agents in Web Applications

<small>Part 5 of 9 in the **Agent Design Patterns** series</small>

---

## Full-Stack Agent Architecture

```mermaid
graph TD
    subgraph FRONTEND["Frontend"]
        UI["UI Layer<br/>React / Next.js"]
        STREAM["Streaming Response Handler<br/>Server-Sent Events / WebSocket"]
        STATE["Client State<br/>Agent conversation history"]
        UI --- STATE
    end

    subgraph BACKEND["Backend"]
        API["API Layer<br/>REST / GraphQL"]
        AGENT["Agent Runtime<br/>──────<br/>Reasoning loop<br/>Tool orchestration<br/>Memory management"]
        QUEUE["Task Queue<br/>Long-running agent jobs"]
    end

    subgraph INFRA["Infrastructure"]
        LLM_API["LLM Provider<br/>Claude / GPT / Local"]
        VS["Vector Store"]
        DB["Application DB"]
        CACHE["Cache Layer"]
    end

    UI --> API
    API --> AGENT
    AGENT --> STREAM
    STREAM --> UI
    AGENT --> QUEUE
    AGENT --> LLM_API
    AGENT --> VS
    AGENT --> DB
    AGENT --> CACHE

    style FRONTEND fill:#f5f5f5,stroke:#616161
    style BACKEND fill:#e0e0e0,stroke:#424242
    style INFRA fill:#bdbdbd,stroke:#212121
    style AGENT fill:#9e9e9e,stroke:#000,color:#fff,stroke-width:2px
```

---

## Request Lifecycle: Traditional vs Agent-Driven

```mermaid
sequenceDiagram
    participant U as Browser
    participant API as API Server
    participant A as Agent Runtime
    participant LLM as LLM API
    participant T as Tools
    participant DB as Database

    Note over U,DB: Traditional: single request-response
    U->>API: POST /api/report
    API->>DB: Query data
    DB-->>API: Results
    API-->>U: JSON response (200ms)

    Note over U,DB: Agent-driven: multi-step, streamed
    U->>API: POST /api/agent/report
    API->>A: Start agent task
    A->>LLM: Plan report structure
    LLM-->>A: Plan (3 sections)
    A-->>U: [stream] Planning complete...
    A->>T: SQL query for section 1
    T-->>A: Data
    A->>LLM: Analyze data
    LLM-->>A: Analysis
    A-->>U: [stream] Section 1 ready...
    A->>T: SQL query for section 2
    T-->>A: Data
    A->>LLM: Analyze + reflect
    LLM-->>A: Revised analysis
    A-->>U: [stream] Section 2 ready...
    A->>LLM: Synthesize final report
    LLM-->>A: Report
    A-->>U: [stream] Complete (4.2s total)
```

---

## Where Agents Sit in Common Web Architectures

```mermaid
graph TD
    subgraph SPA["Single Page App"]
        SPA_UI["React SPA"] --> SPA_API["API Server"]
        SPA_API --> SPA_AGENT["Agent<br/>as backend service"]
    end

    subgraph SSR["Server-Side Rendered"]
        SSR_UI["Next.js / Nuxt"] --> SSR_AGENT["Agent<br/>in server actions"]
        SSR_AGENT --> SSR_LLM["LLM"]
    end

    subgraph EDGE["Edge + Agent"]
        EDGE_CDN["CDN / Edge"] --> EDGE_ROUTER["Agent Router<br/>at edge"]
        EDGE_ROUTER -->|simple| EDGE_FAST["Cache / static"]
        EDGE_ROUTER -->|complex| EDGE_ORIGIN["Origin + Agent"]
    end

    subgraph REALTIME["Real-Time / Collaborative"]
        RT_WS["WebSocket Server"]
        RT_WS --> RT_AGENT["Agent per session"]
        RT_AGENT --> RT_SHARED["Shared Context Store"]
    end

    style SPA fill:#f5f5f5,stroke:#616161
    style SSR fill:#e0e0e0,stroke:#424242
    style EDGE fill:#bdbdbd,stroke:#212121
    style REALTIME fill:#9e9e9e,stroke:#000,color:#fff
```

---

## Background Agent Jobs

```mermaid
graph LR
    subgraph SYNC["Synchronous (blocking)"]
        REQ1["Request"] --> AGENT1["Agent<br/>runs inline"] --> RES1["Response<br/>Acceptable for under 5s tasks"]
    end

    subgraph ASYNC["Asynchronous (non-blocking)"]
        REQ2["Request"] --> ENQUEUE["Enqueue job"]
        ENQUEUE --> RES2["202 Accepted<br/>+ job ID"]
        ENQUEUE --> WORKER["Background Worker<br/>Agent runs here"]
        WORKER --> NOTIFY["Notify via<br/>WebSocket / webhook"]
    end

    style SYNC fill:#f5f5f5,stroke:#616161
    style ASYNC fill:#e0e0e0,stroke:#424242
```

| Approach | Latency Budget | Use Case |
|----------|---------------|----------|
| Synchronous | Under 5 seconds | Classification, routing, simple Q&A |
| Streaming | Under 30 seconds | Report generation, code writing |
| Background + notify | Minutes to hours | Data analysis, batch processing, multi-agent tasks |

---

## Authentication and Authorization for Agent Tools

```mermaid
graph TD
    USER["Authenticated User<br/>JWT / session"] --> API["API Layer<br/>Validates token"]
    API --> AGENT["Agent Runtime"]
    AGENT --> TOOLS["Tool Calls"]

    TOOLS --> T1["DB Query<br/>Scoped to user's data"]
    TOOLS --> T2["Email Send<br/>Requires explicit consent"]
    TOOLS --> T3["File Write<br/>Sandboxed directory"]
    TOOLS --> T4["External API<br/>Service account, audited"]

    AGENT -.-> AUDIT["Audit Log<br/>Every tool call recorded<br/>with user context"]

    style AGENT fill:#bdbdbd,stroke:#212121,stroke-width:2px
    style AUDIT fill:#9e9e9e,stroke:#000,color:#fff
```

Every tool call inherits the user's permission scope.
No tool call executes without an audit trail.

---

## Frontend Patterns for Agent UIs

```mermaid
graph LR
    P1["Streaming Text<br/>──────<br/>Token-by-token display<br/>SSE / WebSocket"] --> P2["Step Indicator<br/>──────<br/>Show reasoning steps<br/>Planning, Searching, Writing"] --> P3["Tool Call Visibility<br/>──────<br/>Show what the agent called<br/>Collapsible detail panels"] --> P4["Human Checkpoint<br/>──────<br/>Pause for confirmation<br/>before irreversible actions"] --> P5["Progress + Cancel<br/>──────<br/>Estimated time remaining<br/>Abort button with cleanup"]

    style P1 fill:#f5f5f5,stroke:#616161
    style P2 fill:#e0e0e0,stroke:#424242
    style P3 fill:#bdbdbd,stroke:#212121
    style P4 fill:#9e9e9e,stroke:#000,color:#fff
    style P5 fill:#616161,stroke:#000,color:#fff
```

---

```
 Web applications with agents shift from
 request-response to request-observe-stream.
 The frontend becomes a dashboard for agent activity.
 The backend becomes a runtime for agent execution.
```
