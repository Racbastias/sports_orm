from django.shortcuts import render, redirect
from .models import League, Team, Player
from django.db.models import Q

from . import team_maker

def index(request):
	context = {
		"leagues": League.objects.all(),
		"baseball": League.objects.filter(sport__contains='Baseball'),
		"women_leagues": League.objects.filter(name__contains='Women'),
		"allhockey": League.objects.filter(sport__contains='Hockey'),
		"nofootball": League.objects.exclude(sport__contains='Football'),
		"conference": League.objects.filter(name__contains='Conference'),
		"atlantic": League.objects.filter(name__contains='Atlantic'),
		"teams": Team.objects.all(),
		"dallas": Team.objects.filter(location='Dallas'),
		"raptors": Team.objects.filter(team_name__contains='Raptors'),
		"city": Team.objects.filter(location__icontains='City'),
		"firsT": Team.objects.filter(team_name__startswith='T'),
		"orderlocation": Team.objects.all().order_by("location"),
		"reverseorder": Team.objects.all().order_by("-team_name"),
		"players": Player.objects.all(),
		"cooper": Player.objects.filter(last_name = 'Cooper'),
		"joshua": Player.objects.filter(first_name = 'Joshua'),
		"notjoshua": Player.objects.filter(last_name = 'Cooper').exclude(first_name = 'Joshua'),
		"alexwyatt": Player.objects.filter(Q(first_name = 'Alexander') |Q(first_name = 'Wyatt'))
	}
	return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")