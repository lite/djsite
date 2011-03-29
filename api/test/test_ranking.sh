#####api######

### game
#curl -i -H "Accept: application/json" http://192.168.1.113:8000/api/ranking

### score
#curl -u -i -H "Accept: application/json" http://192.168.1.113:8000/api/ranking/score/1

### gamerank
curl -i -H "Accept: application/json" http://192.168.1.107:8000/api/ranking/1

### add score
#curl -u lite:7u8i9o0p -i -H "Accept: application/json" -X POST http://192.168.1.113:8000/api/ranking/addscore -d "game=1&score=101"
# curl -i -H "Accept: application/json" -X POST http://192.168.1.113:8000/api/ranking/addscore/ -d "game=1&score=101"
