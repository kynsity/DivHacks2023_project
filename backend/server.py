from flask import Flask, render_template, request, jsonify
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
import os
import openai
import time
import secrets_2


app = Flask(__name__)
# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = secrets_2.SECRET_KEY

# Initialize the OpenAI API client
openai.api_key = os.environ["OPENAI_API_KEY"]

activeloop_token = secrets_2.TOKEN
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
def landing():
    return render_template('landing.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    print(f"API Entered: {time.time()}")
    user_question = request.form.get('user_question')
    input_prompt = f"What's your question? '{user_question}'"

    question = f"""You are a smart chatbot named CiCi that is a CS advisor for Columbia students. You have access to the following 
    information as context. Do not use external information and do not make up answers. Answer the question to the best of your ability and try to be as specific as possible. 
    If you don't know the answer, just say that you do not know. Keep your answers short and concise. Your answer should be at 
    least 100 words and no more than 200 words. Split your answer into paragraphs where it makes grammatical sense and using two \n to split the paragraphs.
    Try to include course numbers if you can.
    Feel free to include relevant links.
    You can add these links if you feel that they are relevant.
    If the question is related to CS advising, you can return this link as part of your answer: "https://www.cs.columbia.edu/academic-advising/"
    If the question is related to CS careers, you can return this link as part of your answer: "https://www.cs.columbia.edu/career/student-resources/"
    If the question is related to CS faculty, you can return this link as part of your answer: "https://www.cs.columbia.edu/people/faculty/"
    If the question is related to CS student organizations, you can return this link as part of your answer: "https://www.cs.columbia.edu/student-organizations/"
    If the question is related to prospective CS students FAQ, you can return this link as part of your answer: "https://www.cs.columbia.edu/education/undergraduate/prospectivefaq/"
    Return your answer in markdown format.
    This is the question you should answer: {input_prompt} \n 

    If you don't know the answer, don't make anything up otherwise you'll be fired. Your answer should be at 
    least 100 words and no more than 300 words. This is the question you should answer: {input_prompt} \n
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