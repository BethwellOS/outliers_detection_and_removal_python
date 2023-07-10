# Outlier detection and removal methods using Z-score, Percentile, and IQR in Jupyter Notebook

The code demonstrates how outliers can be detected and removed using Z-score, Percentile, and IQR. It focuses on applying these methods to identify and eliminate outliers in climate change data.

The methodology used in the paper includes three outlier detection and removal methods: Z-score, Percentile, and IQR.

The Z-score method is applied to columns with a normal or almost normal distribution. It identifies outliers by checking if a value falls outside of 3 standard deviations from the mean.

The Percentile method compares values to other scores from the same set. A value greater than the 99th or 95th percentile (depending on the problem statement) or less than the 1st or 5th percentile is considered an outlier.

The IQR (Inter Quartile Range) method is used for skewed data. It calculates the minimum and maximum values based on the 25th and 75th percentiles (Q1 and Q3). Any value less than the minimum or greater than the maximum is considered an outlier.

The repository provides code examples for implementing these methods for outlier detection and removal in climate change data.

Overall, the methodology involves applying these outlier detection and removal techniques to identify and handle outliers in the dataset.
