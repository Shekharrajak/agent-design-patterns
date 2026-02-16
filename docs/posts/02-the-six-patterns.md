---
description: Chaining, Routing, Reflection, Tool Use, Planning, and Multi-Agent -- compared visually.
---

# The Six Patterns

<small>Part 2 of 9 in the **Agent Design Patterns** series</small>

---

## Overview

```mermaid
graph TB
    subgraph SIMPLE["Lower Complexity"]
        P1["CHAINING<br/>A then B then C"] --- P2["ROUTING<br/>Classify, dispatch"]
    end
    subgraph MODERATE["Moderate Complexity"]
        P3["REFLECTION<br/>Generate, critique, rewrite"] --- P4["TOOL USE<br/>Call external APIs/code"]
    end
    subgraph ADVANCED["Higher Complexity"]
        P5["PLANNING<br/>Orchestrator delegates dynamically"] --- P6["MULTI-AGENT<br/>Team of specialized agents"]
    end

    SIMPLE --> MODERATE --> ADVANCED

    style SIMPLE fill:#f5f5f5,stroke:#616161
    style MODERATE fill:#e0e0e0,stroke:#424242
    style ADVANCED fill:#bdbdbd,stroke:#212121
```

---

## 1. Prompt Chaining

```mermaid
graph LR
    IN["Input"] --> S1["LLM 1<br/>Generate"] --> G{"Gate"} -->|pass| S2["LLM 2<br/>Refine"] --> S3["LLM 3<br/>Format"] --> OUT["Output"]
    G -->|fail| S1

    style G fill:#bdbdbd,stroke:#212121
```

Fixed pipeline. Each step feeds the next. Gates catch failures between steps.

---

## 2. Routing

```mermaid
graph TD
    IN["Input"] --> R{"Router<br/>Classify"}
    R -->|Type A| HA["Handler A<br/>Small model, fast"]
    R -->|Type B| HB["Handler B<br/>Large model, accurate"]
    R -->|Type C| HC["Handler C<br/>Specialized pipeline"]
    HA --> OUT["Output"]
    HB --> OUT
    HC --> OUT

    style R fill:#bdbdbd,stroke:#212121,stroke-width:2px
```

Separation of concerns. Optimize each path independently.

---

## 3. Reflection

```mermaid
graph TD
    IN["Task"] --> GEN["Generate"] --> EVAL{"Good<br/>enough?"}
    EVAL -->|No| CRIT["Critique"] --> GEN
    EVAL -->|Yes| OUT["Output"]

    style EVAL fill:#bdbdbd,stroke:#212121,stroke-width:2px
```

Highest ROI pattern. GPT-3.5 with reflection (95.1%) surpasses GPT-4 zero-shot (67.0%) on HumanEval.

---

## 4. Tool Use

```mermaid
graph LR
    LLM["LLM decides<br/>what to call"] --> T1["Search"]
    LLM --> T2["Code Exec"]
    LLM --> T3["APIs"]
    LLM --> T4["File I/O"]
    T1 --> LLM
    T2 --> LLM
    T3 --> LLM
    T4 --> LLM

    style LLM fill:#bdbdbd,stroke:#212121,stroke-width:2px
```

Without tools, an LLM is a brain without hands.

---

## 5. Planning / Orchestrator-Workers

```mermaid
graph TD
    IN["Complex Task"] --> O["Orchestrator<br/>Analyzes, decomposes"]
    O -->|dynamic| W1["Worker 1"]
    O -->|dynamic| W2["Worker 2"]
    O -->|dynamic| W3["Worker N"]
    W1 --> SYN["Orchestrator<br/>Synthesize"]
    W2 --> SYN
    W3 --> SYN
    SYN --> OUT["Result"]

    style O fill:#bdbdbd,stroke:#212121,stroke-width:2px
    style SYN fill:#bdbdbd,stroke:#212121
```

Subtasks are not predefined. The orchestrator discovers them at runtime.

---

## 6. Multi-Agent

```mermaid
graph TD
    IN["Request"] --> PM["Agent: PM<br/>Requirements"]
    PM --> DEV["Agent: Developer<br/>Implementation"]
    DEV --> QA["Agent: QA<br/>Validation"]
    QA -->|issues| DEV
    QA -->|pass| OUT["Delivered"]

    style PM fill:#e0e0e0,stroke:#424242
    style DEV fill:#bdbdbd,stroke:#212121
    style QA fill:#9e9e9e,stroke:#000,color:#fff
```

Same LLM, different role prompts. Ablation studies confirm multi-agent outperforms single-agent.

---

## Comparison Matrix

| Pattern | Predictability | Cost | Flexibility | Maturity |
|---------|---------------|------|-------------|----------|
| Chaining | High | Low | None | High |
| Routing | High | Low | Low | High |
| Reflection | Medium-High | Medium | Medium | High |
| Tool Use | Medium | Medium | Medium | High |
| Planning | Medium | High | High | Medium |
| Multi-Agent | Low-Medium | High | High | Emerging |

---

## Selection Flowchart

```mermaid
graph TD
    START(("Start")) --> Q1{"Single call<br/>sufficient?"}
    Q1 -->|Yes| P0["Prompt + Retrieval"]
    Q1 -->|No| Q2{"Fixed steps?"}
    Q2 -->|Yes| Q3{"Need classification?"}
    Q3 -->|Yes| P1["ROUTING"]
    Q3 -->|No| P2["CHAINING"]
    Q2 -->|No| Q4{"Quality improves<br/>with critique?"}
    Q4 -->|Yes| P3["REFLECTION"]
    Q4 -->|No| Q5{"Need external<br/>data or actions?"}
    Q5 -->|Yes| P4["TOOL USE"]
    Q5 -->|No| Q6{"Role decomposition<br/>helps?"}
    Q6 -->|Yes| P6["MULTI-AGENT"]
    Q6 -->|No| P5["PLANNING"]

    style START fill:#bdbdbd,stroke:#212121
    style P0 fill:#f5f5f5,stroke:#616161
    style P1 fill:#f5f5f5,stroke:#616161
    style P2 fill:#f5f5f5,stroke:#616161
    style P3 fill:#e0e0e0,stroke:#424242
    style P4 fill:#e0e0e0,stroke:#424242
    style P5 fill:#bdbdbd,stroke:#212121
    style P6 fill:#9e9e9e,stroke:#000,color:#fff
```
