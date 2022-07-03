from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time


subscription_key = "cb8b5c94042043038fd59ad12a92e9dd"
endpoint = "https://20220702sak.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

def get_tags(filepath):
    local_image = open(filepath, 'rb')
    tags_result = computervision_client.tag_image_in_stream(local_image)
    tags = tags_result.tags
    tags_name = []
    for tag in tags:
        tags_name.append(tag.name)
    return tags_name


def detect_objects(filepath):
    local_image = open(filepath, 'rb')

    detect_objects_results = computervision_client.detect_objects_in_stream(local_image)
    objects = detect_objects_results.objects
    return objects


import streamlit as st
from PIL import ImageDraw
from PIL import ImageFont

st.title('物体検出ツール')

uploaded_file = st.file_uploader('画像を選択してください。', type=['jpg', 'png'])
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_path = f'img/{uploaded_file.name}'
    img.save(img_path)
    objects = detect_objects(img_path)

    # 矩形を描く
    draw = ImageDraw.Draw(img)
    for object in objects:
        x = object.rectangle.x
        y = object.rectangle.y
        w = object.rectangle.w
        h = object.rectangle.h
        caption = object.object_property

        # フォント情報を作成する
        font = ImageFont.truetype('./Helvetica 400.ttf', size=50)
        # テキストのサイズを指定する
        text_w, text_h = draw.textsize(caption, font=font)

        # 物体を囲む矩形を描く
        draw.rectangle([(x, y), (x+w, y+h)], fill=None, outline='green', width=10)
        # テキストを囲む矩形を描く
        draw.rectangle([(x, y), (x+text_w, y+text_h)], fill='green')
        # テキストを書き込む
        draw.text((x, y), caption, fill='white', font=font)
    st.image(img)

    # タグを取得する
    tags_name = get_tags(img_path)
    tags_name = ' ,  '.join(tags_name)
    st.markdown('**認識されたコンテンツ**')
    st.markdown(f'> {tags_name}')

else:
    st.write('まずは画像を選択してください。')


