import os
import openai
import nltk.corpus
nltk.download("stopwords")
from nltk.corpus import stopwords

MAX_INPUT_LENGTH = 250

def main():
    prompt = "I want to build a big data app. It will survey users from our website and store their data. It will transform and organize our data. It will store the transformed data. It will query the datasets. It will use a data lake. It will analyze data using machine learning. It will produce charts."
    clean_prompt = "App keywords: " + clean_text(prompt)

    if validate_length(clean_prompt):
        generate_aws_services(clean_prompt)
    else:
        raise ValueError(
            f"Input must be less than {MAX_INPUT_LENGTH} characters.")

def clean_text(prompt: str) -> str:
    stop = set(stopwords.words('english') + ["I", "It", "need", "needs", "want", "wants", "build","will", "should"])
    prompt_without_stopwords = " ".join([word for word in prompt.split() if word not in (stop)])
    prompt_list = prompt_without_stopwords.split(".")
    prompt_clean_list = [phrase.strip() for phrase in prompt_list if phrase.strip() != ""]

    return ", ".join(prompt_clean_list)

def validate_length(prompt: str):
    return len(prompt) <= MAX_INPUT_LENGTH

def generate_aws_services(prompt: str) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(
    model="text-davinci-002",
    prompt=f"App keywords: e-commerce app, highly available, store survey results, use survey results to find the best fit from database, store purchase transactions, chatbot to guide users\nAWS services: S3, CloudFront, Amplify, AppSync, Aurora, DynamoDB, Lambda, ElasticSearch, Lex, Connect\n\nApp keywords: mobile app that utilizes data from wearable device, stream real-time data, analyze data in real time, store streaming data, send push notifications, store and analyze device data, embed dashboards\nAWS services: Kinesis Data Streams, Kinesis Data Firehose, Kinesis Data Analytics, S3, Lambda, SNS, Timestream, QuickSight\n\nApp keywords: mobile application to pitch startup ideas, authentication, analytics, store pitch videos, fast loading, store data in sync, store data, serverless, email customers\nAWS services: Cognito, Amplify, Lambda, S3, CloudFront, DynamoDB, SES\n\nApp keywords: app to predict outcome of sports games, serverless, monitor model's performance, accessible via rest api, store games scores\nAWS services: SageMaker, Lambda, API Gateway, DynamoDB\n\nApp keywords: ai voice assistant app, store medical records and insurance documents, extract data from documents, store data from documents, agents talk to customers, chatbot, store chatbot history, store user information, analyze chatbot conversations, analyze calls\nAWS services: Comprehend, Connect, Lex, Aurora, DynamoDB, Transcribe, CloudWatch\n\nApp keywords: {prompt}\nAWS services:",
    temperature=0.3,
    max_tokens=64,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    return response.choices[0].text

if __name__ == "__main__":
    main()