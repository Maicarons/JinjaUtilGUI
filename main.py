import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, Menu
import json
import os
import webbrowser
from datetime import datetime
from template_processor import TemplateProcessor
from i18n import _, set_language, get_supported_languages, i18n_manager


class JinjaTemplateGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("JinjaUtilGUI")
        self.root.geometry("800x600")
        
        # 初始化变量
        self.template_content = ""
        self.template_vars = {}
        self.current_file = None
        self.processor = TemplateProcessor()
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建主界面
        self.setup_ui()
        
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        self.file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label=_("File"), menu=self.file_menu)
        self.file_menu.add_command(label=_("Open"), command=self.select_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label=_("Export"), command=self.export_result, accelerator="Ctrl+E")
        self.file_menu.add_separator()
        self.file_menu.add_command(label=_("Close File"), command=self.close_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=_("Exit"), command=self.root.quit, accelerator="Alt+F4")
        
        # 语言菜单
        self.lang_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label=_("Language"), menu=self.lang_menu)
        self.populate_language_menu()
        
        # 关于菜单
        self.about_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label=_("About"), menu=self.about_menu)
        self.about_menu.add_command(label=_("About Project"), command=self.show_about)
        self.about_menu.add_command(label=_("Project Address"), command=self.open_project_url)
        self.about_menu.add_command(label=_("Documentation"), command=self.open_documentation)
        
        # 绑定快捷键
        self.root.bind('<Control-o>', lambda e: self.select_file())
        self.root.bind('<Control-e>', lambda e: self.export_result())
        
    def populate_language_menu(self):
        """填充语言菜单"""
        self.lang_menu.delete(0, tk.END)  # 清空现有菜单项
        supported_langs = get_supported_languages()
        for lang_code, lang_name in supported_langs.items():
            self.lang_menu.add_command(
                label=lang_name,
                command=lambda lc=lang_code: self.change_language(lc)
            )
    
    def change_language(self, lang_code):
        """切换语言"""
        if set_language(lang_code):
            # 重新创建菜单栏以更新翻译
            self.create_menu_bar()
            # 更新窗口标题
            self.root.title("JinjaUtilGUI")
            # 更新界面文本
            self.update_ui_texts()
            # 标记等待重启状态
            self.mark_pending_restart()
            # 重启程序
            self.restart_program()
    
    def update_ui_texts(self):
        """更新界面文本"""
        # 更新标签框架文本
        for child in self.root.winfo_children():
            if isinstance(child, ttk.Frame):
                self.update_widget_texts(child)
    
    def update_widget_texts(self, widget):
        """递归更新控件文本"""
        # 更新LabelFrame文本
        if isinstance(widget, ttk.LabelFrame):
            current_text = str(widget.cget('text'))
            text_mapping = {
                "Template File": _("Template File"),
                "Variable Data": _("Variable Data"),
                "Generated Result": _("Generated Result")
            }
            if current_text in text_mapping:
                widget.configure(text=text_mapping[current_text])
        
        # 更新按钮文本
        elif isinstance(widget, ttk.Button):
            current_text = str(widget.cget('text'))
            text_mapping = {
                "Select File": _("Select File"),
                "Reload": _("Reload"),
                "Generate JSON Template": _("Generate JSON Template"),
                "Clear JSON": _("Clear JSON"),
                "Generate Text": _("Generate Text"),
                "Save Result": _("Save Result"),
                "Clear All": _("Clear All")
            }
            if current_text in text_mapping:
                widget.configure(text=text_mapping[current_text])
        
        # 递归处理子控件
        for child in widget.winfo_children():
            self.update_widget_texts(child)
    
    def setup_ui(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # 文件选择区域
        self.create_file_selection(main_frame)
        
        # 分隔线
        ttk.Separator(main_frame, orient='horizontal').grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # 数据输入区域
        self.create_data_input(main_frame)
        
        # 分隔线
        ttk.Separator(main_frame, orient='horizontal').grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # 结果显示区域
        self.create_result_display(main_frame)
        
        # 操作按钮区域
        self.create_action_buttons(main_frame)
        
    def create_file_selection(self, parent):
        # 文件选择框架
        file_frame = ttk.LabelFrame(parent, text="模板文件", padding="5")
        file_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        file_frame.columnconfigure(1, weight=1)
        
        # 文件路径显示
        ttk.Label(file_frame, text="当前文件:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.file_path_var = tk.StringVar(value="未选择文件")
        file_label = ttk.Label(file_frame, textvariable=self.file_path_var)
        file_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # 按钮框架
        button_frame = ttk.Frame(file_frame)
        button_frame.grid(row=0, column=2, padx=5)
        
        ttk.Button(button_frame, text="选择文件", command=self.select_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="重新加载", command=self.reload_template).pack(side=tk.LEFT, padx=2)
        
    def create_data_input(self, parent):
        # 数据输入框架
        data_frame = ttk.LabelFrame(parent, text=_("Variable Data"), padding="5")
        data_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        data_frame.columnconfigure(0, weight=1)
        data_frame.rowconfigure(0, weight=1)
        
        # 创建notebook用于多标签页
        self.data_notebook = ttk.Notebook(data_frame)
        self.data_notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 表单输入标签页
        self.form_frame = ttk.Frame(self.data_notebook)
        self.data_notebook.add(self.form_frame, text=_("Form Input"))
        self.form_frame.columnconfigure(0, weight=1)
        self.form_frame.rowconfigure(0, weight=1)
        
        # 表单内容框架
        form_content = ttk.Frame(self.form_frame)
        form_content.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        form_content.columnconfigure(1, weight=1)
        
        # 滚动区域
        canvas = tk.Canvas(form_content)
        scrollbar = ttk.Scrollbar(form_content, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # JSON输入标签页
        json_frame = ttk.Frame(self.data_notebook)
        self.data_notebook.add(json_frame, text="JSON输入")
        json_frame.columnconfigure(0, weight=1)
        json_frame.rowconfigure(0, weight=1)
        
        # JSON文本框
        self.json_text = scrolledtext.ScrolledText(json_frame, height=15)
        self.json_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # JSON操作按钮框架
        json_button_frame = ttk.Frame(json_frame)
        json_button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Button(json_button_frame, text="生成JSON模板", command=self.generate_json_template).pack(side=tk.LEFT, padx=5)
        ttk.Button(json_button_frame, text="清空JSON", command=lambda: self.json_text.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
        
        # 绑定JSON文本变化事件
        self.json_text.bind('<KeyRelease>', self.on_json_change)
        
    def create_result_display(self, parent):
        # 结果显示框架
        result_frame = ttk.LabelFrame(parent, text="生成结果", padding="5")
        result_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        # 结果文本框
        self.result_text = scrolledtext.ScrolledText(result_frame, height=15)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
    def create_action_buttons(self, parent):
        # 按钮框架（精简版）
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=5, column=0, columnspan=3, pady=10)
        
        # 保留核心功能按钮
        ttk.Button(button_frame, text=_("Generate Text"), command=self.generate_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=_("Export Variables"), command=self.export_variables_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=_("Export Complete"), command=self.export_complete_package).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=_("Clear All"), command=self.clear_all).pack(side=tk.LEFT, padx=5)
        
    def select_file(self):
        """选择模板文件"""
        file_path = filedialog.askopenfilename(
            title=_("Select Jinja2 Template File"),
            filetypes=[
                (_("Template Files"), "*.j2 *.tpl *.tmpl *.txt *.jinja"),
                (_("All Files"), "*.*")
            ]
        )
        
        if file_path:
            self.load_template(file_path)
    
    def export_result(self):
        """导出结果（菜单功能）"""
        self.save_result()
    
    def export_variables_json(self):
        """导出变量为JSON格式"""
        if not hasattr(self, 'template_vars') or not self.template_vars:
            messagebox.showwarning("警告", "没有可导出的变量")
            return
        
        # 收集变量数据
        variables_data = {}
        for var_name, var_value in self.template_vars.items():
            value = var_value.get().strip()
            if value:
                variables_data[var_name] = self._convert_value(value)
            else:
                variables_data[var_name] = None
        
        if not any(v is not None for v in variables_data.values()):
            messagebox.showwarning("警告", "请先填写变量值")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="导出变量JSON",
            defaultextension=".json",
            filetypes=[
                ("JSON文件", "*.json"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(variables_data, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("成功", f"变量已导出到: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {str(e)}")
    
    def export_complete_package(self):
        """导出完整包（变量JSON + 生成结果）"""
        result_text = self.result_text.get(1.0, tk.END).strip()
        if not result_text:
            messagebox.showwarning("警告", "请先生成结果再导出")
            return
        
        if not hasattr(self, 'template_vars') or not self.template_vars:
            messagebox.showwarning("警告", "没有可导出的变量")
            return
        
        # 创建导出目录
        directory = filedialog.askdirectory(title="选择导出目录")
        if not directory:
            return
        
        try:
            # 收集变量数据
            variables_data = {}
            for var_name, var_value in self.template_vars.items():
                value = var_value.get().strip()
                if value:
                    variables_data[var_name] = self._convert_value(value)
                else:
                    variables_data[var_name] = None
            
            # 导出变量JSON
            variables_file = os.path.join(directory, "variables.json")
            with open(variables_file, 'w', encoding='utf-8') as f:
                json.dump(variables_data, f, ensure_ascii=False, indent=2)
            
            # 导出结果文本
            result_file = os.path.join(directory, "result.txt")
            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(result_text)
            
            # 创建说明文件
            readme_file = os.path.join(directory, "README.md")
            readme_content = f"""# 导出包说明

此包包含以下文件：

- `variables.json`: 模板变量数据
- `result.txt`: 最终生成的文本结果

导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
原始模板: {os.path.basename(self.current_file) if self.current_file else '未知'}
"""
            
            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            messagebox.showinfo("成功", f"完整包已导出到: {directory}")
            
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")
    
    def close_file(self):
        """关闭当前文件"""
        if self.current_file:
            if messagebox.askyesno(_("Confirm"), _("Are you sure you want to close the current file?")):
                self.template_content = ""
                self.current_file = None
                self.file_path_var.set(_("No file selected"))
                
                # 清空变量输入
                for widget in self.scrollable_frame.winfo_children():
                    widget.destroy()
                self.template_vars = {}
                
                # 清空JSON输入
                self.json_text.delete(1.0, tk.END)
                
                # 清空结果
                self.result_text.delete(1.0, tk.END)
    
    def show_about(self):
        """显示关于信息"""
        about_text = _("Jinja Template GUI Tool\n\n") + \
                    _("Version: 1.0\n") + \
                    _("A graphical tool for processing Jinja2 templates.\n\n") + \
                    _("Supports multiple languages and real-time preview.")
        
        messagebox.showinfo(_("About Project"), about_text)
    
    def open_project_url(self):
        """打开项目地址"""
        try:
            webbrowser.open("https://github.com/your-username/jinjautil")
        except Exception as e:
            messagebox.showerror(_("Error"), _("Failed to open URL: {}").format(str(e)))
    
    def open_documentation(self):
        """打开文档"""
        try:
            webbrowser.open("file://" + os.path.abspath("README.md"))
        except Exception as e:
            messagebox.showerror(_("Error"), _("Failed to open documentation: {}").format(str(e)))
    
    def load_template(self, file_path):
        """加载模板文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.template_content = f.read()
            
            self.current_file = file_path
            self.file_path_var.set(os.path.basename(file_path))
            
            # 提取变量
            self.extract_and_display_variables()
            # 生成JSON模板
            self.generate_json_template()
            
            messagebox.showinfo("成功", "模板加载成功！")
            
        except Exception as e:
            messagebox.showerror("错误", f"加载模板失败: {str(e)}")
    
    def reload_template(self):
        """重新加载当前模板"""
        if self.current_file:
            self.load_template(self.current_file)
        else:
            messagebox.showwarning("警告", "请先选择模板文件")
    
    def extract_and_display_variables(self):
        """提取并显示模板变量"""
        if not self.template_content:
            return
        
        # 清除现有控件
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # 提取变量
        variables = self.processor.extract_variables(self.template_content)
        self.template_vars = {}
        
        if not variables:
            ttk.Label(self.scrollable_frame, text=_("No template variables detected")).pack(pady=10)
            return
        
        # 创建变量输入控件
        for i, var_name in enumerate(variables):
            frame = ttk.Frame(self.scrollable_frame)
            frame.pack(fill=tk.X, padx=5, pady=2)
            ttk.Label(frame, text=f"{var_name}:", width=25).pack(side=tk.LEFT)
            
            var_value = tk.StringVar()
            entry = ttk.Entry(frame, textvariable=var_value, width=30)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
            
            # 为每个变量创建StringVar并绑定
            self.template_vars[var_name] = var_value
            
            # 添加示例值提示
            sample_values = {
                'name': '张三',
                'age': '25',
                'email': 'zhangsan@example.com',
                'date': '2024-01-01',
                'items': '["item1", "item2"]',
                'count': '10'
            }
            
            if var_name in sample_values:
                entry.insert(0, sample_values[var_name])
    
    def generate_json_template(self):
        """生成JSON模板"""
        if hasattr(self, 'template_vars') and self.template_vars:
            variables = list(self.template_vars.keys())
            json_template = self._create_json_template(variables)
            self.json_text.delete(1.0, tk.END)
            self.json_text.insert(1.0, json_template)
    
    def _create_json_template(self, variables):
        """创建JSON模板字符串"""
        if not variables:
            return "{\n  \"example_key\": \"example_value\"\n}"
        
        template_dict = {}
        
        # 通用的变量类型映射规则
        type_patterns = {
            # 布尔值相关
            'active': True,
            'enabled': True,
            'visible': True,
            'add_': True,
            
            # 数字相关
            'count': 10,
            'age': 25,
            'price': 99.99,
            'num': 5,
            
            # 字符串相关
            'name': '示例名称',
            'title': '示例标题',
            'text': '示例文本内容',
            'content': '示例内容',
            'description': '示例描述',
            'email': 'example@email.com',
            'token': '<token>',
            'code': 'EXAMPLE_CODE',
            
            # 日期相关
            'date': '2024-01-01',
            'time': '12:00:00',
            
            # 列表相关
            'items': ['item1', 'item2'],
            'list': ['a', 'b', 'c'],
            
            # 对象相关
            'data': {'key': 'value'},
            'config': {'setting': 'value'},
        }
        
        # 复杂结构的特殊处理
        complex_structures = {
            'messages': [
                {
                    'role': 'user',
                    'content': '示例内容'
                }
            ],
            'user': {
                'name': '用户名',
                'email': 'user@example.com'
            }
        }
        
        for var in variables:
            var_lower = var.lower()
            assigned = False
            
            # 首先检查复杂结构
            for pattern, value in complex_structures.items():
                if pattern in var_lower:
                    template_dict[var] = value
                    assigned = True
                    break
            
            if assigned:
                continue
                
            # 然后检查类型模式
            for pattern, value in type_patterns.items():
                if (pattern.endswith('_') and var_lower.startswith(pattern[:-1])) or \
                   (not pattern.endswith('_') and pattern in var_lower):
                    template_dict[var] = value
                    assigned = True
                    break
            
            # 如果都没匹配到，使用通用值
            if not assigned:
                template_dict[var] = '请输入值'
        
        return json.dumps(template_dict, ensure_ascii=False, indent=2)
    
    def on_json_change(self, event):
        """JSON输入变化时的处理"""
        # 这里可以添加实时验证逻辑
        pass
    
    def collect_form_data(self):
        """收集表单数据"""
        form_data = {}
        for var_name, var_value in self.template_vars.items():
            value = var_value.get().strip()
            if value:
                # 尝试转换为适当的类型
                form_data[var_name] = self._convert_value(value)
        return form_data
    
    def _convert_value(self, value):
        """尝试转换值的类型"""
        # 尝试转换为数字
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            pass
        
        # 尝试转换为布尔值
        if value.lower() in ['true', 'false']:
            return value.lower() == 'true'
        
        # 尝试转换为列表（简单判断）
        if value.startswith('[') and value.endswith(']'):
            try:
                return json.loads(value)
            except:
                pass
        
        # 默认返回字符串
        return value
    
    def generate_text(self):
        """生成文本"""
        if not self.template_content:
            messagebox.showwarning("警告", "请先选择模板文件")
            return
        
        try:
            # 收集表单数据
            form_data = self.collect_form_data()
            
            # 处理JSON数据
            json_data = {}
            json_text = self.json_text.get(1.0, tk.END).strip()
            if json_text:
                is_valid, result = self.processor.validate_json_data(json_text)
                if is_valid:
                    json_data = result
                else:
                    messagebox.showerror("JSON错误", result)
                    return
            
            # 合并数据
            merged_data = self.processor.merge_data_sources(form_data, json_data)
            
            if not merged_data:
                messagebox.showwarning("警告", "请输入至少一个变量值")
                return
            
            # 渲染模板
            result = self.processor.render_template(self.template_content, merged_data)
            
            # 显示结果
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, result)
            
        except Exception as e:
            messagebox.showerror("错误", f"生成文本失败: {str(e)}")
    
    def clear_all(self):
        """清空所有内容"""
        if messagebox.askyesno(_("Confirm"), _("Are you sure you want to clear all content?")):
            # 清空模板
            self.template_content = ""
            self.current_file = None
            self.file_path_var.set(_("No file selected"))
            
            # 清空变量输入
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            self.template_vars = {}
            
            # 清空JSON输入
            self.json_text.delete(1.0, tk.END)
            
            # 清空结果
            self.result_text.delete(1.0, tk.END)

    def save_result(self):
        """保存结果"""
        result_text = self.result_text.get(1.0, tk.END).strip()
        if not result_text:
            messagebox.showwarning("警告", "没有可保存的内容")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="保存结果",
            defaultextension=".txt",
            filetypes=[
                ("文本文件", "*.txt"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(result_text)
                messagebox.showinfo("成功", f"文件已保存到: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存文件失败: {str(e)}")
    
    def mark_pending_restart(self):
        """标记等待重启状态"""
        try:
            config = {}
            config = {}
            if os.path.exists('config.json'):
                with open('config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
            
            config['pending_restart'] = True
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Failed to mark pending restart: {e}")
    
    def save_current_state(self):
        """保存当前状态"""
        try:
            state = {
                'current_file': self.current_file,
                'template_content': self.template_content[:1000] if self.template_content else "",  # 限制长度
                'window_geometry': self.root.geometry()
            }
            
            with open('app_state.json', 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Failed to save state: {e}")
    
    def load_saved_state(self):
        """加载保存的状态"""
        try:
            if os.path.exists('app_state.json'):
                with open('app_state.json', 'r', encoding='utf-8') as f:
                    state = json.load(f)
                
                # 恢复窗口位置和大小
                if 'window_geometry' in state:
                    self.root.geometry(state['window_geometry'])
                
                # 恢复文件状态
                if state.get('current_file') and os.path.exists(state['current_file']):
                    self.load_template(state['current_file'])
                
                # 删除状态文件
                os.remove('app_state.json')
                
        except Exception as e:
            print(f"Failed to load saved state: {e}")
    
    def restart_program(self):
        """重启程序"""
        try:
            # 保存当前状态
            self.save_current_state()
            
            # 关闭当前程序
            self.root.quit()
            self.root.destroy()
            
            # 重启程序
            import sys
            import subprocess
            subprocess.Popen([sys.executable] + sys.argv)
            
        except Exception as e:
            messagebox.showerror(_("Error"), _("Failed to restart program: {}").format(str(e)))

def main():
    try:
        root = tk.Tk()
        app = JinjaTemplateGUI(root)
        
        # 检查是否有待重启标记
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                if config.get('pending_restart', False):
                    # 清除重启标记
                    config['pending_restart'] = False
                    with open('config.json', 'w', encoding='utf-8') as f:
                        json.dump(config, f, ensure_ascii=False, indent=2)
                    
                    # 加载之前保存的状态
                    app.load_saved_state()
        except Exception as e:
            print(f"Failed to check restart status: {e}")
        
        root.mainloop()
    except Exception as e:
        print(f"程序启动错误: {str(e)}")
        input("按回车键退出...")


if __name__ == "__main__":
    main()
