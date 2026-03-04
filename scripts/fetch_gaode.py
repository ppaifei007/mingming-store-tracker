# -*- coding: utf-8 -*-
"""
高德地图数据采集脚本
通过高德地图MCP HTTP服务搜索鸣鸣很忙、零食很忙、赵一鸣零食在各省的门店
"""

import json
import time
import requests
from datetime import datetime
from config import (
    BRANDS, PROVINCES, PROVINCE_SHORT_NAMES,
    GAODE_MAP_URL, GAODE_MAP_API_KEY, DATA_RAW_DIR,
    REQUEST_DELAY, MAX_RETRIES, PAGE_SIZE
)


def call_gaode_mcp(method: str, params: dict) -> dict:
    """
    调用高德地图MCP服务
    
    Args:
        method: MCP方法名
        params: 方法参数
    
    Returns:
        MCP返回的结果
    """
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": GAODE_MAP_API_KEY
    }
    
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": method,
            "arguments": params
        }
    }
    
    for retry in range(MAX_RETRIES):
        try:
            response = requests.post(
                GAODE_MAP_URL, 
                headers=headers, 
                json=payload, 
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            if "result" in data:
                return data["result"]
            elif "error" in data:
                print(f"  MCP错误: {data['error']}")
                return {"content": []}
            return data
            
        except Exception as e:
            print(f"  请求失败 (重试 {retry + 1}/{MAX_RETRIES}): {e}")
            if retry < MAX_RETRIES - 1:
                time.sleep(REQUEST_DELAY * (retry + 1))
    
    return {"content": []}


def search_poi_gaode(keywords: str, city: str, page: int = 1) -> list:
    """
    调用高德地图POI搜索
    
    Args:
        keywords: 搜索关键词
        city: 城市/省份名称
        page: 页码，从1开始
    
    Returns:
        POI列表
    """
    result = call_gaode_mcp("maps_text_search", {
        "keywords": keywords,
        "city": city,
        "page": page,
        "offset": PAGE_SIZE
    })
    
    # 解析MCP返回结果
    if isinstance(result, dict) and "content" in result:
        content = result["content"]
        if isinstance(content, list) and len(content) > 0:
            text = content[0].get("text", "")
            try:
                return json.loads(text).get("pois", [])
            except:
                return []
    
    return []


def fetch_brand_stores_in_province(brand: str, province: str) -> list:
    """
    获取某品牌在某省的所有门店
    
    Args:
        brand: 品牌名称
        province: 省份名称
    
    Returns:
        门店列表
    """
    city = PROVINCE_SHORT_NAMES.get(province, province.replace("省", "").replace("市", ""))
    all_stores = []
    page = 1
    
    print(f"  搜索 {brand} 在 {city}...")
    
    while True:
        pois = search_poi_gaode(brand, city, page)
        
        if not pois:
            break
        
        for poi in pois:
            # 过滤：名称必须包含品牌关键词
            name = poi.get("name", "")
            if brand in name or any(b in name for b in ["鸣鸣", "零食很忙", "赵一鸣"]):
                location = poi.get("location", "0,0").split(",")
                store = {
                    "id": poi.get("id", ""),
                    "name": name,
                    "address": poi.get("address", ""),
                    "province": province,
                    "city": poi.get("cityname", ""),
                    "area": poi.get("adname", ""),
                    "lat": float(location[1]) if len(location) > 1 else 0,
                    "lng": float(location[0]) if len(location) > 0 else 0,
                    "tel": poi.get("tel", ""),
                    "brand": brand
                }
                all_stores.append(store)
        
        # 检查是否还有更多页
        if len(pois) < PAGE_SIZE:
            break
        
        page += 1
        time.sleep(REQUEST_DELAY)
    
    return all_stores


def fetch_all_data() -> dict:
    """
    采集所有品牌在所有省份的门店数据
    
    Returns:
        完整的采集数据
    """
    result = {
        "source": "gaode_map",
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
    print("高德地图数据采集")
    print("=" * 50)
    
    data = fetch_all_data()
    
    # 保存原始数据
    output_file = DATA_RAW_DIR / "gaode_raw.json"
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
