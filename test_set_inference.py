from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from datasets import load_dataset

tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
model = AutoModelForSequenceClassification.from_pretrained("bucketresearch/politicalBiasBERT").to('cuda')

dataset = load_dataset("cjziems/Article-Bias-Prediction")
test_set = dataset["train"]

def to_tokens(example):
  tokenized = tokenizer(example['content'], max_length=tokenizer.model_max_length, padding=True, truncation=True, return_tensors="pt")
  return tokenized

test_set = test_set.map(to_tokens, batched=True)
print(test_set)

from tqdm import tqdm

correct = 0
total = 0

for example in tqdm(test_set):
  inputs = {
      'input_ids': torch.tensor(example['input_ids']).reshape((1,-1)).to('cuda'),
      'token_type_ids': torch.tensor(example['token_type_ids']).reshape((1,-1)).to('cuda'),
      'attention_mask': torch.tensor(example['attention_mask']).reshape((1,-1)).to('cuda')
  }
  labels = torch.tensor(example['bias']).to('cuda')
  outputs = model(**inputs, labels=labels)
  loss, logits = outputs[:2]

  pred = logits.softmax(dim=-1)[0].argmax()
  if pred.item() == labels.item():
    correct += 1
  total += 1

print(correct, total)