import os
import json
import requests

HEADERS = {
    'User-Agent': 'TCMHerbAtlas/3.0 (Educational Academic Research; contact@tcm-global.org)'
}

# 首页后4种缺失药材与首页大图对应的维基权威词条
TARGET_WIKI_ENTRIES = {
    "hero_index": "Astragalus_propinquus",  # 首页右上角大图
    "lycium-barbarum": "Lycium_barbarum",
    "glycyrrhiza": "Glycyrrhiza_glabra",
    "ginkgo-biloba": "Ginkgo_biloba",
    "rhodiola-rosea": "Rhodiola_rosea"
}

def get_official_wiki_image(title):
    """通过官方 REST API 获取维基媒体官方签名与认可的合法图片 URL，避免 400 拦截"""
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        if r.status_code == 200:
            data = r.json()
            # 优先取 thumbnail，若无取 originalimage
            img_obj = data.get("thumbnail") or data.get("originalimage")
            if img_obj and "source" in img_obj:
                return img_obj["source"]
    except Exception as e:
        print(f"    API 解析异常 [{title}]: {e}")
    return None

def download_image(url, save_path):
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code == 200 and len(r.content) > 3000:
            with open(save_path, 'wb') as f:
                f.write(r.content)
            return True
    except Exception as e:
        print(f"    下载异常: {e}")
    return False

# 1. 落地首页右上角大图
print("=== 1. 正在获取首页右上角大图 (官方 API 直连) ===")
hero_target = os.path.join("site", "public", "images", "hero_index.jpg")
os.makedirs(os.path.dirname(hero_target), exist_ok=True)
hero_url = get_official_wiki_image(TARGET_WIKI_ENTRIES["hero_index"])
if hero_url:
    print(f"  解析到合法 URL: {hero_url}")
    if download_image(hero_url, hero_target):
        print("  ✓ 首页大图保存成功: site/public/images/hero_index.jpg")
else:
    print("  ! 未获取到首页大图 URL")

# 2. 补齐后 4 种中药
print("\n=== 2. 正在补齐 4 种药材实拍图 ===")
json_path = os.path.join("site", "src", "data", "herbs.json")
with open(json_path, "r", encoding="utf-8") as f:
    herbs = json.load(f)

for herb in herbs:
    hid = herb["id"]
    if hid in TARGET_WIKI_ENTRIES and hid != "hero_index":
        wiki_title = TARGET_WIKI_ENTRIES[hid]
        print(f"\n正在抓取【{herb['cn']}】({wiki_title})...")
        
        target_dir = os.path.join("site", "public", "images", "herbs", hid)
        os.makedirs(target_dir, exist_ok=True)
        hero_file = os.path.join(target_dir, "hero.jpg")
        plant_file = os.path.join(target_dir, "plant.jpg")
        
        img_url = get_official_wiki_image(wiki_title)
        if img_url:
            print(f"  解析到合法 URL: {img_url}")
            ok = download_image(img_url, hero_file)
            if ok:
                with open(plant_file, 'wb') as pf, open(hero_file, 'rb') as hf:
                    pf.write(hf.read())
                herb["hero_img"] = f"/images/herbs/{hid}/hero.jpg"
                herb["plant_img"] = f"/images/herbs/{hid}/plant.jpg"
                print(f"  ✓ 成功落地本地文件: /images/herbs/{hid}/hero.jpg")
            else:
                print("  ! 图片下载失败")
        else:
            print("  ! 未能解析到维基条目图片")

    # 别名字段空值保护，防止 Astro 详情页报错
    if "alias" not in herb or herb["alias"] is None:
        herb["alias"] = []

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(herbs, f, ensure_ascii=False, indent=2)

print("\n=== 全部图片下载与数据修复完成！===")