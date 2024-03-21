import json
import argparse
from pathlib import Path


def get_class_labels(data):
    class_labels_map = {}
    index = 0
    for class_label in data['labels']:
        class_labels_map[class_label] = index
        index += 1
    return class_labels_map


def load_ground_truth(ground_truth_path, subset):
    with ground_truth_path.open('r') as f:
        data = json.load(f)

    class_labels_map = get_class_labels(data)

    ground_truth = []
    for video_id, v in data['database'].items():
        if subset != v['subset']:
            continue
        this_label = v['annotations']['label']
        ground_truth.append((video_id, class_labels_map[this_label]))

    return ground_truth, class_labels_map


def load_result(result_path, top_k, class_labels_map):
    with result_path.open('r') as f:
        data = json.load(f)

    result = {}
    for video_id, v in data['results'].items():
        labels_and_scores = []
        for this_result in v:
            label = class_labels_map[this_result['label']]
            score = this_result['score']
            labels_and_scores.append((label, score))
        labels_and_scores.sort(key=lambda x: x[1], reverse=True)
        result[video_id] = list(zip(*labels_and_scores[:top_k]))[0]
    return result


def remove_nonexistent_ground_truth(ground_truth, result):
    exist_ground_truth = [line for line in ground_truth if line[0] in result]

    return exist_ground_truth


def evaluate(ground_truth_path, result_path, subset, top_k, ignore):
    print('load ground truth')
    ground_truth, class_labels_map = load_ground_truth(ground_truth_path,
                                                       subset)
    print('number of ground truth: {}'.format(len(ground_truth)))

    print('load result')
    result = load_result(result_path, top_k, class_labels_map)
    print('number of result: {}'.format(len(result)))

    n_ground_truth = len(ground_truth)
    ground_truth = remove_nonexistent_ground_truth(ground_truth, result)
    if ignore:
        n_ground_truth = len(ground_truth)
            
    print('calculate top-{} accuracy'.format(top_k))


    if args.otherMeasures is True:

        #print('ground_truth:')
        #print(ground_truth)
        #print('result:')
        #print(result)
        
        #[print('Ground truth: ',line[1],'\tResult: ',result[line[0]]) for line in ground_truth]
        #In our case 0 is abnormal, 1 is normal. Positive values are the abnormal and negative the normal.
        truePos = sum([1 if ((line[1] == 0) and (result[line[0]][0] == 0)) else 0 for line in ground_truth])
        trueNeg = sum([1 if ((line[1] == 1) and (result[line[0]][0] == 1)) else 0 for line in ground_truth])
        falsePos = sum([1 if ((line[1] == 1) and (result[line[0]][0] == 0)) else 0 for line in ground_truth])
        falseNeg = sum([1 if ((line[1] == 0) and (result[line[0]][0] == 1)) else 0 for line in ground_truth])
        print('truePos: ',truePos)
        print('trueNeg: ',trueNeg)
        print('falsePos: ',falsePos)
        print('falseNeg: ',falseNeg)

        accuracy = (truePos+trueNeg)/(truePos + trueNeg +falsePos + falseNeg)
        print('accuracy: ',accuracy)
        precision = truePos / (truePos + falsePos)
        print('precision: ',precision)
        recall = truePos/(truePos + falseNeg)
        print('recall: ',recall)
        f1 = 2 * (precision * recall) / (precision + recall)
        print('f1: ',f1)
        
    else:
        correct = [1 if line[1] in result[line[0]] else 0 for line in ground_truth]
        accuracy = sum(correct) / n_ground_truth


    print('top-{} accuracy: {}'.format(top_k, accuracy))
    return accuracy, precision, recall, f1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ground_truth_path', type=Path)
    parser.add_argument('result_path', type=Path)
    parser.add_argument('-k', type=int, default=1)
    parser.add_argument('--subset', type=str, default='validation')
    parser.add_argument('--save', action='store_true')
    parser.add_argument(
        '--ignore',
        action='store_true',
        help='ignore nonexistent videos in result')

    parser.add_argument(
        '--otherMeasures',action='store_true',
        help='If it is included, besides accuracy it calculates precision, recall and f1 score from a 2 class result\
        (first class as the main class for the purposes of these calculations)')
    
    args = parser.parse_args()

    if args.otherMeasures:

        accuracy,precision,recall,f1 = evaluate(args.ground_truth_path, args.result_path, args.subset,
                            args.k, args.ignore)    
    
    else:
    
        accuracy = evaluate(args.ground_truth_path, args.result_path, args.subset,
                            args.k, args.ignore)

    if args.save:

        print('args.otherMeasures: ',args.otherMeasures)
        print('args.otherMeasures is True: ',args.otherMeasures is True)
        
        if args.otherMeasures:

            print('FLAGSAVE1')
            with (args.result_path.parent / 'top{}.txt'.format(
                    args.k)).open('w') as f:
                f.write('accuracy,precision,recall,f1\n')
                row = '{},{},{},{}'.format(accuracy,precision,recall,f1)
                f.write(row)
        else:

            print('FLAGSAVE2')
            with (args.result_path.parent / 'top{}.txt'.format(
                    args.k)).open('w') as f:
                f.write(str(accuracy))
