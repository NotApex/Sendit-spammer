# huge thanks to ExamV1 for the Trivi spam https://github.com/ExamV1/

import random
import re
import lxml.html
import logging
import aiohttp
import asyncio
import signal
import uuid
from urllib.parse import urlparse
from asyncio import Lock
from fake_useragent import UserAgent

# Configure logging
logging.basicConfig(level=logging.ERROR)  # Set the desired logging level

# Trivia API
url = "https://opentdb.com/api.php"

print('.----------------.')
print('| Made By Apex   |')
print("'----------------'")
print('This will spam a bunch of random trivia questions or custom text to the chosen Sendit')
sticker_link = input("\nEnter the Sendit link: ")
match = re.search(r's/([a-f\d-]+)', sticker_link)
if not match:
    print("Invalid Sendit link.")
    exit()
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

    async def send_question(session, lock):
        params = {
            "amount": 1,
            "type": 'multiple',
        }
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()  # Raise an exception for non-2xx status codes

                data = await response.json()
                questions = [lxml.html.fromstring(q["question"]).text_content() for q in data["results"]]
                answers = [lxml.html.fromstring(q["correct_answer"]).text_content() for q in data["results"]]
                incorrect_answers = [[lxml.html.fromstring(answer).text_content() for answer in q["incorrect_answers"]] for q in data["results"]]

                async with session.get(sticker_link) as page1:
                    soup1 = lxml.html.fromstring(await page1.content.read())
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

                async with lock:
                    send_counter = 0

                while send_count == 0 or send_counter < send_count:
                    choices = [answers[0]] + incorrect_answers[0]
                    random.shuffle(choices)

                    prompt = f"{questions[0]}\n\nA) {choices[0]}\nB) {choices[1]}\nC) {choices[2]}\nD) {choices[3]}\n"
                    
                    # Generate random User-Agent
                    user_agent = UserAgent().random

                    # Generate random shadowToken
                    shadow_token = str(uuid.uuid4())

                    data = {
                        "data": {
                            "postType": "sendit.post-type:question-and-answer-v1",
                            "userId": var_id1,
                            "stickerId": sticker_id,
                            "shadowToken": shadow_token,
                            "platform": "snapchat",
                            "userAgent": user_agent
                        },
                        "replyData": {
                            "question": prompt,
                            "promptText": ""
                        }
                    }

                    async with session.post(send_url, headers=headers, json=data) as response:
                        response.raise_for_status()  # Raise an exception for non-2xx status codes

                    async with lock:
                        send_counter += 1

                    print(f"\nTrivia Question spam sent to Sendit user: {author_display_name}\n#user id: {var_id1}")

                    def loading_line(length):
                        return ''.join(random.choice(['-', '=']) for _ in range(length))

                    print(loading_line(44)) 

        except Exception as e:
            logging.error("Error sending question: %s", str(e))

    # Set the number of threads to use (adjust as per your preference)
    num_threads = int(input("Enter the number of threads to use: "))

    async def main():
        async with aiohttp.ClientSession() as session:
            lock = Lock()  # Create a lock object
            # Submit the sending tasks to the executor
            tasks = [send_question(session, lock) for _ in range(num_threads)]
            await asyncio.gather(*tasks)

    # Run the main function
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

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

    async def send_custom_message(session, lock):
        try:
            page = await session.get(sticker_link)
            soup = lxml.html.fromstring(await page.content.read())
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

            async with lock:
                send_counter = 0

            while send_count == 0 or send_counter < send_count:
                # Generate random User-Agent
                user_agent = UserAgent().random

                # Generate random shadowToken
                shadow_token = str(uuid.uuid4())

                data = {
                    "data": {
                        "postType": "sendit.post-type:question-and-answer-v1",
                        "userId": var_id,
                        "stickerId": sticker_id,
                        "shadowToken": shadow_token,
                        "platform": "snapchat",
                        "userAgent": user_agent
                    },
                    "replyData": {
                        "question": spam_message,
                        "promptText": ""
                    }
                }

                async with session.post(send_url, headers=headers, json=data) as response:
                    response.raise_for_status()  # Raise an exception for non-2xx status codes

                async with lock:
                    send_counter += 1

                print(f"\nCustom message spam sent to Sendit user: {author_display_name}\n#user id: {var_id}")

                def loading_line(length):
                    return ''.join(random.choice(['-', '=']) for _ in range(length))

                print(loading_line(44)) 

        except Exception as e:
            logging.error("Error sending custom message: %s", str(e))

    # Set the number of threads to use (adjust as per your preference)
    num_threads = int(input("Enter the number of threads to use: "))

    async def main():
        async with aiohttp.ClientSession() as session:
            lock = Lock()  # Create a lock object
            # Submit the sending tasks to the executor
            tasks = [send_custom_message(session, lock) for _ in range(num_threads)]
            await asyncio.gather(*tasks)

    # Run the main function
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

else:
    print("Invalid spam type.")
