

import pdfplumber
import re
from typing import List, Tuple, Dict, Any
import csv
from datetime import datetime
import os
import json
import requests

class InvoiceReader:
    def __init__(self, pdf_path: str, api_key: str = None):
        self.pdf_path = pdf_path
        self._text_cache = None
        self.api_key = api_key
        
    def _get_full_text(self) -> str:
        """获取发票的完整文本内容"""
        if self._text_cache is None:
            with pdfplumber.open(self.pdf_path) as pdf:
                self._text_cache = '\n'.join(page.extract_text() for page in pdf.pages)
                print("提取的完整文本：")
                print(self._text_cache)
        return self._text_cache

    def _call_llm_api(self, text: str) -> Dict[str, Any]:
        """
        调用Ollama本地模型API来分析发票文本
        """
        try:
            api_url = "http://localhost:11434/api/generate"
            
            prompt = f"""Human: 你是一个专业的发票信息提取助手。请仔细分析下面的发票文本，并提取关键信息。请只返回一个JSON对象，不要包含任何其他内容。不要解释，不要加入额外的标点符号。

发票文本内容：
{text}

请注意以下提取规则：
1. 发票日期在"开票日期"后面
2. 购买方名称在"买 名 称"后面
3. 购买方税号需要提取，购买方税号是"统一社会信用代码/纳税人识别号"后面的15-20位数字和字母组合
4. 销售方名称在"售 名 称"后面
5. 销售方税号需要提取，销售方税号是"统一社会信用代码/纳税人识别号"后面的15-20位数字和字母组合
6. 商品信息在"项目名称"下面，包括每个商品的名称和金额
7. 总金额在"价税合计(小写)"后面，以¥开头
8. 商品总结：用一两个词简单描述商品，不要使用学术的语言要尽可能简单易懂，例如：
   - 如果是金属制品，就写"钢材"
   - 如果是清洁用品，就写"清洁用品"
   - 如果是布制品，就写"布制品"
   - 如果有多种商品，用顿号分隔，如"钢材、清洁用品"

直接返回以下格式的JSON，不要有任何其他内容：
{{
    "发票日期": "YYYY-MM-DD",
    "购买方名称": "",
    "购买方税号": "",
    "销售方名称": "",
    "销售方税号": "",
    "商品信息": [
        {{"名称": "", "金额": ""}}
    ],
    "总金额": "",
    "商品总结": ""  // 简单描述，如"钢材"、"清洁用品"等
}}"""

            response = requests.post(
                api_url,
                json={
                    "model": self.api_key,
                    "prompt": prompt,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                try:
                    response_text = result.get('response', '')
                    print("\n模型原始输出：")
                    print(response_text)
                    
                    # 尝试找到JSON部分
                    start = response_text.find('{')
                    end = response_text.rfind('}') + 1
                    
                    if start != -1 and end != -1:
                        json_str = response_text[start:end]
                        print("\n提取的JSON字符串：")
                        print(json_str)
                        
                        try:
                            parsed_result = json.loads(json_str)
                            print("\nJSON解析成功")
                            return parsed_result
                        except json.JSONDecodeError as e:
                            print(f"\nJSON解析错误，尝试清理JSON字符串")
                            # 清理JSON字符串
                            json_str = json_str.strip()
                            json_str = re.sub(r'[\n\r\t]', '', json_str)
                            json_str = re.sub(r',\s*}', '}', json_str)
                            print("\n清理后的JSON字符串：")
                            print(json_str)
                            
                            try:
                                parsed_result = json.loads(json_str)
                                print("\nJSON解析成功")
                                return parsed_result
                            except json.JSONDecodeError as e:
                                print(f"\n清理后仍然无法解析JSON：{str(e)}")
                                return self._process_by_rules(text)
                    else:
                        print("\n无法在响应中找到JSON格式的内容，使用规则方式处理")
                        return self._process_by_rules(text)
                        
                except Exception as e:
                    print(f"\n处理模型响应时出错：{str(e)}，使用规则方式处理")
                    return self._process_by_rules(text)
            else:
                print(f"\nAPI调用失败: {response.status_code}")
                print("错误信息:", response.text)
                return self._process_by_rules(text)
                
        except Exception as e:
            print(f"调用Ollama API时出错: {str(e)}")
            return {}

    def process_info(self) -> dict:
        """
        处理发票信息：先提取文本，然后使用语言模型分析
        """
        # 获取完整文本
        text = self._get_full_text()
        
        # 如果没有提供API密钥，使用规则方式处理
        if not self.api_key:
            print("未提供API密钥，使用规则方式处理...")
            return self._process_by_rules(text)
        
        # 使用语言模型处理
        print("使用语言模型处理发票信息...")
        return self._call_llm_api(text)

    def _process_by_rules(self, text: str) -> dict:
        """
        使用规则方式处理文本（作为备选方案）
        """
        # 提取日期
        pattern_date = r'开票日期[:：]?\s*(\d{4}年\d{1,2}月\d{1,2}日)'
        
        # 提取购买方和销售方信息（更精确的匹配）
        pattern_buyer = r'买.*?名\s*称\s*[:：]?\s*([^方\n]+).*?统一社会信用代码/纳税人识别号\s*[:：]?\s*(121000004370964988)'
        pattern_seller = r'售.*?名\s*称\s*[:：]?\s*([^方\n]+).*?统一社会信用代码/纳税人识别号\s*[:：]?\s*([0-9A-Z]{15,20})'
        
        # 分别在购买方和销售方部分查找
        buyer_section = text[text.find('买'):text.find('售')]
        seller_section = text[text.find('售'):]
        
        # 提取购买方信息
        buyer_match = re.search(pattern_buyer, buyer_section, re.DOTALL)
        if buyer_match:
            buyer_name = buyer_match.group(1).strip()
            buyer_tax = buyer_match.group(2)  # 直接使用匹配到的税号
        else:
            # 如果没有匹配到完整模式，尝试单独提取名称和税号
            buyer_name_match = re.search(r'买.*?名\s*称\s*[:：]?\s*([^方\n]+)', buyer_section, re.DOTALL)
            buyer_name = buyer_name_match.group(1).strip() if buyer_name_match else ''
            buyer_tax = "121000004370964988"  # 固定使用此税号
            
        # 提取销售方信息
        seller_match = re.search(pattern_seller, seller_section, re.DOTALL)
        if seller_match:
            seller_name = seller_match.group(1).strip()
            seller_tax = seller_match.group(2)
        else:
            seller_name = ''
            seller_tax = ''
        
        # 提取日期
        date_match = re.search(pattern_date, text)
        invoice_date = ''
        if date_match:
            date_str = date_match.group(1)
            invoice_date = date_str.replace('年', '-').replace('月', '-').replace('日', '')
        
        # 提取总金额
        pattern_total = r'\(小写\)\s*[¥￥]?(\d+\.\d{2})'
        total_match = re.search(pattern_total, text)
        total_amount = total_match.group(1) if total_match else '0.00'  # 直接使用字符串
        
        # 提取商品信息
        items = self._extract_items_by_rules(text)
        
        # 生成简单的商品总结
        goods_summary = self._generate_goods_summary(items)
        
        # 调试输出
        print(f"\n提取的信息：")
        print(f"购买方名称: {buyer_name}")
        print(f"购买方税号: {buyer_tax}")
        print(f"销售方名称: {seller_name}")
        print(f"销售方税号: {seller_tax}")
        print(f"发票日期: {invoice_date}")
        print(f"总金额: {total_amount}")
        print(f"商品总结: {goods_summary}")
        
        return {
            "发票日期": invoice_date,
            "购买方名称": buyer_name,
            "购买方税号": buyer_tax,
            "销售方名称": seller_name,
            "销售方税号": seller_tax,
            "商品信息": items,
            "总金额": total_amount,
            "商品总结": goods_summary
        }

    def _generate_goods_summary(self, items: List[Dict[str, Any]]) -> str:
        """生成简单的商品总结"""
        if not items:
            return "无商品信息"
            
        # 提取所有商品名称中的关键词
        keywords = set()
        for item in items:
            name = item["名称"].lower()
            if "金属" in name or "钢材" in name:
                keywords.add("钢材")
            elif "清洁" in name or "洗涤" in name:
                keywords.add("清洁用品")
            elif "纺织" in name or "布" in name:
                keywords.add("布制品")
            else:
                keywords.add("其他")
        
        # 将关键词组合成简单描述
        summary = "、".join(sorted(keywords))
        return summary

    def _extract_items_by_rules(self, text: str) -> List[Dict[str, Any]]:
        """使用规则提取商品信息"""
        items = []
        # 匹配商品信息（更精确的匹配）
        pattern = r'\*([^*]+)\*([^\n]+?)\s+(\d+)\s+米\s+([\d.]+)\s+([\d.]+)'
        matches = re.finditer(pattern, text)
        
        for match in matches:
            category = match.group(1).strip()
            name = match.group(2).strip()
            quantity = match.group(3)  # 直接使用字符串
            unit_price = match.group(4)  # 直接使用字符串
            amount = match.group(5)  # 直接使用字符串
            
            # 只添加正数金额的商品
            if not amount.startswith('-'):  # 检查字符串是否以负号开头
                items.append({
                    "名称": f"{category}-{name}",
                    "数量": quantity,  # 直接使用字符串
                    "单价": unit_price,  # 直接使用字符串
                    "金额": amount  # 直接使用字符串
                })
        
        return items

    def _extract_total_amount_by_rules(self, text: str) -> str:  # 修改返回类型为str
        """使用规则提取总金额"""
        pattern = r'价税合计.*?\(小写\)\s*[¥￥](\d+\.\d{2})'
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1) if match else '0.00'  # 返回字符串
    
    def save_to_csv(self, output_path: str):
        """
        将处理后的信息保存到CSV文件
        """
        # 获取处理后的信息
        print("\n开始处理发票信息...")
        info = self.process_info()
        
        print("\n处理后的信息：")
        print(json.dumps(info, ensure_ascii=False, indent=2))
        
        # 准备CSV数据，所有数字都保持为字符串
        data = {
            '处理日期': datetime.now().strftime('%Y-%m-%d'),
            '发票日期': info.get('发票日期', ''),
            '购买方名称': info.get('购买方名称', ''),
            '购买方税号': info.get('购买方税号', ''),  # 已经是字符串
            '销售方名称': info.get('销售方名称', ''),
            '销售方税号': info.get('销售方税号', ''),  # 已经是字符串
            '商品总结': info.get('商品总结', ''),
            '总金额': info.get('总金额', '0.00')  # 直接使用字符串
        }
        
        print("\n准备写入CSV的数据：")
        for key, value in data.items():
            print(f"{key}: {value}")
        
        # 写入CSV文件
        try:
            file_exists = os.path.exists(output_path)
            with open(output_path, 'a', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=data.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(data)
            print(f"\nCSV文件写入成功：{output_path}")
        except Exception as e:
            print(f"\nCSV文件写入失败：{str(e)}")
            raise

def main():
    # 设置路径
    input_folder = "./invoices"  # PDF文件所在文件夹
    output_csv = "./output/invoice_records.csv"
    
    # 设置要使用的Ollama模型名称
    model_name = "deepseek-r1:8b"
    
    try:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        
        # 获取文件夹中所有的PDF文件
        pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            print(f"在文件夹 {input_folder} 中没有找到PDF文件")
            return
            
        print(f"找到 {len(pdf_files)} 个PDF文件")
        
        # 处理每个PDF文件
        for i, pdf_file in enumerate(pdf_files, 1):
            pdf_path = os.path.join(input_folder, pdf_file)
            print(f"\n处理第 {i}/{len(pdf_files)} 个文件: {pdf_file}")
            
            try:
                # 创建处理器实例
                processor = InvoiceReader(pdf_path, api_key=model_name)
                
                # 保存到CSV
                processor.save_to_csv(output_csv)
                print(f"文件 {pdf_file} 的信息已保存到：{output_csv}")
                
            except Exception as e:
                print(f"处理文件 {pdf_file} 时出错：{str(e)}")
                continue  # 继续处理下一个文件
        
        print("\n所有文件处理完成！")
        
    except Exception as e:
        print(f"程序执行出错：{str(e)}")

if __name__ == "__main__":
    main() 