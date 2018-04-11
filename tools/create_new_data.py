import sys
import json
# this script generates a json file based file with messages to be sent to kafka.


def main(dataFile):
    with open(dataFile, 'r') as fin:
        for line in fin:
            ps=parse_line(line)
            print(ps)

def parse_line(line):
    mtr={}
    if line != "<EXPERIMENT_COMPLETED>":
        parts = line.rstrip().split('\t')
        mtr["time"] = float(parts[0])
        mtr["experimentTime"] = float(parts[1])
        mtr["epochs"] = float(parts[2])
        mtr["count"] = float(parts[2])
        mtr["cost"] = float(parts[3])
        mtr["accuarcy"] = float(parts[4])
        mtr["precision"] = float(parts[5])
        mtr["recall"] = float(parts[6])
        mtr["true_positives"] = float(parts[7])
        mtr["false_positives"] = float(parts[8])
        mtr["false_negatives"] = float(parts[9])
        return json.dumps({"type": "metrics", "metrics": mtr})
    else:
        return json.dumps({"type": "service", "msg": "experiment_completed"})
    return None



if __name__ == '__main__':
    main(sys.argv[1])
