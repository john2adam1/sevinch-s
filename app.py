import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Employee Motivation & Stress Tracker",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'user'
if 'test_completed' not in st.session_state:
    st.session_state.test_completed = False

# Function to initialize CSV file
def initialize_csv():
    if not os.path.exists('results.csv'):
        df = pd.DataFrame(columns=[
            'Name', 'Department', 'Date', 
            'Internal_Motivation_Score', 'External_Motivation_Score',
            'Stress_Level_Score', 'Burnout_Risk_Score',
            'Rule_Based_Advice'
        ])
        df.to_csv('results.csv', index=False)

# Function to save results to CSV
def save_results(name, dept, scores, advice):
    new_row = {
        'Name': name,
        'Department': dept,
        'Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Internal_Motivation_Score': scores['internal'],
        'External_Motivation_Score': scores['external'],
        'Stress_Level_Score': scores['stress'],
        'Burnout_Risk_Score': scores['burnout'],
        'Rule_Based_Advice': advice
    }
    
    df = pd.read_csv('results.csv')
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv('results.csv', index=False)

# Function to get rule-based analysis
def get_rule_based_analysis(scores, name, department):
    
    # Classify motivation type
    total_motivation = (scores['internal'] + scores['external']) / 2
    
    if scores['internal'] >= 8:
        motivation_type = "High Internal Motivation"
        motivation_status = "success"
    elif scores['internal'] >= 6:
        motivation_type = "Moderate Internal Motivation"
        motivation_status = "info"
    elif scores['external'] >= 7:
        motivation_type = "High External/Low Motivation"
        motivation_status = "warning"
    else:
        motivation_type = "Low Motivation"
        motivation_status = "error"
    
    # Classify stress level
    avg_stress = (scores['stress'] + scores['burnout']) / 2
    
    if avg_stress >= 7:
        stress_type = "High Stress/Risk of Burnout"
        stress_status = "error"
    elif avg_stress >= 5:
        stress_type = "Moderate Stress"
        stress_status = "warning"
    else:
        stress_type = "Healthy Stress Level"
        stress_status = "success"
    
    # Generate recommendations based on scores
    recommendations = []
    
    # Stress-based recommendations
    if scores['stress'] >= 7:
        recommendations.append("🧘 Take regular short breaks and practice deep breathing exercises.")
        recommendations.append("💬 Consider talking to your supervisor about workload management.")
    elif scores['stress'] >= 5:
        recommendations.append("⚖️ Focus on work-life balance and set clear boundaries.")
        recommendations.append("🚶 Incorporate physical activity into your daily routine.")
    
    # Burnout-based recommendations
    if scores['burnout'] >= 7:
        recommendations.append("🛑 Take immediate action to prevent burnout - consider time off.")
        recommendations.append("🤝 Seek support from HR or a mental health professional.")
    elif scores['burnout'] >= 5:
        recommendations.append("🎯 Reconnect with your personal values and work purpose.")
        recommendations.append("📅 Schedule regular breaks and vacation time.")
    
    # Motivation-based recommendations
    if scores['internal'] < 4:
        recommendations.append("🌟 Try to find personal growth goals within your current tasks.")
        recommendations.append("🔍 Identify aspects of your work that align with your values.")
    elif scores['external'] > 8 and scores['internal'] < 6:
        recommendations.append("⚖️ Balance external rewards with internal satisfaction.")
        recommendations.append("🎖️ Focus on the meaning behind your work, not just rewards.")
    
    # Add positive reinforcement
    if scores['internal'] >= 7:
        recommendations.append("🎉 Excellent! Your strong internal motivation is a great asset.")
    if avg_stress < 4:
        recommendations.append("💚 Great job maintaining healthy stress levels!")
    
    # Format the advice
    advice = f"### {motivation_type} | {stress_type}\n\n"
    advice += "**Personalized Recommendations:**\n\n"
    for rec in recommendations:
        advice += f"• {rec}\n"
    
    # Add overall status summary
    advice += f"\n---\n**Overall Status:** "
    if avg_stress < 4 and scores['internal'] >= 6:
        advice += "🟢 **Excellent** - You're in a great position!"
    elif avg_stress < 6 and scores['internal'] >= 5:
        advice += "🟡 **Good** - Keep monitoring your wellness."
    else:
        advice += "🔴 **Needs Attention** - Focus on the recommendations above."
    
    return advice, motivation_type, stress_type, motivation_status, stress_status

# Sidebar navigation
st.sidebar.title("🧠 Employee Wellness Tracker")
page = st.sidebar.radio("Navigate", ["Employee Test", "Admin Dashboard"])

# Initialize CSV file
initialize_csv()

