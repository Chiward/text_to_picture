import asyncio
import os
import argparse
import re
import base64
from pathlib import Path
from playwright.async_api import async_playwright

# --- 新的动态加载逻辑 ---
def load_parser_func():
    """从外部文件加载并返回解析函数。"""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    parser_path = os.path.join(project_root, 'src', 'parser_logic.py')
    
    with open(parser_path, 'r', encoding='utf-8') as f:
        parser_code = f.read()
    
    # 在一个受控的命名空间中执行代码
    namespace = {}
    exec(parser_code, namespace)
    
    # 从命名空间中返回函数对象
    return namespace['parse_text_v10']

async def create_images_v2(pages_data, avatar_base64, output_dir, css_content):
    """
    V2版图片生成：
    1. 接受Base64编码的头像数据。
    2. 动态生成HTML时，只有带标题的页面才添加<h1>标签。
    """
    
    pages_html = ""
    for i, page_data in enumerate(pages_data):
        page_num = i + 1
        page_class = "page-1-background" if i == 0 else "page-n-background"
        
        avatar_html = ""
        title_html = ""

        # 仅第一页有头像
        if i == 0:
            avatar_uri = f"data:image/webp;base64,{avatar_base64}"
            avatar_html = f'''
            <div class="avatar-container">
                <img class="avatar-img" src="{avatar_uri}">
            </div>
            '''
        
        # 仅有标题的页面(即第一页)才生成h1标签
        if page_data["title"]:
            title_html = f'<h1 class="title">{page_data["title"]}</h1>'

        if i == 0:
            # 第一页的特殊结构
            pages_html += f'''
            <div class="page page-1-container" id="page-{page_num}">
                <div class="page1-header"></div>
                <div class="page1-body">
                    {avatar_html}
                    {title_html}
                    <div class="content">{page_data["content_html"]}</div>
                </div>
            </div>
            '''
        else:
            # 后续页面的结构
            pages_html += f'''
            <div class="page page-n-container" id="page-{page_num}">
                <div class="content">{page_data["content_html"]}</div>
            </div>
            '''

    script_content = '''
    <script>
        function showPage(pageNumber) {
            const pages = document.querySelectorAll('.page');
            pages.forEach((page, index) => {
                if (index + 1 === pageNumber) {
                    page.style.display = 'block';
                } else {
                    page.style.display = 'none';
                }
            });
        }
    </script>
    '''

    full_html = (
        "<!DOCTYPE html>"
        '<html lang="zh-CN">'
        "<head>"
        '<meta charset="UTF-8">'
        '<title>Generated Content</title>'
        f"<style>{css_content}</style>"
        "</head>"
        "<body>"
        f'<div id="canvas">{pages_html}</div>'
        f"{script_content}"
        "</body>"
        "</html>"
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        await page.set_content(full_html, wait_until="load")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for i in range(len(pages_data)):
            page_num = i + 1
            await page.evaluate(f'showPage({page_num})')
            page_element = page.locator(f'#page-{page_num}')
            await page_element.screenshot(path=os.path.join(output_dir, f"output_{page_num}.png"))
            print(f"已生成图片: output_{page_num}.png")

        await browser.close()

def main():
    parser = argparse.ArgumentParser(description="自动化生成宣传图")
    
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    default_text_path = os.path.join(project_root, '素材', 'input.txt')
    default_avatar_path = os.path.join(project_root, '素材', 'avatar.webp')
    default_output_dir = os.path.join(project_root, 'dist')
    css_path = os.path.join(project_root, 'src', 'style.css')

    parser.add_argument("--text_file", default=default_text_path, help="输入的文本文件路径")
    parser.add_argument("--avatar_file", default=default_avatar_path, help="用户头像文件路径")
    parser.add_argument("--output_dir", default=default_output_dir, help="图片输出目录")
    
    args = parser.parse_args()

    try:
        # 动态加载解析函数
        parse_text_v10 = load_parser_func()

        with open(args.text_file, 'r', encoding='utf-8') as f:
            raw_text = f.read()
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        with open(args.avatar_file, 'rb') as f:
            avatar_data = f.read()
            avatar_base64 = base64.b64encode(avatar_data).decode('utf-8')
    except FileNotFoundError as e:
        print(f"错误: 输入文件未找到 - {e}")
        return
    except Exception as e:
        print(f"加载解析函数时出错: {e}")
        return

    pages_data = parse_text_v10(raw_text)
    
    if not pages_data:
        print("错误: 未能从文本中解析出任何页面。请检查文本格式。")
        return

    print("应用最终修正，开始生成图片...")
    asyncio.run(create_images_v2(pages_data, avatar_base64, args.output_dir, css_content))
    print(f"图片生成完毕，已保存至 {args.output_dir} 目录。")

if __name__ == "__main__":
    main()
