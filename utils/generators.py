import time
import random
import string

def generate_unique_user(prefix="user"):
    """
    Tạo username và email unique, tránh bị trùng khi chạy test nhiều lần.
    """
    timestamp = int(time.time())  # Lấy timestamp hiện tại (giây)
    rand = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))  # 4 ký tự random

    username = f"{prefix}_{rand}_{timestamp}"
    email = f"{username}@example.com"
    return username, email
