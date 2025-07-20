# Option Assignment System

A Python web application that assigns options to users based on seniority and preferences from an Excel file.

## Features

- Upload Excel files (.xlsx or .xls)
- Automatic option assignment based on seniority
- Preference-based assignment algorithm
- Modern web interface
- Real-time validation and error handling

## How It Works

1. **Seniority-Based Processing**: The system processes users from top to bottom (most senior first)
2. **Preference Matching**: Each person gets their highest available preference
3. **No Duplicates**: Each option can only be assigned to one person
4. **Current User Focus**: The last row is treated as the current user uploading the file

## File Format Requirements

Your Excel file must contain the following columns:
- `Name`: Person's name
- `UDISE`: UDISE code
- `OPTION1` to `OPTION30`: Numerical preference values (1-30)

### Example Excel Structure:
| Name | UDISE | OPTION1 | OPTION2 | OPTION3 | ... | OPTION30 |
|------|-------|---------|---------|---------|-----|----------|
| John Doe | 12345 | 5 | 12 | 3 | ... | 20 |
| Jane Smith | 67890 | 8 | 1 | 15 | ... | 7 |
| Current User | 11111 | 2 | 9 | 4 | ... | 11 |

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open your browser and go to:**
   ```
   http://localhost:5000
   ```

## Usage

1. **Prepare your Excel file** with the required columns and data
2. **Sort by seniority** (most senior person at the top)
3. **Place yourself in the last row**
4. **Upload the file** through the web interface
5. **View your assigned option** and all other assignments

## Algorithm Details

The assignment algorithm works as follows:

1. **Initialize**: Start with no options assigned
2. **Process by seniority**: Go through each person from top to bottom
3. **Find available preference**: For each person, find their highest preference that hasn't been assigned yet
4. **Assign option**: Give that person their highest available preference
5. **Continue**: Move to the next person and repeat

## Example Scenario

If you have 3 people and 5 options:

**Person 1 (Most Senior):**
- Preferences: [3, 1, 5]
- Gets: Option 3

**Person 2:**
- Preferences: [1, 2, 4]
- Gets: Option 1 (Option 3 is already taken)

**Person 3 (Current User):**
- Preferences: [2, 4, 5]
- Gets: Option 2 (Options 1 and 3 are already taken)

## Error Handling

The application handles various error scenarios:
- Invalid file formats
- Missing required columns
- Empty files
- Data processing errors
- Invalid preference values

## Technical Requirements

- Python 3.7 or higher
- Flask web framework
- Pandas for data processing
- OpenPyXL for Excel file reading

## Security Notes

- Change the `secret_key` in `app.py` for production use
- The application currently runs in debug mode (disable for production)
- File uploads are processed in memory (no permanent storage)

## Troubleshooting

**Common Issues:**

1. **"Missing required columns" error:**
   - Ensure your Excel file has exactly: Name, UDISE, OPTION1, OPTION2, ..., OPTION30

2. **"Invalid file type" error:**
   - Make sure you're uploading a .xlsx or .xls file

3. **"Excel file is empty" error:**
   - Check that your Excel file contains data in the required format

4. **Installation issues:**
   - Make sure you have Python 3.7+ installed
   - Try upgrading pip: `pip install --upgrade pip`
   - Install dependencies one by one if needed

## License

This project is open source and available under the MIT License. 