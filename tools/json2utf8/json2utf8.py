import os
import json
import argparse
from tqdm import tqdm

def convert_json_file(input_path, output_path, encoding):
    try:
        with open(input_path, 'r', encoding=encoding) as f:
            data = json.load(f)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        print(f"[!] JSON error in {input_path}: {e}")

def convert_jsonl_file(input_path, output_path, encoding):
    try:
        with open(input_path, 'r', encoding=encoding) as fin, \
             open(output_path, 'w', encoding='utf-8') as fout:
            for lineno, line in enumerate(fin, 1):
                try:
                    obj = json.loads(line.strip())
                    fout.write(json.dumps(obj, ensure_ascii=False) + '\n')
                except json.JSONDecodeError as e:
                    print(f"[!] Skipping line {lineno} in {input_path}: {e}")
    except UnicodeDecodeError as e:
        print(f"[!] Decode error in {input_path}: {e}")

def collect_json_files(input_dir):
    json_files = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.json') or file.lower().endswith('.jsonl'):
                full_path = os.path.join(root, file)
                json_files.append(full_path)
    return json_files

def convert_directory(input_dir, output_dir, encoding):
    json_files = collect_json_files(input_dir)
    if not json_files:
        print("[!] No .json or .jsonl files found.")
        return

    for input_path in tqdm(json_files, desc="Converting files", unit="file"):
        rel_path = os.path.relpath(input_path, input_dir)
        output_path = os.path.join(output_dir, rel_path)

        if input_path.lower().endswith('.json'):
            convert_json_file(input_path, output_path, encoding)
        elif input_path.lower().endswith('.jsonl'):
            convert_jsonl_file(input_path, output_path, encoding)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert non-UTF-8 .json and .jsonl files to UTF-8.")
    parser.add_argument("input_dir", help="Input directory with .json/.jsonl files")
    parser.add_argument("output_dir", help="Output directory for UTF-8 converted files")
    parser.add_argument("--encoding", default="windows-1251", help="Input file encoding (default: windows-1251)")

    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        print(f"[!] Input directory not found: {args.input_dir}")
    else:
        convert_directory(args.input_dir, args.output_dir, args.encoding)
