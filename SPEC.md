# 题库刷题系统 · 产品规格书

> 版本：v1.0  
> 日期：2026-06-22  
> 负责人：衍姝

---

## 1. 产品概述

**产品名称：** 智学题库  
**类型：** 微信小程序（面向初高中学生）  
**核心价值：** AI智能出题 + 真题库打底 + 个性化练习

**目标用户：** 初高中学生（13-18岁）

**支持科目：** 语文、数学、英语、政治、历史、地理

---

## 2. 功能模块

### 2.1 科目选择首页
- 6个科目入口（语/数/英/政/史/地）
- 每个科目显示：总题量、本周练习次数、正确率
- 快捷入口：错题本、学习报告

### 2.2 章节练习
- 按知识点/章节选择题目
- 题型：选择题（单选/多选）、填空题、判断题
- 答题模式：即时判分 + 显示答案
- 题目来源：优先从题库抽取，题库不足时AI补充

### 2.3 AI出题
- 输入知识点关键词
- AI生成针对性练习题（3-5道/组）
- 支持指定难度（基础/进阶/拔高）
- 支持指定题型

### 2.4 AI解析
- 答题后展示详细解析
- 解析内容：解题思路 + 知识点拆解 + 相关考点
- 关联知识点推送（类似题目推荐）

### 2.5 错题本
- 自动收录做错的题目
- 支持分类查看（按科目/按知识点）
- 支持重新练习
- 错题复习提醒（可设置）

### 2.6 学习报告
- 每周刷题量统计
- 各科正确率趋势
- 薄弱知识点标识
- 与AI的对话历史（提问记录）

---

## 3. 技术架构

### 3.1 前端
| 项目 | 技术 |
|------|------|
| 框架 | uni-app |
| 平台 | 微信小程序 |
| 状态管理 | Vuex |
| UI组件 | uView |

### 3.2 后端
| 项目 | 技术 |
|------|------|
| 框架 | Flask |
| 数据库 | SQLite |
| AI接入 | 百度文心一言 API (ERNIE 4.0) |
| 题库 | 本地SQLite + AI动态生成 |

### 3.3 数据库设计

**题目表 (questions)**
- id, subject, chapter, knowledge_point, type, difficulty, content, options(JSON), answer, explanation, source, created_at

**用户答题记录表 (answer_records)**
- id, openid, question_id, user_answer, is_correct, answered_at

**错题表 (wrong_questions)**
- id, openid, question_id, wrong_count, last_reviewed, mastered

**用户表 (users)**
- id, openid, nickname, avatar, created_at

---

## 4. API设计

| 接口 | 方法 | 说明 |
|------|------|------|
| /api/subjects | GET | 获取科目列表 |
| /api/questions | GET | 获取题目列表（按科目/章节） |
| /api/questions/{id} | GET | 获取题目详情 |
| /api/ai/generate | POST | AI生成题目 |
| /api/ai/explain | POST | AI题目解析 |
| /api/answers | POST | 提交答题记录 |
| /api/wrong | GET | 获取错题列表 |
| /api/stats | GET | 获取学习统计 |
| /api/wrong/{id}/review | POST | 标记已掌握 |

---

## 5. AI Prompt设计

### 出题Prompt
```
你是一个资深中学教师，请根据以下知识点生成{count}道练习题。

科目：{subject}
知识点：{knowledge_point}
难度：{difficulty}
题型：{type}

要求：
1. 贴近真实考试风格
2. 答案准确，解析详细
3. 以JSON格式输出
```

### 解析Prompt
```
题目：{question_content}
正确答案：{correct_answer}
你的答案：{user_answer}

请分析：
1. 解题思路
2. 知识点拆解
3. 易错点提示
```

---

## 6. 交付物

- [ ] 微信小程序前端（uni-app项目）
- [ ] Flask后端服务
- [ ] SQLite题库（初始1000题/科）
- [ ] AI接入模块
- [ ] 部署文档

---

## 7. 优先级

| 阶段 | 内容 | 目标 |
|------|------|------|
| P0 | 章节练习 + AI出题 | 核心闭环跑通 |
| P1 | AI解析 + 错题本 | 学习效果保障 |
| P2 | 学习报告 + 数据统计 | 提升粘性 |
| P3 | 题库完善 + 运营功能 | 长期价值 |
