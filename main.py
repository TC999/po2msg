import argparse
import polib
import os


def parse_args():
    parser = argparse.ArgumentParser(description='Convert .po files to .msg files.')
    parser.add_argument('input_file', type=str, help='Path to the .po input file')
    parser.add_argument('output_file', type=str, help='Path to the .msg output file')
    return parser.parse_args()


def read_po_file(po_file_path):
    po = polib.pofile(po_file_path)
    return po


def get_language_code_from_filename(filename):
    # 提取文件名中最后一个".po"之前的部分作为语言代码
    base_name = os.path.basename(filename)
    language_code = base_name.split('.po')[0]
    return language_code


def convert_po_to_msg(po_data, language_code):
    # 从第一个条目中提取头部信息
    header_content = ""
    if po_data:
        header_content = po_data[0].msgstr if po_data[0].msgstr else ""

    # 转义 msg 文件中的特殊字符，但保留 Unicode 字符
    def escape_msg_string(s):
        return s.replace('"', '\\"').replace('\n', '\\n')

    msg_header = f'set ::msgcat::header "{header_content}"\n'
    msg_content = [msg_header]
    for entry in po_data:
        if entry.msgid and entry.msgstr:
            # 替换 %1$s 为 %{1}，在 Tcl 中这是正确的变量替换语法
            msgid_escaped = escape_msg_string(
                entry.msgid.replace('%', '%%').replace('$', '\\$').replace('{', '\\{').replace('}', '\\}'))
            msgstr_escaped = escape_msg_string(
                entry.msgstr.replace('%', '%%').replace('$', '\\$').replace('{', '\\{').replace('}', '\\}'))
            msg_content.append(f'::msgcat::mcset {language_code} "{msgid_escaped}" "{msgstr_escaped}"\n')
    return "".join(msg_content)


def write_msg_file(msg_content, msg_file_path):
    with open(msg_file_path, 'w', encoding='utf-8') as f:
        f.write(msg_content)


def main():
    args = parse_args()
    po_data = read_po_file(args.input_file)
    language_code = get_language_code_from_filename(args.input_file)
    msg_content = convert_po_to_msg(po_data, language_code)
    write_msg_file(msg_content, args.output_file)
    print(f"Conversion completed. Output file: {args.output_file}")


if __name__ == "__main__":
    main()