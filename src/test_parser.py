
import unittest
import sys
import os

# 将src目录添加到Python路径中，以便能够导入main模块
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# 导入我们需要测试的函数
from main import parse_text_v3

class TestTextParser(unittest.TestCase):

    def test_parsing_logic_v3(self):
        """
        测试V3版本的文本解析逻辑，覆盖以下场景：
        - 正确提取第一页标题。
        - 正确提取第一页的第一段内容。
        - 正确按双换行符分割后续页面。
        - 正确处理加粗 `**...**` 格式。
        - 正确处理红色 `/.../` 格式。
        """
        sample_text = """第一行是标题

这是第一页的第一段内容。
该段落有两行。

这是第二页，包含 **加粗** 的文字。

这是第三页，包含 /红色/ 的文字。"""

        expected_output = [
            {
                'title': '第一行是标题',
                'content_html': '这是第一页的第一段内容。<br>该段落有两行。'
            },
            {
                'title': '',
                'content_html': '这是第二页，包含 <strong class="bold">加粗</strong> 的文字。'
            },
            {
                'title': '',
                'content_html': '这是第三页，包含 <span class="red-text">红色</span> 的文字。'
            }
        ]

        actual_output = parse_text_v3(sample_text)
        
        self.assertEqual(actual_output, expected_output)

if __name__ == '__main__':
    unittest.main()
