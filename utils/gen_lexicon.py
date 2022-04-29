import csv
import jiwer

transformation = jiwer.Compose(\
        [jiwer.RemovePunctuation(), jiwer.ToLowerCase()])

if __name__ == "__main__":
    utterances = set()
    
    with open("metadata_dgaddy_preds.csv") as metadata:
        flist = csv.reader(metadata, delimiter="|", quotechar="'", quoting=csv.QUOTE_MINIMAL)
        _flist = list(flist)
        fis = []
        for fi in _flist:
            line = fi
            _, text, _, _ = line
            utterance = transformation(text).split(" ")
            utterances = utterances.union(set(utterance))
    
    utterances = list(utterances)
    utterances = list(filter(None, utterances))

    with open("lexicon.txt", "w") as f:
        for utter in utterances:
            word        = utter
            tokens      = "".join([w + " " for w in word])
            space_split = " "
            f.write(f"{word} {tokens}{space_split}\n")