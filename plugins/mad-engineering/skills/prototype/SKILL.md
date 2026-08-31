---
name: prototype
description: Build the smallest disposable software experience that can answer a product, interaction, or feasibility question. Use when trying the idea will teach more than discussing it; do not use for production implementation.
---

# Prototype

Turn one important uncertainty into something the user can experience or measure. Optimize for learning speed, not completeness.

## Define the question

State the question the prototype must answer, who will try it, the evidence that would change the decision, and what fidelity that evidence requires. If the question is still unclear, return to exploration before building.

Choose the thinnest end-to-end path that exposes the uncertain interaction or technical boundary. Fake data, services, and secondary screens unless their realism is the question being tested.

## Keep it disposable

Isolate the prototype from production paths and label shortcuts that would be unsafe to retain. Avoid migrations, generalized architecture, extensive testing, polished edge cases, or infrastructure that does not improve the experiment.

Use the project's existing stack when it is cheap. Choose a faster local medium when production fidelity would add cost without improving the answer. Do not publish, deploy, contact users, or mutate production systems without separate authorization.

## Learn from the real surface

Run the prototype on the closest practical surface: browser, device, simulator, or focused technical probe. Observe what happened rather than treating completed code as validation.

Finish with the question, what was built, what was deliberately faked or omitted, evidence observed, limitations, and the resulting decision: discard, revise, test again, or proceed to durable implementation. Do not silently harden the prototype into production code.
