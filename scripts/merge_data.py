# -*- coding: utf-8 -*-
"""
数据整合脚本
整合百度地图、高德地图数据和财报数据，计算分省年均收入和增长率
"""

import json
from datetime import datetime
from config import PROVINCES, DATA_RAW_DIR, DATA_PROCESSED_DIR, DOCS_DATA_DIR


def load_json(file_path):
    """加载JSON文件"""
    if not file_path.exists():
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_province_revenue(province_stores: int, total_stores: int, total_revenue: float) -> float:
    """
    计算省份年均收入（基于门店数量权重分摊）
    
    Args:
        province_stores: 省份门店数量
        total_stores: 全国门店总数
        total_revenue: 全国总营收（亿元）
    
    Returns:
        省份估算营收（万元）
    """
    if total_stores == 0:
        return 0
    
    # 分摊比例
    ratio = province_stores / total_stores
    # 转换为万元
    return round(total_revenue * 10000 * ratio, 2)


def merge_data():
    """
    整合所有数据
    
    Returns:
        最终报告数据
    """
    # 加载去重后的数据
    baidu_data = load_json(DATA_PROCESSED_DIR / "baidu_dedup.json")
    gaode_data = load_json(DATA_PROCESSED_DIR / "gaode_dedup.json")
    financial_data = load_json(DATA_RAW_DIR / "financial_raw.json")
    
    # 获取财报数据
    fin_2024 = financial_data.get("financial_data", {}).get("2024", {}) if financial_data else {}
    fin_2025 = financial_data.get("financial_data", {}).get("2025", {}) if financial_data else {}
    
    revenue_2024 = fin_2024.get("total_revenue", 390)  # 默认值（亿元）
    revenue_2025 = fin_2025.get("total_revenue", 500)
    stores_2024 = fin_2024.get("total_stores", 13000)
    stores_2025 = fin_2025.get("total_stores", 15000)
    
    result = {
        "meta": {
            "generated_at": datetime.now().isoformat(),
            "sources": ["baidu_map", "gaode_map", "sina_finance"],
            "financial_years": ["2024", "2025"]
        },
        "financial_summary": {
            "2024": {
                "total_revenue_billion": revenue_2024,
                "total_stores": stores_2024,
                "yoy_growth": fin_2024.get("yoy_growth", 0.45)
            },
            "2025": {
                "total_revenue_billion": revenue_2025,
                "total_stores": stores_2025,
                "yoy_growth": fin_2025.get("yoy_growth", 0.28)
            }
        },
        "baidu_data": {
            "provinces": []
        },
        "gaode_data": {
            "provinces": []
        }
    }
    
    # 处理百度数据
    if baidu_data:
        baidu_total_stores = sum(
            baidu_data["provinces"].get(p, {}).get("total", 0) 
            for p in PROVINCES
        )
        
        for province in PROVINCES:
            p_data = baidu_data["provinces"].get(province, {})
            mingming = p_data.get("鸣鸣很忙", {}).get("count", 0)
            lingshi = p_data.get("零食很忙", {}).get("count", 0)
            zhaoyiming = p_data.get("赵一鸣零食", {}).get("count", 0)
            total = p_data.get("total", mingming + lingshi + zhaoyiming)
            
            # 计算收入（使用2024年数据估算该省收入）
            revenue_2024_province = calculate_province_revenue(total, baidu_total_stores, revenue_2024)
            revenue_2025_province = calculate_province_revenue(total, baidu_total_stores, revenue_2025)
            
            # 计算增长率
            growth_rate = 0
            if revenue_2024_province > 0:
                growth_rate = round((revenue_2025_province - revenue_2024_province) / revenue_2024_province * 100, 2)
            
            result["baidu_data"]["provinces"].append({
                "province": province,
                "mingming": mingming,
                "lingshi": lingshi,
                "zhaoyiming": zhaoyiming,
                "total": total,
                "revenue_2024": revenue_2024_province,
                "revenue_2025": revenue_2025_province,
                "growth_rate": growth_rate
            })
        
        result["baidu_data"]["total_stores"] = baidu_total_stores
    
    # 处理高德数据
    if gaode_data:
        gaode_total_stores = sum(
            gaode_data["provinces"].get(p, {}).get("total", 0) 
            for p in PROVINCES
        )
        
        for province in PROVINCES:
            p_data = gaode_data["provinces"].get(province, {})
            mingming = p_data.get("鸣鸣很忙", {}).get("count", 0)
            lingshi = p_data.get("零食很忙", {}).get("count", 0)
            zhaoyiming = p_data.get("赵一鸣零食", {}).get("count", 0)
            total = p_data.get("total", mingming + lingshi + zhaoyiming)
            
            # 计算收入
            revenue_2024_province = calculate_province_revenue(total, gaode_total_stores, revenue_2024)
            revenue_2025_province = calculate_province_revenue(total, gaode_total_stores, revenue_2025)
            
            # 计算增长率
            growth_rate = 0
            if revenue_2024_province > 0:
                growth_rate = round((revenue_2025_province - revenue_2024_province) / revenue_2024_province * 100, 2)
            
            result["gaode_data"]["provinces"].append({
                "province": province,
                "mingming": mingming,
                "lingshi": lingshi,
                "zhaoyiming": zhaoyiming,
                "total": total,
                "revenue_2024": revenue_2024_province,
                "revenue_2025": revenue_2025_province,
                "growth_rate": growth_rate
            })
        
        result["gaode_data"]["total_stores"] = gaode_total_stores
    
    return result


def main():
    """主函数"""
    print("=" * 50)
    print("数据整合处理")
    print("=" * 50)
    
    result = merge_data()
    
    # 保存到processed目录
    output_file = DATA_PROCESSED_DIR / "final_report.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n保存到: {output_file}")
    
    # 同时保存到docs/data目录供网站使用
    web_output = DOCS_DATA_DIR / "report.json"
    with open(web_output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"网站数据: {web_output}")
    
    # 显示汇总
    print("\n=== 数据汇总 ===")
    print(f"财报数据:")
    print(f"  2024年: {result['financial_summary']['2024']['total_revenue_billion']} 亿元")
    print(f"  2025年: {result['financial_summary']['2025']['total_revenue_billion']} 亿元")
    
    if result["baidu_data"]["provinces"]:
        print(f"\n百度地图数据: {result['baidu_data'].get('total_stores', 0)} 家门店")
    
    if result["gaode_data"]["provinces"]:
        print(f"高德地图数据: {result['gaode_data'].get('total_stores', 0)} 家门店")


if __name__ == "__main__":
    main()
