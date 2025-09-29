from flask import Flask, render_template_string, request

app = Flask(__name__)

# Mock data
VALID_USERS = ['alice.smith', 'bob.jones', 'carol.wilson', 'dave.brown']
DOCKER_IMAGES = ['archival-basic', 'data-transfer', 'db-export', 'ftp-sync', 'Custom']

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Build-a-Server-Forge</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="text"], input[type="date"], input[type="number"], select, textarea {
            width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;
        }
        textarea { height: 80px; }
        .inline-group { display: flex; gap: 10px; align-items: center; }
        .inline-group input { flex: 1; }
        .inline-group select { flex: 0 0 80px; }
        .custom-docker { display: none; background: #f5f5f5; padding: 15px; border-radius: 4px; margin-top: 10px; }
        button { background: #007cba; color: white; padding: 12px 24px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #005a87; }
    </style>
    <script>
        function toggleCustomDocker() {
            const dockerSelect = document.getElementById('docker_image');
            const customDiv = document.getElementById('custom_docker_fields');
            customDiv.style.display = dockerSelect.value === 'Custom' ? 'block' : 'none';
        }
    </script>
</head>
<body>
    <h1>Build-a-Server Forge</h1>
    
    <form method="POST">
        <div class="form-group">
            <label>Software Pre-installed:</label>
            <div style="margin-left: 20px;">
                <label><input type="checkbox" name="software" value="imagemagick"> ImageMagick</label><br>
                <label><input type="checkbox" name="software" value="anaconda"> Anaconda</label><br>
                <label><input type="checkbox" name="software" value="jupyter"> Jupyter</label><br>
                <label><input type="checkbox" name="software" value="pandas"> pandas</label><br>
                <label><input type="checkbox" name="software" value="swift"> Swift client</label><br>
                <label><input type="checkbox" name="software" value="yt-dlp"> yt-dlp</label>
            </div>
        </div>
        
        <div class="form-group">
            <label for="userid">User ID:</label>
            <input type="text" id="userid" name="userid" value="current.user" readonly style="background: #f0f0f0;">
        </div>
        
        <div class="form-group">
            <label for="access_users">Who has access:</label>
            <select id="access_users" name="access_users" multiple size="4">
                {% for user in users %}
                <option value="{{ user }}" {% if user == 'current.user' %}selected{% endif %}>{{ user }}</option>
                {% endfor %}
            </select>
            <small>Hold Ctrl/Cmd to select multiple users</small>
        </div>
        
        <div class="form-group">
            <label for="project_name">Project Name:</label>
            <input type="text" id="project_name" name="project_name" required>
        </div>
        
        <div class="form-group">
            <label for="description">Description:</label>
            <textarea id="description" name="description" placeholder="Brief description of the archival project..."></textarea>
        </div>
        
        <div class="form-group">
            <label for="start_date">Project Start Date:</label>
            <input type="date" id="start_date" name="start_date" required>
        </div>
        
        <div class="form-group">
            <label for="end_date">Project End Date:</label>
            <input type="date" id="end_date" name="end_date">
            <small>Leave blank for ongoing projects</small>
        </div>
        
        <div class="form-group">
            <label for="cpu_cores">CPU Cores:</label>
            <input type="number" id="cpu_cores" name="cpu_cores" min="2" value="2" required>
        </div>
        
        <div class="form-group">
            <label for="memory_size">Memory Size:</label>
            <input type="number" id="memory_size" name="memory_size" min="2" value="2" step="0.1" required>
            <small>Minimum 2GB</small>
        </div>
        
        <div class="form-group">
            <label for="disk_size">Disk Size:</label>
            <div class="inline-group">
                <input type="number" id="disk_size" name="disk_size" min="1" value="10" required>
                <select id="disk_unit" name="disk_unit">
                    <option value="GB">GB</option>
                    <option value="TB">TB</option>
                </select>
            </div>
        </div>
        
        <div class="form-group">
            <label for="mount_path">Data Mount Path:</label>
            <input type="text" id="mount_path" name="mount_path" value="/data" placeholder="/data" required>
        </div>
        
        <div class="form-group">
            <label for="docker_image">Docker Image:</label>
            <select id="docker_image" name="docker_image" onchange="toggleCustomDocker()" required>
                <option value="">-- Select Image --</option>
                {% for image in images %}
                <option value="{{ image }}">{{ image }}</option>
                {% endfor %}
            </select>
            
            <div id="custom_docker_fields" class="custom-docker">
                <h4>Custom Docker Image Details</h4>
                
                <div class="form-group">
                    <label for="registry_url">Docker Registry URL:</label>
                    <input type="text" id="registry_url" name="registry_url" placeholder="https://registry.example.com">
                </div>
                
                <div class="form-group">
                    <label for="image_name_tag">Image Name:Tag:</label>
                    <input type="text" id="image_name_tag" name="image_name_tag" placeholder="myorg/archiver:latest">
                </div>
                
                <div class="form-group">
                    <label>
                        <input type="checkbox" id="registry_auth" name="registry_auth" value="1">
                        Registry Credentials Required
                    </label>
                </div>
            </div>
        </div>
        
        <button type="submit">Submit Deployment Request</button>
    </form>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def container_form():
    if request.method == 'POST':
        # Just dump form data for now
        return f"<h2>Form Submitted!</h2><pre>{dict(request.form)}</pre>"
    
    return render_template_string(HTML_TEMPLATE, users=VALID_USERS, images=DOCKER_IMAGES)

if __name__ == '__main__':
    app.run(debug=True)
