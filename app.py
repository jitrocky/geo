import streamlit as st
import openai  # 如果用Groq，替换为 from groq import Groq

# 设置页面标题
st.set_page_config(page_title="GEO Audit Tool", page_icon="🔍")
st.title("🔍 GEO内容审计工具 | Generative Engine Optimization Auditor")
st.write("输入任意语言的内容，AI帮您优化在ChatGPT/Perplexity中的可见度！报告用中文，优化文案保持原语言。新增：优化后重新评分对比。")

# API Key输入
api_key = st.sidebar.text_input("输入您的OpenAI API Key（测试后可隐藏）", type="password")
if not api_key:
    st.info("👈 先在侧边栏输入API Key")
    st.stop()

# 初始化客户端
client = openai.OpenAI(api_key=api_key)

# 输入区
content = st.text_area("输入内容（e.g., 产品描述）", placeholder="例如：This is a smartwatch with heart rate monitoring... 或 这是一款支持心率监测的智能手表...", height=150)

if st.button("🚀 开始审计", type="primary"):
    if not content:
        st.error("请输入内容！")
    else:
        with st.spinner("AI正在分析..."):
            try:
                # 第一步：分析原内容（得分 + 建议）
                prompt_original = f"""
                你是GEO专家。分析以下内容在生成式AI搜索（如ChatGPT）中的优化潜力。
                规则：
                - 自动检测输入内容的语言。
                - 输出结构用中文：
                  1. 当前得分（1-10分）：基于权威性（来源支持）、结构化（列表/标题）、用户意图匹配（直接回答问题）。用这个固定标准评分。
                  2. 问题点：3-5个改进建议（用中文）。
                - 整个报告用中文回复，简洁专业。
                内容：{content}
                """
                
                response_original = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt_original}]
                )
                original_result = response_original.choices[0].message.content
                
                # 提取原得分（简单解析，假设格式如“当前得分：7/10”）
                import re
                original_score_match = re.search(r'当前得分：(\d+)/10', original_result)
                original_score = int(original_score_match.group(1)) if original_score_match else 5  # 默认5
                
                # 第二步：生成优化版本
                prompt_optimize = f"""
                你是GEO专家。根据以下分析和建议，重写内容提升GEO潜力。
                规则：
                - 用输入内容的原语言重写。
                - 融入建议：提升权威性（加可靠来源）、结构化（用列表/小标题）、意图匹配（直接针对用户痛点）。
                - 保持原意，长度类似。
                原分析：{original_result}
                原内容：{content}
                输出：只输出优化后版本，无额外文字。
                """
                
                response_optimize = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt_optimize}]
                )
                optimized_content = response_optimize.choices[0].message.content.strip()
                
                # 第三步：重新评分优化版（用相同标准）
                prompt_rescore = f"""
                你是GEO专家。用与之前相同的固定标准（权威性、结构化、用户意图匹配）评分以下优化内容。
                输出结构用中文：
                1. 优化后得分（1-10分）。
                2. 对比：与原得分相比，提升点（用中文）。
                内容：{optimized_content}
                """
                
                response_rescore = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt_rescore}]
                )
                rescore_result = response_rescore.choices[0].message.content
                
                # 提取优化得分
                rescore_score_match = re.search(r'优化后得分：(\d+)/10', rescore_result)
                optimized_score = int(rescore_score_match.group(1)) if rescore_score_match else 5
                
                # 显示完整结果
                st.success("审计完成！")
                st.markdown("### 📊 原内容分析")
                st.markdown(original_result)
                
                st.markdown("### ✏️ 优化后版本")
                st.markdown(optimized_content)
                
                st.markdown("### 📈 优化后重新评分 & 对比")
                st.markdown(rescore_result)
                st.metric("得分变化", f"{optimized_score - original_score}分", delta=f"{optimized_score - original_score:+.0f}")
                
                # 下载
                full_report = f"原分析：\n{original_result}\n\n优化版本：\n{optimized_content}\n\n重新评分：\n{rescore_result}"
                st.download_button("💾 下载完整报告", data=full_report, file_name="geo_full_report.txt")
                
            except Exception as e:
                st.error(f"哎呀，出错了！错误信息：{str(e)}。检查API Key或网络。")
                st.info("提示：试试Groq免费API替换OpenAI。")

# 页脚
st.sidebar.markdown("---")
st.sidebar.info("基于Python + Streamlit | 支持任意语言 | 新增：优化后对比评分")
