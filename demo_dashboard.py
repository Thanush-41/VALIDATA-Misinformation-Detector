import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import os

def load_demo_data():
    """Load data from the demo database"""
    db_path = "data/demo.db"
    
    if not os.path.exists(db_path):
        return None
    
    conn = sqlite3.connect(db_path)
    
    query = '''
        SELECT t.content, t.author, t.date,
               c.classification, c.reasoning, c.confidence, c.created_at
        FROM tweets t
        JOIN classifications c ON t.tweet_id = c.tweet_id
        ORDER BY c.created_at DESC
    '''
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df

def create_classification_pie_chart(df):
    """Create pie chart showing classification distribution"""
    if df is None or df.empty:
        return None
    
    classification_counts = df['classification'].value_counts()
    
    fig = px.pie(
        values=classification_counts.values,
        names=classification_counts.index,
        title="Tweet Classification Distribution",
        color_discrete_map={
            'Likely True': '#2E8B57',
            'Likely False': '#DC143C', 
            'Misleading': '#FF8C00',
            'Unknown': '#808080'
        }
    )
    
    return fig

def create_confidence_chart(df):
    """Create bar chart showing confidence distribution"""
    if df is None or df.empty:
        return None
    
    confidence_counts = df['confidence'].value_counts()
    
    fig = px.bar(
        x=confidence_counts.index,
        y=confidence_counts.values,
        title="Classification Confidence Distribution",
        labels={'x': 'Confidence Level', 'y': 'Number of Tweets'},
        color=confidence_counts.values,
        color_continuous_scale='RdYlGn'
    )
    
    return fig

def main():
    st.set_page_config(
        page_title="Misinformation Detection Demo Dashboard",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 Misinformation Detection Demo Dashboard")
    st.markdown("Interactive analysis of social media misinformation detection results")
    
    # Load data
    df = load_demo_data()
    
    if df is None or df.empty:
        st.warning("⚠️ No data found! Please run the demo first:")
        st.code("python demo.py")
        st.stop()
    
    # Sidebar
    st.sidebar.title("🎛️ Controls")
    
    if st.sidebar.button("🔄 Refresh Data"):
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Filters
    st.sidebar.subheader("📊 Filters")
    
    classification_filter = st.sidebar.selectbox(
        "Filter by Classification",
        options=['All'] + list(df['classification'].unique()),
        index=0
    )
    
    confidence_filter = st.sidebar.selectbox(
        "Filter by Confidence",
        options=['All'] + list(df['confidence'].unique()),
        index=0
    )
    
    # Apply filters
    filtered_df = df.copy()
    
    if classification_filter != 'All':
        filtered_df = filtered_df[filtered_df['classification'] == classification_filter]
    
    if confidence_filter != 'All':
        filtered_df = filtered_df[filtered_df['confidence'] == confidence_filter]
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tweets", len(filtered_df))
    
    with col2:
        likely_false = len(filtered_df[filtered_df['classification'] == 'Likely False'])
        st.metric("Likely False", likely_false, delta=f"{likely_false/len(filtered_df)*100:.1f}%" if len(filtered_df) > 0 else "0%")
    
    with col3:
        misleading = len(filtered_df[filtered_df['classification'] == 'Misleading'])
        st.metric("Misleading", misleading, delta=f"{misleading/len(filtered_df)*100:.1f}%" if len(filtered_df) > 0 else "0%")
    
    with col4:
        likely_true = len(filtered_df[filtered_df['classification'] == 'Likely True'])
        st.metric("Likely True", likely_true, delta=f"{likely_true/len(filtered_df)*100:.1f}%" if len(filtered_df) > 0 else "0%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        pie_chart = create_classification_pie_chart(filtered_df)
        if pie_chart:
            st.plotly_chart(pie_chart, use_container_width=True)
    
    with col2:
        confidence_chart = create_confidence_chart(filtered_df)
        if confidence_chart:
            st.plotly_chart(confidence_chart, use_container_width=True)
    
    # Data table
    st.subheader("📋 Classified Tweets")
    
    if len(filtered_df) > 0:
        # Display data with custom styling
        for idx, row in filtered_df.iterrows():
            with st.expander(f"Tweet {idx + 1}: {row['content'][:60]}..."):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write("**Content:**")
                    st.write(row['content'])
                    st.write("**Reasoning:**")
                    st.write(row['reasoning'])
                
                with col2:
                    st.write("**Author:**", row['author'])
                    
                    # Color-coded classification
                    classification = row['classification']
                    if classification == 'Likely False':
                        st.error(f"🚫 {classification}")
                    elif classification == 'Likely True':
                        st.success(f"✅ {classification}")
                    else:
                        st.warning(f"⚠️ {classification}")
                    
                    st.write("**Confidence:**", row['confidence'])
                    st.write("**Date:**", row['date'])
    else:
        st.info("No tweets match the current filters.")
    
    # Statistics
    st.subheader("📈 Statistics")
    
    if len(df) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Classification Breakdown:**")
            classification_stats = df['classification'].value_counts()
            for classification, count in classification_stats.items():
                percentage = (count / len(df)) * 100
                st.write(f"- {classification}: {count} ({percentage:.1f}%)")
        
        with col2:
            st.write("**Confidence Breakdown:**")
            confidence_stats = df['confidence'].value_counts()
            for confidence, count in confidence_stats.items():
                percentage = (count / len(df)) * 100
                st.write(f"- {confidence}: {count} ({percentage:.1f}%)")
    
    # Export functionality
    st.subheader("📥 Export Data")
    
    if st.button("📊 Download Results as CSV"):
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="💾 Download CSV File",
            data=csv,
            file_name="misinformation_analysis_demo.csv",
            mime="text/csv"
        )
    
    # Information section
    st.sidebar.markdown("---")
    st.sidebar.subheader("ℹ️ About")
    st.sidebar.info(
        "This dashboard displays results from the misinformation detection demo. "
        "The system analyzes social media content and classifies it as 'Likely True', "
        "'Likely False', or 'Misleading' with explanatory reasoning."
    )
    
    st.sidebar.markdown("**Technologies Used:**")
    st.sidebar.markdown("- Rule-based classification")
    st.sidebar.markdown("- SQLite database")
    st.sidebar.markdown("- Streamlit dashboard")
    st.sidebar.markdown("- Plotly visualizations")
    
    # Footer
    st.markdown("---")
    st.markdown("🔍 **Misinformation Detection System Demo** | Built with Streamlit")

if __name__ == "__main__":
    main()
