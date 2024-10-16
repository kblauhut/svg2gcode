import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# Path to the Juicy G-code binary
JUICY_GCODE_PATH = "/app/juicy-gcode"  # Path to the Juicy G-code executable
GCODE_CONFIG_PATH = "/app/gcodeconfig.yml"  # Path to the G-code configuration file

@app.route('/convert', methods=['POST'])
def convert_svg_to_gcode():
    data = request.get_json()

    if 'svg' not in data:
        return jsonify({"error": "No SVG provided"}), 400

    svg_string = data['svg']

    # Write SVG string to a temporary file
    svg_file_path = '/app/temp.svg'
    with open(svg_file_path, 'w') as svg_file:
        svg_file.write(svg_string)

    # Log the content of the SVG file for debugging
    with open(svg_file_path, 'r') as svg_file:
        svg_content = svg_file.read()
        # print("SVG Content:", svg_content)  # Log the content

    # Run the Juicy G-code command
    try:
        command = [JUICY_GCODE_PATH, svg_file_path, '-f', GCODE_CONFIG_PATH]
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print("Juicy G-code output:", result.stdout.strip())  # Log the output

        return jsonify({"gcode": result.stdout.strip()})

    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": f"Failed to convert SVG to G-code: {str(e)}",
            "output": e.stdout.strip(),
            "stderr": e.stderr.strip()  # Capture standard error output
        }), 500

    finally:
        if os.path.exists(svg_file_path):
            os.remove(svg_file_path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
