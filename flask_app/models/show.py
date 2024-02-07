from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
EMAIL_REGEX = re.compile(r'([A-Za-z0-9]+[.\-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Za-z]{2,})+')

PASWORD_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class Show:
    db_name = "examreview"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.releaseDate = data['releaseDate']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM shows;"
        results = connectToMySQL(cls.db_name).query_db(query)
        shows = []
        if results:
            for show in results:
                shows.append(show)
            return shows
        return shows

    @classmethod
    def get_show_by_id(cls, data):
        query = 'SELECT * FROM shows left join users on shows.user_id = users.id where shows.id = %(id)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            query2 = 'SELECT * FROM comments left join users on comments.user_id = users.id WHERE comments.show_id = %(id)s;'
            results2 =  connectToMySQL(cls.db_name).query_db(query2, data)
            comments = []
            if results2:
                for comment in results2:
                    comments.append(comment)
            result[0]['comments'] = comments
            return result[0]
        return False
        
    @classmethod
    def addComment(cls, data):
        query = "INSERT INTO comments (komenti, user_id, show_id) VALUES (%(komenti)s, %(user_id)s, %(show_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    @classmethod
    def get_comment_by_id(cls, data):
        query = 'SELECT * FROM comments where id = %(id)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False
    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO shows (title, network, releaseDate, description, user_id) VALUES (%(title)s, %(network)s, %(releaseDate)s, %(description)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def deleteAllPostComments(cls, data):
        query = "DELETE FROM comments where comments.show_id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM shows where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def deleteComment(cls, data):
        query = "DELETE FROM comments where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE shows set title=%(title)s, network = %(network)s, description = %(description)s, releaseDate = %(releaseDate)s where shows.id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_show(user):
        is_valid = True
        
        if len(user['title'])<3:
            flash("Title is required!", 'title')
            is_valid = False
        if len(user['network'])<3:
            flash("Network is required!", 'network')
            is_valid = False
        if len(user['description'])<3:
            flash("Description is required!", 'description')
            is_valid = False
        if not user['releaseDate']:
            flash("Release date is required!", 'releaseDate')
            is_valid = False
        return is_valid
    
  