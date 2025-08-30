import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from database import DatabaseManager
from main_pipeline import MisinformationDetectionPipeline

class MisinformationDashboard:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.pipeline = MisinformationDetectionPipeline()
    
    def load_data(self):
        """Load data from database"""
        return self.db_manager.get_all_classified_tweets()
    
    def create_classification_pie_chart(self, data):
        """Create pie chart showing classification distribution"""
        if not data:
            return None
        
        df = pd.DataFrame(data)
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
    
    def create_timeline_chart(self, data):
        """Create timeline showing classifications over time"""
        if not data:
            return None
        
        df = pd.DataFrame(data)
        df['classified_at'] = pd.to_datetime(df['classified_at'])
        df['date'] = df['classified_at'].dt.date
        
        # Group by date and classification
        timeline_data = df.groupby(['date', 'classification']).size().reset_index(name='count')
        
        fig = px.bar(
            timeline_data,
            x='date',
            y='count',
            color='classification',
            title="Classification Timeline",
            color_discrete_map={
                'Likely True': '#2E8B57',
                'Likely False': '#DC143C',
                'Misleading': '#FF8C00',
                'Unknown': '#808080'
            }
        )
        
        return fig
    
    def create_confidence_distribution(self, data):
        """Create histogram showing confidence distribution"""
        if not data:
            return None
        
        df = pd.DataFrame(data)
        
        # Filter out None confidence scores
        df_filtered = df[df['confidence_score'].notna()]
        
        if df_filtered.empty:
            return None
        
        fig = px.histogram(
            df_filtered,
            x='confidence_score',
            nbins=20,
            title="Classification Confidence Distribution",
            labels={'confidence_score': 'Confidence Score', 'count': 'Number of Tweets'}
        )
        
        return fig

def main():
    st.set_page_config(
        page_title="Misinformation Detection Dashboard",
        page_icon="🔍",
        layout="wide"
    )
    
    # Initialize dashboard
    dashboard = MisinformationDashboard()
    
    # Sidebar
    st.sidebar.title("🔍 Misinformation Detector")
    st.sidebar.markdown("---")
    
    # Main controls
    if st.sidebar.button("🔄 Refresh Data"):
        st.rerun()
    
    if st.sidebar.button("▶️ Run Pipeline"):
        with st.spinner("Running pipeline..."):
            summary = dashboard.pipeline.run_full_pipeline(max_tweets=20)
            st.sidebar.success("Pipeline completed!")
            st.sidebar.json(summary)
    
    # Data collection controls
    st.sidebar.subheader("Data Collection")
    
    keywords_input = st.sidebar.text_area(
        "Keywords (one per line)",
        value="vaccine misinformation\ncovid conspiracy\nclimate change hoax"
    )
    
    max_tweets = st.sidebar.slider("Max Tweets to Collect", 10, 500, 50)
    
    if st.sidebar.button("🎯 Collect Tweets"):
        keywords = [k.strip() for k in keywords_input.split('\n') if k.strip()]
        with st.spinner("Collecting tweets..."):
            count = dashboard.pipeline.collect_data(keywords, max_tweets)
            st.sidebar.success(f"Collected {count} tweets!")
    
    if st.sidebar.button("🤖 Classify Tweets"):
        with st.spinner("Classifying tweets..."):
            results = dashboard.pipeline.classify_tweets()
            st.sidebar.success(f"Classified {len(results)} tweets!")
    
    # Main dashboard
    st.title("🔍 Misinformation Detection Dashboard")
    st.markdown("Real-time analysis of social media misinformation")
    
    # Load and display data
    data = dashboard.load_data()
    
    if not data:
        st.warning("No data available. Please run the pipeline to collect and classify tweets.")
        return
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    df = pd.DataFrame(data)
    
    with col1:
        st.metric("Total Tweets", len(df))
    
    with col2:
        likely_false = len(df[df['classification'] == 'Likely False'])
        st.metric("Likely False", likely_false, delta=f"{likely_false/len(df)*100:.1f}%")
    
    with col3:
        misleading = len(df[df['classification'] == 'Misleading'])
        st.metric("Misleading", misleading, delta=f"{misleading/len(df)*100:.1f}%")
    
    with col4:
        likely_true = len(df[df['classification'] == 'Likely True'])
        st.metric("Likely True", likely_true, delta=f"{likely_true/len(df)*100:.1f}%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        pie_chart = dashboard.create_classification_pie_chart(data)
        if pie_chart:
            st.plotly_chart(pie_chart, use_container_width=True)
    
    with col2:
        timeline_chart = dashboard.create_timeline_chart(data)
        if timeline_chart:
            st.plotly_chart(timeline_chart, use_container_width=True)
    
    # Confidence distribution
    confidence_chart = dashboard.create_confidence_distribution(data)
    if confidence_chart:
        st.plotly_chart(confidence_chart, use_container_width=True)
    
    # Data table with filtering
    st.subheader("📊 Classified Tweets")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        classification_filter = st.selectbox(
            "Filter by Classification",
            options=['All'] + list(df['classification'].unique()),
            index=0
        )
    
    with col2:
        author_filter = st.selectbox(
            "Filter by Author",
            options=['All'] + list(df['author'].unique())[:20],  # Limit to first 20 authors
            index=0
        )
    
    with col3:
        date_filter = st.date_input(
            "Filter by Date (from)",
            value=datetime.now().date() - timedelta(days=7)
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if classification_filter != 'All':
        filtered_df = filtered_df[filtered_df['classification'] == classification_filter]
    
    if author_filter != 'All':
        filtered_df = filtered_df[filtered_df['author'] == author_filter]
    
    filtered_df['classified_at'] = pd.to_datetime(filtered_df['classified_at'])
    filtered_df = filtered_df[filtered_df['classified_at'].dt.date >= date_filter]
    
    # Display filtered data
    st.dataframe(
        filtered_df[['content', 'author', 'classification', 'reasoning', 'classified_at']],
        use_container_width=True,
        height=400
    )
    
    # Individual tweet analysis
    st.subheader("🔍 Tweet Analysis")
    
    if len(filtered_df) > 0:
        selected_tweet_idx = st.selectbox(
            "Select a tweet to analyze",
            options=range(len(filtered_df)),
            format_func=lambda x: f"Tweet {x+1}: {filtered_df.iloc[x]['content'][:100]}..."
        )
        
        selected_tweet = filtered_df.iloc[selected_tweet_idx]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Tweet Content:**")
            st.write(selected_tweet['content'])
            
            st.write("**Author:**", selected_tweet['author'])
            st.write("**Date:**", selected_tweet['date'])
            
            if 'url' in selected_tweet and selected_tweet['url']:
                st.write("**URL:**", selected_tweet['url'])
        
        with col2:
            st.write("**Classification:**", selected_tweet['classification'])
            st.write("**Reasoning:**")
            st.write(selected_tweet['reasoning'])
            
            if 'confidence_score' in selected_tweet and selected_tweet['confidence_score']:
                st.write("**Confidence Score:**", selected_tweet['confidence_score'])
            
            st.write("**Classified At:**", selected_tweet['classified_at'])
    
    # Export functionality
    st.subheader("📥 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export to CSV"):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"misinformation_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📈 Export Charts"):
            st.info("Chart export functionality would be implemented here")
    
    # Footer
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit | Misinformation Detection System")

if __name__ == "__main__":
    main()
