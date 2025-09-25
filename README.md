# 操作手册 (manual.md)

本文档详细说明了如何配置和运行“宣传图文转图片”自动化脚本。

---

### **1. 环境配置**

在运行脚本之前，你需要一个安装了 Python 和 pip 的环境。

1.  **安装依赖**: 
    脚本的核心依赖是 `playwright`。通过以下命令安装所有必要的依赖：
    ```bash
    pip install playwright
    ```

2.  **安装浏览器驱动**:
    Playwright 需要下载它所控制的浏览器驱动。运行以下命令来完成安装（这个过程可能需要一些时间）：
    ```bash
    playwright install
    ```

### **2. 文件结构**

请确保项目包含以下结构：

```
/
├───dist/                 # 最终生成的图片输出目录
├───src/
│   ├─── main.py          # 主脚本
│   ├─── style.css        # 样式文件
│   └─── parser_logic.py  # 文本解析逻辑
└───素材/
    ├─── input.txt        # 【需替换】要生成图片的源文本
    └─── avatar.webp      # 【需替换】要使用的头像图片
```

### **3. 如何运行**

1.  **准备素材**:
    *   将你要转换的文本内容放入 `素材/input.txt` 文件中。
    *   将用作头像的图片（推荐使用 `.webp` 或 `.png` 格式）放入 `素材/avatar.webp` 文件中。

2.  **执行脚本**:
    打开终端或命令行，导航到项目的根目录，然后运行以下命令：
    ```bash
    python src/main.py
    ```

3.  **查看结果**:
    脚本执行完毕后，生成的图片将会保存在 `dist/` 目录中，文件名为 `output_1.png`, `output_2.png` ...

### **4. 自定义参数 (可选)**

你也可以通过命令行参数来自定义输入和输出路径：

```bash
python src/main.py --text_file /path/to/your/text.txt --avatar_file /path/to/your/avatar.png --output_dir /path/to/your/output_folder
```

-   `--text_file`: 指定自定义的文本文件路径。
-   `--avatar_file`: 指定自定义的头像文件路径。
-   `--output_dir`: 指定自定义的图片输出目录。