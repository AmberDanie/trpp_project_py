import torch
from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizerFast
from typing import Dict

TOKENIZER_MODEL = 'blanchefort/rubert-base-cased-sentiment-rusentiment'
SENTIMENT_MODEL = 'blanchefort/rubert-base-cased-sentiment-rusentiment'

class OutputSentimentModel:
    NEUTRAL: float
    POSITIVE: float
    NEGATIVE: float

class SentimentModel:
    """class SentimentModel

    :Arguments:
        tokenizer(transformers.models.bert.tokenization_bert_fast.BertTokenizerFast): model that create tokens
        model(transformers.models.bert.modeling_bert.BertForSequenceClassification): model that return sentiment score

    """
    def __init__(self):
        self.tokenizer = BertTokenizerFast.from_pretrained(TOKENIZER_MODEL)
        self.model = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL, return_dict=True)

    @torch.no_grad()
    def predict(self, text: str) -> OutputSentimentModel:
        """Class methods that return dict with sentiment score

        Arguments:
            text(str) : the input text that to be calculated for sentiment score

        Returns:
            sentiment_dict(OutputSentimentModel): the sentiment score, the dict that contains three keys ('NEUTRAL', 'POSITIVE', 'NEGATIVE')

        """
        inputs = self.tokenizer(text, max_length=512, padding=True, truncation=True, return_tensors='pt')
        outputs = self.model(**inputs)
        predicted = torch.nn.functional.softmax(outputs.logits, dim=1)
        sentiment_dict = {'NEUTRAL': predicted[0][0].item(),
                          'POSITIVE': predicted[0][1].item(),
                          'NEGATIVE': predicted[0][2].item()}
        return sentiment_dict


