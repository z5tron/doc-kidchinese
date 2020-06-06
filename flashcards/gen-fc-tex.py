import sys
import jinja2
import os
from jinja2 import Template

words = []
for line in open(sys.argv[1], 'r'):
    col = line.split()
    for w in col[1:]:
        c = {'chap': col[0],
             'text': w,
             'type': 'Danzi', }
        if len(w) > 2: c['type'] = 'Juzi'
        elif len(w) == 2: c['type'] = 'Ci'
        else: c['type'] = 'Danzi'
        words.append(c)
        
# print(words)
latex_jinja_env = jinja2.Environment(
    block_start_string = '\BLOCK{',
    block_end_string = '}',
    variable_start_string = '\VAR{',
    variable_end_string = '}',
    comment_start_string = '\#{',
    comment_end_string = '}',
    line_statement_prefix = '%%',
    line_comment_prefix = '%#',
    trim_blocks = True,
    autoescape = False,
    loader = jinja2.FileSystemLoader(os.path.abspath('.'))
)

template = latex_jinja_env.get_template('fc-template.tex.jinja')

print(template.render(words=words))
