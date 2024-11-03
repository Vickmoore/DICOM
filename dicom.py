import os
import shutil
import pydicom
import warnings
import logging

data_folder = 'C:/Users/USER/Desktop/data'
output_folder = 'sorted_data'

def print_dicom_attributes(file_path):
    try:
        dicom_data = pydicom.dcmread(file_path)
        print(f"Attributes for {file_path}:")
        for elem in dicom_data:
            print(f"{elem.tag}: {elem.name} ({elem.VR}): {elem.value}")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

for file_name in os.listdir(data_folder):
    if file_name.endswith('.dcm'):
        file_path = os.path.join(data_folder, file_name)
        print_dicom_attributes(file_path)

def create_dir(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            logging.info(f"Created directory {path}")
    except Exception as e:
        logging.error(f"Error creating directory {path}: {e}")

def modify_filename(filename):
    return filename.replace(':', '_').replace('\\', '_').replace('/', '_').replace('?', '_').replace('*', '_')

def get_unique_filename(folder_path, file_name):
    base, ext = os.path.splitext(file_name)
    counter = 1
    new_file_name = file_name
    while os.path.exists(os.path.join(folder_path, new_file_name)):
        new_file_name = f"{base}_{counter}{ext}"
        counter += 1
    return new_file_name

for file_name in os.listdir(data_folder):
    if file_name.endswith('.dcm'):
        file_path = os.path.join(data_folder, file_name)
        try:
            dicom_data = pydicom.dcmread(file_path)

            # Extract and sanitize metadata
            modality = modify_filename(dicom_data.Modality)
            body_part = modify_filename(dicom_data.BodyPartExamined)
            patient_id = modify_filename(dicom_data.PatientID)

            # Define folder paths
            modality_folder = os.path.join(output_folder, modality)
            body_part_folder = os.path.join(modality_folder, body_part)
            patient_folder = os.path.join(body_part_folder, patient_id)

            # Create the required directories
            create_dir(patient_folder)

            # Ensure the file exists before moving
            if not os.path.exists(file_path):
                logging.error(f"File {file_path} does not exist")
                continue

            # Move the file to the new directory
            dest_file_name = get_unique_filename(patient_folder, file_name)
            dest_path = os.path.join(patient_folder, dest_file_name)
            shutil.move(file_path, dest_path)
            logging.info(f"Moved {file_name} to {dest_path}")

        except Exception as e:
            logging.error(f"Error processing {file_name}: {e}")

logging.info("Sorting complete!")