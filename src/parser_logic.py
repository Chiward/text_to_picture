import re

def parse_text_v10(raw_text: str, num_pages: int = 3):
    """
    V10版解析逻辑：生成<p>标签以控制段间距。
    """
    # 1. 预处理
    text = raw_text.replace('\r\n', '\n').strip()
    text = re.sub(r'(\n[\t ]*)(\d+\.)', r'\n\n\2', text)

    lines = text.split('\n')
    title = lines[0]
    body_text = '\n'.join(lines[1:]).strip()

    # 2. 获取所有内容块
    blocks = [b.strip() for b in body_text.split('\n\n') if b.strip()]
    
    if not blocks:
        return []

    pages_content = []

    # 3. 固定第一页内容
    num_blocks_for_page1 = 1
    if len(blocks) >= num_blocks_for_page1:
        pages_content.append('\n\n'.join(blocks[:num_blocks_for_page1]))
        remaining_blocks = blocks[num_blocks_for_page1:]
    else:
        pages_content.append('\n\n'.join(blocks))
        remaining_blocks = []

    # 4. 基于字数，精确分配剩余的块
    if remaining_blocks:
        total_remaining_chars = sum(len(b) for b in remaining_blocks)
        target_chars_for_page2 = total_remaining_chars / 2

        page2_blocks = []
        page3_blocks = []
        current_chars = 0
        
        for block in remaining_blocks:
            if current_chars < target_chars_for_page2:
                page2_blocks.append(block)
                current_chars += len(block)
            else:
                page3_blocks.append(block)
        
        if page2_blocks:
            pages_content.append('\n\n'.join(page2_blocks))
        if page3_blocks:
            pages_content.append('\n\n'.join(page3_blocks))

    # 5. 格式化输出为带<p>标签的HTML
    pages_data = []
    for i, content_part in enumerate(pages_content):
        paragraphs = content_part.split('\n\n')
        html_paragraphs = []
        for p in paragraphs:
            p_html = p.replace('\n', '<br>')
            p_html = re.sub(r'\*\*(.*?)\*\*\*', r'<strong class="bold">\1</strong>', p_html)
            p_html = re.sub(r'/(.*?)/', r'<span class="red-text">\1</span>', p_html)
            html_paragraphs.append(f'<p>{p_html}</p>')
        
        content_html = ''.join(html_paragraphs)
        
        current_title = title if i == 0 else ""
        pages_data.append({"title": current_title, "content_html": content_html})
            
    return pages_data