import sys
import markdown

def convert_md_to_html(input_file, output_file):
    # マークダウンファイルを読み込む
    with open(input_file, 'r', encoding='utf-8') as file:
        md_content = file.read()

    # マークダウンをHTMLに変換
    html_content = markdown.markdown(md_content)

    # 変換したHTMLをファイルに書き込む
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python <script_name>.py <input_md_file> <output_html_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_md_to_html(input_file, output_file)
