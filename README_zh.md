# Jinja模板GUI工具

这是一个基于tkinter的图形界面工具，用于处理Jinja2模板文件。

## 🌍 国际化支持

本工具现已支持7种语言的国际化：
- 简体中文 (默认)
- English
- 日本語
- 한국어
- Deutsch
- Français
- Italiano

通过顶部菜单栏的 "Language" 选项可以切换语言。

## 功能特性

- 🖥️ 直观的图形化界面操作
- 📁 支持选择Jinja2模板文件（.j2, .tpl, .tmpl等格式）
- 📝 双模式数据输入（表单输入和JSON输入）
- 🔍 自动识别模板变量
- 👁️ 实时预览生成结果
- 💾 结果保存功能
- 🔄 模板热重载

## 安装依赖

安装所需依赖：

```bash
pip install -r requirements.txt
```

## 使用方法

运行主程序：
```bash
python main.py
```

## 界面说明

### 1. 模板选择区域
- **选择文件**：浏览并选择Jinja2模板文件
- **重新加载**：重新加载当前模板文件
- 显示当前选中的文件名

### 2. 数据输入区域
提供两种数据输入方式：

**表单输入标签页**：
- 自动识别模板中的变量
- 为每个变量生成输入框
- 支持自动类型转换（数字、布尔值、列表等）

**JSON输入标签页**：
- 直接输入JSON格式的数据
- 适合复杂数据结构
- 实时语法验证

### 3. 结果显示区域
- 实时显示生成的文本结果
- 支持滚动查看长文本
- 语法高亮友好显示

### 4. 操作按钮
- **生成文本**：根据输入数据渲染模板
- **保存结果**：将生成的结果保存到文件
- **清空所有**：清除所有输入和结果

## 模板语法支持

支持标准Jinja2语法及特殊函数：

### 变量替换
```jinja2
Hello {{ name }}!
Your age is {{ age }} years.
```

### 条件语句
```jinja2
{% if age >= 18 %}
Adult
{% else %}
Minor
{% endif %}
```

### 循环语句
```jinja2
<ul>
{% for item in items %}
<li>{{ item }}</li>
{% endfor %}
</ul>
```

### 特殊函数支持
```jinja2
{# 异常处理函数 #}
{{ raise_exception("错误信息") }}

{# 字符串处理函数 #}
{{ text | trim }}
```

### 复杂模板示例
工具支持复杂的聊天模板，如 `chat_template.jinja`，包含：
- 多语言支持
- 角色交替验证
- 内容类型处理（文本/图像）
- 严格的格式验证

## 示例模板

项目包含两个示例模板：

1. `test_template.html.j2` - HTML简历模板
2. `resume_template.txt.j2` - 文本简历模板

## 配置文件

程序会自动生成 `config.json` 配置文件，存储：
- 最近使用的模板
- 窗口大小设置
- 字体大小
- 上次使用的变量值

## 错误处理

- 模板语法错误提示
- JSON格式验证
- 文件读写异常处理
- 用户友好的错误消息

## 开发信息

### 项目结构
```
jinjautil/
├── main.py              # 主程序入口
├── template_processor.py # 模板处理核心逻辑
├── i18n.py              # 国际化管理器
├── requirements.txt      # 依赖包列表
├── README.md            # 英文文档
├── README_zh.md         # 中文文档
├── config.json          # 统一配置文件
├── locales/             # 翻译文件目录
│   ├── zh_CN/          # 中文翻译
│   ├── en_US/          # 英文翻译
│   └── ...             # 其他语言翻译
└── example/             # 示例模板文件
    ├── test_template.html.j2
    └── resume_template.txt.j2
```

### 核心组件

1. **主应用程序 (`main.py`)**
   - 基于Tkinter的GUI实现
   - 菜单系统支持语言切换
   - 文件选择和模板加载
   - 数据输入处理（表单和JSON模式）
   - 结果显示和导出功能

2. **模板处理器 (`template_processor.py`)**
   - Jinja2环境配置
   - 从模板中提取变量
   - 使用数据合并渲染模板
   - 自定义函数和过滤器支持

3. **国际化管理器 (`i18n.py`)**
   - 多语言支持管理
   - 基于gettext的翻译系统
   - 支持运行时语言切换
   - 配置持久化

### 依赖项

- **Jinja2** (>=3.1.0): 模板引擎
- **Babel** (>=2.12.0): 国际化工具
- **Python标准库**: tkinter, json, os, pathlib

### 添加新语言

1. 创建新语言目录: `locales/{language_code}/LC_MESSAGES/`
2. 复制现有的 `.po` 文件并翻译消息
3. 编译翻译: `pybabel compile -d locales`
4. 在 `i18n.py` 中添加语言到 `SUPPORTED_LANGUAGES`

### 贡献指南

1. Fork仓库
2. 创建功能分支
3. 进行修改
4. 彻底测试
5. 提交Pull Request

### 支持

如有问题、功能请求或疑问：
- 在GitHub上提交Issue
- 查看现有文档
- 查阅示例模板了解使用模式