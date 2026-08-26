from typing import Iterable, Generator
from ...client_configs import PermissionRule
from ..namespace import Namespace

class PermissionChecker:
    def __init__(
        self,
        rules: Iterable[PermissionRule]
    ):
        self.super_groups: set[str] = set()
        self.super_users: set[str] = set()
        self.super_namespaces: set[Namespace] = set()
        self._rules: list[PermissionRule] = []

        for rule in rules:
            if rule.group_id is not None and rule.user_id is not None:
                super_namespace = Namespace(
                    group_id = rule.group_id,
                    user_id = rule.user_id
                )
                self.super_namespaces.add(super_namespace)
            elif rule.group_id is not None:
                self.super_groups.add(rule.group_id)
            elif rule.user_id is not None:
                self.super_users.add(rule.user_id)
            else:
                raise ValueError("PermissionRule must have at least one of super_group or super_user")

            self._rules.append(rule)

    def check(self, namespace: Namespace) -> bool:
        if namespace in self.super_namespaces:
            return True
        if namespace.group_id in self.super_groups:
            return True
        if namespace.user_id in self.super_users:
            return True
        return False

    def to_rules(self) -> list[PermissionRule]:
        return self._rules.copy()

    def copy(self) -> "PermissionChecker":
        return self.__class__(
            self._rules
        )