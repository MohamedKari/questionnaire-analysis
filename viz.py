from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.pyplot import Axes

import fire

FORMAT = "png"
OUTPUT_DIR = Path("figures")

palettes = {
    "tlx": {
        1: cm.get_cmap("Greens", 11)(10),
        2: cm.get_cmap("Greens", 11)(9),
        3: cm.get_cmap("Greens", 11)(8),
        4: cm.get_cmap("Greens", 11)(7),
        5: cm.get_cmap("Greens", 11)(6),
        6: cm.get_cmap("Greens", 11)(5),
        7: cm.get_cmap("Greens", 11)(4),
        8: cm.get_cmap("Greens", 11)(3),
        9: cm.get_cmap("Greens", 11)(2),
        10: cm.get_cmap("Greens", 11)(1),
        11: cm.get_cmap("Reds", 10)(0),
        12: cm.get_cmap("Reds", 10)(1),
        13: cm.get_cmap("Reds", 10)(2),
        14: cm.get_cmap("Reds", 10)(3),
        15: cm.get_cmap("Reds", 10)(4),
        16: cm.get_cmap("Reds", 10)(5),
        17: cm.get_cmap("Reds", 10)(6),
        18: cm.get_cmap("Reds", 10)(7),
        19: cm.get_cmap("Reds", 10)(8),
        20: cm.get_cmap("Reds", 10)(9),
        20: cm.get_cmap("Reds", 10)(10)
    },
    "borg": {
        0: cm.get_cmap("Greens", 4)(2),
        1: cm.get_cmap("Greens", 4)(1),
        2: cm.get_cmap("Blues", 4)(1),
        3: cm.get_cmap("Blues", 4)(2),
        4: cm.get_cmap("Reds", 8)(1),
        5: cm.get_cmap("Reds", 8)(2),
        6: cm.get_cmap("Reds", 8)(3),
        7: cm.get_cmap("Reds", 8)(4),
        8: cm.get_cmap("Reds", 8)(5),
        9: cm.get_cmap("Reds", 8)(6),
        10: cm.get_cmap("Reds", 8)(7)
    }, 
    "likert": {
        1: cm.get_cmap("Reds", 4)(3),
        2: cm.get_cmap("Reds", 4)(2),
        3: cm.get_cmap("Reds", 4)(1),
        4: cm.get_cmap("Greens", 4)(0),
        5: cm.get_cmap("Greens", 4)(1),
        6: cm.get_cmap("Greens", 4)(2),
        7: cm.get_cmap("Greens", 4)(3),
    }
}


# https://matplotlib.org/stable/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html
def set_scale(ax, scale_name, scale_dict):
    # fig, ax = plt.subplots(figsize=(20, 1))
    
    for key, color_value in scale_dict.items():
        r, g, b, a = color_value
        bar_container =  ax.bar(key - 0.5, height=0.5, width=1, color=color_value)
        text_color = 'white' if r * g * b < 0.4 else 'black'

        ax.axis("on")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        ax.grid(False)
        ax.set_xlabel(scale_name, fontsize=15)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.bar_label(bar_container, labels=[key], label_type='center', color=text_color)
    
    # plt.savefig(f"{scale_name}.pdf", bbox_inches="tight")

    return ax


def viz_question(question_reponses: pd.DataFrame, condition: str, ax: Axes, question_id: str, question_text: str, scale: str):
    palette = palettes[scale or "default"]
    ax = sns.histplot(
        question_reponses, 
        y=condition, 
        hue='Response', 
        multiple='stack', 
        palette=palette, 
        hue_order=reversed(palette.keys()), 
        shrink=.8, 
        linewidth=0, 
        ax=ax, 
        alpha=0.8, 
        legend=False)
    
    ax.axis("on")
    ax.grid(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    ax.set_title(f"{question_id}: {question_text}")
    ax.set_xlabel("Participant ID")
    ax.set_ylabel("") # ax.set_ylabel("Condition")

    ax.tick_params(axis="y", which="major",length=0)
    ax.set_facecolor('white')

def load_questionnaire(path_to_csv):
    q = pd.read_csv(path_to_csv, sep=";")
    assert "Condition" in q.columns
    assert "QuestionId" in q.columns
    assert "QuestionText" in q.columns
    assert "Scale" in q.columns

    return q

def viz(path_to_csv):
    q = load_questionnaire(path_to_csv)
    
    cols_participants = set(q.columns).difference(set(["Condition", "QuestionId", "QuestionText", "Scale"]))

    print(f"Asserting {cols_participants} represent the responses per Participant")

    q_melted = q.melt(id_vars=["Condition", "QuestionId", "QuestionText", "Scale"], value_vars=cols_participants, var_name="ParticipantId", value_name="Response")
    scales = q_melted["Scale"].unique()

    for scale in scales:

        question_ids = q[q["Scale"] == scale]["QuestionId"].unique()
        n_questions = len(question_ids)

        # fig, axes = plt.subplots(n_questions, 1, figsize=(3 * n_questions, 1.1 * n_questions), 
        fig, axes = plt.subplots(n_questions, 1, figsize=(10, 1.5 * n_questions), 
            sharex="col", sharey="all",

            gridspec_kw={
                "hspace": 0.8, 
                "wspace": 0.1, 
                "left": 0.1, 
                "bottom": 0.4 * 1 / n_questions, 
                "right":0.9, 
                "top": 1 - (0.2 * 1 / n_questions)})
        
        for question_idx in range(n_questions):
            question_id = question_ids[question_idx]
            question_responses = q_melted[q_melted["QuestionId"] == question_id]
            
            
            question_text = question_responses["QuestionText"].values[0]
            question_scale = question_responses["Scale"].values[0]

            question_reponses = q_melted[q_melted["QuestionId"] == question_id]

            if n_questions > 1:
                ax = axes[question_idx]
            else:
                ax = axes

            viz_question(question_reponses, "Condition", ax, question_id, question_text, question_scale)
        
        
        # ax = fig.add_axes([0.25, 0.075, 0.5, 0.05])
        # set_scale(ax, scale, palettes[scale])
        OUTPUT_DIR.mkdir(exist_ok=True)
        plt.savefig(OUTPUT_DIR / f"questionnaire_{scale}.{FORMAT}")


        fig, ax = plt.subplots(figsize=(10, 1), gridspec_kw={"top": 1, "left": 0, "right": 1, "bottom": 0.5})
        set_scale(ax, scale, palettes[scale])
        fig.savefig(OUTPUT_DIR / f"scale_{scale}.{FORMAT}")

    

if __name__ == "__main__":
    # python viz.py questionnaire.csv
    fire.Fire(viz)
    