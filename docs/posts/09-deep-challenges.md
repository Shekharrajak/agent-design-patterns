---
description: Compounding errors, evaluation, cost, latency, safety, memory, observability, and trust.
---

# Deep Challenges and Open Problems

<small>Part 9 of 9 in the **Agent Design Patterns** series</small>

---

## Challenge Map

```mermaid
mindmap
  root((Open<br/>Challenges))
    Reliability
      Compounding errors
      Non-determinism
      Hallucination propagation
    Evaluation
      No standard benchmarks
      Variable execution paths
      Intermediate step quality
    Cost
      Token multiplication
      Unpredictable cost per request
      Cost vs quality tradeoff
    Latency
      Multi-step execution time
      LLM inference bottleneck
      User experience degradation
    Safety
      Tool access risk
      Prompt injection
      Unintended actions
    Memory
      Context window limits
      Retrieval noise
      Long-horizon coherence
    Observability
      Non-deterministic traces
      Debugging reasoning
      Root cause analysis
    Trust
      Explaining agent decisions
      Accountability
      Regulatory compliance
```

---

## 1. Compounding Errors

```mermaid
graph LR
    S1["Step 1<br/>90% correct"] --> S2["Step 2<br/>81%"] --> S3["Step 3<br/>73%"] --> S5["Step 5<br/>59%"] --> S10["Step 10<br/>35%"]

    style S1 fill:#f5f5f5,stroke:#616161
    style S2 fill:#e0e0e0,stroke:#424242
    style S3 fill:#bdbdbd,stroke:#212121
    style S5 fill:#9e9e9e,stroke:#000,color:#fff
    style S10 fill:#616161,stroke:#000,color:#fff
```

| Steps | Per-step accuracy | Overall success |
|-------|------------------|-----------------|
| 3 | 95% | 85.7% |
| 5 | 95% | 77.4% |
| 10 | 95% | 59.9% |
| 10 | 90% | 34.9% |
| 20 | 90% | 12.2% |

Mitigation strategies:

```mermaid
graph LR
    M1["Verification gates<br/>after every step"] --> M2["Minimize step count<br/>fewer steps = fewer failures"] --> M3["Self-correction loops<br/>detect and retry"] --> M4["Ground truth anchors<br/>test results, API responses"] --> M5["Graceful degradation<br/>partial results over no results"]

    style M1 fill:#f5f5f5,stroke:#616161
    style M2 fill:#e0e0e0,stroke:#424242
    style M3 fill:#bdbdbd,stroke:#212121
    style M4 fill:#9e9e9e,stroke:#000,color:#fff
    style M5 fill:#616161,stroke:#000,color:#fff
```

---

## 2. Evaluation: The Unsolved Problem

```mermaid
graph LR
    subgraph TRAD["Traditional Software Testing"]
        TI["Input"] --> TF["Function"] --> TO["Output<br/>Assert output == expected"]
    end

    subgraph AGENT["Agent Evaluation"]
        AI["Input"] --> AF["Agent<br/>variable path"]
        AF --> AO1["Output A"]
        AF --> AO2["Output B"]
        AF --> AO3["Output C"]
    end

    style TRAD fill:#f5f5f5,stroke:#616161
    style AGENT fill:#e0e0e0,stroke:#424242
```

| Dimension | What to Measure | Difficulty |
|-----------|----------------|------------|
| Final output quality | Does the result solve the task? | Medium |
| Path efficiency | Did the agent take unnecessary steps? | Hard |
| Tool selection | Did it pick the right tools? | Hard |
| Cost efficiency | Could it have been done cheaper? | Medium |
| Robustness | Same quality across varied inputs? | Very Hard |
| Safety | Did it avoid harmful actions? | Very Hard |

```mermaid
graph LR
    E1["Unit Tests<br/>on individual tools"] --> E2["End-to-End Evals<br/>task completion rate"] --> E3["Trajectory Evals<br/>score each step"] --> E4["Human Judges<br/>expert review"]
    E3 --> E5["LLM-as-Judge<br/>automated scoring"]

    style E1 fill:#f5f5f5,stroke:#616161
    style E2 fill:#e0e0e0,stroke:#424242
    style E3 fill:#bdbdbd,stroke:#212121
    style E4 fill:#9e9e9e,stroke:#000,color:#fff
    style E5 fill:#9e9e9e,stroke:#000,color:#fff
```

