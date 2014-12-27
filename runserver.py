from glim import app
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # for fast template loading
    app.jinja_env.cache = {}
    app.run(host='0.0.0.0', port=port, debug=True)
