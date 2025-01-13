import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
# Values used to find a makeshift matrix during the initial phase of a manufacture being added to the system
D=[]
M=[]

class VinProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VIN Processor")
        self.root.configure(bg="black")
        self.root.geometry("400x600")
        self.root.minsize(800, 800)

        # Initialize variables
        self.input_file = None
        self.output_directory = None
        self.placeholder_input = None
        self.placeholder_output = None
        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        status_text = ''
        # Create a frame to hold the entire content with a black background and a border
        main_frame = tk.Frame(root, bg="black", bd=10)
        main_frame.pack(fill="both", expand=True)

        # Row 2 Frame: Large box spanning all of width
        self.TopRow = tk.Frame(main_frame, bg="black", bd=10)
        self.TopRow.pack(fill="x", pady=10)
        self.TopRow.rowconfigure(0, weight=1)
        self.TopRow.rowconfigure(1, weight=1)
        self.TopRow.rowconfigure(2, weight=1)
        self.TopRow.columnconfigure(0, weight=1)
        self.TopRow.columnconfigure(1, weight=1)

        self.Input = tk.Button(self.TopRow, bg="white", font=("Arial", 16), height=5, width=50, text="Input ", cursor='hand2',
                          relief='flat', bd=1, activebackground='red', command=self.select_file)
        self.Input.grid(row=0, column=0, columnspan=1, padx=10, pady=5)

        self.Output = tk.Button(self.TopRow, bg="white", font=("Arial", 16), height=5, width=50, text="Output", cursor='hand2',
                           relief='flat', bd=1, activebackground='red', command=self.select_output_directory)
        self.Output.grid(row=0, column=1, columnspan=1, padx=10, pady=5)

        self.status_label = tk.Label(self.TopRow, font=("Rubik", 16),
                             text='Please input the CSV file and choose a output folder.\n\nCSV files can use ="" formating however any other changes to the text used may cause errors.\n\nAll pre-existing output files in the chosen flder will be overidden.', bg="white",
                             fg='black', height=30, width=100, justify='center', wraplength=660)
        self.status_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.large_button = tk.Button(self.TopRow, bg="white", fg='Black', font=("Rubik", 16), height=5, width=100,
                                 text="Run Processing", cursor='hand2', bd=1, activebackground="red",
                                 activeforeground="black", command=self.run_processing)
        self.large_button.grid(row=2, column=0, columnspan=2, padx=10, pady=15)

    def check_files(self):
        # Determine the directory of the executable or script
        if getattr(sys, 'frozen', False):  # Check if running as a PyInstaller bundle
            script_dir = os.path.dirname(sys.executable)
        else:  # Running in a normal Python environment
            script_dir = os.path.dirname(os.path.abspath(__file__))

        # List of expected matrix files
        expected_files = [
            'FordMatrix.csv',
            'MazdaMatrix.csv',
            'ToyotaMatrix.csv',
            'LandRoverMatrix.csv',
            'JaguarMatrix.csv'
        ]

        # Check for missing files
        missing_files = [file for file in expected_files if not os.path.isfile(os.path.join(script_dir, file))]

        # Return the result
        if missing_files:
            # Display an error message with missing files
            missing_files_str = "\n".join(missing_files)
            messagebox.showerror("Error", f"Missing the following required files:\n{missing_files_str}")
            return False
        else:
            return True

    def select_file(self):
        self.input_file = filedialog.askopenfilename(
            title="Select a CSV File",
            filetypes=[("CSV Files", "*.csv")]
        )
        if self.input_file:
            if self.placeholder_output:
                self.update_status('replace', f'\nInput CSV File;\n{self.placeholder_input}')
            self.update_status('additive', f'\nInput CSV File;\n{self.input_file}')
            self.Input.config(bg='red', activebackground='white', relief='sunken')
            self.placeholder_input = self.input_file
        else:
            self.update_status('replace', f'\nInput CSV File;\n{self.placeholder_input}')
            self.Input.config(bg='white', activebackground='red', relief='flat')

    def select_output_directory(self):
        self.output_directory = filedialog.askdirectory(
            title="Select Output Directory"
        )
        if self.output_directory:
            if self.placeholder_output:
                self.update_status('replace', f'\nOutput Directory;\n{self.placeholder_output}')
            self.update_status('additive', f'\nOutput Directory;\n{self.output_directory}')
            self.Output.config(bg='red', activebackground='white', relief='sunken')
            self.placeholder_output = self.output_directory
        else:
            self.update_status('replace', f'\nOutput Directory;\n{self.placeholder_output}')
            self.Output.config(bg='white', activebackground='red', relief='flat')

    def update_status(self, type, text):
        if text != '' and type == 'replace':
            original_text = self.status_label.cget('text')
            self.status_label.config(text=original_text.replace(text, ""))
        elif text != '' and type == 'additive':
            original_text = self.status_label.cget('text')
            if original_text.startswith('Please') or original_text.startswith('Processing'):
                self.status_label.config(text=str(text))
            else:
                self.status_label.config(text=f"{original_text}\n{text}")
        elif text != '' and type == 'override':
            self.status_label.config(text=str(text))

        if self.input_file and self.output_directory:
            self.large_button.config(bg='red', activebackground='white')
        else:
            self.large_button.config(bg='white', activebackground='red')

    def run_processing(self):
        if not self.input_file or not self.output_directory:
            messagebox.showerror("Error", "Please select both input file and output directory.")
            return
        if not self.check_files():
            messagebox.showerror("Error", "Please ensure the accompanying Matrix CSV Files are present!.")
            return
        try:
            # Load and Globalise the Matrix CSV Files
            global ford_matrix, ford_matrix_columns, mazda_matrix, mazda_matrix_columns, toyota_matrix, toyota_matrix_columns, landrover_matrix, landrover_matrix_columns, jaguar_matrix, jaguar_matrix_columns
            ford_matrix = pd.read_csv('FordMatrix.csv')
            ford_matrix_columns = ford_matrix.columns.tolist()
            mazda_matrix = pd.read_csv('MazdaMatrix.csv')
            mazda_matrix_columns = mazda_matrix.columns.tolist()
            toyota_matrix = pd.read_csv('ToyotaMatrix.csv')
            toyota_matrix_columns = toyota_matrix.columns.tolist()
            landrover_matrix = pd.read_csv('LandRoverMatrix.csv')
            landrover_matrix_columns = landrover_matrix.columns.tolist()
            jaguar_matrix = pd.read_csv('JaguarMatrix.csv')
            jaguar_matrix_columns = jaguar_matrix.columns.tolist()

            # Load the input file
            df = pd.read_csv(self.input_file)

            # Initialize dataframes and lists for processing VINs
            df_confirmed_vins = pd.DataFrame()
            df_incorrect_vins = pd.DataFrame()
            incorrect_vins = []
            invalid_vins = []
            confirmed_vins = []

            # Run the function
            df, df_incorrect_vins, df_confirmed_vins, invalid_vins, incorrect_vins = self.sort_vins(
                df, invalid_vins, incorrect_vins, confirmed_vins)

            # Convert lists to DataFrames and reset indices
            invalid_vins_df = pd.DataFrame(invalid_vins).reset_index(drop=True)
            incorrect_vins_df = pd.DataFrame(incorrect_vins).reset_index(drop=True)

            # Combine incorrect DataFrames
            combined_incorrect_vins_df = pd.concat([incorrect_vins_df, invalid_vins_df], ignore_index=True)
            combined_incorrect_vins_df = combined_incorrect_vins_df.reset_index(drop=True)

            # Define output file paths
            correct_vins_file = f"{self.output_directory}/correct_vins.csv"
            incorrect_vins_file = f"{self.output_directory}/incorrect_vins.csv"
            invalid_vins_file = f"{self.output_directory}/invalid_vins.csv"

            # Testing Procedure
            # Create a DataFrame D + M
            df = pd.DataFrame({
                'Make': D,
                'Model': M
            })
            # Group by Make and Model, and count occurrences
            grouped_df = df.groupby(['Make', 'Model']).size().reset_index(name='Count')

            # Save DataFrames to output CSV files
            df_confirmed_vins.to_csv(correct_vins_file, index=False)
            incorrect_vins_df.to_csv(incorrect_vins_file, index=False)
            invalid_vins_df.to_csv(invalid_vins_file, index=False)

            # Update status label
            self.update_status("override", f"Processing complete! \nNumber of Correct VINs: {len(df_confirmed_vins)} \nNumber of Invalid VINs: {len(invalid_vins_df)} \nNumber of Incorrect VINs: {len(incorrect_vins_df)}\nPlease check the output folder for the 3 CSV Files it now contains.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def sort_vins(self, df, invalid_vins, incorrect_vins, confirmed_vins):
        # Process the VINs
        df.apply(lambda row: self.distribute_vin(row, confirmed_vins, incorrect_vins, invalid_vins), axis=1)
        df_incorrect_vins = pd.DataFrame()
        # Convert lists to DataFrames
        df_confirmed_vins = pd.DataFrame(confirmed_vins).reset_index(drop=True)
        df_incorrect_vins = pd.concat([df_incorrect_vins, pd.DataFrame(incorrect_vins)], ignore_index=True)

        return df, df_incorrect_vins, df_confirmed_vins, invalid_vins, incorrect_vins

    def distribute_vin(self, row, confirmed_vins, incorrect_vins, invalid_vins):
        make = row['Make'].upper()
        if make in self.vin_validators:
            # Pass the required arguments when calling the validator
            self.vin_validators[make](self, row, confirmed_vins, incorrect_vins, invalid_vins)
        else:
            pass

    def verify_ford(self, row, confirmed_vins, incorrect_vins, invalid_vins):
        vin = row['VIN']
        if vin.startswith('="') and vin.endswith('"'):
            vin = vin[2:-1]
        model = row['Model']
        if model.startswith('="') and model.endswith('"'):
            model = model[2:-1]
        if len(vin) != 17:
            incorrect_vins.append(row.copy())
        else:
            if vin[8] in ford_matrix_columns:
                if model in ford_matrix[vin[8]].values:
                    confirmed_vins.append(row.copy())  # VIN is valid for Ford
                elif model == 'MUSTANG' or model == 'EDGE':
                    pass
                else:
                    invalid_vins.append(row.copy())  # VIN is invalid for Ford
            elif model == 'MUSTANG' or model == 'EDGE':
                pass
            else:
                incorrect_vins.append(row.copy())  # VIN is incorrect for Ford

    def verify_mazda(self, row, confirmed_vins, incorrect_vins, invalid_vins):
        vin = row['VIN']
        if vin.startswith('="') and vin.endswith('"'):
            vin = vin[2:-1]
        model = row['Model']
        if model.startswith('="') and model.endswith('"'):
            model = model[2:-1]
        if len(vin) != 17:
            incorrect_vins.append(row.copy())
        else:
            if vin[3:5] in mazda_matrix_columns:
                if model in mazda_matrix[vin[3:5]].values:
                    confirmed_vins.append(row.copy())
                else:
                    invalid_vins.append(row.copy())
            else:
                incorrect_vins.append(row.copy())

    def verify_toyota(self, row, confirmed_vins, incorrect_vins, invalid_vins):
        vin = row['VIN']
        if vin.startswith('="') and vin.endswith('"'):
            vin = vin[2:-1]
        model = row['Model']
        if model.startswith('="') and model.endswith('"'):
            model = model[2:-1]
        if vin[7] in toyota_matrix_columns:
            if model in toyota_matrix[vin[7]].values and len(vin) == 17:
                confirmed_vins.append(row.copy())
            elif model in toyota_matrix['SUB17'].values and len(vin) != 17:
                confirmed_vins.append(row.copy())
            else:
                invalid_vins.append(row.copy())
        else:
            incorrect_vins.append(row.copy())

    def verify_landrover(self, row, confirmed_vins, incorrect_vins, invalid_vins):
        vin = row['VIN']
        if vin.startswith('="') and vin.endswith('"'):
            vin = vin[2:-1]
        model = row['Model'].upper()
        if model.startswith('="') and model.endswith('"'):
            model = model[2:-1]
        if len(vin) != 17:
            incorrect_vins.append(row.copy())
        else:
            if vin[3] in landrover_matrix_columns:
                if model in landrover_matrix[vin[3]].values:
                    confirmed_vins.append(row.copy())
                else:
                    invalid_vins.append(row.copy())
            else:
                incorrect_vins.append(row.copy())

    def verify_jaguar(self, row, confirmed_vins, incorrect_vins, invalid_vins):
        vin = row['VIN']
        if vin.startswith('="') and vin.endswith('"'):
            vin = vin[2:-1]
        model = row['Model']
        if model.startswith('="') and model.endswith('"'):
            model = model[2:-1]
        if len(vin) != 17:
            incorrect_vins.append(row.copy())
        else:
            if model in jaguar_matrix_columns:
                if vin[0:7] in jaguar_matrix[model].values:
                    confirmed_vins.append(row.copy())
                else:
                    invalid_vins.append(row.copy())
            else:
                incorrect_vins.append(row.copy())

    vin_validators = {
        'FORD': verify_ford,
        'MAZDA': verify_mazda,
        'TOYOTA': verify_toyota,
        'LAND ROVER': verify_landrover,
        'JAGUAR': verify_jaguar,
        # TODO add more car makes (x) including a verify_x function and a xMatrix.csv
        # Add other makes here (e.g., 'TOYOTA': verify_toyota, etc.)
    }


# Create and run the application
root = tk.Tk()
app = VinProcessorApp(root)
root.mainloop()
