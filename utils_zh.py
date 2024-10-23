#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from collections import defaultdict
from chat_tools import get_completion_from_messages, get_completion_and_token_count

# 商品和目录的数据文件
products_file = 'data/products_zh.json'

# 从商品数据中获取
def get_products():
    with open(products_file, 'r') as file:
        products = json.load(file)
    return products

# 获取商品和目录
def get_products_and_category():
    """
    获取类别下产品列表的dict
    """
    products = get_products()
    
    products_by_category = defaultdict(list)
    for product_name, product_info in products.items():
        category = product_info.get('类别')
        if category:
            products_by_category[category].append(product_info.get('名称'))
    
    return dict(products_by_category)

# 相比上一个函数，可获取的商品直接在 template 中限定
def find_category_and_product_only(user_input, products_and_category):
    delimiter = "####"
    system_message = f"""
    您将获得客户服务查询。
    客户服务查询将使用{delimiter}字符作为分隔符。
    请仅输出一个可解析的Python列表，列表每一个元素是一个JSON对象，每个对象具有以下格式：
    'category': <包括以下几个类别：Computers and Laptops、Smartphones and Accessories、Televisions and Home Theater Systems、Gaming Consoles and Accessories、Audio Equipment、Cameras and Camcorders>,
    以及
    'products': <必须是下面的允许产品列表中找到的产品列表>

    类别和产品必须在客户服务查询中找到。
    如果提到了某个产品，它必须与允许产品列表中的正确类别关联。
    如果未找到任何产品或类别，则输出一个空列表。
    除了列表外，不要输出其他任何信息！

    允许的产品：

    Computers and Laptops category:
    TechPro Ultrabook
    BlueWave Gaming Laptop
    PowerLite Convertible
    TechPro Desktop
    BlueWave Chromebook

    Smartphones and Accessories category:
    SmartX ProPhone
    MobiTech PowerCase
    SmartX MiniPhone
    MobiTech Wireless Charger
    SmartX EarBuds

    Televisions and Home Theater Systems category:
    CineView 4K TV
    SoundMax Home Theater
    CineView 8K TV
    SoundMax Soundbar
    CineView OLED TV

    Gaming Consoles and Accessories category:
    GameSphere X
    ProGamer Controller
    GameSphere Y
    ProGamer Racing Wheel
    GameSphere VR Headset

    Audio Equipment category:
    AudioPhonic Noise-Canceling Headphones
    WaveSound Bluetooth Speaker
    AudioPhonic True Wireless Earbuds
    WaveSound Soundbar
    AudioPhonic Turntable

    Cameras and Camcorders category:
    FotoSnap DSLR Camera
    ActionCam 4K
    FotoSnap Mirrorless Camera
    ZoomMaster Camcorder
    FotoSnap Instant Camera
        
    只输出对象列表，不包含其他内容。
    """
    messages =  [  
    {'role':'system', 'content': system_message},    
    {'role':'user', 'content': f"{delimiter}{user_input}{delimiter}"},  
    ] 
    return get_completion_from_messages(messages)

def find_category_and_product_v1(user_input, products_and_category):
    """
    从用户输入中获取产品和类别

    参数：
    user_input：用户的查询
    products_and_category：产品类型和对应产品的字典
    """
    delimiter = "####"
    system_message = f"""
    您将获得客户服务查询。
    客户服务查询将使用{delimiter}字符作为分隔符。
    请仅输出一个可解析的Python列表，列表每一个元素是一个JSON对象，每个对象具有以下格式：
    'category': <包括以下几个类别：Computers and Laptops、Smartphones and Accessories、Televisions and Home Theater Systems、Gaming Consoles and Accessories、Audio Equipment、Cameras and Camcorders>,
    以及
    'products': <必须是下面的允许产品列表中找到的产品列表>

    类别和产品必须在客户服务查询中找到。
    如果提到了某个产品，它必须与允许产品列表中的正确类别关联。
    如果未找到任何产品或类别，则输出一个空列表。
    
    根据产品名称和产品类别与客户服务查询的相关性，列出所有相关的产品。
    不要从产品的名称中假设任何特性或属性，如相对质量或价格。

    允许的产品以JSON格式提供。
    每个项目的键代表类别。
    每个项目的值是该类别中的产品列表。
    允许的产品：{products_and_category}
    """

    few_shot_user_1 = """我想要最贵的电脑"""
    few_shot_assistant_1 = """[{'category': 'Computers and Laptops', \
'products': ['TechPro Ultrabook', 'BlueWave Gaming Laptop', 'PowerLite Convertible', 'TechPro Desktop', 'BlueWave Chromebook']}]
    """
    messages =  [  
    {'role':'system', 'content': system_message},  
    {'role':'user', 'content':f"{delimiter}{few_shot_user_1}{delimiter}"},
    {'role':'assistant', 'content': few_shot_assistant_1}, 
    {'role':'user', 'content': f"{delimiter}{user_input}{delimiter}"},  
    ] 
    return get_completion_from_messages(messages)

