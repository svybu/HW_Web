import pika
from faker import Faker
from models import Contact
import connect

fake = Faker()

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

def generate_fake_contacts(num_contacts):
    for _ in range(num_contacts):
        contact = Contact(fullname=fake.name(),
                          email=fake.email(),
                          additional_info=fake.text())
        contact.save()
        channel.basic_publish(exchange='',
                              routing_key='email_queue',
                              body=str(contact.id))
    print(f"Generated {num_contacts} fake contacts and added them to the email_queue.")

if __name__ == "__main__":
    generate_fake_contacts(10)
    connection.close()
