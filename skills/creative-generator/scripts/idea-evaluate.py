#!/usr/bin/env python3
"""
创意评估器 - 多维度评估创意价值
支持可行性、影响力、工作量、风险等多维度评分
"""

import argparse
import json
import sys
from datetime import datetime
from typing import List, Dict, Any, Tuple


class IdeaEvaluator:
    """创意评估器"""
    
    def __init__(self):
        self.dimensions = {
            "feasibility": {
                "name": "可行性",
                "description": "技术上能实现吗？",
                "weight": 1.0,
                "scoring": {
                    5: "现有技术完全支持",
                    4: "需要少量技术开发",
                    3: "需要中等技术开发",
                    2: "需要大量技术开发",
                    1: "技术不成熟或不可行"
                }
            },
            "impact": {
                "name": "影响力",
                "description": "能带来多大价值？",
                "weight": 1.2,
                "scoring": {
                    5: "颠覆性影响，显著提升核心竞争力",
                    4: "重要影响，显著提升用户体验或效率",
                    3: "中等影响，有明显改进",
                    2: "较小影响，边际改进",
                    1: "影响微弱或难以衡量"
                }
            },
            "effort": {
                "name": "工作量",
                "description": "需要多少努力？（分数越高越好，表示工作量越低）",
                "weight": 0.8,
                "scoring": {
                    5: "1周内可完成",
                    4: "1-4周可完成",
                    3: "1-3个月可完成",
                    2: "3-6个月可完成",
                    1: "超过6个月或需要大量资源"
                }
            },
            "risk": {
                "name": "风险",
                "description": "失败可能性？（分数越高越好，表示风险越低）",
                "weight": 0.9,
                "scoring": {
                    5: "风险极低，几乎必定成功",
                    4: "风险较低，成功概率高",
                    3: "中等风险，有一定不确定性",
                    2: "风险较高，需要谨慎",
                    1: "风险很高，失败可能性大"
                }
            }
        }
    
    def evaluate_single_idea(
        self,
        idea: str,
        scores: Dict[str, int] = None,
        notes: str = ""
    ) -> Dict[str, Any]:
        """评估单个创意"""
        if scores is None:
            # 返回评估模板
            return {
                "idea": idea,
                "status": "待评估",
                "instructions": self._generate_evaluation_instructions(idea)
            }
        
        # 计算加权总分
        total_score = 0
        total_weight = 0
        dimension_scores = {}
        
        for dim_key, dim_info in self.dimensions.items():
            score = scores.get(dim_key, 3)
            weight = dim_info["weight"]
            weighted_score = score * weight
            total_score += weighted_score
            total_weight += weight
            dimension_scores[dim_key] = {
                "name": dim_info["name"],
                "score": score,
                "weighted_score": round(weighted_score, 2),
                "description": dim_info["scoring"].get(score, "")
            }
        
        final_score = round(total_score / total_weight, 2)
        
        return {
            "idea": idea,
            "status": "已评估",
            "total_score": final_score,
            "dimension_scores": dimension_scores,
            "notes": notes,
            "recommendation": self._get_recommendation(final_score)
        }
    
    def evaluate_multiple_ideas(
        self,
        ideas: List[str],
        scores_list: List[Dict[str, int]] = None,
        notes_list: List[str] = None
    ) -> Dict[str, Any]:
        """评估多个创意"""
        if scores_list is None:
            # 返回批量评估模板
            return {
                "status": "待评估",
                "ideas_count": len(ideas),
                "ideas": ideas,
                "instructions": self._generate_batch_evaluation_instructions(ideas)
            }
        
        # 评估每个创意
        evaluated_ideas = []
        for i, idea in enumerate(ideas):
            scores = scores_list[i] if i < len(scores_list) else {}
            notes = notes_list[i] if notes_list and i < len(notes_list) else ""
            evaluated_ideas.append(self.evaluate_single_idea(idea, scores, notes))
        
        # 排序
        sorted_ideas = sorted(
            [idea for idea in evaluated_ideas if idea["status"] == "已评估"],
            key=lambda x: x["total_score"],
            reverse=True
        )
        
        return {
            "status": "已评估",
            "total_ideas": len(ideas),
            "evaluated_ideas": len(sorted_ideas),
            "ranking": sorted_ideas,
            "summary": self._generate_summary(sorted_ideas)
        }
    
    def generate_matrix(self, ideas: List[str]) -> str:
        """生成评估矩阵（用于手动填写）"""
        matrix = [
            "| 创意 | 可行性(1-5) | 影响力(1-5) | 工作量(1-5) | 风险(1-5) | 备注 |",
            "|------|-------------|-------------|-------------|-----------|------|"
        ]
        
        for idea in ideas:
            matrix.append(f"| {idea} | | | | | |")
        
        return "\n".join(matrix)
    
    def _generate_evaluation_instructions(self, idea: str) -> str:
        """生成评估指导"""
        instructions = f"""
请为以下创意评分（1-5分）：

创意：{idea}

评分标准：
"""
        for dim_key, dim_info in self.dimensions.items():
            instructions += f"\n{dim_info['name']} ({dim_info['description']}):\n"
            for score, desc in dim_info["scoring"].items():
                instructions += f"  {score}分: {desc}\n"
        
        instructions += f"""
输出格式（JSON）：
{{
  "feasibility": [1-5],
  "impact": [1-5],
  "effort": [1-5],
  "risk": [1-5],
  "notes": "评估备注"
}}
"""
        return instructions
    
    def _generate_batch_evaluation_instructions(self, ideas: List[str]) -> str:
        """生成批量评估指导"""
        instructions = f"""
请为以下 {len(ideas)} 个创意评分：

"""
        for i, idea in enumerate(ideas, 1):
            instructions += f"{i}. {idea}\n"
        
        instructions += f"""
评分维度（1-5分）：
- 可行性：技术上能实现吗？
- 影响力：能带来多大价值？
- 工作量：需要多少努力？（分数越高表示工作量越低）
- 风险：失败可能性？（分数越高表示风险越低）

输出格式（JSON数组）：
[
  {{
    "idea": "创意1",
    "scores": {{"feasibility": 4, "impact": 3, "effort": 4, "risk": 4}},
    "notes": "备注"
  }},
  ...
]
"""
        return instructions
    
    def _get_recommendation(self, score: float) -> str:
        """根据分数给出建议"""
        if score >= 4.5:
            return "强烈推荐：优先实施"
        elif score >= 4.0:
            return "推荐：应优先考虑"
        elif score >= 3.5:
            return "中性：可以作为备选"
        elif score >= 3.0:
            return "谨慎：需要进一步评估"
        else:
            return "暂缓：当前不适合实施"
    
    def _generate_summary(self, sorted_ideas: List[Dict]) -> str:
        """生成总结"""
        if not sorted_ideas:
            return "暂无已评估创意"
        
        top_3 = sorted_ideas[:3]
        summary = f"Top 3 创意：\n"
        for i, idea in enumerate(top_3, 1):
            summary += f"  {i}. {idea['idea']} (得分: {idea['total_score']})\n"
        
        avg_score = sum(idea["total_score"] for idea in sorted_ideas) / len(sorted_ideas)
        summary += f"\n平均得分: {round(avg_score, 2)}"
        
        return summary


