import os
import openai
import re

MAX_INPUT_LENGTH = 350
STOPWORDS = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as",
             "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]


def main():
    prompt = "I want to build a big data app. It will survey users from our website and store their data. It will transform and organize our data. It will store the transformed data. It will query the datasets. It will use a data lake. It will analyze data using machine learning. It will produce charts."
    clean_prompt = clean_text(prompt)

    if validate_length(clean_prompt):
        generate_aws_services(clean_prompt)
    else:
        raise ValueError(
            f"Input must be less than {MAX_INPUT_LENGTH} characters.")


def clean_text(prompt: str) -> str:
    prompt = prompt.lower()
    stop = set(STOPWORDS + ["i", "it", "need", "needs",
               "want", "wants", "build", "will", "should"])
    prompt_without_stopwords = " ".join(
        [word for word in prompt.split() if word not in (stop)])
    prompt_list = re.split(r"[,.]", prompt_without_stopwords)
    prompt_clean_list = [phrase.strip()
                         for phrase in prompt_list if phrase.strip() != ""]

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

    return response.choices[0].text.strip()


if __name__ == "__main__":
    main()
