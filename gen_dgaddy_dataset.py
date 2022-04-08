import argparse
import os
import json
import jiwer
import csv

parser = argparse.ArgumentParser(\
    description=\
        "Generates a regular ASR dataset from `DGaddy/Silent Speech` dataset")
parser.add_argument(\
    "--emg_data_dir", type=str, help="EMG Data path with audio and text", required=True)
args = parser.parse_args()

if __name__ == "__main__":
    base_dir = args.emg_data_dir
    top_dirs = [
        "closed_vocab/voiced/",
        "nonparallel_data/",
        "voiced_parallel_data/"
    ]
    # top_dirs = top_dirs[0:1]
    transformation = jiwer.Compose(\
        [jiwer.RemovePunctuation(), jiwer.ToLowerCase()])
    with open("metadata_dgaddy.csv", "w", newline="") as csvfile:
        csv_writer = csv.writer(
            csvfile,
            delimiter=" ",
            quotechar="|",
            quoting=csv.QUOTE_MINIMAL)
        for top_dir in top_dirs:
            sub_dirs = os.listdir(os.path.join(base_dir, top_dir))
            for sub_dir in sub_dirs:
                cur_fis   = os.listdir(os.path.join(base_dir, top_dir, sub_dir))
                cur_infos = list(filter(lambda fi: fi.endswith(".json"), cur_fis))
                for info_fi in cur_infos:
                    info_path = os.path.join(base_dir, top_dir, sub_dir, info_fi)
                    with open(info_path) as f:
                        info = json.loads(f.read())
                        sentence_idx = info["sentence_index"]

                        if sentence_idx != -1:
                            file_idx = info_fi.split("_")[0]
                            fname = f"{file_idx}_audio_clean.flac"
                            audio_path = \
                                os.path.join(base_dir, top_dir, sub_dir, fname)
                            text = info["text"]
                            normalised_text = transformation(text)
                            csv_writer.writerow([audio_path, text, normalised_text])