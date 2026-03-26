#!/usr/bin/env python3
"""
创意生成器 - 头脑风暴脚本
支持多种头脑风暴方法和场景化工作流
"""

import argparse
import json
import sys
from datetime import datetime
from typing import List, Dict, Any


class BrainstormGenerator:
    """头脑风暴生成器"""
    
    def __init__(self, method: str = "classic"):
        self.method = method
        self.methods = {
            "classic": self._classic_brainstorm,
            "scamper": self._scamper,
            "hats": self._six_hats,
            "reverse": self._reverse_brainstorm,
            "5whys": self._five_whys,
            "starburst": self._starburst,
            "constraint": self._constraint_release,
        }
    
    def generate(self, **kwargs) -> Dict[str, Any]:
        """生成创意"""
        if self.method not in self.methods:
            return {"error": f"Unknown method: {self.method}"}
        
        return self.methods[self.method](**kwargs)
    
    def _classic_brainstorm(self, theme: str, count: int = 10, **kwargs) -> Dict[str, Any]:
        """经典头脑风暴"""
        return {
            "method": "经典头脑风暴",
            "theme": theme,
            "instructions": f"""
快速头脑风暴任务：

主题：{theme}

要求：
- 生成 {count} 个创意点子
- 混合常规与非常规点子
- 每个点子用1句话描述
- 包含至少2个"疯狂点子"

输出格式：
1. [点子描述]
2. [点子描述]
...
""",
            "count": count
        }
    
    def _scamper(self, target: str, **kwargs) -> Dict[str, Any]:
        """SCAMPER 变换法"""
        return {
            "method": "SCAMPER 变换法",
            "target": target,
            "instructions": f"""
SCAMPER 分析任务：

目标：{target}

对每个维度生成2-3个创新点子：

- S (Substitute)：可替换什么？替代材料、组件、人员、流程？
- C (Combine)：可合并什么？组合功能、整合流程、混合元素？
- A (Adapt)：可调整什么？借鉴其他行业、修改设计？
- M (Modify/Magnify)：可放大什么？增加尺寸、频率、强度？
- P (Put to other uses)：还能做什么？新应用场景、新用户群？
- E (Eliminate)：可删除什么？简化流程、去除冗余？
- R (Reverse/Rearrange)：可重组什么？改变顺序、逆向思维？

输出格式：
每个维度列出具体的创新点子。
"""
        }
    
    def _six_hats(self, decision: str, **kwargs) -> Dict[str, Any]:
        """六顶思考帽"""
        return {
            "method": "六顶思考帽",
            "decision": decision,
            "instructions": f"""
六顶思考帽分析任务：

决策：{decision}

按顺序思考：

🎩 白帽（事实）：我们知道什么？数据、信息、已知事实
🎩 红帽（情感）：直觉反应是什么？感受、预感、第一印象
🎩 黑帽（谨慎）：可能出什么问题？风险、困难、潜在问题
🎩 黄帽（乐观）：有什么好处？价值、利益、机会
🎩 绿帽（创意）：有什么替代方案？新点子、新方法
🎩 蓝帽（过程）：最佳方法是什么？总结、决策、下一步

输出格式：
为每顶帽子提供完整的分析内容。
"""
        }
    
    def _reverse_brainstorm(self, target: str, **kwargs) -> Dict[str, Any]:
        """逆向头脑风暴"""
        return {
            "method": "逆向头脑风暴",
            "target": target,
            "instructions": f"""
逆向头脑风暴任务：

目标：{target}

步骤1：如何让这个目标失败？（列出5-10个方法）
步骤2：将每个失败方法翻转为成功策略
步骤3：识别隐藏风险
步骤4：制定预防措施

输出格式：
1. 失败方法列表
2. 对应的成功策略
3. 风险识别
4. 预防措施
"""
        }
    
    def _five_whys(self, problem: str, **kwargs) -> Dict[str, Any]:
        """5 Whys 根因分析"""
        return {
            "method": "5 Whys 根因分析",
            "problem": problem,
            "instructions": f"""
5 Whys 根因分析任务：

问题：{problem}

连续问5次"为什么"，直到找到根本原因：

为什么1：[问题发生的原因？]
  ↓
为什么2：[原因1发生的原因？]
  ↓
为什么3：[原因2发生的原因？]
  ↓
为什么4：[原因3发生的原因？]
  ↓
为什么5：[根本原因？]

然后提出针对性解决方案。

输出格式：
完整的5层分析 + 解决方案建议。
"""
        }
    
    def _starburst(self, theme: str, **kwargs) -> Dict[str, Any]:
        """星爆法"""
        return {
            "method": "星爆法 (Starbursting)",
            "theme": theme,
            "instructions": f"""
星爆法探索任务：

主题：{theme}

回答6个核心问题，每个问题深入展开3个子问题：

- Who：谁？涉及谁？谁受益？
- What：什么？核心是什么？
- Where：哪里？在什么场景？
- When：何时？什么时机？
- Why：为什么？目的是什么？
- How：如何？怎么实现？

输出格式：
每个核心问题 + 3个子问题 + 回答。
"""
        }
    
    def _constraint_release(self, problem: str, constraints: str = "", **kwargs) -> Dict[str, Any]:
        """约束释放法"""
        return {
            "method": "约束释放法",
            "problem": problem,
            "constraints": constraints,
            "instructions": f"""
无约束头脑风暴任务：

问题：{problem}
当前约束：{constraints if constraints else "请列出当前约束"}

思考：
1. 预算无限制时会怎样？
2. 时间不是问题时会怎样？
3. 有任何技术时会怎样？
4. 没有历史包袱时会怎样？

然后：哪些点子可以缩小规模到现实？

输出格式：
1. 无约束场景下的点子
2. 可落地的缩小版本
"""
        }


