

from flask import Flask, jsonify, request, redirect, url_for, session
from flask.helpers import flash
from flask.templating import render_template
from flask_pymongo import PyMongo
from random import randint
import random
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from pymongo.message import MAX_INT32
import requests
import bcrypt

app = Flask(__name__)
app.config["MONGO_URI"] = 'mongodb+srv://james:07121999@collegecluster.rssdv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
mongo = PyMongo(app)

#collection variables to call collection in methods
db_operations = mongo.db.users
db_recipe_operations = mongo.db.recipes
db_breakfast = mongo.db.breakfast

#All the routings in app will be mentioned here.
@app.route('/index')
def index():
    if session['Name'] != None:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/calories')
def calories():
        return render_template('calories.html')

@app.route('/update')
def update():
    if session['Name'] != None:
        return render_template('update.html')
    else:
        return render_template('login.html')

@app.route('/recipes')
def recipes():
    if session['Name'] != None:
        recipesFunc()
        return render_template('recipes.html')
    else:
        return render_template('login.html')

@app.route('/create-recipe')
def addRecipes():
    return render_template('addRecipes.html')

#logout feature
@app.route('/logout', methods =['POST'])
def logout():
    if request.method == 'POST':
            session['Name'] = None
            session['Calories'] = None
            session['Age'] = None
            session['Password'] = None
            return redirect(url_for('login'))

#login in function for user
userLoggedIn = False
@app.route('/login', methods =['POST'])
def loginFunc():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'Name' : request.form['Name']})
        session['Calories'] = login_user['Calories']
        session['Age'] = login_user['Age']
        session['Password'] = login_user['Password']
        if login_user:
            if bcrypt.hashpw(request.form['Password'].encode('utf-8'), login_user['Password']) == login_user['Password']:
                session['Name'] = request.form['Name']
                userLoggedIn = True
                return redirect(url_for('index'))
            else:
                return 'wrong username/password' 
    return 'something else wrong'

#register function for user
@app.route('/register', methods =['POST','GET'])
def registerFunc():
    getUserId = db_operations.find().sort("_id", -1).limit(1)
    for doc in getUserId:
        user_id = (doc['_id'])
        user_id+=1
    if request.method == 'POST':
            reg_userName = request.form['regUserName']
            reg_password = request.form['regPassword']
            reg_age = request.form['regAge']
            reg_cals = int(request.form['regCals'])
            hashPassword = bcrypt.hashpw(request.form['regPassword'].encode('utf-8'), bcrypt.gensalt())
            new_user = {'_id': user_id, 'Name' : reg_userName ,'Password': hashPassword, 'Age' : reg_age, 'Calories':reg_cals, "bRecipe": '', "recipe2": '', "recipe3": '', "recipe4": '', "recipe5": '' }
            db_operations.insert_one(new_user)
            session['Name'] = reg_userName
            session['Calories'] = reg_cals
            session['Age'] = reg_age
            session['Password'] = hashPassword
            userLoggedIn = True
            return redirect(url_for('index'))
    return 'Invalid username or password'


#update user details - username, password, age and calories
@app.route('/update', methods =['POST','GET'])
def updateFunc():
    if request.method == 'POST':
            new_username = request.form['newUsername']
            new_password = bcrypt.hashpw(request.form['newPassword'].encode('utf-8'), bcrypt.gensalt())
            new_age = request.form['newAge']
            new_cals = int(request.form['newCals'])
            myquery = { "Name": session['Name'], "Password": session['Password'], "Age": session['Age'], "Calories": session['Calories'] }
            newvalues = { "$set": { "Name": new_username, "Password": new_password, "Age": new_age, "Calories": new_cals } }
            db_operations.update_one(myquery, newvalues)
            session['Name'] = new_username
            session['Calories'] = new_cals
            session['Age'] = new_age
            session['Password'] = new_password
            return redirect(url_for('index'))
    return 'Invalid username or password'
    

