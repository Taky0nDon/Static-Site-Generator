from re import findall


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    result = []
    all_alt_text = findall(r"!\[.*?\]", text)
    all_urls = findall(r"\(.*?\)", text)
    for alt, url in zip(all_alt_text, all_urls):
        result.append((alt[2:-1], url[1:-1]))
    return result

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    result = []
    all_link_text = findall(r"\[.*?\]", text)
    all_urls = findall(f"\(.*?\)", text)
    for text, url in zip(all_link_text, all_urls):
        result.append(
                (text[1:-1], url[1:-1])
                )
    return result

