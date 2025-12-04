#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#####################################作者:丁真(化名)######################################################################

import sqlite3
from datetime import datetime

DB_PATH = "money_system.db"  # 数据库文件，会自动在当前目录生成


# ===================== 一、数据库相关函数 =====================

def get_connection():
    """获取数据库连接"""
    return sqlite3.connect(DB_PATH)


def init_db():
    """初始化数据库：创建 users 和 transactions 表"""
    conn = get_connection()
    cur = conn.cursor()

    # 用户表：以用户名为键，每个用户有自己的密码和余额
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        balance REAL NOT NULL DEFAULT 0
    )
    """)

    # 交易日志表：每条记录都挂在一个 user_id 上
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        type TEXT NOT NULL,           -- '存入' / '取出'
        amount REAL NOT NULL,         -- 本次移动金额（正数）
        balance_after REAL NOT NULL,  -- 本次操作后的剩余存款
        created_at TEXT NOT NULL,     -- 时间戳
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()


def user_exists(username: str) -> bool:
    """检查用户名是否已存在"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row is not None


def create_user(username: str, password: str, initial_balance: float = 1000.0) -> int:
    """创建新用户，返回 user_id"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, password, balance) VALUES (?, ?, ?)",
        (username, password, initial_balance)
    )
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id


def authenticate_user(username: str, password: str):
    """
    用户名 + 密码 登录校验
    登录成功返回一个 dict：{"id": ..., "username": ..., "balance": ...}
    登录失败返回 None
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username, balance FROM users WHERE username = ? AND password = ?",
        (username, password)
    )
    row = cur.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "username": row[1], "balance": row[2]}
    return None


def get_balance(user_id: int) -> float:
    """从数据库查询当前用户余额"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return float(row[0])
    return 0.0


def set_balance(user_id: int, new_balance: float):
    """更新数据库中的余额"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, user_id))
    conn.commit()
    conn.close()


