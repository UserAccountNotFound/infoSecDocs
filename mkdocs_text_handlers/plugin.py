from mkdocs.plugins import BasePlugin
from mkdocs.config.config_options import Type
import re

class NonBreakingSpacePlugin(BasePlugin):
    config_scheme = (
        ('enabled', Type(bool, default=True)),
        ('prepositions', Type(list, default=['АО', 'ООО','ПАО', 'а', 'в', '(в','на', 'и', 'о', 'от', 'по', 'к', 'с', 'со','за', '(за', 'об', 'не', '№', '"О', '«О', 'ее', 'её'])),
    )
    
    def on_page_content(self, html, page, config, files):
        if not self.config['enabled']:
            return html
        
        # Обработка предлогов
        pattern = re.compile(
            r'(?<!\w)(' + '|'.join(re.escape(p) for p in self.config['prepositions']) + r')(\s+)',
            re.IGNORECASE
        )
        html = pattern.sub(lambda m: f"{m.group(1)}&nbsp;", html)
        
        # Обработка цифр с единицами измерения
        units_pattern = re.compile(
            r'(\d+)(\s+)(г|кг|мм|см|м|км)\b',
            re.IGNORECASE
        )
        html = units_pattern.sub(lambda m: f"{m.group(1)}&nbsp;{m.group(3)}", html)

        # Обработка инициалов и слов вокруг них
        initials_pattern = re.compile(
            r'(\s|^)([А-ЯЁа-яёA-Za-z])\.\s*([А-ЯЁа-яёA-Za-z])\.|'       # А. Б.
            r'(\w+)\s+([А-ЯЁа-яёA-Za-z])\.\s*([А-ЯЁа-яёA-Za-z])\.|'     # Фамилия А.Б.
            r'([А-ЯЁа-яёA-Za-z])\.\s*([А-ЯЁа-яёA-Za-z])\.\s+(\w+)'      # А.Б. Фамилия
        )
        
        def replace_initials(match):
            if match.group(2) and match.group(3):                                           # Случай "А. Б."
                return f"{match.group(1)}{match.group(2)}.&nbsp;{match.group(3)}."
            elif match.group(5) and match.group(6):                                         # Случай "Фамилия А.Б."
                return f"{match.group(4)}&nbsp;{match.group(5)}.&nbsp;{match.group(6)}."
            elif match.group(7) and match.group(8):                                         # Случай "А.Б. Фамилия"
                return f"{match.group(7)}.&nbsp;{match.group(8)}.&nbsp;{match.group(9)}"
            return match.group(0)
        
        html = initials_pattern.sub(replace_initials, html)
        
        
        return html