class WorkflowRunner:
    """工作流运行器"""
    
    def run_product_innovation(self, product: str, user: str, pain: str) -> Dict[str, Any]:
        """产品创新工作流"""
        return {
            "workflow": "产品创新",
            "steps": [
                {
                    "step": "同理心",
                    "task": f"描述 {user} 的用户画像和 {pain} 痛点"
                },
                {
                    "step": "定义",
                    "task": f"形成HMW问题陈述：如何让 {user} 不再受 {pain} 困扰？"
                },
                {
                    "step": "创意",
                    "task": f"使用SCAMPER为 {product} 生成功能创新点子"
                },
                {
                    "step": "原型",
                    "task": "描述最小可行方案(MVP)"
                },
                {
                    "step": "测试",
                    "task": "设计验证计划"
                }
            ]
        }
    
    def run_problem_solving(self, problem: str) -> Dict[str, Any]:
        """问题解决工作流"""
        return {
            "workflow": "问题解决",
            "steps": [
                {
                    "step": "根因分析",
                    "task": f"使用5 Whys分析：{problem}"
                },
                {
                    "step": "风险识别",
                    "task": "使用逆向头脑风暴识别风险"
                },
                {
                    "step": "多角度分析",
                    "task": "使用六顶思考帽分析"
                },
                {
                    "step": "方案生成",
                    "task": "生成解决方案"
                },
                {
                    "step": "评估推荐",
                    "task": "评估并推荐最佳方案"
                }
            ]
        }
    
    def run_strategy_planning(self, org: str, state: str) -> Dict[str, Any]:
        """战略规划工作流"""
        return {
            "workflow": "战略规划",
            "steps": [
                {
                    "step": "现状分析",
                    "task": f"SWOT分析：{org} 的 {state}"
                },
                {
                    "step": "地平线规划",
                    "task": "三层地平线规划"
                },
                {
                    "step": "组合设计",
                    "task": "创新组合设计"
                },
                {
                    "step": "流程适配",
                    "task": "Stage-Gate流程适配"
                },
                {
                    "step": "指标定义",
                    "task": "关键指标定义"
                }
            ]
        }


def main():
    parser = argparse.ArgumentParser(
        description="创意生成器 - 头脑风暴脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # 基础参数
    parser.add_argument("--theme", type=str, help="头脑风暴主题")
    parser.add_argument("--count", type=int, default=10, help="生成点子数量")
    parser.add_argument("--target", type=str, help="SCAMPER目标")
    parser.add_argument("--decision", type=str, help="六顶思考帽决策")
    parser.add_argument("--problem", type=str, help="问题描述")
    parser.add_argument("--constraints", type=str, help="当前约束")
    
    # 方法参数
    parser.add_argument(
        "--method",
        type=str,
        choices=["classic", "scamper", "hats", "reverse", "5whys", "starburst", "constraint"],
        default="classic",
        help="头脑风暴方法"
    )
    
    # 工作流参数
    parser.add_argument("--workflow", type=str, choices=["product", "problem", "strategy"], help="场景化工作流")
    parser.add_argument("--product", type=str, help="产品名称（用于产品创新工作流）")
    parser.add_argument("--user", type=str, help="目标用户（用于产品创新工作流）")
    parser.add_argument("--pain", type=str, help="用户痛点（用于产品创新工作流）")
    parser.add_argument("--org", type=str, help="组织名称（用于战略规划工作流）")
    parser.add_argument("--state", type=str, help="当前状态（用于战略规划工作流）")
    
    # 输出格式
    parser.add_argument("--output", type=str, choices=["text", "json"], default="text", help="输出格式")
    
    args = parser.parse_args()
    
    # 处理工作流
    if args.workflow:
        runner = WorkflowRunner()
        if args.workflow == "product":
            if not all([args.product, args.user, args.pain]):
                print("错误：产品创新工作流需要 --product, --user, --pain 参数")
                sys.exit(1)
            result = runner.run_product_innovation(args.product, args.user, args.pain)
        elif args.workflow == "problem":
            if not args.problem:
                print("错误：问题解决工作流需要 --problem 参数")
                sys.exit(1)
            result = runner.run_problem_solving(args.problem)
        elif args.workflow == "strategy":
            if not all([args.org, args.state]):
                print("错误：战略规划工作流需要 --org, --state 参数")
                sys.exit(1)
            result = runner.run_strategy_planning(args.org, args.state)
    else:
        # 处理单次头脑风暴
        generator = BrainstormGenerator(args.method)
        kwargs = {
            "theme": args.theme,
            "count": args.count,
            "target": args.target,
            "decision": args.decision,
            "problem": args.problem,
            "constraints": args.constraints,
        }
        # 过滤 None 值
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        result = generator.generate(**kwargs)
    
    # 输出结果
    if args.output == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 60)
        print(f"创意生成器 - {result.get('method', result.get('workflow', 'Unknown'))}")
        print("=" * 60)
        print(result.get("instructions", ""))
        if "steps" in result:
            for i, step in enumerate(result["steps"], 1):
                print(f"\n步骤{i}: {step['step']}")
                print(f"  任务: {step['task']}")


if __name__ == "__main__":
    main()