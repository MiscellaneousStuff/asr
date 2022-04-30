import csv

import jiwer
transformation = jiwer.Compose(\
        [jiwer.RemovePunctuation(), jiwer.ToLowerCase()])

if __name__ == "__main__":
    metadata_path = "metadata_dgaddy_preds.csv"

    with open(metadata_path) as metadata:
        with open("lexicon.txt", "w") as f:
            flist = csv.reader(metadata, delimiter="|", quotechar="'", quoting=csv.QUOTE_MINIMAL)
            _flist = list(flist)
            fis = []
            all_words = set()
            for fi in _flist:
                line = fi
                _, text, _, _  = line
                words = transformation(text)
                words = ''.join([i for i in words if not i.isdigit()])
                words = words.split(" ")
                all_words = all_words.union(set(words))
            all_words = list(all_words)
            all_words = list(filter(None, all_words))
            for word in all_words:    
                spaced    = " ".join([u for u in word])
                last      = "<unk>"
                f.write(f"{word} {spaced} {last}\n")