import streamlit as st
import base64
from PIL import Image
import io
import os

# 页面设置
st.set_page_config(page_title="晚夜·黄金ETF系统 (V8.0 终极自检版)", layout="wide")

# 侧边栏
with st.sidebar:
    st.header("🛠️ 维修中心")
    api_key = st.text_input("输入 Google Gemini API Key", type="password")
    
    # ---------------- 关键修改：自检按钮 ----------------
    if api_key:
        st.markdown("---")
        if st.button("🔍 第一步：检测我的 Key 能用什么模型"):
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                
                # 列出所有支持 generateContent 的模型
                models = []
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        models.append(m.name)
                
                if models:
                    st.success(f"连接成功！发现 {len(models)} 个可用模型。")
                    st.session_state['valid_models'] = models
                else:
                    st.error("连接成功，但没有发现可用模型。这通常是因为 Key 所在的区域受限。")
            except Exception as e:
                st.error(f"连接失败。原因：{str(e)}")
                st.info("💡 提示：请检查 Key 是否有多余空格，或者去 aistudio.google.com 重新生成一个。")

    # 如果检测到了模型，显示下拉框让用户选
    if 'valid_models' in st.session_state:
        selected_model = st.selectbox("请选择一个模型:", st.session_state['valid_models'], index=0)
    else:
        # 默认备选项
        selected_model = "models/gemini-1.5-flash"

# 主界面
st.title("🏛️ 黄金 ETF 深度决策系统 (V8.0)")
st.caption("如果不确定用哪个模型，请先点击左侧的‘检测’按钮")

col1, col2 = st.columns([1.5, 1])

# 核心逻辑
def analyze_image(image_bytes, key, model_name, prompt):
    import google.generativeai as genai
    genai.configure(api_key=key)
    
    # 使用用户选定的模型
    model = genai.GenerativeModel(model_name)
    image = Image.open(io.BytesIO(image_bytes))
    
    try:
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"❌ 分析出错: {str(e)}"

# 提示词
system_prompt = """
请扮演一位结合了“晚夜博主”趋势战法与“华尔街量化”因子的黄金分析师。
针对用户的 ETF (无杠杆) 交易需求，分析这张 K 线图。

【分析重点】：
1. **画线定位**：是蓝色急涨通道还是紫色稳涨通道？支撑位在哪里（MA30/前低）？
2. **量化排雷**：乖离率是否过大？MACD是否有顶背离？布林带是否变盘？
3. **操作建议**：ETF是买入、持有还是止盈？万金油抄底点位在哪里？

请输出清晰的 Markdown 报告。
"""

if api_key:
    with col1:
        uploaded_file = st.file_uploader("📤 上传 K 线图", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            st.image(uploaded_file, caption="待分析盘面", use_column_width=True)
    
    with col2:
        if uploaded_file:
            st.subheader("🤖 分析报告")
            if st.button("开始分析", type="primary"):
                with st.spinner(f"正在使用 {selected_model} 进行分析..."):
                    result = analyze_image(uploaded_file.getvalue(), api_key, selected_model, system_prompt)
                    st.markdown(result)
else:
    st.info("👈 请先在左侧输入 Key，并点击‘检测’按钮")
