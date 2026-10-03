@@ tool-calling
topics: why models need tools, tool definitions with names, descriptions and JSON Schemas, the tool_use and tool_result cycle, stop_reason tool_use, returning errors with is_error, parallel tool calls, tool_choice and its limits on the newest models, strict tools, client tools and server tools, tool token overhead, designing tools a model uses well
terms:
- **Tool (function) calling:** the model requesting that your code run a named function with arguments it chooses.
- **Tool definition:** a tool's name, description and JSON Schema for its input.
- **tool_use block:** the part of a reply that names a tool, its arguments and a call id.
- **tool_result block:** your reply to a tool call, matched by `tool_use_id`, with the output or an error.
- **Parallel tool calls:** several tool calls requested in one reply.
- **Client tool:** a tool your application executes.
- **Server tool:** a tool the provider executes, such as web search or code execution.
mistakes:
- Vague tool descriptions that don't say when to use the tool.
- Dropping the assistant's tool_use reply or thinking blocks from the history.
- Leaving a tool_use without a tool_result after an error.
- Returning huge raw outputs instead of the fields the model needs.
- Executing tool arguments without validating them.

glance:
- Schema from a function | inspect the signature; map type hints; no default means required | O(parameters) | O(parameters)
- Execute tool calls | dispatch table; one result per call; errors as is_error results | O(calls) | O(calls)
- One tool round | reply with tool_use → run → tool_result message → call again | — | —

@@ agent-loop
topics: workflows versus agents, when to use an agent, the agent loop, stopping conditions, turn limits, budgets and timeouts, other stop reasons, SDK tool runners, the Claude Agent SDK and other agent frameworks, tools and environment feedback, plans and checkpoints, reading transcripts, detecting stuck agents, orchestrator-worker and evaluator-optimiser patterns
terms:
- **Agent:** a system where a model decides its next action in a loop, using tools and feedback.
- **Workflow:** a fixed sequence of model calls and tools defined by your code.
- **Agent loop:** call the model, run any requested tools, append the results, repeat until it stops.
- **Turn limit:** the maximum number of model calls an agent may make for one task.
- **Orchestrator-workers:** a lead agent splitting a task among sub-agents and combining their results.
- **Evaluator-optimiser:** one model producing and another critiquing, in a loop.
mistakes:
- Building an agent where a simple workflow would do.
- Looping with no turn limit or budget.
- Stopping an agent just because it reuses a tool with different inputs.
- Adopting a framework without understanding the loop it hides.
- Using many agents for a task one agent handles well.

glance:
- Agent loop | model → tools → results → repeat; stop on a non-tool reply or the limit | O(turns) calls | O(history)
- Stuck detection | last k calls identical, or the last 2k alternate | O(k) | O(k)
- Choose a design | workflow if the steps are known; agent if they aren't | — | —

@@ mcp
topics: the integration problem, hosts, clients and servers, tools, resources and prompts, JSON-RPC 2.0 requests, responses, errors and notifications, stdio and Streamable HTTP transports, the 2026-07-28 specification, the Python SDK, connecting servers to hosts and the MCP connector, namespacing tools, too many tools and tool search, MCP security and tool poisoning, governance under the Agentic AI Foundation
terms:
- **Model Context Protocol (MCP):** an open standard for connecting AI applications to tools and data sources.
- **MCP host:** the application the user works in, which contains MCP clients.
- **MCP server:** a program exposing tools, resources and prompts from some system.
- **Resource:** data an MCP server offers for the application to read into context.
- **JSON-RPC 2.0:** the request-response message format MCP uses.
- **Transport:** how messages travel: stdio for local subprocesses, Streamable HTTP for web services.
- **Tool poisoning:** malicious instructions hidden in a tool's description or results.
mistakes:
- Installing MCP servers from unknown sources.
- Giving servers broader credentials than they need.
- Connecting dozens of servers so every request carries hundreds of tool definitions.
- Reporting tool failures as protocol errors, hiding them from the model.
- Letting tools from different servers clash by name.

glance:
- MCP request handling | route by method; echo the id; result or error | O(1) dispatch | O(tools) for a list
- Namespaced tool names | server__tool; validate the pattern; reject duplicates | O(tools) | O(tools)
- Pick a transport | local subprocess → stdio; shared or remote → Streamable HTTP | — | —

@@ memory-and-context
topics: context engineering, context rot, what fills an agent's context, write, select, compress and isolate, just-in-time context, compaction and summaries, server-side compaction, clearing old tool results and context editing, sub-agents, long-term memory, the memory tool, progress files, stale memories, privacy and injected memories
terms:
- **Context engineering:** choosing what information goes into the model's context at each step.
- **Context rot:** degraded recall and reasoning as the context grows long and noisy.
- **Compaction:** replacing older conversation turns with a summary.
- **Context editing:** automatically clearing old tool results or thinking from the history.
- **Just-in-time context:** loading information through tools only when it's needed.
- **Long-term memory:** information stored outside the model and loaded into later conversations.
- **Memory tool:** a tool that lets the model create, read and update memory files.
mistakes:
- Filling the context because there's room.
- Summarising on every turn instead of past a threshold.
- Deleting tool_result blocks instead of clearing their content.
- Keeping memories without dates, sources or a way for users to delete them.
- Saving untrusted text into memory where it influences future sessions.

glance:
- Compact history | summarise the older part; keep a recent tail starting with a user turn | O(n) + 1 call | O(n)
- Clear old tool results | copy; replace all but the newest k results with a placeholder | O(blocks) | O(n)
- Context strategies | write, select, compress, isolate | — | —

@@ agent-safety
topics: excessive agency, classifying actions by reversibility and reach, allow, ask and deny policies, default deny, meaningful human approval, sandboxes, scoped credentials, staging and dry runs, idempotency, turn, token and cost budgets, timeouts and rate limits, injection through tool results, action review, audit logs, behavioural testing
terms:
- **Excessive agency:** an AI system having more tools, permissions or autonomy than its task needs.
- **Permission policy:** rules deciding whether each action is allowed, needs approval or is denied.
- **Human in the loop:** a person approving or reviewing consequential actions.
- **Sandbox:** an isolated environment where code can run without access to real systems or secrets.
- **Scoped credentials:** access tokens limited to the minimum resources and operations.
- **Dry run:** producing the plan of changes without applying them.
- **Audit log:** a record of every action, its arguments, result and approval.
mistakes:
- Allowing any tool not explicitly denied.
- Approval prompts so frequent or vague that people approve without reading.
- Running agent code with the developer's own credentials.
- Checking budgets only after a task finishes.
- Letting a crashing permission rule count as permission.

glance:
- Permission decision | look up a rule (default deny); call it if it's a function; deny on error | O(1) | O(1)
- Budget | add usage after each call; raise when over a limit | O(1) per call | O(1)
- Action risk | reversible and contained → allow; consequential → ask; irreversible and external → ask or deny | — | —
