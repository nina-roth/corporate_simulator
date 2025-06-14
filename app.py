import webview
import logging
from API.email_api import InboxAPI
from API.chat_api import ChatAPI

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger('corporate_simulator')
    
    # Enable webview debug mode
    webview.logger.level = logging.DEBUG

    api = {
        "email_inbox": InboxAPI(),
        "chat": ChatAPI()
    }
    
    logger.debug('Starting application...')
    window = webview.create_window(
        "Corporate Dashboard",
        "index.html",
        js_api=api
    )
    webview.start(debug=True)