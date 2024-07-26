import streamlit as st
import google.generativeai as genai
import os

# Set your actual API key here
api_key = 'AIzaSyDvcSjpnS1w486Y9B6qoa-x13nOmRMn_kk'
os.environ['GOOGLE_API_KEY'] = api_key

# Retrieve the API key from the environment variable
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    st.error("No API key found. Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

# Initialize the GenerativeModel with the API key
genai.api_key = api_key

# Initialize the context
context = []

# Define the prompt function with user input
def prompt(user_input):
    return f"""
    You are OrderBot, an automated service to collect orders for a pizza restaurant.
    You first greet the customer, then collect the order,
    and then ask if it's a pickup or delivery.
    You wait to collect the entire order, then summarize it and check
    if the customer wants to add anything else.
    If it's a delivery, you ask for an address.
    Finally, you collect the payment.
    Make sure to clarify all options, extras, and sizes to uniquely
    identify the item from the menu.
    The menu includes
    pepperoni pizza 12.95, 10.00, 7.00
    cheese pizza 10.95, 9.25, 6.50
    eggplant pizza 11.95, 9.75, 6.75
    fries 4.50, 3.50
    greek salad 7.25
    Toppings:
      extra cheese 2.00,
      mushrooms 1.50
      sausage 3.00
      canadian bacon 3.50
      AI sauce 1.50
      peppers 1.00
    Drinks:
      coke 3.00, 2.00, 1.00
      sprite 3.00, 2.00, 1.00
      bottled water 5.00
    question: {user_input}
    """

# Function to get a response from the model
def get_response(user_input):
    try:
        text = prompt(user_input)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(text)

        # Extract response text
        assistant_message = response['choices'][0]['message']['content']
        
    except Exception as e:
        assistant_message = f"Sorry, I couldn't process your request. Error: {e}"

    # Append user and assistant messages to context
    context.append({'role': 'user', 'content': user_input})
    context.append({'role': 'assistant', 'content': assistant_message})

    return assistant_message

# Streamlit app layout
st.title("Pizza Bot")
st.write("Welcome to the Pizza Bot! Ask me anything about pizzas.")

# User input
user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input:
        response = get_response(user_input)
        st.write("Bot:", response)
    else:
        st.write("Please enter a message.")

# Display conversation history
conversation_history = "\n\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in context])
st.markdown(conversation_history)
