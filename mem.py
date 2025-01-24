from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage
from dotenv import load_dotenv
from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory
load_dotenv()   
project_id='qrproject-e7f3e'
session_id='session_1'
collection_name='llm_history'
print('initilizing firebase')
client=firestore.Client(project=project_id)

# initilizing firestore chat msg history
print('initilizing firestore chat msg history')
chat_history=FirestoreChatMessageHistory(
    session_id=session_id,
    collection=collection_name,
    client=client
)

print('chat history initilized')
print(chat_history.messages)

llm=ChatGroq()

chat_history.add_message(SystemMessage(content='you are an ai assistent'))
while True:
    query=input("You :")
    if query.lower() == 'exit':
        break
    else:
        chat_history.add_user_message(query)
        resp=llm.invoke(chat_history.messages)
        print(resp.content)
        chat_history.add_ai_message(resp.content)

