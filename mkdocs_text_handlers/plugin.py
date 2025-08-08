from mkdocs.plugins import BasePlugin
from mkdocs.config.config_options import Type
import re

class NonBreakingSpacePlugin(BasePlugin):
    config_scheme = (
        ('enabled', Type(bool, default=True)),
        ('prepositions', Type(list, default=['АО', 'ООО','ПАО','ОАО', 'а', 'в', 'на', 'и', 'о', 'к', 'с', 'со','за', '(за', 'об', 'не', '№', '"О', '«О', 'ее', 'её'])),
    )
    
    def on_page_content(self, html, page, config, files):
        if not self.config['enabled']:
            return html
        
        pattern = re.compile(
            r'(?<!\w)(' + '|'.join(re.escape(p) for p in self.config['prepositions']) + r')(\s+)',
            re.IGNORECASE
        )
        
        return pattern.sub(lambda m: f"{m.group(1)}&nbsp;", html)