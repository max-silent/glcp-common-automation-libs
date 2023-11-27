"""
Create role details data template
"""
from dataclasses import InitVar, dataclass, field

from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils


@dataclass
class RoleDetailsData:
    rand: InitVar[str] = RandomGenUtils.random_string_of_chars(7)
    role: str = field(init=False, default=f"{rand} role")
    description: str = field(init=False, default=f"{rand} description")

    def __post_init__(self, rand):
        self.role: str = f"{rand} role"
        self.description: str = f"{rand} description"
