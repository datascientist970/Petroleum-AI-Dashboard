# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from pathlib import Path
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime, timedelta
import random
import io
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

REALTIME_FILE = Path("analytics/realtime_data.csv")

def generate_sample_data():
    """Generate sample data if file doesn't exist"""
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    data = {
        'Date': dates,
        'Brent': np.random.uniform(80, 90, 30).cumsum() / 10 + 70,
        'WTI': np.random.uniform(75, 85, 30).cumsum() / 10 + 65,
        'NaturalGas': np.random.uniform(2.5, 3.5, 30).cumsum() / 10 + 2
    }
    df = pd.DataFrame(data)
    
    # Save sample data for future use
    df.to_csv(REALTIME_FILE, index=False)
    
    return df

def load_or_generate_data(time_range='30days', asset_filter='All Commodities'):
    """Load data with filters"""
    if not REALTIME_FILE.exists():
        df = generate_sample_data()
    else:
        df = pd.read_csv(REALTIME_FILE)
    
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    
    # Apply time range filter
    end_date = df['Date'].max()
    if time_range == 'today':
        start_date = end_date - pd.Timedelta(days=1)
    elif time_range == '7days':
        start_date = end_date - pd.Timedelta(days=7)
    elif time_range == '30days':
        start_date = end_date - pd.Timedelta(days=30)
    elif time_range == 'quarter':
        start_date = end_date - pd.Timedelta(days=90)
    elif time_range == 'year':
        start_date = end_date - pd.Timedelta(days=365)
    else:
        start_date = df['Date'].min()
    
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    
    # Apply asset filter
    if asset_filter != 'All Commodities':
        if asset_filter == 'Brent Crude':
            df = df[['Date', 'Brent']] if 'Brent' in df.columns else pd.DataFrame()
        elif asset_filter == 'WTI Crude':
            df = df[['Date', 'WTI']] if 'WTI' in df.columns else pd.DataFrame()
        elif asset_filter == 'Natural Gas':
            df = df[['Date', 'NaturalGas']] if 'NaturalGas' in df.columns else pd.DataFrame()
    
    return df

def create_line_chart(df, title="Real-Time Oil & Gas Prices"):
    """Create line chart from data"""
    numeric_cols = [c for c in df.columns if c != 'Date']
    if not numeric_cols or df.empty:
        # Return empty chart placeholder
        fig = go.Figure()
        fig.update_layout(
            title=title,
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=400,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=20)
        )
        return fig.to_html(full_html=False, include_plotlyjs=False)
    
    fig = go.Figure()
    
    colors = ['#00A8E8', '#FF6B35', '#2ECC71']
    for idx, col in enumerate(numeric_cols):
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df[col],
            mode='lines+markers',
            name=col,
            line=dict(width=2, color=colors[idx % len(colors)]),
            marker=dict(size=6, color=colors[idx % len(colors)])
        ))
    
    fig.update_layout(
        title=title,
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        hovermode='x unified',
        height=400,
        xaxis=dict(
            gridcolor='rgba(100, 149, 237, 0.1)',
            title="Date"
        ),
        yaxis=dict(
            gridcolor='rgba(100, 149, 237, 0.1)',
            title="Price ($)"
        )
    )
    
    return fig.to_html(full_html=False, include_plotlyjs=False)

