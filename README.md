# 🤖 智能发票提取助手 - AI-Powered Invoice Extractor

> 基于强大的 DeepSeek R1 模型，打造的本地化智能化发票处理工具，让发票信息提取变得简单而准确！

> Based on the powerful DeepSeek R1 model, we have developed a locally intelligent invoice processing tool that makes invoice information extraction simple and accurate!

[![GitHub](https://img.shields.io/badge/GitHub-Travisma2233-blue?style=flat&logo=github)](https://github.com/Travisma2233)

## 项目描述 | Project Description

[English]

An intelligent invoice processing tool powered by the cutting-edge DeepSeek R1 Model. This advanced AI model, known for its superior understanding of Chinese text and document structures, automatically extracts and organizes information from Chinese VAT invoices with exceptional accuracy. The tool processes invoice PDFs and outputs structured data in CSV format, including processing date, invoice date, buyer/seller information, tax IDs, goods summary, and total amount. Perfect for businesses handling large volumes of invoices and needing efficient, accurate data extraction.

[中文]

一个智能化的发票处理工具，采用尖端的 DeepSeek R1模型。这个先进的 AI 模型以其出色的中文理解能力和文档结构分析能力而著称，能够以极高的准确度自动提取和整理中国增值税发票信息。本工具可处理PDF格式的发票，并将信息以CSV格式输出，包括处理日期、发票日期、购销方信息、税号、商品总结和总金额等关键信息。特别适合需要处理大量发票并要求高效、准确数据提取的企业使用。

[English](#english) | [中文](#chinese)

## English <a name="english"></a>

### 🎯 Introduction
Transform your invoice processing with the power of AI! This cutting-edge tool leverages Large Language Models (LLM) to intelligently extract information from Chinese VAT invoices with unprecedented accuracy. Say goodbye to manual data entry and hello to automated, intelligent invoice processing!

### 🌟 Why Choose This Tool?
- 🧠 **Powerful R1 Model**: Utilizes DeepSeek R1, a state-of-the-art LLM optimized for Chinese text processing
- 🚀 **Zero Configuration**: The R1 model understands invoice context automatically
- 🎯 **High Precision**: Smart recognition powered by advanced neural networks
- ⚡ **Batch Processing**: Handle multiple invoices in seconds
- 🛡️ **Local Processing**: All data processed locally with Ollama for maximum security

### 🔥 Key Features
- 🤖 **Intelligent Extraction**: Powered by Ollama's deepseek-r1 model
- 🎯 **Context-Aware**: Understands invoice layout and context
- 📊 **Smart Data Recognition**:
  - Automatic date parsing
  - Intelligent entity recognition
  - Smart amount calculation
  - Context-based goods categorization
- 💾 **Structured Output**: Clean, organized TXT format with the following fields:

| Field | Description |
|-------|-------------|
| 处理日期 | Processing Date |
| 发票日期 | Invoice Date |
| 购买方名称 | Buyer Name |
| 购买方税号 | Buyer Tax ID |
| 销售方名称 | Seller Name |
| 销售方税号 | Seller Tax ID |
| 商品总结 | Goods Summary |
| 总金额 | Total Amount |

### 🚀 Quick Start
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up the AI engine:
```bash
ollama pull deepseek-r1:8b
```

3. Prepare your files:
   - Create an `invoices` folder
   - Drop your PDF invoices in
   - Watch the magic happen!

4. Run the AI:
```bash
python invoice_reader.py
```

### 📂 Project Structure
```
.
├── invoices/           # Your invoice PDFs
├── output/            # AI-processed results
├── invoice_reader.py  # AI processing engine
└── requirements.txt   # Dependencies
```

## 中文 <a name="chinese"></a>

### 🎯 简介
让AI为您处理发票！本工具采用最新的大语言模型（LLM）技术，智能化提取增值税发票信息，实现前所未有的准确度。告别手动录入，拥抱智能化处理！

### 🌟 为什么选择本工具？
- 🧠 **强大的R1模型**: 采用 DeepSeek R1，专为中文处理优化的顶尖大语言模型
- 🚀 **零配置**: R1 模型自动理解发票上下文
- 🎯 **高精度**: 由先进神经网络支持的智能识别
- ⚡ **批量处理**: 秒级处理多张发票
- 🛡️ **本地处理**: 使用 Ollama 进行本地处理，确保数据安全

### 🔥 核心特性
- 🤖 **智能提取**: 由Ollama的deepseek-r1模型驱动
- 🎯 **上下文感知**: 自动理解发票布局和内容关系
- 📊 **智能数据识别**:
  - 自动解析日期格式
  - 智能实体识别
  - 智能金额计算
  - 基于上下文的商品分类
- 💾 **结构化输出**: 整洁有序的TXT格式，包含以下字段：

| 字段名 | 说明 | 示例 |
|--------|------|------|
| 处理日期 | 程序处理发票的日期 | 2024-03-20 |
| 发票日期 | 发票开具日期 | 2024-03-19 |
| 购买方名称 | 发票上的购买方名称 | XX科技有限公司 |
| 购买方税号 | 购买方的税号 | 121000004370964988 |
| 销售方名称 | 发票上的销售方名称 | XX贸易有限公司 |
| 销售方税号 | 销售方的税号 | 91320XXXXXXXXXX |
| 商品总结 | 发票商品的简要描述 | 钢材、清洁用品 |
| 总金额 | 发票的总金额 | 1234.56 |

### 🚀 快速开始
1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置AI引擎：
```bash
ollama pull deepseek-r1:8b
```

3. 准备文件：
   - 创建 `invoices` 文件夹
   - 放入PDF发票
   - 见证AI的魔力！

4. 运行AI：
```bash
python invoice_reader.py
```

### 📂 项目结构
```
.
├── invoices/           # 发票PDF文件
├── output/            # AI处理结果
├── invoice_reader.py  # AI处理引擎
└── requirements.txt   # 项目依赖
```

### 📝 注意事项
- 💫 本工具采用最新AI技术，确保最佳识别效果
- 🔒 所有处理均在本地完成，数据安全有保障
- 📄 支持标准增值税发票格式
- ⚙️ 需要安装并运行Ollama服务 
