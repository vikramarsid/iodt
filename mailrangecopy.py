import RPi.GPIO as GPIO
import smtplib
import requests
import subprocess
from email.mime.text import MIMEText
from email.header    import Header
import poplib
from email import parser
#from gmail import Gmail
import time
import imaplib
from config_map import ConfigMap
import time
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("device.config")
cfgfile = open("device.config", 'r')
email = Config.get("userprofile", "email")
print email
GPIO.setmode(GPIO.BCM)

TRIG = 20 
ECHO = 26

obj = imaplib.IMAP4_SSL('imap.gmail.com', '993')
obj.login('iodt2016', 'project2016')

pop_conn = poplib.POP3_SSL('pop.gmail.com')
pop_conn.user('iodt2016')
pop_conn.pass_('project2016')
#Get messages from server:
messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
# Concat message pieces:
messages = ["\n".join(mssg[1]) for mssg in messages]
#Parse message into an email object:
messages = [parser.Parser().parsestr(mssg) for mssg in messages]


smtp_host = 'smtp.gmail.com'

login = 'iodt2016@gmail.com'
password = 'project2016'

recipients_emails = ['"%s"' % email]
print recipients_emails


print "Calculating the level"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)
print "Waiting"
time.sleep(2)

GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)

while GPIO.input(ECHO)==0:
  pulse_start = time.time()

while GPIO.input(ECHO)==1:
  pulse_end = time.time()

pulse_duration = pulse_end - pulse_start

distance = pulse_duration * 17150

distance = round(distance, 2)

print "Level:",distance,"cm"

i = str(distance)


msg = MIMEText('Detergent is less. Reordering it via AMAZON. Please reply to this email with yes in subject to proceed', 'plain', 'utf-8')
msg['Subject'] = Header('Reorder Alert: Detergent level is '+i+' cm', 'utf-8')
msg['From'] = login
msg['To'] = ", ".join(recipients_emails)

s = smtplib.SMTP(smtp_host, 587, timeout=10)

s.set_debuglevel(1)



#pop_conn = poplib.POP3_SSL('pop.gmail.com')
#pop_conn.user('iodt2016')
#pop_conn.pass_('project2016')
#Get messages from server:
#messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
# Concat message pieces:
#messages = ["\n".join(mssg[1]) for mssg in messages]
#Parse message intom an email object:
#messages = [parser.Parser().parsestr(mssg) for mssg in messages]
#for message in messages:
#    print message['subject']

if distance > 100:

 for message in messages:
      
  subject = message['subject']
  print subject 

 try:
    s.starttls()
    s.login(login, password)
    s.sendmail(msg['iodt2016@gmail.com'], recipients_emails, msg.as_string())
    #subprocess.Popen({'sh', 'curls.sh'})
    
    #for message in messages:
      
      #subject = message['subject']
      #print subject
    #mails = s.inbox().mail()
    #for i in mails:
      #print i
    while True:
        
      time.sleep(100)
        
      if subject == "yes":
        print "Success order..."
        obj.select('Inbox')
        typ ,data = obj.search(None, 'UnSeen')
        obj.store(data[0].replace(' ',','),'+FLAGS','\Seen')
        subprocess.Popen({'sh', 'curls.sh'})
        break
      else:
        print "Order wont be processed"
        obj.select('Inbox')
        typ ,data = obj.search(None, 'UnSeen')
        obj.store(data[0].replace(' ',','),'+FLAGS','\Seen')
        break


 finally:
    #s.quit()
    GPIO.cleanup()
    pop_conn.quit()

