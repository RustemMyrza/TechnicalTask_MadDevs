from bs4 import BeautifulSoup

MAX_LEN = 4096

def split_message(html: str, max_len: int):
    soup = BeautifulSoup(html, "html.parser")
    fragments = []
    current_fragment = ""
    open_tags = []
    
    for element in soup.recursiveChildGenerator():
        if isinstance(element, str):
            if len(current_fragment) + len(element) > max_len:
                for tag in reversed(open_tags):
                    current_fragment += f"</{tag}>"
                fragments.append(current_fragment)
                current_fragment = ""
                for tag in open_tags:
                    current_fragment += f"<{tag}>"
            current_fragment += element
        else:
            if element.name:
                if len(current_fragment) + len(str(element)) > max_len:
                    for tag in reversed(open_tags):
                        current_fragment += f"</{tag}>"
                    fragments.append(current_fragment)
                    current_fragment = ""
                    for tag in open_tags:
                        current_fragment += f"<{tag}>"
            
                if element.name in ["p", "b", "strong", "i", "ul", "ol", "div", "span"]:
                    if element.name not in open_tags:
                        open_tags.append(element.name)
                current_fragment += str(element)  

    if current_fragment:
        for tag in reversed(open_tags):
            current_fragment += f"</{tag}>"
        fragments.append(current_fragment)
    return fragments

def extract_text_from_html(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return ""
    

if __name__ == "__main__":
    file_path = "source.html"
    text = extract_text_from_html(file_path)
    split_message(text, MAX_LEN)