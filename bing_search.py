import requests
from text_analyzer import analyze_audio
from conf import ROOT_FOLDER

key = "04c74a871d624275914bfbbb65f57e0b"

search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"

def scrape_important(audioFile):

    important = []

    with open(ROOT_FOLDER + 'figures.txt', 'r') as source:
        for line in source:
            important.append(line.strip())

    timestamped_phrases = analyze_audio(audioFile)

    timeline_annotations = []

    for time_start, keyPhrase_dict in timestamped_phrases:
        keyPhrases = keyPhrase_dict["keyPhrases"]
        done = False
        for phrase in keyPhrases:
            words = map(lambda x: x.lower(), phrase.split(" ")[0])
            for word in words:
                if word in important:
                    query, link = search(phrase)
                    timeline_annotations.append((time_start, query, link))
                    done = True
                    break
            if done:
                break

    return timeline_annotations

def search(search_term):

    headers = {"Ocp-Apim-Subscription-Key": key}
    params = {"q": search_term, "textDecorations": True, "textFormat": "HTML", "responseFilter": ["Entities", "RelatedSearches", "Webpages", "Videos"]}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    if 'videos' not in search_results:
        if 'webPages' not in search_results:
            return search_results['queryContext']['originalQuery'], "Nothing"
        return search_results['queryContext']['originalQuery'], search_results['webPages']['value'][0]['url']
    else:
        return search_results['queryContext']['originalQuery'], search_results['videos']['value'][0]['contentUrl']