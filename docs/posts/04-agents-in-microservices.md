---
description: Sidecars, semantic discovery, adaptive sagas, and deployment topology for agent-augmented services.
---

# Agents in Microservice Architecture

<small>Part 4 of 9 in the **Agent Design Patterns** series</small>

---

## Where Agents Fit in a Microservice Stack

```mermaid
graph TD
    CLIENT["Client"]
    CLIENT --> GW["API Gateway"]

    GW --> AGENT_LAYER["Agent Layer<br/>──────<br/>Routing Agent<br/>classifies and dispatches"]

    AGENT_LAYER --> SVC_A["Service A<br/>User Management"]
    AGENT_LAYER --> SVC_B["Service B<br/>Order Processing"]
    AGENT_LAYER --> SVC_C["Service C<br/>Recommendation"]

    SVC_A --> DB_A["DB A"]
    SVC_B --> DB_B["DB B"]
    SVC_C --> VS["Vector Store"]

    SVC_B --> AGENT_ORCH["Orchestrator Agent<br/>──────<br/>Multi-step order fulfillment<br/>calls services dynamically"]
    AGENT_ORCH --> SVC_A
    AGENT_ORCH --> SVC_D["Service D<br/>Payment"]
    AGENT_ORCH --> SVC_E["Service E<br/>Inventory"]

    style AGENT_LAYER fill:#bdbdbd,stroke:#212121,stroke-width:2px
    style AGENT_ORCH fill:#9e9e9e,stroke:#000,color:#fff,stroke-width:2px
    style GW fill:#e0e0e0,stroke:#424242
```

---

## Traditional Orchestration vs Agent Orchestration

```mermaid
graph TD
    subgraph TRAD["Traditional: Hardcoded Saga"]
        T1["Step 1: Reserve inventory"] --> T2["Step 2: Charge payment"] --> T3["Step 3: Ship order"] --> T4["Step 4: Send confirmation"]
    end

    subgraph AGENT["Agent: Dynamic Orchestration"]
        A1["Agent reads order context"] --> A2{"Decide next action<br/>based on state"}
        A2 -->|"stock low"| A3["Find alternative supplier"]
        A2 -->|"payment failed"| A4["Retry with backup method"]
        A2 -->|"all good"| A5["Standard fulfillment"]
    end

    style TRAD fill:#f5f5f5,stroke:#616161
    style AGENT fill:#e0e0e0,stroke:#212121
```

---

## Agent as Sidecar

```mermaid
graph LR
    subgraph POD["Kubernetes Pod"]
        SVC["Service Container<br/>──────<br/>Business logic<br/>REST API"]
        SIDECAR["Agent Sidecar<br/>──────<br/>Request analysis<br/>Adaptive retry<br/>Intelligent routing<br/>Anomaly detection"]
        SVC <-->|"local"| SIDECAR
    end

    MESH["Service Mesh<br/>Istio / Linkerd"] <--> POD

    style POD fill:#e0e0e0,stroke:#424242
    style SIDECAR fill:#bdbdbd,stroke:#212121,stroke-width:2px
    style MESH fill:#f5f5f5,stroke:#616161
```

An agent sidecar intercepts requests and responses, adding reasoning capabilities
without modifying service code. Analogous to how Envoy proxies add observability.

---

## Agent-Driven Service Discovery

```mermaid
sequenceDiagram
    participant C as Client Agent
    participant R as Registry
    participant A as Service A
    participant B as Service B
    participant X as Service X (new)

    C->>R: "I need a service that validates addresses"
    R-->>C: Service A (match: 0.92), Service X (match: 0.87)
    C->>C: Select Service A (highest match, proven uptime)
    C->>A: Validate address
    A-->>C: Result

    Note over C,X: If Service A is down
    C->>R: "Alternative for address validation?"
    R-->>C: Service X (fallback)
    C->>X: Validate address
    X-->>C: Result
```

Semantic service discovery: agents query registries by intent, not by endpoint name.
Fallback selection uses reasoning rather than round-robin.

---

## Observability: Agent Traces in a Microservice Call Graph

```mermaid
graph TD
    REQ["Incoming Request<br/>trace-id: abc-123"]
    REQ --> AG["Agent: Route<br/>span: classify-intent<br/>latency: 120ms"]
    AG --> S1["Service: Users<br/>span: get-user<br/>latency: 45ms"]
    AG --> S2["Service: Orders<br/>span: create-order<br/>latency: 200ms"]
    S2 --> AG2["Agent: Orchestrate<br/>span: plan-fulfillment<br/>latency: 340ms"]
    AG2 --> S3["Service: Payment<br/>span: charge<br/>latency: 180ms"]
    AG2 --> S4["Service: Inventory<br/>span: reserve<br/>latency: 90ms"]
    AG2 --> S2

    style AG fill:#bdbdbd,stroke:#212121,stroke-width:2px
    style AG2 fill:#9e9e9e,stroke:#000,color:#fff,stroke-width:2px
```

Agent spans appear alongside service spans in distributed traces.
Every reasoning step, tool call, and retry is a traceable span.

---

## Microservice Patterns Enhanced by Agents

| Classic Pattern | Without Agent | With Agent |
|----------------|---------------|------------|
| **Circuit Breaker** | Fixed thresholds, binary open/close | Agent analyzes error patterns, adaptive thresholds |
| **Saga** | Hardcoded compensation steps | Agent plans compensation dynamically |
| **Service Discovery** | DNS / registry lookup by name | Semantic lookup by intent |
| **API Gateway** | Static routing rules | Intelligent routing by content analysis |
| **Bulkhead** | Fixed resource partitions | Agent reallocates based on load patterns |
| **Retry** | Exponential backoff, fixed | Agent decides if retry is worthwhile given context |

---

## Deployment Topology

```mermaid
graph TD
    subgraph CLUSTER["Kubernetes Cluster"]
        subgraph NS_AGENTS["namespace: agents"]
            ROUTER["Router Agent<br/>Deployment<br/>replicas: 3"]
            ORCH["Orchestrator Agent<br/>Deployment<br/>replicas: 2"]
        end
        subgraph NS_SERVICES["namespace: services"]
            S1["Service A<br/>Deployment"]
            S2["Service B<br/>Deployment"]
            S3["Service C<br/>Deployment"]
        end
        subgraph NS_INFRA["namespace: infra"]
            VS["Vector Store<br/>StatefulSet"]
            MQ["Message Queue<br/>StatefulSet"]
            OBS["Observability<br/>Jaeger + Prometheus"]
        end
    end

    ROUTER --> S1
    ROUTER --> S2
    ORCH --> S2
    ORCH --> S3
    ROUTER --> ORCH
    S1 --> VS
    ORCH --> MQ
    S1 -.-> OBS
    ORCH -.-> OBS

    style NS_AGENTS fill:#bdbdbd,stroke:#212121
    style NS_SERVICES fill:#e0e0e0,stroke:#424242
    style NS_INFRA fill:#f5f5f5,stroke:#616161
```

---

```
 Agents do not replace microservice patterns.
 They make existing patterns adaptive:
 static rules become dynamic reasoning,
 fixed sagas become planned sequences,
 hardcoded routing becomes intent-based dispatch.
```
