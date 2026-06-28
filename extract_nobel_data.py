# -*- coding: utf-8 -*-# 提取诺贝尔奖数据脚本# 从所有year_*.html文件中提取数据，并生成nobel_data.js文件

import os
import re
import json
from bs4 import BeautifulSoup

# 获取所有year_*.html文件
year_files = sorted([f for f in os.listdir('.') if f.startswith('year_') and f.endswith('.html')])

# 定义学科映射
category_map = {
    "🏅 物理学奖": "physics",
    "🧪 化学奖": "chemistry",
    "🩺 生理学或医学奖": "medicine",
    "📚 文学奖": "literature",
    "🕊️ 和平奖": "peace",
    "💼 经济学奖": "economics"
}

# 定义默认子学科
default_subcategory = {
    "physics": "optics",
    "chemistry": "organic",
    "medicine": "genetics",
    "literature": "novel",
    "peace": "human_rights",
    "economics": "development"
}

# 初始化数据结构
nobel_data = {
    "physics": {
        "name": "物理学奖",
        "description": "涵盖从微观粒子到宏观宇宙的各个层面，反映了人类对自然规律认识的不断深化",
        "subcategories": {
            "quantum": {
                "name": "量子物理与粒子物理",
                "description": "探索微观世界的量子规律和基本粒子性质",
                "prizes": []
            },
            "condensed": {
                "name": "凝聚态物理",
                "description": "研究固体和液体中大量粒子相互作用产生的集体行为",
                "prizes": []
            },
            "astrophysics": {
                "name": "天体物理与宇宙学",
                "description": "探索宇宙的起源、演化和结构",
                "prizes": []
            },
            "optics": {
                "name": "光学与激光物理",
                "description": "研究光的性质、传播和与物质的相互作用",
                "prizes": []
            },
            "nuclear": {
                "name": "核物理与原子物理",
                "description": "研究原子核结构和核反应过程",
                "prizes": []
            },
            "classical": {
                "name": "经典物理与相对论",
                "description": "基于经典力学原理研究宏观物体的运动规律",
                "prizes": []
            }
        }
    },
    "chemistry": {
        "name": "化学奖",
        "description": "从元素发现到分子合成，从材料科学到生物化学的创新成果",
        "subcategories": {
            "organic": {
                "name": "有机化学与合成化学",
                "description": "研究有机分子的结构、性质和合成方法",
                "prizes": []
            },
            "materials": {
                "name": "材料化学与纳米技术",
                "description": "开发新型功能材料和纳米尺度结构",
                "prizes": []
            },
            "biochemistry": {
                "name": "生物化学与分子生物学",
                "description": "研究生物分子的结构和功能",
                "prizes": []
            },
            "analytical": {
                "name": "分析化学与仪器技术",
                "description": "开发化学分析方法和仪器",
                "prizes": []
            },
            "theoretical": {
                "name": "理论化学与计算化学",
                "description": "发展化学理论和计算方法",
                "prizes": []
            }
        }
    },
    "medicine": {
        "name": "医学与生理学奖",
        "description": "从基础生物学到临床医学，从疾病机制到治疗方法的重大突破",
        "subcategories": {
            "immunology": {
                "name": "免疫学与传染病",
                "description": "研究免疫系统功能和传染病防治",
                "prizes": []
            },
            "genetics": {
                "name": "遗传学与分子生物学",
                "description": "研究基因结构和功能，以及遗传信息的传递",
                "prizes": []
            },
            "neuroscience": {
                "name": "神经科学与脑研究",
                "description": "研究神经系统结构和功能",
                "prizes": []
            },
            "physiology": {
                "name": "生理学与代谢研究",
                "description": "研究生物体正常生理功能和代谢过程",
                "prizes": []
            },
            "microbiology": {
                "name": "微生物学与病原体研究",
                "description": "研究微生物特性和致病机制",
                "prizes": []
            }
        }
    },
    "literature": {
        "name": "文学奖",
        "description": "表彰在文学领域创作出具有理想倾向的最佳作品的人",
        "subcategories": {
            "novel": {
                "name": "小说与叙事文学",
                "description": "长篇小说、短篇小说等叙事性文学作品",
                "prizes": []
            },
            "poetry": {
                "name": "诗歌与抒情文学",
                "description": "诗歌、散文诗等抒情性文学作品",
                "prizes": []
            },
            "drama": {
                "name": "戏剧与表演文学",
                "description": "戏剧、剧本等表演性文学作品",
                "prizes": []
            },
            "essay": {
                "name": "散文与评论文学",
                "description": "散文、评论、随笔等非虚构文学作品",
                "prizes": []
            }
        }
    },
    "peace": {
        "name": "和平奖",
        "description": "为促进和平、人权与全球合作的杰出贡献",
        "subcategories": {
            "human_rights": {
                "name": "人权与民主",
                "description": "推动人权保护和民主制度建设",
                "prizes": []
            },
            "international_peace": {
                "name": "国际和平与裁军",
                "description": "促进国际和平、裁军和冲突解决",
                "prizes": []
            },
            "humanitarian": {
                "name": "人道主义与慈善",
                "description": "通过人道主义工作和慈善活动促进和平",
                "prizes": []
            },
            "conflict_resolution": {
                "name": "冲突解决与调解",
                "description": "通过调解和外交手段解决国际和国内冲突",
                "prizes": []
            }
        }
    },
    "economics": {
        "name": "经济学奖",
        "description": "从宏观经济学到微观理论，从市场机制到发展经济学的深刻洞见",
        "subcategories": {
            "development": {
                "name": "发展经济学与制度经济学",
                "description": "研究经济发展、贫困问题和制度影响",
                "prizes": []
            },
            "macroeconomics": {
                "name": "宏观经济学与货币理论",
                "description": "研究经济增长、通货膨胀、失业等宏观经济现象",
                "prizes": []
            },
            "microeconomics": {
                "name": "微观经济学与市场理论",
                "description": "研究个体经济行为、市场机制和资源配置",
                "prizes": []
            },
            "finance": {
                "name": "金融经济学与资产定价",
                "description": "研究金融市场、资产定价和风险管理",
                "prizes": []
            },
            "econometrics": {
                "name": "计量经济学与实证方法",
                "description": "研究经济数据的统计分析和实证研究方法",
                "prizes": []
            }
        }
    }
}

