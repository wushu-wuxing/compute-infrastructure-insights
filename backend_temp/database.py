# -*- coding: utf-8 -*-
"""数据库操作模块"""

import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any
import json

DATABASE_PATH = 'question_bank.db'


def get_conn():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库"""
    conn = get_conn()
    cursor = conn.cursor()

    # 题目表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            chapter TEXT,
            knowledge_point TEXT,
            type TEXT NOT NULL,
            difficulty TEXT DEFAULT 'medium',
            content TEXT NOT NULL,
            options TEXT,
            answer TEXT NOT NULL,
            explanation TEXT,
            source TEXT DEFAULT 'ai',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 用户答题记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS answer_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            openid TEXT NOT NULL,
            question_id INTEGER NOT NULL,
            user_answer TEXT,
            is_correct INTEGER,
            answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
    ''')

    # 错题表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wrong_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            openid TEXT NOT NULL,
            question_id INTEGER NOT NULL,
            wrong_count INTEGER DEFAULT 1,
            last_reviewed TIMESTAMP,
            mastered INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (question_id) REFERENCES questions(id),
            UNIQUE(openid, question_id)
        )
    ''')

    # 用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            openid TEXT UNIQUE NOT NULL,
            nickname TEXT,
            avatar TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()


def get_subjects() -> List[Dict[str, Any]]:
    """获取所有科目及统计"""
    conn = get_conn()
    cursor = conn.cursor()

    subjects = ['语文', '数学', '英语', '政治', '历史', '地理']
    result = []

    for subject in subjects:
        cursor.execute('SELECT COUNT(*) as total FROM questions WHERE subject = ?', (subject,))
        total = cursor.fetchone()['total']

        cursor.execute('''
            SELECT COUNT(DISTINCT ar.question_id) as practiced
            FROM answer_records ar
            JOIN questions q ON ar.question_id = q.id
            WHERE q.subject = ?
        ''', (subject,))
        practiced = cursor.fetchone()['practiced']

        cursor.execute('''
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN ar.is_correct = 1 THEN 1 ELSE 0 END) as correct
            FROM answer_records ar
            JOIN questions q ON ar.question_id = q.id
            WHERE q.subject = ?
        ''', (subject,))
        stats = cursor.fetchone()
        accuracy = round(stats['correct'] / stats['total'] * 100, 1) if stats['total'] > 0 else 0

        result.append({
            'name': subject,
            'total': total,
            'practiced': practiced,
            'accuracy': accuracy
        })

    conn.close()
    return result


def get_questions(subject: str, chapter: Optional[str] = None,
                   knowledge_point: Optional[str] = None,
                   limit: int = 10) -> List[Dict[str, Any]]:
    """获取题目列表"""
    conn = get_conn()
    cursor = conn.cursor()

    query = 'SELECT * FROM questions WHERE subject = ?'
    params = [subject]

    if chapter:
        query += ' AND chapter = ?'
        params.append(chapter)

    if knowledge_point:
        query += ' AND knowledge_point = ?'
        params.append(knowledge_point)

    query += ' ORDER BY RANDOM() LIMIT ?'
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        item = dict(row)
        if item.get('options'):
            item['options'] = json.loads(item['options'])
        result.append(item)

    return result


def get_question_by_id(question_id: int) -> Optional[Dict[str, Any]]:
    """获取单题详情"""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions WHERE id = ?', (question_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        item = dict(row)
        if item.get('options'):
            item['options'] = json.loads(item['options'])
        return item
    return None


def add_question(subject: str, content: str, q_type: str, answer: str,
                 options: Optional[Dict] = None, explanation: Optional[str] = None,
                 chapter: Optional[str] = None, knowledge_point: Optional[str] = None,
                 difficulty: str = 'medium', source: str = 'ai') -> int:
    """添加题目"""
    conn = get_conn()
    cursor = conn.cursor()

    options_json = json.dumps(options, ensure_ascii=False) if options else None

    cursor.execute('''
        INSERT INTO questions (subject, chapter, knowledge_point, type, difficulty,
                              content, options, answer, explanation, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (subject, chapter, knowledge_point, q_type, difficulty,
          content, options_json, answer, explanation, source))

    question_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return question_id


def add_answer_record(openid: str, question_id: int, user_answer: str,
                      is_correct: bool) -> int:
    """添加答题记录"""
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO answer_records (openid, question_id, user_answer, is_correct)
        VALUES (?, ?, ?, ?)
    ''', (openid, question_id, user_answer, 1 if is_correct else 0))

    record_id = cursor.lastrowid

    # 如果答错，加入错题本
    if not is_correct:
        cursor.execute('''
            INSERT OR REPLACE INTO wrong_questions (openid, question_id, wrong_count, last_reviewed)
            VALUES (?, ?, COALESCE((SELECT wrong_count + 1 FROM wrong_questions
                                   WHERE openid = ? AND question_id = ?), 1), CURRENT_TIMESTAMP)
        ''', (openid, question_id, openid, question_id))

    conn.commit()
    conn.close()
    return record_id


def get_wrong_questions(openid: str) -> List[Dict[str, Any]]:
    """获取用户错题列表"""
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT wq.*, q.subject, q.type, q.content, q.options, q.answer, q.explanation
        FROM wrong_questions wq
        JOIN questions q ON wq.question_id = q.id
        WHERE wq.openid = ? AND wq.mastered = 0
        ORDER BY wq.last_reviewed DESC
    ''', (openid,))

    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        item = dict(row)
        if item.get('options'):
            item['options'] = json.loads(item['options'])
        result.append(item)

    return result


def mark_mastered(openid: str, question_id: int):
    """标记已掌握"""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE wrong_questions SET mastered = 1 WHERE openid = ? AND question_id = ?
    ''', (openid, question_id))
    conn.commit()
    conn.close()


def get_stats(openid: str) -> Dict[str, Any]:
    """获取学习统计"""
    conn = get_conn()
    cursor = conn.cursor()

    # 总答题数
    cursor.execute('SELECT COUNT(*) as total FROM answer_records WHERE openid = ?', (openid,))
    total = cursor.fetchone()['total']

    # 正确数
    cursor.execute('SELECT COUNT(*) as correct FROM answer_records WHERE openid = ? AND is_correct = 1', (openid,))
    correct = cursor.fetchone()['correct']

    # 各科统计
    cursor.execute('''
        SELECT q.subject,
               COUNT(*) as total,
               SUM(CASE WHEN ar.is_correct = 1 THEN 1 ELSE 0 END) as correct
        FROM answer_records ar
        JOIN questions q ON ar.question_id = q.id
        WHERE ar.openid = ?
        GROUP BY q.subject
    ''', (openid,))

    subjects = []
    for row in cursor.fetchall():
        t = row['total']
        c = row['correct']
        subjects.append({
            'name': row['subject'],
            'total': t,
            'correct': c,
            'accuracy': round(c / t * 100, 1) if t > 0 else 0
        })

    # 错题数
    cursor.execute('SELECT COUNT(*) FROM wrong_questions WHERE openid = ? AND mastered = 0', (openid,))
    wrong_count = cursor.fetchone()[0]

    conn.close()

    return {
        'total': total,
        'correct': correct,
        'accuracy': round(correct / total * 100, 1) if total > 0 else 0,
        'wrong_count': wrong_count,
        'subjects': subjects
    }


def get_or_create_user(openid: str, nickname: str = None, avatar: str = None) -> Dict[str, Any]:
    """获取或创建用户"""
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE openid = ?', (openid,))
    user = cursor.fetchone()

    if not user:
        cursor.execute('''
            INSERT INTO users (openid, nickname, avatar) VALUES (?, ?, ?)
        ''', (openid, nickname, avatar))
        conn.commit()
        cursor.execute('SELECT * FROM users WHERE openid = ?', (openid,))
        user = cursor.fetchone()

    conn.close()
    return dict(user)


if __name__ == '__main__':
    init_db()
    print('数据库初始化完成')
