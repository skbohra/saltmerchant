from django.shortcuts import *
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse

from .models import *
import random 
import uuid 
from django.db.models import Avg, Count, Min, Sum
from .forms import *
from django.db.models.functions import Coalesce

'''
SALT MERCHANT

'''
def index(request):
    return render(request,'index.html')


def new_game(request):
    player = request.GET['player_name']
    player = Player(player_name=player)
    player.save()

    game_code = uuid.uuid4().hex[:6].upper()
    game = GameSession(player=player,game_code=game_code,status="active")
    game.save()

    

    request.session['game_code'] = game.game_code
    request.session['player'] = game.player.player_name
    
    game_player = GamePlayer(player=player,game=game)
    game_player.save()


    url = "/game/"
    return HttpResponseRedirect(url)


def add_factory(request):
    
    player = request.session['player']
    game_code = request.session['game_code']

    game = get_object_or_404(GameSession,game_code=game_code)
    player = get_object_or_404(Player,player_name=player)
   
    factory = request.GET['factory']
    factory = FactoryCard.objects.get(card_code=factory)


    wells  = request.GET['wells'].split(',')
    wells = WellCard.objects.filter(card_code__in=wells)
    automations = request.GET['automations'].split(',')
    automations = AutomationCard.objects.filter(card_code__in=automations)
    
    labours = request.GET['labours'].split(',')
    labours = LabourCard.objects.filter(card_code__in=labours)

    
    factory = PlayerFactory(factory=factory,player=player,game=game)
    factory.save()

    factory.well.add(*wells)
    factory.automation.add(*automations)
    factory.labour.add(*labours)
    factory.save()

    return HttpResponse("/dashboard/")


def join_game(request):
    player = request.GET['player_name']
    game = request.GET['game_code']
    
    game = get_object_or_404(GameSession,game_code=game)

    player = Player(player_name=player)
    player.save()



    game_player = GamePlayer(player=player,game=game)
    game_player.save()


    request.session['game_code'] = game.game_code
    request.session['player'] = player.player_name

    return HttpResponse("/dashboard/")


def dashboard(request):
    game = request.session['game_code']
    player = request.player['player']

    game_players = GamePlayer.objects.filter(game=game)
    
    reports = []
    for player in game_players:
        data = {}
        data['player'] = player
        data['factories'] = PlayerFactory.objects.filter(player=player,game=game)
        reports.append(data)




def payout(request):
    try:
        game = request.session['game_code']
        player = request.session['player']
    except:
        return HttpResponseRedirect("/new_game/")
    game = get_object_or_404(GameSession,game_code=game)
    player = get_object_or_404(Player,player_name=player)
    payout_code = request.GET['payout_card']
    
    payout_card = get_object_or_404(PayOutCard,card_code=payout_code)

    game_players = GamePlayer.objects.filter(game=game)
    reports = []
    print(game)
    print(game_players)
    for game_player in game_players:
        total_payout = 0 
        data = {}
        factories = PlayerFactory.objects.filter(game=game,player=game_player.player)
        print(factories)
        for player_factory in factories:
            print("here")
            factory = player_factory.factory
            wells = player_factory.well
            labours = player_factory.labour
            automations = player_factory.automation
            total_labours = 0 
            total_wells = 0
            total_autos = 0 

            for labour in labours.all():
                total_labours = total_labours + labour.labour
            for well in wells.all():
                total_wells = total_wells + well.capacity
            for auto in automations.all():
                total_autos = total_autos + auto.capacity

            labour_cost = labours.all().aggregate(total = Sum("cost"))['total']
            total_labours = total_labours + total_autos
            
            if total_labours > factory.maximum_production:
                total_labours = factory.maximum_production
            if total_wells > factory.maximum_production:
                total_wells = factory.maximum_production
            #if total_autos= factory.maximum_capacity:
            #    total_autos = factory.maximum_capacity:

            if total_labours < total_wells:
                production_capacity = total_labours
            else:
                production_capacity = total_wells

            if production_capacity > factory.maximum_production:
               production_capacity = factory.maximum_production
            
            print("----------------------")
            print(factory.factory_type)
            print(factory)
            if factory.factory_type == "free_flow": 
                payout = production_capacity/100 * payout_card.free_flow_payout
                payout = payout - labour_cost 
                total_payout = total_payout + payout
                print(production_capacity)
                print(payout_card.free_flow_payout)
                print(labour_cost)

            if factory.factory_type == "iodized": 
                payout = production_capacity/100 * payout_card.free_flow_payout
                payout = payout - labour_cost 
                total_payout = total_payout + payout

            if factory.factory_type == "crude": 
                payout = production_capacity/100 * payout_card.free_flow_payout
                payout = payout - labour_cost 
                total_payout = total_payout + payout


        

        data['player'] = player.player_name
        data['payout'] = total_payout 
        reports.append(data)
        print(reports)
    return JsonResponse({'data':reports})




 
