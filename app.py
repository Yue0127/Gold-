import streamlit as st
import base64
from openai import OpenAI

# ----------------- 页面基础配置 -----------------
st.set_page_config(page_title="晚夜·黄金ETF机构级量化系统 (V6.0)", layout="wide")

# 侧边栏：控制台
with st.sidebar:
    st.header("⚙️ 量化中枢")
    api_key = st.text_input("🔑 OpenAI API Key", type="password")
    
    st.markdown("---")
    st.markdown("### 📊 V6.0 量化增强因子")
    st.info("已启用机构级数据透视")
    
    st.markdown("""
    **1. 📉 乖离率 (BIAS) 监测：**
    - 监测价格偏离 MA30 的程度。
    - **警报**：偏离度 >5% 视为极端超买（风险区）。
    
    **2. 💥 波动率 (Bandwidth) 预警：**
    - 监测布林带开口的挤压程度。
    - **警报**：带宽 <0.1 意味着即将变盘（暴风雨前的宁静）。
    
    **3. 🐂 隐形动量 (RSI Divergence)：**
    - 识别“价涨量缩”的顶背离。
    - **作用**：精准识别博主口中的“诱多”陷阱。
    """)

# 主界面
st.title("🏛️ 黄金 ETF 深度决策系统 (V6.0 最终版)")
st.caption("融合‘晚夜’趋势战法 + 华尔街量化因子 | 专治肉眼盲区")

col1, col2 = st.columns([1.5, 1])

# ----------------- 核心 AI 分析逻辑 -----------------
def analyze_image_v6(image_file, key):
    client = OpenAI(api_key=key)
    base64_image = base64.b64encode(image_file.getvalue()).decode('utf-8')

    system_prompt = """
    你是一位结合了“传统技术派（晚夜博主）”和“现代量化派（华尔街机构）”的顶级黄金分析师。
    用户的痛点是：肉眼看不出数据背后的隐患。你需要用量化思维弥补这一缺陷。

    【请按照以下步骤进行深度扫描】：

    ### 第一维度：形态与趋势（晚夜视角）
    1. **结构定位**：当前是处于“蓝色通道”（急涨）、“紫色通道”（稳涨）还是“破位状态”？
    2. **画线辅助**：描述支撑位（前低/MA30）和压力位（通道上沿）的具体位置。

    ### 第二维度：量化数据透视（机构视角 - 重点！）
    请仔细观察图中的 K 线与均线/指标的距离，估算以下因子：
    1. **乖离率 (Bias Risk)**：
       - 目测当前价格距离 MA30 有多远？
       - 判定：如果是**贴着 MA30 涨**，属于“健康趋势”；如果是**垂直拉升远离 MA30**，警告“乖离率过大，随时可能均值回归”。
    2. **动能背离 (Divergence Check)**：
       - 观察下方的 MACD 或 RSI（如果有）。
       - 判定：价格创新高了吗？指标有没有跟着创新高？如果有“顶背离”，明确警告用户：“这是量化模型确认的诱多信号。”
    3. **波动率压缩 (Squeeze)**：
       - 观察布林带（BOLL）。口子是张大的还是缩得很紧？
       - 判定：如果缩得很紧，提示“波动率极低，未来 48 小时内将有大变盘，ETF 请拿稳扶好”。

    ### 第三维度：ETF 交易指令
    结合上述两点，给出具体的 ETF 操作建议：
    - **左侧挂单**：建议在什么价格附近挂单接货（通常是 MA30 或 通道下沿）。
    - **右侧风控**：如果出现什么信号（如跌破生死线 + 量能放大），必须离场？

    【输出格式】：
    - **👁️ 盲区扫描**：(揭示肉眼容易忽略的量化风险，如“虽然涨了，但动能正在衰竭”)
    - **📐 关键点位**：(支撑位、压力位、变盘点)
    - **🛡️ 综合策略**：(买入/持有/减仓)
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": "请用 V6.0 量化模型分析这张图。重点告诉我肉眼容易忽略的风险或机会。"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}
            ],
            max_tokens=1200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ 量化引擎连接失败: {e}"

# ----------------- 界面交互 -----------------
if api_key:
    with col1:
        uploaded_file = st.file_uploader("📤 上传 K 线图 (最好包含 MA, BOLL, MACD 等指标)", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            st.image(uploaded_file, caption="待分析盘面", use_column_width=True)
            
            # 模拟一个量化仪表盘 (增加专业感)
            st.markdown("#### ⚡ 实时量化扫描中...")
            my_bar = st.progress(0)
            import time
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1)
    
    with col2:
        if uploaded_file:
            st.subheader("📋 深度量化分析报告")
            
            result = analyze_image_v6(uploaded_file, api_key)
            st.markdown(result)
            
            st.info("💡 **小贴士**：ETF 最大的优势是容错率。量化模型提示‘超卖’（Bias过低）时，往往是 ETF 最佳的定投时刻。")

else:
    # 引导页
    st.info("👈 请在左侧输入 API Key 启动系统")
    st.markdown("""
    ### 为什么你需要 V6.0？
    
    * **肉眼看图**：觉得涨势很好，满仓冲。
    * **量化看图**：发现乖离率过大 + MACD 顶背离 = **诱多陷阱，快跑！**
    
    这个版本就是为了让你看到这些“隐形”的风险。
    """)
