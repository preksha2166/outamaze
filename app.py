from flask import Flask, render_template, request, jsonify, url_for
import re
import random
import long_responses as long
from flask import Flask, render_template, request
#import flask_excel as excel
from flask import Flask, render_template, request, jsonify, url_for

app = Flask(__name__)
#excel.init_excel(app)

app = Flask(__name__, template_folder='templates', static_folder='static')  # Use '.' for the current directory

# Rest of the code remains the same

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Sorry, I can\'t help you with that', ['find', 'me', 'something'], required_words=['something'])
    response('Hello there! How can I assist you today?', ['hi', 'hey', 'hello'], single_response=True)
    response('I\'m an AI assistant created by OutAamze. It\'s nice to meet you!', ['who', 'are', 'you'], single_response=True)
    response('I\'m doing well, thank you for asking!', ['how', 'are', 'you'], required_words=['how'])
    response('Have a great day!', ['bye', 'goodbye', 'see', 'you'], single_response=True)
    response("I'm afraid I don't have enough information to find something for you. Could you please provide more details?", ['find', 'something'], required_words=['something'])
    response("I'm an AI assistant, so I don't have personal experiences to share. However, I'd be happy to provide information or assistance with tasks if you have any specific questions.", ['tell', 'me', 'about', 'yourself'], single_response=True)
    response("Unfortunately, I don't have the capability to set reminders or alarms. However, I can provide information on various topics or assist with other tasks if you'd like.", ['set', 'reminder', 'alarm'], single_response=True)
    response("I don't actually have feelings or emotions since I'm an AI. I'm designed to have natural conversations and provide helpful information to users.", ['are', 'you', 'happy', 'sad', 'angry'], single_response=True)
    response("As an AI, I don't have personal preferences or opinions on topics like politics or religion. However, I can provide factual information from reliable sources if you're interested in learning more about those subjects.", ['what', 'is', 'your', 'opinion', 'on'], required_words=['opinion'])
    

    # Add responses related to Outamaze
    response('Outamaze is your ultimate travel companion!', ['what', 'is', 'outamaze'], required_words=['outamaze'])
    response('Discover new destinations with Outamaze! <a href="{0}">Click here</a>'.format(url_for('search')), ['find', 'some', 'trending', 'places'], required_words=['trending'])
    response('I am an AI assistant created by Outamaze to help you plan your travels and find interesting destinations.', ['what', 'do', 'you', 'do'], single_response=True)
    response('Unfortunately, I do not have the capability to book or purchase travel services directly. However, I can provide information and suggestions to help you plan your trip.', ['can', 'you', 'book', 'tickets', 'hotels'], single_response=True)
    response('I do not have personal experiences to share since I am an AI, but I can provide you with information about popular tourist attractions, activities, and cultural experiences in different destinations.', ['have', 'you', 'been', 'to'], required_words=['been', 'to'])
    response('I do not have specific recommendations for restaurants or accommodations, but I can suggest looking at review websites or travel guides for highly rated options in your desired location...You can start with our site', ['recommend', 'good', 'restaurant', 'hotel'], required_words=['recommend', 'restaurant', 'hotel'])
    response('Here are some tips for safe and responsible travel: research your destination, get travel insurance, keep copies of important documents, and respect local customs and laws.', ['travel', 'tips', 'advice'], required_words=['tips', 'advice'])
    response('I do not have personal travel preferences, but I can provide information on destinations suitable for different budgets, interests, and travel styles.', ['where', 'would', 'you', 'recommend'], required_words=['recommend'])
    response('Here are some top places in Mumbai <a href="{0}">Click here</a>'.format(url_for('destinations_template')), ['top', 'places', 'in', 'mumbai'], required_words=['places', 'in', 'mumbai'])
    response('Here are some top places in Pune <a href="{0}">Click here</a>'.format(url_for('puneage3happ')), ['top', 'places', 'in', 'pune'], required_words=['places', 'in', 'pune'])
    response('Here are some top places in Hyderabad <a href="{0}">Click here</a>'.format(url_for('hydaage2happ')), ['top', 'places', 'in', 'hyderabad'], required_words=['places', 'in', 'hyderabad'])



    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return unknown() if highest_prob_list[best_match] < 1 else best_match

