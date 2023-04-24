import pika
from models import Contact
import connect

def send_email(contact):
    print(f"Sending email to {contact.fullname} <{contact.email}>")
    contact.message_sent = True
    contact.save()

def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id=contact_id).first()
    if contact and not contact.message_sent:
        send_email(contact)
    else:
        print("Contact not found or already processed.")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
