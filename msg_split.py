MAX_LEN = 4096

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
    

if __name__ == "__main__":
    file_path = "source.html"  # Укажите путь к вашему HTML-файлу
    text = extract_text_from_html(file_path)
    fragments = split_message(text, MAX_LEN)
    for el in fragments:
        print("Fragment:")
        print(el)