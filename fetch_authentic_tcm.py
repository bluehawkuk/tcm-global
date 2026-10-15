import os
import json
import requests

HEADERS = {
    'User-Agent': 'TCMHerbAtlas/3.0 (Educational Academic Research; contact@tcm-global.org)'
}

# 严格绑定学术条目名，后续扩展到100种中药只需在此追加映射
WIKI_SPECIES = {
    "astragalus": "Astragalus_propinquus",
    "panax-ginseng": "Panax_ginseng",
    "coptis-chinensis": "Coptis_chinensis",
    "angelica-sinensis": "Angelica_sinensis",
    "artemisia-annua": "Artemisia_annua"
}

def get_wiki_summary_image(title):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        if r.status_code == 200:
            data = r.json()
            # 获取条目专属权威原图/高清缩略图
            img_info = data.get("originalimage") or data.get("thumbnail")
            if img_info and "source" in img_info:
                return img_info["source"]
    except Exception as e:
        print(f"    Wiki API 异常 [{title}]: {e}")
    return None

def download_img(url, filepath):
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code == 200 and len(r.content) > 3000:
            with open(filepath, 'wb') as f:
                f.write(r.content)
            return True
    except Exception as e:
        print(f"    下载异常: {e}")
    return False

json_path = os.path.join("site", "src", "data", "herbs.json")
if not os.path.exists(json_path):
    print("找不到 herbs.json！")
    exit(1)

with open(json_path, "r", encoding="utf-8") as f:
    herbs = json.load(f)

print("=== 开始通过 Wikipedia 物种学术接口下载真实植物照片 ===")

for herb in herbs:
    hid = herb["id"]
    species_title = WIKI_SPECIES.get(hid)
    if not species_title:
        continue
    
    target_dir = os.path.join("site", "public", "images", "herbs", hid)
    os.makedirs(target_dir, exist_ok=True)
    
    print(f"\n[检索学术条目] {herb['cn']} -> {species_title}")
    img_url = get_wiki_summary_image(species_title)
    
    if img_url:
        print(f"  解析到物种权威原图: {img_url}")
        # 保存为本地物理文件
        hero_local = os.path.join(target_dir, "hero.jpg")
        plant_local = os.path.join(target_dir, "plant.jpg")
        
        ok = download_img(img_url, hero_local)
        if ok:
            # plant 图复用该真实物种图，确保图文高度契合
            with open(plant_local, 'wb') as f:
                with open(hero_local, 'rb') as src:
                    f.write(src.read())
            
            herb["hero_img"] = f"/images/herbs/{hid}/hero.jpg"
            herb["plant_img"] = f"/images/herbs/{hid}/plant.jpg"
            print(f"  ✓ 成功下载并配置本地物种实拍图！")
        else:
            print("  ! 下载超时或中断")
    else:
        print("  ! 未获取到有效条目配图")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(herbs, f, ensure_ascii=False, indent=2)

print("\n=== 全部真实物种图片已落地至 site/public/images/herbs/ ===")