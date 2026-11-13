.PHONY: init task check digest digest-ack queue answer attention
init:
	git init -q 2>/dev/null || true
	cp tools/hooks/pre-commit .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
	@command -v lake >/dev/null && (cd lean && lake update >/dev/null 2>&1 || true) || echo "lake not found: install elan to enable Lean certificates"
	@echo "ready. Edit SPEC.md first."
task:
	@python3 tools/new_task.py "$(T)"
check:
	@python3 tools/check_report.py
digest:
	@python3 tools/digest.py
digest-ack:
	@python3 tools/finalize_digest.py
queue:
	@python3 tools/queue.py list
attention:
	@python3 tools/attention.py
answer:
	@python3 tools/queue.py answer $(Q) "$(A)"

# ---- education loop ----
# AGENT_CMD: how to run an agent headlessly. Override: make morning AGENT_CMD='claude -p "$$(cat Education/.context/dispatch.txt)" --allowedTools Edit,Write,Read,Bash'
AGENT_CMD ?= echo "no AGENT_CMD set; dispatch manually:" && cat Education/.context/dispatch.txt
.PHONY: morning brief-check
morning:
	@python3 tools/education.py >/dev/null
	@echo "Read Education/AGENT.md and produce today's brief ($$(date +%F)). When done run: python3 tools/check_brief.py Education/briefs/$$(date +%F).md && python3 tools/render_brief.py Education/briefs/$$(date +%F).md" > Education/.context/dispatch.txt
	@$(AGENT_CMD)
	@python3 tools/finalize_brief.py
brief-check:
	@python3 tools/check_brief.py Education/briefs/$$(date +%F).md && python3 tools/render_brief.py Education/briefs/$$(date +%F).md
