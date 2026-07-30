# Fool-proof Review Method Notes

These notes preserve the longer method behind the skill. Load only when more calibration examples are needed.

## Core Mechanism

The reader is not lazy. They may inspect available docs, code, configs, and links. The useful failure mode is: they can observe facts but cannot connect the causal chain. The document must explain why facts exist, not merely where they are.

Example pattern:

- Fact seen: Redis stores `user:{id}` with fields similar to MySQL.
- Wrong mental model: Redis is another source database.
- Useful question: "I saw Redis and MySQL both have user fields. If they conflict, which one wins? Why not just read MySQL?"

## Hidden Premise Pattern

Do not say the premise directly. Ask a question that reveals it.

- Hidden premise: cache = database.
- Ask: "If Redis and MySQL disagree, which one is correct?"

- Hidden premise: async = nobody knows success.
- Ask: "If this is async, how does the caller know it worked? Does it poll?"

- Hidden premise: idempotent = byte-for-byte same response.
- Ask: "If the timestamp changes on retry, why is this still idempotent?"

- Hidden premise: distributed lock = mutex with extra steps.
- Ask: "Why not use the language's normal lock here?"

## Useful Question Types

- Motivation: "Why do this at all? What breaks if we skip it?"
- Source: "Where does this input come from? Who sends it?"
- Jump: "What happens between A and B?"
- Boundary: "What if this fails or is delayed?"
- Choice: "Why A instead of B?"
- Textbook mapping: "Isn't this just the thing from OS/database/networking class?"
- Apparent contradiction: "Earlier says X, here says Y; are those the same thing?"
- Complexity challenge: "This feels heavy. What scale or risk makes it necessary?"

## Voice Calibration

Good:

> 我看了这段，感觉它是在说配置中心才是最终来源，但后面又说数据库里也有配置。那到底谁是 source of truth？

Bad:

> 建议补充配置中心与数据库之间的数据同步机制。

Good:

> 这个限流是防谁的？如果是内部系统，正常用户也不会打爆它吧？

Bad:

> 此处应说明内部系统也存在异常调用和流量尖峰风险。

## Drift Corrections

If output becomes too formal, return to casual questions.
If output becomes too many questions, limit to 1-3.
If output starts inventing files, stop and use only retrieved evidence.
If output becomes technical review, return to readability confusion.
If output becomes random without anchors, tie each question to a phrase, section, diagram, or real external material.
