from django.db import models

class Player(models.Model):
    player_name = models.CharField(max_length=20,unique=True)

class GameSession(models.Model):
    game_code = models.CharField(max_length=6,unique=True)
    player = models.ForeignKey(Player,on_delete=models.CASCADE,related_name="owner")
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)


class FactoryCard(models.Model):
    card_code = models.CharField(max_length=4)
    cost = models.IntegerField()
    maximum_production = models.IntegerField()
    production_capacity = models.IntegerField()
    CHOICES = (('free_flow','free_flow'),('iodized','iodized'),('crude','crude'))
    factory_type = models.CharField(max_length=20,choices=CHOICES)
    def __str__(self):
        return self.card_code

class LabourCard(models.Model):
    card_code = models.CharField(max_length=4)
    cost = models.IntegerField()
    labour = models.IntegerField()
    def __str__(self):
        return self.card_code


class AutomationCard(models.Model):
    card_code = models.CharField(max_length=4)
    cost = models.IntegerField()
    capacity = models.IntegerField()
    def __str__(self):
        return self.card_code

class WellCard(models.Model):
    card_code = models.CharField(max_length=4)
    cost = models.IntegerField()
    capacity = models.IntegerField()
    def __str__(self):
        return self.card_code



class PayOutCard(models.Model):
    card_code = models.CharField(max_length=4)
    CHOICES = (('normal','normal'),('fire','fire'),('rain','rain'),('strike','strike'),('no_buyer','no_buyer'))
    free_flow_payout_type = models.CharField(max_length=20,choices=CHOICES)
    iodized_payout_type = models.CharField(max_length=20,choices=CHOICES)
    crude_payout_type = models.CharField(max_length=20,choices=CHOICES)
    free_flow_payout = models.IntegerField()
    iodized_payout = models.IntegerField()
    crude_payout  = models.IntegerField()
    def __str__(self):
        return self.card_code


class GamePlayer(models.Model):
    game = models.ForeignKey(GameSession,on_delete=models.CASCADE,related_name='game')
    player = models.ForeignKey(Player,on_delete=models.CASCADE,related_name='game_player')


class PlayerFactory(models.Model):
    player = models.ForeignKey(Player,on_delete=models.CASCADE) 
    game = models.ForeignKey(GameSession,on_delete=models.CASCADE)
    factory = models.ForeignKey(FactoryCard,on_delete=models.CASCADE)
    labour = models.ManyToManyField(LabourCard)
    well = models.ManyToManyField(WellCard)
    automation  = models.ManyToManyField(AutomationCard)


class PlayerPayout(models.Model):
    factory = models.ForeignKey(FactoryCard,on_delete=models.CASCADE) 
    wells = models.ManyToManyField(WellCard) 
    labours = models.ManyToManyField(LabourCard,null=True,blank=True)
    automations = models.ManyToManyField(AutomationCard,null=True,blank=True)
    payout = models.ForeignKey(PayOutCard,on_delete=models.CASCADE)

