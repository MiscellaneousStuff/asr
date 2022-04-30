import argparse
import os
import json
import csv
from unidecode import unidecode

parser = argparse.ArgumentParser(\
    description=\
        "Generates a regular ASR dataset from `DGaddy/Silent Speech` dataset")
parser.add_argument(\
    "--emg_data_dir", type=str, help="EMG Data path with audio and text", required=True)
parser.add_argument(\
    "--semg_transduction_preds_path",
    type=str,
    help="Override audio data with mel_spectrogram preds from semg transduction model")

args = parser.parse_args()

if __name__ == "__main__":
    base_dir = args.emg_data_dir
    
    """
    top_dirs = [
        ["closed_vocab/silent/", "silent"],
        ["closed_vocab/voiced/", "voiced"]]
    """
    
    """
    "nonparallel_data/",
    "voiced_parallel_data/"
    """
    
    top_dirs = [
        ["voiced_parallel_data", "voiced"],
        ["silent_parallel_data", "silent"],
        ["nonparallel_data",     "voiced"]
    ]

    # testset_path = "testset_closed.json"
    testset_path = "testset_largedev.json"

    with open(testset_path) as f:
        datasets = json.loads(f.read())

    csv_path = "metadata_dgaddy.csv"

    if args.semg_transduction_preds_path:
        csv_path = "metadata_dgaddy_preds.csv"

    with open(csv_path, "w", newline="") as csvfile:
        csv_writer = csv.writer(
            csvfile,
            delimiter="|",
            quotechar="'",
            quoting=csv.QUOTE_MINIMAL)
        for top_dir, modality in top_dirs:
            sub_dirs = os.listdir(os.path.join(base_dir, top_dir))
            for sub_dir in sub_dirs:
                cur_fis   = os.listdir(os.path.join(base_dir, top_dir, sub_dir))
                cur_infos = list(filter(lambda fi: fi.endswith(".json"), cur_fis))
                for info_fi in cur_infos:
                    info_path = os.path.join(base_dir, top_dir, sub_dir, info_fi)
                    with open(info_path) as f:
                        info = json.loads(f.read())
                        sentence_idx = info["sentence_index"]
                        book = info["book"]

                        if sentence_idx != -1:
                            file_idx = info_fi.split("_")[0]
                            fname = f"{file_idx}_audio_clean.flac"
                            audio_path = \
                                os.path.join(base_dir, top_dir, sub_dir, fname)

                            cur_pair = [book, sentence_idx]
                            dataset = "train"
                            dataset = "valid" if cur_pair in datasets["dev"]  else "train"
                            dataset = "test"  if cur_pair in datasets["test"] else "train"

                            valid_idxs = [d[1] for d in datasets["dev"]]

                            text = unidecode(info["text"])

                            if args.semg_transduction_preds_path:
                                
                                if book == "books/War_of_the_Worlds.txt":
                                    file_path = "/home/joe/projects/silent_speech/pred_audio/open_vocab_parallel"
                                else:
                                    file_path = "/home/joe/projects/silent_speech/pred_audio/open_vocab_non_parallel"
                                """
                                mel_spectrogram_path = \
                                    os.path.join(args.semg_transduction_preds_path, \
                                                 modality, \
                                                 str(sentence_idx))
                                """
                                mel_spectrogram_path = \
                                    os.path.join(file_path, \
                                                 modality, \
                                                 str(sentence_idx))
                                audio_path = mel_spectrogram_path

                            if modality == "voiced":
                                if sentence_idx in valid_idxs:
                                    dataset = "valid"
                                    
                            csv_writer.writerow([audio_path, text, dataset, modality])