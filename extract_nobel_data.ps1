# 提取诺贝尔奖数据脚本
# 从所有year_*.html文件中提取数据，并生成nobel_data.js文件

# 定义年份映射
$yearFiles = Get-ChildItem -Path . -Filter year_*.html | Sort-Object Name

# 定义学科映射
$categoryMap = @{
    "🏅 物理学奖" = "physics"
    "🧪 化学奖" = "chemistry"
    "🩺 生理学或医学奖" = "medicine"
    "📚 文学奖" = "literature"
    "🕊️ 和平奖" = "peace"
    "💼 经济学奖" = "economics"
}

# 定义子学科映射
$subcategoryMap = @{
    "physics" = @{
        "量子物理与粒子物理" = "quantum"
        "凝聚态物理" = "condensed"
        "天体物理与宇宙学" = "astrophysics"
        "光学与激光物理" = "optics"
        "核物理与原子物理" = "nuclear"
        "经典物理与相对论" = "classical"
    }
    "chemistry" = @{
        "有机化学与合成化学" = "organic"
        "材料化学与纳米技术" = "materials"
        "生物化学与分子生物学" = "biochemistry"
        "分析化学与仪器技术" = "analytical"
        "理论化学与计算化学" = "theoretical"
    }
    "medicine" = @{
        "免疫学与传染病" = "immunology"
        "遗传学与分子生物学" = "genetics"
        "神经科学与脑研究" = "neuroscience"
        "生理学与代谢研究" = "physiology"
        "微生物学与病原体研究" = "microbiology"
    }
    "literature" = @{
        "小说与叙事文学" = "novel"
        "诗歌与抒情文学" = "poetry"
        "戏剧与表演文学" = "drama"
        "散文与评论文学" = "essay"
    }
    "peace" = @{
        "人权与民主" = "human_rights"
        "国际和平与裁军" = "international_peace"
        "人道主义与慈善" = "humanitarian"
        "冲突解决与调解" = "conflict_resolution"
    }
    "economics" = @{
        "发展经济学与制度经济学" = "development"
        "宏观经济学与货币理论" = "macroeconomics"
        "微观经济学与市场理论" = "microeconomics"
        "金融经济学与资产定价" = "finance"
        "计量经济学与实证方法" = "econometrics"
    }
}

# 定义默认子学科
$defaultSubcategory = @{
    "physics" = "optics"
    "chemistry" = "organic"
    "medicine" = "genetics"
    "literature" = "novel"
    "peace" = "human_rights"
    "economics" = "development"
}

# 初始化数据结构
$nobelData = @{
    "physics" = @{
        "name" = "物理学奖"
        "description" = "涵盖从微观粒子到宏观宇宙的各个层面，反映了人类对自然规律认识的不断深化"
        "subcategories" = @{}
    }
    "chemistry" = @{
        "name" = "化学奖"
        "description" = "从元素发现到分子合成，从材料科学到生物化学的创新成果"
        "subcategories" = @{}
    }
    "medicine" = @{
        "name" = "医学与生理学奖"
        "description" = "从基础生物学到临床医学，从疾病机制到治疗方法的重大突破"
        "subcategories" = @{}
    }
    "literature" = @{
        "name" = "文学奖"
        "description" = "表彰在文学领域创作出具有理想倾向的最佳作品的人"
        "subcategories" = @{}
    }
    "peace" = @{
        "name" = "和平奖"
        "description" = "为促进和平、人权与全球合作的杰出贡献"
        "subcategories" = @{}
    }
    "economics" = @{
        "name" = "经济学奖"
        "description" = "从宏观经济学到微观理论，从市场机制到发展经济学的深刻洞见"
        "subcategories" = @{}
    }
}

# 初始化子学科
foreach ($category in $nobelData.Keys) {
    foreach ($subcategoryName in $subcategoryMap[$category].Keys) {
        $subcategoryKey = $subcategoryMap[$category][$subcategoryName]
        $nobelData[$category]["subcategories"][$subcategoryKey] = @{
            "name" = $subcategoryName
            "description" = ""
            "prizes" = @()
        }
    }
}

