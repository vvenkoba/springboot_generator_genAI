import os
from app import app

if __name__ == "__main__":
    # Azure App Service will provide the PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False) 