import praw
import concurrent
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from config import reddit, post


start_time = datetime.now()

def comment_handler(comment):
    comment_date = datetime.fromtimestamp(comment.created_utc)
    comment_author = comment.author
    comment_text = comment.body.encode('utf-8', errors='ignore')
    return [comment_date.strftime('%d-%m-%Y %H:%M:%S'),
            comment_author.name if comment_author else '*Удаленный автор*',
            comment_text.decode()]


def scraper(post_id, flows = 8):
    submission = reddit.submission(id=post_id)
    submission.comments.replace_more(limit=None)

    with ThreadPoolExecutor(max_workers=flows) as executor:
        futures = {
            executor.submit(comment_handler, comment) : comment
            for comment in submission.comments.list()
        }

        parsed_counter = 0
        error_counter = 0
        for elem in concurrent.futures.as_completed(futures):
            try:
                result = elem.result()
                file = open('data.txt', 'a', encoding='utf-8')
                file.writelines(' // '.join(result))
                file.writelines('\n')
                file.writelines(100*'==' + '\n')
                file.close()
                parsed_counter += 1
            except Exception as exception:
                print(f'Ошибка: {exception}')
                error_counter += 1
        return [parsed_counter, error_counter]

response = scraper(post, flows=4)
end_time = datetime.now()
print(f'Извлечено записей: {response[0]}')
print(f'Количество ошибок: {response[1]}')
print(f'Время работы: {end_time - start_time}')
