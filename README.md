# 港股分析 Skill

这是一个面向 OpenClaw/Codex 的港股研究 Skill，只分析香港上市股票。它会结合行情数据、技术指标、HKEX 公告、公司新闻和市场环境，生成“研究参考型”的港股分析简报。

本 Skill 不提供个性化投资建议，也不输出直接买入、卖出、止损、仓位、目标价等交易指令。

## 功能特点

- 支持港股代码格式：
  - `HK00700`
  - `00700.HK`
  - `00700`
- 支持中文公司名输入，会先联网查询对应港股代码。
- 明确拒绝非港股代码，例如：
  - `AAPL`
  - `TSLA`
  - `600519`
  - `000001.SZ`
- 行情数据源按优先级降级：
  - `efinance`
  - `akshare`
  - `yfinance`
- 输出结构化港股研究简报，包含：
  - 行情与估值快照
  - 技术面
  - HKEX 公告与公司新闻
  - 市场与行业环境
  - 证据权重
  - 观察清单
- 内置事实校验闸门，重点减少港股事件股常见错误。

## 事实校验闸门

Skill 内置 `references/fact-check-rules.md`，用于约束要约、复牌、配售、并购、重大涨跌幅等事件驱动股票的分析。

输出报告前必须：

- 优先核对 HKEX / 公司公告。
- 复算溢价或折让：

  ```text
  (要约价或交易价 - 基准价) / 基准价 * 100
  ```

- 结果为负数必须写“折让”，只有结果为正数才能写“溢价”。
- 复算涨跌幅：

  ```text
  (现价或收盘价 - 昨收) / 昨收 * 100
  ```

- 区分盘中数据和收盘数据。
- 财年口径必须以年报/中报标题为准。
- 无法复算的 PE、PB、市值、股息率等数据，必须标注“第三方口径，未能复算”。
- 对要约、复牌、配售、并购、大幅异动股票，必须降低技术指标权重。

示例：

```text
8.323 vs 30.00 = (8.323 - 30.00) / 30.00 = -72.26%
```

正确写法：

```text
较30.00港元折让约72.26%
```

错误写法：

```text
较30.00港元溢价72.26%
```

## 安装方式

可以把本仓库放到你的项目 `skills/` 目录中：

```bash
mkdir -p skills
git clone https://github.com/xinchengai/hk-stock-analysis.git skills/hk-stock-analysis
```

也可以放到 OpenClaw 全局 Skill 目录：

```bash
mkdir -p ~/.openclaw/skills
git clone https://github.com/xinchengai/hk-stock-analysis.git ~/.openclaw/skills/hk-stock-analysis
```

如果你的运行环境自带 Skill 安装器，也可以直接通过安装器安装这个 GitHub 仓库。

## 可选依赖

Skill 本身可以在没有 Python 依赖的情况下被加载。  
但内置行情脚本需要至少一个行情数据源依赖，推荐安装：

```bash
python3 -m pip install efinance akshare yfinance pandas requests
```

如果没有安装任何行情依赖，脚本会返回结构化 JSON 安装提示，不会直接崩溃。

## 使用示例

分析腾讯控股：

```text
分析 HK00700
```

指定代码格式：

```text
分析 00700.HK，重点看公告和技术面
```

使用中文公司名：

```text
分析腾讯控股这支港股
```

分析事件驱动股票时，可以明确要求核验：

```text
分析 01657.HK，并核对要约价、折让/溢价、今日涨跌幅和公告来源
```

## 文件结构

```text
SKILL.md
agents/openai.yaml
references/fact-check-rules.md
references/output-format-template.md
references/stock_data_fetcher.py
```

## 验证命令

检查脚本语法：

```bash
python3 -m py_compile references/stock_data_fetcher.py
```

测试非港股代码拒绝：

```bash
python3 references/stock_data_fetcher.py AAPL
python3 references/stock_data_fetcher.py 600519
```

这两个输入应返回 `unsupported_ticker` JSON。

测试港股代码标准化：

```bash
python3 references/stock_data_fetcher.py HK00700 --days 30
python3 references/stock_data_fetcher.py 00700.HK --days 30
python3 references/stock_data_fetcher.py 00700 --days 30
```

这些格式都应标准化为 `HK00700`。

## 免责声明

本 Skill 仅用于研究参考，不构成投资建议、个性化投资推荐、交易指令、仓位建议或风险管理建议。港股小市值股票、复牌股票、要约股票和事件驱动股票波动可能非常剧烈。请务必核对 HKEX 公告等一手资料，并在需要时咨询持牌投资顾问。
