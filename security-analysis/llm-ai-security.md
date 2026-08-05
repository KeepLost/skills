# LLM and AI Security

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## When to Load

The task involves assessing the security of an LLM-based application or
AI agent system. This includes: prompt injection testing, tool misuse
assessment, output safety validation, or AI supply chain review.

## Defensive Testing Framework

### Phase 1: Map the Attack Surface

1. Identify all LLM interaction points: chat, RAG queries, tool calls,
   agent planning.
2. Enumerate registered tools and their permissions: what can each tool
   do? What data can it access?
3. Map data flow: user input → (retrieval?) → prompt → model → tool
   call? → output → downstream system.
4. Identify human-in-the-loop approval points: what triggers them? Can
   they be bypassed?

### Phase 2: Prompt Injection Testing

Test coverage across five levels (as a checklist, not as attack
instructions):

1. **Direct override**: can the user instruct the model to ignore its
   system prompt?
2. **Role play**: can the model be induced to act outside its role via
   persona framing?
3. **Encoding**: does the model process encoded/obfuscated instructions
   (base64, unicode, pig latin)?
4. **Multi-turn**: can restrictions be eroded over multiple turns?
5. **Indirect injection**: can content retrieved from external sources
   (RAG, web pages, documents) inject instructions?

For each level, test whether the model's guardrails hold or fail.
Record the specific failure mode, not just "it failed."

### Phase 3: Tool Misuse Testing

1. Enumerate tools and their parameters.
2. Test: can a tool be called with parameters outside its intended scope?
3. Test: can tool calls be chained in unintended ways?
4. Test: can the human-in-the-loop approval be bypassed (urgency framing,
   authority claims, technical confusion)?
5. Verify: does each tool have minimum necessary permissions?

### Phase 4: Memory and Context Poisoning

1. Knowledge base injection: can injected content in the retrieval store
   affect model behavior?
2. Long-term memory: can past interactions poison future ones?
3. Verify: does retrieval enforce permission checks on returned content?

### Phase 5: Output Safety

1. Test: does the model output content that is dangerous when rendered
   (XSS in chat UI, markdown injection)?
2. Test: does the model output content that is dangerous when passed to
   downstream systems (SQL, shell commands, API calls)?
3. Verify: does the downstream system sanitize LLM output before
   execution?

### Phase 6: System Prompt Leakage

1. Embed canary tokens in the system prompt.
2. Test: do any injection techniques cause the model to output the
   canary?
3. If the canary appears in output → system prompt is leaked.

### Phase 7: Cascading Failures

1. Single-point memory poisoning → what else is affected?
2. Tool privilege escalation → can a compromised tool access other
   tools?
3. Agent self-replication → can an agent create persistent copies?
4. Emergency stop → does the kill switch actually work?

## Defense Principles

1. **Separate planning from execution**: the model that interprets
   intent should not be the model that executes actions.
2. **Bind identity, purpose, scope, and time**: do not grant broad
   environment permissions to tools.
3. **Log everything**: tool calls, memory operations, and inter-agent
   communication as security telemetry.
4. **Blast radius control**: circuit breakers, rollback, and emergency
   stop take priority over convenience.
5. **All natural language input is untrusted**: including retrieved
   content from RAG, web pages, and documents.
6. **Output is also untrusted**: sanitize before rendering, executing,
   or querying.

## OWASP LLM Top 10 (as assessment checklist)

| ID | Category | Assessment question |
|---|---|---|
| LLM01 | Prompt Injection | Can instructions override the system prompt? |
| LLM02 | Sensitive Info Disclosure | Does the model leak training data or user data? |
| LLM03 | Supply Chain | Are third-party models/plugins/datasets vetted? |
| LLM04 | Data & Model Poisoning | Can training data be tampered with? |
| LLM05 | Improper Output Handling | Is model output sanitized before downstream use? |
| LLM06 | Excessive Agency | Do tools have more permissions than needed? |
| LLM07 | System Prompt Leakage | Can the system prompt be extracted? |
| LLM08 | Vector & Embedding Weaknesses | Can retrieval be poisoned? |
| LLM09 | Misinformation | Does the system verify factual claims? |
| LLM10 | Unbounded Consumption | Can resource exhaustion be triggered? |

## Tool Roles

| Role | Tools |
|---|---|
| Automated probing | garak (100+ injection probes) |
| Multi-turn attack orchestration | PyRIT |
| CI/CD integration | promptfoo |
| Agent benchmarking | AgentThreatBench (UK AISI) |

Load [tool-catalog.md](tool-catalog.md) only if this role summary is insufficient.

## Stop Conditions

- Testing an LLM system requires access to the application → confirm
  Level 3 authorization for the test instance.
- Tool misuse testing could cause real side effects (file writes, API
  calls, emails) → ensure testing is against a sandboxed instance.
- Do not test prompt injection on production systems where output is
  shown to real users.
- Installing external AI skills or MCP servers for testing → review
  supply chain security first (see
  [supply-chain-security.md](supply-chain-security.md)).
