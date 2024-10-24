import re
import pandas as pd
from sympy.parsing.latex import parse_latex


def convert_symb(match):
    math_symbol = match.group(1)
    try:
        math_expr = parse_latex(math_symbol)
        return str(math_expr)
    except Exception:
        return math_symbol


def parse_md_to_excel(md_file, excel_file):
    with open(md_file, 'r', encoding='utf-8') as md:
        content = md.read()
        part_pattern = r'#+ ЧАСТЬ (\d+)'
        q_pattern = r'([BCВ]\d+)\s+(.+?)(?=\n\s*[BCВ]\d+|\Z)'
        imag_pattern = r'!\[.*\]\((.*?)\)'
        math_pattern = r'\$(.+?)\$'
    data = []
    parts = re.split(part_pattern, content)
    for i in range(1, len(parts), 2):
        part_number = parts[i].strip()
        part_content = parts[i+1]
        questions = re.findall(q_pattern, part_content, re.DOTALL)

        for question in questions:
            q_number = question[0]
            q_text = question[1].strip()
            images = re.findall(imag_pattern, q_text)
            clean_text = re.sub(imag_pattern, '', q_text).strip()
            math_text = re.sub(math_pattern, convert_symb, clean_text)

            data.append(
                [part_number, q_number, math_text,
                    ', '.join(images) if images else '']
                )

    df = pd.DataFrame(data, columns=['Часть', 'Номер вопроса',
                                     'Вопрос', 'Рисунок'])
    df.to_excel(excel_file, index=False)


if __name__ == '__main__':
    parse_md_to_excel('questioncd(1).md', 'questions_output.xlsx')
