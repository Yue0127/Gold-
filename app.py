import streamlit as st
import base64
from PIL import Image
import io
import time

# 页面配置
st.set_page_config(page_title="晚夜·黄金ETF决策系统 (V7.1兼容版)", layout="wide")

# 侧边栏
with st.sidebar:
    st.header("⚙️ 核心设置")
    model_provider = st.radio("选择 AI 引擎:", ["Google Gemini (免费)", "OpenAI GPT-4o (付费)"])
    api_key = st.text_input(f"输入 {model_provider.split()[0]} API Key", type="password")
    st.info("💡 如果 Gemini 报错，系统会自动尝试切换不同版本的模型。")

st.title("🏛️ 黄金 ETF 深度决策系统 (V7.1 自动纠错版)")
st.caption(f"当前引擎: {model_provider} | 自动适配模型版本")

col1, col2 = st.columns([1.5, 1])

# ----------------- 核心逻辑 -----------------

def analyze_with_gemini_auto(image_bytes, key, prompt):
    import google.generativeai as genai
    
    genai.configure(api_key=key)
    
    # 备选模型列表（AI 会挨个尝试，直到成功）
    candidate_models = [
        "gemini-1.5-flash",          # 最新标准名
        "gemini-1.5-flash-latest",   # 别名1
        "gemini-1.5-flash-001",      # 特定版本号
        "gemini-1.5-pro",            # 备用：Pro版本
    ]
    
    image = Image.open(io.BytesIO(image_bytes))
    last_error = ""

    # 循环尝试
    for model_name in candidate_models:
        try:
            # 创建模型对象
            model = genai.GenerativeModel(model_name)
            # 尝试生成
            response = model.generate_content([prompt, image])
            return f"✅ 成功连接模型: **{model_name}**\n\n" + response.text
        except Exception as e:
            last_error = str(e)
            continue # 如果失败，尝试列表里的下一个
            
    return f"❌ 所有模型尝试均失败。可能是 Key 无效或区域受限。\n最后一次报错: {last_error}"

def analyze_with_openai(image_bytes, key, prompt):
    from openai import OpenAI
    client = OpenAI(api_key=key)
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    try:
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": "你是一个黄金交易分析师。"},
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}
            ],
            max_tokens=1200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ OpenAI 连接失败: {str(e)}"

# 提示词
system_prompt = """
请扮演一位结合了“晚夜博主”趋势战法与“华尔街量化”因子的黄金分析师。
针对用户的 ETF (无杠杆) 交易需求，分析这张 K 线图。

【重点分析维度】：
1. **画线定位**：
   - 识别图中的【通道结构】：是急涨的蓝色通道，还是稳涨的紫色通道？
   - 找出【支撑位】：前低或 MA30 均线在哪里？
   
2. **量化排雷 (肉眼盲区)**：
   - **乖离率风险**：价格是否偏离 MA30 太远？(暗示回调风险)
   - **顶背离**：观察 MACD/RSI，是否有“价涨量缩”的诱多迹象？
   - **布林带**：是否极度收口(变盘前兆)或开口过大(超买)？

3. **操作指令 (ETF专属)**：
   - 给出明确建议：【买入半仓】、【满仓持有】 还是 【止盈减仓】？
   - 提醒：如果是 ETF，越跌越补的“万金油”点位在哪里（例如布林下轨）？

请用清晰的 Markdown 格式输出，包含【👁️ 盲区扫描】、【📐 关键点位】和【🛡️ 操作策略】。
"""

# ----------------- 界面交互 -----------------
if api_key:
    with col1:
        uploaded_file = st.file_uploader("📤 上传 K 线图", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            st.image(uploaded_file, caption="待分析盘面", use_column_width=True)
    
    with col2:
        if uploaded_file:
            st.subheader("🤖 AI 分析报告")
            img_bytes = uploaded_file.getvalue()
            
            if st.button("开始深度扫描", type="primary"):
                with st.spinner("正在自动寻找可用的 Gemini 模型..."):
                    if "Gemini" in model_provider:
                        result = analyze_with_gemini_auto(img_bytes, api_key, system_prompt)
                    else:
                        result = analyze_with_openai(img_bytes, api_key, system_prompt)
                    
                    st.markdown(result)
                    st.success("分析完成！")
else:
    st.info("👈 请在左侧选择 AI 引擎并输入 Key")
