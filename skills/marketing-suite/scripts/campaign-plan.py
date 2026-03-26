#!/usr/bin/env python3
"""
营销活动策划脚本
支持多种活动类型的策划方案生成
"""

import argparse
import json
from datetime import datetime, timedelta
from typing import Optional

# 活动类型配置
CAMPAIGN_TYPES = {
    "brand": {
        "name": "品牌活动",
        "objectives": ["品牌认知", "品牌形象", "用户好感度"],
        "channels": ["社交媒体", "KOL合作", "线下活动"],
        "kpi": ["曝光量", "互动率", "品牌搜索指数"]
    },
    "promotion": {
        "name": "促销活动",
        "objectives": ["销售转化", "新客获取", "复购提升"],
        "channels": ["电商平台", "私域社群", "直播带货"],
        "kpi": ["GMV", "转化率", "ROI", "客单价"]
    },
    "launch": {
        "name": "新品发布",
        "objectives": ["新品认知", "种子用户", "口碑传播"],
        "channels": ["发布会", "媒体评测", "KOL种草"],
        "kpi": ["新品销量", "好评率", "话题热度"]
    },
    "festival": {
        "name": "节日营销",
        "objectives": ["节日关联", "促销转化", "用户互动"],
        "channels": ["节日专题", "限时活动", "互动游戏"],
        "kpi": ["活动参与人数", "销售额", "用户增长"]
    }
}

# 预算分配模板
BUDGET_TEMPLATES = {
    "small": {"媒体投放": 0.4, "内容制作": 0.3, "KOL合作": 0.2, "其他": 0.1},
    "medium": {"媒体投放": 0.35, "内容制作": 0.25, "KOL合作": 0.25, "线下活动": 0.1, "其他": 0.05},
    "large": {"媒体投放": 0.3, "内容制作": 0.2, "KOL合作": 0.2, "线下活动": 0.15, "公关传播": 0.1, "其他": 0.05}
}


def create_campaign_plan(
    campaign_type: str,
    budget: str = "medium",
    duration: int = 14,
    brand: Optional[str] = None,
    product: Optional[str] = None,
    goals: Optional[list] = None
) -> dict:
    """
    创建活动策划方案
    
    Args:
        campaign_type: 活动类型
        budget: 预算规模 (small/medium/large)
        duration: 活动周期（天）
        brand: 品牌名称
        product: 产品名称
        goals: 营销目标
    
    Returns:
        活动策划方案
    """
    type_config = CAMPAIGN_TYPES.get(campaign_type, CAMPAIGN_TYPES["brand"])
    budget_config = BUDGET_TEMPLATES.get(budget, BUDGET_TEMPLATES["medium"])
    
    # 生成时间规划
    start_date = datetime.now()
    end_date = start_date + timedelta(days=duration)
    
    phases = generate_phases(duration)
    
    plan = {
        "meta": {
            "campaign_type": type_config["name"],
            "campaign_code": campaign_type,
            "brand": brand or "[品牌名称]",
            "product": product or "[产品名称]",
            "created_at": datetime.now().isoformat()
        },
        "overview": {
            "background": "[待填写活动背景]",
            "objectives": goals or type_config["objectives"],
            "target_audience": "[待填写目标人群画像]",
            "key_message": "[待填写核心传播信息]"
        },
        "timeline": {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "duration_days": duration,
            "phases": phases
        },
        "budget": {
            "scale": budget,
            "allocation": budget_config,
            "breakdown": generate_budget_breakdown(budget_config)
        },
        "channels": type_config["channels"],
        "kpi": type_config["kpi"],
        "risks": [
            {"risk": "舆情风险", "mitigation": "建立舆情监控机制，准备应急预案"},
            {"risk": "执行偏差", "mitigation": "设立里程碑检查点，及时调整"},
            {"risk": "预算超支", "mitigation": "预留10%应急预算"}
        ],
        "appendix": {
            "content_plan": "[待补充内容规划]",
            "media_plan": "[待补充媒介计划]",
            "kol_list": "[待补充KOL名单]"
        }
    }
    
    return plan


