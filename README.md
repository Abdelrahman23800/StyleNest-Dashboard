# 📊 StyleNest Boutique - Sales Performance Dashboard

A professional e-commerce analytics dashboard built with Streamlit, designed for data-driven decision making and growth optimization.

## ✨ Features

### Core Analytics
- **Real-time KPI Monitoring**: Revenue, Orders, Average Order Value, Conversion Rate
- **Channel Performance Analysis**: Track revenue and efficiency across marketing channels
- **Sales Rep Leaderboard**: Identify top performers and coaching opportunities
- **Customer Segmentation**: Analyze revenue by customer type
- **Time-Based Insights**: Weekly revenue trends and time-of-day patterns

### Reporting & Export
- **Executive Recommendations**: AI-powered insights based on your data
- **Text Report Export**: Download detailed reports as .txt files
- **PDF Report Export**: Generate executive summaries in PDF format

### Interactive Filters
- Date range selection
- Channel filtering
- Customer type segmentation
- Business/Branch filtering

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download the repository**
```bash
git clone <repository-url>
cd sales-dashboard
```

2. **Install required packages**
```bash
pip install -r requirements.txt
```

3. **Run the dashboard**
```bash
streamlit run sales_dashboard_pro.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

## 📦 Dependencies

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.14.0
fpdf>=1.7.2
openpyxl>=3.1.0
```

Create a `requirements.txt` file with the above packages.

## 📁 Data Format

### Required Columns (Flexible)
The dashboard automatically adapts to your data structure. Common columns include:

| Column Name | Type | Description | Required |
|-------------|------|-------------|----------|
| Date | datetime | Transaction date | Recommended |
| Revenue | float | Transaction revenue | Yes |
| Channel | string | Marketing/sales channel | Recommended |
| Sales Rep | string | Sales representative name | Optional |
| Customer Type | string | New/Returning/VIP etc. | Optional |
| Conversions | integer | Number of conversions | Optional |
| Average Order Size | float | Order value | Optional |
| Time of Day | string | Morning/Afternoon/Evening | Optional |
| Business | string | Branch/store identifier | Optional |

### Sample Data Format (CSV/XLSX)

```csv
Date,Revenue,Channel,Sales Rep,Customer Type,Conversions,Average Order Size,Time of Day,Business
2024-01-15,1500.00,Online,John Smith,New,1,1500.00,Morning,Main Branch
2024-01-15,2300.00,Retail,Sarah Jones,Returning,1,2300.00,Afternoon,Main Branch
2024-01-16,890.00,Social Media,Mike Brown,New,1,890.00,Evening,Branch 2
```

## 🎯 Usage Guide

### 1. Upload Your Data
- Click "Upload sales file" in the sidebar
- Supports both Excel (.xlsx, .xls) and CSV formats
- Maximum file size: 200MB

### 2. Apply Filters
Use the sidebar filters to focus on specific segments:
- **Date Range**: Select start and end dates
- **Channel**: Filter by marketing/sales channels
- **Customer Type**: Focus on specific customer segments
- **Business/Branch**: Analyze specific locations

### 3. Analyze Insights
- **KPI Cards**: View key metrics at the top
- **Channel Analysis**: Identify best-performing channels
- **Trend Charts**: Spot growth patterns over time
- **Rep Performance**: See individual sales performance
- **Recommendations**: Get actionable insights

### 4. Export Reports
- **Text Report**: Click "Download Text Report" for a formatted .txt file
- **PDF Report**: Click "Download PDF Report" for an executive summary

## 🎨 Customization

### Branding
Edit the styling section in `sales_dashboard_pro.py`:
```python
STYLE = """
<style>
[data-testid="stAppViewContainer"] {background: linear-gradient(180deg, #fff 0%, #f7fbff 100%);}
h1 {color:#0b3b5c;}
/* Add your custom CSS here */
</style>
"""
```

### Title & Description
```python
st.title("Your Company Name — Sales Dashboard")
st.markdown("Your custom description here")
```

## 🚀 Deployment

### Streamlit Cloud (Free)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy!

### Local Server
```bash
streamlit run sales_dashboard_pro.py --server.port 8501 --server.address 0.0.0.0
```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY sales_dashboard_pro.py .
EXPOSE 8501
CMD ["streamlit", "run", "sales_dashboard_pro.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 📊 Sample Insights

The dashboard automatically generates insights such as:
- **Channel Optimization**: "Focus investment on Social Media — highest revenue per conversion"
- **Time-Based**: "Peak selling window: Evening. Schedule paid promotions in this window"
- **Team Performance**: "Consider targeted coaching for lower performers"
- **Data Gaps**: Identifies missing data fields for fuller analysis

## 🔧 Troubleshooting

### Common Issues

**"Upload your sales file to run the dashboard"**
- Ensure you've uploaded a valid CSV or Excel file
- Check that the file isn't corrupted

**"Could not read file"**
- Verify file format (CSV or XLSX)
- Check for special characters in column names
- Ensure the file isn't password-protected

**Charts not showing**
- Ensure required columns exist (Revenue, Date, etc.)
- Check for null/empty values in key fields

**PDF Download Issues**
- Use the Text Report download as an alternative
- PDF generation requires ASCII-compatible text
- Long text fields may cause issues

## 📈 Performance Tips

- Keep datasets under 100,000 rows for optimal performance
- Use date filters to focus on specific periods
- Close unused browser tabs while running
- Clear cache if data seems stale (click ⋮ → Settings → Clear cache)

## 🤝 Support

For issues, questions, or feature requests:
- Create an issue in the repository
- Email: support@yourcompany.com
- Documentation: [Link to docs]

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - Dashboard framework
- [Plotly](https://plotly.com/) - Interactive visualizations
- [Pandas](https://pandas.pydata.org/) - Data processing
- [FPDF](http://www.fpdf.org/) - PDF generation

---

**Version**: 1.0.0  
**Last Updated**: October 2024  
**Author**: Your Name/Company

---

## 🚀 Quick Start Example

```bash
# 1. Install dependencies
pip install streamlit pandas plotly fpdf openpyxl

# 2. Run the dashboard
streamlit run sales_dashboard_pro.py

# 3. Upload your sales data file
# 4. Start analyzing!
```

**Made with Abdelrahman Nabil for data-driven e-commerce growth**
