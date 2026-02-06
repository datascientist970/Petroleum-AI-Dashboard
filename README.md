# Petroleum AI Dashboard

## 📋 **Project Overview**
Petroleum AI Dashboard is a sophisticated, real-time monitoring system designed for the petroleum industry. It combines data analytics, artificial intelligence, and predictive maintenance to provide actionable insights for energy companies, refineries, and commodity traders.

## 🎯 **Core Theory & Concept**

### **Problem Statement**
The petroleum industry faces challenges in:
- Real-time monitoring of volatile commodity prices
- Predictive maintenance of expensive equipment
- Operational efficiency optimization
- Data-driven decision making

### **Solution Architecture**
The dashboard provides:
1. **Real-time Analytics**: Live tracking of Brent, WTI, and Natural Gas prices
2. **Predictive Maintenance**: AI-driven equipment failure prediction
3. **Operational Intelligence**: Data-driven recommendations
4. **Automated Reporting**: PDF generation with executive insights

### **Technology Stack**
- **Backend**: Django (Python) for business logic and API
- **Frontend**: HTML5, CSS3, JavaScript with Bootstrap 5
- **Visualization**: Plotly.js for interactive charts
- **Reporting**: ReportLab for PDF generation
- **Data Processing**: Pandas, NumPy

## 📦 **Requirements**

### **System Requirements**
- Python 3.8 or higher
- Django 4.0+
- Modern web browser (Chrome, Firefox, Edge)
- 4GB RAM minimum
- 500MB free disk space

### **Python Dependencies**
- Django 4.2.0
- pandas 2.0.3
- numpy 1.24.3
- plotly 5.15.0
- reportlab 4.0.4

### **Frontend Dependencies**
- Bootstrap 5.3.0
- Font Awesome 6.4.0
- Plotly.js (latest)
- jQuery (via Bootstrap)

## 🚀 **Clone & Setup**

### **Step 1: Clone the Repository**
```
git clone https://github.com/yourusername/petroleum-ai-dashboard.git
cd petroleum-ai-dashboard
```

### **Step 2: Set Up Virtual Environment**
```
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### **Step 3: Install Dependencies**
```
pip install django pandas numpy plotly reportlab
```

### **Step 4: Configure Django Project**
```
django-admin startproject petroleum_dashboard .
python manage.py startapp dashboard
```

### **Step 5: Run Server**
```
python manage.py migrate
python manage.py runserver
```

### **Step 6: Access Dashboard**
Open browser and navigate to: `http://127.0.0.1:8000/`

## 📸 **Screenshots**

### **Dashboard Overview**
```
┌─────────────────────────────────────────────────────────┐
│  PETROLEUM AI DASHBOARD                                │
│  Real-time Energy Intelligence Platform                │
├─────────────────────────────────────────────────────────┤
│  [📊] Brent Crude: $84.76    ↑2.4%                    │
│  [⛽] WTI Crude: $79.45      ↑1.8%                    │
│  [🔥] Natural Gas: $3.25     ↓0.5%                    │
│  [⚙️] Efficiency: 88.7%      ↑5.3%                    │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐             │
│  │  📈 Line Chart  │  │  📊 Bar Chart   │             │
│  │  Price Trends   │  │  Latest Prices  │             │
│  └─────────────────┘  └─────────────────┘             │
│                                                       │
│  ┌─────────────────┐  ┌─────────────────┐             │
│  │  🥧 Pie Chart   │  │  📋 Summary     │             │
│  │  Contribution   │  │  Statistics     │             │
│  └─────────────────┘  └─────────────────┘             │
├─────────────────────────────────────────────────────────┤
│  🛠️ PREDICTIVE MAINTENANCE DASHBOARD                 │
│  ┌────┬────────────┬───────┬────────┬──────┬────────┐│
│  │ ID │ Asset      │Health │ Status │ Prob │ Action ││
│  ├────┼────────────┼───────┼────────┼──────┼────────┤│
│  │ 01 │ Pump-1     │ 95%   │ ✅Opt  │ 0.05 │ View   ││
│  │ 02 │ Compressor │ 87%   │ ⚠️Warn │ 0.15 │ Details││
│  │ 03 │ Valve-3    │ 72%   │ 🔥Crit │ 0.28 │ Fix    ││
│  └────┴────────────┴───────┴────────┴──────┴────────┘│
└─────────────────────────────────────────────────────────┘
```

