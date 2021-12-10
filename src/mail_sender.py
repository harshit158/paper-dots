import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

# Loading environment variables
from dotenv import load_dotenv; load_dotenv()
FROM_ADRS = os.getenv('FROM_ADRS')
EMAIL_PWD = os.getenv('EMAIL_PWD')

def send_mail(toaddr, subject='', body='', html_body='', book_image=None):
	fromaddr = FROM_ADRS

	msg = MIMEMultipart()
		  
	# storing the senders email address
	msg['From'] = fromaddr 

	# storing the subject  
	msg['Subject'] = "{}".format(subject)

	body = "{}".format(body)

	msg.attach(MIMEText(body, 'plain'))
	msg.attach(MIMEText(html_body, 'html'))
	
	# Attaching book cover image
	if book_image is not None:
		msg.attach(MIMEImage(book_image))

	# creates SMTP session
	s = smtplib.SMTP('smtp.gmail.com', 587) 
		  
	# start TLS for security
	s.starttls() 
		  
	# Authentication
	s.login(fromaddr, EMAIL_PWD)

	# storing the receivers email address
	msg['To'] = toaddr
	  
	# filename = "Paper.pdf".format(addr.split('@')[0])
	# attachment = open("/home/hs/Desktop/{}".format(filename), "rb")
	  
	# To change the payload into encoded form 
	#p.set_payload((attachment).read())
		
	# encode into base64
	#encoders.encode_base64(p)
		   
	# p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
		
	# attach the instance 'p' to instance 'msg' 
	# msg.attach(p)

	# Converts the Multipart msg into a string 
	text = msg.as_string()

	# sending the mail
	s.sendmail(fromaddr, toaddr, text)

	# terminating the session
	s.quit()

if __name__=="__main__":
	send_mail('harshit158@gmail.com')