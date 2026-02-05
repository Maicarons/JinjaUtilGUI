import gettext
import os
import locale
import json
from pathlib import Path


class I18nManager:
    """国际化管理器"""
    
    # 支持的语言列表
    SUPPORTED_LANGUAGES = {
        'zh_CN': '简体中文',
        'en_US': 'English',
        'ja_JP': '日本語',
        'ko_KR': '한국어',
        'de_DE': 'Deutsch',
        'fr_FR': 'Français',
        'it_IT': 'Italiano'
    }
    
    def __init__(self, default_lang='zh_CN'):
        """初始化国际化管理器"""
        self.default_lang = default_lang
        self.current_lang = default_lang
        self.translators = {}
        self.config_file = 'config.json'
        self.locales_dir = Path(__file__).parent / 'locales'
        
        # 加载配置
        self.load_config()
        
        # 初始化所有语言的翻译器
        self.init_translators()
        
        # 设置当前语言
        self.set_language(self.current_lang)
    
    def init_translators(self):
        """初始化所有支持语言的翻译器"""
        for lang_code in self.SUPPORTED_LANGUAGES.keys():
            try:
                # 创建翻译器
                translator = gettext.translation(
                    'messages',
                    localedir=str(self.locales_dir),
                    languages=[lang_code],
                    fallback=True
                )
                self.translators[lang_code] = translator
            except Exception as e:
                print(f"Failed to initialize translator for {lang_code}: {e}")
                # 使用默认翻译器作为后备
                self.translators[lang_code] = gettext.NullTranslations()
    
    def set_language(self, lang_code):
        """设置当前语言"""
        if lang_code in self.SUPPORTED_LANGUAGES:
            self.current_lang = lang_code
            # 安装当前语言的翻译器
            self.translators[lang_code].install()
            # 保存配置
            self.save_config()
            return True
        return False
    
    def get_current_language(self):
        """获取当前语言"""
        return self.current_lang
    
    def get_supported_languages(self):
        """获取支持的语言列表"""
        return self.SUPPORTED_LANGUAGES.copy()
    
    def get_language_name(self, lang_code):
        """获取语言名称"""
        return self.SUPPORTED_LANGUAGES.get(lang_code, lang_code)
    
    def _(self, message):
        """翻译消息"""
        if self.current_lang in self.translators:
            return self.translators[self.current_lang].gettext(message)
        return message
    
    def gettext(self, message):
        """翻译消息的别名方法"""
        return self._(message)
    
    def load_config(self):
        """加载国际化配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.current_lang = config.get('language', self.default_lang)
        except Exception as e:
            print(f"Failed to load i18n config: {e}")
            self.current_lang = self.default_lang
    
    def save_config(self):
        """保存国际化配置"""
        try:
            # 读取现有配置
            config = {}
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            
            # 更新国际化相关配置
            config.update({
                'language': self.current_lang,
                'supported_languages': list(self.SUPPORTED_LANGUAGES.keys()),
                'pending_restart': False
            })
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Failed to save i18n config: {e}")
    
    def format_message(self, message, *args, **kwargs):
        """格式化翻译后的消息"""
        translated = self._(message)
        try:
            if args:
                return translated.format(*args)
            elif kwargs:
                return translated.format(**kwargs)
            else:
                return translated
        except (KeyError, IndexError) as e:
            print(f"Message formatting error: {e}")
            return translated


# 全局国际化管理器实例
i18n_manager = I18nManager()


def _(message):
    """全局翻译函数"""
    return i18n_manager._(message)


def set_language(lang_code):
    """设置全局语言"""
    return i18n_manager.set_language(lang_code)


def get_current_language():
    """获取当前语言"""
    return i18n_manager.get_current_language()


def get_supported_languages():
    """获取支持的语言"""
    return i18n_manager.get_supported_languages()


def format_message(message, *args, **kwargs):
    """格式化消息"""
    return i18n_manager.format_message(message, *args, **kwargs)