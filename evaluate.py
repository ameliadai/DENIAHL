from rouge import Rouge

def evaluate_model(ground_truth, results, metric):
    # print(ground_truth)
    # print(ground_truth)
    # print(results)
    # if isinstance(results[0],str):
    #     results = [int(s.strip().strip('"')) for s in results]
    # print(results)

    if metric == 'rouge':
        rouge = Rouge()
        scores = []
        for res in results:
            score = rouge.get_scores(res, ground_truth)
            scores.append(score[0]['rouge-1']['r'])
        return scores

    ground_truth = [str(t) for t in ground_truth]
    if metric == 'exact':
        scores = []
        for y, gt in zip(results, ground_truth):
            if isinstance(gt, (str)) and isinstance(y, (str)) and gt in y:
                scores.append(1)
            elif isinstance(gt, (str)) and isinstance(y, (str)) and gt not in y:
                scores.append(0)
            else:
                cleaned_y = ''.join(filter(str.isdigit, str(y)))
                str_gt = str(gt)

                if cleaned_y == str_gt:
                    scores.append(1)
                else:
                    scores.append(0)
        #scores = [1.0 if y in gt else 0.0 for y, gt in zip(results, ground_truth)]
    elif metric == 'hamming':
        scores = []
        for y, gt in zip(results, ground_truth):

            if len(y) != len(gt):
                scores.append(1-sum(c1 != c2 for c1, c2 in zip(y, gt))/len(gt))
    acc = sum(scores)/len(results)


    return acc
