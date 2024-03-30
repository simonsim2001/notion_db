from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.post("/query-database/{database_id}")
async def query_database(database_id: str, api_key: str):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    data = {"page_size": 100}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        episodes = response.json().get('results', [])
        result = []
        for episode in episodes:
            text_entries = episode['properties'].get('Text', {}).get('rich_text', [])
            text_content = " ".join([entry['plain_text'] for entry in text_entries if entry.get('plain_text')])
            show_entries = episode['properties'].get('Show', {}).get('rich_text', [])
            show_title = " ".join([entry['plain_text'] for entry in show_entries if entry.get('plain_text')])
            result.append({"Podcast Title": show_title, "Episode Snippet": text_content})
        return result
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve data from Notion API")
