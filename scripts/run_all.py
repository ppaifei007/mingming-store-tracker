# -*- coding: utf-8 -*-
"""
一键运行所有数据采集和处理脚本
"""

import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent


def run_script(name: str):
    """运行指定脚本"""
    script_path = SCRIPTS_DIR / name
    
    if not script_path.exists():
        print(f"错误: 脚本不存在 {script_path}")
        return 1
    
    print(f"\n{'='*60}")
    print(f"运行: {name}")
    print('='*60)
    
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(SCRIPTS_DIR)
    )
    
    if result.returncode != 0:
        print(f"警告: {name} 返回码 {result.returncode}")
    
    return result.returncode


def main():
    """主函数"""
    print("="*60)
    print("鸣鸣很忙门店数据 - 全量更新")
    print("="*60)
    
    # 按顺序运行脚本
    scripts = [
        "fetch_baidu.py",      # 采集百度数据
        "fetch_gaode.py",      # 采集高德数据
        "fetch_financial.py",  # 采集财报数据
        "dedup.py",            # 数据去重
        "merge_data.py",       # 数据整合
        "generate_site.py"     # 生成网站
    ]
    
    for script in scripts:
        run_script(script)
    
    print("\n" + "="*60)
    print("全部完成!")
    print("="*60)


if __name__ == "__main__":
    main()
