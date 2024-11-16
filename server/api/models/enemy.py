from server.api.models.base_response import BaseResponse
from server.api.models.creatures import CreatureModel


class EnemyResponse(BaseResponse):
    """
    Response model for creating or retrieving a enemy.
    Inherits from BaseResponse

    - `message`: A descriptive message about the action performed.
    - `enemy`: The actual enemy data, represented by the `CreatureModel`.
    """

    enemy: CreatureModel
