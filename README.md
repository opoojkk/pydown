# Markdown Image Converter

## 项目简介

Markdown Image Converter 是一个 Python 工具，用于处理 Markdown 文件中的图片引用。该项目包括两个功能：

1. **上传本地图片到 Imgur**：将 Markdown 文件中的本地图片转换为 PNG 格式，上传到 Imgur，并更新 Markdown 文件中的图片链接。
2. **转换 Base64 图片为文件**：提取 Markdown 文件中的 Base64 格式图片，将其解码为图片文件，并在 Markdown 文件中更新引用。

## 文件说明

- `imgur_image_uploader.py`：负责将本地图片上传到 Imgur 的脚本。
- `base64_image_converter.py`：负责将 Markdown 文件中的 Base64 图片转换为图片文件的脚本。

## 使用方法

### 环境要求

Python3

你可以使用以下命令安装所需库：

```bash
pip install -r requirements.txt
```
## 使用 Imgur 图片上传工具
1. 在`imgur_image_uploader.py`文件中，将 `IMGUR_CLIENT_ID` 替换为你的 Imgur Client ID。
2. 运行脚本，并提供输入 Markdown 文件的路径：
```bash
python imgur_image_uploader.py <path_to_markdown_file>
```
该脚本会处理文件中的本地图片，上传到 Imgur，并保存更新后的 Markdown 文件。

## 使用 Base64 图片转换工具
1. 运行脚本，并提供输入 Markdown 文件的路径：

```bash
python base64_image_converter.py <path_to_markdown_file>
````
该脚本会处理文件中的 Base64 图片，生成相应的图片文件，并更新 Markdown 文件中的引用。

# 输出文件
- 在处理本地图片的情况下，生成的 Markdown 文件名为 publish_<原始文件名>，保存于与原始文件相同的目录。
- 在处理 Base64 图片的情况下，生成的 Markdown 文件名为 converted_<原始文件名>，同时在指定的输出目录中保存解码后的图片文件。

# 许可证
此项目采用 MIT 许可证，详细信息请查看 LICENSE 文件。