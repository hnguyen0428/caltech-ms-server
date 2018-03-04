import requests
from text_analyzer import analyze_audio

key = "04c74a871d624275914bfbbb65f57e0b"

search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"

def scrape_important(audioFile):

    important = []

    with open('./figures.txt', 'r') as source:
        for line in source:
            important.append(line.strip())

    timestamped_phrases = analyze_audio(audioFile)
    print(timestamped_phrases)

    timeline_annotations = []

    for time_start, keyPhrase_dict in timestamped_phrases:
        keyPhrases = keyPhrase_dict["keyPhrases"]
        for phrase in keyPhrases:
            words = map(lambda x: x.lower(), phrase.split(" ")[0])
            for word in words:
                if word in important:
                    link = search(phrase)
                    timeline_annotations.append((time_start, phrase, link))
                    break

    return timeline_annotations

def search(search_term):

    headers = {"Ocp-Apim-Subscription-Key": key}
    params = {"q": search_term, "textDecorations": True, "textFormat": "HTML", "responseFilter": ["Entities", "RelatedSearches", "Webpages", "Videos"]}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    print(search_results)

    return search_results['videos']['value'][0]['contentUrl']