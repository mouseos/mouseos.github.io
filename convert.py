import os
import markdown2
import re
def get_creation_date(path):
    date_format="%Y年%m月%d日"
    try:
        # ファイルが存在しない場合、エラーメッセージを返す
        if not os.path.exists(path):
            return "指定されたパスのファイルが存在しません"

        # ファイルの作成日を取得
        creation_time = os.path.getctime(path)
        creation_date = datetime.datetime.fromtimestamp(creation_time)

        # 指定された形式で日付をフォーマット
        formatted_date = creation_date.strftime(date_format)
        
        return formatted_date
    except Exception as e:
        return f"エラー: {e}"

def marge_htmls(htmls):
    tmp_html = ""
    for html in htmls:
        with open(html, 'r', encoding='utf-8') as html_file:
            html_content = html_file.read()
            tmp_html += html_content
    return tmp_html


def load_txt(path):
    with open(path, 'r', encoding='utf-8') as txt_file:
        txt_content = txt_file.read()
        return txt_content


# マークダウンファイルをHTMLに変換する関数


def convert_markdown_to_html(input_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as markdown_file:
        markdown_content = markdown_file.read()
        html_content = markdown2.markdown(markdown_content, extras=[
                                          "tables", "fenced-code-blocks","code-color","fenced-code-blocks","header-ids"])
        return html_content

# 指定されたディレクトリ内のすべてのマークダウンファイルを変換


def convert_markdown_files_in_directory(directory_path, max_depth=3):
    html_list = []
    nav = load_txt("templates/nav.html")
    footer = load_txt("templates/footer.html")
    if max_depth < 0:
        return

    for root, _, files in os.walk(directory_path):
        if max_depth > 0:
            for file_name in files:
                if file_name.endswith('.md'):
                    input_file_path = os.path.join(root, file_name)
                    html_content = convert_markdown_to_html(input_file_path)

                    # .md を .html に変更して保存
                    output_file_path = os.path.splitext(
                        input_file_path)[0] + '.html'
                    #作成日を取得
                    creation_date=get_creation_date(output_file_path)
                    # 先頭からドットを抜く
                    output_file_path_to_save = re.sub(
                        r'^\.', '', output_file_path).replace("\\", "/")
                    output_file_path_to_save = re.sub(
                        r'^\/', '', output_file_path_to_save)
                    html_list.append(output_file_path_to_save)
                    if ("articles" in output_file_path):
                        print("articles")
                        nav = re.sub("""<link rel="stylesheet" href="./templates/style/main.css" type="text/css">""",
                                     """<link rel="stylesheet" href="../../templates/style/main.css" type="text/css">""", nav)
                        html_content = nav+f"""<div class="col s12 l9 z-depth-1 article">
                        <h1>記事タイトル</h1>
                    <p class="post-info">
                        <i class="material-icons">date_range</i> 投稿日: {creation_date} |
                        <i class="material-icons">person</i> 投稿者: Yuu
                    </p>
                    <hr>
                    <article>
                        """ + \
                            html_content+"</article></div>"+footer

                    with open(output_file_path, 'w', encoding='utf-8') as html_file:
                        html_file.write(html_content)

        # サブディレクトリに再帰的に探索
        for subdirectory in os.listdir(root):
            subdirectory_path = os.path.join(root, subdirectory)
            if os.path.isdir(subdirectory_path):
                convert_markdown_files_in_directory(
                    subdirectory_path, max_depth - 1)
    return html_list


# ./articles と ./pages ディレクトリ内のマークダウンファイルを変換
articles = convert_markdown_files_in_directory('./articles')
pages = convert_markdown_files_in_directory('./pages')


nav = load_txt("templates/nav.html")
footer = load_txt("templates/footer.html")
article_html = ""
article_html += nav
article_html += ("""
<div class="articles col s12 l9">
          <div class="row">
""")
for article in articles:
    print(article)
    article_html += (f"""
    <!--card開始-->
    <div class="card col s12 m6 l4">
        <div class="card-image"> <img src="https://materializeweb.com/images/sample-1.jpg">
        </div>
        <div class="card-content">
        <p>{article}</p>
        </div>
        <div class="card-action">
        <div class="right">
            <a href="{article}">
            <button style="" class="btn waves-effect waves-light">記事を読む
            </button>
            </a>
        </div>
        </div>
    </div>
    <!--card終了-->
""")
article_html += footer
with open("index.html", 'w', encoding='utf-8') as html_file:
    html_file.write(article_html)