#getting recipes from the database - 1 breakfast recipe and 4 varied recipes
@app.route('/recipes', methods = ['POST','GET'])
def recipesFunc():
    name = session['Name']
    userDetails = db_operations.find_one({'Name': 'newTest'})
    userCalories = (userDetails['Calories'])
    #getting first recipe - i created a breakfast collection to for this - only 5 recipes
    """recipeLessThanUserCals = { "Calories": {"$lt": userCalories} }
    breakfast_recipe = db_breakfast.find_one(recipeLessThanUserCals)"""
    user = db_operations.find_one({'Name': session['Name']})
    myquery = db_breakfast.aggregate([ { '$sample': { 'size': 3 } } ])
    for doc in myquery:
        breakfast_recipe = (doc)
    #verifying if the new breakfast recipe is the same as the previous recipe
    if breakfast_recipe['name'] != (user['bRecipe']):
        name = (breakfast_recipe['name'])
        session['recipe_name'] = (breakfast_recipe['name'])
        session['intCals'] = (breakfast_recipe['Calories'])
        session['recipe_calories'] = str(session['intCals'] )
        session['recipe_ingr'] = (breakfast_recipe['Ingredients'])
        session['recipe_method'] = (breakfast_recipe['Methods'])
        session['recipe_serving'] = (breakfast_recipe['ServingSize'])
        session['recipe_nutr']= (breakfast_recipe['Nutrients'])
        session['recipe_fullNutr']= (breakfast_recipe['Full Nutrition'])
        #updating calories leftover
        session['updated_cals'] = (userCalories - session['intCals'] )
        session['updated_cals']
    else:
        recipesFunc()
    #this code runs in a loop to get 5 recipes from the recipes collection
    x= 1
    intCalories = 0
    while x<=4:
        user = db_operations.find_one({'Name': session['Name']})
        y = str(x)
        #myquery2 = { "Calories": {"$lt": updated_cals} }
        #second_recipe = db_recipe_operations.find_one( { "$and": [ { "Calories": { "$lt": updated_cals } }, { "name": { "$exists": True, "$nin": [session['recipe_name']] } } ] } )
        myquery2 = db_recipe_operations.aggregate([ { '$sample': { 'size': 3 } } ])
        for doc in myquery2:
            second_recipe = (doc)
        if session['recipe_name'+y] != (user['recipe2']) or (user['recipe3']) or (user['recipe4']) or (user['recipe5']):
            session['recipe_name'+y] = (second_recipe['name'])
            session['intCalories'+y] = (second_recipe['Calories'])
            session['recipe_calories'+y] = str(session['intCalories'+y])
            session['recipe_ingr'+y] = (second_recipe['Ingredients'])
            session['recipe_method'+y] = (second_recipe['Methods'])
            session['recipe_serving'+y] = (second_recipe['ServingSize'])
            session['recipe_nutr'+y]= (second_recipe['Nutrients'])
            session['recipe_fullNutr'+y]= (second_recipe['Full Nutrition'])
        else:
            x = x

        x+=1
    session['allRecipes_cals'] = int(session['intCals']  + session['intCalories2'] + session['intCalories3'] + session['intCalories4'] + session['intCalories5'])
    
    if session['allRecipes_cals'] < (session['Calories'] - 350) or session['allRecipes_cals'] > (session['Calories'] + 100):
        recipesFunc()

        #try save recipe names to try not duplicate recipes
        myquery = { "Name": session['Name'], "Password": session['Password'], "Age": session['Age'], "Calories": session['Calories'] }
        newvalues = { "$set": { "Name": session['Name'], "Password": session['Password'], "Age": session['Age'], "Calories": session['Calories'], "bRecipe": session['recipe_name'], "recipe2": session['recipe_name2'], "recipe3": session['recipe_name3'], "recipe4": session['recipe_name4'], "recipe5": session['recipe_name5']   } }
        db_operations.update_one(myquery, newvalues)
        
        updated_cals2 = (session['updated_cals'] - intCalories)
        updated_cals2 = 1200
    
#random selector - gets a random document
myquery = db_recipe_operations.aggregate(
        [ { '$sample': { 'size': 3 } } ])

#get a pancake recipe - could be used for breakfast recipes
anotherTest = db_recipe_operations.find_one({"name" : {'$regex' : ".*Pancakes.*"}})
len(anotherTest)


