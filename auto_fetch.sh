#!/usr/bin/env bash

# 每隔 5 分钟自动执行一次 git fetch origin
while true; do
    echo "=== Auto fetch at: $(date) ==="
    git fetch origin
    # 可选：显示一下有哪些远程分支更新
    git remote -v
    echo "================================"
    # 休眠 300 秒（5 分钟）
    sleep 300
done



