# Figma Review Reference

用于 Figma frame、变量、组件及 `ui/figma-handoff.md`；严重性与不能放行条件见 [共享规则](../../qwerdf-common/ui-review-rules.md)，不另定义门禁。

- 按可用 Figma skill 获取目标 frame context 与 screenshot，记录文件 / frame 标识、版本或读取时间、尺寸、状态。无访问权限时保留证据缺口，不编造截图结论。
- 对照产品事实与页面规格确认范围，再检查 `MASTER` / Page Overrides、语义变量、字体样式、组件 variant、交互反馈及响应式约束；不要把组件名称相同当作行为一致。
- 复用现有组件与变量映射，确认实例使用哪个组件、variant 和 token。截图只支持视觉观察，未读节点时不声称变量绑定或精确尺寸已验证。
- 检查适用状态与异常恢复。共享组件可统一展示一次状态，页面记录引用和差异，不要求每页复制整套状态 frame。
- 放大复核主 CTA、关键金额 / 状态、固定栏及用户指出区域；检查同类组件的语义和布局策略，允许批准变体与合理内容高度差。
- Figma 与产品事实冲突回 `$pd-blueprint` / `$pd-plan`；设计稿问题归 `$pd-figma`。判定实现偏离时，同时提供可比 Figma 与页面证据。
