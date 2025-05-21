from .send_gift import SendGift
from .gift_premium_subscription import GiftPremiumSubscription

class GiftsMethodsMixin(
    SendGift,
    GiftPremiumSubscription
):
    """Gift handling methods.
    
    This mixin includes all methods related to sending gifts,
    such as sending regular gifts and gifting premium subscriptions.
    """
    pass 