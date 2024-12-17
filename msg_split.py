import argparse

MAX_LEN = 4096  # Значение по умолчанию, если не передано в командной строке

def split_message(html: str, max_len: int):
    if not html:  # Пустая строка
        return [""]

    fragments = []  # Инициализация списка фрагментов
    if len(html) <= max_len:
        fragments.append(html)
        return fragments

    openedTags = []  # Список открытых тегов
    tagName = ""  # Имя текущего тега
    inTag = False  # Флаг, указывающий на нахождение внутри тега
    fragment = ""  # Фрагмент текста

    for line in html.split("\n"):
        # Если добавление текущей строки превысит max_len, добавляем фрагмент в список
        if len(fragment) + len(line) > max_len:
            fragments.append(fragment)
            fragment = ""
            if openedTags:
                for el in reversed(openedTags):
                    fragment += f"</{el}>"

        for symbol in line:
            fragment += symbol
            if inTag:
                # Завершаем тег, когда встречаем пробел или символ ">"
                if symbol in [" ", ">"]:
                    if tagName.startswith("/"):
                        # Закрываем тег и удаляем из openedTags
                        if tagName[1:] in openedTags:
                            openedTags.remove(tagName[1:])
                        tagName = ""
                    else:
                        # Добавляем открывающий тег в список
                        openedTags.append(tagName)
                    inTag = False
                    tagName = ""
                    continue
                else:
                    tagName += symbol
                    continue

            if symbol == "<":
                # Начинаем обработку тега
                inTag = True

        # После завершения строки добавляем закрывающие теги
        for el in reversed(openedTags):
            fragment += f"</{el}>"

    # Добавляем последний фрагмент
    if fragment:
        fragments.append(fragment)

    # Разбиваем длинные строки без тегов
    for i in range(len(fragments)):
        if len(fragments[i]) > max_len:
            part = fragments[i]
            while len(part) > max_len:
                fragments[i] = part[:max_len]
                part = part[max_len:]
                fragments.append(part)

    return fragments

def extract_text_from_html(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return ""

def main():
    # Создаем парсер для аргументов командной строки
    parser = argparse.ArgumentParser(description="Split an HTML file into fragments of a specified maximum length.")
    
    # Добавляем аргументы для максимальной длины и пути к файлу
    parser.add_argument('--max-len', type=int, default=MAX_LEN, help="Maximum length of each fragment (default is 4096).")
    parser.add_argument('file', type=str, help="Path to the HTML file to be processed.")
    
    # Разбираем аргументы
    args = parser.parse_args()

    # Читаем содержимое HTML-файла
    text = extract_text_from_html(args.file)
    
    # Разбиваем HTML-содержимое на фрагменты
    fragments = split_message(text, args.max_len)
    
    # Выводим фрагменты
    for idx, fragment in enumerate(fragments, start=1):
        print(f"Fragment #{idx}: {len(fragment)} characters")
        print(fragment)
        print("-" * 40)

if __name__ == "__main__":
    main()
