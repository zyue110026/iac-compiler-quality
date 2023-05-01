from compiler_fuzzing.utils.yaml import get_config, get_yaml_data, check_ansible_syntax
from compiler_fuzzing.strings import remove_tilda
from compiler_fuzzing.openai import get_response
from compiler_fuzzing.utils.log_utils import *
from tqdm import tqdm
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--config", type=str, default="compilier_fuzzing/confs/config.yaml")
args = parser.parse_args()

config = get_config(name=args.config)

dummy_prompt = config["dummy_prompt"]
github_data_path = config["github_issue_path"]
github_issue_file_name = config['github_issue_file_name']

def get_prompts(df):
    df['prompt'] = dummy_prompt + df['TITLE']
    
    return df
def get_dataframe(path, generation_limit=10):
    df = pd.read_excel(path)
    
    df = get_prompts(df)
    df['response'] = ''
    df = df[:generation_limit]

    count = 0
    list_of_responses = []
    
    with tqdm(total=None, desc="Generating playbooks") as pbar:
        for ind in df.index:
            if count >= generation_limit:
                break
            if df.iloc[ind]['response'] == '':
                resp = get_response(df.iloc[ind]['prompt'], config=config)
                response = resp['choices'][0]['message']['content']
                logger.info(f"response: {response}")
                column_index = df.columns.get_loc('response')
                df.iloc[ind, column_index] = response
                pbar.update(1)
                count += 1
    
    print("Number of playbooks created:", (df.response != '').sum())           
    return df
    

def get_valid_annotation(df):
    df['code'] =df['response'].apply(remove_tilda)
    df['valid_yaml'] = df['code'].apply(get_yaml_data)
    # df['valid_syntax'] = df['code'].apply(check_ansible_syntax)
    print(df['valid_yaml'].sum(), df['valid_syntax'].sum())
    return df

def main():
	excel_path = f"{github_data_path}/{github_issue_file_name}"
	df = get_dataframe(excel_path, generation_limit=5)

	df = get_valid_annotation(df)

	df.to_feather(f'{github_data_path}/chatgpt_github_yaml.feather', index=False)

	df.to_csv(f'{github_data_path}/chatgpt_github_yaml.csv', index=False)

