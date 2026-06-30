# Table 11. Significance Summary

Significance uses Wilcoxon signed-rank p-value when available; paired t-test p-value is also reported. Stars: *** p<0.001, ** p<0.01, * p<0.05, ns otherwise.

| experiment      | metric             | comparison   |   n_pairs |   mean_a |   mean_b |   mean_diff | direction   |   paired_t_p |   wilcoxon_p |   primary_p | significance   | significant_0.05   |
|:----------------|:-------------------|:-------------|----------:|---------:|---------:|------------:|:------------|-------------:|-------------:|------------:|:---------------|:-------------------|
| cross_arch_8b9b | correction_success | C2_minus_C1  |       150 |   0.819  |   0      |      0.819  | increase    |    3.31e-113 |     3.58e-27 |    3.58e-27 | ***            | True               |
| cross_arch_8b9b | correction_success | C3_minus_C1  |       150 |   0.8524 |   0      |      0.8524 | increase    |    1.08e-124 |     3.03e-27 |    3.03e-27 | ***            | True               |
| cross_arch_8b9b | correction_success | C2_minus_C0  |       150 |   0.819  |   0.0029 |      0.8162 | increase    |    9.87e-113 |     4.36e-27 |    4.36e-27 | ***            | True               |
| cross_arch_8b9b | correction_success | C3_minus_C2  |       150 |   0.8524 |   0.819  |      0.0333 | increase    |    0.0041    |     0.0111   |    0.0111   | *              | True               |
| cross_arch_8b9b | correction_success | C4_minus_C2  |       150 |   0.8257 |   0.819  |      0.0067 | increase    |    0.5544    |     0.3444   |    0.3444   | ns             | False              |
| cross_arch_8b9b | repeated_error     | C2_minus_C1  |       150 |   0.1467 |   0.8276 |     -0.681  | decrease    |    2.42e-89  |     1.69e-26 |    1.69e-26 | ***            | True               |
| cross_arch_8b9b | repeated_error     | C3_minus_C1  |       150 |   0.121  |   0.8276 |     -0.7067 | decrease    |    1.26e-94  |     1.72e-26 |    1.72e-26 | ***            | True               |
| cross_arch_8b9b | repeated_error     | C2_minus_C0  |       150 |   0.1467 |   0.821  |     -0.6743 | decrease    |    7.9e-90   |     1.67e-26 |    1.67e-26 | ***            | True               |
| cross_arch_8b9b | repeated_error     | C3_minus_C2  |       150 |   0.121  |   0.1467 |     -0.0257 | decrease    |    0.0196    |     0.0196   |    0.0196   | *              | True               |
| cross_arch_8b9b | repeated_error     | C4_minus_C2  |       150 |   0.1276 |   0.1467 |     -0.019  | decrease    |    0.0518    |     0.0443   |    0.0443   | *              | True               |
| cross_arch_8b9b | memory_recall      | C2_minus_C1  |       150 |   0.819  |   0      |      0.819  | increase    |    3.31e-113 |     3.58e-27 |    3.58e-27 | ***            | True               |
| cross_arch_8b9b | memory_recall      | C3_minus_C1  |       150 |   0.8524 |   0      |      0.8524 | increase    |    1.08e-124 |     3.03e-27 |    3.03e-27 | ***            | True               |
| cross_arch_8b9b | memory_recall      | C2_minus_C0  |       150 |   0.819  |   0      |      0.819  | increase    |    3.31e-113 |     3.58e-27 |    3.58e-27 | ***            | True               |
| cross_arch_8b9b | memory_recall      | C3_minus_C2  |       150 |   0.8524 |   0.819  |      0.0333 | increase    |    0.0041    |     0.0111   |    0.0111   | *              | True               |
| cross_arch_8b9b | memory_recall      | C4_minus_C2  |       150 |   0.8257 |   0.819  |      0.0067 | increase    |    0.5544    |     0.3444   |    0.3444   | ns             | False              |
| main_7b14b_qwen | correction_success | C2_minus_C1  |       100 |   0.8757 |   0      |      0.8757 | increase    |    2.32e-102 |     2.65e-19 |    2.65e-19 | ***            | True               |
| main_7b14b_qwen | correction_success | C3_minus_C1  |       100 |   0.8771 |   0      |      0.8771 | increase    |    1.25e-110 |     5.16e-20 |    5.16e-20 | ***            | True               |
| main_7b14b_qwen | correction_success | C2_minus_C0  |       100 |   0.8757 |   0      |      0.8757 | increase    |    2.32e-102 |     2.65e-19 |    2.65e-19 | ***            | True               |
| main_7b14b_qwen | correction_success | C3_minus_C2  |       100 |   0.8771 |   0.8757 |      0.0014 | increase    |    0.8849    |     0.5764   |    0.5764   | ns             | False              |
| main_7b14b_qwen | correction_success | C4_minus_C2  |       100 |   0.8414 |   0.8757 |     -0.0343 | decrease    |    0.0023    |     0.013    |    0.013    | *              | True               |
| main_7b14b_qwen | repeated_error     | C2_minus_C1  |       100 |   0.1086 |   0.8129 |     -0.7043 | decrease    |    4.04e-66  |     2.88e-18 |    2.88e-18 | ***            | True               |
| main_7b14b_qwen | repeated_error     | C3_minus_C1  |       100 |   0.11   |   0.8129 |     -0.7029 | decrease    |    5.68e-69  |     2.59e-18 |    2.59e-18 | ***            | True               |
| main_7b14b_qwen | repeated_error     | C2_minus_C0  |       100 |   0.1086 |   0.8029 |     -0.6943 | decrease    |    5.54e-65  |     2.94e-18 |    2.94e-18 | ***            | True               |
| main_7b14b_qwen | repeated_error     | C3_minus_C2  |       100 |   0.11   |   0.1086 |      0.0014 | increase    |    0.8972    |     0.9253   |    0.9253   | ns             | False              |
| main_7b14b_qwen | repeated_error     | C4_minus_C2  |       100 |   0.1243 |   0.1086 |      0.0157 | increase    |    0.1803    |     0.1825   |    0.1825   | ns             | False              |
| main_7b14b_qwen | memory_recall      | C2_minus_C1  |       100 |   0.8757 |   0      |      0.8757 | increase    |    2.32e-102 |     2.65e-19 |    2.65e-19 | ***            | True               |
| main_7b14b_qwen | memory_recall      | C3_minus_C1  |       100 |   0.8771 |   0      |      0.8771 | increase    |    1.25e-110 |     5.16e-20 |    5.16e-20 | ***            | True               |
| main_7b14b_qwen | memory_recall      | C2_minus_C0  |       100 |   0.8757 |   0      |      0.8757 | increase    |    2.32e-102 |     2.65e-19 |    2.65e-19 | ***            | True               |
| main_7b14b_qwen | memory_recall      | C3_minus_C2  |       100 |   0.8771 |   0.8757 |      0.0014 | increase    |    0.8849    |     0.5764   |    0.5764   | ns             | False              |
| main_7b14b_qwen | memory_recall      | C4_minus_C2  |       100 |   0.8414 |   0.8757 |     -0.0343 | decrease    |    0.0023    |     0.013    |    0.013    | *              | True               |