### **Features Screenshots**

#### **1. Main Dashboard Interface**
```
DARK THEME INTERFACE WITH GRADIENT HEADER
┌─────────────────────────────────────────────────────┐
│ 🔥 Petroleum AI Dashboard v3.1                      │
├─────────────────────────────────────────────────────┤
│ METRICS CARDS (4) with trend indicators            │
│ • Brent Crude: $84.76 ↑2.4%                        │
│ • Daily Production: 245,820 barrels ↑1.2%          │
│ • Equipment Health: 94.2% Optimal                  │
│ • Operational Efficiency: 88.7% AI Score           │
├─────────────────────────────────────────────────────┤
│ INTERACTIVE CHARTS SECTION                         │
│ • Line Chart: Multi-commodity price trends         │
│ • Bar Chart: Latest commodity prices comparison    │
│ • Pie Chart: Market contribution percentages       │
│ • Summary Table: Statistical analysis              │
├─────────────────────────────────────────────────────┤
│ PREDICTIVE MAINTENANCE TABLE                       │
│ • 10 assets monitored                              │
│ • Color-coded status (Green/Yellow/Red)            │
│ • Failure probability scores                       │
│ • Last update timestamps                           │
└─────────────────────────────────────────────────────┘
```

#### **2. AI Insights Modal**
```
┌─────────────────────────────────────────────────────┐
│ 🤖 AI-POWERED INSIGHTS                             │
├─────────────────────────────────────────────────────┤
│ 🔴 CRITICAL (1)                                    │
│ • Pump #342: 12% efficiency drop                   │
│   Schedule maintenance within 48 hours             │
│                                                    │
│ 🟡 HIGH PRIORITY (2)                               │
│ • Brent crude: 2-3% upside predicted               │
│ • Refinery Alpha: 8% energy optimization possible  │
│                                                    │
│ 🔵 RECOMMENDATIONS (3)                             │
│ • Increase production allocation by 5%             │
│ • Review hedging strategy                          │
│ • Optimize Well #42 parameters                     │
└─────────────────────────────────────────────────────┘
```

#### **3. Time Filter Controls**
```
TIME RANGE SELECTOR
┌─────────────────────────────────────┐
│ [●] Today    [ ] 7 Days             │
│ [ ] 30 Days  [ ] Quarter  [ ] Year  │
└─────────────────────────────────────┘

ASSET FILTER DROPDOWN
┌──────────────────────────┐
│ ▼ All Commodities       │
├──────────────────────────┤
│ • Brent Crude           │
│ • WTI Crude             │
│ • Natural Gas           │
└──────────────────────────┘
```

#### **4. Control Panel**
```
CONTROL BUTTONS
┌─────────────────────────────────────┐
│ [📄] Generate PDF Report           │
│ [🤖] AI Insights                   │
│ [🔄] Auto-Refresh: ON              │
│ [📥] Export Data                   │
└─────────────────────────────────────┘
```

### **Visual Design Elements**

#### **Color Scheme**
```
┌─────────────────────────────────────────────────────┐
│ PRIMARY COLORS                                      │
│ • Header Gradient: #0d3b66 → #1a5f7a               │
│ • Accent Border: #ff9f1c (orange)                  │
│ • Card Background: #112240 (dark blue)             │
│ • Text: #e6f1ff (light blue/white)                 │
│                                                    │
│ STATUS INDICATORS                                  │
│ • Success: #2ecc71 (green)     [✅ Optimal]       │
│ • Warning: #e74c3c (red)       [⚠️ Warning]       │
│ • Critical: #ff9f1c (orange)   [🔥 Critical]      │
│ • Info: #00a8e8 (blue)         [ℹ️ Info]          │
└─────────────────────────────────────────────────────┘
```

#### **Chart Types & Visualization**
```
CHARTS AVAILABLE
1. LINE CHART
   • Multi-line trends
   • Date range selector
   • Hover details
   • Zoom/pan controls

2. BAR CHART
   • Latest prices comparison
   • Color-coded by commodity
   • Value labels

3. PIE CHART
   • Market share distribution
   • Interactive legend
   • Percentage labels
```

