import os
import openai
import gradio as gr

#
#we will now define the openai API key
#if you have OPEN AI API key as an environment variable, enable the below
#openai.api._key = os.getenv("OPENAI_API_KEY")

#if you have OpenAI API key as a string, enable the below


#now we will have a start sequence and restart sequence which says AI, Human

#then we have a prompt that we copied from the openai's example on their code with it's settings and preferences configurated

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: "

def openai_create(prompt):

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.9,
    max_tokens=3000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
)
#now we will take the response and return text
    return response.choices[0].text

#now we create a new function called py_talkbot, it has 2 arguments 'input, history', this is required for gradio
#for a gradio application to work, anything that we need to do in gradio has to be wrapped inside a function
#that  function should have an input and an output, one or more inputs, or one or more outputs
#in this case, we have an inut which is a text,
# the 2nd is something called history, which stores the state of the current gradio application
#with the history, we aer able to build the context and keep the knowledge of the context of the memory,
#of what is happening in the past as well. If history does not exist then it is a empty list
#then we're going to take history converted it to a list and then appened our current input,
#which is basically what we are going to send, a current message along with the history
#each message we input gets appended to the entire conversation's history's context
#the entire context of the conversation goes to openai as a prompt, then we append the input to that,
#and then that input goes inside, (like whatever we created, the entire thing, the history plus input goes inside 'openai_create' )
#which is the function that we created as the input, so that goes as a prompt and based on that openai generates a response,
# #and that response then gets added as output. So; history gets added, one input, one output, then we return 'history, history'
# and that gets displayed in the response of the bot. How does it gets displayed you may ask?
#we're going to use blocks which is an advanced method to create gradio applications. There aer 2 ways, 
#one is interface, one is block. The reason why we are using block is for us to get a very chat GPT style interface,
#like top to bottom, which is easy to do in blocks, and interface would have a 2 column view that's why i used blocks 


def py_talkbot(input, history):
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    inp = ' '.join(s)
    output = openai_create(inp)
    history.append((input, output))
    return history, history

# in block, first we have the title, first thing we have to define is gr.Blocks(as you can see in the beginning we import gr as gradio)
# firstly we need a chatbot, we need an input textbox where we can type input, we kept the placeholder text as the prompt we defined earlier
# then we need to store the state, then we need a button where we can click send
#then we say, whenever the submit button is clicke, i am going to call the function being passed with the input and output being passed  
#the input contains the actual input message which is the message from the textbox and also the current state
#and the output contains the output back from the chatbot clone function, and also the state,
# that's why we are returning a double here 
# then we click block.launch and then this is going to launch our application
#once it launches, it'll let you open the terminal 
#input the command 'python3 app.py', making sure to be inside the current working project directory
block = gr.Blocks()

with block:
    gr.Markdown("""<h1><center>pyTalkbot by sevtekkycodes</center></h1>""")
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder=prompt)
    state = gr.State()
    submit = gr.Button("SEND")
    submit.click(py_talkbot, inputs=[message, state], outputs=[chatbot, state])

    block.launch(debug = True)
