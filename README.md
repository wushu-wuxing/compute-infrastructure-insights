# 题库刷题系统后端

智学题库微信小程序后端服务。

## 技术栈
- Flask + SQLite
- 百度文心一言AI

## 本地运行
```bash
pip install -r requirements.txt
python server.py
```

## API服务
- 科目列表: GET /api/subjects
- 题目列表: GET /api/questions?subject=数学&limit=10
- AI出题: POST /api/ai/generate
- AI解析: POST /api/ai/explain
- 答题记录: POST /api/answers
- 错题列表: GET /api/wrong
- 学习统计: GET /api/stats
