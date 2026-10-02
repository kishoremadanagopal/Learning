@@ ab-testing
topics: randomised experiments, pre-registration, sample size for proportions, sample ratio mismatch, the two-proportion z-test, absolute vs relative lift, guardrail metrics, segments, peeking
terms:
- **A/B test:** a randomised experiment comparing a control (A) with a new version (B).
- **Control / treatment:** the current version, and the version being tested.
- **Randomisation:** assigning users to groups by chance, so the groups differ only in the change.
- **Primary metric:** the one measure the test is designed to judge.
- **Guardrail metric:** a measure that mustn't get worse, like revenue or page speed.
- **Minimum detectable effect (MDE):** the smallest lift the test is sized to detect.
- **Sample ratio mismatch (SRM):** groups that differ in size more than chance allows, usually a sign of a bug.
- **Two-proportion z-test:** a test comparing two rates, like conversion rates.
- **Absolute lift:** the difference between rates, in percentage points.
- **Relative lift:** the difference divided by the control rate, as a percentage.
- **Peeking:** checking results repeatedly and stopping when they look significant.
mistakes:
- Peeking and stopping early.
- Mixing up percentage points and percent.
- Treating unplanned segment results as conclusions.

@@ final-project
topics: an end-to-end statistical analysis: describing, visualising, intervals, ANOVA, multiple regression, model checks, residual-based insights, and a write-up with caveats
terms:
- **Exploratory analysis:** describing and visualising data before testing anything.
- **Like-for-like comparison:** comparing groups with other factors held fixed.
- **Fitted value:** the model's prediction for a row in the data.
- **Observational data:** data collected without randomly assigning anything, which shows associations rather than proven causes.
- **Caveat:** a stated limit on how far results can be trusted or generalised.
mistakes:
- Comparing raw group averages when the groups differ in other important ways.
- Writing numbers in the report that don't match the output.
- Claiming causation from observational data.
