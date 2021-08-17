from django.shortcuts import render, redirect
from .models import League, Team, Player
from django.db.models import Q, Count


from . import team_maker

def index(request):
	wichita = Team.objects.get(team_name='Vikings', location='Wichita')
	wichitall = wichita.all_players.all()
	wichitaid = [player.id for player in wichita.curr_players.all()]
	wichitaformer = [player for player in wichitall if player.id not in wichitaid]
	
	jacob = Player.objects.get(first_name='Jacob', last_name='Gray')
	jacoball = jacob.all_teams.all()
	jacobteams = [team for team in jacoball if jacob.curr_team.id not in jacoball]

	teams12 = Team.objects.annotate(Count('all_players')).filter(all_players__count__gt=12)
	
	players = Player.objects.annotate(Count('all_teams')).order_by('all_teams__count')

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
		"alexwyatt": Player.objects.filter(Q(first_name = 'Alexander') |Q(first_name = 'Wyatt')),
		"atlantics": Team.objects.filter(league__name = 'Atlantic Soccer Conference'),
		"bostonpenguins": Player.objects.filter(curr_team__location='Boston', curr_team__team_name='Penguins'),
		"internationalcbc": Player.objects.filter(curr_team__league__name='International Collegiate Baseball Conference'),
		"lopezfromleague": Player.objects.filter(last_name='Lopez', curr_team__league__name='American Conference of Amateur Football'),
		"footballplayers": Player.objects.filter(curr_team__league__sport='Football'),
		"teamsophia": Team.objects.filter(curr_players__first_name='Sophia'),
		"leaguesophia": League.objects.filter(teams__curr_players__first_name='Sophia'),
		"floresnotwr": Player.objects.filter(last_name='Flores').exclude(curr_team__team_name='Roughriders', curr_team__location='Washington'),
		"samuelevansteams": Team.objects.filter(all_players__first_name='Samuel', all_players__last_name='Evans'),
		"manitoba": Player.objects.filter(all_teams__team_name='Tiger-Cats', all_teams__location='Manitoba'),
		"wichitaformer": wichitaformer,
		"jacobteams": jacobteams,
		"joshuateams": Player.objects.filter(first_name='Joshua', all_teams__league__name='Atlantic Federation of Amateur Baseball Players'),
		"teams12": teams12,
		"players": players
	}	
	return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")
