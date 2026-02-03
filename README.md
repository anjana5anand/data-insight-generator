# Automated EDA System

An intelligent exploratory data analysis system that automatically analyzes CSV datasets and generates comprehensive reports with statistics, visualizations, and actionable insights.

## Features

- 📊 **Comprehensive Statistics**: Numeric and categorical analysis with outlier detection
- 📈 **Rich Visualizations**: Histograms, boxplots, bar charts, scatterplots, correlation heatmaps
- 🔍 **Smart Insights**: Automatic pattern detection and data quality assessment
- 📄 **Professional Reports**: Markdown and PDF outputs with embedded plots
- 🗂️ **Batch Processing**: Analyze multiple datasets at once
- 📋 **Schema Support**: Optional data dictionary for enhanced analysis
- 🔒 **Privacy Awareness**: Detects and warns about potentially sensitive columns
- 🛡️ **Robust Handling**: Handles missing values, dates, edge cases

## Installation

### Prerequisites
- Python 3.8 or higher
- For PDF generation: `pandoc` and `pdflatex` (texlive)

### Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Install PDF Tools (Optional but Recommended)

**On Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install pandoc texlive-latex-base texlive-latex-extra
```

**On macOS:**
```bash
brew install pandoc
brew install --cask mactex
```

**On Windows:**
- Download Pandoc from https://pandoc.org/installing.html
- Download MiKTeX from https://miktex.org/download

## Usage

### Basic Usage - Single File
```bash
python eda.py data.csv
```

### Multiple Files
```bash
python src/eda.py file1.csv file2.csv file3.csv
```

### Process Entire Directory
```bash
python src/eda.py /path/to/data/
```

### Using Wildcards
```bash
python eda.py "data/*.csv"
```

## Output Structure

```
output/
└── [dataset_name]/
    ├── report.md              # Markdown report
    ├── report.pdf             # PDF report (if pandoc installed)
    ├── plots/                 # All visualizations
    │   ├── hist_*.png
    │   ├── box_*.png
    │   ├── bar_*.png
    │   ├── scatter_*.png
    │   └── correlation_heatmap.png
    ├── overview.csv           # Column-level metadata
    ├── numeric_stats.csv      # Detailed numeric statistics
    ├── categorical_stats.csv  # Categorical frequencies
    └── quality_report.txt     # Data quality summary
```

## What the System Analyzes

### Dataset Overview
- Row and column counts
- Data types for each column
- Missing value summary
- Duplicate detection
- Single-value columns
- High-missingness warnings

### Descriptive Statistics
- **Numeric columns**: min, max, mean, median, mode, std, IQR, outliers
- **Categorical columns**: frequency counts, percentages, cardinality

### Visualizations
- Histograms showing distributions
- Boxplots for outlier detection
- Bar charts for categorical data
- Scatterplots for relationships
- Correlation heatmaps

### Insights (5-10 per dataset)
- Distribution patterns (skewness, bimodality)
- Outlier identification with counts
- Correlation findings
- Data quality issues
- Cardinality analysis
- Missing data patterns
- Potential biases and limitations

## Examples

### Run on your dataset
```bash
python eda.py crime_data.csv
```

Output includes insights like:
- "TIME OCC shows bimodal distribution with peaks at 1200 and 1800 hours"
- "6 columns have >50% missing data, limiting weapon analysis"
- "Strong geographic clustering in certain areas (correlation: 0.85)"

## Troubleshooting

### PDF Generation Fails
- Ensure pandoc and pdflatex are installed
- The system will still generate markdown reports if PDF fails

### Memory Issues with Large Files
- The system loads entire CSV into memory
- For very large files (>1GB), consider sampling first

### Date Columns Not Detected
- Ensure dates are in standard formats (YYYY-MM-DD, MM/DD/YYYY)
- System attempts automatic detection and parsing

## Project Structure

```
.
├── eda.py                 # Main analysis script
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── logs/
│   └── genai_log.md       # GenAI usage documentation
└── video/
    └── demo.mp4           # Demonstration video
```

## Credits

This system was developed as part of a data science course assignment, utilizing GenAI tools (Claude) for code assistance and brainstorming. All code has been verified for correctness and all insights are computationally validated.

## License

This project is for educational purposes.
