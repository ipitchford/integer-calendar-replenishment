"""Rebuild the manuscript from Markdown; requires Pandoc and LuaLaTeX (release built with TinyTeX, TeX Live 2026)."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def build(source, output, appendices=()):
    source, output = Path(source), Path(output)
    command = ['pandoc', source.name, *(str(path) for path in appendices),
               '--from=markdown+tex_math_single_backslash+tex_math_dollars',
               '--standalone', '--pdf-engine=lualatex',
               '-V', 'documentclass=article', 
                
               '-V', 'geometry:margin=25mm', '-V', 'fontsize=11pt',
               '-V', 'papersize=a4',
               '-o', str(output)]
    subprocess.run(command, cwd=source.parent, check=True)
    if 'paper' in source.parts:
        tex = output.with_suffix('.tex')
        subprocess.run(['pandoc', source.name,
                        '--from=markdown+tex_math_single_backslash+tex_math_dollars',
                        '--standalone', '-t', 'latex',
                        '-V', 'documentclass=article',
                        
                        
                        
                        '-V', 'geometry:margin=25mm', '-V', 'fontsize=11pt',
                        '-V', 'papersize=a4', '-o', str(tex)],
                       cwd=source.parent, check=True)


if __name__ == '__main__':
    build(ROOT/'paper/integer_calendar_replenishment.md',
          ROOT/'paper/integer_calendar_replenishment.pdf')
