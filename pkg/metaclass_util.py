from abc import ABCMeta
from typing import Type, Any, List, Dict, Union


def build_required_attributes_metaclass(required_attrs: List[Dict[str, Union[str, type]]]) -> Type[ABCMeta]:
    """クラス変数が定義されていないとエラーになるメタクラスを生成する。

    Args:
        *required_attrs: 必要なクラス変数名。

    Returns:
        RequiredAttributesMeta: メタクラス。

    See Also:
        https://stackoverflow.com/questions/22046369/enforcing-class-variables-in-a-subclass#answer-22047600
    """

    class RequiredAttributesMeta(ABCMeta):
        def __init__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]):
            super(RequiredAttributesMeta, cls).__init__(name, bases, namespace)

            missing_attrs = [attr for attr in required_attrs
                             if not hasattr(cls, attr['name']) or type(getattr(cls, attr['name'])) != attr['type']]
            if missing_attrs:
                s = 's' * (len(missing_attrs) != 1)
                joined_attrs = ', '.join(map(lambda x: f"'{x['name']}'", missing_attrs))
                raise AttributeError(f"class {name} requires attribute{s}: {joined_attrs}")

    return RequiredAttributesMeta
