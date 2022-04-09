# Gets the duration of the silent speech audio files in hours and minutes

import csv
import torchaudio

duration_secs = 0
metadata_path = "metadata_dgaddy.csv"
with open(metadata_path) as metadata:
    flist = csv.reader(metadata, delimiter="|", quotechar="'", quoting=csv.QUOTE_MINIMAL)
    flist = list(flist)
    for i, item in enumerate(flist):
        path, txt = item
        waveform, sr = torchaudio.load(path)
        duration_secs += waveform.shape[1] / sr
        print(i, "/", len(flist))

duration_mins  = duration_secs / 60
hrs  = duration_mins // 60
mins = duration_mins % 60

print(f"{hrs}:{mins}")