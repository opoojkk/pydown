import re
import base64
import os
import argparse


def read_markdown_file(file_path):
    """从Markdown文件中读取内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def convert_base64_images(markdown_text, output_dir):
    # 正则表达式匹配Base64图片
    base64_pattern = r'!\[.*?\]\((data:image/(.*?);base64,([A-Za-z0-9+/=]+))\)'

    # 创建输出目录，如果不存在
    os.makedirs(output_dir, exist_ok=True)

    def replace_base64(match):
        # 获取文件扩展名
        file_type = match.group(1).split('/')[1]
        base64_data = match.group(3)

        # 生成文件名
        file_name = f'image_{hash(base64_data)}.{file_type}'
        file_path = os.path.join(output_dir, file_name)

        # 解码并保存图片
        with open(file_path, 'wb') as img_file:
            img_file.write(base64.b64decode(base64_data))

        # 返回Markdown中的新引用
        return f'![image]({file_path})'

    # 替换Markdown中的Base64图片引用
    new_markdown_text = re.sub(base64_pattern, replace_base64, markdown_text)
    return new_markdown_text


def save_converted_markdown(output_file, markdown_text):
    """保存转换后的Markdown内容到文件"""
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(markdown_text)


# 示例用法
if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description='Convert Base64 images in Markdown to image files.')
    parser.add_argument('input_file', help='Path to the input Markdown file')
    args = parser.parse_args()

    # 获取输入文件的目录
    input_dir = os.path.dirname(args.input_file)

    # 设置输出目录为输入文件夹上一级的assets路径
    output_dir = os.path.join(os.path.dirname(input_dir), 'assets')
    output_file = os.path.join(input_dir, 'converted_' + os.path.basename(args.input_file))

    # 从文件中读取Markdown内容
    markdown_content = read_markdown_file(args.input_file)

    # 转换Base64图片并获取新的Markdown内容
    converted_markdown = convert_base64_images(markdown_content, output_dir)

    # 保存转换后的Markdown到新文件
    save_converted_markdown(output_file, converted_markdown)

    print(f'Converted Markdown saved to {output_file}')