---

## 3. Cost: The Hidden Multiplier

```mermaid
graph LR
    VC["Visible Cost<br/>──────<br/>LLM API tokens<br/>billed per request"] --> HC1["Planning calls<br/>before execution"] --> HC2["Reflection loops<br/>re-processing output"] --> HC3["Failed attempts<br/>retries and fallbacks"]

    VC --> HC4["Memory retrieval<br/>embedding + search"] --> HC5["Tool execution<br/>compute, API fees"] --> HC6["Observability<br/>logging, storage"]

    style VC fill:#f5f5f5,stroke:#616161
    style HC1 fill:#e0e0e0,stroke:#424242
    style HC2 fill:#e0e0e0,stroke:#424242
    style HC3 fill:#e0e0e0,stroke:#424242
    style HC4 fill:#bdbdbd,stroke:#212121
    style HC5 fill:#bdbdbd,stroke:#212121
    style HC6 fill:#bdbdbd,stroke:#212121
```

A single user request can trigger 10-50 LLM calls internally.
Cost varies 10x between simple and complex inputs for the same agent.

---

## 4. Latency Budget

```mermaid
graph LR
    B1["LLM inference<br/>500ms - 2s per call"] --> B2["Tool execution<br/>100ms - 10s per tool"] --> B3["Memory retrieval<br/>50 - 200ms"] --> B4["Network overhead<br/>50 - 100ms per hop"] --> TOTAL["TOTAL for 5-step agent<br/>3s - 40s"]

    style B1 fill:#f5f5f5,stroke:#616161
    style B2 fill:#e0e0e0,stroke:#424242
    style B3 fill:#bdbdbd,stroke:#212121
    style B4 fill:#9e9e9e,stroke:#000,color:#fff
    style TOTAL fill:#616161,stroke:#000,color:#fff
```

| User Experience | Max Latency | Implication |
|----------------|-------------|-------------|
| Interactive chat | Under 3s | 1-2 LLM calls max |
| Streamed response | Under 10s for first token | Start streaming planning phase |
| Background task | Minutes | Use async + notification |
| Batch processing | Hours | No user waiting |

---

## 5. Safety: Real Attack Vectors

```mermaid
graph TD
    subgraph ATTACKS["Threat Model"]
        ATK1["Prompt Injection<br/>──────<br/>Malicious input overrides<br/>agent instructions"]
        ATK2["Tool Misuse<br/>──────<br/>Agent tricked into<br/>calling tools harmfully"]
        ATK3["Data Exfiltration<br/>──────<br/>Agent leaks private data<br/>through tool outputs"]
        ATK4["Privilege Escalation<br/>──────<br/>Agent accesses resources<br/>beyond user's scope"]
        ATK5["Denial of Service<br/>──────<br/>Crafted input causes<br/>infinite agent loops"]
    end

    subgraph DEFENSES["Defenses"]
        DEF1["Input sanitization<br/>and injection detection"]
        DEF2["Tool allowlists<br/>per user role"]
        DEF3["Output filtering<br/>PII detection"]
        DEF4["Scoped credentials<br/>principle of least privilege"]
        DEF5["Hard iteration limits<br/>cost caps, timeouts"]
    end

    ATK1 --> DEF1
    ATK2 --> DEF2
    ATK3 --> DEF3
    ATK4 --> DEF4
    ATK5 --> DEF5

    style ATTACKS fill:#bdbdbd,stroke:#212121
    style DEFENSES fill:#e0e0e0,stroke:#424242
```

---

## 6. Memory: The Long-Horizon Problem

```mermaid
graph TD
    P1["Context window = finite<br/>128K tokens is not infinite"] --> A1["Hierarchical memory<br/>summary layers at different granularities"]
    P2["Vector retrieval = noisy<br/>top-k results may miss key facts"] --> A2["Episodic memory<br/>store full interaction episodes"]
    P3["Summarization = lossy<br/>compressing context loses detail"] --> A3["Working memory management<br/>agent decides what to keep in context"]
    P4["Cross-session memory = unsolved<br/>what to remember, what to forget?"] --> A4["Memory consolidation<br/>periodic reflection to extract insights"]

    style P1 fill:#bdbdbd,stroke:#212121
    style P2 fill:#bdbdbd,stroke:#212121
    style P3 fill:#bdbdbd,stroke:#212121
    style P4 fill:#bdbdbd,stroke:#212121
    style A1 fill:#e0e0e0,stroke:#424242
    style A2 fill:#e0e0e0,stroke:#424242
    style A3 fill:#e0e0e0,stroke:#424242
    style A4 fill:#e0e0e0,stroke:#424242
```

