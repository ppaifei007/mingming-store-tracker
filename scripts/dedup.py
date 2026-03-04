# -*- coding: utf-8 -*-
"""
数据去重脚本
对零食很忙和赵一鸣零食的门店进行去重，剔除与鸣鸣很忙物理地址重复的门店
"""

import json
import math
from difflib import SequenceMatcher
from config import (
    BRANDS, PROVINCES, DATA_RAW_DIR, DATA_PROCESSED_DIR,
    DEDUP_DISTANCE_THRESHOLD, DEDUP_TEXT_SIMILARITY_THRESHOLD
)


def haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    使用Haversine公式计算两点间的地理距离（米）
    
    Args:
        lat1, lng1: 第一个点的纬度和经度
        lat2, lng2: 第二个点的纬度和经度
    
    Returns:
        两点间距离（米）
    """
    R = 6371000  # 地球半径（米）
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lng = math.radians(lng2 - lng1)
    
    a = (math.sin(delta_lat / 2) ** 2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * 
         math.sin(delta_lng / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


def text_similarity(text1: str, text2: str) -> float:
    """
    计算两段文本的相似度
    
    Args:
        text1, text2: 两段文本
    
    Returns:
        相似度（0-1）
    """
    if not text1 or not text2:
        return 0.0
    return SequenceMatcher(None, text1, text2).ratio()


def is_duplicate(store1: dict, store2: dict) -> bool:
    """
    判断两个门店是否为重复（同一物理位置）
    
    Args:
        store1, store2: 两个门店信息
    
    Returns:
        是否重复
    """
    lat1 = store1.get("lat", 0)
    lng1 = store1.get("lng", 0)
    lat2 = store2.get("lat", 0)
    lng2 = store2.get("lng", 0)
    
    # 如果经纬度有效，优先使用地理距离判断
    if lat1 and lng1 and lat2 and lng2:
        distance = haversine_distance(lat1, lng1, lat2, lng2)
        if distance < DEDUP_DISTANCE_THRESHOLD:
            return True
    
    # 使用地址文本相似度辅助判断
    addr1 = store1.get("address", "")
    addr2 = store2.get("address", "")
    
    if addr1 and addr2:
        similarity = text_similarity(addr1, addr2)
        if similarity >= DEDUP_TEXT_SIMILARITY_THRESHOLD:
            return True
    
    return False


def dedup_stores_against_reference(stores: list, reference_stores: list) -> tuple:
    """
    根据参考门店列表去重
    
    Args:
        stores: 待去重的门店列表
        reference_stores: 参考门店列表（基准）
    
    Returns:
        (去重后的门店列表, 被剔除的门店数量)
    """
    if not reference_stores:
        return stores, 0
    
    unique_stores = []
    removed_count = 0
    
    for store in stores:
        is_dup = False
        for ref_store in reference_stores:
            if is_duplicate(store, ref_store):
                is_dup = True
                break
        
        if not is_dup:
            unique_stores.append(store)
        else:
            removed_count += 1
    
    return unique_stores, removed_count


def dedup_within_list(stores: list) -> list:
    """
    在同一列表内部去重（去除重复记录）
    
    Args:
        stores: 门店列表
    
    Returns:
        去重后的门店列表
    """
    if not stores:
        return []
    
    unique_stores = []
    
    for store in stores:
        is_dup = False
        for existing in unique_stores:
            if is_duplicate(store, existing):
                is_dup = True
                break
        
        if not is_dup:
            unique_stores.append(store)
    
    return unique_stores


def process_source_data(source: str) -> dict:
    """
    处理单个数据源的门店数据
    
    Args:
        source: 数据源名称（baidu或gaode）
    
    Returns:
        处理后的数据
    """
    # 加载原始数据
    raw_file = DATA_RAW_DIR / f"{source}_raw.json"
    if not raw_file.exists():
        print(f"  警告: {raw_file} 不存在，跳过")
        return {}
    
    with open(raw_file, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    
    result = {
        "source": source,
        "provinces": {}
    }
    
    for province in PROVINCES:
        print(f"  处理 {province}...")
        
        # 获取各品牌在该省的门店
        mingming_stores = raw_data["data"].get("鸣鸣很忙", {}).get(province, {}).get("stores", [])
        lingshi_stores = raw_data["data"].get("零食很忙", {}).get(province, {}).get("stores", [])
        zhaoyiming_stores = raw_data["data"].get("赵一鸣零食", {}).get(province, {}).get("stores", [])
        
        # Step 1: 鸣鸣很忙内部去重
        mingming_unique = dedup_within_list(mingming_stores)
        
        # Step 2: 零食很忙去重（剔除与鸣鸣很忙重复的）
        lingshi_dedup, lingshi_removed = dedup_stores_against_reference(
            lingshi_stores, mingming_unique
        )
        lingshi_dedup = dedup_within_list(lingshi_dedup)  # 内部去重
        
        # Step 3: 赵一鸣零食去重（剔除与鸣鸣很忙和零食很忙重复的）
        zhaoyiming_dedup, zhaoyiming_removed = dedup_stores_against_reference(
            zhaoyiming_stores, mingming_unique + lingshi_dedup
        )
        zhaoyiming_dedup = dedup_within_list(zhaoyiming_dedup)  # 内部去重
        
        # 汇总该省数据
        result["provinces"][province] = {
            "鸣鸣很忙": {
                "count": len(mingming_unique),
                "stores": mingming_unique
            },
            "零食很忙": {
                "original_count": len(lingshi_stores),
                "count": len(lingshi_dedup),
                "removed": lingshi_removed,
                "stores": lingshi_dedup
            },
            "赵一鸣零食": {
                "original_count": len(zhaoyiming_stores),
                "count": len(zhaoyiming_dedup),
                "removed": zhaoyiming_removed,
                "stores": zhaoyiming_dedup
            },
            "total": len(mingming_unique) + len(lingshi_dedup) + len(zhaoyiming_dedup)
        }
    
    return result


def main():
    """主函数"""
    print("=" * 50)
    print("数据去重处理")
    print("=" * 50)
    
    for source in ["baidu", "gaode"]:
        print(f"\n处理 {source} 数据...")
        result = process_source_data(source)
        
        if result:
            # 保存处理后的数据
            output_file = DATA_PROCESSED_DIR / f"{source}_dedup.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            print(f"  保存到: {output_file}")
            
            # 统计汇总
            total_mingming = sum(
                result["provinces"][p]["鸣鸣很忙"]["count"] 
                for p in result["provinces"]
            )
            total_lingshi = sum(
                result["provinces"][p]["零食很忙"]["count"] 
                for p in result["provinces"]
            )
            total_zhaoyiming = sum(
                result["provinces"][p]["赵一鸣零食"]["count"] 
                for p in result["provinces"]
            )
            
            print(f"\n  === {source} 去重汇总 ===")
            print(f"  鸣鸣很忙: {total_mingming} 家")
            print(f"  零食很忙(去重后): {total_lingshi} 家")
            print(f"  赵一鸣零食(去重后): {total_zhaoyiming} 家")
            print(f"  合计: {total_mingming + total_lingshi + total_zhaoyiming} 家")


if __name__ == "__main__":
    main()
