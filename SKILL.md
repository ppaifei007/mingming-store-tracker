# Skill: 鸣鸣很忙门店数据更新

手动触发鸣鸣很忙门店数据更新，采集百度/高德地图最新门店数据并重新生成网站。

## 触发词

- 更新门店数据
- 刷新鸣鸣很忙数据
- 重新采集地图数据
- 更新鸣鸣很忙
- mingming update
- /mingming-update

## 功能说明

此 Skill 用于手动触发门店数据的更新流程，包括：

1. **数据采集**: 从百度地图和高德地图API采集"鸣鸣很忙"、"零食很忙"、"赵一鸣零食"在全国31个省份的门店数据
2. **数据去重**: 剔除零食很忙和赵一鸣零食中与鸣鸣很忙物理地址重复的门店（基于50米地理距离阈值）
3. **财报整合**: 从新浪财经获取最新财报数据，计算分省年均收入和增长率
4. **网站更新**: 重新生成静态网站数据文件

## 项目位置

```
c:/AGENTIC/mingming-store-tracker/
```

## 执行方式

### 方式1: 本地运行（推荐测试时使用）

```bash
cd c:/AGENTIC/mingming-store-tracker/scripts
python run_all.py
```

或单独运行各脚本：

```bash
python fetch_baidu.py      # 采集百度地图数据
python fetch_gaode.py      # 采集高德地图数据
python fetch_financial.py  # 采集财报数据
python dedup.py            # 数据去重
python merge_data.py       # 数据整合
python generate_site.py    # 生成网站
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

| 文件路径 | 说明 |
|---------|------|
| `data/raw/baidu_raw.json` | 百度地图原始数据 |
| `data/raw/gaode_raw.json` | 高德地图原始数据 |
| `data/raw/financial_raw.json` | 财报原始数据 |
| `data/processed/baidu_dedup.json` | 百度数据（去重后） |
| `data/processed/gaode_dedup.json` | 高德数据（去重后） |
| `data/processed/final_report.json` | 最终整合报告 |
| `docs/data/report.json` | 网站数据文件 |

## 环境配置

### 必需的环境变量

在本地运行前需要配置以下环境变量：

```bash
# Windows PowerShell
$env:BAIDU_MAP_API_KEY = "your_baidu_api_key"
$env:GAODE_MAP_API_KEY = "your_gaode_api_key"

# Linux/Mac
export BAIDU_MAP_API_KEY="your_baidu_api_key"
export GAODE_MAP_API_KEY="your_gaode_api_key"
```

### GitHub Secrets 配置

在 GitHub 仓库中配置以下 Secrets（Settings → Secrets and variables → Actions）：

- `BAIDU_MAP_API_KEY` - 百度地图API密钥
- `GAODE_MAP_URL` - 高德地图MCP服务URL
- `GAODE_MAP_API_KEY` - 高德地图MCP API密钥

### 依赖安装

```bash
pip install requests httpx
```

## Agent执行步骤

当用户触发此 Skill 时，按以下步骤执行：

1. 确认用户意图（全量更新 vs 仅更新某数据源）
2. 检查环境变量配置是否完整
3. 询问执行方式（本地运行 or GitHub Actions）
4. 执行相应的更新命令
5. 监控执行进度并报告结果

## 示例对话

**用户**: 帮我更新鸣鸣很忙的门店数据

**Agent**: 好的，我来帮您更新鸣鸣很忙门店数据。请问您想：
1. 本地运行更新脚本（测试用）
2. 触发 GitHub Actions 更新（生产用）

**用户**: 本地运行

**Agent**: 正在执行本地更新...

```bash
cd c:/AGENTIC/mingming-store-tracker/scripts && python run_all.py
```

更新完成！数据已保存到 docs/data/report.json

---

## 自动更新说明

GitHub Actions 已配置为每月1日 UTC 00:00（北京时间08:00）自动运行。

查看自动更新状态：
- GitHub 仓库 → Actions → "Update Store Data" workflow

## 网站访问

部署后可通过 GitHub Pages 访问：
- URL: `https://{username}.github.io/mingming-store-tracker/`
