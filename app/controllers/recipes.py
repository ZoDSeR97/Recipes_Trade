from app import app
from app.models import recipe, user
from flask import render_template, redirect, request, session

# Reading all recipes with users
@app.route('/recipes')
def profile():
    if 'user_id' not in session:
        return redirect('/')
    return render_template("recipes.html", user=user.User.get_one({'id': session['user_id']})[0], recipes=recipe.Recipe.get_all())

# Reading one recipe
@app.route('/recipes/<int:id>')
def recipeInfo(id):
    if 'user_id' not in session:
        return redirect('/')
    return render_template('recipe.html', user=user.User.get_one({'id': session['user_id']})[0], recipe=recipe.Recipe.get_one({'id': id}))

# Efiting recipe
@app.route('/recipes/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/')
    return render_template('edit_recipe.html', recipe=recipe.Recipe.get_one({'id':id}))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if recipe.Recipe.is_valid(request.form):
        recipe.Recipe.update({'id': id, **request.form})
        return redirect('/recipes')
    else:
        return redirect('/recipes/edit/'+str(id))

# Delete one recipe
@app.route('/recipes/delete/<int:id>')
def remove(id):
    recipe.Recipe.remove({'id':id})
    return redirect('/recipes')

# New Recipe
@app.route('/recipes/new')
def new():
    return render_template('add_recipe.html')


@app.route('/Add/<int:id>', methods=['POST'])
def new_recipe(id):
    if session['user_id'] == id and recipe.Recipe.is_valid(request.form):
        data = {'user_id': id, **request.form}
        recipe.Recipe.save(data)
        return redirect('/recipes')
    else:
        return redirect('/recipes/new')
