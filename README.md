# Employee Motivation & Stress Tracking Application

A comprehensive web application built with Streamlit to assess and track employee motivation levels and stress indicators, with AI-powered personalized recommendations.

## Features

### Employee Test Section
- **User Profile**: Simple input for name and department selection
- **10-Question Assessment**: 
  - 5 questions on Internal vs External Motivation
  - 5 questions on Stress Levels and Burnout Risk
- **Rule-Based Analysis**: Intelligent recommendations based on score ranges
- **Instant Results**: Visual representation of scores with actionable advice

### Admin Dashboard
- **Overview Statistics**: Total assessments, average scores, department metrics
- **Department Analytics**: Bar charts showing stress and burnout levels by department
- **Motivation Analysis**: Internal vs External motivation comparison
- **Data Filtering**: Filter results by department and date range
- **Export Functionality**: Download filtered results as CSV
- **Detailed Results Table**: Complete view of all assessment data

## Installation & Setup

### Prerequisites
- Python 3.8 or higher

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## Usage Guide

### For Employees
1. **Enter Profile**: Fill in your name and select your department
2. **Complete Assessment**: Answer all 10 questions honestly
3. **View Results**: See your motivation and stress profiles with visualizations
4. **Get Recommendations**: Receive personalized AI-powered advice

### For Managers/Administrators
1. **Navigate to Admin Dashboard**: Use the sidebar to switch views
2. **View Analytics**: Monitor department-wide trends and patterns
3. **Filter Data**: Use department and date filters for specific insights
4. **Export Reports**: Download data for further analysis or reporting

## Data Storage

- All assessment results are automatically saved to `results.csv`
- The file is created automatically when the first assessment is completed
- No database setup required - uses simple CSV storage
- Data includes: Name, Department, Date, Scores, and AI Recommendations

## Question Categories

### Motivation Assessment
- Internal motivation: Personal interest, accomplishment, values
- External motivation: Rewards, recognition, external expectations

### Stress & Burnout Assessment
- Emotional exhaustion and sleep issues
- Cynicism and detachment
- Work-life balance and resource adequacy

## Scoring System

- All questions use a 5-point Likert scale (Never to Always)
- Scores are normalized to 1-10 scale
- Higher stress/burnout scores indicate greater risk
- Higher motivation scores indicate stronger drivers

## Technical Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas
- **Rule-Based Engine**: Custom Python logic
- **Visualization**: Plotly
- **Storage**: CSV files

## Security & Privacy

- No sensitive personal data is collected beyond name and department
- Results are stored locally in CSV format
- No external API calls or data transmission
- 100% offline operation once installed

## Troubleshooting

### Common Issues

1. **CSV File Not Found**
   - The application creates `results.csv` automatically
   - Ensure write permissions in the application directory

2. **Visualization Not Loading**
   - Check internet connection for Plotly charts
   - Refresh the browser page

### Getting Help

If you encounter issues:
1. **Check the terminal output** for error messages
2. **Verify all dependencies** are installed correctly
3. **Ensure Python is properly configured** on your system

## Customization

### Adding New Questions
1. Modify the question list in `app.py`
2. Update the scoring logic accordingly
3. Adjust the AI prompt for new categories

### Changing Departments
1. Update the department list in the selectbox
2. Ensure consistency across the application

### Modifying Recommendation Logic
1. Edit the `get_rule_based_analysis` function in `app.py`
2. Adjust score thresholds and recommendation messages
3. Add new recommendation categories as needed

## License

This project is provided as-is for educational and internal organizational use.
