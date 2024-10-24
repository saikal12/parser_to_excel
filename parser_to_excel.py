import re
import pandas as pd


def parse_md_to_excel(md_file, excel_file):
    with open(md_file, 'r', encoding='utf-8') as md:
        content = md.read()
        q_pattern = r'([BC]\d+)\s+(.+?)(?=\n\s*[BC]\d+|\n\s*##|\n\s*#|\Z)'
        imag_pattern = r'!\[.*\]\((.*?)\)'
    questions = re.findall(q_pattern, content, re.DOTALL)
    print(questions)
    data = []
    for question in questions:
        q_number = question[0]
        q_text = question[1].strip()
        images = re.findall(imag_pattern, q_text)
        clean_text = re.sub(imag_pattern, '', q_text).strip()
        data.append(
            [q_number, clean_text, ', '.join(images) if images else '']
            )

    df = pd.DataFrame(data, columns=['Номер вопроса', 'Вопрос', 'Рисунок'])
    df.to_excel(excel_file, index=False)


if __name__ == '__main__':
    parse_md_to_excel('questioncd(1).md', 'questions_output.xlsx')
