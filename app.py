import streamlit as st
from streamlit_ace import st_ace
from utils import *
import json
from streamlit_quill import st_quill

line_wrap = False

st.title("Easy Text Generator")
st.write("Use language models with just a few clicks")

model_names = []
for model_dict in models:
    for key, value in model_dict.items():
        model_names.append(key)

if "model_select" in locals():
    st.header(model_select)

st.sidebar.title("Options")

# Setup sidebar
max_length = st.sidebar.slider(
    """ Max Text Length 
    (Longer length, slower generation)""",
    50,
    1000,
    value=100
)

model_selectbox = st.sidebar.selectbox("Model", model_names)

for item in models:
    for key, value in item.items():
        if key == model_selectbox:
            model_data = value

model_select = model_data["path"]

context = st.sidebar.text_area("Starting text")

advanced = st.sidebar.checkbox("Advanced options", False, "advanced")

if advanced:
    top_k = st.sidebar.slider("Words to consider (top_k)", 1, 100, value=50)
    top_p = st.sidebar.slider("Creativity (top_p)", 0.0, 1.0, value=0.95)
    custom_model = st.sidebar.text_input(label="Model from transformers")
    if custom_model != '':
        model_select = custom_model
else:
    top_k = 50
    top_p = 0.95

if st.sidebar.button("Generate"):
    model, tokenizer = load_model(model_dir=model_select)

    if context:
        sample = generate(model,tokenizer,input_text=context,max_length=max_length, top_k=top_k, top_p=top_p)
    else: 
        sample = generate(model,tokenizer,max_length=max_length, top_k=top_k, top_p=top_p)
    st.balloons()

else:
    sample = ['']

# Fix up line wrapping
if line_wrap == True:
    sample[0] = wrap_text(sample[0], length=80)
else:
    sample[0] = sample[0]
st.text(sample[0])

#placeholder = st.sidebar.text_input("Placeholder", "Some placeholder text")
#html = st.sidebar.checkbox("Return HTML", False)
#read_only = st.sidebar.checkbox("Read only", False)
if sample[0]:
	placeholder = sample[0]

st.content = st_quill(
    placeholder=sample[0],
    html=False,
    readonly=True,
)

#st.write(content)

