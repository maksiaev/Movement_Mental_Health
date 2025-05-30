import os
import csv
import glob
import argparse

import pandas as pd

from datetime import datetime
from tsfresh import extract_features

parser = argparse.ArgumentParser(description="Script extract features from patient activity files.")

parser.add_argument("-i", "--input-dir", type=str, default="C:/Users/maksi/Documents/Statistics/Projects/Movement_Mental_Health/hyperaktiv/hyperaktiv_with_controls/hyperaktiv_with_controls/activity_data/")
parser.add_argument("-o", "--output-dir", type=str, default="C:/Users/maksi/Documents/Statistics/Projects/Movement_Mental_Health/results/")

def read_activity_file(filepath, patient_id):
    data = [ ]
    with open(filepath) as f:
        csv_reader = csv.reader(f, delimiter=";")
        next(csv_reader)
        for line in csv_reader:
            data.append([ datetime.strptime(line[0], "%m-%d-%Y %H:%M").timestamp(), int(line[1].split(" ")[0])])
    data = pd.DataFrame(data, columns=["TIME", "ACC"])
    data["ID"] = patient_id
    return data
    
if __name__ == "__main__":
    
    args = parser.parse_args()
    
    input_dir = args.input_dir
    output_dir = args.output_dir
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filepath in glob.glob(os.path.join(input_dir, "*.csv")):
        print("Reading %s" % filepath)
        patient_id = os.path.splitext(os.path.basename(filepath))[0]
        feature_filepath = os.path.join(output_dir, "%s_features.csv" % patient_id)

        if os.path.exists(feature_filepath):
            print("Skipped...")
            continue
        
        data = read_activity_file(filepath, patient_id)
        features = extract_features(data, column_id="ID", column_value="ACC", column_sort="TIME", n_jobs=0, show_warnings=False)
        features.to_csv(feature_filepath, index=False, sep=";")    
    