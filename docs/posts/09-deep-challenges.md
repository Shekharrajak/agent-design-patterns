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
graph TD
    subgraph MITIGATIONS[""]
        M1["Verification gates<br/>after every step"]
        M2["Minimize step count<br/>fewer steps = fewer failures"]
        M3["Self-correction loops<br/>detect and retry"]
        M4["Ground truth anchors<br/>test results, API responses"]
        M5["Graceful degradation<br/>partial results > no results"]
    end

    style MITIGATIONS fill:#e0e0e0,stroke:#424242
```

---

## 2. Evaluation: The Unsolved Problem

```mermaid
graph TD
    subgraph TRAD["Traditional Software Testing"]
        direction LR
        TI["Input"] --> TF["Function"] --> TO["Output"]
        TC["Assert output == expected"]
    end

    subgraph AGENT["Agent Evaluation"]
        direction LR
        AI["Input"] --> AF["Agent<br/>variable path"]
        AF --> AO1["Output A"]
        AF --> AO2["Output B"]
        AF --> AO3["Output C"]
        AC["Which output is 'correct'?<br/>Was the path efficient?<br/>Were the right tools used?"]
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
    subgraph EVAL_APPROACHES["Evaluation Approaches"]
        E1["Unit Tests<br/>on individual tools"]
        E2["End-to-End Evals<br/>task completion rate"]
        E3["Trajectory Evals<br/>score each step"]
        E4["Human Judges<br/>expert review"]
        E5["LLM-as-Judge<br/>automated scoring"]
    end

    E1 --> E2 --> E3 --> E4
    E3 --> E5

    style EVAL_APPROACHES fill:#e0e0e0,stroke:#424242
```

---

## 3. Cost: The Hidden Multiplier

```mermaid
graph TD
    subgraph VISIBLE["Visible Cost"]
        VC["LLM API tokens<br/>billed per request"]
    end

    subgraph HIDDEN["Hidden Costs"]
        HC1["Planning calls<br/>before execution"]
        HC2["Reflection loops<br/>re-processing output"]
        HC3["Failed attempts<br/>retries and fallbacks"]
        HC4["Memory retrieval<br/>embedding + search"]
        HC5["Tool execution<br/>compute, API fees"]
        HC6["Observability<br/>logging, storage"]
    end

    VISIBLE --- HIDDEN

    style VISIBLE fill:#f5f5f5,stroke:#616161
    style HIDDEN fill:#bdbdbd,stroke:#212121
```

A single user request can trigger 10-50 LLM calls internally.
Cost varies 10x between simple and complex inputs for the same agent.

---

## 4. Latency Budget

```mermaid
graph LR
    subgraph BUDGET["Latency Breakdown"]
        direction TB
        B1["LLM inference<br/>500ms-2s per call"]
        B2["Tool execution<br/>100ms-10s per tool"]
        B3["Memory retrieval<br/>50-200ms"]
        B4["Network overhead<br/>50-100ms per hop"]
    end

    subgraph TOTAL["Total for 5-step agent"]
        T1["5 LLM calls: 2.5-10s"]
        T2["3 tool calls: 0.3-30s"]
        T3["2 retrievals: 0.1-0.4s"]
        T4["TOTAL: 3s - 40s"]
    end

    BUDGET --> TOTAL

    style BUDGET fill:#e0e0e0,stroke:#424242
    style TOTAL fill:#bdbdbd,stroke:#212121
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
    subgraph PROBLEM["The Problem"]
        P1["Context window = finite<br/>128K tokens is not infinite"]
        P2["Vector retrieval = noisy<br/>top-k results may miss key facts"]
        P3["Summarization = lossy<br/>compressing context loses detail"]
        P4["Cross-session memory = unsolved<br/>what to remember, what to forget?"]
    end

    subgraph APPROACHES["Emerging Approaches"]
        A1["Hierarchical memory<br/>summary layers at different granularities"]
        A2["Episodic memory<br/>store full interaction episodes"]
        A3["Working memory management<br/>agent decides what to keep in context"]
        A4["Memory consolidation<br/>periodic reflection to extract insights"]
    end

    PROBLEM --> APPROACHES

    style PROBLEM fill:#bdbdbd,stroke:#212121
    style APPROACHES fill:#e0e0e0,stroke:#424242
```

---

## 7. Observability: Debugging Non-Determinism

```mermaid
graph TD
    subgraph TRACE["Agent Trace"]
        T1["Step 1: Classified as 'data analysis'"]
        T2["Step 2: Called SQL tool, got 47 rows"]
        T3["Step 3: Reflected, found missing filter"]
        T4["Step 4: Re-called SQL tool, got 12 rows"]
        T5["Step 5: Generated summary"]
    end

    subgraph DEBUG["Debugging Questions"]
        D1["Why did it take 5 steps instead of 3?"]
        D2["Was the reflection necessary or wasteful?"]
        D3["Would a different model take a better path?"]
        D4["Why did user B get a different result than user A?"]
    end

    TRACE --> DEBUG

    style TRACE fill:#e0e0e0,stroke:#424242
    style DEBUG fill:#bdbdbd,stroke:#212121
```

Requirements for agent observability:

```mermaid
graph LR
    subgraph OBS[""]
        O1["Full step traces<br/>every LLM call, tool call, decision"]
        O2["Cost attribution<br/>cost per step, per tool, per request"]
        O3["Replay capability<br/>re-run with same inputs to reproduce"]
        O4["Comparison views<br/>diff two runs of same input"]
        O5["Anomaly detection<br/>flag unusual step counts, costs, paths"]
    end

    style OBS fill:#e0e0e0,stroke:#424242
```

---

## 8. Trust and Accountability

```mermaid
graph TD
    subgraph TRUST["Trust Requirements"]
        TR1["Explainability<br/>──────<br/>Why did the agent do X?<br/>Show reasoning chain"]
        TR2["Auditability<br/>──────<br/>Complete log of actions<br/>Tamper-proof records"]
        TR3["Accountability<br/>──────<br/>Who is responsible?<br/>The developer? The user? The model?"]
        TR4["Compliance<br/>──────<br/>GDPR: right to explanation<br/>SOX: audit trails<br/>HIPAA: data handling"]
    end

    style TRUST fill:#e0e0e0,stroke:#424242
```

---

## Challenge Maturity Map

```mermaid
graph LR
    subgraph SOLVED["Mostly Solved"]
        S1["Basic tool calling"]
        S2["Single-step reflection"]
        S3["Prompt chaining"]
    end

    subgraph PROGRESS["Active Progress"]
        P1["Multi-agent coordination"]
        P2["Cost optimization"]
        P3["Streaming UIs"]
        P4["Observability tooling"]
    end

    subgraph OPEN["Wide Open"]
        O1["Long-horizon memory"]
        O2["Agent evaluation standards"]
        O3["Safety guarantees"]
        O4["Agent-to-agent trust"]
        O5["Regulatory frameworks"]
    end

    SOLVED --> PROGRESS --> OPEN

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
