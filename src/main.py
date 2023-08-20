
# This is a sample Python script.
from swat import google_utils
import vertexai
import pandas as pd
import openpyxl
import json


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def get_reports_multiple_patients(file="./resources/sample_report.xlsx"):
    df_report = pd.read_excel(file)
    df_report = df_report.round(2)
    df_units = pd.read_csv("resources/param_units.csv")
    params = list(df_report.columns)
    params.remove('Patient Name')
    params.remove('Patient Age')
    params.remove('Patient Gender')

    content_types = ['Diet Plan', 'Workout and Exercises', 'Lifestyle', 'Medicines and Drugs', 'Health Supplements']

    patient_plan = {}
    for index, row in df_report[:1].iterrows():
        df = dict(row)
        patient_plan['name'] = str(df['Patient Name'])
        patient_plan['age'] = str(df['Patient Age'])
        patient_plan['gender'] = str(df['Patient Gender'])
        response_dict = {}

        for content_type in content_types:
            prompt_summary_prefix = 'What {content_type} would you suggest to a patient who is ' + str(
                df['Patient Age']) + ' years old ' + str(df['Patient Gender']) + 'with '
            param_arr = []
            for col in params:
                unit = ""
                if len(df_units[df_units['param'] == col]['unit']) != 0:
                    unit = df_units[df_units['param'] == col]['unit'].values[0]

                param_arr.append(str(col) + 'value of ' + str(df[col]) + ' ' + str(unit))
            prompt_summary_str = (prompt_summary_prefix + ("and ".join(param_arr) + "?")).format(
                content_type=content_type)
            response = google_utils.get_response_from_prompt(prompt_summary_str)
            response_dict[content_type] = response.text

        patient_plan['plan'] = response_dict
        json_object = json.dumps(patient_plan, indent=4)
        return json_object


def get_reports_from_input(patient_detail=None):
    # patient_detail_keys = ['Patient Name', 'Patient Age', 'Patient Gender']
    if patient_detail is None:
        return json.dumps({}, indent=4)

    # pd.DataFrame(columns=['Patient Name', 'Patient Age', 'Patient Gender'])

    dict_report = {key: round(value, 2) if isinstance(value, (float, int)) else value for key, value in patient_detail.items()}
    dict_report = {key: ("" if value is None else value) for key, value in dict_report.items()}

    df_units = pd.read_csv("resources/param_units.csv")
    params = list(dict_report.keys())

    content_types = ['Diet Plan', 'Workout and Exercises', 'Lifestyle', 'Medicines and Drugs', 'Health Supplements']

    patient_plan = {'name': str(dict_report['Patient Name']), 'age': str(dict_report['Patient Age']), 'gender': str(dict_report['Patient Gender'])}
    response_dict = {}

    for content_type in content_types:
        prompt_summary_prefix = 'What {content_type} would you suggest to a patient who is ' + str(
            dict_report['Patient Age']) + ' years old ' + str(dict_report['Patient Gender']) + 'with '
        param_arr = []
        for col in params:
            unit = ""
            if len(df_units[df_units['param'] == col]['unit']) != 0:
                unit = df_units[df_units['param'] == col]['unit'].values[0]

            param_arr.append(str(col) + 'value of ' + str(dict_report[col]) + ' ' + str(unit))
        prompt_summary_str = (prompt_summary_prefix + ("and ".join(param_arr) + "?")).format(
            content_type=content_type)
        response = google_utils.get_response_from_prompt(prompt_summary_str)
        response_dict[content_type] = response.text

    patient_plan['plan'] = response_dict
    json_object = json.dumps(patient_plan, indent=4)
    print(json_object)
    return json_object


# if __name__ == '__main__':
#     google_utils.init_vertex_ai()
#     get_reports_multiple_patients()