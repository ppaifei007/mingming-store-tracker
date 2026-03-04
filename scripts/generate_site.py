# -*- coding: utf-8 -*-
"""
网站生成脚本
生成静态HTML网站展示门店数据
"""

import json
from datetime import datetime
from pathlib import Path
from config import DATA_PROCESSED_DIR, DOCS_DATA_DIR

PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"


def generate_html():
    """生成HTML页面"""
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>鸣鸣很忙门店数据追踪平台</title>
    <link rel="stylesheet" href="assets/style.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.7/css/jquery.dataTables.min.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>鸣鸣很忙门店数据追踪平台</h1>
            <p class="update-time">数据更新时间: <span id="updateTime">-</span></p>
        </header>
        
        <section class="summary-cards">
            <div class="card">
                <h3>2024年总营收</h3>
                <p class="value" id="revenue2024">-</p>
                <span class="unit">亿元</span>
            </div>
            <div class="card">
                <h3>2025年总营收</h3>
                <p class="value" id="revenue2025">-</p>
                <span class="unit">亿元</span>
            </div>
            <div class="card">
                <h3>同比增长</h3>
                <p class="value" id="yoyGrowth">-</p>
                <span class="unit">%</span>
            </div>
        </section>
        
        <section class="tabs">
            <button class="tab-btn active" data-tab="baidu">百度地图数据</button>
            <button class="tab-btn" data-tab="gaode">高德地图数据</button>
        </section>
        
        <section class="tab-content" id="baidu-tab">
            <h2>百度地图数据 <span class="total-stores" id="baiduTotal">-</span></h2>
            <table id="baiduTable" class="display">
                <thead>
                    <tr>
                        <th>省份</th>
                        <th>鸣鸣很忙</th>
                        <th>零食很忙</th>
                        <th>赵一鸣零食</th>
                        <th>合计</th>
                        <th>2024营收(万)</th>
                        <th>2025营收(万)</th>
                        <th>增长率</th>
                    </tr>
                </thead>
                <tbody id="baiduBody"></tbody>
            </table>
        </section>
        
        <section class="tab-content hidden" id="gaode-tab">
            <h2>高德地图数据 <span class="total-stores" id="gaodeTotal">-</span></h2>
            <table id="gaodeTable" class="display">
                <thead>
                    <tr>
                        <th>省份</th>
                        <th>鸣鸣很忙</th>
                        <th>零食很忙</th>
                        <th>赵一鸣零食</th>
                        <th>合计</th>
                        <th>2024营收(万)</th>
                        <th>2025营收(万)</th>
                        <th>增长率</th>
                    </tr>
                </thead>
                <tbody id="gaodeBody"></tbody>
            </table>
        </section>
        
        <footer>
            <p>数据说明:</p>
            <ul>
                <li>门店数据来源: 百度地图API、高德地图API</li>
                <li>财报数据来源: 新浪财经</li>
                <li>零食很忙和赵一鸣零食门店已剔除与鸣鸣很忙物理地址重复的门店</li>
                <li>分省营收为基于门店数量权重的估算值</li>
            </ul>
        </footer>
    </div>
    
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js"></script>
    <script src="assets/app.js"></script>
</body>
</html>'''
    
    output_file = DOCS_DIR / "index.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"生成: {output_file}")


def generate_css():
    """生成CSS样式"""
    css = '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

.container {
    max-width: 1400px;
    margin: 0 auto;
    background: white;
    border-radius: 16px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    overflow: hidden;
}

header {
    background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
    color: white;
    padding: 30px;
    text-align: center;
}

header h1 {
    font-size: 2rem;
    margin-bottom: 10px;
}

.update-time {
    opacity: 0.9;
    font-size: 0.9rem;
}

.summary-cards {
    display: flex;
    justify-content: center;
    gap: 30px;
    padding: 30px;
    background: #f8f9fa;
}

.card {
    background: white;
    border-radius: 12px;
    padding: 25px 40px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s;
}

.card:hover {
    transform: translateY(-5px);
}

.card h3 {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 10px;
}

.card .value {
    font-size: 2.5rem;
    font-weight: bold;
    color: #333;
}

.card .unit {
    color: #999;
    font-size: 0.9rem;
}

.tabs {
    display: flex;
    border-bottom: 2px solid #eee;
    padding: 0 30px;
}

.tab-btn {
    padding: 15px 30px;
    border: none;
    background: none;
    font-size: 1rem;
    cursor: pointer;
    color: #666;
    transition: all 0.3s;
    border-bottom: 3px solid transparent;
    margin-bottom: -2px;
}

.tab-btn:hover {
    color: #333;
}

.tab-btn.active {
    color: #667eea;
    border-bottom-color: #667eea;
    font-weight: bold;
}

.tab-content {
    padding: 30px;
}

.tab-content.hidden {
    display: none;
}

.tab-content h2 {
    margin-bottom: 20px;
    color: #333;
}

.total-stores {
    font-size: 0.9rem;
    color: #666;
    font-weight: normal;
}

table.dataTable {
    width: 100% !important;
}

table.dataTable thead th {
    background: #667eea;
    color: white;
    padding: 12px 15px;
}

table.dataTable tbody td {
    padding: 10px 15px;
}

table.dataTable tbody tr:hover {
    background: #f5f5f5;
}

.growth-positive {
    color: #27ae60;
    font-weight: bold;
}

.growth-negative {
    color: #e74c3c;
    font-weight: bold;
}

footer {
    background: #f8f9fa;
    padding: 30px;
    border-top: 1px solid #eee;
}

footer p {
    font-weight: bold;
    margin-bottom: 10px;
    color: #333;
}

footer ul {
    margin-left: 20px;
    color: #666;
    font-size: 0.9rem;
    line-height: 1.8;
}

@media (max-width: 768px) {
    .summary-cards {
        flex-direction: column;
        align-items: center;
    }
    
    .card {
        width: 100%;
        max-width: 300px;
    }
    
    .tabs {
        flex-direction: column;
    }
    
    .tab-btn {
        border-bottom: none;
        border-left: 3px solid transparent;
    }
    
    .tab-btn.active {
        border-bottom: none;
        border-left-color: #667eea;
    }
}'''
    
    output_file = DOCS_DIR / "assets" / "style.css"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(css)
    print(f"生成: {output_file}")


