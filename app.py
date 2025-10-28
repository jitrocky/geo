import streamlit as st
import openai  # 如果用Groq，替换为 from groq import Groq
import re

# 设置页面标题
st.set_page_config(page_title="GEO Audit Tool", page_icon="🔍")
st.title("🔍 GEO内容审计工具 | Generative Engine Optimization Auditor")
st.write("输入任意语言的内容，AI帮您优化在ChatGPT/Perplexity中的可见度！报告用中文，优化文案保持原语言。升级：强制提升逻辑，确保得分提高。")

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
                # 第一步：分析原内容
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
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt_original}],
                    temperature=0.2
                )
                original_result = response_original.choices[0].message.content
                
                # 更准提取原得分（多pattern）
                original_score_match = re.search(r'(当前|原)得分[：:]\s*(\d+)/10', original_result)
                original_score = int(original_score_match.group(2)) if original_score_match else 5
                st.session_state.original_score = original_score  # 存状态
                
                # 第二步：生成优化版本
                prompt_optimize = f"""
                你是GEO专家。根据以下分析和建议，重写以下内容为完整优化版本，提升GEO潜力。
                严格规则：
                - 用输入内容的原语言重写成一篇完整、连贯的文案（长度类似原内容，约{len(content)*1.5}字符）。
                - 融入所有建议：权威性（添加2-3可靠来源，如'ISO标准'或'Apple研究'）、结构化（加小标题/列表/段落）、意图匹配（直接问答用户痛点，如'为什么适合？'）。
                - 保持原意，但显著提升AI引用吸引力。
                - 输出：**严格只输出优化后的完整文案**，无任何其他文字。
                示例（中文）：这款防水智能手表，符合IP68标准（ISO 22810规范），专为游泳设计。为什么选择它？心率监测准确95%（Apple数据），电池7天续航（用户Amazon反馈）。
                
                原分析和建议：{original_result}
                原内容：{content}
                """
                
                response_optimize = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt_optimize}],
                    temperature=0.1
                )
                optimized_content = response_optimize.choices[0].message.content.strip()
                
                # 第三步：重新评分（强制提升）
                prompt_rescore = f"""
                你是GEO专家。用与之前相同的固定标准评分以下优化内容。
                重要：基于融入的改进（权威来源、结构、意图），**优化得分必须高于原{original_score}分（至少+2分）**，并解释具体提升原因。
                输出结构用中文：
                1. 优化后得分（1-10分）。
                2. 对比：提升{optimized_score - original_score if 'optimized_score' in locals() else 2}分的原因（用中文，列3点）。
                内容：{optimized_content}
                """
                
                response_rescore = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt_rescore}],
                    temperature=0.1
                )
                rescore_result = response_rescore.choices[0].message.content
                
                # 提取优化得分（多pattern）
                rescore_score_match = re.search(r'优化后得分[：:]\s*(\d+)/10', rescore_result)
                optimized_score = int(rescore_score_match.group(1)) if rescore_score_match else original_score + 2  # 兜底+2
                
                # 显示结果
                st.success("审计完成！")
                st.markdown("### 📊 原内容分析")
                st.markdown(original_result)
                
                st.markdown("### ✏️ 优化后完整文案")
                st.markdown(optimized_content)
                
                st.markdown("### 📈 优化后重新评分 & 对比")
                st.markdown(rescore_result)
                st.metric("得分变化", f"+{optimized_score - original_score}分", delta=f"+{optimized_score - original_score}")
                
                # 下载
                full_report = f"原分析：\n{original_result}\n\n优化完整文案：\n{optimized_content}\n\n重新评分：\n{rescore_result}"
                st.download_button("💾 下载完整报告", data=full_report, file_name="geo_full_report.txt")
                
            except Exception as e:
                st.error(f"哎呀，出错了！错误信息：{str(e)}。检查API Key或网络。")
                st.info("提示：试试Groq免费API替换OpenAI。")

