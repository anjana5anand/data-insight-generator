# GenAI Usage Log

**Course**: Data Science EDA Assignment  
**Student**: Anjana and Sofie
**Tool Used**: Claude 3.5 Sonnet (Anthropic)  
**Date**: February 2026

---

## Summary

This document logs all interactions with Claude AI during the development of the automated EDA system. Claude was used extensively for code generation, debugging, feature implementation, and documentation writing. All generated code was reviewed, tested, and verified for correctness before inclusion in the final submission.

---

## Session 1: Initial Code Review and Bug Fix

### Prompt 1: PDF Plot Issue
**My Prompt**:
```
can you fix this code so the pdf file gives plots in them
[uploaded eda.py file]
```

**Claude's Response**:
- Identified that Pandoc needed proper markdown image syntax instead of raw LaTeX
- Changed image references from `![](path)` to `![](path){ width=X% }`
- Added YAML header with geometry settings
- Changed `\pagebreak` to `\newpage` for better compatibility

**What we Changed/Verified**:
- Tested the PDF generation with pandoc
- Verified that images now appear in the PDF
- Confirmed image sizing works correctly

---

## Session 2: Multi-File Processing Feature

### Prompt 2: Multiple Dataset Support
**My Prompt**:
```
can this be automated to accept different documents or just one?
```

**Claude's Response**:
- Created `eda_multi.py` with support for:
  - Single files
  - Multiple files
  - Entire directories
  - Wildcard patterns (*.csv)
- Added separate output directories per dataset
- Implemented progress tracking

**What we Changed/Verified**:
- Tested with multiple CSV files
- Verified no file overwrites occur
- Confirmed error handling works for individual file failures
- Added my own modifications to output formatting

---

## Session 3: Assignment Requirements Check

### Prompt 3: Completeness Check
**My Prompt**:
```
can you check if all are completed
[uploaded assignment requirements document]
```

**Claude's Response**:
- Created comprehensive checklist comparing requirements vs implementation
- Identified CRITICAL gaps:
  1. Insights too generic (only 3, need 5-10 specific ones)
  2. No schema/data dictionary support
  3. Missing requirements.txt and README.md
  4. No privacy warnings for sensitive columns
  5. No handling of missing value codes
  6. No date column detection
  7. No limitations/bias section

**What we Changed/Verified**:
- Reviewed the checklist thoroughly
- Prioritized which features to implement
- Decided to fix all high-priority issues

---

## Session 4: Comprehensive Feature Implementation

### Prompt 4: Fix All Issues
**My Prompt**:
```
can you fix these issues?
this is my requirements.txt:
pandas
numpy
matplotlib
seaborn
```

**Claude's Response**:
Generated complete production-ready version with:

1. **requirements.txt**: Added scipy for statistical functions
2. **README.md**: Comprehensive documentation with:
   - Installation instructions
   - Usage examples
   - Schema format documentation
   - Output structure explanation
   - Troubleshooting guide

3. **Enhanced eda.py** with new features:
   - Schema loading from JSON files
   - Privacy/sensitivity detection (IDs, emails, phone, high cardinality)
   - Missing value code handling (-999, "NA", etc.)
   - Date column detection and parsing
   - Distribution analysis (skewness detection)
   - Advanced insight generation (5-10 specific insights)
   - Limitations and bias analysis
   - Edge case handling (all-numeric, all-categorical datasets)
   - Better error messages and progress indicators

**What we Changed/Verified**:

### Code Verification Process:
1. **Schema Support**:
   - Created test schema JSON file
   - Verified schema loading works
   - Confirmed missing codes are replaced correctly
   - **Verified**: Works as expected

2. **Privacy Detection**:
   - Tested with dataset containing ID columns
   - Confirmed high cardinality detection works
   - Verified warning messages appear
   - **Verified**: Correctly identifies sensitive columns

3. **Missing Value Handling**:
   - Created test data with -999, "NA", "unknown" values
   - Confirmed they're converted to NaN
   - Verified statistics calculated correctly after conversion
   - **Verified**: Works correctly

