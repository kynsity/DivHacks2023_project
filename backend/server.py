from flask import Flask, render_template, request, jsonify
import openai
import os
from PyPDF2 import PdfReader

app = Flask(__name__)

# Set your OpenAI API key
api_key = "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"

# Initialize the OpenAI API client
openai.api_key = api_key
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake

os.environ["OPENAI_API_KEY"] = "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"
activeloop_token = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY5NTQ5NDY5MiwiZXhwIjoxNzI3MTE3MDg2fQ.eyJpZCI6InlnYW8ifQ.TRSWixYV991CCw2VqZ8QJN3yUmBsxQTyXmHZ661v7GM6rKGfLDyj1vW-wN0D5E79pSK1B7Ht-Ibdqg07iLugWw'
os.environ["ACTIVELOOP_TOKEN"] = activeloop_token

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.form.get('user_question')
    # Define the input prompt for the chat conversation
    input_prompt = f"What's your question? '{user_question}'"
    
    #connect to deeplake to check embeddings
    embeddings = OpenAIEmbeddings(disallowed_special=())
    username = "ygao"  # replace with your username from app.activeloop.ai
    db = DeepLake(
    dataset_path=f"hub://{username}/divhacks23-2000",
    read_only=True,
    embedding_function=embeddings,)

    retriever = db.as_retriever()
    retriever.search_kwargs["distance_metric"] = "cos"
    retriever.search_kwargs["fetch_k"] = 10
    retriever.search_kwargs["maximal_marginal_relevance"] = True
    retriever.search_kwargs["k"] = 5 #top 10 similar chunks

    from langchain.chat_models import ChatOpenAI
    from langchain.chains import ConversationalRetrievalChain

    model = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0.1)  # switch to 'gpt-4'
    qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever, return_source_documents=False) 
    question = f"""You are a smart chatbot that is a CS advisor for Columbia students. You have access to the following 
    information as context. Do not use external information and do not make up answers. Answer the question to the best of your ability and try to be as specific as possible. 
    Feel free to include relevant links.
    If you don't know the answer, just say "Hmm, I'm not sure." Your answer should be at 
    least 100 words and no more than 300 words. This is the question you should answer: {input_prompt} \n
    """
    chat_history = []
    result = qa({"question": question, "chat_history": chat_history})
    response = result['answer']

    # Get the generated response
    output = response

    return jsonify({'response': output})

if __name__ == '__main__':
    app.run(debug=True)