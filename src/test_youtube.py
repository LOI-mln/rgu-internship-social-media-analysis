import yt_dlp

# Une vidéo au hasard (par exemple une vidéo sur Aberdeen ou RGU)
video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' # Tu peux changer l'URL

ydl_opts = {
    'quiet': True,
    'no_warnings': True,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        info = ydl.extract_info(video_url, download=False)
        print(f"--- Succès ! ---")
        print(f"Titre : {info.get('title')}")
        print(f"Vues : {info.get('view_count')}")
        print(f"Description : {info.get('description')}")
    except Exception as e:
        print(f"Erreur : {e}")