def generate_phases(duration: int) -> list:
    """生成活动阶段规划"""
    if duration <= 7:
        return [
            {"phase": "预热期", "days": "第1-2天", "tasks": ["预告发布", "话题预热"]},
            {"phase": "爆发期", "days": "第3-5天", "tasks": ["活动上线", "集中推广"]},
            {"phase": "延续期", "days": "第6-7天", "tasks": ["二次传播", "数据复盘"]}
        ]
    elif duration <= 30:
        return [
            {"phase": "预热期", "days": "第1-3天", "tasks": ["悬念营销", "KOL预热"]},
            {"phase": "引爆期", "days": "第4-10天", "tasks": ["活动上线", "全网推广", "KOL集中发声"]},
            {"phase": "持续期", "days": "第11-25天", "tasks": ["用户互动", "内容发酵", "促销转化"]},
            {"phase": "收尾期", "days": "第26-30天", "tasks": ["活动收官", "数据复盘", "用户沉淀"]}
        ]
    else:
        return [
            {"phase": "筹备期", "days": "第1-7天", "tasks": ["资源准备", "预热宣传"]},
            {"phase": "引爆期", "days": "第8-20天", "tasks": ["活动上线", "全网推广"]},
            {"phase": "持续期", "days": "第21-40天", "tasks": ["用户运营", "内容传播"]},
            {"phase": "转化期", "days": "第41-50天", "tasks": ["促销转化", "销售冲刺"]},
            {"phase": "收官期", "days": "第51-60天", "tasks": ["活动收官", "数据复盘"]}
        ]


def generate_budget_breakdown(allocation: dict) -> dict:
    """生成预算明细"""
    # 以10万为基准
    base_amount = 100000
    breakdown = {}
    for category, ratio in allocation.items():
        amount = int(base_amount * ratio)
        breakdown[category] = {
            "ratio": f"{ratio*100:.0f}%",
            "amount": f"¥{amount:,}",
            "details": []
        }
    return breakdown


def format_output(plan: dict, output_format: str = "markdown") -> str:
    """格式化输出"""
    if output_format == "json":
        return json.dumps(plan, ensure_ascii=False, indent=2)
    
    # Markdown 格式
    md = f"""# {plan['meta']['campaign_type']}策划方案

## 基本信息
- **品牌**：{plan['meta']['brand']}
- **产品**：{plan['meta']['product']}
- **创建时间**：{plan['meta']['created_at']}

---

## 一、活动背景
{plan['overview']['background']}

## 二、活动目标
"""
    for obj in plan['overview']['objectives']:
        md += f"- {obj}\n"
    
    md += f"""
## 三、目标人群
{plan['overview']['target_audience']}

## 四、核心信息
{plan['overview']['key_message']}

---

## 五、时间规划
- **开始日期**：{plan['timeline']['start_date']}
- **结束日期**：{plan['timeline']['end_date']}
- **活动周期**：{plan['timeline']['duration_days']}天

### 阶段规划
| 阶段 | 时间 | 主要任务 |
|------|------|---------|
"""
    for phase in plan['timeline']['phases']:
        tasks = "、".join(phase['tasks'])
        md += f"| {phase['phase']} | {phase['days']} | {tasks} |\n"
    
    md += """
---

## 六、预算分配
"""
    for category, detail in plan['budget']['breakdown'].items():
        md += f"- **{category}**：{detail['ratio']}（{detail['amount']}）\n"
    
    md += """
---

## 七、传播渠道
"""
    for channel in plan['channels']:
        md += f"- {channel}\n"
    
    md += """
---

## 八、核心KPI
"""
    for kpi in plan['kpi']:
        md += f"- {kpi}\n"
    
    md += """
---

## 九、风险预案
| 风险 | 应对措施 |
|------|---------|
"""
    for risk in plan['risks']:
        md += f"| {risk['risk']} | {risk['mitigation']} |\n"
    
    md += """
---

## 附录
- 内容规划：待补充
- 媒介计划：待补充
- KOL名单：待补充

---
*本方案由营销套件自动生成，请根据实际情况调整完善。*
"""
    return md


def main():
    parser = argparse.ArgumentParser(description="营销活动策划工具")
    parser.add_argument("--type", "-t", default="brand",
                        choices=list(CAMPAIGN_TYPES.keys()),
                        help="活动类型")
    parser.add_argument("--budget", "-b", default="medium",
                        choices=list(BUDGET_TEMPLATES.keys()),
                        help="预算规模")
    parser.add_argument("--duration", "-d", type=int, default=14,
                        help="活动周期（天）")
    parser.add_argument("--brand", help="品牌名称")
    parser.add_argument("--product", help="产品名称")
    parser.add_argument("--goals", nargs="+", help="营销目标")
    parser.add_argument("--format", "-f", default="markdown",
                        choices=["markdown", "json"],
                        help="输出格式")
    parser.add_argument("--output", "-o", help="输出文件路径")
    
    args = parser.parse_args()
    
    plan = create_campaign_plan(
        args.type,
        args.budget,
        args.duration,
        args.brand,
        args.product,
        args.goals
    )
    
    output = format_output(plan, args.format)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"策划方案已保存到：{args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()