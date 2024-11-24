import wandb
import pandas as pd

def log_to_wandb(prompts, ground_truth, results, acc, experiment_name):

    # log the result table
    df = pd.DataFrame({
            'prompt': prompts,
            'ground_truth': ground_truth,
            'result': results
            })
    res_table = wandb.Table(dataframe=df)

    # start a new wandb run to track this script
    wandb.init(
        project="DENIAL",
        name=experiment_name
    )

    wandb.log({"accuracy": acc, "results_table": res_table})

    # [optional] finish the wandb run, necessary in notebooks
    wandb.finish()