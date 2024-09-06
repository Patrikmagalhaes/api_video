from flask import Flask, request, jsonify, send_file
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os

app = Flask(__name__)

@app.route('/download_audio', methods=['POST'])
def download_audio():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        # Baixar o áudio do YouTube
        yt = YouTube(url, on_progress_callback=on_progress)
  

        # Obter a stream de áudio de menor qualidade
        audio_streams = yt.streams.filter(only_audio=True).order_by('bitrate')  # Ordena pela taxa de bits
        lowest_quality_stream = audio_streams.first()  # Pega a stream de menor qualidade

        if not lowest_quality_stream:
            return jsonify({'error': 'No audio streams available'}), 404

        # Salvar como MP3 com um nome específico
        audio_file = lowest_quality_stream.download(filename="audio.mp3")  # Salva como audio.mp3

        return send_file(audio_file, as_attachment=True, download_name="audio.mp3")

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
