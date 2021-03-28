import os
import shutil
import yaml


RAW_SPECS_PATH = 'tmp_raw_specs/specs'
OUTPUT_DIR = 'specs'


def clean_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    clean_folder(OUTPUT_DIR)
    base_specs_data = {}
    files = [file for file in os.listdir(RAW_SPECS_PATH) if file.endswith('yaml')]

    for base_spec_file in files:
        with open(os.path.join(RAW_SPECS_PATH, base_spec_file), 'r') as f:
            data = yaml.safe_load(f)
        procedure_spec_data = data['prozorro-sale-procedure']['spec']
        base_specs_data.update(procedure_spec_data)

    for spec_name, spec_content in base_specs_data.items():
        f_name = os.path.join(OUTPUT_DIR, spec_name + '.yml')
        with open(f_name, 'w') as f:
            data = yaml.dump({'procedure': spec_content}, f)
    print('Specs unpacked successfully!')