def add_transaction(user_id: int, tx_type: str, amount: float, balance_after: float):
    """插入一条交易记录到日志表"""
    conn = get_connection()
    cur = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute(
        """
        INSERT INTO transactions (user_id, type, amount, balance_after, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, tx_type, amount, balance_after, created_at)
    )
    conn.commit()
    conn.close()


def get_transactions(user_id: int):
    """查询某个用户的全部交易记录（按时间顺序）"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT type, amount, balance_after, created_at
        FROM transactions
        WHERE user_id = ?
        ORDER BY id
        """,
        (user_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows


# ===================== 二、原代码里的菜单 UI =====================

def show():
    print("=======菜单=======")
    print("请输入您要执行的功能:")
    print("=================")
    print("1、查询余额")
    print("2、存钱操作")
    print("3、取钱操作")
    print("4、查看日志")
    print("5、退出程序")
    print("=================")


# ===================== 三、核心业务：登录后的操作 =====================

def load(user: dict):
    """
    登录成功后进入此函数
    user 是一个 dict，包含：
    - user["id"]
    - user["username"]
    """
    user_id = user["id"]
    username = user["username"]

    while True:
        show()

        choice_input = input()

        # 字符串不是数字 → 无效输入
        if not choice_input.isdigit():
            print("无效输入，请输入 1-5")
            continue

        choice = int(choice_input)

        # 数字不在 1-5 范围内 → 无效输入
        if choice not in (1, 2, 3, 4, 5):
            print("无效输入，请输入 1-5")
            continue

        if choice == 1:
            # 查询余额：直接从数据库查
            balance = get_balance(user_id)
            print(f'用户 {username}，您现在的余额为: {balance} ¥')

        elif choice == 2:
            # 存钱操作
            try:
                save_input = float(input("请输入存入金额："))
            except ValueError:
                print("金额必须是数字")
                continue

            if save_input <= 0:
                print("金额必须大于 0")
                continue

            amount = save_input
            old_balance = get_balance(user_id)
            new_balance = old_balance + amount

            # 1. 更新用户余额
            set_balance(user_id, new_balance)
            # 2. 写一条日志
            add_transaction(user_id, "存入", amount, new_balance)

            print(f"成功存入 {amount} 元！当前余额：{new_balance} 元。")

        elif choice == 3:
            # 取钱操作
            try:
                take_input = float(input("请输入取出金额："))
            except ValueError:
                print("金额必须是数字")
                continue

            if take_input <= 0:
                print("金额必须大于 0")
                continue

            amount = take_input
            old_balance = get_balance(user_id)

            if amount > old_balance:
                print(f"余额不足！当前余额：{old_balance} 元。")
                continue

            new_balance = old_balance - amount

            # 1. 更新用户余额
            set_balance(user_id, new_balance)
            # 2. 写一条日志
            add_transaction(user_id, "取出", amount, new_balance)

            print(f"成功取出 {amount} 元！当前余额：{new_balance} 元。")

        elif choice == 4:
            # 查看日志：只看当前登录用户的
            records = get_transactions(user_id)
            if not records:
                print("目前暂无记录")
            else:
                print(f"==== 用户 {username} 的交易日志 ====")
                for tx_type, amount, balance_after, created_at in records:
                    print(
                        f"{created_at} | 类型:{tx_type}, 移动金额:{amount}, 剩余存款:{balance_after}"
                    )

        elif choice == 5:
            print("正在退出中......")
            exit()


# ===================== 四、注册 & 登录（改造点最多的部分） =====================

def signin():
    """注册：以用户名为键，创建独立账户、密码、初始余额和日志空间"""
    username = input("请输入您要注册的用户名:\n").strip()
    if not username:
        print("用户名不能为空！")
        return

    if user_exists(username):
        print("该用户名已存在，请换一个，或者直接去登录。")
        return

    pwd_input1 = input("请输入您要注册的密码:\n")
    pwd_input2 = input("请确认您要注册的密码:\n")

    if pwd_input1 != pwd_input2:
        print("前后密码不一致！")
        return

    # 创建用户：初始余额可以沿用你原来写死的 1000 元
    user_id = create_user(username, pwd_input1, initial_balance=1000.0)
    print(f"注册成功！用户名：{username}，初始余额：1000 元。（user_id = {user_id}）")


def login():
    """登录：用户名 + 密码，多用户隔离"""
    username = input("请输入您的用户名:\n").strip()
    if not username:
        print("用户名不能为空！")
        return

    if not user_exists(username):
        print("用户不存在，请先注册。")
        return

    # 最多 3 次密码尝试
    for _ in range(3):
        input_pwd = input("请输入您的密码:\n")
        user = authenticate_user(username, input_pwd)
        if user:
            print("登录成功！")
            # 进入当前用户的会话
            load(user)
            return
        else:
            print("密码错误！请重试。")
            continue

    print("登录失败，密码错误次数过多，请稍后再试！")
    exit()


def menu():
    """顶层菜单：登录 / 注册"""
    while True:
        print("1、登录")
        print("2、注册")
        pick_input = input("输入你要选择的功能:")

        if pick_input == "1":
            login()
        elif pick_input == "2":
            signin()
        else:
            print("不能输入无效的字符，只能是 1 或 2")
            continue


# ===================== 五、程序入口 =====================

if __name__ == "__main__":
    # 启动程序前，先确保数据库结构存在
    init_db()
    menu()


'''v0.2更新内容:
1、解决了存钱取钱输入字符串报错导致系统崩溃的问题
2、增加了校验环节,增强了程序的稳定性
3、解决了在执行功能时输入字符串报错导致系统崩溃的问题
'''

"""v0.3更新内容:
1、更新了注册系统
2、优化了代码结构
"""

### 现在：以用户名为键，构建了一个用户数据库（users + transactions），
### 每个用户拥有独立的账户、密码和日志，通过登录会话（login -> load）控制访问权限。
