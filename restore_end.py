with open('index.html', 'r') as f:
    lines = f.readlines()

# The script deleted everything. Let's put back the audio nodes, body and html.
end_content = """        </div>
    </div>
    <script src="app.js?v=17"></script>
<!-- Haptic audio simulation nodes -->
    <audio id="sndTap" src="https://assets.mixkit.co/active_storage/sfx/2568/2568-84.wav" preload="auto"></audio>
    <audio id="sndConfirm" src="https://assets.mixkit.co/active_storage/sfx/2019/2019-84.wav" preload="auto"></audio>
    <audio id="sndAlert" src="https://assets.mixkit.co/active_storage/sfx/911/911-84.wav" preload="auto"></audio>

</body>
</html>
"""

with open('index.html', 'a') as f:
    f.write(end_content)

