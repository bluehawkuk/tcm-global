import os
import json

# 每味药材对应的维基百科真实植物学原图与药材图
AUTHENTIC_REAL_IMAGES = {
    "astragalus": {
        "hero_img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Astragalus_propinquus_01.JPG/800px-Astragalus_propinquus_01.JPG",
        "plant_img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Astragalus_mongholicus_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-019.jpg/600px-Astragalus_mongholicus_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-019.jpg"
    },
    "panax-ginseng": {
        "hero_img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Panax_ginseng_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-102.jpg/600px-Panax_ginseng_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-102.jpg",
        "plant_img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Panax_ginseng_plant.jpg/800px-Panax_ginseng_plant.jpg"
    },
    "coptis-chinensis": {
        "hero_img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Coptis_chinensis_01.JPG/800px-Coptis_chinensis_01.JPG",
        "plant_img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Coptis_teeta_-_Curtis%27s_Botanical_Magazine_113_%281887%29.jpg/600px-Coptis_teeta_-_Curtis%27s_Botanical_Magazine_113_%281887%29.jpg"
    },
    "angelica-sinensis": {
        "hero_img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Angelica_sinensis_-_Flora_de_Filipinas.jpg/600px-Angelica_sinensis_-_Flora_de_Filipinas.jpg",
        "plant_img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Angelica_sinensis_plant.JPG/800px-Angelica_sinensis_plant.JPG"
    },
    "artemisia-annua": {
        "hero_img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Artemisia_annua_002.JPG/800px-Artemisia_annua_002.JPG",
        "plant_img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Artemisia_annua_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-016.jpg/600px-Artemisia_annua_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-016.jpg"
    }
}

json_path = os.path.join("site", "src", "data", "herbs.json")
if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        herbs = json.load(f)

    for h in herbs:
        hid = h["id"]
        if hid in AUTHENTIC_REAL_IMAGES:
            h["hero_img"] = AUTHENTIC_REAL_IMAGES[hid]["hero_img"]
            h["plant_img"] = AUTHENTIC_REAL_IMAGES[hid]["plant_img"]
            # 饮片切片图字段清除
            h.pop("slice_img", None)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(herbs, f, ensure_ascii=False, indent=2)
    print("✓ 数据已更新为真实植物实拍与古籍标本图源！")