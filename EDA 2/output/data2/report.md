---
title: "data2 - EDA"
date: "2026-02-03"
---

**PRIVACY WARNING**: Sensitive columns detected

# Overview

- Rows: 1,016
- Columns: 8
- Duplicates: 0

\newpage

# Numeric Analysis

## Supply Chain Emission Factors without Margins

Min: 0.03 | Max: 3.85 | Mean: 0.26 | Median: 0.16 | Std: 0.31

Outliers: 93 (9.2%)

![](plots/hist_Supply_Chain_Emission_Factors_without_Margins.png){ width=48% } ![](plots/box_Supply_Chain_Emission_Factors_without_Margins.png){ width=48% }

## Margins of Supply Chain Emission Factors

Min: 0.00 | Max: 0.12 | Mean: 0.02 | Median: 0.00 | Std: 0.02

Outliers: 17 (1.7%)

![](plots/hist_Margins_of_Supply_Chain_Emission_Factors.png){ width=48% } ![](plots/box_Margins_of_Supply_Chain_Emission_Factors.png){ width=48% }

## Supply Chain Emission Factors with Margins

Min: 0.03 | Max: 3.92 | Mean: 0.28 | Median: 0.17 | Std: 0.32

Outliers: 84 (8.3%)

![](plots/hist_Supply_Chain_Emission_Factors_with_Margins.png){ width=48% } ![](plots/box_Supply_Chain_Emission_Factors_with_Margins.png){ width=48% }

\newpage

# Categorical: 2017 NAICS Title

| Value | Count | % |
|-------|-------|---|
| Soybean Farming | 1 | 0.1 |
| Book Publishers | 1 | 0.1 |
| Other Support Activities for Road Transportation | 1 | 0.1 |
| Freight Transportation Arrangement | 1 | 0.1 |
| Packing and Crating | 1 | 0.1 |
| All Other Support Activities for Transportation | 1 | 0.1 |
| Postal Service | 1 | 0.1 |
| Couriers and Express Delivery Services | 1 | 0.1 |
| Local Messengers and Local Delivery | 1 | 0.1 |
| General Warehousing and Storage | 1 | 0.1 |

![](plots/bar_2017_NAICS_Title.png){ width=70% }

\newpage

# Correlation

![](plots/scatter_2017_NAICS_Code_Supply_Chain_Emission_Factors_without_Margins.png){ width=48% } ![](plots/correlation_heatmap.png){ width=48% }

\newpage

# Key Insights

1. 1,016 rows x 8 cols, 100.0% complete

2. No duplicates - good quality

3. Margins of Supply Chain Emission Factors: high variability (CV=1.38), range: 0.0 to 0.1

4. Supply Chain Emission Factors without Margins: 9.2% outliers

5. Supply Chain Emission Factors without Margins: right-skewed (skew=4.33)

6. 2017 NAICS Title: 1016 unique values, evenly distributed

7. Perfect correlation (1.00): Supply Chain Emission Factors without Margins and Supply Chain Emission Factors with Margins are likely duplicates/derived

8. WARNING: 2 sensitive columns detected

# Limitations

- Dataset represents specific time/location scope
- 2 columns may contain sensitive information

*Auto-generated. All statistics verified.*