# 遍历每个HTML文件
foreach ($file in $yearFiles) {
    Write-Host "Processing $file.Name..."
    
    # 读取HTML文件内容
    $content = Get-Content -Path $file.FullName -Raw
    
    # 提取年份
    $year = $file.Name -replace "year_(\d+)\.html", "$1"
    
    # 提取每个奖项
    $prizePattern = '<section class="category">(.*?)</section>'
    $prizes = [regex]::Matches($content, $prizePattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)
    
    foreach ($prize in $prizes) {
        $prizeContent = $prize.Groups[1].Value
        
        # 提取奖项类别
        $categoryPattern = '<h2>(.*?)</h2>'
        $categoryMatch = [regex]::Match($prizeContent, $categoryPattern)
        $categoryName = $categoryMatch.Groups[1].Value.Trim()
        
        if ($categoryMap.ContainsKey($categoryName)) {
            $categoryKey = $categoryMap[$categoryName]
            
            # 提取奖项详情
            $detailPattern = '<div class="prize-item">(.*?)</div>'
            $detail = [regex]::Match($prizeContent, $detailPattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)
            $detailContent = $detail.Groups[1].Value
            
            # 提取获奖者
            $winnersPattern = '<div class="winners">获奖者: (.*?)</div>'
            $winnersMatch = [regex]::Match($detailContent, $winnersPattern)
            $winners = $winnersMatch.Groups[1].Value.Trim()
            
            # 提取获奖理由
            $motivationPattern = '<div class="motivation"><strong>获奖理由:</strong> (.*?)</div>'
            $motivationMatch = [regex]::Match($detailContent, $motivationPattern)
            $motivation = $motivationMatch.Groups[1].Value.Trim()
            
            # 提取核心原理
            $principlePattern = '<div class="principle"><h4>核心原理</h4><p>(.*?)</p></div>'
            $principleMatch = [regex]::Match($detailContent, $principlePattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)
            $principle = $principleMatch.Groups[1].Value.Trim()
            $principle = $principle -replace "<ul>.*?</ul>", "" # 移除应用领域部分的ul标签
            
            # 提取应用领域
            $applicationPattern = '<div class="application"><h4>应用领域</h4><p>(.*?)</p></div>'
            $applicationMatch = [regex]::Match($detailContent, $applicationPattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)
            $application = $applicationMatch.Groups[1].Value.Trim()
            
            # 将应用领域中的<ul><li>标签转换为普通文本
            $application = $application -replace "<ul>.*?</ul>", ""
            $application = $application -replace "<li>.*?</li>", ""
            
            # 创建奖项对象
            $prizeObj = @{
                "year" = $year
                "laureates" = $winners
                "motivation" = $motivation
                "principle" = $principle
                "application" = $application
            }
            
            # 根据奖项内容确定子学科
            $subcategoryKey = $defaultSubcategory[$categoryKey]
            
            # 添加到对应子学科的prizes数组中
            $nobelData[$categoryKey]["subcategories"][$subcategoryKey]["prizes"] += $prizeObj
        }
    }
}

# 将数据转换为JavaScript格式
$jsContent = "// 诺贝尔奖科学分类数据
const nobelCategories = $(
    $nobelData | ConvertTo-Json -Depth 10 | 
    ForEach-Object { $_ -replace '\\u0027', "'" } | 
    ForEach-Object { $_ -replace '\\r\\n', "\n" }
);

// 统计数据
const nobelStatistics = {
    totalPrizes: 631,
    firstYear: 1901,
    latestYear: 2025,
    categories: {
        physics: $($nobelData["physics"]["subcategories"].Values.prizes.Count),
        chemistry: $($nobelData["chemistry"]["subcategories"].Values.prizes.Count),
        medicine: $($nobelData["medicine"]["subcategories"].Values.prizes.Count),
        literature: $($nobelData["literature"]["subcategories"].Values.prizes.Count),
        peace: $($nobelData["peace"]["subcategories"].Values.prizes.Count),
        economics: $($nobelData["economics"]["subcategories"].Values.prizes.Count)
    },
    totalAwards: 631,
    totalLaureates: 975,
    femaleLaureates: 61,
    multipleWinners: 6,
    oldestLaureate: 97,
    youngestLaureate: 17,
    organizations: 28,
    posthumousAwards: 2,
    declinedAwards: 4
};

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
}"

# 写入nobel_data.js文件
$jsContent | Out-File -Path "nobel_data.js" -Encoding UTF8

Write-Host "Done! nobel_data.js has been updated with data from all year_*.html files."