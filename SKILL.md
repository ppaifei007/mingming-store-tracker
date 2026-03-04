# Skill: 鸣鸣很忙门店数据更新

手动触发鸣鸣很忙门店数据更新，采集百度/高德地图最新门店数据并重新生成网站。

## 触发词

- 更新门店数据
- 刷新鸣鸣很忙数据
- 重新采集地图数据
- 更新鸣鸣很忙
- mingming update

## 功能说明

此 Skill 用于手动触发门店数据的更新流程，包括：

1. **数据采集**: 从百度地图和高德地图API采集"鸣鸣很忙"、"零食很忙"、"赵一鸣零食"在全国31个省份的门店数据
2. **数据去重**: 剔除零食很忙和赵一鸣零食中与鸣鸣很忙物理地址重复的门店
3. **财报整合**: 从新浪财经获取最新财报数据，计算分省年均收入和增长率
4. **网站更新**: 重新生成静态网站数据文件

## 执行方式

### 方式1: 本地运行（推荐测试时使用）

```bash
cd c:/AGENTIC/mingming-store-tracker/scripts
python run_all.py
```

### 方式2: 触发 GitHub Actions（推荐生产使用）

通过 GitHub API 触发 workflow_dispatch 事件：

```bash
# 使用 gh CLI
gh workflow run update-data.yml --repo {owner}/{repo}

# 或使用 curl
curl -X POST \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/{owner}/{repo}/actions/workflows/update-data.yml/dispatches \
  -d '{"ref":"main"}'
```

## 数据输出

更新完成后，以下文件将被更新：

- `data/raw/baidu_raw.json` - 百度地图原始数据
- `data/raw/gaode_raw.json` - 高德地图原始数据
- `data/raw/financial_raw.json` - 财报原始数据
- `data/processed/baidu_dedup.json` - 百度数据（去重后）
- `data/processed/gaode_dedup.json` - 高德数据（去重后）
- `data/processed/final_report.json` - 最终整合报告
- `docs/data/report.json` - 网站数据文件

## 执行步骤

当用户触发此 Skill 时，按以下步骤执行：

1. 确认用户意图（全量更新 vs 仅更新某数据源）
2. 询问执行方式（本地运行 or GitHub Actions）
3. 执行相应的更新命令
4. 报告执行结果

## 环境要求

- Python 3.8+
- 依赖包: requests, httpx
- API密钥: BAIDU_MAP_API_KEY, GAODE_MAP_API_KEY (配置在环境变量或 GitHub Secrets)

## 示例对话

**用户**: 帮我更新鸣鸣很忙的门店数据

**Agent**: 好的，我来帮您更新鸣鸣很忙门店数据。请问您想：
1. 本地运行更新脚本（测试用）
2. 触发 GitHub Actions 更新（生产用）

**用户**: 本地运行

**Agent**: 正在执行本地更新...
```
cd c:/AGENTIC/mingming-store-tracker/scripts && python run_all.py
```
更新完成！数据已保存到 docs/data/report.json
