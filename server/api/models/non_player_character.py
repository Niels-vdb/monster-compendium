from server.api.models.base_response import BaseResponse
from server.api.models.creatures import CreatureModel


class NPCResponse(BaseResponse):
    """
    Response model for creating or retrieving an npc.
    Inherits from BaseResponse

    - `message`: A descriptive message about the action performed.
    - `npc`: The actual npc data, represented by the `CreatureModel`.
    """

    npc: CreatureModel
