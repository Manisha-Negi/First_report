import cx_Oracle
import pandas as pd
import urllib.parse as urlparse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from IPython.display import display
from IPython.display import HTML
import pyshorteners

conn = cx_Oracle.connect('CONSULTIT/Alpha1234@XePDB1')
c = conn.cursor()

#def details(name,url,hospital_name,ClaimNo):
def details(name,url,hospital_name,ClaimNo,email,company):

    html_t =f"""\
    <html>
      <head></head>
      <body>
      <p>
        Dear Mr. /Ms. {name}, <br><br>
        Thanks for choosing {company}! <br><br>
        We hope you are recovering well. Please spare a minute to fill in the Hospital Survey Questionnaire <br>
        by clicking on {url}. This will help us to serve you better. <br><br>
        Feel free to contact us at (0129-4289999/crcm@rakshatpa.com) for any other query. <br><br>
        This is an automated mail and do not reply to the same. <br>
        <br>
        Best Regards <br>
        Raksha Health Insurance TPA Pvt. Ltd. <br>
        </p>  
        </body>
        </html>
        """
    try:
        msg = MIMEMultipart()
        # Step 3 - Create message body
        message = html_t
        # Step 4 - Declare SMTP credential
        password = "info#@5164"
        username = "info"
        # smtphost = "mailx.rakshamail.com:587"   #initially this was used...as host
        smtphost = "mailx.rakshamail.com:587"
        # Step 5 - Declare message elements
        msg['From'] = "info@rakshatpa.com"
        #msg['To'] =  'rohitcrk1@gmail.com'
        msg['To'] =  email
        msg['Subject'] = "Hospital Survey Questionnaire for your Hospitalization at {} – {}".format(hospital_name,ClaimNo)
        # Step 6 - Add the message body to the object instance
        msg.attach(MIMEText(message, 'html'))
        # Step 7 - Create the server connection
        s = smtplib.SMTP(smtphost)
        s.starttls()
        # Step 9 - Authenticate with the server
        s.login(username, password)
        s.sendmail(msg['From'], msg['To'], msg.as_string())

        # Step 11 - Disconnect
        s.quit()
        status_value = "Successfully sent email message to %s:" % (msg['To'])
        print(status_value)
        c.execute("""update SURVEY_URL set EMAIL_FLAG = 'Y' where CLAIM_NO = '{}' """.format(ClaimNo))
        conn.commit()

    except Exception as e:
        print(e)
        c.execute("""update SURVEY_URL set EMAIL_FLAG = 'P' where CLAIM_NO = '{}' """.format(ClaimNo))
        conn.commit()
        
        
df = c.execute(""" SELECT * from SURVEY_URL where EMAIL_FLAG = 'N' and EMAIL not in ('NA', 'na@na.com') """)
df1 = df.fetchall()
#print(df1)
for i in df1:

    Name = i[4]
    #print(Name)

    Claim = i[6]
    #print(Claim)

    HosName = i[5]
    #print(HosName)
    
    MobileNo = i[2]
    #print(MobileNo)

    mail = i[3]
    #print(mail)

    new_url = i[1]
    #print(new_url)

    comp_name = i[10]
    #print(comp_name)

    s = pyshorteners.Shortener()
    New_Url = s.tinyurl.short(new_url)
    
    details(Name,New_Url,HosName,Claim,mail,comp_name)
    
    #details(Name,new_url,HosName,Claim)



