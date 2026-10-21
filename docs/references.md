# External References

qwerdf borrows structure and process ideas from established skill repositories without copying their content verbatim.

中文：本项目只借鉴开源项目的组织方式和可验证流程，不复制外部风格库、营销话术或受保护内容。

## Referenced Projects

- [agentskills/agentskills](https://github.com/agentskills/agentskills)
- [anthropics/skills](https://github.com/anthropics/skills)
- [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)
- [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)

## Borrowed Patterns

- From `agentskills/agentskills`: select context by stage, run helpers without loading their source, and keep format validation separate from output-quality evaluation.
- From `anthropics/skills`: concise `SKILL.md`, strong trigger descriptions, progressive disclosure, references and scripts for reusable detail.
- From `vercel-labs/agent-skills`: evidence-first engineering checks, high-risk-first review flow, and framework-specific references loaded on demand.
- From `nextlevelbuilder/ui-ux-pro-max-skill`: Design System Generator thinking, `MASTER` design system plus `Page Overrides`, domain UI quality checklists, and pre-delivery visual QA gates.

## Local Adaptation

qwerdf adapts these ideas to a Product Delivery chain:

```text
$pd-vet -> $pd-prd -> $pd-blueprint -> $pd-figma -> $pd-ui-review -> $pd-plan -> $pd-fe + $pd-be -> $pd-sync -> $pd-test -> $pd-review -> $pd-git -> $pd-release
```

The local rules are intentionally product-delivery-specific:

- Product facts override design references.
- UI references influence visual style and interaction detail, not product scope.
- Real dependency readiness blocks formal implementation when dependencies are not ready.
- Mock/stub/fake implementations cannot be accepted as done, synced, or tested.
- Review findings must include evidence, severity, owner, and validation guidance.

Product-stage source review, adaptations, validation limits and usage: [Product Skills](product-skills.md).

Design-stage source review and local adaptations: [Design Skills](design-skills.md).
