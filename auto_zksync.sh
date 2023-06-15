#!/bin/bash
#45000 12.5h
interval_seconds=60
array=( $(seq 0 2) )
array=(1 0)
index=0
count=0

while [ $count -lt ${#array[@]} ]; do
    cd /home/cc/sci_projects/zksync2/zksync
    source /home/cc/sci_projects/.venv/bin/activate
    nohup python main.py "${array[$index]}" >>/home/cc/sci_projects/zksync2/zksync/logs/output.log &

    sleep $interval_seconds

    # 更新索引和计数器
    index=$(( (index + 1) % ${#array[@]} ))
    count=$((count + 1))
done

