import re
from typing import List, Tuple

class LOOP_ARGUMENTS:
    end_of_loop_header = r'+?%}'

class RegexThings:
    loop = r'{%for.*?{%endloop%}'
    variable = r'{{.*}}'
    loop_value = r'for '

    remove_template_from_loop = r'{%for(.*?){%endloop%}'

    loop_starts_with = '{%for '
    loop_ends_with = '{%endloop%}'

class AldTemplateEngine(RegexThings, LOOP_ARGUMENTS):
    def find_template_loops(self, template: str) -> List[str]:
        loops: List[str] = re.findall(RegexThings.loop, template, re.DOTALL)
        return loops

    def create_dumb_loop(self, template_loop: str) -> str:
        dumb_loop = re.findall(RegexThings.remove_template_from_loop, template_loop, re.DOTALL)[0].replace('%}', ':')
        return 'for' + dumb_loop

    def loop_parser(self, dumb_loop: str) -> Tuple[str, str]:
        loop_header_ends = dumb_loop.find('\n')
        for_loop_header = dumb_loop[0: loop_header_ends - 0x1]
        vars = dumb_loop[loop_header_ends:]
        return for_loop_header, vars

    def execute(self, for_loop_header: str, vars: str) -> str:
        vars = vars[0x1:].replace('\n', '').replace('{{', '{').replace('}}', '}')
        code = f'''''.join(f'{vars}' {for_loop_header})'''
        try:
            return eval(code)
        except Exception as e:
            raise SystemExit(e)    

    def generate_template(self, template: str) -> str:
        new_template = template
        loops = self.find_template_loops(template)
        for loop in loops:
            dumb_loop = self.create_dumb_loop(loop)
            for_loop_header, vars = self.loop_parser(dumb_loop)
            loop_template_result = self.execute(for_loop_header, vars)
            new_template = new_template.replace(loop, loop_template_result)
        return new_template

    def template_render(self, template_file):
        return self.generate_template(template_file)