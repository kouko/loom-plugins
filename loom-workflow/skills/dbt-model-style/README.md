# dbt-model-style

[Loom](https://github.com/kouko/loom-plugins/blob/main/README.md) / [loom-workflow](../../README.md) / dbt-model-style

Keep dbt models for Redshift consistently structured and documented without changing their calculations.

## When to use

Use this when writing, editing or reviewing a dbt model. Apply the rules to new models and the part of an existing model you are touching, rather than rewriting unrelated models.

## What you get

A model with traceable reference and transformation CTEs, stable names, readable column comments and structured headers. The final CTE selects already-named columns and contains no calculations, filters or renaming.

## How to use

Install the plugin as described in its [README](../../README.md), then ask
your coding agent to use the skill. For example:

```text
Use loom-workflow:dbt-model-style to review the style of models/marts/revenue.sql; keep its calculations unchanged.
```

## Boundaries

- Calculation logic, metric definitions, NULL semantics and layer-dependency design are outside this skill’s scope.
- The agent may inspect computation to check whether a name is accurate, but flags a calculation defect rather than silently changing it.
- Mechanical header validation checks structure. Its optional manifest input checks referenced model names; neither proves business correctness.

## Further reading

- [Complete model example](references/example-model.sql)
- [Model self-check](checklists/dbt-model-self-check.md)

## Related skills

- [loom-code:build](https://github.com/kouko/loom-plugins/blob/main/loom-code/skills/build/README.md)
- [loom-workflow:critique](../critique/README.md)

Runtime instructions: [SKILL.md](SKILL.md).
