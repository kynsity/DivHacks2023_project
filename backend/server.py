from flask import Flask, render_template, request, jsonify
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
import os
import openai
import time
import secrets_1


app = Flask(__name__)
# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = secrets_1.SECRET_KEY

# Initialize the OpenAI API client
openai.api_key = os.environ["OPENAI_API_KEY"]

#os.environ["OPENAI_API_KEY"] = "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"
activeloop_token = secrets_1.TOKEN
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

# from flask import Flask, render_template, request, jsonify
# import openai
# import os
# from PyPDF2 import PdfReader

# app = Flask(__name__)

# # Set your OpenAI API key
# api_key = "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"

# # Initialize the OpenAI API client
# openai.api_key = api_key

# @app.route('/')
# def landing():
#     return render_template('landing.html')

# @app.route('/chat')
# def chat():
#     return render_template('chat.html')

# @app.route('/ask', methods=['POST'])
# def ask():
#     user_question = request.form.get('user_question')
    
#     # Define the input prompt for the chat conversation
#     input_prompt = f"What's your question? '{user_question}'"

#     print(user_question)
#     ## read pdf
#     # Directory containing your PDF files
#     pdf_directory = './data/'

#     # Get a list of all PDF files in the directory
#     pdf_files = [file for file in os.listdir(pdf_directory) if file.endswith('.pdf')]

#     context_text = ""
#     # Loop through each PDF file and extract text
#     for pdf_file in pdf_files:
#         pdf_path = os.path.join(pdf_directory, pdf_file)
        
#         # Creating a PDF reader object for the current PDF file
#         reader = PdfReader(pdf_path)
        
#         # Printing the number of pages in the PDF file
#         print(f"Number of pages in '{pdf_file}': {len(reader.pages)}")
        
#     # Loop through each page and extract text
#     for page_num, page in enumerate(reader.pages, 1):
#         text = page.extract_text()
#         context_text+= text
#         #print(f"Text from page {page_num} of '{pdf_file}':")
#         #print(text)

#     # Create a chat completion request
#     # response = openai.ChatCompletion.create(
#     #     model="gpt-4",  # Specify the model you want to use
#     #     messages=[
#     #         {"role": "system", "content": "You are a helpful assistant that translates English to French."},
#     #         {"role": "user", "content": input_prompt}
#     #     ]
#     # )
#     system_msg = """
#     You are a smart chatbot that is a CS advisor for Columbia students. You have access to the following information as context. Do not use external information and do not make up answers. Answer the  question to the best of your ability.
#     """ 
#     context = context_text
#     #user_input = "what classes should I take as if I want to do the Vision and Graphics track?"
#     prompt = f"""
#     #### SYSTEM MESSAGE ####
#     {system_msg}
#     #### SYSTEM MESSAGE DONE ####
#     #### CONTEXT PROMPT ####
#     {context}
#     ####USER PROMPT END###
#     #### USER PROMPT ####
#     {user_question}
#     ####USER PROMPT END###
#     """

#     response = openai.ChatCompletion.create(
#     model="gpt-4",
#     messages=[{"role": "user", "content": prompt}],
#     temperature=1, #degree of randomness/creativity (1 being least random)
#     max_tokens=300, #to limit response length
#     top_p=0.5, #another parameter for randomness (1 being least random)
#     #frequency_penalty=0.26,
#     #presence_penalty=0.08
#     )

#     # Get the generated response
#     output = response['choices'][0]['message']['content']

#     return jsonify({'response': output})

# if __name__ == '__main__':
#     app.run(debug=True)