def create_bar_chart(df):
    """Create bar chart from latest data"""
    numeric_cols = [c for c in df.columns if c != 'Date']
    if not numeric_cols or df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="Latest Commodity Prices",
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=300,
            showlegend=False
        )
        return fig.to_html(full_html=False, include_plotlyjs=False)
    
    latest = df.tail(1)[numeric_cols].T.reset_index()
    latest.columns = ['Commodity', 'Price']
    
    colors = ['#00A8E8', '#FF6B35', '#2ECC71']
    
    fig = go.Figure(data=[
        go.Bar(
            x=latest['Commodity'],
            y=latest['Price'],
            marker_color=colors[:len(latest)],
            text=latest['Price'].round(2),
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Latest Commodity Prices",
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=300,
        showlegend=False,
        xaxis=dict(title="Commodity"),
        yaxis=dict(title="Price ($)")
    )
    
    return fig.to_html(full_html=False, include_plotlyjs=False)

def create_pie_chart(df):
    """Create pie chart from latest data"""
    numeric_cols = [c for c in df.columns if c != 'Date']
    if not numeric_cols or df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="Commodity Contribution",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=300
        )
        return fig.to_html(full_html=False, include_plotlyjs=False)
    
    latest = df.tail(1)[numeric_cols].T.reset_index()
    latest.columns = ['Commodity', 'Price']
    
    colors = ['#00A8E8', '#FF6B35', '#2ECC71']
    
    fig = go.Figure(data=[go.Pie(
        labels=latest['Commodity'],
        values=latest['Price'],
        hole=0.3,
        marker_colors=colors[:len(latest)],
        textinfo='label+percent',
        insidetextorientation='radial'
    )])
    
    fig.update_layout(
        title="Commodity Contribution",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=300,
        showlegend=True,
        legend=dict(
            font=dict(color='white')
        )
    )
    
    return fig.to_html(full_html=False, include_plotlyjs=False)

def run_predictive_maintenance_demo():
    """Generate realistic maintenance data"""
    assets = ['Pump-{}'.format(i) for i in range(1, 11)]
    metrics = ['Pressure', 'Temperature', 'Vibration', 'Flow Rate', 'Efficiency']
    
    maintenance_data = []
    for i, asset in enumerate(assets):
        metric = metrics[i % len(metrics)]
        current_value = np.round(np.random.uniform(50, 100), 1)
        failure_prob = np.round(np.random.uniform(0, 0.3), 2)
        health_score = np.round(100 - (failure_prob * 100), 1)
        
        if failure_prob < 0.1:
            status = 'Optimal'
            status_class = 'success'
        elif failure_prob < 0.2:
            status = 'Warning'
            status_class = 'warning'
        else:
            status = 'Critical'
            status_class = 'danger'
            
        last_update = (datetime.now() - timedelta(hours=np.random.randint(0, 24))).strftime('%H:%M:%S')
            
        maintenance_data.append({
            'Asset ID': asset,
            'Metric': metric,
            'Current Value': f'{current_value}',
            'Predicted Failure': f'{failure_prob:.2f}',
            'Health Score': f'{health_score}%',
            'Status': f'<span class="badge bg-{status_class}">{status}</span>',
            'Last Update': last_update
        })
    
    return pd.DataFrame(maintenance_data)

def calculate_summary(df):
    """Calculate summary statistics"""
    numeric_cols = [c for c in df.columns if c != 'Date']
    if not numeric_cols or df.empty:
        return "<div class='alert alert-info'>No data available for summary</div>"
    
    summary = df[numeric_cols].describe().loc[['mean','max','min','std']].round(2)
    
    html = '''
    <table class="table table-dark table-sm table-hover">
        <thead class="bg-primary">
            <tr>
                <th>Statistic</th>
    '''
    for col in summary.columns:
        html += f'<th class="text-light">{col}</th>'
    html += '</tr></thead><tbody>'
    
    for idx, row in summary.iterrows():
        html += f'<tr><td class="fw-bold">{idx.capitalize()}</td>'
        for col in summary.columns:
            value = row[col]
            html += f'<td class="text-light">{value}</td>'
        html += '</tr>'
    
    html += '</tbody></table>'
    return html

def calculate_metrics(df):
    """Calculate key metrics"""
    metrics = []
    
    # Brent metrics
    if 'Brent' in df.columns and not df['Brent'].empty:
        brent_values = df['Brent'].dropna()
        if len(brent_values) > 1:
            current = brent_values.iloc[-1]
            previous = brent_values.iloc[-2] if len(brent_values) > 1 else current
            trend = np.round(((current - previous) / previous) * 100, 1)
            metrics.append({
                'label': 'Brent Crude',
                'value': f'${current:.2f}',
                'unit': 'Per Barrel',
                'trend': trend,
                'icon': 'dollar-sign',
                'color': '#00A8E8'
            })
    
    # WTI metrics
    if 'WTI' in df.columns and not df['WTI'].empty:
        wti_values = df['WTI'].dropna()
        if len(wti_values) > 1:
            current = wti_values.iloc[-1]
            previous = wti_values.iloc[-2] if len(wti_values) > 1 else current
            trend = np.round(((current - previous) / previous) * 100, 1)
            metrics.append({
                'label': 'WTI Crude',
                'value': f'${current:.2f}',
                'unit': 'Per Barrel',
                'trend': trend,
                'icon': 'gas-pump',
                'color': '#FF6B35'
            })
    
    # Natural Gas metrics
    if 'NaturalGas' in df.columns and not df['NaturalGas'].empty:
        gas_values = df['NaturalGas'].dropna()
        if len(gas_values) > 1:
            current = gas_values.iloc[-1]
            previous = gas_values.iloc[-2] if len(gas_values) > 1 else current
            trend = np.round(((current - previous) / previous) * 100, 1)
            metrics.append({
                'label': 'Natural Gas',
                'value': f'${current:.2f}',
                'unit': 'Per MMBtu',
                'trend': trend,
                'icon': 'fire',
                'color': '#2ECC71'
            })
    
    # Production metrics
    production_trend = np.random.uniform(-2, 5)
    metrics.append({
        'label': 'Daily Production',
        'value': f'{np.random.randint(200000, 250000):,}',
        'unit': 'Barrels/Day',
        'trend': np.round(production_trend, 1),
        'icon': 'tachometer-alt',
        'color': '#9C27B0'
    })
    
    # Efficiency metrics
    efficiency_trend = np.random.uniform(0, 3)
    metrics.append({
        'label': 'Operational Efficiency',
        'value': f'{np.random.randint(85, 95)}%',
        'unit': 'AI Score',
        'trend': np.round(efficiency_trend, 1),
        'icon': 'cogs',
        'color': '#FFC107'
    })
    
    return metrics

def get_dashboard_data(time_range='30days', asset_filter='All Commodities'):
    """Get all dashboard data with filters"""
    df = load_or_generate_data(time_range, asset_filter)
    
    return {
        'graph_line_html': create_line_chart(df),
        'graph_bar_html': create_bar_chart(df),
        'graph_pie_html': create_pie_chart(df),
        'maintenance_df': run_predictive_maintenance_demo(),
        'summary_html': calculate_summary(df),
        'metrics': calculate_metrics(df),
        'dataframe': df,
        'time_range': time_range,
        'asset_filter': asset_filter
    }

def home(request):
    """Main dashboard view"""
    time_range = request.GET.get('time_range', '30days')
    asset_filter = request.GET.get('asset_filter', 'All Commodities')
    
    dashboard_data = get_dashboard_data(time_range, asset_filter)
    
    # Convert maintenance DataFrame to HTML
    maintenance_html = dashboard_data['maintenance_df'].to_html(
        classes="table table-dark table-striped table-hover",
        index=False,
        escape=False
    )
    
    context = {
        "graph_line_html": dashboard_data['graph_line_html'],
        "graph_bar_html": dashboard_data['graph_bar_html'],
        "graph_pie_html": dashboard_data['graph_pie_html'],
        "maintenance_html": maintenance_html,
        "summary_html": dashboard_data['summary_html'],
        "initial_metrics": json.dumps(dashboard_data['metrics']),
        "current_time_range": time_range,
        "current_asset_filter": asset_filter
    }
    
    return render(request, "home.html", context)

@csrf_exempt
def api_dashboard_data(request):
    """API endpoint for AJAX updates"""
    if request.method == 'GET':
        time_range = request.GET.get('time_range', '30days')
        asset_filter = request.GET.get('asset_filter', 'All Commodities')
        
        dashboard_data = get_dashboard_data(time_range, asset_filter)
        
        # Convert maintenance DataFrame to HTML
        maintenance_html = dashboard_data['maintenance_df'].to_html(
            classes="table table-dark table-striped table-hover",
            index=False,
            escape=False
        )
        
        return JsonResponse({
            'graph_line_html': dashboard_data['graph_line_html'],
            'graph_bar_html': dashboard_data['graph_bar_html'],
            'graph_pie_html': dashboard_data['graph_pie_html'],
            'maintenance_html': maintenance_html,
            'summary_html': dashboard_data['summary_html'],
            'metrics': dashboard_data['metrics'],
            'timestamp': datetime.now().isoformat(),
            'time_range': time_range,
            'asset_filter': asset_filter,
            'data_sample': dashboard_data['dataframe'].tail(5).to_dict('records') if not dashboard_data['dataframe'].empty else []
        })

def api_ai_insights(request):
    """API endpoint for AI insights"""
    insights = [
        {
            "title": "Market Analysis",
            "content": "Brent crude showing resilience above $84 support. AI predicts 2-3% upside in next 7 days based on inventory data and geopolitical factors.",
            "icon": "chart-line",
            "priority": "high",
            "color": "#00A8E8"
        },
        {
            "title": "Operational Efficiency",
            "content": "Refinery Alpha shows 8% higher energy consumption than benchmark. Optimizing distillation unit #3 could save $42K monthly in energy costs.",
            "icon": "cogs",
            "priority": "medium",
            "color": "#FF6B35"
        },
        {
            "title": "Predictive Maintenance",
            "content": "Pump #342 at Refinery Delta showing 12% efficiency drop. Schedule maintenance within 48 hours to prevent potential failure costing $150K in downtime.",
            "icon": "tools",
            "priority": "critical",
            "color": "#E74C3C"
        },
        {
            "title": "Production Optimization",
            "content": "Adjusting drilling parameters at Well #42 could increase output by 4%. AI recommends testing new configuration during low-demand periods.",
            "icon": "oil-can",
            "priority": "medium",
            "color": "#2ECC71"
        },
        {
            "title": "Inventory Management",
            "content": "Natural gas inventories 15% below seasonal average. Consider increasing storage purchases during current price dip.",
            "icon": "warehouse",
            "priority": "high",
            "color": "#9C27B0"
        }
    ]
    
    return JsonResponse({
        'insights': insights,
        'generated_at': datetime.now().isoformat(),
        'total_insights': len(insights)
    })

def generate_pdf_report(request):
    """Generate PDF report"""
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    
    # Create the PDF object
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Container for 'Flowable' objects
    elements = []
    styles = getSampleStyleSheet()
    
    # Add title
    title = Paragraph("Petroleum AI Dashboard Report", styles['Title'])
    elements.append(title)
    
    # Add date
    date_str = datetime.now().strftime("%B %d, %Y %H:%M:%S")
    date = Paragraph(f"Generated on: {date_str}", styles['Normal'])
    elements.append(date)
    
    elements.append(Paragraph("<br/><br/>", styles['Normal']))
    
    # Add summary section
    elements.append(Paragraph("Executive Summary", styles['Heading2']))
    summary_text = """
    This report provides a comprehensive analysis of petroleum operations, including:
    - Real-time commodity price tracking
    - Production efficiency metrics
    - Predictive maintenance status
    - AI-driven insights and recommendations
    """
    elements.append(Paragraph(summary_text, styles['Normal']))
    
    # Add metrics section
    elements.append(Paragraph("<br/><br/>Key Metrics", styles['Heading2']))
    
    # Get current data for the report
    dashboard_data = get_dashboard_data()
    metrics = dashboard_data['metrics']
    
    # Create metrics table
    metrics_data = [['Metric', 'Value', 'Trend', 'Unit']]
    for metric in metrics:
        metrics_data.append([
            metric['label'],
            metric['value'],
            f"{metric['trend']}%",
            metric['unit']
        ])
    
    metrics_table = Table(metrics_data)
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(metrics_table)
    
    # Add maintenance section
    elements.append(Paragraph("<br/><br/>Predictive Maintenance Status", styles['Heading2']))
    
    maintenance_df = dashboard_data['maintenance_df']
    maintenance_data = [list(maintenance_df.columns)]
    for _, row in maintenance_df.iterrows():
        # Remove HTML tags from status
        status = str(row['Status']).replace('<span class="badge bg-', '').replace('</span>', '')
        status = status.split('>')[-1] if '>' in status else status
        maintenance_data.append([
            row['Asset ID'],
            row['Metric'],
            row['Current Value'],
            row['Predicted Failure'],
            row['Health Score'],
            status,
            row['Last Update']
        ])
    
    if len(maintenance_data) > 1:
        maint_table = Table(maintenance_data)
        maint_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(maint_table)
    
    # Add recommendations
    elements.append(Paragraph("<br/><br/>AI Recommendations", styles['Heading2']))
    recommendations = [
        "1. Increase Brent crude production allocation by 5%",
        "2. Schedule maintenance for Pump #342 within 48 hours",
        "3. Optimize distillation unit #3 for energy efficiency",
        "4. Review hedging strategy for natural gas positions",
        "5. Implement AI recommendations for Well #42 optimization"
    ]
    
    for rec in recommendations:
        elements.append(Paragraph(rec, styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    
    # Create HTTP response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="petroleum_dashboard_report.pdf"'
    response.write(pdf)
    
    return response