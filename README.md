# DivHacks2023_project
### Columbia Advising Chatbot
### Created by: Kylie Berg, Charles Liu, Anna Reis, and Eris Gao
An AI powered chatbot to help Columbia CS students get their advising questions answered quick!

[link to demo video](https://youtu.be/wMQmq_cwxLE?si=-kDxpVf-M2GuODNI)

[link to slides presentation](https://www.canva.com/design/DAFvT-iM7p4/boT1OEoTPTcmALlNhhcgng/edit?utm_content=DAFvT-iM7p4&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

[link to devpost page](https://devpost.com/software/columbia-advising-chatbot)

NOTE: To use app you need to have access to an OpenAI API key and an Active Loop Deep Lake API key.

To run, navigate to backend folder, type "flask run" in terminal and website should be accessible on localhost!


## elevator pitch

CS classes are hard. CS advising shouldn’t be. Get answer to all your Columbia computer science questions from CiCi!

## inspiration

One of the hardest parts of being a CS major at Columbia is not the classes: it’s advising. The current system is overwhelming and unsustainable for CS advisors and students alike, and this reality motivated us to build CiCi.

## what it does

CiCi is an AI chatbot trained on Columbia CS advising data. It uses this history along with its broader chatbot capability to answer any questions you have about the CS major, coursework, or career options at Columbia.

## how we built it

Backend: We created embeddings using Columbia CS Advising documents and stored them in a vector database. We then used the OpenAI API to make a chatbot that would answer CS advising questions by searching through the vector database for the most relevant text and compiling them into a single concise answer.

Frontend: HTML/CSS/JavaScript
