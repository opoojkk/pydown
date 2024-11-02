import re
import os
import requests
import argparse
from PIL import Image

# 替换为你的 Imgur Client ID
IMGUR_CLIENT_ID = os.getenv('IMGUR_CLIENT_ID')

if not IMGUR_CLIENT_ID:
    raise ValueError("Please set the IMGUR_CLIENT_ID environment variable.")


def convert_image_to_png(image_path):
    """将图片转换为PNG格式并返回新的文件路径"""
    img = Image.open(image_path)
    png_path = f"{os.path.splitext(image_path)[0]}.png"
    img.convert('RGBA').save(png_path, 'PNG')
    return png_path


def upload_image_to_imgur(image_path):
    """上传图片到 Imgur，返回图片链接"""
    headers = {'Authorization': f'Client-ID {IMGUR_CLIENT_ID}'}
    with open(image_path, 'rb') as image_file:
        response = requests.post(
            'https://api.imgur.com/3/upload',
            headers=headers,
            files={'image': image_file}
        )

    # 检查响应状态
    if response.status_code == 200:
        return response.json()['data']['link']
    else:
        print(f"Failed to upload {image_path}: {response.status_code}, {response.text}")
        return None


def read_markdown_file(file_path):
    """读取Markdown文件内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def save_converted_markdown(output_file, markdown_text):
    """保存转换后的Markdown内容到文件"""
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(markdown_text)


def convert_local_images_in_markdown(markdown_text, markdown_dir):
    # 匹配 Markdown 中的本地图片路径
    local_image_pattern = r'!\[.*?\]\(([^http][^)]+)\)'

    def replace_local_image(match):
        local_image_path = os.path.join(markdown_dir, match.group(1).strip())

        # 检查文件是否存在
        if not os.path.isfile(local_image_path):
            print(f"File not found: {local_image_path}")
            return match.group(0)  # 保留原始链接

        # 转换为PNG格式
        png_image_path = convert_image_to_png(local_image_path)

        # 上传本地PNG图片到 Imgur
        imgur_link = upload_image_to_imgur(png_image_path)
        if imgur_link:
            print(f"Uploaded {local_image_path} to Imgur: {imgur_link}")
            return f'![image]({imgur_link})'
        else:
            return match.group(0)  # 如果上传失败，保留原始链接

    # 替换 Markdown 内容中的所有本地图片路径
    new_markdown_text = re.sub(local_image_pattern, replace_local_image, markdown_text)
    return new_markdown_text


# 示例用法
if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description='Upload local images in Markdown to Imgur and update the links.')
    parser.add_argument('input_file', help='Path to the input Markdown file')
    args = parser.parse_args()

    # 获取输入 Markdown 文件路径
    input_file = args.input_file
    markdown_dir = os.path.dirname(input_file)

    # 从文件中读取Markdown内容
    markdown_content = read_markdown_file(input_file)

    # 转换Markdown内容中的本地图片链接为 Imgur 链接
    converted_markdown = convert_local_images_in_markdown(markdown_content, markdown_dir)

    # 保存转换后的Markdown到新文件
    output_file = os.path.join(markdown_dir, 'publish_' + os.path.basename(input_file))
    save_converted_markdown(output_file, converted_markdown)

    print(f'Converted Markdown saved to {output_file}')
