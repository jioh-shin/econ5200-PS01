"""Functions for checking data and calculating robust means"""

import numpy as np
import pandas as pd


def audit_report(df: pd.DataFrame) -> pd.DataFrame:
    """One row per column: missingness, dtype, skew and outlier count."""
    report = pd.DataFrame()
    report["missingness"] = df.isna().sum()
    report["dtype"] = df.dtypes
    report["skew"] = df.skew(numeric_only=True)
    outlier_counts = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            outlier_counts[col] = ((df[col] < q1 - 1.5 * iqr) |
                                   (df[col] > q3 + 1.5 * iqr)).sum()
        else:
            outlier_counts[col] = np.nan
    report["outlier_count"] = pd.Series(outlier_counts)
    return report


def robust_mean(x, method: str = "median", customer_id=None) -> float:
    """Calculate a robust average using median, trimming, or B2B exclusion."""
    if method == "median":
        return float(np.median(x))
    
    elif method == "trimmed":
        x_sorted = np.sort(x)
        n = len(x_sorted)
        cut = int(n * 0.1)
        return float(np.mean(x_sorted[cut:n-cut]))

    elif method == "b2b_exclusion":
        if customer_id is None:
            raise ValueError("customer_id is required for B2B exclusion")
        x = np.asarray(x)
        customer_id = np.asarray(customer_id)
        return float(np.mean(x[customer_id <= 1500]))
          
    else:
        raise ValueError("method must be 'median','trimmed',or 'b2b_exclusion")


if __name__ == "__main__":
    # A short demonstration that runs when the file is run as a script
    x = np.array([10, 20, 30, 40, 100])
    print("Median:", robust_mean(x, method="median"))
    print("Trimmed mean:", robust_mean(x, method="trimmed"))
