from piston.handler import BaseHandler
from piston.utils import rc, throttle

from csrfhandler import CsrfHandler
from xml.etree.ElementTree import Element, SubElement, tostring
import socket
  
class MesgSendHandler(CsrfHandler):
    allowed_methods = ('POST', )
    
    def create(self, request):
        receivers = request.POST.getlist('receivers[]')
        message = request.POST['message']
        if message and receivers:
            top = Element('news')
            ele_msg = SubElement(top, 'message')
            ele_msg.text = message
            ele_receivers = SubElement(top, 'receivers')
            for phone in receivers:
                ele_receiver = SubElement(ele_receivers, 'receiver')
                ele_receiver.text = phone
            raw_data = tostring(top, 'UTF-8')
            #pdb.set_trace()          
            #print(raw_data)
            is_done = self.do_send(raw_data)
            if is_done:
                return {'status':0, "message": "Sent successfully."}
            else:
                return {'status':-1, "message": "Sorry, sent message failed."}
        else:
            return {'status':-2, "message": "Message or receivers is null."}
    
    def do_send(self, raw_data):
        # HOST = '192.168.1.100'    
        HOST = '127.0.0.1'  
        PORT = 20000
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            s.send(raw_data)
            data = s.recv(1024)
            s.close()
            return True
        except:
            return False