def unknown():
    response = ["Could you please re-phrase that? ",
                "...",
                "Sounds about right.",
                "What does that mean?"][
        random.randrange(4)]
    return response

def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    return check_all_messages(split_message)

# Route for rendering the HTML frontend interface
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('bot.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/marine')
def marine():
    return render_template('marine.html')

@app.route('/iskon')
def iskon():
    return render_template('iskontemple.html')

@app.route('/hg')
def hg():
    return render_template('hg.html')

@app.route('/gorai')
def gorai():
    return render_template('gorai.html')

@app.route('/sd')
def sd():
    return render_template('siddhivinayak.html')

@app.route('/pg')
def pg():
    return render_template('pagoga.html')

@app.route('/search')
def search():
    return render_template('searchpage.html')

#route for redirecting 
@app.route('/destinations_template.html')
def destinations_template():
    trending_places_url = url_for('index')
    return render_template('destinations_template.html', trending_places_url=trending_places_url)

@app.route('/hydaage1happ')
def hydaage1happ():
    return render_template('hydaage1happ.html')

@app.route('/outghappage2')
def outghappage2():
   return render_template('outghappage2.html')
    
@app.route('/outghappage3')
def outghappage3():
   return render_template('outghappage3.html')
        
@app.route('/outgsadage1')
def outgsadage1():
   return render_template('outgsadage1.html')
    
@app.route('/outgsadage2')
def outgsadage2():
   return render_template('outgsadage2.html')
    
@app.route('/outgsadage3')
def outgsadage3():
   return render_template('outgsadage3.html')
    
@app.route('/puneage1happ')
def puneage1happ():
   return render_template('puneage1happ.html')
    
@app.route('/puneage2happ')
def puneage2happ():
   return render_template('puneage2happ.html')
    
@app.route('/puneage3happ')
def puneage3happ():
   return render_template('puneage3happ.html')
    
@app.route('/puneage1sad')
def puneage1sad():
   return render_template('puneage1sad.html')
    
@app.route('/puneage2sad')
def puneage2sad():
   return render_template('puneage2sad.html')
    
@app.route('/puneage3sad')
def puneage3sad():
   return render_template('puneage3sad.html')
    
@app.route('/hydaage2happ')
def hydaage2happ():
    return render_template('hydaage2happ.html')

@app.route('/hydaage3happ')
def hydaage3happ():
    return render_template('hydaage3happ.html')

@app.route('/hydaage1sad')
def hydaage1sad():
    return render_template('hydaage1sad.html')

@app.route('/hydaage2sad')
def hydaage2sad():
    return render_template('hydaage2sad.html')

@app.route('/hydaage3sad')
def hydaage3sad():
    return render_template('hydaage3sad.html')

    
# Define routes for all the other URLs used in the combinations dictionary

@app.route('/search_results', methods=['POST'])
def search_results():
    city = request.form['city']
    mood = request.form['mood']
    age_category = request.form['age_category']

    # Create a dictionary or list of dictionaries containing the destination data
    # for the specific combination of city, mood, and age_category
    destination_data = get_destination_data(city, mood, age_category)

    # Render the template with the destination data
    return render_template('destinations_template.html', destinations=destination_data)

def get_destination_data(city, mood, age_category):
    # Logic to retrieve the destination data based on the combination of
    # city, mood, and age_category
    # You can use a database, files, or any other data source
    # Return a list of dictionaries containing the destination data
    # Example:
    if city == '1' and mood == 'A' and age_category == 'X':
        return [
            {
                'image': url_for('static', filename='images/gallery222.jpg'),
                'title': 'Destination 1',
                'description': 'Description for Destination 1',
                'link': 'https://example.com/destination1'
            },
            {
                'image': 'https://example.com/image2.jpg',
                'title': 'Destination 2',
                'description': 'Description for Destination 2',
                'link': 'https://example.com/destination2'
            }
        ]
    elif city == '1' and mood == 'A' and age_category == 'Y':
        # Return a different set of destination data
        pass
    # Add more conditions for other combinations of city, mood, and age_category
# Route for processing incoming messages from the frontend
@app.route('/message', methods=['POST'])
def process_message():
    user_input = request.json['message']
    response = get_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)