4. **Date Detection**:
   - Tested with various date formats
   - Confirmed automatic parsing works
   - Verified date range calculations in insights
   - **Verified**: Successfully detects and parses dates

5. **Insights Generation**:
   - Ran on multiple datasets
   - Verified all insights reference actual computed values
   - Confirmed no hallucinated statistics
   - Checked that insights are specific and data-driven
   - **Verified**: All insights are based on real computations

6. **Distribution Analysis**:
   - Tested skewness calculations
   - Verified scipy.stats integration
   - Confirmed distribution descriptions are accurate
   - **Verified**: Statistical calculations correct

7. **Edge Cases**:
   - Tested with all-numeric dataset (no categorical columns)
   - Tested with all-categorical dataset (no numeric columns)
   - Tested with very small datasets (<10 rows)
   - Tested with large datasets (>1M rows)
   - **Verified**: Handles all edge cases gracefully

8. **Output Quality**:
   - Verified PDF includes all plots
   - Checked markdown formatting
   - Confirmed file organization
   - Tested on different operating systems
   - **Verified**: Professional quality outputs

---

## Key Code Modifications I Made

While Claude generated the bulk of the code, we made several important modifications:

1. **Adjusted Insight Thresholds**:
   - Changed cardinality threshold from 0.9 to 0.95 for better sensitivity detection
   - Modified outlier percentage threshold based on my domain knowledge

2. **Enhanced Error Messages**:
   - Added more descriptive error messages
   - Improved progress indicators with emojis for better UX

3. **Statistical Validation**:
   - Verified all statistical calculations match pandas documentation
   - Cross-referenced scipy.stats.skew implementation
   - Confirmed IQR outlier method follows standard 1.5×IQR rule

4. **Performance Optimization**:
   - Added limits to number of bins in histograms for large datasets
   - Limited bar charts to top 15 categories instead of all

5. **Documentation Improvements**:
   - Added more examples to README
   - Clarified schema format with comments
   - Enhanced inline code comments for maintainability

---

## Verification and Testing

### Datasets Tested:
1. **Crime Dataset** (1M+ rows): Verified numeric analysis, outlier detection
2. **Sales Dataset** (50K rows): Verified categorical analysis, date parsing
3. **Synthetic Test Data**: Created specifically to test edge cases

### Statistical Verification:
- Cross-checked mean/median/std calculations with Excel
- Verified correlation coefficients using scipy independently
- Confirmed outlier counts manually for small test dataset
- Validated skewness calculations against scipy documentation

### All Statistics Are Correct:
- No hallucinated values
- All insights based on actual computed statistics
- All visualizations accurately represent the data

---

## What Claude Did vs What we Did

### Claude Generated:
- 95% of the code structure and implementation
- All documentation templates
- Statistical function implementations
- Visualization code
- Error handling logic

### We Did:
- Reviewed every line of code for correctness
- Tested all functionality thoroughly
- Modified thresholds and parameters based on my understanding
- Verified statistical accuracy
- Ensured insights are meaningful and non-generic
- Tested edge cases
- Validated against assignment requirements
- Made final adjustments for my specific use case

---

## Conclusion

Claude AI significantly accelerated development of this EDA system, reducing what would have been 20+ hours of coding to about 3-4 hours of prompt engineering and verification. However, the quality of the final product depended entirely on my ability to:
- Ask the right questions
- Verify correctness
- Understand the code
- Test thoroughly
- Make informed modifications

All final code has been reviewed and tested. I can explain and defend every line of the implementation.

---

**Total Time Spent**:
- With Claude: ~4 hours (prompt engineering + verification)
- Estimated without Claude: ~20-25 hours (coding from scratch)
- Time saved: ~80%

**Code Quality**: Production-ready, well-documented, thoroughly tested
**Statistical Accuracy**: All calculations verified and correct
**Insight Quality**: Specific, data-driven, non-generic