if page == "Employee Test":
    st.title("🧠 Employee Motivation & Stress Assessment")
    st.markdown("---")
    
    # User Profile Section
    st.header("👤 User Profile")
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Enter your name:", placeholder="John Doe")
    
    with col2:
        department = st.selectbox("Select your department:", 
                                ["Engineering", "Sales", "Marketing", "HR", "Finance", "Operations", "Other"])
    
    if not name:
        st.warning("Please enter your name to proceed.")
        st.stop()
    
    st.markdown("---")
    
    # Motivation and Stress Test
    st.header("📋 Assessment Questions")
    st.write("Please answer all questions honestly. This will help us provide you with personalized recommendations.")
    
    # Questions for Internal vs External Motivation
    st.subheader("🎯 Motivation Assessment")
    
    q1 = st.radio("1. I work because I find the tasks inherently interesting and enjoyable:", 
                  ["Never", "Rarely", "Sometimes", "Often", "Always"], index=2)
    q2 = st.radio("2. I am motivated by external rewards like bonuses and recognition:", 
                  ["Never", "Rarely", "Sometimes", "Often", "Always"], index=2)
    q3 = st.radio("3. I feel a sense of personal accomplishment when I complete my work:", 
                  ["Never", "Rarely", "Sometimes", "Often", "Always"], index=2)
    q4 = st.radio("4. I work mainly to meet others' expectations:", 
                  ["Never", "Rarely", "Sometimes", "Often", "Always"], index=2)
    q5 = st.radio("5. I am driven by my own values and beliefs in my work:", 
                  ["Never", "Rarely", "Sometimes", "Often", "Always"], index=2)
    
    # Stress and Burnout Questions
    st.subheader("😰 Stress & Burnout Assessment")
    
    q6 = st.radio("6. I feel emotionally drained from my work:", 
                  ["Never", "Rarely", "Sometimes", "Often", "Always"], index=2)
    q7 = st.radio("7. I have trouble sleeping due to work-related stress:", 
                  ["Never", "Rarely", "Sometimes", "Often", "Always"], index=2)
    q8 = st.radio("8. I feel cynical or detached from my work:", 
                  ["Never", "Rarely", "Sometimes", "Often", "Always"], index=2)
    q9 = st.radio("9. I have enough time and resources to complete my work effectively:", 
                  ["Never", "Rarely", "Sometimes", "Often", "Always"], index=3)
    q10 = st.radio("10. I feel satisfied with my work-life balance:", 
                   ["Never", "Rarely", "Sometimes", "Often", "Always"], index=2)
    
    # Calculate scores
    def calculate_score(response):
        score_map = {"Never": 1, "Rarely": 2, "Sometimes": 3, "Often": 4, "Always": 5}
        return score_map[response]
    
    if st.button("🚀 Submit Assessment", type="primary"):
        # Calculate motivation scores
        internal_motivation = (calculate_score(q1) + calculate_score(q3) + calculate_score(q5)) * 2/3
        external_motivation = (calculate_score(q2) + calculate_score(q4)) * 2/2
        
        # Calculate stress scores
        stress_level = (calculate_score(q6) + calculate_score(q7)) * 2/2
        burnout_risk = (calculate_score(q8) + (6 - calculate_score(q9)) + (6 - calculate_score(q10))) * 2/3
        
        scores = {
            'internal': round(internal_motivation, 1),
            'external': round(external_motivation, 1),
            'stress': round(stress_level, 1),
            'burnout': round(burnout_risk, 1)
        }
        
        # Get rule-based analysis
        with st.spinner("Generating personalized recommendations..."):
            advice, motivation_type, stress_type, motivation_status, stress_status = get_rule_based_analysis(scores, name, department)
        
        # Save results
        save_results(name, department, scores, advice)
        
        # Display results
        st.success("✅ Assessment completed successfully!")
        st.markdown("---")
        
        st.header("📊 Your Results")
        
        # Score visualization
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Motivation Profile")
            fig_motivation = go.Figure(data=[
                go.Bar(name='Internal Motivation', x=[''], y=[scores['internal']], marker_color='#4CAF50'),
                go.Bar(name='External Motivation', x=[''], y=[scores['external']], marker_color='#2196F3')
            ])
            fig_motivation.update_layout(barmode='group', yaxis=dict(range=[0, 10]))
            st.plotly_chart(fig_motivation, use_container_width=True)
            
        with col2:
            st.subheader("😰 Stress Profile")
            fig_stress = go.Figure(data=[
                go.Bar(name='Stress Level', x=[''], y=[scores['stress']], marker_color='#FF9800'),
                go.Bar(name='Burnout Risk', x=[''], y=[scores['burnout']], marker_color='#F44336')
            ])
            fig_stress.update_layout(barmode='group', yaxis=dict(range=[0, 10]))
            st.plotly_chart(fig_stress, use_container_width=True)
        
        # Status Badges
        col1, col2 = st.columns(2)
        with col1:
            if motivation_status == "success":
                st.success(f"🎯 {motivation_type}")
            elif motivation_status == "info":
                st.info(f"🎯 {motivation_type}")
            elif motivation_status == "warning":
                st.warning(f"🎯 {motivation_type}")
            else:
                st.error(f"🎯 {motivation_type}")
                
        with col2:
            if stress_status == "success":
                st.success(f"😰 {stress_type}")
            elif stress_status == "warning":
                st.warning(f"😰 {stress_type}")
            else:
                st.error(f"😰 {stress_type}")
        
        # Rule-Based Advice
        st.subheader("🤖 Personalized Recommendations")
        st.markdown(advice)
        
        st.session_state.test_completed = True

