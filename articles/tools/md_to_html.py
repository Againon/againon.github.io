# 安装 markdown 库：pip3 install markdown
# 安装 pymdownx 扩展来支持语法高亮和代码块的自定义样式：pip3 install pymdown-extensions
# 安装 Pygments 使语法高亮，失败：pip3 install Pygments 安装超时，更换镜像源-阿里：pip3 install library -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
# 还是失败：清华源：pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple library
import markdown
from pathlib import Path
from pymdownx.highlight import HighlightExtension
from pymdownx.superfences import SuperFencesCodeExtension

def convert_markdown_to_html(file_path, output_path=None):
    """
    将 Markdown 文件转换为 HTML 文件，并设置 HTML 的 title 为文件名。

    参数:
    file_path (str): Markdown 文件的路径。
    output_path (str, optional): 输出 HTML 文件的路径，默认为 None，表示输出到与 Markdown 文件同名的 HTML 文件。

    返回:
    str: 输出 HTML 文件的完整路径。
    """
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 提取文件名（不包括扩展名）作为标题
    title = Path(file_path).stem

    # 转换 Markdown 为 HTML
    html = markdown.markdown(content, extensions=[
        'fenced_code',
        SuperFencesCodeExtension(),
        HighlightExtension(linenums=True,linenums_style='pymdownx-inline')
    ])

    # 创建完整的 HTML 文件
    full_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <link rel="stylesheet" type="text/css" href="../css/article.css">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" integrity="sha512-Fo3rlrZj/k7ujTnHg4CGR2D7kSs0v4LLanw2qksYuRlEzO+tcaEPQogQ0KaoGN26/zrn20ImR1DfuLWnOo7aBA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
        </head>
        <body>
            {html}
            <script type="text/javascript" src="../js/article.js"></script>
        </body>
        </html>
        """

    # 写入 HTML 文件
    if output_path is None:
        output_path = Path(file_path).with_suffix('.html')
    else:
        output_path = Path(output_path)

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(full_html)

    return str(output_path)


# 使用示例
# 用于区分脚本是被直接运行还是被导入到其他脚本中。
if __name__ == "__main__":
    # 指定 Markdown 文件路径
    file_path = './path/to/your/file.md'

    # 转换 Markdown 为 HTML 文件
    html_file_path = convert_markdown_to_html(file_path)

    # 输出 HTML 文件的路径
    print(f"HTML file created at: {html_file_path}")