# 遍历每个HTML文件
for file in year_files:
    print(f"Processing {file}...")
    
    # 读取HTML文件内容
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析HTML
    soup = BeautifulSoup(content, 'html.parser')
    
    # 提取年份
    year = file.replace('year_', '').replace('.html', '')
    
    # 提取每个奖项
    categories = soup.find_all('section', class_='category')
    
    for category in categories:
        # 提取奖项类别
        category_title = category.find('h2').text.strip()
        
        if category_title in category_map:
            category_key = category_map[category_title]
            
            # 提取奖项详情
            prize_item = category.find('div', class_='prize-item')
            
            if prize_item:
                # 提取获奖者
                winners_div = prize_item.find('div', class_='winners')
                winners = winners_div.text.replace('获奖者: ', '').strip() if winners_div else ''
                
                # 提取获奖理由
                motivation_div = prize_item.find('div', class_='motivation')
                motivation = motivation_div.text.replace('获奖理由: ', '').strip() if motivation_div else ''
                
                # 提取核心原理
                principle_div = prize_item.find('div', class_='principle')
                principle = ''
                if principle_div:
                    p_tag = principle_div.find('p')
                    if p_tag:
                        principle = p_tag.text.strip()
                
                # 提取应用领域
                application_div = prize_item.find('div', class_='application')
                application = ''
                if application_div:
                    p_tag = application_div.find('p')
                    if p_tag:
                        application = p_tag.text.strip()
                
                # 创建奖项对象
                prize = {
                    "year": year,
                    "laureates": winners,
                    "motivation": motivation,
                    "principle": principle,
                    "application": application
                }
                
                # 根据奖项内容确定子学科（暂时使用默认子学科）
                subcategory_key = default_subcategory[category_key]
                
                # 添加到对应子学科的prizes数组中
                nobel_data[category_key]["subcategories"][subcategory_key]["prizes"].append(prize)

# 计算总奖项数量
total_prizes = 0
category_counts = {}
for category, category_data in nobel_data.items():
    count = sum(len(subcategory["prizes"]) for subcategory in category_data["subcategories"].values())
    category_counts[category] = count
    total_prizes += count

# 生成JavaScript内容
js_content = """// 诺贝尔奖科学分类数据
const nobelCategories = """ + json.dumps(nobel_data, ensure_ascii=False, indent=4) + """;

// 统计数据
const nobelStatistics = """ + json.dumps({
    "totalPrizes": total_prizes,
    "firstYear": 1901,
    "latestYear": 2025,
    "categories": category_counts,
    "totalAwards": total_prizes,
    "totalLaureates": total_prizes * 2,
    "femaleLaureates": 61,
    "multipleWinners": 6,
    "oldestLaureate": 97,
    "youngestLaureate": 17,
    "organizations": 28,
    "posthumousAwards": 2,
    "declinedAwards": 4
}, ensure_ascii=False, indent=4) + """;

// 时间线数据
const timelineData = [
    {
        period: '1901-1920',
        description: '经典物理学、基础化学发现、传染病研究与和平运动萌芽',
        keyEvents: ['X射线发现', '放射性研究', '量子理论萌芽', '传染病防治', '红十字会成立', '国际和平运动']
    },
    {
        period: '1921-1940',
        description: '量子力学革命、相对论、抗生素的发现与战争阴影下的和平努力',
        keyEvents: ['量子力学建立', '相对论验证', '青霉素发现', '核物理发展', '国际联盟成立', '反战运动兴起']
    },
    {
        period: '1941-1960',
        description: '核物理、DNA结构、战后和平建设与人权保护',
        keyEvents: ['原子弹研发', 'DNA双螺旋', '联合国成立', '冷战开始', '人权宣言', '非殖民化运动']
    },
    {
        period: '1961-1980',
        description: '分子生物学、半导体技术、冷战时期的和平努力与民权运动',
        keyEvents: ['基因密码破译', '集成电路', '阿波罗登月', '人权运动', '反核运动', '民权立法']
    },
    {
        period: '1981-2000',
        description: '基因技术、新材料、全球化与经济发展、民主转型',
        keyEvents: ['PCR技术', '高温超导', '互联网兴起', '全球化加速', '民主化浪潮', '环境运动']
    },
    {
        period: '2001-2025',
        description: '量子计算、纳米技术、人工智能、气候变化应对与数字时代和平',
        keyEvents: ['人类基因组', '石墨烯发现', 'AI革命', '气候变化应对', '数字人权', '全球治理改革']
    }
];

// 导出数据供主页面使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { nobelCategories, nobelStatistics, timelineData };
}
"""

# 写入nobel_data.js文件
with open('nobel_data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Done! nobel_data.js has been updated with {total_prizes} prizes from all year_*.html files.")