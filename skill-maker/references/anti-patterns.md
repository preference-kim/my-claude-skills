# Skill design checks

Apply these checks in order. Correct routing before polishing a body that will
not load for its intended task.

1. Routing is evaluated. A new skill or changed description needs at least three
   positive utterances, one negative, and one adjacent collision. Compare old and
   new routes before accepting the change. Qualify broad words such as "review"
   with the intended artifact or task. Record reusable collisions in the existing
   routing cases.
2. The description serves discovery. State when the user needs the skill, not
   what its files contain. Every session pays for this text. Name relevant user
   actions and enough scope to distinguish neighboring workflows. A negative case
   must have an explainable exclusion.
3. Each loaded rule prevents a plausible failure. Retain scope, entry conditions,
   required behavior, completion criteria, and local contracts. Remove motivation,
   tutorials, planning notes, repeated conclusions, and abstract instructions that
   cannot change a decision. Let document structure follow the task rather than
   imposing one output template on unrelated work.
4. Reusable failures become regression cases. Capture the general failure and
   smallest preventive rule at its existing owner. Keep incident IDs, dates, and
   history out of runtime instructions unless they affect execution. During
   critique, report candidate cases separately. Integrate them when maintenance
   is authorized, otherwise include them in the proposed bundle.
5. Global rules stay global. A skill needs a sharper local contract or exception
   to repeat a general editing, safety, communication, or collaboration rule.
   For example, inspect frontmatter and referenced files to assess a skill's
   loading behavior. Do not repeat generic repository-inspection advice.
6. File boundaries reduce actual load or reconstruction. Use references for
   conditional knowledge, scripts for reusable deterministic work, and assets for
   output resources. Each reference needs an entry condition and purpose. Trace
   requirements through every consumer, including isolated reviewers. Moving the
   entire body to a file that is always read saves no context. Empty folders and
   duplicate READMEs provide no execution benefit.
7. Volatile facts have an owner or task-time lookup. Current model catalogs,
   pricing, service limits, and API shapes need an authoritative lookup or a
   maintained conditional reference. Durable local policy can remain inline.
   Keep the applicability conditions of any version-specific fact.
8. Exact recipes earn their space. Preserve commands that are the reusable
   artifact or contain fragile local flags. For ordinary shell and Git steps,
   state the intended result and constraints so the agent can adapt to the
   current environment.

These checks adapt Perplexity Research's
["Designing, Refining, and Maintaining Agent Skills at Perplexity"](https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity).
