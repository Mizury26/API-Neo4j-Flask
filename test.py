import requests
import json

BASE_URL = "http://localhost:5000"

def print_response(response):
    """Affiche la réponse JSON formatée."""
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print("Invalid JSON response")
    print("---")

def test_create_users():
    """Créer des utilisateurs."""
    print("Creating users...")

    users = []
    for name, email in [("Alice", "alice@example2.com"), ("Bob", "bob@example2.com")]:
        response = requests.post(f"{BASE_URL}/users", json={"name": name, "email": email})
        print_response(response)
        if response.status_code == 201:
            users.append(response.json()["user"]["id"])

    return users if len(users) == 2 else (None, None)

def test_get_users():
    """Récupérer tous les utilisateurs."""
    print("Fetching all users...")
    response = requests.get(f"{BASE_URL}/users")
    print_response(response)

def test_update_user(user_id):
    """Mettre à jour un utilisateur."""
    print(f"Updating user {user_id}...")
    response = requests.put(f"{BASE_URL}/users/{user_id}", json={"name": "Alice Updated"})
    print_response(response)

def test_delete_user(user_id):
    """Supprimer un utilisateur."""
    print(f"Deleting user {user_id}...")
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    print_response(response)

def test_create_friendship(user1_id, user2_id):
    """Ajouter une relation d'amitié."""
    print(f"Making {user1_id} and {user2_id} friends...")
    response = requests.post(f"{BASE_URL}/users/{user1_id}/friends", json={"friend_id": user2_id})
    print_response(response)

def test_check_friendship(user1_id, user2_id):
    """Vérifier si deux utilisateurs sont amis."""
    print(f"Checking if {user1_id} and {user2_id} are friends...")
    response = requests.get(f"{BASE_URL}/users/{user1_id}/friends/{user2_id}")
    print_response(response)

def test_get_friends(user_id):
    """Récupérer la liste des amis d'un utilisateur."""
    print(f"Fetching friends of user {user_id}...")
    response = requests.get(f"{BASE_URL}/users/{user_id}/friends")
    print_response(response)

def test_get_mutual_friends(user1_id, user2_id):
    """Récupérer les amis en commun."""
    print(f"Fetching mutual friends between {user1_id} and {user2_id}...")
    response = requests.get(f"{BASE_URL}/users/{user1_id}/mutual-friends/{user2_id}")
    print_response(response)

def test_delete_friendship(user1_id, user2_id):
    """Supprimer une relation d’amitié."""
    print(f"Removing friendship between {user1_id} and {user2_id}...")
    response = requests.delete(f"{BASE_URL}/users/{user1_id}/friends/{user2_id}")
    print_response(response)

def test_create_post(user_id):
    """Créer un post pour un utilisateur."""
    print(f"Creating post for user {user_id}...")
    response = requests.post(f"{BASE_URL}/users/{user_id}/posts", json={"title": "Test Post", "content": "This is a test post."})
    print_response(response)

    return response.json()["post"]["id"] if response.status_code == 201 else None

def test_get_posts():
    """Récupérer tous les posts."""
    print("Fetching all posts...")
    response = requests.get(f"{BASE_URL}/posts")
    print_response(response)

def test_update_post(post_id):
    """Mettre à jour un post."""
    print(f"Updating post {post_id}...")
    response = requests.put(f"{BASE_URL}/posts/{post_id}", json={"title": "Updated Post Title"})
    print_response(response)

def test_delete_post(post_id):
    """Supprimer un post."""
    print(f"Deleting post {post_id}...")
    response = requests.delete(f"{BASE_URL}/posts/{post_id}")
    print_response(response)

def test_like_post(post_id, user_id):
    """Liker un post."""
    print(f"User {user_id} liking post {post_id}...")
    response = requests.post(f"{BASE_URL}/posts/{post_id}/like", json={"user_id": user_id})
    print_response(response)

def test_add_comment(post_id, user_id):
    """Ajouter un commentaire à un post."""
    print(f"User {user_id} commenting on post {post_id}...")
    response = requests.post(f"{BASE_URL}/posts/{post_id}/comments", json={"content": "Great post!", "user_id": user_id})
    print_response(response)

    return response.json()["comment"]["id"] if response.status_code == 201 else None

def test_delete_comment(comment_id):
    """Supprimer un commentaire."""
    print(f"Deleting comment {comment_id}...")
    response = requests.delete(f"{BASE_URL}/comments/{comment_id}")
    print_response(response)

def test_unlike_post(post_id, user_id):
    """Supprimer un like d'un post."""
    print(f"User {user_id} unliking post {post_id}...")
    response = requests.delete(f"{BASE_URL}/posts/{post_id}/like", json={"user_id": user_id})
    print_response(response)

def run_tests():
    """Exécuter tous les tests."""
    user1_id, user2_id = test_create_users()
    if not user1_id or not user2_id:
        print("User creation failed. Stopping tests.")
        return

    test_get_users()
    test_update_user(user1_id)

    test_create_friendship(user1_id, user2_id)
    test_check_friendship(user1_id, user2_id)
    test_get_friends(user1_id)
    test_get_mutual_friends(user1_id, user2_id)

    post_id = test_create_post(user1_id)
    if not post_id:
        print("Post creation failed. Stopping tests.")
        return

    test_get_posts()
    test_update_post(post_id)
    test_like_post(post_id, user2_id)

    comment_id = test_add_comment(post_id, user2_id)
    if not comment_id:
        print("Comment creation failed. Stopping tests.")
        return

    test_delete_comment(comment_id)
    test_unlike_post(post_id, user2_id)
    test_delete_post(post_id)
    
    test_delete_friendship(user1_id, user2_id)
    test_delete_user(user1_id)
    test_delete_user(user2_id)

if __name__ == "__main__":
    run_tests()