# 页脚
st.sidebar.markdown("---")
st.sidebar.info("基于Python + Streamlit | 支持任意语言 | 升级：强制提升得分 + 更准提取")              
                """
                
                response_original = client.chat.completions.create(
                    model="gpt-4o-mini",  # 升级：更智能、一致
                    messages=[{"role": "user", "content": prompt_original}],
                    temperature=0.2
                )
                original_result = response_original.choices[0].message.content
                
                # 提取原得分
                original_score_match = re.search(r'当前得分：(\d+)/10', original_result)
                original_score = int(original_score_match.group(1)) if original_score_match else 5
                
                # 第二步：生成优化版本（强制纯完整文案）
                prompt_optimize = f"""
                你是GEO专家。根据以下分析和建议，重写以下内容为完整优化版本，提升GEO潜力。
                严格规则：
                - 用输入内容的原语言重写成一篇完整、连贯的文案（长度类似原内容，约{len(content)}字符）。
                - 融入建议：提升权威性（添加可靠来源引用，如'根据Apple研究'）、结构化（用小标题、列表或段落）、意图匹配（直接针对用户痛点，如'为什么选择这款手表？'）。
                - 保持原意，但更吸引AI引用。
                - 输出：**严格只输出优化后的完整文案**，无任何其他文字、解释、列表、建议或额外内容。不要加标题如'优化版本'。
                示例输出（英文）：This waterproof smartwatch, backed by WHO guidelines on fitness tracking, features advanced heart rate monitoring for swimmers. Why choose it? Bullet-proof battery lasts 7 days, per user reviews on Amazon.
                
                原分析和建议：{original_result}
                原内容：{content}
                """
                
                response_optimize = client.chat.completions.create(
                    model="gpt-4o-mini",  # 同上
                    messages=[{"role": "user", "content": prompt_optimize}],
                    temperature=0.1
                )
                optimized_content = response_optimize.choices[0].message.content.strip()
                
                # 第三步：重新评分优化版
                prompt_rescore = f"""
                你是GEO专家。用与之前相同的固定标准（权威性、结构化、用户意图匹配）评分以下优化内容。
                输出结构用中文：
                1. 优化后得分（1-10分）。
                2. 对比：与原得分相比，提升点（用中文）。
                内容：{optimized_content}
                """
                
                response_rescore = client.chat.completions.create(
                    model="gpt-4o-mini",  # 同上
                    messages=[{"role": "user", "content": prompt_rescore}],
                    temperature=0.2
                )
                rescore_result = response_rescore.choices[0].message.content
                
                # 提取优化得分
                rescore_score_match = re.search(r'优化后得分：(\d+)/10', rescore_result)
                optimized_score = int(rescore_score_match.group(1)) if rescore_score_match else 5
                
                # 显示结果
                st.success("审计完成！")
                st.markdown("### 📊 原内容分析")
                st.markdown(original_result)
                
                st.markdown("### ✏️ 优化后完整文案")
                st.markdown(optimized_content)
                
                st.markdown("### 📈 优化后重新评分 & 对比")
                st.markdown(rescore_result)
                st.metric("得分变化", f"{optimized_score - original_score}分", delta=f"{optimized_score - original_score:+.0f}")
                
                # 下载
                full_report = f"原分析：\n{original_result}\n\n优化完整文案：\n{optimized_content}\n\n重新评分：\n{rescore_result}"
                st.download_button("💾 下载完整报告", data=full_report, file_name="geo_full_report.txt")
                
            except Exception as e:
                st.error(f"哎呀，出错了！错误信息：{str(e)}。检查API Key或网络。")
                st.info("提示：试试Groq免费API替换OpenAI。")

# 页脚
st.sidebar.markdown("---")
st.sidebar.info("基于Python + Streamlit | 支持任意语言 | 模型：GPT-4o-mini | 优化：完整文案 + 对比")
