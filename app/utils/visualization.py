import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from app.models.models import Keyword, Ranking, Cluster
from app.database.database import get_db

class DataVisualizer:
    def __init__(self, db_session):
        self.db = db_session
    
    def create_ranking_comparison_chart(self, keyword_id):
        """
        Create a comparison chart of rankings across platforms
        """
        # Get rankings for the keyword
        rankings = self.db.query(Ranking).filter(Ranking.keyword_id == keyword_id).all()
        
        if not rankings:
            return None
        
        # Prepare data for plotting
        platforms = [r.platform for r in rankings]
        positions = [r.position if r.position else 0 for r in rankings]
        visibility_scores = [r.visibility_score if r.visibility_score else 0 for r in rankings]
        
        # Create subplot with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add position bars
        fig.add_trace(
            go.Bar(x=platforms, y=positions, name="Position", marker_color="blue"),
            secondary_y=False,
        )
        
        # Add visibility score line
        fig.add_trace(
            go.Scatter(x=platforms, y=visibility_scores, mode='lines+markers', name="Visibility Score", line=dict(color='red')),
            secondary_y=True,
        )
        
        # Set axis titles
        fig.update_xaxes(title_text="Platform")
        fig.update_yaxes(title_text="Position", secondary_y=False)
        fig.update_yaxes(title_text="Visibility Score (%)", secondary_y=True)
        
        # Update layout
        fig.update_layout(
            title="Keyword Ranking Comparison Across Platforms",
            showlegend=True
        )
        
        return fig.to_json()
    
    def create_keyword_cluster_map(self):
        """
        Create a visualization of keyword clusters
        """
        # Get all clusters and their keywords
        clusters = self.db.query(Cluster).all()
        
        if not clusters:
            return None
        
        # Prepare data for plotting
        cluster_names = []
        keyword_counts = []
        
        for cluster in clusters:
            cluster_names.append(cluster.name)
            keyword_count = len(cluster.keywords)
            keyword_counts.append(keyword_count)
        
        # Create bar chart
        fig = go.Figure(data=[
            go.Bar(x=cluster_names, y=keyword_counts, marker_color='indianred')
        ])
        
        fig.update_layout(
            title="Keyword Cluster Distribution",
            xaxis_title="Clusters",
            yaxis_title="Number of Keywords"
        )
        
        return fig.to_json()
    
    def create_visibility_trend_chart(self, keyword_id, days=30):
        """
        Create a trend chart showing visibility score over time
        """
        # Get historical rankings for the keyword
        rankings = self.db.query(Ranking).filter(
            Ranking.keyword_id == keyword_id
        ).order_by(Ranking.timestamp.desc()).limit(days).all()
        
        if not rankings:
            return None
        
        # Prepare data for plotting
        dates = [r.timestamp for r in rankings]
        visibility_scores = [r.visibility_score if r.visibility_score else 0 for r in rankings]
        
        # Create line chart
        fig = go.Figure()
        
        fig.add_trace(
            go.Scatter(x=dates, y=visibility_scores, mode='lines+markers', name="Visibility Score")
        )
        
        fig.update_layout(
            title="Keyword Visibility Score Trend",
            xaxis_title="Date",
            yaxis_title="Visibility Score (%)"
        )
        
        return fig.to_json()
    
    def create_keyword_difficulty_scatter(self):
        """
        Create a scatter plot showing keyword volume vs difficulty
        """
        # Get all keywords
        keywords = self.db.query(Keyword).all()
        
        if not keywords:
            return None
        
        # Prepare data for plotting
        volumes = [k.volume if k.volume else 0 for k in keywords]
        difficulties = [k.difficulty if k.difficulty else 0 for k in keywords]
        keyword_texts = [k.keyword for k in keywords]
        
        # Create scatter plot
        fig = go.Figure(data=go.Scatter(
            x=volumes,
            y=difficulties,
            mode='markers',
            marker=dict(
                size=10,
                color=difficulties,
                colorscale='Viridis',
                showscale=True
            ),
            text=keyword_texts,
            textposition="top center"
        ))
        
        fig.update_layout(
            title="Keyword Volume vs Difficulty",
            xaxis_title="Search Volume",
            yaxis_title="Keyword Difficulty"
        )
        
        return fig.to_json()