import streamlit as st
import pandas as pd
import json
import os
import random

pre_consultation_list=[]
# 把预问诊打分和病历打分合在一起
with open("eval_pre_consultation.txt","r",encoding="utf-8") as f:
    for line in f:
        tmp=line.split("#")
        pre=tmp[:-1]
        last=eval(tmp[-1])
        pre_consultation_list.append([pre,last])

datas=[]
with open('eval_medical_record_13.txt','r',encoding='utf-8') as f:
        # 读取所有行
    lines = f.readlines()

    # 随机选择 100 行
    random_lines = random.sample(lines, 100)
    for i,line in enumerate(random_lines):
        tmp=line.split("#")
        pre=tmp[:-1]
        last=tmp[-1]
        tmp2=eval(last)
        chats=tmp2['问诊过程']
        
        for score,chat in pre_consultation_list:
            if chat==chats:
                datas.append([chats,tmp2['病历'],pre,score])
                break
print(datas[0])

# 总页数
total_pages = len(datas)

# 创建一个分页功能
current_page = st.number_input('选择页面:', min_value=1, max_value=total_pages, step=1)

# 获取当前页面的数据
current_data = datas[current_page - 1]
dialogue, pathology, rating ,consultation_result= current_data

# print(type(dialogue))
#对话进行修改：以对话框形式显示
dialogues=[]
for i,item in enumerate(dialogue):
    if i%2==0:
        dialogues.append({"speaker": "患者", "text": item})
    else:
        dialogues.append({"speaker": "医生", "text": item})
# print(dialogus_list)
    
# 创建评分字典，按顺序插入
result = {
    "格式规范性": {
        "得分": int(rating[0]),
        "优点": rating[1],
        "缺点": rating[2]
    },
    "描述完整性": {
        "得分": int(rating[3]),
        "优点": rating[4],
        "缺点": rating[5]
    },
    "内容准确性": {
        "得分": int(rating[6]),
        "优点": rating[7],
        "缺点": rating[8]
    },
    "关键信息抓取": {
        "得分": int(rating[9]),
        "优点": rating[10],
        "缺点": rating[11]
    }
}

# 预问诊的评分 转成json格式
consultation_result_json = {
    "问诊效率与准确性": {
        "分值": int(consultation_result[0]),
        "解释": consultation_result[1]
    },
    "用户交互体验": {
        "分值": int(consultation_result[2]),
        "解释": consultation_result[3]
    },
    "医疗临床思维": {
        "分值": int(consultation_result[4]),
        "解释": consultation_result[5]
    }
}


# 页面标题
st.title(f"页面 {current_page}/{total_pages}")

# 使用 Markdown 渲染三个元素
st.markdown(f"### 对话：\n")


# 自定义对话框样式，医生对话框在左，患者对话框在右
st.markdown("""
    <style>
    .chat-container {
        display: flex;
        flex-direction: column;
        margin-bottom: 10px;
    }

    .chat-row {
        display: flex;
        margin-bottom: 10px;
        width: 100%;
    }

    .chat-bubble {
        border-radius: 15px;
        padding: 10px;
        margin: 5px;
        display: inline-block;
        max-width: 60%;  /* 限制对话框最大宽度 */
        word-wrap: break-word;  /* 长单词换行 */
    }

    .doctor {
        justify-content: flex-start;
    }

    .patient {
        justify-content: flex-end;
    }

    .doctor-bubble {
        background-color: #d1e7dd;
        color: #0f5132;
        text-align: left;
    }

    .patient-bubble {
        background-color: #f8d7da;
        color: #842029;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

# 渲染对话框
for dialogue in dialogues:
    if dialogue["speaker"] == "医生":
        st.markdown(f'''
            <div class="chat-row doctor">
                <div class="chat-bubble doctor-bubble"><strong>{dialogue["speaker"]}:</strong> {dialogue["text"]}</div>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
            <div class="chat-row patient">
                <div class="chat-bubble patient-bubble"><strong>{dialogue["speaker"]}:</strong> {dialogue["text"]}</div>
            </div>
        ''', unsafe_allow_html=True)
st.markdown(f"### 病理：\n{pathology}")
st.markdown(f"### 预问诊对话过程评测：\n")
st.json(consultation_result_json)

st.markdown(f"### 病历评测：\n")
st.json(result)

# 提供文本输入
user_input = st.text_area("请输入您的评论：", key=f"input_{current_page}")

# 文件路径
excel_file = "user_comments.xlsx"

# 检查是否已有 Excel 文件，并初始化 DataFrame
if os.path.exists(excel_file):
    df = pd.read_excel(excel_file)
else:
    # 如果文件不存在，则创建一个空的 DataFrame，包含“页面”和“用户评论”列
    df = pd.DataFrame(columns=["页面", "用户评论"])

# 显示输入的内容并保存
if st.button("提交"):
    # 将当前页面和用户输入存入 DataFrame
    new_data = pd.DataFrame({"页面": [current_page], "用户评论": [user_input]})
    
    # 追加到现有的 DataFrame
    df = pd.concat([df, new_data], ignore_index=True)
    
    # 保存到 Excel 文件
    df.to_excel(excel_file, index=False)

    st.success("评论已保存！")
    
    # 显示更新后的数据
    st.write(df)
