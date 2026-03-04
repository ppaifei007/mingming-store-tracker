# -*- coding: utf-8 -*-
"""
百度地图数据采集脚本
通过百度地图API搜索鸣鸣很忙、零食很忙、赵一鸣零食在各省的门店
"""

import json
import time
import requests
from datetime import datetime
from config import (
    BRANDS, PROVINCES, PROVINCE_SHORT_NAMES,
    BAIDU_MAP_API_KEY, DATA_RAW_DIR,
    REQUEST_DELAY, MAX_RETRIES, PAGE_SIZE
)


def search_poi_baidu(query: str, region: str, page_num: int = 0) -> dict:
    """
    调用百度地图POI搜索API
    
    Args:
        query: 搜索关键词（品牌名）
        region: 搜索区域（省份）
        page_num: 页码，从0开始
    
    Returns:
        API返回的JSON数据
    """
    url = "https://api.map.baidu.com/place/v2/search"
    params = {
        "query": query,
        "region": region,
        "output": "json",
        "ak": BAIDU_MAP_API_KEY,
        "page_size": PAGE_SIZE,
        "page_num": page_num,
        "scope": 2  # 返回详细信息
    }
    
    for retry in range(MAX_RETRIES):
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == 0:
                return data
            else:
                print(f"  API错误: {data.get('message', '未知错误')}")
                return {"results": [], "total": 0}
                
        except Exception as e:
            print(f"  请求失败 (重试 {retry + 1}/{MAX_RETRIES}): {e}")
            if retry < MAX_RETRIES - 1:
                time.sleep(REQUEST_DELAY * (retry + 1))
    
    return {"results": [], "total": 0}


def fetch_brand_stores_in_province(brand: str, province: str) -> list:
    """
    获取某品牌在某省的所有门店
    
    Args:
        brand: 品牌名称
        province: 省份名称
    
    Returns:
        门店列表
    """
    region = PROVINCE_SHORT_NAMES.get(province, province.replace("省", "").replace("市", ""))
    all_stores = []
    page_num = 0
    
    print(f"  搜索 {brand} 在 {region}...")
    
    while True:
        data = search_poi_baidu(brand, region, page_num)
        results = data.get("results", [])
        
        if not results:
            break
        
        for poi in results:
            # 过滤：名称必须包含品牌关键词
            name = poi.get("name", "")
            if brand in name or any(b in name for b in ["鸣鸣", "零食很忙", "赵一鸣"]):
                location = poi.get("location") or {}
                store = {
                    "uid": poi.get("uid", ""),
                    "name": name,
                    "address": poi.get("address", ""),
                    "province": province,
                    "city": poi.get("city", ""),
                    "area": poi.get("area", ""),
                    "lat": location.get("lat", 0) if isinstance(location, dict) else 0,
                    "lng": location.get("lng", 0) if isinstance(location, dict) else 0,
                    "tel": poi.get("telephone", ""),
                    "brand": brand
                }
                all_stores.append(store)
        
        # 检查是否还有更多页
        total = data.get("total", 0)
        if (page_num + 1) * PAGE_SIZE >= total:
            break
        
        page_num += 1
        time.sleep(REQUEST_DELAY)
    
    return all_stores


def fetch_all_data() -> dict:
    """
    采集所有品牌在所有省份的门店数据
    
    Returns:
        完整的采集数据
    """
    result = {
        "source": "baidu_map",
        "fetch_time": datetime.now().isoformat(),
        "data": {}
    }
    
    for brand in BRANDS:
        print(f"\n采集品牌: {brand}")
        result["data"][brand] = {}
        
        for province in PROVINCES:
            stores = fetch_brand_stores_in_province(brand, province)
            result["data"][brand][province] = {
                "count": len(stores),
                "stores": stores
            }
            print(f"    {province}: {len(stores)} 家门店")
            time.sleep(REQUEST_DELAY)
    
    return result


def main():
    """主函数"""
    print("=" * 50)
    print("百度地图数据采集")
    print("=" * 50)
    
    data = fetch_all_data()
    
    # 保存原始数据
    output_file = DATA_RAW_DIR / "baidu_raw.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n数据已保存到: {output_file}")
    
    # 统计汇总
    print("\n=== 采集汇总 ===")
    for brand in BRANDS:
        total = sum(
            data["data"][brand][p]["count"] 
            for p in PROVINCES 
            if p in data["data"][brand]
        )
        print(f"{brand}: 共 {total} 家门店")


if __name__ == "__main__":
    main()
