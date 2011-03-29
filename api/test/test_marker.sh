#####api######

### marker
#curl -i -H "Accept: application/json" http://10.1.2.102:8000/api/location/
# "markers": [
#         {
#             "date": "2010-10-10 22:05:50", 
#             "phone": "", 
#             "message": "from nanjing", 
#             "longitude": "118.7000000000", 
#             "latitude": "32.0000000000"
#         }
#     ]
#     
### add marker
# curl -u admin:jsjt -i -H "Accept: application/json" -X POST http://192.168.1.107:8000/api/location/addmarker/ -d "phone=55555&latitude=32.01&longitude=118.69&message=from_api"
# curl -u lite:7u8i9o0p -i -H "Accept: application/json" -X POST http://10.1.2.102:8000/api/location/addmarker/ -d "phone=22222&latitude=31.99&longitude=118.71&message=from_api"
#curl -X POST http://10.1.2.102:8000/api/location/addmarker/ -d "phone=99999&latitude=123.234555&longitude=23.4324343&message=from_api&date=2010-10-16 17:07:34"
#curl -i -H -X POST http://192.168.1.106:8000/api/location/addmarker/ -d "phone=55555&latitude=32.01&longitude=118.69&message=from_api"

### del marker
#curl -u lite:7u8i9o0p -i -H "Accept: application/json" -X POST http://10.1.2.102:8000/api/location/delmarker/ -d "id=33&id=32&id=31&id=14&id=13"