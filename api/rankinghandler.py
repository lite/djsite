from piston.handler import BaseHandler
from piston.utils import rc, throttle

from apps.ranking.models import Game, Score
from datetime import datetime
from csrfhandler import CsrfHandler

# ranking
class GameHandler(BaseHandler):
    allowed_methods = ('GET', )
    model = Game
    exclude = ()

class ScoreHandler(BaseHandler):
    allowed_methods = ('GET', )
    model = Score
    
    def read(self, request, score_id):
        score = Score.objects.get(pk=score_id)
        return score

class GameRankHandler(BaseHandler):
    allowed_methods = ('GET', )
    
    def read(self, request, game_id):
        game = Game.objects.get(pk=game_id)
        scores = Score.objects.all().filter(game__exact=game).order_by('-score')[:10]
        return {'scores': scores }

class AddScoreHandler(CsrfHandler):
    allowed_methods = ('POST', )
    
    # @throttle(5, 10*60) # allow 5 times in 10 minutes
    def create(self, request):
        # Create/POST code goes here. 
        if request.user.is_authenticated():
            game_id =  request.POST.get('game')       
            game = Game.objects.get(pk=game_id)
            if game:
                score = Score()
                score.game = game
                score.date = datetime.now()
                score.player = request.user.username
                score.score = request.POST.get('score')
                score.save()
                return score
