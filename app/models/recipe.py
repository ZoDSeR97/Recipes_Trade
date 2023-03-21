from app.models import base, user
from app.config import mySQLconnect
from flask import flash

class Recipe(base.Base):
    db='recipe_db'
    tbl_name='recipe'
    def __init__(self, data) -> None:
        super().__init__(data)
        self.name = data["name"]
        self.under = data["under"]
        self.description = data["description"]
        self.instruction = data["instruction"]
        self.date_made = data["date_made"]
        
    @classmethod
    def get_all(cls): # Get all recipes with users
        query = """
            SELECT * FROM recipe JOIN user ON recipe.user_id = user.id
        """
        results = mySQLconnect.connect(cls.db).run_query(query)
        # should not fail since user can only request if there is any
        recipes = []
        for item in results:
            recipe = cls(item)
            user_info = {
                'id': item['user.id'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'email': item['email'],
                'password': item['password'],
                'mumbo_jumbo': item['mumbo_jumbo'],
                'created_at': item['user.created_at'],
                'updated_at': item['user.updated_at'],
            }
            recipe.user = user.User(user_info)
            recipes.append(recipe)
        return recipes

    @classmethod
    def get_one(cls, data): # Get one recipe with user 
        query = """
            SELECT * FROM recipe JOIN user ON recipe.user_id = user.id
            WHERE recipe.id=%(id)s
        """
        result = mySQLconnect.connect(cls.db).run_query(query,data)
        recipe = cls(result[0]) # should not fail since user can only request if there is any
        for item in result:
            user_info = {
                'id': item['user.id'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'email': item['email'],
                'password': item['password'],
                'mumbo_jumbo': item['mumbo_jumbo'],
                'created_at': item['user.created_at'],
                'updated_at': item['user.updated_at'],
            }
            recipe.user = user.User(user_info)
        return recipe
    
    @staticmethod
    def is_valid(data):
        error = {}
        if len(data['name']) < 3:
            error['name'] = 'Name need to be at least 3 characters'
        
        if len(data['description']) < 3:
            error['description'] = 'Description need to be at least 3 characters'
            
        if len(data['instruction']) < 3:
            error['instruction'] = 'Instruction need to be at least 3 characters'
        
        if 'under' not in data:
            error['under'] = 'Is the recipe under 30 minutes???'
        
        if 'date_made' not in data:
            error['date_made'] = "When was this recipe created???"
        
        for catagory, message in error.items():
            flash(message, catagory)
        
        return not bool(error)
