---
title: Post-Training and Fine-Tuning
date: 2026-08-1 22:57:24
tags: ["LLM","微调","Post-Traning","Fine-Tuning"]
categories: ["大模型算法"]
---

**`Post-Trianing` 流程**
```bash
预训练模型 Base Model

        ↓

1. SFT 指令微调
        ↓

2. 偏好对齐
   RLHF / DPO / IPO 等
        ↓

3. 能力强化
   推理、工具调用、代码、Agent等
        ↓

4. 安全和行为优化
        ↓

最终 Instruct / Chat Model
```

**`Post-Trianing` 常见方式**
- SFT（Supervised Fine-Tuning，监督微调）
  - 全量 SFT : 更新所有参数
  - LoRA SFT : 冻结模型+训练LoRA
    ```
    输入
    ↓
    模型
    ↓
    预测标准答案
    ↓
    计算loss
    ↓
    更新参数
    ```
- RLHF（Reinforcement Learning from Human Feedback）：强化学习人类反馈。
  - SFT
     ```
        Base Model
             ↓
        SFT Model
    ```
  - 训练奖励模型 Reward Model
  - 强化学习 PPO
    ```
    回答
    ↓
    Reward Model
    ↓
    分数
    ```
- DPO（Direct Preference Optimization）:不训练奖励模型，直接用偏好数据优化模型。
  ```
  {
    "prompt":"写邮件",
    "chosen":"好的邮件",
    "rejected":"差的邮件"
  }
  ```
- IPO / KTO / ORPO 等偏好优化, DPO的拓展
- Continued Pretraining（持续预训练）： 让模型学习新的领域知识。
- Instruction Tuning（指令调优）
- Reasoning Fine-tuning（推理微调）: 学习思考过程
    ```
    {
    "question":"一个数学问题",
    "reasoning":"步骤",
    "answer":"结果"
    }
    ```
- Tool / Agent Fine-tuning ： 训练模型使用工具。
    ```
    {
    "name":"search",
    "arguments":{
    "query":"天气"
    }
    }
    ```
- 多模态后训练（VLM）
  - Vision SFT
  - Visual Preference Alignment



## SFT （Supervised Fine-Tuning，监督微调）

    通过人工构造的高质量输入-输出示例，使预训练模型学习遵循指令、完成特定任务，并形成符合人类期望的交互行为。

**训练数据**：
```
{
  "instruction": "解释什么是光合作用",
  "output": "光合作用是植物利用光能..."
}
```
**本质**: 语言模型训练
```
输入
 ↓
模型
 ↓
预测答案
 ↓
计算预测答案与标准答案差异
 ↓
更新参数
```

