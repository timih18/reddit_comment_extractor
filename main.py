import praw
import concurrent.futures
from datetime import datetime
from config import reddit, post

start_time = datetime.now()


def escape_xml(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def comment_handler(comment):
    comment_date = datetime.fromtimestamp(comment.created_utc)
    comment_author = comment.author
    comment_text = comment.body.encode('utf-8', errors='ignore').decode()
    return f'''  <comment>
    <date>{comment_date.strftime('%d-%m-%Y %H:%M:%S')}</date>
    <author>{comment_author.name if comment_author else '*Удаленный автор*'}</author>
    <text>{escape_xml(comment_text)}</text>
  </comment>'''


def scraper(post_id, flows=8):
    submission = reddit.submission(id=post_id)
    submission.comments.replace_more(limit=None)

    with open('data.xml', 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<comments>\n')

    with concurrent.futures.ThreadPoolExecutor(max_workers=flows) as executor:
        futures = {executor.submit(comment_handler, comment): comment for comment in submission.comments.list()}

        parsed_counter = 0
        error_counter = 0

        for elem in concurrent.futures.as_completed(futures):
            try:
                result = elem.result()
                with open('data.xml', 'a', encoding='utf-8') as f:
                    f.write(result + '\n')
                parsed_counter += 1
            except Exception as exception:
                error_counter += 1
                print(f'Ошибка: {exception}')

        with open('data.xml', 'a', encoding='utf-8') as f:
            f.write('</comments>')

    return [parsed_counter, error_counter]


response = scraper(post, flows=4)
end_time = datetime.now()

print(f'Извлечено записей: {response[0]}')
print(f'Ошибок: {response[1]}')
print(f'Время работы: {end_time - start_time}')
