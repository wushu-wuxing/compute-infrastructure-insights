# -*- coding: utf-8 -*-
"""百度文心一言 API 客户端"""

import requests
import json
import re
from typing import Dict, List, Optional, Any

# ============== 配置 ==============
BAIDU_API_KEY = '608afbf5c41f492585bcdac70c102fc6'
BAIDU_SECRET_KEY = '264f41f4288b435db396a05de3169b32'

# ============== 获取Access Token ==============
def get_access_token():
    """获取百度文心access_token"""
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": BAIDU_API_KEY,
        "client_secret": BAIDU_SECRET_KEY
    }
    response = requests.post(url, params=params)
    result = response.json()
    return result.get('access_token')


# ============== 工具函数 ==============
def parse_json_from_response(text: str) -> Optional[Dict]:
    """从AI响应中提取JSON"""
    # 尝试直接解析
    try:
        return json.loads(text)
    except:
        pass

    # 尝试从 ```json 块中提取
    match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
    if match:
        try:
            return json.loads(match.group(1))
        except:
            pass

    # 尝试找JSON对象
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        try:
            return json.loads(match.group(0))
        except:
            pass

    return None


# ============== AI出题 ==============
def generate_questions(subject: str, knowledge_point: str,
                       count: int = 5, difficulty: str = 'medium',
                       q_type: str = '选择题') -> List[Dict[str, Any]]:
    """
    AI生成练习题

    Args:
        subject: 科目
        knowledge_point: 知识点
        count: 生成数量
        difficulty: 难度 (easy/medium/hard)
        q_type: 题型

    Returns:
        题目列表
    """
    access_token = get_access_token()
    if not access_token:
        return []

    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={access_token}"

    difficulty_map = {
        'easy': '基础',
        'medium': '中等',
        'hard': '拔高'
    }
    difficulty_cn = difficulty_map.get(difficulty, '中等')

    prompt = f"""你是一个资深中学教师，请根据以下知识点生成{count}道练习题。

科目：{subject}
知识点：{knowledge_point}
难度：{difficulty_cn}
题型：{q_type}

要求：
1. 贴近真实考试风格，题目严谨
2. 答案准确，解析详细
3. 只返回题目，不要其他解释
4. 以JSON格式输出，结构如下：
{{
  "questions": [
    {{
      "content": "题目内容",
      "options": {{"A": "选项A", "B": "选项B", "C": "选项C", "D": "选项D"}},
      "answer": "A",
      "explanation": "解析内容"
    }}
  ]
}}

注意：只输出JSON，不要其他文字。"""

    payload = {
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    if 'error_code' in result:
        print(f"API错误: {result}")
        return []

    content = result.get('result', '')
    parsed = parse_json_from_response(content)

    if parsed and 'questions' in parsed:
        questions = []
        for q in parsed['questions']:
            questions.append({
                'subject': subject,
                'knowledge_point': knowledge_point,
                'type': q_type,
                'difficulty': difficulty,
                'content': q.get('content', ''),
                'options': q.get('options', {}),
                'answer': q.get('answer', ''),
                'explanation': q.get('explanation', '')
            })
        return questions

    return []


# ============== AI解析 ==============
def explain_question(question_content: str, correct_answer: str,
                     user_answer: str, options: Optional[Dict] = None) -> str:
    """
    AI生成题目解析

    Args:
        question_content: 题目内容
        correct_answer: 正确答案
        user_answer: 用户答案
        options: 选项（如有）

    Returns:
        解析文本
    """
    access_token = get_access_token()
    if not access_token:
        return "AI解析服务暂不可用"

    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={access_token}"

    options_text = ""
    if options:
        options_text = "\n选项：\n" + "\n".join([f"{k}. {v}" for k, v in options.items()])

    prompt = f"""请分析以下题目：

题目：{question_content}{options_text}

正确答案：{correct_answer}
你的答案：{user_answer}

请从以下角度进行分析：
1. 解题思路（详细步骤）
2. 知识点拆解
3. 易错点提示
4. 如果答错，说明错误原因

请用清晰的结构回答。"""

    payload = {
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    if 'error_code' in result:
        return f"解析失败: {result.get('error_msg', '未知错误')}"

    return result.get('result', '解析内容获取失败')


# ============== AI知识点推荐 ==============
def recommend_knowledge_points(subject: str, wrong_count: int = 0) -> List[str]:
    """
    推荐薄弱知识点

    Args:
        subject: 科目
        wrong_count: 错题数量

    Returns:
        知识点列表
    """
    access_token = get_access_token()
    if not access_token:
        return []

    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={access_token}"

    prompt = f"""作为中学教育专家，请为{subject}科目推荐5个常见的薄弱知识点。

要求：
1. 针对中学生常见的易错点
2. 列出知识点名称即可
3. 以JSON格式输出：{{"points": ["知识点1", "知识点2", ...]}}"""

    payload = {
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    if 'error_code' in result:
        return []

    content = result.get('result', '')
    parsed = parse_json_from_response(content)

    if parsed and 'points' in parsed:
        return parsed['points']

    return []


if __name__ == '__main__':
    # 测试
    print("测试出题...")
    questions = generate_questions("数学", "一元二次方程", count=2)
    for q in questions:
        print(f"题目: {q['content']}")
        print(f"答案: {q['answer']}")
        print()
