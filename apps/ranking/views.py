from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from datetime import datetime
from models import Game, Score
from forms import ScoreForm

def index(request):
    games = Game.objects.all()
    for game in games:
        game.scores = Score.objects.all().filter(game__exact=game).order_by('-score')[:10]
    return render_to_response('ranking/index.html', {'games':games}, context_instance=RequestContext(request))

def addscore(request, game_id):
    if request.method == 'POST':
        form = ScoreForm(request.POST)
        if form.is_valid():
            score = Score() 
            score.score = form.cleaned_data.get("score", "0")
            score.player = request.user
            score.game = get_object_or_404(Game, pk=game_id)
            score.date = datetime.now()
            score.save()
            return HttpResponseRedirect(reverse('ranking:index'))
    else:
        form = ScoreForm()
            
    return render_to_response('ranking/addscore.html', {'form':form, 'game_id':game_id}, context_instance=RequestContext(request))

