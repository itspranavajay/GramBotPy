from .read_business_message import ReadBusinessMessage
from .delete_business_messages import DeleteBusinessMessages
from .set_business_account_name import SetBusinessAccountName

class BusinessMethodsMixin(
    ReadBusinessMessage,
    DeleteBusinessMessages,
    SetBusinessAccountName
):
    """Business account handling methods.
    
    This mixin includes methods related to managing business accounts,
    such as reading and deleting messages, and changing profile information.
    """
    pass 