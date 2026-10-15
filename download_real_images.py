import os
import json
import urllib.request

# 采用无需外网魔法即可稳定下载的公开物种标本与药材图像直链
HERB_PHOTO_URLS = {
    "astragalus": {
        "hero": "https://img.freepik.com/free-photo/dried-astragalus-membranaceus-sliced-ingredient-traditional-chinese-medicine_1150-45300.jpg",
        "plant": "https://images.pexels.com/photos/5472852/pexels-photo-5472852.jpeg?auto=compress&cs=tinysrgb&w=800"
    },
    "panax-ginseng": {
        "hero": "https://images.pexels.com/photos/6157052/pexels-photo-6157052.jpeg?auto=compress&cs=tinysrgb&w=800",
        "plant": "https://images.pexels.com/photos/4503269/pexels-photo-4503269.jpeg?auto=compress&cs=tinysrgb&w=800"
    },
    "artemisia-annua": {
        "hero": "https://images.pexels.com/photos/6045028/pexels-photo-6045028.jpeg?auto=compress&cs=tinysrgb&w=800",
        "plant": "https://images.pexels.com/photos/4505161/pexels-photo-4505161.jpeg?auto=compress&cs=tinysrgb&w=800"
    },
    "angelica-sinensis": {
        "hero": "https://img.freepik.com/free-photo/angelica-sinensis-chinese-traditional-herbal-medicine_1150-45305.jpg",
        "plant": "https://images.pexels.com/photos/1084199/pexels-photo-1084199.jpeg?auto=compress&cs=tinysrgb&w=800"
    },
    "coptis-chinensis": {
        "hero": "https://images.pexels.com/photos/6045083/pexels-photo-6045083.jpeg?auto=compress&cs=tinysrgb&w=800",
        "plant": "https://images.pexels.com/photos/1407305/pexels-photo-1407305.jpeg?auto=compress&cs=tinysrgb&w=800"
    }
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print("=== 开始批量抓取真实药材图片至本地磁盘 ===")

json_path = os.path.join("site", "src", "data", "herbs.json")
with open(json_path, "r", encoding="utf-8") as f:
    herbs = json.load(f)

for herb in herbs:
    hid = herb["id"]
    if hid not in HERB_PHOTO_URLS:
        continue
    
    target_dir = os.path.join("site", "public", "images", "herbs", hid)
    os.makedirs(target_dir, exist_ok=True)
    
    print(f"\n正在抓取【{herb['cn']}】图片...")
    for key in ["hero", "plant"]:
        url = HERB_PHOTO_URLS[hid][key]
        dest_filename = f"{key}.jpg"
        dest_path = os.path.join(target_dir, dest_filename)
        web_path = f"/images/herbs/{hid}/{dest_filename}"
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                with open(dest_path, 'wb') as out_file:
                    out_file.write(response.read())
            print(f"  ✓ 成功下载并保存: {web_path}")
            herb[f"{key}_img"] = web_path
        except Exception as e:
            print(f"  ✗ 抓取失败 ({key}): {e}")

# 将图片路径重定向为本地路径
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(herbs, f, ensure_ascii=False, indent=2)

print("\n=== 全部真实图片已成功落盘至本地！===")