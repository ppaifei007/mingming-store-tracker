# -*- coding: utf-8 -*-
"""
鸣鸣很忙门店数据追踪 - 配置文件
"""

import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 数据目录
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DOCS_DATA_DIR = PROJECT_ROOT / "docs" / "data"

# 确保目录存在
DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DATA_DIR.mkdir(parents=True, exist_ok=True)

# 品牌名称
BRANDS = [
    "鸣鸣很忙",
    "零食很忙", 
    "赵一鸣零食"
]

# 31个省级行政区
PROVINCES = [
    # 直辖市
    "北京市", "天津市", "上海市", "重庆市",
    # 省份
    "河北省", "山西省", "辽宁省", "吉林省", "黑龙江省",
    "江苏省", "浙江省", "安徽省", "福建省", "江西省",
    "山东省", "河南省", "湖北省", "湖南省", "广东省",
    "海南省", "四川省", "贵州省", "云南省", "陕西省",
    "甘肃省", "青海省", "台湾省",
    # 自治区
    "内蒙古自治区", "广西壮族自治区", "西藏自治区", 
    "宁夏回族自治区", "新疆维吾尔自治区",
    # 特别行政区
    "香港特别行政区", "澳门特别行政区"
]

# 省份简称映射（用于地图API搜索）
PROVINCE_SHORT_NAMES = {
    "北京市": "北京",
    "天津市": "天津",
    "上海市": "上海",
    "重庆市": "重庆",
    "河北省": "河北",
    "山西省": "山西",
    "辽宁省": "辽宁",
    "吉林省": "吉林",
    "黑龙江省": "黑龙江",
    "江苏省": "江苏",
    "浙江省": "浙江",
    "安徽省": "安徽",
    "福建省": "福建",
    "江西省": "江西",
    "山东省": "山东",
    "河南省": "河南",
    "湖北省": "湖北",
    "湖南省": "湖南",
    "广东省": "广东",
    "海南省": "海南",
    "四川省": "四川",
    "贵州省": "贵州",
    "云南省": "云南",
    "陕西省": "陕西",
    "甘肃省": "甘肃",
    "青海省": "青海",
    "台湾省": "台湾",
    "内蒙古自治区": "内蒙古",
    "广西壮族自治区": "广西",
    "西藏自治区": "西藏",
    "宁夏回族自治区": "宁夏",
    "新疆维吾尔自治区": "新疆",
    "香港特别行政区": "香港",
    "澳门特别行政区": "澳门"
}

# API配置（从环境变量读取，支持GitHub Actions）
BAIDU_MAP_API_KEY = os.environ.get("BAIDU_MAP_API_KEY", "uxkjfRCGhKgbvuUrVZRdtNhGea0n2o6J")

GAODE_MAP_URL = os.environ.get(
    "GAODE_MAP_URL", 
    "https://instance-d3476d81547545fdabe2a1e7425bc4b2.agentfusion.cn-beijing.volcmcp.com/mcp/amap"
)
GAODE_MAP_API_KEY = os.environ.get(
    "GAODE_MAP_API_KEY",
    "MjY0YWU3MTk3MTcxNDZlZGE2YzhkMWM2MGM1MjIyMmQ"
)

SINA_FINANCE_URL = os.environ.get(
    "SINA_FINANCE_URL",
    "https://mcp.finance.sina.com.cn/mcp-http"
)

# 去重配置
DEDUP_DISTANCE_THRESHOLD = 50  # 50米内视为同一门店
DEDUP_TEXT_SIMILARITY_THRESHOLD = 0.85  # 地址文本相似度阈值

# API请求配置
REQUEST_DELAY = 0.5  # 请求间隔（秒）
MAX_RETRIES = 3  # 最大重试次数
PAGE_SIZE = 20  # 每页结果数