def generate_js():
    """生成JavaScript脚本"""
    js = '''// 加载并显示数据
async function loadData() {
    try {
        const response = await fetch('data/report.json');
        const data = await response.json();
        
        // 更新时间
        document.getElementById('updateTime').textContent = 
            new Date(data.meta.generated_at).toLocaleString('zh-CN');
        
        // 财报摘要
        const fin = data.financial_summary;
        document.getElementById('revenue2024').textContent = fin['2024'].total_revenue_billion;
        document.getElementById('revenue2025').textContent = fin['2025'].total_revenue_billion;
        
        const growth = ((fin['2025'].total_revenue_billion - fin['2024'].total_revenue_billion) 
            / fin['2024'].total_revenue_billion * 100).toFixed(1);
        document.getElementById('yoyGrowth').textContent = growth;
        
        // 百度地图数据表
        renderTable('baiduBody', data.baidu_data.provinces);
        document.getElementById('baiduTotal').textContent = 
            `(共 ${data.baidu_data.total_stores || 0} 家门店)`;
        
        // 高德地图数据表
        renderTable('gaodeBody', data.gaode_data.provinces);
        document.getElementById('gaodeTotal').textContent = 
            `(共 ${data.gaode_data.total_stores || 0} 家门店)`;
        
        // 初始化DataTables
        $('#baiduTable').DataTable({
            language: {
                url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/zh.json'
            },
            pageLength: 15,
            order: [[4, 'desc']]
        });
        
        $('#gaodeTable').DataTable({
            language: {
                url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/zh.json'
            },
            pageLength: 15,
            order: [[4, 'desc']]
        });
        
    } catch (error) {
        console.error('加载数据失败:', error);
    }
}

// 渲染表格
function renderTable(bodyId, provinces) {
    const tbody = document.getElementById(bodyId);
    
    if (!provinces || provinces.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8">暂无数据</td></tr>';
        return;
    }
    
    tbody.innerHTML = provinces.map(p => {
        const growthClass = p.growth_rate >= 0 ? 'growth-positive' : 'growth-negative';
        const growthSign = p.growth_rate >= 0 ? '+' : '';
        
        return `
            <tr>
                <td>${p.province}</td>
                <td>${p.mingming}</td>
                <td>${p.lingshi}</td>
                <td>${p.zhaoyiming}</td>
                <td><strong>${p.total}</strong></td>
                <td>${p.revenue_2024.toLocaleString()}</td>
                <td>${p.revenue_2025.toLocaleString()}</td>
                <td class="${growthClass}">${growthSign}${p.growth_rate}%</td>
            </tr>
        `;
    }).join('');
}

// Tab切换
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        // 移除所有active
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.add('hidden'));
        
        // 激活当前
        btn.classList.add('active');
        document.getElementById(btn.dataset.tab + '-tab').classList.remove('hidden');
    });
});

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', loadData);'''
    
    output_file = DOCS_DIR / "assets" / "app.js"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(js)
    print(f"生成: {output_file}")


def main():
    """主函数"""
    print("=" * 50)
    print("生成静态网站")
    print("=" * 50)
    
    # 确保目录存在
    (DOCS_DIR / "assets").mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "data").mkdir(parents=True, exist_ok=True)
    
    # 生成文件
    generate_html()
    generate_css()
    generate_js()
    
    print("\n网站生成完成!")
    print(f"预览: 在浏览器中打开 {DOCS_DIR / 'index.html'}")


if __name__ == "__main__":
    main()