#### **Data Presentation**
```
METRIC CARDS LAYOUT
┌─────────────────────────────┐
│ [Icon] Label                │
│        Large Value          │
│        Unit                 │
│        Trend: ↑↓ %          │
└─────────────────────────────┘

MAINTENANCE TABLE
┌─────┬──────────┬───────┬────────┬─────────┬───────┐
│ ID  │ Asset    │Health │ Status │ Failure │ Time  │
├─────┼──────────┼───────┼────────┼─────────┼───────┤
│ Badges: ●Optimal ●Warning ●Critical            │
│ Statistics: 4 Optimal | 3 Warning | 3 Critical │
└─────────────────────────────────────────────────┘
```

### **Mobile Responsive View**
```
MOBILE LAYOUT (Single Column)
┌─────────────────────────┐
│ Petroleum AI Dashboard  │
├─────────────────────────┤
│ [Metric Card 1]         │
│ [Metric Card 2]         │
│ [Metric Card 3]         │
│ [Metric Card 4]         │
├─────────────────────────┤
│ [Full-width Line Chart] │
├─────────────────────────┤
│ [Bar Chart]             │
│ [AI Insight Box]        │
├─────────────────────────┤
│ [Pie Chart]             │
│ [Summary Table]         │
├─────────────────────────┤
│ [Maintenance Table]     │
│ [Scrollable]            │
└─────────────────────────┘
```

### **PDF Report Preview**
```
PDF REPORT STRUCTURE
┌─────────────────────────────────────┐
│ PETROLEUM AI DASHBOARD REPORT      │
│ Generated: [Date Time]             │
├─────────────────────────────────────┤
│ EXECUTIVE SUMMARY                  │
│ • Market overview                  │
│ • Key findings                     │
│ • Recommendations                  │
├─────────────────────────────────────┤
│ KEY METRICS TABLE                  │
│ • Commodity prices                 │
│ • Production stats                 │
│ • Efficiency scores                │
├─────────────────────────────────────┤
│ MAINTENANCE STATUS                 │
│ • Asset health breakdown           │
│ • Critical issues                  │
│ • Action items                     │
├─────────────────────────────────────┤
│ AI RECOMMENDATIONS                 │
│ • Priority actions                 │
│ • Timeline                         │
│ • Expected impact                  │
└─────────────────────────────────────┘
```

## 🎨 **UI/UX Features**

### **Interactive Elements**
- **Live Updates**: Data refreshes every 15 seconds
- **Hover Effects**: Cards and charts have hover animations
- **Click Actions**: Interactive charts with tooltips
- **Modal Windows**: AI insights in popup modals
- **Dropdown Filters**: Asset and time range selectors

### **Visual Indicators**
- **Trend Arrows**: Up/down indicators for metrics
- **Color Coding**: Status-based color schemes
- **Progress Bars**: Health scores visualization
- **Badges**: Priority and status badges
- **Icons**: Font Awesome icons throughout

### **Navigation & Controls**
- **Time Range Buttons**: Quick period selection
- **Refresh Toggle**: Enable/disable auto-refresh
- **Export Options**: PDF and data export
- **Filter Controls**: Asset-specific filtering
- **View Details**: Drill-down capabilities

## 📊 **Data Flow Architecture**
```
DATA SOURCES → BACKEND PROCESSING → FRONTEND DISPLAY → USER INTERACTION
    CSV           Django Views        HTML/CSS/JS        Filters/Controls
    APIs           Pandas/Numpy       Plotly Charts      PDF Generation
    Real-time      AI Algorithms      Bootstrap UI       Export Functions
```

## 🔄 **Update Cycle**
```
EVERY 15 SECONDS:
1. Fetch new data from CSV/APIs
2. Process with Pandas/NumPy
3. Generate updated charts
4. Refresh metrics display
5. Update maintenance status
6. Trigger AI analysis
```

## 🎯 **Target Users**
- **Energy Analysts**: Market trend analysis
- **Operations Managers**: Equipment monitoring
- **Traders**: Commodity price tracking
- **Executives**: Executive reporting
- **Maintenance Teams**: Predictive maintenance alerts

This dashboard represents a complete, professional solution for petroleum industry analytics with modern UI/UX, real-time capabilities, and actionable intelligence.
