# locustfile.py
from locust import HttpUser, task, between

class FastAPIUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_root(self):
        self.client.get("/")

    @task
    def get_about(self):
        self.client.get("/about")

    @task
    def post_message(self):
        msg_name = "test-message"
        self.client.post(f"/messages/{msg_name}/")

    @task
    def get_messages(self):
        self.client.get("/messages")
        