else:  # Admin Dashboard
    st.title("📊 Admin Dashboard")
    st.markdown("---")
    
    # Check if CSV exists and has data
    try:
        df = pd.read_csv('results.csv')
        
        if df.empty:
            st.warning("No assessment data available yet.")
        else:
            # Summary Statistics
            st.header("📈 Overview Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Assessments", len(df))
            with col2:
                avg_stress = df['Stress_Level_Score'].mean()
                st.metric("Avg Stress Level", f"{avg_stress:.1f}/10")
            with col3:
                avg_burnout = df['Burnout_Risk_Score'].mean()
                st.metric("Avg Burnout Risk", f"{avg_burnout:.1f}/10")
            with col4:
                dept_count = df['Department'].nunique()
                st.metric("Departments", dept_count)
            
            st.markdown("---")
            
            # Department-wise Analysis
            st.header("🏢 Department Analysis")
            
            # Average stress by department
            dept_stress = df.groupby('Department')['Stress_Level_Score'].mean().reset_index()
            fig_dept_stress = px.bar(dept_stress, x='Department', y='Stress_Level_Score', 
                                    title='Average Stress Level by Department',
                                    color='Stress_Level_Score', color_continuous_scale='RdYlGn_r')
            st.plotly_chart(fig_dept_stress, use_container_width=True)
            
            # Average burnout risk by department
            dept_burnout = df.groupby('Department')['Burnout_Risk_Score'].mean().reset_index()
            fig_dept_burnout = px.bar(dept_burnout, x='Department', y='Burnout_Risk_Score', 
                                      title='Average Burnout Risk by Department',
                                      color='Burnout_Risk_Score', color_continuous_scale='RdYlGn_r')
            st.plotly_chart(fig_dept_burnout, use_container_width=True)
            
            # Motivation analysis by department
            st.subheader("🎯 Motivation Analysis by Department")
            dept_motivation = df.groupby('Department')[['Internal_Motivation_Score', 'External_Motivation_Score']].mean().reset_index()
            
            fig_motivation = go.Figure()
            fig_motivation.add_trace(go.Bar(name='Internal Motivation', x=dept_motivation['Department'], 
                                          y=dept_motivation['Internal_Motivation_Score'], marker_color='#4CAF50'))
            fig_motivation.add_trace(go.Bar(name='External Motivation', x=dept_motivation['Department'], 
                                          y=dept_motivation['External_Motivation_Score'], marker_color='#2196F3'))
            fig_motivation.update_layout(barmode='group', title='Motivation Profile by Department')
            st.plotly_chart(fig_motivation, use_container_width=True)
            
            st.markdown("---")
            
            # Detailed Results Table
            st.header("📋 Detailed Assessment Results")
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                selected_dept = st.selectbox("Filter by Department:", ["All"] + list(df['Department'].unique()))
            with col2:
                date_range = st.date_input("Filter by Date Range:", [])
            
            # Apply filters
            filtered_df = df.copy()
            if selected_dept != "All":
                filtered_df = filtered_df[filtered_df['Department'] == selected_dept]
            
            if len(date_range) == 2:
                filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
                start_date = pd.to_datetime(date_range[0])
                end_date = pd.to_datetime(date_range[1])
                filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]
            
            # Display table
            st.dataframe(filtered_df, use_container_width=True)
            
            # Export option
            if st.button("📥 Export Filtered Results"):
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"employee_wellness_results_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
    
    except FileNotFoundError:
        st.error("No data file found. Please ensure assessments have been completed.")
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")

# Footer
st.markdown("---")
st.markdown("💚 *Employee Wellness Tracker - Supporting mental health and motivation in the workplace*")
