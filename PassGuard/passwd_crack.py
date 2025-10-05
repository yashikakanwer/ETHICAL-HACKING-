import string
import time


common_passwords = [
    "123456", "123456789", "qwerty", "password", "111111", "12345678", "abc123", "1234567",
    "password1", "12345", "1234567890", "123123", "000000", "iloveyou", "1234", "1q2w3e4r5t",
    "qwertyuiop", "123", "monkey", "dragon", "123456a", "654321", "123321", "666666", "1qaz2wsx",
    "myspace1", "121212", "homelesspa", "123qwe", "a123456", "123abc", "1q2w3e4r", "qwe123",
    "7777777", "qwerty123", "target123", "tinkle", "987654321", "qwerty1", "222222", "zxcvbnm",
    "gwerty", "fuckyou", "112233", "asdfghjkl", "123123123", "qazwsx", "computer", "princess",
    "159753", "michael", "football", "sunshine", "1234qwer", "aaaaaa", "789456123", "daniel",
    "princess1", "123654", "11111", "asdfgh", "999999", "11111111", "passer2009", "888888",
    "shadow", "superman", "jordan23", "jessica", "monkey1", "baseball", "killer", "samsung",
    "master", "soccer", "jordan", "linkedin", "thomas", "liverpool", "michelle", "nicole",
    "131313", "asdfasdf", "987654", "andrew", "hello1", "justin", "anthony", "angel1", "1111111",
    "hello", "hunter", "naruto", "bitch1", "welcome", "tigger", "babygirl", "parola", "robert",
    "696969", "0987654321", "secret", "purple", "baseball1", "1111111111", "buster", "hannah",
    "freedom", "george", "william", "amanda", "number1", "qwerty12", "flower", "maggie",
    "pakistan", "letmein", "superman1", "batman", "mustang", "sunshine1", "internet",
    "london", "harley", "alexander", "xbox360", "pepper", "family", "loveyou", "50cent",
    "whatever", "joshua", "status", "david", "cookie", "martin", "again", "madison",
    "patricia", "kristina", "a1234567", "pokemon", "nirvana", "destiny", "qwe123", "shadow1",
    "patrick", "nicole1", "jordan1", "12345qwerty", "august", "liverpool1", "test123",
    "qazwsx123", "christina", "rae", "flower1", "chelsea", "qwerty12345", "qwerty1234",
    "charlie1", "mylove", "michael1", "jessica1", "princess12", "baseball12", "football12",
    "hockey", "teddy", "robbie", "marlboro", "charlotte1", "jones", "1234asdf", "loveme",
    "q123456", "computer1", "michelle1", "williams", "soccer11", "christmas", "money",
    "harvey", "taylor1", "private", "butterfly1", "dragonball", "king", "panther", "qwertz",
    "summer", "sasuke", "iloveyou12", "samantha", "victory", "marcus", "chelsea1", "pussy",
    "dolphins", "football2", "pass123", "iloveu2", "internet1", "rangers", "catdog", "dreamer",
    "woaini", "cookies", "freddy", "danielle", "alexis", "jessie", "cameron", "oscar", "canada",
    "shadow123", "pastore", "lover", "ilovejesus", "123qweasd", "angel", "theman", "qwertyui",
    "dragon1", "access", "kitten", "derek", "whale", "peach", "matrix", "football1", "testtest",
    "hannah1", "maryjane", "message", "marina", "frank", "flower", "buddy", "lake", "peggy",
    "lucky", "marie", "mario", "josh", "rachel", "water", "pokemon123", "happy", "monica", "summer1"

]

def check_password_strength(pw):
    length = len(pw) >= 8
    uppercase = any(c.isupper() for c in pw)
    digit = any(c.isdigit() for c in pw)
    special = any(c in string.punctuation for c in pw)
    score = sum([length, uppercase, digit, special])
    return score

def dictionary_attack(pw):
    print("\nStarting dictionary attack...")
    time.sleep(1)
    if pw in common_passwords:
        print(f"Password cracked by dictionary attack: {pw}")
        return True
    else:
        print("Not found in dictionary, moving to brute force...")
        return False

def brute_force_attack(pw, max_length=4):
    print("\nStarting brute force attack...")
    chars = string.ascii_lowercase + string.digits
    attempt_count = 0
    
    def brute_force(current=''):
        nonlocal attempt_count
        if len(current) > max_length:
            return False
        attempt_count += 1
        if current == pw:
            return True
        for c in chars:
            if brute_force(current + c):
                return True
        return False
    
    start_time = time.time()
    found = brute_force()
    end_time = time.time()
    
    if found:
        print(f"Password cracked by brute force after {attempt_count} attempts in {end_time-start_time:.2f} seconds.")
        return True
    else:
        print(f"Brute force failed after {attempt_count} attempts.")
        return False

def main():
    user_password = input("Enter a password to test: ")
    
    strength_score = check_password_strength(user_password)
    
    print(f"\nPassword Strength Score (out of 4): {strength_score}")
    if strength_score < 3:
        print("Warning: Your password is weak. Consider using uppercase letters, digits, and special symbols.")
    else:
        print("Your password has good complexity.")
    
    if not dictionary_attack(user_password):
        brute_force_attack(user_password)

if __name__ == "__main__":
    main()
