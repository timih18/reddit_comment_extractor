from lxml import etree
from datetime import datetime


def extract_stats_from_comments(xml_file):
    tree = etree.parse(xml_file)
    root = tree.getroot()

    list_dates, word_counts = [], []
    count_deleted_comments = count_deleted_authors = 0

    for comment in root.xpath('//comment'):
        date_str = comment.find('date').text
        list_dates.append(datetime.strptime(date_str, '%d-%m-%Y %H:%M:%S'))

        author = comment.find('author').text
        if author and "*Удаленный автор*" in author:
            count_deleted_authors += 1

        text = comment.find('text')
        if text is not None and text.text is not None:
            if "[deleted]" in text.text:
                count_deleted_comments += 1
            else:
                cleaned_text = text.text.strip()
                word_counts.append(len(cleaned_text.split()))

    return word_counts, count_deleted_comments, count_deleted_authors, list_dates


def calculate_stats(word_counts):
    if not word_counts:
        return 0, 0, 0
    return min(word_counts), max(word_counts), sum(word_counts) / len(word_counts)


xml_file = "data.xml"
word_counts, count_deleted_comments, count_deleted_authors, list_dates = extract_stats_from_comments(xml_file)
min_words, max_words, avg_words = calculate_stats(word_counts)

print("Количество записей: 7867")
print(
    f"Диапазон дат: от {min(list_dates).strftime('%Y-%m-%d %H:%M:%S')} до {max(list_dates).strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Удаленных авторов: {count_deleted_authors}")
print(f"Минимальное количество слов: {min_words}")
print(f"Максимальное количество слов: {max_words}")
print(f"Среднее количество слов: {avg_words:.2f}")
print(f"Удаленных комментариев: {count_deleted_comments}")