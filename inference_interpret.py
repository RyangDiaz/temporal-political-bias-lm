from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from tqdm import tqdm
import glob
import csv
from lime.lime_text import LimeTextExplainer
import numpy as np
import argparse

from transcripts_inference import import_transcripts_by_year

tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
model = AutoModelForSequenceClassification.from_pretrained("bucketresearch/politicalBiasBERT").to('cuda')

def predict_prob(sample):
    inputs = tokenizer(sample, max_length=tokenizer.model_max_length, padding=True, truncation=True, return_tensors="pt").to('cuda')
    outputs = model(**inputs)
    logits = outputs[0]
    scores = logits.softmax(dim=-1)
    
    scores = scores.cpu().detach().numpy()

    return scores

def index_to_class(index):
    return ['left', 'center', 'right'][index]

def interpret_transcripts(transcripts, year, explainer, csv_file_path, filter_cnn=False):
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        for transcript_dict in tqdm(transcripts[f'{year}']):
            transcript = transcript_dict['transcript']
            date = None
            if 'date' in transcript_dict.keys():
                date = transcript_dict['date']
            if filter_cnn:
                transcript = transcript.replace('CNN', 'News Network')
            
            with torch.no_grad():
                pred = np.argmax(predict_prob(transcript))
                exp = explainer.explain_instance(transcript, predict_prob, num_features=6, num_samples=500, top_labels=3)
                # print(exp.available_labels())
                # print(exp.as_list(label=0))

            exp_list = exp.as_list(label=pred)
            writer.writerow([year, date, transcript, index_to_class(pred)] + [exp[0] for exp in exp_list] + [[exp[1] for exp in exp_list]])

def main(args):
    dataset = args.dataset
    csv_file_path = f'LIME_output/lime_outputs_{dataset}.csv'
    filter_cnn = args.filter_cnn

    os.makedir('LIME_output', exist_ok=True)

    transcripts = import_transcripts_by_year(dataset=dataset)

    class_names = ['left', 'center', 'right']
    explainer = LimeTextExplainer(class_names=class_names)

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Year', 'Date', 'Text', 'Prediction', 'Explainer 1', 'Explainer 2', 'Explainer 3', 'Explainer 4', 'Explainer 5', 'Explainer 6', 'Scores'])

    for year in range(min([int(year) for year in transcripts.keys()]),max([int(year) for year in transcripts.keys()])+1):
        interpret_transcripts(
            transcripts=transcripts,
            year=year,
            explainer=explainer,
            csv_file_path=csv_file_path,
            filter_cnn=True
        )

# def main1():
#     dataset = 'cnn_lad'
#     filter_cnn = True

#     transcripts = import_transcripts_by_year(dataset=dataset)
#     # sample = transcripts['2002'][45]['transcript']
#     sample = transcripts['2003'][84]['transcript']

#     if filter_cnn:
#         sample = sample.replace('CNN', 'News Network')

#     class_names = ['left', 'center', 'right']
#     explainer = LimeTextExplainer(class_names=class_names)

#     print(predict_prob(sample))
#     exp = explainer.explain_instance(sample, predict_prob, num_features=6, num_samples=30, top_labels=3) # 30
#     print(exp.as_list())

#     if filter_cnn:
#         filename = f'LIME_output/{dataset}_filtered_new.html'
#     else:
#         filename = f'LIME_output/{dataset}_new.html'

#     exp.save_to_file(filename, text=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default='tucker')
    parser.add_argument('--filter_cnn', action='store_true', default=False)
    args = parser.parse_args()
    main(args)