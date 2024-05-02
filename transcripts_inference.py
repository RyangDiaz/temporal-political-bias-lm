from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from tqdm import tqdm
import glob
import csv
import argparse
import sys
import os

csv.field_size_limit(sys.maxsize)

def import_transcripts_by_year(dataset='fox'):
    assert dataset in ['fox_news', 'tucker', 'lemon', 'nyt', 'cnn_ltm', 'cnn_lad']
    transcripts = {}
    if dataset == 'fox_news':
        for f in glob.glob('data/transcripts_fox/*.txt'):
            year = f.split('.')[0].split('-')[-1]
            date = f.split('/')[-1].split('.')[0]
            if year not in transcripts.keys():
                transcripts[f'{year}'] = []
            
            with open(f, 'r', encoding='windows-1252') as fl:
                transcripts[f'{year}'].append({'date': date, 'transcript': fl.read()})
    elif dataset == 'tucker':
        for f in glob.glob('data/transcripts_tucker/*.txt'):
            with open(f, 'r', encoding='windows-1252') as fl:
                script = fl.read()
                if len(script) >= 60:
                    year = f.split('/')[-1].split('-')[0]
                    date = f.split('/')[-1].split('.')[0]
                    if year not in transcripts.keys():
                        transcripts[f'{year}'] = []
                    transcripts[f'{year}'].append({'date': date, 'transcript': script})
    elif dataset == 'lemon':
        for f in glob.glob('data/transcripts_lemon/*.txt'):
            with open(f, 'r') as fl:
                script = fl.read()
                if len(script) >= 40:
                    year = f.split('/')[-1].split('-')[0]
                    date = f.split('/')[-1].split('.')[0]
                    if year not in transcripts.keys():
                        transcripts[f'{year}'] = []
                    transcripts[f'{year}'].append({'date': date, 'transcript': script})
    elif dataset == 'nyt':
        for f in glob.glob('data/nyt_headlines/*.csv'):
            year = f.split('/')[-1].split('-')[0]
            if year not in transcripts.keys():
                transcripts[f'{year}'] = []

            with open(f, newline='') as csvfile:
                reader = csv.reader(csvfile)
                max_file, curr_file = 100, 0
                for row in reader:
                    if curr_file > 0 and curr_file <= max_file:
                        script = row[3]
                        date = row[1]
                        transcripts[f'{year}'].append({'date': date, 'transcript': script})
                    elif curr_file != 0:
                        break
                    curr_file += 1
    elif dataset == 'cnn_ltm':
        for f in glob.glob('data/CNN_LTM/*.txt'):
            with open(f, 'r') as fl:
                script = fl.read()
                if len(script) >= 40:
                    year = f.split('/')[-1].split('-')[-1].split('.')[0]
                    date = f.split('/')[-1].split('.')[0]
                    dates = date.split('-')
                    date = f'{dates[2]}-{dates[0]}-{dates[1]}'
                    if year not in transcripts.keys():
                        transcripts[f'{year}'] = []
                    transcripts[f'{year}'].append({'date': date, 'transcript': script})
    elif dataset == 'cnn_lad':
        for f in glob.glob('data/CNN_LAD_2005/*.txt'):
            with open(f, 'r') as fl:
                script = fl.read()
                if len(script) >= 40:
                    year = f.split('/')[-1].split('-')[-1].split('.')[0]
                    date = f.split('/')[-1].split('.')[0]
                    dates = date.split('-')
                    date = f'{dates[2]}-{dates[0]}-{dates[1]}'
                    if year not in transcripts.keys():
                        transcripts[f'{year}'] = []
                    transcripts[f'{year}'].append({'date': date, 'transcript': script})
    
    return transcripts

def predict_transcripts(transcripts, year, csv_file_path, dataset, filter_cnn=False):
    pred_count = [0,0,0]
    total = 0

    id2label = {'0': 'left', '1': 'center', '2': 'right'}

    model.eval()

    with open(csv_file_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        for transcript_dict in tqdm(transcripts[f'{year}']):
            transcript = transcript_dict['transcript']
            date = None
            if 'date' in transcript_dict.keys():
                date = transcript_dict['date']
            if filter_cnn:
                transcript = transcript.replace('CNN', 'News Network')
            inputs = tokenizer(transcript, max_length=tokenizer.model_max_length, padding=True, truncation=True, return_tensors="pt").to('cuda')
            outputs = model(**inputs)
            logits = outputs[0]
            scores = logits.softmax(dim=-1)
            pred = scores.argmax()
            pred_count[pred.item()] += 1
            total += 1

            scores = scores.tolist()
            writer.writerow([year, date, transcript, id2label[f'{pred}'], scores[0][0], scores[0][1], scores[0][2]])

        print('='*20)
        print(f"Predictions for {year} ([left, center, right])")
        print("Total:", total, "|", pred_count)
        print('='*20)

        # if dataset == 'nyt':
        #     writer.writerow([year, date, total, pred_count[0], pred_count[1], pred_count[2]])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default='tucker')
    parser.add_argument('--filter_cnn', action='store_true', default=False)
    args = parser.parse_args()

    os.makedir('output', exist_ok=True)

    tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
    model = AutoModelForSequenceClassification.from_pretrained("bucketresearch/politicalBiasBERT").to('cuda')

    dataset = args.dataset

    transcripts = import_transcripts_by_year(dataset=dataset)
    csv_file_path = f'output/softmax_predictions_{dataset}.csv'

    if args.filter_cnn:
        csv_file_path = f'output/softmax_predictions_{dataset}_filtered.csv'

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # if dataset == 'nyt':
        #     writer.writerow(['Year', 'Total', 'Left', 'Center', 'Right'])
        # else:
        writer.writerow(['Year', 'Date', 'Text', 'Prediction', 'Score (Left)', 'Score (Center)', 'Score (Right)'])

    for year in range(min([int(year) for year in transcripts.keys()]),max([int(year) for year in transcripts.keys()])+1):
        predict_transcripts(transcripts, year=year, csv_file_path=csv_file_path, dataset=dataset, filter_cnn=args.filter_cnn)
