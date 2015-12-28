import sys,os,re
import mimetypes
from time import sleep
from smtplib import SMTP
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.MIMEBase import MIMEBase
from email import Encoders
from email import encoders
from email.utils import COMMASPACE, formatdate

class Email(object):
    def __init__(self, config):
        self.config = config
        
    def sendEmail(self, subject, msgText, sender = 'Standard Sender', imgNames=None, imagesInMsgBody = False, replyTo=None, maxWidth="600px"):
        """
        Sends an e-mail with or without images attached.

        Parameters
        ----------
        subject : e-mail subject
        msgText : body of the e-mail in html
        imgNames : list of images to be attached, default None
        imagesInMsgBody: if True leave a key {IMAGES} in the place you want the images to be placed, default False
        maxWidth : max width of the images attached

        Returns
        -------
        

        """
    
        try:
            conn = SMTP(self.config['server'], self.config['port'])

            msg = MIMEMultipart()
            msg['Subject']= subject
            msg['From']   = sender
            msg['cc'] = ''

            if replyTo:
                msg['reply-to'] = replyTo

            #Attach images
            imagesHtml = ""
            if imgNames:
                i = 0
                for imgName in imgNames:
                    fp = open(imgName, 'rb')
                    img = MIMEImage(fp.read())
                    img.add_header('Content-Id', '<image_{i}>'.format(i = i))
                    imagesHtml += '<p><img style="max-width:{MAX_WIDTH}; width:100%" src="cid:image_{i}" /></p>'.format(MAX_WIDTH=maxWidth,i = i)
                    fp.close()
                    msg.attach(img)
                    i += 1
            
            body=""

            #Place images in HTML body in presence of {IMAGES}
            if imagesInMsgBody:
                try:
                    body = msgText.format(IMAGES=imagesHtml)
                except Exception, e:
                    pass
            else:
                body+=imagesHtml
                body+=msgText

            msg.attach(MIMEText(body, _subtype='html'))

            conn.ehlo()
            conn.starttls()
            conn.set_debuglevel(False)
            conn.login(self.config['username'],self.config['password'])
            try:
                conn.sendmail(sender, self.config['to'], msg.as_string())
            finally:
                conn.close()
        except:
            print "Unexpected error:", sys.exc_info()[0]