"""ドメイン例外定義."""


class DomainError(Exception):
    """ドメイン層の基底例外クラス."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class AdGenerationError(DomainError):
    """広告文生成エラー."""

    pass


class InvalidInputError(DomainError):
    """不正な入力エラー."""

    pass