from flask import Flask, render_template, request, flash, redirect, url_for
import pandas as pd
import os
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def assign_options(df):
    """
    Assign options to people based on seniority (top to bottom).
    Each option can only be assigned to one person.
    """
    # Get the number of people and options
    num_people = len(df)
    num_options = 30  # OPTION1 to OPTION30
    
    # Initialize assignment tracking
    assigned_options = set()  # Track which options have been assigned
    assignments = {}  # Track who got what option
    
    # Process each person in order of seniority (top to bottom)
    for index, row in df.iterrows():
        person_name = row['Name']
        person_udise = row['UDISE']
        
        # Get their preferences (OPTION1 to OPTION30)
        preferences = []
        for i in range(1, 31):
            option_col = f'OPTION {i}'
            if option_col in row and pd.notna(row[option_col]):
                preferences.append(int(row[option_col]))
        
        # Find the first available option from their preferences
        assigned_option = None
        for preference in preferences:
            if preference not in assigned_options:
                assigned_option = preference
                assigned_options.add(preference)
                break
        
        # Store the assignment
        assignments[index] = {
            'name': person_name,
            'udise': person_udise,
            'assigned_option': assigned_option,
            'preferences': preferences
        }
    
    return assignments

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['file']
        
        # Check if file was selected
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload an Excel file (.xlsx or .xls)')
            return redirect(request.url)
        
        try:
            # Read the Excel file
            df = pd.read_excel(file)
            
            # Validate required columns
            required_columns = ['Name', 'UDISE']
            option_columns = [f'OPTION{i}' for i in range(1, 31)]
            all_required = required_columns + option_columns
            
            missing_columns = [col for col in all_required if col not in df.columns]
            if missing_columns:
                flash(f'Missing required columns: {", ".join(missing_columns)}')
                return redirect(request.url)
            
            # Check if file has data
            if len(df) == 0:
                flash('Excel file is empty')
                return redirect(request.url)
            
            # Perform the assignment
            assignments = assign_options(df)
            
            # Get the current user's assignment (last row)
            current_user_index = len(df) - 1
            current_user_assignment = assignments.get(current_user_index)
            
            if current_user_assignment is None:
                flash('Error processing current user assignment')
                return redirect(request.url)
            
            # Prepare data for template
            all_assignments = []
            for index, assignment in assignments.items():
                all_assignments.append({
                    'rank': index + 1,
                    'name': assignment['name'],
                    'udise': assignment['udise'],
                    'assigned_option': assignment['assigned_option'],
                    'preferences': assignment['preferences'][:5]  # Show first 5 preferences
                })
            
            return render_template('results.html', 
                                assignments=all_assignments,
                                current_user=current_user_assignment,
                                total_people=len(df))
            
        except Exception as e:
            flash(f'Error processing file: {str(e)}')
            return redirect(request.url)
    
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 