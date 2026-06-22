# -*- coding: utf-8 -*-
"""Initialize question bank with seed data"""

from database import init_db, add_question

SEED_QUESTIONS = [
    {
        "subject": "\u6570\u5b66",
        "chapter": "\u4e00\u5143\u4e8c\u6b21\u65b9\u7a0b",
        "knowledge_point": "\u6c42\u6839\u516c\u5f0f",
        "type": "\u9009\u62e9\u9898",
        "difficulty": "easy",
        "content": "\u4e00\u5143\u4e8c\u6b21\u65b9\u7a0b x\u00b2 - 5x + 6 = 0 \u7684\u89e3\u662f\uff1f",
        "options": {"A": "x=1 \u6216 x=6", "B": "x=2 \u6216 x=3", "C": "x=-2 \u6216 x=-3", "D": "x=1 \u6216 x=5"},
        "answer": "B",
        "explanation": "\u56e0\u5f0f\u5206\u89e3\uff1a(x-2)(x-3)=0\u6545x=2\u6216x=3"
    },
    {
        "subject": "\u6570\u5b66",
        "chapter": "\u4e00\u5143\u4e8c\u6b21\u65b9\u7a0b",
        "knowledge_point": "\u5224\u522b\u5f0f",
        "type": "\u9009\u62e9\u9898",
        "difficulty": "medium",
        "content": "\u5173\u4e8e x \u7684\u65b9\u7a0b x\u00b2 + mx + 4 = 0 \u6709\u4e24\u4e2a\u76f8\u7b49\u7684\u5b9e\u6570\u6839\uff0c\u5219 m \u7684\u503c\u4e3a\uff1f",
        "options": {"A": "m=4 \u6216 m=-4", "B": "m=4", "C": "m=-4", "D": "m=\u00b14"},
        "answer": "A",
        "explanation": "\u5224\u522b\u5f0f\u0394=m\u00b2-16=0\uff0c\u6240\u4ee5m\u00b2=16\uff0cm=\u00b14"
    },
    {
        "subject": "\u6570\u5b66",
        "chapter": "\u4e09\u89d2\u5f62",
        "knowledge_point": "\u52fe\u80a1\u5b9a\u7406",
        "type": "\u586b\u7a7a\u9898",
        "difficulty": "easy",
        "content": "\u5728\u76f4\u89d2\u4e09\u89d2\u5f62\u4e2d\uff0c\u4e24\u6761\u76f4\u89d2\u8fb9\u5206\u522b\u4e3a3\u548c4\uff0c\u5219\u659c\u8fb9\u957f\u4e3a____",
        "options": None,
        "answer": "5",
        "explanation": "\u52fe\u80a1\u5b9a\u7406\uff1a3\u00b2+4\u00b2=9+16=25\uff0c\u659c\u8fb9=\u221a25=5"
    },
    {
        "subject": "\u8bed\u6587",
        "chapter": "\u6587\u8a00\u6587",
        "knowledge_point": "\u5b9e\u8bcd\u89e3\u91ca",
        "type": "\u9009\u62e9\u9898",
        "difficulty": "medium",
        "content": "\u201c\u901d\u8005\u5982\u65af\u592b\uff0c\u4e0d\u820d\u6635\u591c\u201d\u4e2d\u201c\u901d\u201d\u5b57\u7684\u542b\u4e49\u662f\uff1f",
        "options": {"A": "\u6b7b\u4ea1", "B": "\u8fc7\u53bb", "C": "\u4e22\u5931", "D": "\u79bb\u5f00"},
        "answer": "B",
        "explanation": "\u201c\u901d\u201d\u5728\u6b64\u5904\u610f\u4e3a\u201c\u6d41\u901d\u3001\u6d88\u901d\u201d\uff0c\u5f62\u5bb9\u65f6\u95f4\u50cf\u6d41\u6c34\u4e00\u6837\u6d41\u901d"
    },
    {
        "subject": "\u8bed\u6587",
        "chapter": "\u53e4\u8bd7\u8bcd",
        "knowledge_point": "\u8bd7\u53e5\u7406\u89e3",
        "type": "\u9009\u62e9\u9898",
        "difficulty": "easy",
        "content": "\u201c\u4f1a\u5f53\u51cc\u7edd\u9876\uff0c\u4e00\u89c8\u4f17\u5c71\u5c0f\u201d\u51fa\u81ea\u675c\u752b\u7684\uff1f",
        "options": {"A": "\u300a\u6625\u671b\u300b", "B": "\u300a\u671b\u5cb8\u300b", "C": "\u300a\u767b\u9ad8\u300b", "D": "\u300a\u8305\u5c4b\u4e3a\u79cb\u98ce\u6240\u7834\u6b4c\u300b"},
        "answer": "B",
        "explanation": "\u6b64\u53e5\u51fa\u81ea\u675c\u752b\u7684\u300a\u671b\u5cb8\u300b\uff0c\u63cf\u5199\u7684\u662f\u6cf0\u5c71\u7684\u96c4\u4f1f\u666f\u8c61"
    },
    {
        "subject": "\u82f1\u8bed",
        "chapter": "\u8bed\u6cd5",
        "knowledge_point": "\u65f6\u6001",
        "type": "\u9009\u62e9\u9898",
        "difficulty": "easy",
        "content": "She _____ to school every day. (not walk)",
        "options": {"A": "doesn't walks", "B": "doesn't walk", "C": "don't walk", "D": "isn't walk"},
        "answer": "B",
        "explanation": "\u4e3b\u8bedShe\u662f\u7b2c\u4e09\u4eba\u79cd\u5355\u6570\uff0c\u5426\u5b9a\u53e5\u7528doesn't\uff0c\u540e\u63a5\u52a8\u8bcd\u539f\u5f62walk"
    },
    {
        "subject": "\u82f1\u8bed",
        "chapter": "\u8bcd\u6c47",
        "knowledge_point": "\u8bcd\u4e49\u8fa8\u6790",
        "type": "\u9009\u62e9\u9898",
        "difficulty": "medium",
        "content": "The movie was so _____ that I fell asleep.",
        "options": {"A": "interesting", "B": "exciting", "C": "boring", "D": "amazing"},
        "answer": "C",
        "explanation": "\u6839\u636e\u540e\u534a\u53e5\u6211\u7761\u89c9\u4e86\u53ef\u77e5\u7535\u5f71\u5f88\u65e0\u804a\uff0cboring\u610f\u4e3a\u65e0\u804a\u7684"
    },
    {
        "subject": "\u653f\u6cbb",
        "chapter": "\u7ecf\u6d4e",
        "knowledge_point": "\u5e02\u573a\u7ecf\u6d4e",
        "type": "\u9009\u62e9\u9898",
        "difficulty": "easy",
        "content": "\u793e\u4f1a\u4e3b\u4e49\u5e02\u573a\u7ecf\u6d4e\u7684\u57fa\u672c\u7279\u5f81\u662f\uff1f",
        "options": {"A": "\u8ba1\u5212\u4e3a\u4e3b\uff0c\u5e02\u573a\u4e3a\u8f85", "B": "\u5e02\u573a\u8d77\u51b3\u5b9a\u6027\u4f5c\u7528", "C": "\u4ee5\u516c\u6709\u5236\u4e3a\u4e3b\u4f53", "D": "\u5b8c\u5168\u7ade\u4e89"},
        "answer": "C",
        "explanation": "\u793e\u4f1a\u4e3b\u4e49\u5e02\u573a\u7ecf\u6d4e\u7684\u57fa\u672c\u7279\u5f81\u662f\u4ee5\u516c\u6709\u5236\u4e3a\u4e3b\u4f53\uff0c\u591a\u79cd\u6240\u6709\u5236\u7ecf\u6d4e\u5171\u540c\u53d1\u5c55"
    },
    {
        "subject": "\u5386\u53f2",
        "chapter": "\u4e2d\u56fd\u53e4\u4ee3\u53f2",
        "knowledge_point": "\u671d\u4ee3\u987a\u5e8f",
        "type": "\u9009\u62e9\u9898",
        "difficulty": "easy",
        "content": "\u4ee5\u4e0b\u671d\u4ee3\u6309\u65f6\u95f4\u987a\u5e8f\u6392\u5217\u6b63\u786e\u7684\u662f\uff1f",
        "options": {"A": "\u79e6-\u6c49-\u5510-\u5b8b", "B": "\u6c49-\u79e6-\u5510-\u5b8b", "C": "\u79e6-\u6c49-\u5b8b-\u5510", "D": "\u6c49-\u5510-\u79e6-\u5b8b"},
        "answer": "A",
        "explanation": "\u4e2d\u56fd\u671d\u4ee3\u987a\u5e8f\uff1a\u79e6\u2192\u6c49\u2192\u4e09\u56fd\u2192\u664b\u2192\u5357\u5317\u671d\u2192\u968b\u2192\u5510\u2192\u5b8b\u2192\u5143\u2192\u660e\u2192\u6e05"
    },
    {
        "subject": "\u5386\u53f2",
        "chapter": "\u4e2d\u56fd\u8fd1\u4ee3\u53f2",
        "knowledge_point": "\u91cd\u8981\u4e8b\u4ef6",
        "type": "\u586b\u7a7a\u9898",
        "difficulty": "medium",
        "content": "1911\u5e74\u7206\u53d1\u7684\u8f9b\u4ea8\u9769\u547d\u63a8\u7ffc\u4e86____\u738b\u671d\u7684\u7edf\u6cbb\u3002",
        "options": None,
        "answer": "\u6e05\u671d",
        "explanation": "\u8f9b\u4ea8\u9769\u547d\u4e8e1911\u5e7410\u670810\u65e5\u6b66\u660c\u8d77\u4e49\u7206\u53d1\uff0c\u6700\u7ec8\u63a8\u7ffc\u4e86\u6e05\u671d\u7684\u7edf\u6cbb\uff0c\u5efa\u7acb\u4e86\u4e2d\u534e\u6c11\u56fd"
    },
    {
        "subject": "\u5730\u7406",
        "chapter": "\u81ea\u7136\u5730\u7406",
        "knowledge_point": "\u6c14\u5019\u7c7b\u578b",
        "type": "\u9009\u62e9\u9898",
        "difficulty": "easy",
        "content": "\u5317\u4eac\u5c5e\u4e8e\u54ea\u79cd\u6c14\u5019\u7c7b\u578b\uff1f",
        "options": {"A": "\u70ed\u5e26\u5b63\u98ce\u6c14\u5019", "B": "\u4e9a\u70ed\u5e26\u5b63\u98ce\u6c14\u5019", "C": "\u6e29\u5e26\u5b63\u98ce\u6c14\u5019", "D": "\u6e29\u5e26\u5927\u9646\u6027\u6c14\u5019"},
        "answer": "C",
        "explanation": "\u5317\u4eac\u4f4d\u4e8e\u534e\u5317\u5e73\u539f\uff0c\u5c5e\u6e29\u5e26\u5b63\u98ce\u6c14\u5019\uff0c\u590f\u5b63\u9ad8\u6e29\u591a\u96e8\uff0c\u51ac\u5b63\u5bd2\u51b7\u5e72\u71e5"
    },
    {
        "subject": "\u5730\u7406",
        "chapter": "\u4e2d\u56fd\u5730\u7406",
        "knowledge_point": "\u884c\u653f\u533a\u5212",
        "type": "\u9009\u62e9\u9898",
        "difficulty": "easy",
        "content": "\u4e2d\u56fd\u9762\u79ef\u6700\u5927\u7684\u7701\u7ea7\u884c\u653f\u533a\u5212\u662f\uff1f",
        "options": {"A": "\u65b0\u7586\u7ef4\u543e\u5c14\u81ea\u6cbb\u533a", "B": "\u897f\u85cf\u81ea\u6cbb\u533a", "C": "\u5185\u8499\u53e4\u81ea\u6cbb\u533a", "D": "\u9752\u6d77\u7701"},
        "answer": "A",
        "explanation": "\u65b0\u7586\u7ef4\u543e\u5c14\u81ea\u6cbb\u533a\u9762\u79ef\u7ea2166\u4e07\u5e73\u65b9\u516c\u91cc\uff0c\u662f\u4e2d\u56fd\u9762\u79ef\u6700\u5927\u7684\u7701\u7ea7\u884c\u653f\u533a\u5212"
    },
]


def seed_questions():
    init_db()
    count = 0
    for q in SEED_QUESTIONS:
        add_question(
            subject=q["subject"],
            content=q["content"],
            q_type=q["type"],
            answer=q["answer"],
            options=q.get("options"),
            explanation=q.get("explanation"),
            chapter=q.get("chapter"),
            knowledge_point=q.get("knowledge_point"),
            difficulty=q.get("difficulty", "medium"),
            source="seed"
        )
        count += 1
    print(f"Imported {count} seed questions")


if __name__ == "__main__":
    seed_questions()
