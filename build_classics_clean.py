import json
import os

# 1. 确保 site/src/data/classics.json 纯正规矩
classics_data = [
  {
    "id": "shennong-bencaojing",
    "title_cn": "《神农本草经》",
    "title_en": "Shennong's Classic of Materia Medica (Shennong Bencao Jing)",
    "dynasty_cn": "东汉 (公元200年前后)",
    "dynasty_en": "Eastern Han Dynasty (c. 200 AD)",
    "author_cn": "托名神农，秦汉医家搜集整理",
    "author_en": "Attributed to Shennong; Compiled by Qin-Han Physicians",
    "desc_cn": "中国现存最早的药物学专著，奠定了中药学理论基石。全书收载药物365种，首次创立了根据药物功效与毒性划分的“上、中、下三品”分类法，系统阐述了“君臣佐使”组方原则与“四气五味”药性理论。",
    "desc_en": "The earliest extant pharmacopoeia in China, establishing the foundation of Chinese pharmacology. It catalogues 365 medicinal substances, introduced the three-tier classification (Superior, Medium, and Inferior grades), and systematized theories of four natures, five flavors, and monarch-minister formula architecture.",
    "herbs_count": "365味",
    "cn_link": "https://ctext.org/shennong-bencao-jing/zh",
    "en_link": "https://en.wikipedia.org/wiki/Shennong_Ben_Cao_Jing"
  },
  {
    "id": "shanghan-za-bing-lun",
    "title_cn": "《伤寒杂病论》(经方用药规制)",
    "title_en": "Treatise on Cold Damage and Miscellaneous Diseases (Shanghan Zabing Lun)",
    "dynasty_cn": "东汉 (公元200—210年)",
    "dynasty_en": "Eastern Han Dynasty (200–210 AD)",
    "author_cn": "张仲景",
    "author_en": "Zhang Zhongjing (Zhang Ji)",
    "desc_cn": "中医方药学鼻祖巨著，确立了“理法方药”辨证论治体系。全书精选214味地道中药，严谨规定了单味药炮制、先煎后下、煎药用水与服用频次等临床规制，被尊为“众方之祖”，其用药法度是后世历代本草临床实战的标准准绳。",
    "desc_en": "The seminal foundation of Chinese clinical pharmacology and formula architecture. Utilizing 214 classical herbs across 269 formulas, it established rigorous clinical rules for herb preparation, boiling durations, and dosage intervals, regarded as the prime ancestor of all clinical prescriptions.",
    "herbs_count": "214味核心经药",
    "cn_link": "https://ctext.org/shang-han-lun/zh",
    "en_link": "https://en.wikipedia.org/wiki/Shanghan_Lun"
  },
  {
    "id": "bencao-jing-jizhu",
    "title_cn": "《本草经集注》",
    "title_en": "Collected Commentaries on the Materia Medica (Bencao Jing Jizhu)",
    "dynasty_cn": "南北朝 · 梁 (公元500年)",
    "dynasty_en": "Southern and Northern Dynasties (Liang, c. 500 AD)",
    "author_cn": "陶弘景",
    "author_en": "Tao Hongjing",
    "desc_cn": "首创按药物自然属性（玉石、草木、虫兽、果菜、米食）分类的划时代本草专著。在《神农本草经》基础上增补魏晋名医名药365种，总计达730种，首创朱墨分书以辨别古经与后世注记，确立了古代药学注释体例。",
    "desc_en": "A milestone pharmacopoeia that pioneered classification by natural properties (minerals, herbs, animals, fruits, grains). Adding 365 Wei-Jin medicines to expand the total to 730, Tao Hongjing invented red/black ink differentiation to distinguish original scriptures from commentaries.",
    "herbs_count": "730味",
    "cn_link": "https://ctext.org/wiki.pl?if=gb&res=662057",
    "en_link": "https://en.wikipedia.org/wiki/Tao_Hongjing"
  },
  {
    "id": "xinxiu-bencao",
    "title_cn": "《新修本草》(唐本草)",
    "title_en": "Newly Revised Materia Medica (Xinxiu Bencao / Tang Bencao)",
    "dynasty_cn": "唐代 (公元659年)",
    "dynasty_en": "Tang Dynasty (659 AD)",
    "author_cn": "苏敬 等23人奉敕编修",
    "author_en": "Su Jing et al. (Commissioned by Imperial Court)",
    "desc_cn": "世界上第一部由中央政府颁布实施的国家药典，比欧洲《佛罗伦萨药典》早800余年。全书收药850种，开创了本草学附录药图的先例（本草、药图、图经三位一体），广泛吸收了丝绸之路西域传入的药材。",
    "desc_en": "The world's first officially promulgated national pharmacopoeia, preceding the European Pharmacopoeia of Florence by over 800 years. Compiling 850 medicinal substances, it originated the tripartite integration of classical text, illustrated atlas, and morphological notes.",
    "herbs_count": "850味",
    "cn_link": "https://ctext.org/wiki.pl?if=gb&res=222830",
    "en_link": "https://en.wikipedia.org/wiki/Tang_Bencao"
  },
  {
    "id": "qianjin-yaofang-shizhi",
    "title_cn": "《备急千金要方》(食治与本草卷)",
    "title_en": "Essential Prescriptions Worth a Thousand Pieces of Gold (Qianjin Yaofang)",
    "dynasty_cn": "唐代 (公元652年)",
    "dynasty_en": "Tang Dynasty (652 AD)",
    "author_cn": "孙思邈",
    "author_en": "Sun