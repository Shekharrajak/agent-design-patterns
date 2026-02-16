---
description: Communication topologies, scaling strategies, state management, and failure modes.
---

# Multi-Agent System Architecture

<small>Part 6 of 9 in the **Agent Design Patterns** series</small>

---

## Communication Topologies

```mermaid
graph TB
    subgraph STAR["Star / Hub-Spoke"]
        direction TB
        SH["Hub Agent"] --> SS1["Worker"]
        SH --> SS2["Worker"]
        SH --> SS3["Worker"]
    end

    subgraph MESH["Full Mesh"]
        direction TB
        MA["Agent A"] <--> MB["Agent B"]
        MB <--> MC["Agent C"]
        MA <--> MC
    end

    subgraph PIPE["Pipeline"]
        direction LR
        PA["Agent A"] --> PB["Agent B"] --> PC["Agent C"]
    end

    subgraph TREE["Hierarchical Tree"]
        direction TB
        TL["Leader"]
        TL --> TM1["Manager"]
        TL --> TM2["Manager"]
        TM1 --> TW1["Worker"]
        TM1 --> TW2["Worker"]
        TM2 --> TW3["Worker"]
    end

    style STAR fill:#f5f5f5,stroke:#616161
    style MESH fill:#e0e0e0,stroke:#424242
    style PIPE fill:#bdbdbd,stroke:#212121
    style TREE fill:#9e9e9e,stroke:#000,color:#fff
```

| Topology | Message Complexity | Fault Tolerance | Best For |
|----------|-------------------|-----------------|----------|
| Star | O(n) | Low (hub is SPOF) | Orchestrated tasks |
| Mesh | O(n^2) | High | Debate, negotiation |
| Pipeline | O(n) | Low | Sequential processing |
| Tree | O(n log n) | Medium | Large-scale delegation |

---

## Debate Pattern: Improving Factual Accuracy

```mermaid
sequenceDiagram
    participant P as Proposer Agent
    participant O as Opponent Agent
    participant J as Judge Agent

    P->>J: Claim: "X is true because A, B, C"
    J->>O: Evaluate this claim
    O->>J: Counter: "B is incorrect, evidence D contradicts it"
    J->>P: Address the counter-argument
    P->>J: Revised: "X is true because A, C, and E"
    J->>J: Evaluate both positions
    J-->>J: Verdict: Accept revised claim
```

Debate reduces hallucination. Opposing agents surface weaknesses
that self-reflection often misses.

---

## Scaling Multi-Agent Systems

```mermaid
graph TD
    subgraph SMALL["Small Scale: In-Process"]
        S_ORCH["Orchestrator"] --> S_W1["Worker"]
        S_ORCH --> S_W2["Worker"]
        S_NOTE["Same process<br/>Function calls<br/>Shared memory"]
    end

    subgraph MEDIUM["Medium Scale: Message Queue"]
        M_ORCH["Orchestrator"] --> MQ["Message Queue"]
        MQ --> M_W1["Worker Pod"]
        MQ --> M_W2["Worker Pod"]
        MQ --> M_W3["Worker Pod"]
        M_NOTE["Separate processes<br/>Async messages<br/>Horizontal scaling"]
    end

    subgraph LARGE["Large Scale: Distributed Agents"]
        L_LB["Load Balancer"]
        L_LB --> L_O1["Orchestrator"]
        L_LB --> L_O2["Orchestrator"]
        L_O1 --> L_MQ["Distributed Queue"]
        L_O2 --> L_MQ
        L_MQ --> L_W["Auto-scaled<br/>Worker Fleet"]
        L_W --> L_STORE["Distributed State Store"]
        L_NOTE["Multi-region<br/>Durable execution<br/>State externalized"]
    end

    SMALL --> MEDIUM --> LARGE

    style SMALL fill:#f5f5f5,stroke:#616161
    style MEDIUM fill:#e0e0e0,stroke:#424242
    style LARGE fill:#bdbdbd,stroke:#212121
```

---

## Agent Communication Protocol Layers

```mermaid
graph TB
    subgraph LAYERS["Communication Stack"]
        L4["Application Layer<br/>──────<br/>Task descriptions, results, feedback<br/>Natural language or structured JSON"]
        L3["Semantic Layer<br/>──────<br/>Intent classification, entity extraction<br/>Shared ontology between agents"]
        L2["Transport Layer<br/>──────<br/>HTTP, gRPC, WebSocket, message queue<br/>Serialization, compression"]
        L1["Infrastructure Layer<br/>──────<br/>Service discovery, load balancing<br/>TLS, authentication"]
    end

    L4 --> L3 --> L2 --> L1

    style L4 fill:#f5f5f5,stroke:#616161
    style L3 fill:#e0e0e0,stroke:#424242
    style L2 fill:#bdbdbd,stroke:#212121
    style L1 fill:#9e9e9e,stroke:#000,color:#fff
```

---

## State Management in Multi-Agent Systems

```mermaid
graph LR
    subgraph OPTIONS["State Strategies"]
        direction TB
        STATELESS["Stateless Agents<br/>──────<br/>All state in messages<br/>Easy to scale<br/>Limited context"]
        
        EXTERNAL["Externalized State<br/>──────<br/>Redis / DynamoDB<br/>Agents read/write shared store<br/>Consistency challenges"]
        
        EVENT_SOURCED["Event-Sourced<br/>──────<br/>All agent actions = events<br/>Replay to rebuild state<br/>Full audit trail"]
    end

    style STATELESS fill:#f5f5f5,stroke:#616161
    style EXTERNAL fill:#e0e0e0,stroke:#424242
    style EVENT_SOURCED fill:#bdbdbd,stroke:#212121
```

| Strategy | Scalability | Debuggability | Complexity |
|----------|------------|---------------|------------|
| Stateless | High | Low | Low |
| Externalized | High | Medium | Medium |
| Event-Sourced | High | High | High |

---

## Failure Modes in Multi-Agent Systems

```mermaid
graph TD
    subgraph FAILURES["Failure Taxonomy"]
        F1["Infinite Loop<br/>──────<br/>Two agents keep<br/>delegating to each other"]
        F2["Cascade Failure<br/>──────<br/>One agent's bad output<br/>poisons all downstream"]
        F3["Deadlock<br/>──────<br/>Agent A waits for B<br/>B waits for A"]
        F4["Resource Exhaustion<br/>──────<br/>Uncontrolled spawning<br/>of sub-agents"]
        F5["State Divergence<br/>──────<br/>Agents disagree on<br/>shared state"]
    end

    F1 --> MIT1["Mitigation: max iteration count"]
    F2 --> MIT2["Mitigation: output validation gates"]
    F3 --> MIT3["Mitigation: timeouts on all waits"]
    F4 --> MIT4["Mitigation: agent pool with hard limit"]
    F5 --> MIT5["Mitigation: single source of truth store"]

    style FAILURES fill:#e0e0e0,stroke:#424242
```

---

```
 Multi-agent systems are distributed systems.
 They inherit every problem of distributed computing:
 partial failure, network partitions, state consistency.
 Design for failure from the start.
```
