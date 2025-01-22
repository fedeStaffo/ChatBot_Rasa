import os
import glob
import yaml

"""
Domain's intents are extracted from NLU's intents.
"""

input_path = 'data/nlu'
output_file = 'domains/intents.yml'
intents_yml = {'verson': '3.1', 'intents': []}

globs = glob.glob(os.path.join(input_path, '*.yml'))
for filename in globs:
    with open(filename, 'r', encoding='utf-8') as fp:
        yaml_file = yaml.safe_load(fp)
        intents = map(lambda item: item['intent'], filter(
            lambda item: 'intent' in item, yaml_file['nlu']))
        intents_yml['intents'].extend(intents)

print(intents_yml)

with open(output_file, 'w', encoding='utf-8') as fp:
    yaml.safe_dump(intents_yml, fp, sort_keys=False)