def main():
    parser = argparse.ArgumentParser(
        description="创意评估器 - 多维度评估创意价值",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # 输入参数
    parser.add_argument("--ideas", type=str, help="创意列表（逗号分隔）")
    parser.add_argument("--idea-file", type=str, help="创意文件（每行一个）")
    
    # 评分参数
    parser.add_argument("--scores", type=str, help="评分JSON（格式：[{\"feasibility\":4,...},...]）")
    
    # 输出格式
    parser.add_argument("--output", type=str, choices=["text", "json", "matrix"], default="text", help="输出格式")
    
    # 操作类型
    parser.add_argument("--action", type=str, choices=["evaluate", "template", "matrix"], default="evaluate", help="操作类型")
    
    args = parser.parse_args()
    
    # 获取创意列表
    ideas = []
    if args.ideas:
        ideas = [idea.strip() for idea in args.ideas.split(",") if idea.strip()]
    elif args.idea_file:
        try:
            with open(args.idea_file, "r", encoding="utf-8") as f:
                ideas = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"错误：无法读取文件 {args.idea_file}: {e}")
            sys.exit(1)
    
    if not ideas:
        print("错误：请提供创意列表 (--ideas 或 --idea-file)")
        sys.exit(1)
    
    evaluator = IdeaEvaluator()
    
    # 执行操作
    if args.action == "template":
        # 输出评估模板
        if len(ideas) == 1:
            result = evaluator.evaluate_single_idea(ideas[0])
            print(result["instructions"])
        else:
            result = evaluator.evaluate_multiple_ideas(ideas)
            print(result["instructions"])
    
    elif args.action == "matrix":
        # 输出评估矩阵
        print(evaluator.generate_matrix(ideas))
    
    else:  # evaluate
        # 解析评分
        scores_list = None
        if args.scores:
            try:
                scores_list = json.loads(args.scores)
            except json.JSONDecodeError as e:
                print(f"错误：无效的JSON格式: {e}")
                sys.exit(1)
        
        # 执行评估
        if len(ideas) == 1:
            result = evaluator.evaluate_single_idea(ideas[0], scores_list[0] if scores_list else None)
        else:
            result = evaluator.evaluate_multiple_ideas(ideas, scores_list)
        
        # 输出结果
        if args.output == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("=" * 60)
            print("创意评估结果")
            print("=" * 60)
            
            if "ranking" in result:
                print(f"\n共评估 {result['total_ideas']} 个创意\n")
                for i, idea in enumerate(result["ranking"], 1):
                    print(f"第{i}名: {idea['idea']}")
                    print(f"  总分: {idea['total_score']}")
                    print(f"  建议: {idea['recommendation']}")
                    print()
                print(result["summary"])
            elif "total_score" in result:
                print(f"\n创意: {result['idea']}")
                print(f"总分: {result['total_score']}")
                print(f"建议: {result['recommendation']}")
                print("\n维度评分:")
                for dim_key, dim_data in result["dimension_scores"].items():
                    print(f"  {dim_data['name']}: {dim_data['score']}分 - {dim_data['description']}")


if __name__ == "__main__":
    main()