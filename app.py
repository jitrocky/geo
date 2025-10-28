import streamlit as st
import openai  # 如果用Groq，替换为 from groq import Groq

# 设置页面标题
st.set_page_config(page_title="GEO Audit Tool", page_icon="🔍")
st.title("🔍 GEO内容审计工具 | Generative Engine Optimization Auditor")
st.write("输入任意语言的内容，AI帮您优化在ChatGPT/Perplexity中的可见度！报告用中文，优化文案保持原语言。")

# API Key输入（安全起见，让用户本地输入）
api_key = st.sidebar.text_input("输入您的OpenAI API Key（测试后可隐藏）", type="password")
if not api_key:
    st.info("👈 先在侧边栏输入API Key")
    st.stop()

# 初始化客户端（OpenAI示例；Groq替换：client = Groq(api_key=api_key)）
client = openai.OpenAI(api_key=api_key)

# 输入区（任意语言）
content = st.text_area("输入内容（e.g., 产品描述）", placeholder="例如：This is a smartwatch with heart rate monitoring... 或 这是一款支持心率监测的智能手表...", height=150)

if st.button("🚀 开始审计", type="primary"):
    if not content:
        st.error("请输入内容！")
    else:
        with st.spinner("AI正在分析..."):
            try:
                # GEO优化Prompt（自动处理语言：报告中文，优化文案原语言）
                prompt = f"""
                你是GEO专家。分析以下内容在生成式AI搜索（如ChatGPT）中的优化潜力。
                规则：
                - 自动检测输入内容的语言（e.g., English, Chinese, French）。
                - 输出结构用中文：
                  1. 当前得分（1-10分）：基于权威性、结构化、用户意图匹配。
                  2. 问题点：3-5个改进建议（用中文）。
                  3. 优化后版本：用输入内容的原语言重写，提升AI引用率。
                - 整个报告用中文回复，简洁专业。
                内容：{content}
                """
                
                # 调用API
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",  # 便宜版；升级到gpt-4o-mini
                    messages=[{"role": "user", "content": prompt}]
                )
                audit_result = response.choices[0].message.content
                
                # 显示结果
                st.success("审计完成！")
                st.markdown("### 📊 审计报告")
                st.markdown(audit_result)
                
                # 下载优化版本
                st.download_button("💾 下载优化内容", data=audit_result, file_name="geo_optimized.txt")
                
            except Exception as e:
                st.error(f"哎呀，出错了！错误信息：{str(e)}。检查API Key或网络。")
                st.info("提示：试试Groq免费API替换OpenAI。")

# 页脚
st.sidebar.markdown("---")
st.sidebar.info("基于Python + Streamlit | 支持任意语言 | 扩展：加法语支持或数据库")                用{lang}回复，简洁专业。
                """
                
                # 调用API
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",  # 便宜版；升级到gpt-4o-mini
                    messages=[{"role": "user", "content": prompt}]
                )
                audit_result = response.choices[0].message.content
                
                # 显示结果
                st.success("审计完成！")
                st.markdown("### 📊 审计报告")
                st.markdown(audit_result)
                
                # 下载优化版本
                st.download_button("💾 下载优化内容", data=audit_result, file_name="geo_optimized.txt")
                
            except Exception as e:
                st.error(f"哎呀，出错了！错误信息：{str(e)}。检查API Key或网络。")
                st.info("提示：试试Groq免费API替换OpenAI。")

# 页脚
st.sidebar.markdown("---")
st.sidebar.info("基于Python + Streamlit | 扩展：加法语支持或数据库")