def payout_calculation(request):
    
    form = PayOutForm()
    
    if request.method == "POST":
        form = PayOutForm(request.POST)
        if form.is_valid():
            
            payout_card = form.cleaned_data['payout']

            total_payout = 0 
            data = {}
            factory = form.cleaned_data['factory']
            wells = form.cleaned_data['wells'].all()
            labours = form.cleaned_data['labours'].all()
            automations = form.cleaned_data['automations'].all()
            
            total_labours = 0 
            total_wells = 0
            total_autos = 0 
            labour_cost = 0 
            for labour in labours:
                total_labours = total_labours + labour.labour
            for well in wells:
                total_wells = total_wells + well.capacity
            for auto in automations:
                total_autos = total_autos + auto.capacity

            labour_cost = labours.aggregate(total = Coalesce(Sum("cost"),0))['total']
            total_labours = total_labours + total_autos
            
            if total_labours > factory.maximum_production:
                total_labours = factory.maximum_production
            if total_wells > factory.maximum_production:
                total_wells = factory.maximum_production
            #if total_autos= factory.maximum_capacity:
            #    total_autos = factory.maximum_capacity:

            if total_labours < total_wells:
                production_capacity = total_labours
            else:
                production_capacity = total_wells
            
            print(total_wells)
            print(production_capacity)
            if production_capacity > factory.maximum_production:
               production_capacity = factory.maximum_production
            
            print("----------------------")
            print(factory.factory_type)
            print(factory)
            if factory.factory_type == "free_flow":
                if payout_card.free_flow_payout < 0:
                    total_payout = payout_card.free_flow_payout - labour_cost
                else:
                    payout = production_capacity/100 * payout_card.free_flow_payout
                    payout = payout - labour_cost 
                    total_payout = total_payout + payout
                    print(production_capacity)
                    print(payout_card.free_flow_payout)
                    print(labour_cost)

            if factory.factory_type == "iodized": 
                if payout_card.iodized_payout < 0:
                    total_payout = payout_card.iodized_payout - labour_cost
                
                else:
                    payout = production_capacity/100 * payout_card.iodized_payout
                    payout = payout - labour_cost 
                    total_payout = total_payout + payout

            if factory.factory_type == "crude": 
                if payout_card.crude_payout < 0:
                    total_payout = payout_card.crude_payout - labour_cost
                else:
                    payout = production_capacity/100 * payout_card.crude_payout
                    payout = payout - labour_cost 
                    total_payout = total_payout + payout



            data['payout'] = total_payout 
            if total_payout < 0:
                msg = "Pay To Bank"
                print(msg)
            else:
                msg = "Take From Bank" 
            total_payout = abs(total_payout)
            form = PayOutForm()
            return render(request,'payout_calculation.html',{'form':form,'payout':abs(total_payout),'msg': msg})

    return render(request,'payout_calculation.html',{'form':form})





        
