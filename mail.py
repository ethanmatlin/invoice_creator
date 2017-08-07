#! /usr/bin/env python

#####for tex to pdf

#proc = subprocess.Popen(['pdflatex', 'cover.tex'])
#proc.communicate()
#######

# For guessing MIME type
import mimetypes
# Import the email modules we'll need
import email
import email.mime.application
#allows email stuff
import smtplib
#import requests
import json
import csv
import argparse
import pdfkit
import webbrowser
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("subject",
                        help="subject of email to be sent to all students")
    args = parser.parse_args()
    cur_dir= "."

    csv_path = cur_dir + '/emails.csv'
    config_path = cur_dir + '/config.json'
    subject=args.subject
    recipients={}

    if subject.find("oach") != -1:
        message_text = cur_dir + '/messageCoach.txt'
    else:
        message_text=cur_dir + '/messageShuttle.txt'

    # get config file
    with open(config_path) as config_file:
         data = json.load(config_file)

    recipients = csv_parser(csv_path)

    print recipients

    for user, email in recipients.iteritems():
        pdfkit.from_file(cur_dir + '/' + user+'.html',cur_dir+'/'+user+'.pdf')
        os.remove(cur_dir + '/' + user+'.html')

    recipients = check_batch(recipients, cur_dir)[0]

    if (raw_input('Type confirm to send emails:') == 'confirm'):
        print "confirm"
        send_all(data, recipients, subject, message_text, cur_dir)
    else:
        print "problem"
# get user and email addresses form CSV into a dictionary
def csv_parser(file_path):
    csv_file = open(file_path, 'r')
    dictionary = {}
    with csv_file as emails:
        reader = csv.DictReader(emails)
        for row in reader:
            dictionary[row['USER']] = row['EMAIL']
    return dictionary

def check_batch(recipients, parent_directory):
    succeed_recipients = {}
    failed_recipients = {}

    # try opening each file that we are going to send
    for user, email in recipients.iteritems():
        try:
            with open(make_path(user, parent_directory)) as attachment:
                succeed_recipients[user] = email
        except IOError:
            failed_recipients[user] = email
        print make_path(user, parent_directory)

    # print results
    print "Files found for the following students:"
    for usr, eml in succeed_recipients.iteritems():
        print '\033[92m' + usr + '<'+ eml + '>' + '\033[0m'

    print "Files NOT found for the following student:"
    for usr, eml in failed_recipients.iteritems():
        print '\033[91m' + usr + '<'+ eml + '>' + '\033[0m'

    return [succeed_recipients, failed_recipients]

# send personalized email to student with grade
def send_grade(sender_info, recipient, subject, message, attachment):
    print attachment
    if subject.find("oach") != -1:
        print "SageCoach Bill"
        atch = ["./Expense Transfer Form.pdf",attachment]
    else:
        print "Sage Shuttle Bill"
        atch = [attachment]

    msg = email.mime.Multipart.MIMEMultipart()
    msg['Subject'] = subject
    msg['To'] =  recipient
    msg['Cc'] = "ethanmatlin@gmail.com, ethan.matlin@pomona.edu, bls04747@mymail.pomona.edu"
    msg['From'] = sender_info['SENDER']
    msg.add_header('reply-to', "ethan.matlin@pomona.edu")
    with open (message, "r") as myfile:
        bodyText=myfile.read().replace('\n', '')

    html = email.mime.Text.MIMEText(bodyText, 'html')
    msg.attach(html)

    print atch
    for f in atch or []:
        filename=f
        fp=open(filename,'rb')
        att = email.mime.application.MIMEApplication(fp.read(),_subtype="pdf")
        fp.close()
        att.add_header('Content-Disposition','attachment',filename=filename)
        msg.attach(att)

    mail = smtplib.SMTP(sender_info['SERVER'], sender_info['PORT'])
    mail.starttls()
    mail.login(sender_info['USERNAME'], sender_info['PASSWORD'])
    mail.sendmail(sender_info['SENDER'], [recipient,"ethanmatlin@gmail.com, em002014@pomona.edu, bls04747@pomona.edu"], msg.as_string())
    mail.quit()


# send emails to all students
def send_all(sender_info, recipients, subject, message, parent_directory):
    print "Sending..."
    print recipients
    for user, email in recipients.iteritems():
        attachment1=make_path(user, parent_directory)
        send_grade(sender_info, email, subject, message, attachment1)
        print '\033[92m' + 'SENT  ' + user + '<' + email + '>' + '(I think)'+'\033[0m'
    print "Complete."

# generate file path for directory structure
def make_path(user, directory):
    return directory + '/' + user +".pdf"

if __name__ == "__main__": main()
