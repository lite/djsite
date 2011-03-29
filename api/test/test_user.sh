#####api######

### login
#curl -i -X POST http://192.168.1.113:8000/api/accounts/login/ -d "username=lite&password=7u8i9o0p"
#curl -i -X POST http://192.168.1.113:8000/api/accounts/login/ -d "username=lite&password=123"

### register
#url -i -X POST http://192.168.1.113:8000/api/accounts/register/ -d "username=lite&password=123&email=test@hotmail.com&mobile=1234"
#curl -i -X POST http://192.168.1.113:8000/api/accounts/register/ -d "username=test&password=test&email=test@hotmail.com&mobile=1234"

### school
#curl -i http://192.168.1.113:8000/api/accounts/profile/school/2/
### grade
curl -i http://192.168.1.107:8000/api/accounts/profile/grade/2
### classes
curl -i http://192.168.1.107:8000/api/accounts/profile/classes/3/