from src.database.config import supabase
import bcrypt

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode('utf-8'), hashed.encode('utf-8'))

def check_teacher_exists(username):
    """
    Check if a teacher with the given username exists in the database.

    Args:
        username (str): The username of the teacher to check.

    Returns:
        bool: True if the teacher exists, False otherwise.
    """
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0

def create_teacher(username, name, password):
    """
    Create a new teacher in the database.

    Args:
        username (str): The username of the teacher.
        name (str): The name of the teacher.
        password (str): The password of the teacher.

    Returns:
        dict: The created teacher's data.
    """
    hashed_password = hash_pass(password)
    data = {
        "username": username,
        "name": name,
        "password": hashed_password
    }
    response = supabase.table("teachers").insert(data).execute()
    return response.data

def teacher_login(username, password):
    """
    Authenticate a teacher with the given username and password.

    Args:
        username (str): The username of the teacher.
        password (str): The password of the teacher.

    Returns:
        dict or None: The teacher's data if authentication is successful, None otherwise.
    """
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if len(response.data) == 0:
        return None
    teacher = response.data[0]
    if check_pass(password, teacher["password"]):
        return teacher
    return None

def get_all_students():
    response = supabase.table('students').select("*").execute()
    return response.data

def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {'name':new_name, 'face_embedding':face_embedding, 'voice_embedding':voice_embedding}
    
    response = supabase.table('students').insert(data).execute()
    
    return response.data
    