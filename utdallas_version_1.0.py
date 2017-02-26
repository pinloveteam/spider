import urllib.request
import re

def get_email_address_from_page(page_address):

    request = urllib.request.Request(page_address)
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    
    email_pattern = re.compile('[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,5}')
    emails = re.findall(email_pattern, content)

    return emails


web_address = 'http://utdchinese.forumotion.com'

# Capture topic 
web_request = urllib.request.Request(web_address) 
web_response = urllib.request.urlopen(web_request)
web_page =  web_response.read().decode('utf-8')

topic_address_pattern = re.compile('<a href="/f(\d+)-forum" class="forumtitle">')    
topic_addresses = re.findall(topic_address_pattern, web_page)

print('There are %d topics' % len(topic_addresses))

#f = open("dump.txt", "w", encoding="utf-8")
#f.write(web_page)
#f.close()

#print(topic_addresses)

emails = set([])

# Topic page 
for topic_address_idx in topic_addresses:

    topic_address = web_address + '/f' + str(topic_address_idx) + '-forum'
    
    print('Working on topic ' + topic_address) 

    topic_request = urllib.request.Request(topic_address) 
    topic_response = urllib.request.urlopen(topic_request)
    topic_page = topic_response.read().decode('utf-8')

    # Capture topic sub-pages 
    topic_sub_page_count_pattern = re.compile('<a href="/f\dp(.*?)-forum">.*?</a>')
    topic_sub_page_count_str = re.findall(topic_sub_page_count_pattern, topic_page)
    topic_sub_page_count = []
    for item in topic_sub_page_count_str:
        topic_sub_page_count.append(int(item))

    max_topic_sub_page_count = 0 
    if len(topic_sub_page_count) != 0 :
        max_topic_sub_page_count = max(topic_sub_page_count)

    # Generate address for topic sub-pages
    topic_sub_page_addresses = [topic_address]
    for i in range(50, max_topic_sub_page_count+1, 50):
        topic_sub_page_addresses.append(web_address + '/f' + str(topic_address_idx) + 'p' + str(i) +'-forum')

    print('There are %d topic sub-pages' % len(topic_sub_page_addresses))
    # print(topic_sub_page_addresses)

    # Loop the address
    for topic_sub_page_address in topic_sub_page_addresses: 

        print('Working on topic sub-page ' + topic_sub_page_address)
    
        # Topic sub-page
        topic_sub_page_request = urllib.request.Request(topic_sub_page_address)
        topic_sub_page_response = urllib.request.urlopen(topic_sub_page_request)
        topic_sub_page = topic_sub_page_response.read().decode('utf-8')

        post_address_pattern = re.compile('<a class="topictitle" href="(.*?)">')
        post_addresses = re.findall(post_address_pattern, topic_sub_page)

        # print(post_addresses) 

        for item in post_addresses:
            post_address = web_address + item
            email_from_one_page = get_email_address_from_page(post_address)
            emails.update(email_from_one_page)
            # print(emails)
        
        print(leng(emails))

email_file = open("emails.txt", "w", encoding="utf-8")
email_file。write(emails)
email_file.close()

#f = open("dump.txt", "w", encoding="utf-8")
#f.write(web_page)
#f.close()



