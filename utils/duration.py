# Gets the duration of the silent speech audio files in hours and minutes

import csv
import torchaudio
import os
metadata_path = "metadata_dgaddy.csv"

if not os.path.exists("duration.txt"):
    emg_total_bytes = 0
    audio_total_bytes = 0
    duration_secs = 0

    with open(metadata_path) as metadata:
        flist = csv.reader(metadata, delimiter="|", quotechar="'", quoting=csv.QUOTE_MINIMAL)
        flist = list(flist)
        for i, item in enumerate(flist):
            path, txt = item

            # Get audio duration
            waveform, sr = torchaudio.load(path)
            cur_secs = waveform.shape[1] / sr
            duration_secs += cur_secs

            # Get EMG size
            cur_emg_path = path.split("/")
            cur_idx = cur_emg_path[-1].split("_")[0]
            cur_emg_file = f"{cur_idx}_emg.npy"
            cur_emg_path = "/".join(cur_emg_path[0:-1]) + "/" + cur_emg_file
            emg_total_bytes   += os.path.getsize(cur_emg_path)
            audio_total_bytes += os.path.getsize(path)

            print(i, "/", len(flist), cur_secs, cur_emg_path)

    duration_mins  = duration_secs / 60
    hrs  = int(duration_mins // 60)
    mins = int(duration_mins % 60)

    with open("duration.txt", "w") as f:
        data = [hrs, mins, emg_total_bytes, audio_total_bytes]
        data = "\n".join([str(d) for d in data])
        f.write(data)
else:
    with open("duration.txt") as f:
        hrs, mins, emg_total_bytes, audio_total_bytes = f.read().split("\n")

print(f"Data duration (hrs, mins): {hrs}:{mins}")
print("EMG Data Size (bytes):    ", emg_total_bytes)
print("Audio Data Size (bytes):  ", audio_total_bytes)