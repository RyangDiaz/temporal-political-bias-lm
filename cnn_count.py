from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from tqdm import tqdm
import glob
import csv
import argparse
import sys

from transcripts_inference import import_transcripts_by_year

csv.field_size_limit(sys.maxsize)

def count_cnn(transcripts, year, csv_file_path):
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        for transcript_dict in tqdm(transcripts[f'{year}']):
            transcript = transcript_dict['transcript']
            date = transcript_dict['date']
            count = transcript.count('CNN')
            writer.writerow([date, count])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default='tucker')
    args = parser.parse_args()

    dataset = args.dataset

    transcripts = import_transcripts_by_year(dataset=dataset)
    csv_file_path = f'output/cnn_count_{dataset}.csv'

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # if dataset == 'nyt':
        #     writer.writerow(['Year', 'Total', 'Left', 'Center', 'Right'])
        # else:
        writer.writerow(['Date', 'CNN_Count'])

    for year in range(min([int(year) for year in transcripts.keys()]),max([int(year) for year in transcripts.keys()])+1):
        count_cnn(transcripts, year=year, csv_file_path=csv_file_path)
