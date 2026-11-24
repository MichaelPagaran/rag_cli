# Learning log

## 2026-11-18: Learning workflow and first quiz
**Built:** No code changes. Marked `CLAUDE.md` as a learning repo, updated its "Current state", and set up global skills: /next-milestone, /quiz-me, /learning-log.
**Learned:**
- Vector embeddings are coordinates that point to a meaning, based on the language patterns the model learned in training.
- Fixed-size chunking cuts by character count, so a sentence can be split mid-word across two chunks.
- Cosine similarity measures how closely two meaning arrows point the same way. It isn't a percentage. A low *top* score usually means the answer isn't in the document.
- `CREATE TABLE IF NOT EXISTS` won't resize an existing `vector(384)` column, and re-running ingest creates duplicates.
**Surprised by:** "We use the same embedding model in ingest.py and chat.py to avoid incompatibility. Even if both models have the same dimensions, they have different meaning maps."
**Quiz:** 2.5 / 5. Strongest: schema. Revisit: chunking.
**Open questions:** How much chunk overlap is enough? What similarity threshold should count as "relevant"?
