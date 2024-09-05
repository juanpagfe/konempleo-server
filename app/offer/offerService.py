
from app.baseController import ControllerBase
from app.offer.offerDTO import OfferCreateDTO, OfferSoftDelete, OfferUpdateDTO

from models.models import Offer

class ServiceOffer(ControllerBase[Offer, OfferCreateDTO, OfferUpdateDTO, OfferSoftDelete]): 
    ...

offerServices = ServiceOffer(Offer)