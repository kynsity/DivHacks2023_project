from flask import Flask, render_template, request, jsonify
import openai
import os
from PyPDF2 import PdfReader

app = Flask(__name__)

# Set your OpenAI API key
api_key = "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"

# Initialize the OpenAI API client
openai.api_key = api_key

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.form.get('user_question')
    
    # Define the input prompt for the chat conversation
    input_prompt = f"What's your question? '{user_question}'"
    ## read pdf
    # Directory containing your PDF files
    pdf_directory = './data/'

    # Get a list of all PDF files in the directory
    pdf_files = [file for file in os.listdir(pdf_directory) if file.endswith('.pdf')]

    context_text = ""
    # Loop through each PDF file and extract text
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_directory, pdf_file)
        
        # Creating a PDF reader object for the current PDF file
        reader = PdfReader(pdf_path)
        
        # Printing the number of pages in the PDF file
        print(f"Number of pages in '{pdf_file}': {len(reader.pages)}")
        
    # Loop through each page and extract text
    for page_num, page in enumerate(reader.pages, 1):
        text = page.extract_text()
        context_text+= text
        #print(f"Text from page {page_num} of '{pdf_file}':")
        #print(text)

    # Create a chat completion request
    # response = openai.ChatCompletion.create(
    #     model="gpt-4",  # Specify the model you want to use
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant that translates English to French."},
    #         {"role": "user", "content": input_prompt}
    #     ]
    # )
    system_msg = """
    You are a smart chatbot that is a CS advisor for Columbia students. You have access to the following information as context. Do not use external information and do not make up answers. Answer the  question to the best of your ability.
    """ 
    context = context_text
    #user_input = "what classes should I take as if I want to do the Vision and Graphics track?"
    prompt = f"""
    #### SYSTEM MESSAGE ####
    {system_msg}
    #### SYSTEM MESSAGE DONE ####
    #### CONTEXT PROMPT ####
    {context}
    ####USER PROMPT END###
    #### USER PROMPT ####
    {user_question}
    ####USER PROMPT END###
    """

    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=1, #degree of randomness/creativity (1 being least random)
    max_tokens=300, #to limit response length
    top_p=0.5, #another parameter for randomness (1 being least random)
    #frequency_penalty=0.26,
    #presence_penalty=0.08
    )

    # Get the generated response
    output = response['choices'][0]['message']['content']

    return jsonify({'response': output})

if __name__ == '__main__':
    app.run(debug=True)