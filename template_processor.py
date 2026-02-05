from jinja2 import Environment, meta
import re
import json


class TemplateProcessor:
    """Jinja2模板处理器"""
    
    def __init__(self):
        # 创建带自定义函数的环境
        self.env = Environment()
        # 添加自定义函数
        self.env.globals['raise_exception'] = self._raise_exception
        
        # 添加自定义过滤器
        self.env.filters['trim'] = lambda x: x.strip() if isinstance(x, str) else x
        self.env.filters['format_number'] = self._format_number
        self.env.filters['format_currency'] = self._format_currency
        
    def extract_variables(self, template_content):
        """
        从模板内容中提取变量名
        
        Args:
            template_content (str): 模板字符串
            
        Returns:
            list: 变量名列表
        """
        try:
            # 解析模板获取变量
            ast = self.env.parse(template_content)
            variables = meta.find_undeclared_variables(ast)
            return sorted(list(variables))
        except Exception as e:
            # 如果解析失败，尝试通过正则表达式提取
            return self._extract_variables_regex(template_content)
    
    def _extract_variables_regex(self, template_content):
        """
        使用正则表达式提取变量（备用方案）
        
        Args:
            template_content (str): 模板字符串
            
        Returns:
            list: 变量名列表
        """
        # 匹配 {{ variable }} 格式的变量
        pattern = r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}'
        variables = re.findall(pattern, template_content)
        
        # 匹配 {% for item in list %} 中的变量
        for_pattern = r'\{%\s*for\s+[a-zA-Z_][a-zA-Z0-9_]*\s+in\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*%\}'
        for_vars = re.findall(for_pattern, template_content)
        variables.extend(for_vars)
        
        # 匹配 {% if condition %} 中的变量
        if_pattern = r'\{%\s*if\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:==|!=|>|<|>=|<=).*?\s*%\}'
        if_vars = re.findall(if_pattern, template_content)
        variables.extend(if_vars)
        
        # 去重并排序
        return sorted(list(set(variables)))
    
    def render_template(self, template_content, variables):
        """
        渲染模板
        
        Args:
            template_content (str): 模板字符串
            variables (dict): 变量字典
            
        Returns:
            str: 渲染后的文本
        """
        try:
            # 使用环境创建模板以支持自定义函数
            template = self.env.from_string(template_content)
            return template.render(**variables)
        except Exception as e:
            raise Exception(f"模板渲染错误: {str(e)}")
    
    def validate_json_data(self, json_string):
        """
        验证JSON数据格式
        
        Args:
            json_string (str): JSON字符串
            
        Returns:
            tuple: (是否有效, 解析后的数据或错误信息)
        """
        try:
            data = json.loads(json_string)
            return True, data
        except json.JSONDecodeError as e:
            return False, f"JSON格式错误: {str(e)}"
    
    def merge_data_sources(self, form_data, json_data):
        """
        合并表单数据和JSON数据
        
        Args:
            form_data (dict): 表单数据
            json_data (dict): JSON数据
            
        Returns:
            dict: 合并后的数据
        """
        merged_data = {}
        
        # 先添加表单数据
        merged_data.update(form_data)
        
        # 再添加JSON数据（覆盖同名字段）
        merged_data.update(json_data)
        
        return merged_data
    
    def _raise_exception(self, message):
        """抛出异常的辅助函数"""
        raise Exception(message)
    
    def _format_number(self, value):
        """格式化数字显示"""
        if isinstance(value, (int, float)):
            return f"{value:,}"
        return str(value)
    
    def _format_currency(self, value):
        """格式化货币显示"""
        if isinstance(value, (int, float)):
            return f"{value:,.2f}"
        return str(value)