---

## 7. Observability: Debugging Non-Determinism

```mermaid
graph TD
    T1["Step 1: Classified as data analysis"] --> T2["Step 2: Called SQL tool, got 47 rows"] --> T3["Step 3: Reflected, found missing filter"] --> T4["Step 4: Re-called SQL tool, got 12 rows"] --> T5["Step 5: Generated summary"]
    T5 --> D1["Why 5 steps instead of 3?"]
    T5 --> D2["Was the reflection necessary or wasteful?"]
    T5 --> D3["Would a different model take a better path?"]
    T5 --> D4["Why did user B get a different result?"]

    style T1 fill:#e0e0e0,stroke:#424242
    style T2 fill:#e0e0e0,stroke:#424242
    style T3 fill:#e0e0e0,stroke:#424242
    style T4 fill:#e0e0e0,stroke:#424242
    style T5 fill:#e0e0e0,stroke:#424242
    style D1 fill:#bdbdbd,stroke:#212121
    style D2 fill:#bdbdbd,stroke:#212121
    style D3 fill:#bdbdbd,stroke:#212121
    style D4 fill:#bdbdbd,stroke:#212121
```

Requirements for agent observability:

```mermaid
graph LR
    O1["Full step traces<br/>every LLM call, tool call, decision"] --> O2["Cost attribution<br/>cost per step, per tool, per request"] --> O3["Replay capability<br/>re-run with same inputs"] --> O4["Comparison views<br/>diff two runs of same input"] --> O5["Anomaly detection<br/>flag unusual step counts, costs"]

    style O1 fill:#f5f5f5,stroke:#616161
    style O2 fill:#e0e0e0,stroke:#424242
    style O3 fill:#bdbdbd,stroke:#212121
    style O4 fill:#9e9e9e,stroke:#000,color:#fff
    style O5 fill:#616161,stroke:#000,color:#fff
```

---

## 8. Trust and Accountability

```mermaid
graph LR
    TR1["Explainability<br/>──────<br/>Why did the agent do X?<br/>Show reasoning chain"] --> TR2["Auditability<br/>──────<br/>Complete log of actions<br/>Tamper-proof records"] --> TR3["Accountability<br/>──────<br/>Who is responsible?<br/>Developer? User? Model?"] --> TR4["Compliance<br/>──────<br/>GDPR: right to explanation<br/>SOX: audit trails<br/>HIPAA: data handling"]

    style TR1 fill:#f5f5f5,stroke:#616161
    style TR2 fill:#e0e0e0,stroke:#424242
    style TR3 fill:#bdbdbd,stroke:#212121
    style TR4 fill:#9e9e9e,stroke:#000,color:#fff
```

---

## Challenge Maturity Map

```mermaid
graph LR
    subgraph SOLVED["Mostly Solved"]
        S1["Basic tool calling"] --> S2["Single-step reflection"] --> S3["Prompt chaining"]
    end

    subgraph PROGRESS["Active Progress"]
        P1["Multi-agent coordination"] --> P2["Cost optimization"] --> P3["Streaming UIs"] --> P4["Observability tooling"]
    end

    subgraph OPEN["Wide Open"]
        O1a["Long-horizon memory"] --> O2a["Evaluation standards"] --> O3a["Safety guarantees"] --> O4a["Agent-to-agent trust"]
    end

    S3 --> P1
    P4 --> O1a

    style SOLVED fill:#f5f5f5,stroke:#616161
    style PROGRESS fill:#e0e0e0,stroke:#424242
    style OPEN fill:#bdbdbd,stroke:#212121
```

---

```
 The challenges are not reasons to avoid agents.
 They are the engineering problems that define
 the next generation of software infrastructure.

 Whoever solves observability, evaluation, and safety
 for agentic systems builds the next AWS.
```
