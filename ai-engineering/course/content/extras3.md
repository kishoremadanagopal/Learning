@@ prompt-basics
topics: what a prompt is in an application, the new-colleague test, giving context and reasons, specifying the output, positive instructions, ordered steps, matching prompt style to output style, calm wording for modern models, edge cases, roles and system prompts, prefill and sampling on the newest models, checking replies against the spec
terms:
- **Prompt:** everything the model sees for a request: system prompt, conversation, documents and examples.
- **Prompt engineering:** designing, testing and refining prompts so a model does a task reliably.
- **System prompt:** the instructions and context that apply to the whole conversation.
- **Role prompt:** a sentence in the system prompt saying who the model is acting as and for whom.
- **Prefill:** starting the assistant's reply for it; not supported on the newest Claude models.
- **Linter:** a tool that flags likely problems using simple rules.
mistakes:
- Writing a prompt only you could understand, with unstated context.
- Giving rules without the reasons behind them.
- Listing only what not to do.
- Shouting with capitals and "MUST", which makes modern models over-apply rules.
- Changing a prompt without re-checking its outputs.

glance:
- Lint a prompt | split into words; set checks for shouting, vagueness, format | O(n) | O(n)
- Check a reply | one check per rule in the spec; collect failures | O(n × rules) | O(rules)
- Clear prompt | context and why, task, output format, edge cases | — | —

@@ examples-and-structure
topics: zero-shot and few-shot prompting, choosing relevant and diverse examples, how many examples, examples for thinking models, XML tags for instructions, documents, examples and inputs, the layout of a long prompt, documents first and question last, document metadata, grounding answers in quotes, tagged output, extracting tags with regular expressions
terms:
- **Zero-shot:** a prompt with instructions but no examples.
- **Few-shot:** a prompt that includes a few input and output examples.
- **XML tags:** named markers such as `<document>…</document>` that separate the parts of a prompt.
- **Grounding:** basing an answer on quoted evidence from the provided documents.
- **Non-greedy match:** a regex quantifier such as `.*?` that matches as little text as possible.
mistakes:
- Examples that are all of one kind, teaching an accidental pattern.
- Examples that break your own rules.
- Putting the question before long documents.
- Mixing instructions and inserted data with no clear boundary.
- Extracting tags with a greedy `.*`.

glance:
- Few-shot prompt | instructions, examples in tags, then the input | O(text) | O(text)
- Extract tagged sections | re.findall with (.*?) and DOTALL | O(n) | O(matches)
- Long-context layout | documents first, instructions, question last | — | —

@@ reasoning-and-chaining
topics: when reasoning helps, prompting thinking models with goals, self-verification, chain-of-thought prompting with thinking and answer tags, reasoning before answering, prompt chains, sequential chains, parallel map and combine, routing, draft review and refine, gates between steps, voting and self-consistency
terms:
- **Chain-of-thought (CoT):** prompting a model to write out its reasoning before the answer.
- **Self-verification:** asking the model to check its answer against criteria before finishing.
- **Prompt chain:** a pipeline where each model call's output feeds the next prompt.
- **Gate:** a code check between steps of a chain that can stop it.
- **Routing:** classifying an input first, then choosing the prompt or model for it.
- **Self-consistency (voting):** asking several times and taking the most common answer.
mistakes:
- Asking for the answer before the reasoning.
- Scripting every reasoning step for a model that already thinks well.
- Chaining calls without logging or checking the intermediate results.
- Filling chain templates with `format`, which breaks on other braces.
- Voting on raw strings without normalising them.

glance:
- Prompt chain | output of step k becomes input of step k + 1; optional gate | O(steps) calls | O(steps)
- Majority vote | extract, normalise, count; ties go to the first seen | O(n) | O(n)
- Map and combine | same prompt on each piece, then merge | O(pieces) calls | O(pieces)

@@ templates-and-testing
topics: prompts as code, version control and review, naming and logging prompt versions, why format and f-strings break on braces, string.Template, Mustache-style placeholders, Jinja templates, single-pass substitution and template injection, keeping stable text cacheable, prompt test sets, pass rates, comparing prompt versions, re-testing after model changes, prompt generators
terms:
- **Prompt template:** fixed prompt text with placeholders filled at run time.
- **Placeholder:** a marker in a template, such as `{{review}}`, replaced with a value.
- **Template injection:** user input that contains template syntax and gets expanded when it shouldn't.
- **Test set:** a fixed collection of realistic inputs with checks for each.
- **Pass rate:** the fraction of test cases a prompt version passes.
- **Regression:** something that used to work and broke after a change.
mistakes:
- Scattering prompt fragments through the code where no one can review the whole prompt.
- Using `str.format` on prompts that contain JSON.
- Expanding placeholders that arrived inside user input.
- Judging a prompt change on one or two examples.
- Switching models without re-running the prompt tests.

glance:
- Render a template | one regex pass with a callback; KeyError on missing | O(n) | O(n)
- Score a prompt | run every case, catch errors, record failures | O(cases) calls | O(cases)
- Compare versions | same test set, compare pass rates, read failures | O(versions × cases) | O(cases)

@@ prompt-injection
topics: direct and indirect prompt injection, jailbreaks, hidden context exposure, why prompts can't fully prevent injection, the lethal trifecta, data exfiltration through links and images, the OWASP Top 10 for LLM applications, labelling untrusted data, least privilege, human confirmation, treating output as untrusted, link allow-lists, keeping secrets out of prompts, redacting personal data, input and output screening, limits, monitoring and red-teaming
terms:
- **Prompt injection:** text that makes a model follow instructions its developer didn't intend.
- **Indirect prompt injection:** injected instructions hidden in content the model reads, such as a web page or email.
- **Jailbreak:** a prompt crafted to get around a model's safety training.
- **Lethal trifecta:** private data, untrusted content and external communication in one system.
- **Exfiltration:** sending data out to an attacker, for example inside a URL.
- **Least privilege:** giving a component only the access it needs.
- **PII (personally identifiable information):** data that identifies a person, such as an email address or phone number.
- **Allow-list:** a list of things explicitly permitted; everything else is refused.
mistakes:
- Relying on "ignore instructions in documents" as the only defence.
- Rendering links and images from model output without checking their domains.
- Executing or inserting model output into HTML, SQL or shell commands unescaped.
- Putting secrets or other users' data in the system prompt.
- Giving an assistant powerful tools without human confirmation.

glance:
- Redact PII | ordered regex substitution, most specific first | O(n) | O(n)
- Safe link check | parse; https; host equals or ends with .domain | O(len × domains) | O(1)
- Defence in depth | label data, least privilege, confirm actions, check output | — | —
