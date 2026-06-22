# -*- coding: utf-8 -*-
"""题库刷题系统 - Flask服务端"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from database import (
    init_db, get_subjects, get_questions, get_question_by_id,
    add_question, add_answer_record, get_wrong_questions,
    mark_mastered, get_stats, get_or_create_user
)
from ai_client import generate_questions, explain_question
import json

app = Flask(__name__)
CORS(app)

# 初始化数据库
init_db()


@app.route('/')
def index():
    return jsonify({'message': '智学题库API服务运行中', 'version': '1.0'})


# ============== 科目接口 ==============
@app.route('/api/subjects', methods=['GET'])
def api_subjects():
    """获取所有科目及统计"""
    subjects = get_subjects()
    return jsonify({'code': 0, 'data': subjects})


# ============== 题目接口 ==============
@app.route('/api/questions', methods=['GET'])
def api_get_questions():
    """获取题目列表"""
    subject = request.args.get('subject', '')
    chapter = request.args.get('chapter')
    knowledge_point = request.args.get('knowledge_point')
    limit = int(request.args.get('limit', 10))

    if not subject:
        return jsonify({'code': 400, 'msg': '缺少subject参数'})

    questions = get_questions(subject, chapter, knowledge_point, limit)

    # 不返回答案
    for q in questions:
        q.pop('answer', None)
        q.pop('explanation', None)

    return jsonify({'code': 0, 'data': questions})


@app.route('/api/questions/<int:question_id>', methods=['GET'])
def api_get_question(question_id):
    """获取题目详情"""
    question = get_question_by_id(question_id)
    if not question:
        return jsonify({'code': 404, 'msg': '题目不存在'})

    # 不返回答案
    question.pop('answer', None)
    question.pop('explanation', None)

    return jsonify({'code': 0, 'data': question})


# ============== AI接口 ==============
@app.route('/api/ai/generate', methods=['POST'])
def api_ai_generate():
    """AI生成题目"""
    data = request.get_json()

    subject = data.get('subject', '')
    knowledge_point = data.get('knowledge_point', '')
    count = int(data.get('count', 5))
    difficulty = data.get('difficulty', 'medium')
    q_type = data.get('type', '选择题')

    if not subject or not knowledge_point:
        return jsonify({'code': 400, 'msg': '缺少必要参数'})

    questions = generate_questions(subject, knowledge_point, count, difficulty, q_type)

    # 保存到数据库
    saved_ids = []
    for q in questions:
        q_id = add_question(
            subject=q['subject'],
            content=q['content'],
            q_type=q['type'],
            answer=q['answer'],
            options=q.get('options'),
            explanation=q.get('explanation'),
            knowledge_point=q['knowledge_point'],
            difficulty=q['difficulty'],
            source='ai'
        )
        saved_ids.append(q_id)

    return jsonify({
        'code': 0,
        'msg': f'生成{len(questions)}道题目',
        'data': {
            'count': len(questions),
            'saved_ids': saved_ids
        }
    })


@app.route('/api/ai/explain', methods=['POST'])
def api_ai_explain():
    """AI题目解析"""
    data = request.get_json()

    question_content = data.get('question_content', '')
    correct_answer = data.get('correct_answer', '')
    user_answer = data.get('user_answer', '')
    options = data.get('options')

    if not question_content or not correct_answer:
        return jsonify({'code': 400, 'msg': '缺少必要参数'})

    explanation = explain_question(question_content, correct_answer, user_answer, options)

    return jsonify({'code': 0, 'data': {'explanation': explanation}})


# ============== 答题接口 ==============
@app.route('/api/answers', methods=['POST'])
def api_submit_answer():
    """提交答题记录"""
    data = request.get_json()

    openid = data.get('openid', 'test_user')  # 测试用户
    question_id = data.get('question_id')
    user_answer = data.get('user_answer', '')
    is_correct = data.get('is_correct', False)

    if not question_id:
        return jsonify({'code': 400, 'msg': '缺少question_id'})

    record_id = add_answer_record(openid, question_id, user_answer, is_correct)

    return jsonify({
        'code': 0,
        'msg': '答题记录已保存',
        'data': {'record_id': record_id, 'is_correct': is_correct}
    })


# ============== 错题接口 ==============
@app.route('/api/wrong', methods=['GET'])
def api_get_wrong():
    """获取错题列表"""
    openid = request.args.get('openid', 'test_user')
    wrong_list = get_wrong_questions(openid)

    # 不返回答案
    for q in wrong_list:
        q.pop('answer', None)

    return jsonify({'code': 0, 'data': wrong_list})


@app.route('/api/wrong/<int:question_id>/master', methods=['POST'])
def api_mark_master(question_id):
    """标记已掌握"""
    data = request.get_json()
    openid = data.get('openid', 'test_user')

    mark_mastered(openid, question_id)

    return jsonify({'code': 0, 'msg': '已标记为掌握'})


# ============== 统计接口 ==============
@app.route('/api/stats', methods=['GET'])
def api_get_stats():
    """获取学习统计"""
    openid = request.args.get('openid', 'test_user')
    stats = get_stats(openid)
    return jsonify({'code': 0, 'data': stats})


# ============== 用户接口 ==============
@app.route('/api/user', methods=['GET'])
def api_get_user():
    """获取用户信息"""
    openid = request.args.get('openid', 'test_user')
    user = get_or_create_user(openid)
    return jsonify({'code': 0, 'data': user})


# ============== 管理接口 ==============
@app.route('/api/admin/question', methods=['POST'])
def api_add_question():
    """添加题目（手动录入）"""
    data = request.get_json()

    question_id = add_question(
        subject=data.get('subject', ''),
        content=data.get('content', ''),
        q_type=data.get('type', '选择题'),
        answer=data.get('answer', ''),
        options=data.get('options'),
        explanation=data.get('explanation'),
        chapter=data.get('chapter'),
        knowledge_point=data.get('knowledge_point'),
        difficulty=data.get('difficulty', 'medium'),
        source='manual'
    )

    return jsonify({'code': 0, 'msg': '题目添加成功', 'data': {'id': question_id}})


if __name__ == '__main__':
    print('=' * 50)
    print('智学题库系统启动中...')
    print('API地址: http://localhost:5001')
    print('=' * 50)
    app.run(host='0.0.0.0', port=5001, debug=True)
