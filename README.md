# VIN Sorter Overview 🎯🎉🚗

## Introduction 🚦📂📊

The **VIN Sorter** is a Python-based application designed to analyse and categorize data from CSV files containing car makes, models, and Vehicle Identification Numbers (VINs). The application efficiently organizes this data into three distinct categories, ensuring accurate processing and management. The main focus of this system is to sort PNC data for data analytics.

---

## Available Makes 🔍🚗🎯

1. Ford
   - Checked Digits: 9

2. Mazda
   - Checked Digits: 4 to 6

3. Toyota
   - Checked Digits: 8
   - Includes SUB17 for values below 17 digits

4. Landrover
   - Checked Digits: 9

5. Landrover
   - Checked Digits: 4

6. Jaguar
   - Checked Digits: 1 to 8

7. Mercedes Benz
   - Checked Digits: 4 to 7

8. BMW
    - Currently No Digits Checked

9. Fiat
    - Currently No Digits Checked
   
10. Citroen
    - Currently No Digits Checked

**All makes with no digits checked will return all data as incorrect.**

---

## Categories 🚗✅❌

1. **Correct VINs**
   - VINs identified with absolute confidence as accurate and valid.

2. **Incorrect VINs**
   - VINs containing identifiable errors or inconsistencies that preclude their classification as correct.

3. **Invalid VINs**
   - Data that cannot be processed or classified due to:
     - Incompatibility with the system, often caused by the absence of a corresponding model inside of the matrix.
     - Insufficient confidence from the system's algorithms to categorize the data accurately, particularly for certain makes (e.g., Jaguar). 🛠️🔍📉

---

## Dependencies 🖥️🔗⚙️

The **VIN Sorter** relies on specific matrix files, which provide compatibility and processing rules for supported vehicle makes and models. These files are essential for accurate VIN categorization.

These Matrixes are directly corralated by the aforementioned checked digit. When edits are made to the matrixes the digit(s) will be evidently shown in the column names.

## Input Requirements 📝📤🔍

To function effectively, the input data must adhere to the following requirements:

- The input file must be in CSV format.
- The file must include the following three columns:
  - **Make**
  - **Model**
  - **VIN**

 ---

### Column Specifications 🧩📋✔️

- The order of the columns within the file is flexible, but their content must be correctly formatted.
- All entries must be free of extraneous symbols or characters.
- **Special Case**: Entries formatted as `="x"`, where `x` represents the original string, are allowed and will be processed correctly.

---

## Conclusion 📈🚀✅

By adhering to the specified input requirements and utilizing the required matrix files, the **VIN Sorter** provides a robust, reliable, and efficient solution for organizing and analysing vehicle data. Its advanced categorization capabilities ensure accuracy and confidence in data processing, making it a valuable tool for managing automotive information.