#this seems to work fine 
@app.route('/create-recipe', methods =['POST','GET'])
def create_recipe():
    i=0
    userInput = int(request.form['num'])
    while i<=userInput:
        #gets id so i dont have to hardcode it
        getId = db_recipe_operations.find().sort("_id", -1).limit(1)
        for doc in getId:
            r_id = (doc['_id'])
        r_id+=1
        uNum = random.randint(278500, 280000)
        urlNum = str(uNum)
        #save random num as a string so i can add it to url automatically
        my_url=('https://www.allrecipes.com/recipe/'+urlNum+'/')
        print(my_url)
        response = requests.get(my_url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'})
        page_soup = soup(response.content, "html.parser")
        #check if page has a recipe
        page_check = page_soup.find("div",{"class":"error-page__404"})
        if page_check != None:
            pageCheck = (page_check.text)
            index = pageCheck.rfind('/')
            pCheck = pageCheck[:index+9]
            i = i
        else:
            #get recipe name works as needed
            rName = page_soup.find("div", {"class": "headline-wrapper"})
            recipeName = (rName.text.strip())
            print(recipeName)
            #get the ingredients 
            ingr = page_soup.findAll("span", {"class": "ingredients-item-name"})
            ingredients = (' '.join(str(x.text) for x in ingr).replace("", ""))

            #recipe type
            typeCont = page_soup.findAll("span", {"class": "breadcrumbs__title"})
            rType = typeCont[2]
            tempType = rType.text
            index = tempType.rfind('/')
            recipeType = tempType[index+36:index-49]
            #method
            method_container = page_soup.findAll("div", {"class": "paragraph"})
            method = (' '.join(str(x.text) for x in method_container))
            #get calories and serving
            cals = page_soup.find("div", {"class": "nutrition-top light-underline"})
            servingCalories = (cals.text.strip())
            print(servingCalories)
            #get serving size
            sS = page_soup.find("div",{"class":"recipe-adjust-servings__original-serving"})
            serveSize = sS.text
            print(serveSize)
            #just calories
            cals = servingCalories
            index = cals.rfind('/')
            stringCalories = cals[index-4:]
            if stringCalories.rfind(':') == True:
                test = stringCalories[index-5:]
                calories = float(test)
            else:
                print(stringCalories)
                calories = float(stringCalories)
            #fats, carbs , prot
            nutr = page_soup.findAll("div",{"class":"partial recipe-nutrition-section"})
            nutrients_cont = nutr[0].text
            print(nutrients_cont)
            index = nutrients_cont.rfind('/')
            nutrients = nutrients_cont[index+13:index-16]
            print(nutrients)
            #print(nutrients)
            #get full nutrients
            fullNutr_container = page_soup.findAll("span", {"class": "nutrient-value"})
            fullNutrName_container = page_soup.findAll("span", {"class": "nutrient-name"})
            fNutr = (' '.join(str(x.text) for x in fullNutrName_container).replace(" ", "").split())
            nutrientsFull = str(fNutr)
            recipe = { "_id": r_id,
                    "name": recipeName, 
                    "ServingSize": serveSize, 
                    "Calories": calories, 
                    "Ingredients": ingredients, 
                    "Methods": method, 
                    "Nutrients": nutrients, 
                    "Full Nutrition": nutrientsFull }
            if recipeType == 'Breakfast':
                getBId = db_breakfast.find().sort("_id", -1).limit(1)
                for doc in getBId:
                    bR_id = (doc['_id'])
                bR_id +=1
                breakfastRecipe = { "_id": bR_id,
                    "name": recipeName, 
                    "ServingSize": serveSize, 
                    "Calories": calories, 
                    "Ingredients": ingredients, 
                    "Methods": method, 
                    "Nutrients": nutrients, 
                    "Full Nutrition": nutrientsFull }
                db_breakfast.insert_one(breakfastRecipe)
                x = str(i)
                result = ('result: Breakfast recipe: Created successfully'+x)
            else:
                db_recipe_operations.insert_one(recipe)
                x = str(i)
                result = ('result: Created successfully'+x)
            print(result, i)
        i+=1
    return result


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)