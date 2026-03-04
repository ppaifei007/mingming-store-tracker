// 加载并显示数据
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
document.addEventListener('DOMContentLoaded', loadData);