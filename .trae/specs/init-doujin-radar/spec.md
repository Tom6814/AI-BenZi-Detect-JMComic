# AI 本子成分鉴定与防雷雷达 Spec

## Why
读者在阅读同人志或漫画时，往往难以提前预判作品中是否含有自己无法接受的“毒点（避雷内容）”或期待的“萌点（喜欢内容）”。通过构建一款“AI 本子成分鉴定与防雷雷达” Web App，利用 AI 的多维信息审视和推理能力，可以有效保护读者的阅读体验。

## What Changes
- 初始化全栈项目，前端采用 Vue3 + Material 3 Expressive 规范，并在视觉上融入 Aurora Neon（极光霓虹）或 Liquid Glass（液态玻璃）风格。
- 初始化后端项目，采用 FastAPI，复用已有框架和屏蔽词库。
- 开发“AI API 配置模块”，支持 OpenAI 和 Google Gemini 格式的密钥配置与连通性测试。
- 在后端增加数据清洗功能，专门剥离支持“深度思考”模型（如 `<think>` 标签）的推理过程。
- 开发“目标检索与选择模块”，提供双模态智能搜索框（规则A：文本检索展示列表；规则B：纯数字直接锁定）。
- 开发“鉴定规则配置模块”，支持用户自定义并视觉区分【避雷清单】和【喜欢清单】。
- 实现“核心鉴定工作流”，后端整合标题、简介、作者、标签、封面（Base64/URL）和评论，按指定 System Prompt 调用 AI，并强制返回 JSON 格式。
- 开发“鉴定报告渲染”前端模块，根据 JSON 结果的 `contains` 状态应用不同颜色（红/绿/半透明玻璃态），并支持 Markdown 渲染 `reasoning` 字段。

## Impact
- Affected specs: 无历史遗留，全新项目架构。
- Affected code:
  - 前端：所有 Vue 组件、状态管理、路由设计及全局样式（CSS/Tailwind）。
  - 后端：FastAPI 路由、AI 服务调用封装、数据清洗与 JSON 解析逻辑。

## ADDED Requirements
### Requirement: AI API 配置与校验
系统应允许用户输入 API 地址和模型，并进行连通性测试。
#### Scenario: 成功保存配置
- **WHEN** 用户输入有效 API Key 并点击“测试连接”
- **THEN** 后端返回成功状态码，前端允许保存配置。

### Requirement: 数据清洗机制
系统应能处理带思考过程的模型输出。
#### Scenario: 剥离 `<think>` 标签
- **WHEN** AI 返回包含 `<think>...</think>` 的内容
- **THEN** 后端通过正则提取并剥离该内容，仅返回最终的 JSON 结果给前端。

### Requirement: 双模态智能搜索
系统应根据用户输入自动判断搜索策略。
#### Scenario: 纯数字快速定位
- **WHEN** 用户在搜索框输入纯数字（JM 号）
- **THEN** 系统直接锁定目标，仅展示标题和 JM 号确认信息，跳过封面加载以提升速度。

### Requirement: 核心鉴定工作流
系统应按规范请求 AI 接口进行成分鉴定。
#### Scenario: 成功生成报告
- **WHEN** 用户发起鉴定
- **THEN** 后端整合各项信息，使用指定的 System Prompt 请求 AI，并强制返回包含 `avoid`、`like` 和 `reasoning` 的 JSON 对象。

### Requirement: 鉴定报告高亮渲染
系统应根据鉴定结果进行极具视觉冲击力的渲染。
#### Scenario: 命中避雷元素
- **WHEN** 报告中某避雷元素的 `contains` 为 `true`
- **THEN** 该标签使用高警示度的红色/霓虹红渲染，并显示危险概率。`reasoning` 首句以加大加粗的引语样式（Blockquote）展示。
