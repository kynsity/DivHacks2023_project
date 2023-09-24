from flask import Flask, render_template, request, jsonify
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
import os
import openai
import time


app = Flask(__name__)
# Set your OpenAI API key
# api_key = "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"
# openai.api_key = api_key
os.environ["OPENAI_API_KEY"] = "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"

# Initialize the OpenAI API client
openai.api_key = os.environ["OPENAI_API_KEY"]

#os.environ["OPENAI_API_KEY"] = "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"
activeloop_token = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY5NTQ5NDY5MiwiZXhwIjoxNzI3MTE3MDg2fQ.eyJpZCI6InlnYW8ifQ.TRSWixYV991CCw2VqZ8QJN3yUmBsxQTyXmHZ661v7GM6rKGfLDyj1vW-wN0D5E79pSK1B7Ht-Ibdqg07iLugWw'
os.environ["ACTIVELOOP_TOKEN"] = activeloop_token

# Initialize objects once when the app starts
embeddings = OpenAIEmbeddings(disallowed_special=())
username = "ygao"  # replace with your username from app.activeloop.ai
db = DeepLake(
    dataset_path=f"hub://{username}/divhacks23-2000",
    read_only=True,
    embedding_function=embeddings,
)

retriever = db.as_retriever()
retriever.search_kwargs["distance_metric"] = "cos"
retriever.search_kwargs["fetch_k"] = 10
retriever.search_kwargs["maximal_marginal_relevance"] = True
retriever.search_kwargs["k"] = 5  # top 10 similar chunks

model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    print(f"API Entered: {time.time()}")
    user_question = request.form.get('user_question')
    input_prompt = f"What's your question? '{user_question}'"

    question = f"""You are a smart chatbot that is a CS advisor for Columbia students. You have access to the following 
    information as context. Do not use external information and do not make up answers. Answer the question to the best of your ability and try to be as specific as possible. 
    Feel free to include relevant links.
    If you don't know the answer, just say "Hmm, I'm not sure." Your answer should be at 
    least 100 words and no more than 300 words. This is the question you should answer: {input_prompt} \n
    If you don't know the answer, just say that you do not know. Your answer should be at 
    least 100 words and no more than 300 words. 
    You can add these links if you feel that they are relevant.
    If the question is related to CS advising, you can return this link as part of your answer: "https://www.cs.columbia.edu/academic-advising/"
    If the question is related to CS careers, you can return this link as part of your answer: "https://www.cs.columbia.edu/career/student-resources/"
    If the question is related to CS faculty, you can return this link as part of your answer: "https://www.cs.columbia.edu/people/faculty/"
    If the question is related to CS student organizations, you can return this link as part of your answer: "https://www.cs.columbia.edu/student-organizations/"
    If the question is related to prospective CS students FAQ, you can return this link as part of your answer: "https://www.cs.columbia.edu/education/undergraduate/prospectivefaq/"
    Return your answer in markdown format.
    This is the question you should answer: {input_prompt} \n 
>>>>>>>>> Temporary merge branch 2
    """

    chat_history = []
    s_time = time.time()
    print(f"Hitting OpenAI: {time.time()}")
    qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever, return_source_documents=False)
    print(f"Response from openAI: {time.time()}")
    e_time = time.time()
    print(f"Time taken: {e_time - s_time}")
    print(f"Sending result: {time.time()}")

    result = qa({"question": question, "chat_history": chat_history})
    response = result['answer']
    print(f"Final answer: {time.time()}")
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)