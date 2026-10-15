import os
import re
import json

# 1. 检查 herbs.json 中的 id 是否齐全有效
json_path = os.path.join("site", "src", "data", "herbs.json")
if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        herbs = json.load(f)
    print(f"1. herbs.json 收录总数: {len(herbs)}")
    empty_ids = [h.get("cn") for h in herbs if not h.get("id")]
    if empty_ids:
        print(f"   [异常] 存在缺少 id 的药材: {empty_ids}")
    else:
        print(f"   [正常] 所有药材均有有效 id，前 3 个: {[h.get('id') for h in herbs[:3]]}")
else:
    print(f"   [错误] 未找到文件: {json_path}")

# 2. 检查 site/dist/index.html 实际生成的 href 链接
dist_index = os.path.join("site", "dist", "index.html")
if os.path.exists(dist_index):
    with open(dist_index, "r", encoding="utf-8") as f:
        html = f.read()
    # 提取所有 /herbs/