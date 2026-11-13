# Question queue

Agents append when they hit a declared stop condition. The human answers in batch. Managed by `tools/queue.py`.
An unanswered question blocks the task that raised it; the agent does not guess.

<!-- queue entries below; do not edit by hand, use tools/queue.py -->
