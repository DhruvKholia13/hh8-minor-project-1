import asyncio
from aiosmtpd.controller import Controller

class DebuggingHandler:
    async def handle_DATA(self, server, session, envelope):
        print('\n' + '='*40)
        print('      📨 INCOMING EMAIL RECEIVED      ')
        print('='*40)
        print(f'From: {envelope.mail_from}')
        print(f'To: {envelope.rcpt_tos}')
        print('-'*40)
        print('Message Body:')
        # Decode the email content to show it in the console
        print(envelope.content.decode('utf8', errors='replace'))
        print('='*40 + '\n')
        return '250 Message accepted for delivery'

if __name__ == '__main__':
    # Run the server on localhost:1025
    controller = Controller(DebuggingHandler(), hostname='localhost', port=1025)
    controller.start()
    print("✅ Fake Email Server is running on localhost:1025...")
    print("   (Waiting for emails from main.py...)")
    
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass