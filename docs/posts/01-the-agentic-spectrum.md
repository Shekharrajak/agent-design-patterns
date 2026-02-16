---
description: Definitions, components, and the three pillars of LLM-based agents.
---

# The Agentic Spectrum

<small>Part 1 of 9 in the **Agent Design Patterns** series</small>

---

```mermaid
graph LR
    L0["Level 0<br/>Single LLM Call<br/>──────<br/>Prompt in, text out"] 
    --> L1["Level 1<br/>Router<br/>──────<br/>Classify, dispatch"]
    --> L2["Level 2<br/>State Machine<br/>──────<br/>Multi-step, loops"]
    --> L3["Level 3<br/>Autonomous Agent<br/>──────<br/>Plans, tools, self-corrects"]
    --> L4["Level 4<br/>Self-Improving<br/>──────<br/>Builds own tools, learns"]

    style L0 fill:#f5f5f5,stroke:#616161
    style L1 fill:#e0e0e0,stroke:#424242
    style L2 fill:#bdbdbd,stroke:#212121
    style L3 fill:#9e9e9e,stroke:#000,color:#fff
    style L4 fill:#616161,stroke:#000,color:#fff
```

---

## Three Pillars

```mermaid
graph TB
    ENV["Environment"] -->|perceive| MEM

    subgraph AGENT["Agent"]
        MEM["MEMORY<br/>──────<br/>Short-term: context window<br/>Long-term: vector store"]
        BRAIN["BRAIN<br/>──────<br/>Reason, Plan, Decide"]
        TOOLS["TOOLS<br/>──────<br/>Search, Execute, Call APIs"]
        
        MEM -->|context| BRAIN
        BRAIN -->|store| MEM
        BRAIN -->|invoke| TOOLS
        TOOLS -->|results| BRAIN
    end
    
    BRAIN -->|act| ENV

    style BRAIN fill:#e0e0e0,stroke:#212121,stroke-width:2px
    style MEM fill:#e0e0e0,stroke:#212121
    style TOOLS fill:#e0e0e0,stroke:#212121
    style ENV fill:#f5f5f5,stroke:#616161
```

---

## Planning Techniques at a Glance

```mermaid
graph LR
    subgraph COT["Chain of Thought"]
        C1["Step"] --> C2["Step"] --> C3["Answer"]
    end

    subgraph TOT["Tree of Thoughts"]
        T0["Problem"] --> T1["Path A"]
        T0 --> T2["Path B"]
        T1 --> T3["Best"]
    end

    subgraph REACT["ReAct"]
        R1["Think"] --> R2["Act"] --> R3["Observe"] --> R1
    end

    style COT fill:#f5f5f5,stroke:#616161
    style TOT fill:#e0e0e0,stroke:#424242
    style REACT fill:#bdbdbd,stroke:#212121
```

| Technique | Mechanism | Best For |
|-----------|-----------|----------|
| CoT | Linear decomposition | Arithmetic, logic |
| ToT | Branching exploration | Creative, multi-path problems |
| ReAct | Interleaved reasoning + action | Tool-dependent tasks |

---

## Memory Layers

```mermaid
graph LR
    SENSORY["Sensory<br/>Embeddings<br/>Milliseconds"] --> SHORT["Short-Term<br/>Context Window<br/>One Session"] --> LONG["Long-Term<br/>Vector Store<br/>Persistent"]

    style SENSORY fill:#f5f5f5,stroke:#616161
    style SHORT fill:#e0e0e0,stroke:#424242
    style LONG fill:#bdbdbd,stroke:#212121
```

---

```
 Agentic is not a label. It is a dial.
 Turn it up only when the task demands it.
```
