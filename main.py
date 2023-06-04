import requests
import random
import time
import re
import lxml.html
import logging
import concurrent.futures
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.ERROR)  # Set the desired logging level

# Trivia API
url = "https://opentdb.com/api.php"
params = {
    "amount": 1,
    "type": 'multiple',
}

print('.----------------.')
print('| Made By ExamV1 |')
print("'----------------'")
print('This will spam a bunch of random trivia questions to the chosen Sendit')
sticker_link = input("\nEnter the Sendit link: ")
match = re.search(r's/([a-f\d-]+)', sticker_link)
sticker_id = match.group(1)

# Ask for the spam type
spam_type = input("Choose spam type (trivia/custom): ")

if spam_type == 'trivia':
    # Ask for the number of times to send trivia
    while True:
        send_count = input("Enter the number of times to send trivia (0 for unlimited): ")
        if send_count.isdigit():
            send_count = int(send_count)
            break
        else:
            print("Invalid input. Please enter a number.")

    proxy_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=us&ssl=all&anonymity=all"
    proxies = []
    proxy_index = 0
    proxies_rotation_interval = 5

    def validate_proxy(proxy):
        try:
            parsed = urlparse(proxy)
            if parsed.scheme and parsed.netloc:
                return True
        except Exception:
            pass
        return False

    def fetch_proxies():
        try:
            response = requests.get(proxy_url)
            if response.status_code == 200:
                proxies.clear()
                raw_proxies = response.text.strip().split("\n")
                proxies.extend(filter(validate_proxy, raw_proxies))
        except Exception as e:
            logging.error("Error fetching proxies: %s", str(e))

    def get_random_proxy():
        if len(proxies) == 0:
            return None
        return random.choice(proxies)

    def send_question():
        global proxy_index

        if proxy_index % proxies_rotation_interval == 0:
            fetch_proxies()

        proxy = get_random_proxy()
        if proxy:
            proxies_dict = {
                "http": proxy,
                "https": proxy
            }
            session = requests.Session()
            session.proxies = proxies_dict
        else:
            session = requests.Session()

        try:
            response = session.get(url, params=params)
            response.raise_for_status()  # Raise an exception for non-2xx status codes

            data = response.json()
            questions = [lxml.html.fromstring(q["question"]).text_content() for q in data["results"]]
            answers = [lxml.html.fromstring(q["correct_answer"]).text_content() for q in data["results"]]
            incorrect_answers = [[lxml.html.fromstring(answer).text_content() for answer in q["incorrect_answers"]] for q in data["results"]]

            page1 = session.get(sticker_link)
            soup1 = lxml.html.fromstring(page1.content)
            script_text1 = soup1.xpath('/html/body/script[1]/text()')[0]
            author_display_name = soup1.xpath('//*[@id="postedByText"]/span/text()[1]')[0]  # this gets the display name
            matches1 = re.findall(r'"(\w+)":\s*{"id":\s*"([^"]+)"', script_text1)  # this gets the unique id of the user you are sending to

            for i1, match1 in enumerate(matches1):
                if i1 == 1:  # this makes sure it gets the correct user id and outputs it correctly
                    var_id1 = match1[1]

            send_url = "https://reply.getsendit.com/api/v1/sendpost"
            headers = {
                "accept": "*/*",
                "accept-language": "en-GB,en;q=0.9,en-US;q=0.8",
                "content-type": "text/plain;charset=UTF-8",
                "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Microsoft Edge\";v=\"110\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin"
            }

            send_counter = 0
            while send_count == 0 or send_counter < send_count:
                choices = [answers[0]] + incorrect_answers[0]
                random.shuffle(choices)

                prompt = f"{questions[0]}\n\nA) {choices[0]}\nB) {choices[1]}\nC) {choices[2]}\nD) {choices[3]}\n"
                data = {
                    "data": {
                        "postType": "sendit.post-type:question-and-answer-v1",
                        "userId": var_id1,
                        "stickerId": sticker_id,
                        "shadowToken": "ffe4b23a-5977-435a-8109-d57cfb4ab6e2",
                        "platform": "snapchat",
                        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69"
                    },
                    "replyData": {
                        "question": prompt,
                        "promptText": ""
                    }
                }

                response = session.post(send_url, headers=headers, json=data)
                response.raise_for_status()  # Raise an exception for non-2xx status codes

                print("\nTrivia Question spam sent to Sendit user: " + author_display_name + "\n#user id: " + var_id1)

                def loading_line(length):
                    return ''.join(random.choice(['-', '=']) for _ in range(length))

                print(loading_line(10))  # This is just so you know if the code has not stopped

                proxy_index += 1
                send_counter += 1

        except Exception as e:
            logging.error("Error sending question: %s", str(e))

    # Set the number of threads to use (adjust as per your preference)
    num_threads = 10

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit the sending tasks to the executor
        futures = [executor.submit(send_question) for _ in range(num_threads)]

        # Wait for all tasks to complete
        concurrent.futures.wait(futures)

elif spam_type == 'custom':
    # Ask for the custom message
    spam_message = input("Enter the custom message to send: ")

    # Ask for the number of times to send the custom message
    while True:
        send_count = input("Enter the number of times to send the custom message (0 for unlimited): ")
        if send_count.isdigit():
            send_count = int(send_count)
            break
        else:
            print("Invalid input. Please enter a number.")

    session = requests.Session()

    page = session.get(sticker_link)
    soup = lxml.html.fromstring(page.content)
    script_text = soup.xpath('/html/body/script[1]/text()')[0]
    author_display_name = soup.xpath('//*[@id="postedByText"]/span/text()[1]')[0]  # this gets the display name
    matches = re.findall(r'"(\w+)":\s*{"id":\s*"([^"]+)"', script_text)  # this gets the unique id of the user you are sending to

    for i, match in enumerate(matches):
        if i == 1:  # this makes sure it gets the correct user id and outputs it correctly
            var_id = match[1]

    send_url = "https://reply.getsendit.com/api/v1/sendpost"
    headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8",
        "content-type": "text/plain;charset=UTF-8",
        "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Microsoft Edge\";v=\"110\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin"
    }

    send_counter = 0
    while send_count == 0 or send_counter < send_count:
        data = {
            "data": {
                "postType": "sendit.post-type:question-and-answer-v1",
                "userId": var_id,
                "stickerId": sticker_id,
                "shadowToken": "ffe4b23a-5977-435a-8109-d57cfb4ab6e2",
                "platform": "snapchat",
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69"
            },
            "replyData": {
                "question": spam_message,
                "promptText": ""
            }
        }

        response = session.post(send_url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        print("\nCustom message spam sent to Sendit user: " + author_display_name + "\n#user id: " + var_id)

        def loading_line(length):
            return ''.join(random.choice(['-', '=']) for _ in range(length))

        print(loading_line(10))  # This is just so you know if the code has not stopped

        send_counter += 1

else:
    print("Invalid spam type. Please choose 'trivia' or 'custom'.")