def find_category_and_product_v2(user_input, products_and_category):
    """
    从用户输入中获取产品和类别

    添加：不要输出任何不符合JSON格式的额外文本。
    添加了第二个示例（用于few-shot提示），用户询问最便宜的计算机。
    在这两个few-shot示例中，显示的响应只是json格式的完整产品列表

    参数：
    user_input：用户的查询
    products_and_category：产品类型和对应产品的字典
    """
    delimiter = "####"
    system_message = f"""
    您将获得客户服务查询。
    客户服务查询将使用{delimiter}字符作为分隔符。
    请仅输出一个可解析的Python列表，列表每一个元素是一个JSON对象，每个对象具有以下格式：
    'category': <包括以下几个类别：Computers and Laptops、Smartphones and Accessories、Televisions and Home Theater Systems、Gaming Consoles and Accessories、Audio Equipment、Cameras and Camcorders>,
    以及
    'products': <必须是下面的允许产品列表中找到的产品列表>

    类别和产品必须在客户服务查询中找到。
    如果提到了某个产品，它必须与允许产品列表中的正确类别关联。
    如果未找到任何产品或类别，则输出一个空列表。
    
    根据产品名称和产品类别与客户服务查询的相关性，列出所有相关的产品。
    不要从产品的名称中假设任何特性或属性，如相对质量或价格。

    允许的产品以JSON格式提供。
    每个项目的键代表类别。
    每个项目的值是该类别中的产品列表。
    允许的产品：{products_and_category}
    """

    few_shot_user_1 = """我想要最贵的电脑。你推荐哪款"""
    few_shot_assistant_1 = """[{'category': 'Computers and Laptops', \
'products': ['TechPro Ultrabook', 'BlueWave Gaming Laptop', 'PowerLite Convertible', 'TechPro Desktop', 'BlueWave Chromebook']}]
    """
    few_shot_user_2 = """我想要最便宜的电脑，呢推荐哪款"""
    few_shot_assistant_2 = """[{'category': 'Computers and Laptops', \
'products': ['TechPro Ultrabook', 'BlueWave Gaming Laptop', 'PowerLite Convertible', 'TechPro Desktop', 'BlueWave Chromebook']}]"""
    messages =  [  
    {'role':'system', 'content': system_message},  
    {'role':'user', 'content':f"{delimiter}{few_shot_user_1}{delimiter}"},
    {'role':'assistant', 'content': few_shot_assistant_1}, 
    {'role':'user', 'content':f"{delimiter}{few_shot_user_2}{delimiter}"},
    {'role':'assistant', 'content': few_shot_assistant_2},
    {'role':'user', 'content': f"{delimiter}{user_input}{delimiter}"},  
    ] 
    return get_completion_from_messages(messages)


def read_string_to_list(input_string):
    """
    将输入的字符串转换为 Python 列表。

    参数:
    input_string: 输入的字符串，应为有效的 JSON 格式。

    返回:
    list 或 None: 如果输入字符串有效，则返回对应的 Python 列表，否则返回 None。
    """
    if input_string is None:
        return None

    try:
        # 将输入字符串中的单引号替换为双引号，以满足 JSON 格式的要求
        input_string = input_string.replace("'", "\"")  
        input_string = input_string.replace("```json", "")
        input_string = input_string.replace("```", "")
        # print(input_string)
        data = json.loads(input_string)
        return data
    except json.JSONDecodeError:
        print("Error: Invalid JSON string")
        return None  
    
def get_product_by_name(name):
    products = get_products()
    return products.get(name, None)

def get_products_by_category(category):
    products = get_products()
    return [product for product in list(products.values()) if product["类别"] == category]

def generate_output_string(data_list):
    """
    根据输入的数据列表生成包含产品或类别信息的字符串。

    参数:
    data_list: 包含字典的列表，每个字典都应包含 "products" 或 "category" 的键。

    返回:
    output_string: 包含产品或类别信息的字符串。
    """
    output_string = ""
    if data_list is None:
        return output_string

    for data in data_list:
        try:
            if "products" in data and data["products"]:
                products_list = data["products"]
                for product_name in products_list:
                    product = get_product_by_name(product_name)
                    if product:
                        output_string += json.dumps(product, indent=4, ensure_ascii=False) + "\n"
                    else:
                        print(f"Error: Product '{product_name}' not found")
            elif "category" in data:
                category_name = data["category"]
                category_products = get_products_by_category(category_name)
                for product in category_products:
                    output_string += json.dumps(product, indent=4, ensure_ascii=False) + "\n"
            else:
                print("Error: Invalid object format")
        except Exception as e:
            print(f"Error: {e}")

    return output_string


# if __name__ == '__main__':
    # user_input = "请告诉我关于 smartx pro phone 和 the fotosnap camera 的信息。另外，请告诉我关于你们的tvs的情况。"
    # print(find_category_and_product_only(user_input, get_products_and_category()))
# process_user_message_ch(user_input,[])