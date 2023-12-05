"""Types used for django-rules type checking."""
from abc.collections import Sequence
from typing import Any, Protocol

if TYPE_CHECKING:
    from django.contrib.auth.models import Group


class RulesUser(Protocol):
    """
    A rules user mixes aspects of PermissionsMixin and AbstractUser.

    In reality, most django projects derive their User model from AbstractBaseUser
    and PermissionsMixin. Adding AbstractBaseUser as a type hint will mean
    the is_active boolean field not being available.

    On the other hand, directly using django-rules methods inside a django
    project, means that implementers will have to call certain django-rules
    methods using an AbstractUser, a model instance not available in most
    projects because AbstractUser is not subclassed. Otherwise there will be
    type checking problems.

    Therefore we aim for structural equality using a Protocol instead, and
    leave it to the implementer to ensure all properties are present in the
    User model that they use.
    """

    is_active: bool
    # We could define this as a models.ManyToManyField, but that would create
    # a transitive import problem -- Django typings would have to be available
    # in the Django application that uses django-rules
    groups: Sequence[Any]

    # Used for caching
    _group_names_cache: Sequence


PredicateFunction = Union[
    Callable[[RulesUser, Any], bool],
    Callable[[RulesUser], bool],
]
