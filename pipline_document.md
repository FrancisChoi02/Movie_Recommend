## 概述

论文作者提出了RAGAS（**R** etrieval **A** ugmented **G** eneration **As** sessment），一个无需人工标注的自动化评估检索增强生成系统的框架，用于评估RAG系统的多个维度，包括检索系统的能力、生成模块的忠实性以及生成内容的质量。

## 论文核心

作者通过引入忠实性、答案相关性和上下文相关性三个评估维度，使得RAGAs能够在无需人工标注的情况下快速评估RAG系统的表现

### 评估纬度

忠实性（Faithfulness）、答案相关性（Answer Relevance）和上下文相关性（Context Relevance）：

- **忠实性**：生成的答案是否基于给定的上下文，避免幻觉。
- **答案相关性**：生成的答案是否直接回答了问题。
- **上下文相关性**：检索的上下文是否聚焦于问题，避免冗余信息。

### 评估方法（基于不同纬度）

- **忠实性**：通过LLM提取生成答案中的陈述，并验证这些陈述是否可以从上下文中推断出来。
- **答案相关性**：通过LLM生成多个潜在问题，并计算这些问题与原始问题的相似度。
- **上下文相关性**：通过LLM提取上下文中与问题相关的句子，并计算这些句子占上下文总句子的比例。

虽然论文里，作者只提了三个指标，但在RAGAS的官方文档中，其实是有更多维度的指标：

- Faithfulness（忠实度）
- Answer relevancy（答案相关性）
- Context recall（上下文召回率）
- Context precision（上下文精确度）
- Context utilization（上下文利用度）
- Context entity recall（上下文实体召回率）
- Summarization Score（摘要得分）