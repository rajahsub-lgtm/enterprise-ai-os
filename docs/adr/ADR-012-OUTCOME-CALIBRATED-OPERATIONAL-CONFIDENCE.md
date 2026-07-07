\# ADR-012: Operational Confidence Must Be Outcome-Calibrated



\## Status



Accepted



\## Context



EAIOS uses Operational Confidence to determine how much validation, escalation, and governance depth a recommendation or action requires.



In early prototypes, confidence may be represented with simplified or mock values. That is acceptable for a walking skeleton, but it is not sufficient for enterprise trust.



Operational Confidence must eventually be grounded in observed outcomes.



The system should be able to answer:



\* What confidence did we have before action?

\* What outcome did we expect?

\* What action was taken?

\* What actually happened?

\* Was our confidence calibrated?

\* Are we repeatedly overconfident or underconfident for a pattern?



\## Decision



EAIOS will track the outcome of governed actions and compare actual outcomes against the confidence level that preceded them.



For example:



```text

Of actions rated HIGH confidence, what fraction resolved as expected?

```



Outcome-calibrated confidence should track:



\* action ID

\* pattern ID

\* pre-action confidence level

\* pre-action confidence score

\* expected outcome

\* governance decision

\* human approval state, if applicable

\* execution result

\* resolution time

\* recurrence within a defined window

\* human override

\* false positive indicator

\* false negative indicator

\* calibration error

\* learning recommendation



Sustained miscalibration must not silently overwrite memory or reinforce an incorrect pattern.



If miscalibration persists, EAIOS may:



\* lower confidence

\* require additional evidence

\* escalate future similar actions

\* require human review

\* mark the pattern for review

\* weaken or retire a learned pattern

\* recommend threshold adjustment



\## Design Principle



Operational Confidence is not merely a score.



It is an empirically tested claim about expected enterprise outcomes.



\## Sprint 1 Boundary



In EAIOS 2 Sprint 1, Operational Confidence calibration is a Defined Interface.



Sprint 1 may define the outcome record shape and calibration concept, but does not implement the full calibration engine.



Sprint 1 should avoid hardcoded historical success rates where they affect governance decisions.



\## Consequences



This makes the learning loop honest.



It turns confidence from an assertion into evidence.



It also supports a stronger architecture-review story because EAIOS can eventually prove whether its confidence levels are reliable.



\## Future Work



Future EAIOS releases may add:



\* governed action outcome records

\* confidence-vs-outcome comparison

\* calibration error calculation

\* reliability curves

\* confidence threshold adjustment recommendations

\* miscalibration alerts

\* pattern reinforcement

\* pattern weakening

\* human review workflow for miscalibrated patterns

\* Command Center calibration metrics



